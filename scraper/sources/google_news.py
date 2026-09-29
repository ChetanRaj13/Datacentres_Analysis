import time
import urllib.parse
import logging
from typing import Any, Dict, List
from bs4 import BeautifulSoup
import feedparser

from .base import BaseSource

logger = logging.getLogger(__name__)

class GoogleNewsSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("google_news", config, raw_cache_dir)
        self.gn_cfg = config.get("sources", {}).get("google_news", {})
        self.hl = self.gn_cfg.get("hl", "en-IN")
        self.gl = self.gn_cfg.get("gl", "IN")
        self.ceid = self.gn_cfg.get("ceid", "IN:en")

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        queries = [
            f"{topic} India",
            f"{topic} crisis India",
            f"{topic} problem challenges India"
        ]

        for q in queries:
            if len(results) >= limit:
                break
            
            encoded_query = urllib.parse.quote_plus(q)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={self.hl}&gl={self.gl}&ceid={self.ceid}"
            
            # Fetch raw XML via BaseSource to utilize caching & retry
            res = self.fetch_url_with_retry(rss_url, is_json=False)
            if not res or "raw_text" not in res:
                continue

            feed = feedparser.parse(res["raw_text"])
            for entry in feed.entries:
                if len(results) >= limit:
                    break
                
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary_raw = entry.get("summary", "") or entry.get("description", "")
                
                # Clean html from summary
                soup = BeautifulSoup(summary_raw, "html.parser")
                clean_text = soup.get_text(separator=" ").strip()
                if not clean_text:
                    clean_text = title

                pub_time = 0
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    try:
                        pub_time = int(time.mktime(entry.published_parsed))
                    except Exception:
                        pub_time = int(time.time())
                else:
                    pub_time = int(time.time())

                entry_id = entry.get("id") or link

                results.append({
                    "id": entry_id,
                    "source": "google_news",
                    "url": link,
                    "title": title,
                    "text": f"{title}. {clean_text}",
                    "author": entry.get("source", {}).get("title", "GoogleNews"),
                    "created_at": pub_time,
                    "score": 10,  # Baseline score for news
                    "num_comments": 0,
                    "query": q,
                })

        logger.info(f"[google_news] Collected {len(results)} news articles for topic '{topic}'.")
        return results[:limit]
