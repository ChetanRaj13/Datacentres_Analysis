import logging
from typing import Any, Dict, List
from .base import BaseSource

logger = logging.getLogger(__name__)

class HackerNewsSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("hackernews", config, raw_cache_dir)
        self.hn_cfg = config.get("sources", {}).get("hackernews", {})

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        base_url = "https://hn.algolia.com/api/v1/search"
        
        queries = [
            topic,
            f"{topic} India",
            f"{topic} problem",
            f"{topic} issue"
        ]

        for q in queries:
            if len(results) >= limit:
                break
            
            hits_needed = min(30, limit - len(results))
            params = {
                "query": q,
                "tags": "story",
                "hitsPerPage": hits_needed
            }
            
            res_data = self.fetch_url_with_retry(base_url, params=params)
            if not res_data or "hits" not in res_data:
                continue

            for hit in res_data.get("hits", []):
                obj_id = hit.get("objectID")
                title = hit.get("title", "")
                text = hit.get("story_text", "") or title
                url = hit.get("url") or f"https://news.ycombinator.com/item?id={obj_id}"
                
                results.append({
                    "id": str(obj_id),
                    "source": "hackernews",
                    "url": url,
                    "title": title,
                    "text": text,
                    "author": hit.get("author", "unknown"),
                    "created_at": hit.get("created_at_i", 0),
                    "score": hit.get("points", 0) or 0,
                    "num_comments": hit.get("num_comments", 0) or 0,
                    "query": q,
                })

        logger.info(f"[hackernews] Collected {len(results)} items for topic '{topic}'.")
        return results[:limit]
