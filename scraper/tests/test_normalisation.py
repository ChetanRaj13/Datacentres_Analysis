import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from processing.schema import ProblemRecord
from processing.cleaner import (
    clean_and_normalize,
    clean_text_content,
    hash_author,
    is_bot_or_removed,
    is_english_or_hinglish,
    title_similarity,
)

def test_schema_validation_success():
    rec = ProblemRecord(
        id="rec_123",
        source="reddit",
        url="https://reddit.com/r/india/comments/abc123",
        title="Excessive food waste in marriage halls",
        text="Why is there no law against throwing away kilos of food every night in Bangalore banquet halls?",
        author_hash="user_abc12345",
        created_at=1700000000,
        score=45,
        num_comments=12,
        query="food waste"
    )
    assert rec.id == "rec_123"
    assert rec.score == 45
    assert rec.num_comments == 12

def test_schema_validation_empty_id_raises():
    with pytest.raises(ValueError):
        ProblemRecord(
            id="",
            source="reddit",
            url="https://reddit.com",
            title="Title",
            text="Valid text here with enough content",
            author_hash="user_123"
        )

def test_schema_validation_empty_text_raises():
    with pytest.raises(ValueError):
        ProblemRecord(
            id="123",
            source="reddit",
            url="https://reddit.com",
            title="Title",
            text="",
            author_hash="user_123"
        )

def test_hash_author_anonymization():
    h1 = hash_author("my_real_username")
    h2 = hash_author("my_real_username")
    assert h1 == h2
    assert "my_real_username" not in h1
    assert h1.startswith("user_")
    assert hash_author("[deleted]") == "anon_user"
    assert hash_author("AutoModerator") == "anon_user"

def test_bot_and_removed_detection():
    assert is_bot_or_removed("Update", "I am a bot, and this action was performed automatically", "AutoModerator") is True
    assert is_bot_or_removed("[deleted by user]", "[removed]", "user1") is True
    assert is_bot_or_removed("Fresh veggies rot in mandi", "Farmers in Nashik face huge post-harvest loss.", "farmer_advocate") is False

def test_text_cleaning_urls_emojis():
    raw = "Struggling with water crisis in Bangalore! 😭😭 See https://example.com/news &amp; details. Cost ₹5000/tanker."
    cleaned = clean_text_content(raw)
    assert "https://" not in cleaned
    assert "😭😭" not in cleaned
    assert "₹5000/tanker" in cleaned or "₹5000" in cleaned
    assert "&amp;" not in cleaned

def test_deduplication_exact_and_fuzzy():
    raw_records = [
        {
            "id": "1",
            "source": "reddit",
            "url": "https://reddit.com/r/delhi/1",
            "title": "Severe Air Pollution in Delhi Schools",
            "text": "Kids are struggling to breathe due to AQI 450. Air purifiers are too expensive for middle class.",
            "author": "user_a",
            "score": 10,
        },
        {
            "id": "2",
            "source": "reddit",
            "url": "https://reddit.com/r/delhi/1?utm_source=share", # duplicate URL
            "title": "Severe Air Pollution in Delhi Schools",
            "text": "Kids are struggling to breathe due to AQI 450. Air purifiers are too expensive for middle class.",
            "author": "user_a",
            "score": 10,
        },
        {
            "id": "3",
            "source": "google_news",
            "url": "https://news.google.com/article2",
            "title": "Severe Air Pollution in Delhi Schools!", # fuzzy title duplicate
            "text": "Kids are coughing and struggling to breathe as AQI crosses 450.",
            "author": "NewsOrg",
            "score": 5,
        },
        {
            "id": "4",
            "source": "hackernews",
            "url": "https://news.ycombinator.com/item?id=99",
            "title": "E-waste recycling informal sector hazards in Seelampur",
            "text": "Workers burning motherboards with acid face severe lung and skin diseases.",
            "author": "hn_user",
            "score": 30,
        }
    ]

    cleaned = clean_and_normalize(raw_records)
    # Should keep only 2 unique records (delhi air pollution and e-waste)
    assert len(cleaned) == 2
    assert all(r.id and r.text for r in cleaned)
