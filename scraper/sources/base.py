import os
import json
import time
import random
import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import requests

logger = logging.getLogger(__name__)

class BaseSource(ABC):
    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        raw_cache_dir: str = "data/raw",
    ):
        self.name = name
        self.config = config
        self.raw_cache_dir = os.path.join(raw_cache_dir, name)
        os.makedirs(self.raw_cache_dir, exist_ok=True)
        
        req_cfg = config.get("request", {})
        self.user_agent = req_cfg.get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 ProblemDiscovery/1.0"
        )
        self.delay_min = req_cfg.get("delay_seconds_min", 1.0)
        self.delay_max = req_cfg.get("delay_seconds_max", 2.0)
        self.timeout = req_cfg.get("timeout", 15)
        self.max_retries = req_cfg.get("max_retries", 3)
        self.backoff_factor = req_cfg.get("backoff_factor", 2.0)
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        })

    def _get_cache_path(self, key: str) -> str:
        safe_key = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
        return os.path.join(self.raw_cache_dir, f"{safe_key}.json")

    def _read_cache(self, key: str) -> Optional[Any]:
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"[{self.name}] Loaded cached response for key: {key[:50]}...")
                return data
            except Exception as e:
                logger.warning(f"[{self.name}] Failed to read cache at {cache_path}: {e}")
        return None

    def _write_cache(self, key: str, data: Any):
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"[{self.name}] Failed to write cache to {cache_path}: {e}")

    def _sleep_throttle(self):
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)

    def fetch_url_with_retry(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_cache: bool = True,
        is_json: bool = True,
    ) -> Optional[Any]:
        cache_key = f"{url}?{sorted(params.items()) if params else ''}"
        if use_cache:
            cached = self._read_cache(cache_key)
            if cached is not None:
                return cached

        req_headers = self.session.headers.copy()
        if headers:
            req_headers.update(headers)

        backoff = 1.0
        for attempt in range(1, self.max_retries + 1):
            try:
                self._sleep_throttle()
                response = self.session.get(
                    url,
                    params=params,
                    headers=req_headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    if is_json:
                        try:
                            result = response.json()
                        except Exception:
                            result = {"raw_text": response.text}
                    else:
                        result = {"raw_text": response.text}
                        
                    if use_cache:
                        self._write_cache(cache_key, result)
                    return result
                
                elif response.status_code == 429:
                    logger.warning(
                        f"[{self.name}] Rate limit 429 encountered for {url}. Attempt {attempt}/{self.max_retries}. Backing off {backoff:.1f}s."
                    )
                    time.sleep(backoff)
                    backoff *= self.backoff_factor
                elif response.status_code in (403, 401):
                    logger.error(
                        f"[{self.name}] Access denied ({response.status_code}) for {url}. Check credentials or headers."
                    )
                    return None
                elif response.status_code == 404:
                    logger.warning(f"[{self.name}] Not found (404) for {url}.")
                    return None
                else:
                    logger.warning(
                        f"[{self.name}] HTTP {response.status_code} for {url}. Attempt {attempt}/{self.max_retries}."
                    )
                    time.sleep(backoff)
                    backoff *= self.backoff_factor

            except requests.exceptions.RequestException as e:
                logger.warning(f"[{self.name}] Request error on attempt {attempt}: {e}")
                time.sleep(backoff)
                backoff *= self.backoff_factor

        logger.error(f"[{self.name}] Failed to fetch {url} after {self.max_retries} attempts.")
        return None

    @abstractmethod
    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        """Search source for topic and pain phrases, return raw or semi-raw records."""
        pass
