import logging
from typing import Any, Dict, List
from .base import BaseSource

logger = logging.getLogger(__name__)

class QuoraStubSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("quora", config, raw_cache_dir)
        self.reason = config.get("sources", {}).get("quora", {}).get(
            "reason", "disabled: needs auth or ToS risk"
        )

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        logger.info(f"[quora] Skipped: {self.reason}")
        return []

class TwitterStubSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("twitter", config, raw_cache_dir)
        self.reason = config.get("sources", {}).get("twitter", {}).get(
            "reason", "disabled: needs auth or ToS risk"
        )

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        logger.info(f"[twitter] Skipped: {self.reason}")
        return []
