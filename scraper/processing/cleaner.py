import re
import hashlib
import logging
from typing import Any, Dict, List, Set, Tuple
from difflib import SequenceMatcher

from .schema import ProblemRecord

logger = logging.getLogger(__name__)

# Common bot / non-content markers
BOT_AUTHORS = {
    "automoderator", "bot", "reddit", "youtubechannel", "unknown", "[deleted]", "[removed]"
}

BOT_TEXT_PHRASES = [
    "i am a bot",
    "this action was performed automatically",
    "please contact the moderators of this subreddit",
    "your post has been removed",
    "this thread is archived",
    "[deleted]",
    "[removed]"
]

def hash_author(author: str) -> str:
    """Hash username to SHA-256 snippet for zero PII storage."""
    if not author or author.lower() in BOT_AUTHORS:
        return "anon_user"
    clean_auth = author.strip().lower()
    return "user_" + hashlib.sha256(clean_auth.encode("utf-8")).hexdigest()[:12]

def clean_text_content(text: str) -> str:
    """Clean text by stripping URLs, excessive emojis, markdown clutter, and normalization."""
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    # Remove HTML entities and tags
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    # Normalize quotes and dashes
    text = text.replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-")
    # Remove excessive symbols/emojis but keep punctuation and ₹
    text = re.sub(r"[^\w\s\.,!?'\"₹%\-\(\)/]", " ", text)
    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_bot_or_removed(title: str, text: str, author: str) -> bool:
    """Check if post is deleted, removed, or from a bot."""
    if author.lower() in BOT_AUTHORS or "bot" in author.lower():
        if author.lower() != "user":
            return True
    combined = f"{title} {text}".lower()
    for phrase in BOT_TEXT_PHRASES:
        if phrase in combined:
            return True
    return False

def is_english_or_hinglish(text: str) -> bool:
    """Ensure text is predominantly Latin script (covers English & Hinglish)."""
    if not text or len(text) < 10:
        return False
    # Check proportion of latin alphabetic characters + spaces + numbers
    latin_chars = len(re.findall(r"[a-zA-Z0-9\s\.,!?₹%'\-]", text))
    ratio = latin_chars / max(1, len(text))
    return ratio >= 0.70

def title_similarity(t1: str, t2: str) -> float:
    """Compute fuzzy ratio between two titles."""
    norm1 = re.sub(r"\W+", " ", t1.lower()).strip()
    norm2 = re.sub(r"\W+", " ", t2.lower()).strip()
    if not norm1 or not norm2:
        return 0.0
    if norm1 == norm2:
        return 1.0
    return SequenceMatcher(None, norm1, norm2).ratio()

def clean_and_normalize(raw_records: List[Dict[str, Any]]) -> List[ProblemRecord]:
    """Clean, filter, dedupe, and normalize raw records into ProblemRecord instances."""
    cleaned_records: List[ProblemRecord] = []
    seen_urls: Set[str] = set()
    seen_titles: List[str] = []

    for raw in raw_records:
        source = raw.get("source", "unknown")
        raw_id = str(raw.get("id", "")).strip()
        url = str(raw.get("url", "")).strip()
        raw_title = str(raw.get("title", "")).strip()
        raw_text = str(raw.get("text", "")).strip()
        raw_author = str(raw.get("author", "")).strip()

        # Skip if missing ID or URL
        if not raw_id:
            raw_id = hashlib.sha256(f"{url}_{raw_title}".encode()).hexdigest()[:16]
        if not url:
            url = f"https://source.local/{source}/{raw_id}"

        # URL Deduplication
        norm_url = url.split("?")[0].rstrip("/")
        if norm_url in seen_urls:
            continue

        # Check bot / removed
        if is_bot_or_removed(raw_title, raw_text, raw_author):
            continue

        # Clean text & title
        clean_title = clean_text_content(raw_title)
        clean_body = clean_text_content(raw_text)
        
        # Combine if body is minimal
        full_text = clean_body if len(clean_body) > len(clean_title) else f"{clean_title}. {clean_body}".strip()
        if len(full_text) < 15:
            continue

        # Check language
        if not is_english_or_hinglish(full_text):
            continue

        # Fuzzy title deduplication
        is_duplicate = False
        for prev_title in seen_titles:
            if title_similarity(clean_title, prev_title) > 0.85:
                is_duplicate = True
                break
        if is_duplicate:
            continue

        author_hash = hash_author(raw_author)
        score = int(raw.get("score", 0) or 0)
        num_comments = int(raw.get("num_comments", 0) or 0)
        created_at = int(raw.get("created_at", 0) or 0)
        query = str(raw.get("query", "")).strip()

        try:
            record = ProblemRecord(
                id=raw_id,
                source=source,
                url=url,
                title=clean_title or full_text[:80],
                text=full_text,
                author_hash=author_hash,
                created_at=created_at,
                score=score,
                num_comments=num_comments,
                query=query,
                lang="en"
            )
            cleaned_records.append(record)
            seen_urls.add(norm_url)
            seen_titles.append(clean_title)
        except Exception as e:
            logger.warning(f"Validation failed for record {raw_id}: {e}")

    logger.info(f"Normalisation: {len(raw_records)} raw records -> {len(cleaned_records)} validated records.")
    return cleaned_records
