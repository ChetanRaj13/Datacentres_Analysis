import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sources.reddit import RedditSource
from sources.hackernews import HackerNewsSource
from sources.google_news import GoogleNewsSource
from sources.youtube import YouTubeSource
from sources.stubs import QuoraStubSource, TwitterStubSource

CONFIG = {
    "subreddits": ["india", "mumbai", "bangalore", "delhi"],
    "sources": {
        "reddit": {"enabled": True, "max_posts_per_sub": 10},
        "hackernews": {"enabled": True, "max_posts": 25},
        "google_news": {"enabled": True, "max_posts": 25, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"},
        "youtube": {"enabled": True, "max_videos": 3, "max_comments_per_video": 10},
        "quora": {"enabled": False, "reason": "disabled: needs auth or ToS risk"},
        "twitter": {"enabled": False, "reason": "disabled: needs auth or ToS risk"},
    },
    "request": {
        "user_agent": "ProblemDiscoveryBot/1.0 (CaseCompetitionResearch; BIT Mesra Academic)",
        "delay_seconds_min": 0.2,
        "delay_seconds_max": 0.5,
        "timeout": 10,
        "max_retries": 2,
    }
}

def test_reddit_source():
    src = RedditSource(CONFIG, raw_cache_dir="data/raw_test")
    results = src.search("food waste", ["problem", "frustrated"], limit=25)
    assert isinstance(results, list)
    print(f"Reddit returned {len(results)} records")
    # Verify records schema
    if results:
        assert "id" in results[0]
        assert "title" in results[0]
        assert "url" in results[0]

def test_hackernews_source():
    src = HackerNewsSource(CONFIG, raw_cache_dir="data/raw_test")
    results = src.search("food waste", ["problem"], limit=25)
    assert isinstance(results, list)
    print(f"Hacker News returned {len(results)} records")
    assert len(results) >= 5
    assert "id" in results[0]
    assert "url" in results[0]

def test_google_news_source():
    src = GoogleNewsSource(CONFIG, raw_cache_dir="data/raw_test")
    results = src.search("food waste", ["crisis"], limit=25)
    assert isinstance(results, list)
    print(f"Google News returned {len(results)} records")
    assert len(results) >= 5
    assert "id" in results[0]
    assert "url" in results[0]

def test_stubs_disabled():
    quora = QuoraStubSource(CONFIG, raw_cache_dir="data/raw_test")
    twitter = TwitterStubSource(CONFIG, raw_cache_dir="data/raw_test")
    assert len(quora.search("food waste", [])) == 0
    assert len(twitter.search("food waste", [])) == 0
