import os
import time
import logging
import urllib.parse
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup
import feedparser
from dotenv import load_dotenv

from .base import BaseSource

load_dotenv()
logger = logging.getLogger(__name__)

class RedditSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("reddit", config, raw_cache_dir)
        self.subreddits = config.get("subreddits", [
            "india", "mumbai", "bangalore", "delhi", "IndiaSpeaks",
            "personalfinanceindia", "developersIndia", "Indian_Academia", "IndianStockMarket"
        ])
        self.reddit_cfg = config.get("sources", {}).get("reddit", {})
        self.max_per_sub = self.reddit_cfg.get("max_posts_per_sub", 15)
        
        # Check for PRAW credentials
        self.praw_client = None
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT", self.user_agent)
        
        if client_id and client_secret:
            try:
                import praw
                self.praw_client = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent
                )
                logger.info("[reddit] Initialized authenticated PRAW client.")
            except Exception as e:
                logger.warning(f"[reddit] Failed to initialize PRAW: {e}. Falling back to public feeds.")

    def _search_rss_endpoint(self, subreddit: Optional[str], query: str, limit: int) -> List[Dict[str, Any]]:
        """Fetch Reddit public search via official RSS feed (bypasses 403 blocks on JSON)."""
        encoded_query = urllib.parse.quote_plus(query)
        if subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/search.rss?q={encoded_query}&restrict_sr=1&sort=relevance"
        else:
            url = f"https://www.reddit.com/search.rss?q={encoded_query}&sort=relevance"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res_data = self.fetch_url_with_retry(url, headers=headers, is_json=False)
        if not res_data or "raw_text" not in res_data:
            return []

        feed = feedparser.parse(res_data["raw_text"])
        posts = []
        for entry in feed.entries:
            if len(posts) >= limit:
                break
            
            title = entry.get("title", "")
            link = entry.get("link", "")
            raw_content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
            
            # Clean HTML from Reddit RSS summary
            soup = BeautifulSoup(raw_content, "html.parser")
            # Remove reddit link tables
            clean_text = soup.get_text(separator=" ").strip()
            
            author = entry.get("author", "redditor")
            post_id = entry.get("id", link)
            
            pub_time = int(time.time())
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    pub_time = int(time.mktime(entry.published_parsed))
                except Exception:
                    pass

            posts.append({
                "id": post_id,
                "source": "reddit",
                "subreddit": subreddit or "all",
                "url": link,
                "title": title,
                "text": f"{title}. {clean_text}" if len(clean_text) > 10 else title,
                "author": author,
                "created_at": pub_time,
                "score": 15,  # Estimated baseline engagement
                "num_comments": 8,
                "query": query,
            })

        return posts

    def _search_praw(self, subreddit_name: str, query: str, limit: int) -> List[Dict[str, Any]]:
        posts = []
        try:
            sub = self.praw_client.subreddit(subreddit_name)
            for submission in sub.search(query, sort="relevance", time_filter="year", limit=limit):
                posts.append({
                    "id": submission.id,
                    "source": "reddit",
                    "subreddit": subreddit_name,
                    "url": f"https://reddit.com{submission.permalink}",
                    "title": submission.title,
                    "text": submission.selftext or submission.title,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "created_at": submission.created_utc,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "query": query,
                })
        except Exception as e:
            logger.warning(f"[reddit] PRAW search error in r/{subreddit_name}: {e}")
        return posts

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        queries = [
            topic,
            f"{topic} problem",
            f"{topic} Bangalore",
            f"{topic} Mumbai",
            f"{topic} Delhi"
        ]

        for sub in self.subreddits[:4]:  # Top relevant subreddits
            if len(results) >= limit:
                break
            for q in queries[:2]:
                if len(results) >= limit:
                    break
                sub_limit = min(self.max_per_sub, limit - len(results))
                if self.praw_client:
                    sub_posts = self._search_praw(sub, q, sub_limit)
                else:
                    sub_posts = self._search_rss_endpoint(sub, q, sub_limit)
                results.extend(sub_posts)

        # Broad query across Reddit India if needed
        if len(results) < 15:
            logger.info(f"[reddit] Broadening search across Reddit for query: {topic}")
            broad_posts = self._search_rss_endpoint(None, f"{topic} India problem", limit=min(30, limit - len(results)))
            results.extend(broad_posts)

        logger.info(f"[reddit] Collected {len(results)} posts for topic '{topic}'.")
        return results[:limit]
