import os
import time
import logging
from typing import Any, Dict, List
from dotenv import load_dotenv

from .base import BaseSource

load_dotenv()
logger = logging.getLogger(__name__)

class YouTubeSource(BaseSource):
    def __init__(self, config: Dict[str, Any], raw_cache_dir: str = "data/raw"):
        super().__init__("youtube", config, raw_cache_dir)
        self.yt_cfg = config.get("sources", {}).get("youtube", {})
        self.max_videos = self.yt_cfg.get("max_videos", 4)
        self.max_comments = self.yt_cfg.get("max_comments_per_video", 15)
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    def _search_api(self, topic: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        if not self.api_key:
            return results

        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{topic} India problem",
            "type": "video",
            "maxResults": min(self.max_videos, 10),
            "key": self.api_key,
        }
        data = self.fetch_url_with_retry(search_url, params=params)
        if not data or "items" not in data:
            return results

        for item in data.get("items", []):
            vid_id = item.get("id", {}).get("videoId")
            if not vid_id:
                continue
            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            desc = snippet.get("description", "")
            vid_url = f"https://www.youtube.com/watch?v={vid_id}"

            # Video itself
            results.append({
                "id": f"yt_vid_{vid_id}",
                "source": "youtube",
                "url": vid_url,
                "title": title,
                "text": f"{title}. {desc}",
                "author": snippet.get("channelTitle", "YouTubeChannel"),
                "created_at": int(time.time()),
                "score": 25,
                "num_comments": 10,
                "query": topic,
            })

            # Fetch top comments for video
            comments_url = "https://www.googleapis.com/youtube/v3/commentThreads"
            c_params = {
                "part": "snippet",
                "videoId": vid_id,
                "maxResults": self.max_comments,
                "order": "relevance",
                "key": self.api_key,
            }
            c_data = self.fetch_url_with_retry(comments_url, params=c_params)
            if c_data and "items" in c_data:
                for c_item in c_data["items"]:
                    c_snip = c_item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                    c_text = c_snip.get("textDisplay", "")
                    c_author = c_snip.get("authorDisplayName", "user")
                    c_likes = c_snip.get("likeCount", 0)
                    c_id = c_item.get("id", "")
                    results.append({
                        "id": f"yt_comm_{c_id}",
                        "source": "youtube",
                        "url": vid_url,
                        "title": f"Comment on: {title}",
                        "text": c_text,
                        "author": c_author,
                        "created_at": int(time.time()),
                        "score": c_likes,
                        "num_comments": 0,
                        "query": topic,
                    })

        return results

    def _search_ytdlp(self, topic: str, limit: int) -> List[Dict[str, Any]]:
        results = []
        cache_key = f"ytdlp_{topic}_{limit}"
        cached = self._read_cache(cache_key)
        if cached:
            return cached

        try:
            import yt_dlp

            search_query = f"ytsearch{self.max_videos}:{topic} India issue crisis"
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": "in_playlist",
                "skip_download": True,
                "get_comments": True,
                "max_comments": self.max_comments,
                "ignoreerrors": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not info or "entries" not in info:
                    return results

                for entry in info.get("entries", []):
                    if not entry:
                        continue
                    vid_id = entry.get("id", "")
                    title = entry.get("title", "")
                    desc = entry.get("description", "") or ""
                    channel = entry.get("uploader", "YouTubeCreator")
                    url = entry.get("url") or f"https://www.youtube.com/watch?v={vid_id}"

                    # Add video record
                    results.append({
                        "id": f"yt_v_{vid_id}",
                        "source": "youtube",
                        "url": url,
                        "title": title,
                        "text": f"{title}. {desc[:300]}",
                        "author": channel,
                        "created_at": int(time.time()),
                        "score": entry.get("view_count", 100) // 1000 if entry.get("view_count") else 10,
                        "num_comments": entry.get("comment_count", 0) or 0,
                        "query": topic,
                    })

                    # If comments were extracted
                    comments = entry.get("comments") or []
                    for c in comments[:self.max_comments]:
                        c_text = c.get("text", "")
                        if not c_text:
                            continue
                        results.append({
                            "id": f"yt_c_{c.get('id', '') or str(hash(c_text))}",
                            "source": "youtube",
                            "url": url,
                            "title": f"Comment on: {title}",
                            "text": c_text,
                            "author": c.get("author", "user"),
                            "created_at": c.get("timestamp") or int(time.time()),
                            "score": c.get("like_count", 0) or 0,
                            "num_comments": 0,
                            "query": topic,
                        })

            if results:
                self._write_cache(cache_key, results)

        except Exception as e:
            logger.warning(f"[youtube] yt-dlp search error: {e}")

        return results

    def search(self, topic: str, pain_phrases: List[str], limit: int = 50) -> List[Dict[str, Any]]:
        results = []
        if self.api_key:
            results = self._search_api(topic, limit)
        
        if not results:
            results = self._search_ytdlp(topic, limit)

        logger.info(f"[youtube] Collected {len(results)} items for topic '{topic}'.")
        return results[:limit]
