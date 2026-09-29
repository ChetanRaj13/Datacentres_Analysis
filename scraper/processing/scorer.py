import re
import math
import logging
from typing import List
from .schema import ProblemRecord

logger = logging.getLogger(__name__)

PAIN_PHRASES_WEIGHTS = {
    "why is there no": 1.0,
    "wish there was": 1.0,
    "frustrated with": 0.9,
    "struggling with": 0.9,
    "biggest problem": 0.9,
    "can't afford": 0.9,
    "cannot afford": 0.9,
    "no access to": 0.9,
    "how do i deal with": 0.8,
    "broken system": 0.8,
    "nightmare": 0.8,
    "waste": 0.7,
    "huge issue": 0.7,
    "pain point": 0.8,
    "terrible experience": 0.8,
    "unbearable": 0.8,
    "burnout": 0.8,
    "exhausted": 0.7,
    "helpless": 0.8,
    "scam": 0.7,
    "crisis": 0.7,
    "shortage": 0.8,
    "loss": 0.6,
    "struggle": 0.7,
    "problem": 0.5,
    "difficult": 0.5,
    "expensive": 0.6,
    "failed": 0.6,
}

PERSONAS = [
    r"\bstudents?\b", r"\bfarmers?\b", r"\bworkers?\b", r"\btenants?\b", r"\bdrivers?\b",
    r"\bdoctors?\b", r"\bengineers?\b", r"\bpatients?\b", r"\bmsmes?\b", r"\bsmall business\b",
    r"\bvendors?\b", r"\bgig worker\b", r"\bgig workers\b", r"\bdelivery (boy|agent|partner)s?\b",
    r"\bwomen\b", r"\bcommuters?\b", r"\bresidents?\b", r"\bcitizens?\b", r"\bmiddle class\b",
    r"\bcustomers?\b", r"\bfreshers?\b", r"\bgraduates?\b", r"\bchildren\b", r"\bparents?\b"
]

PLACES = [
    r"\bdelhi\b", r"\bmumbai\b", r"\bbangalore\b", r"\bbengaluru\b", r"\bchennai\b",
    r"\bkolkata\b", r"\bpune\b", r"\bhyderabad\b", r"\bgurgaon\b", r"\bnoida\b",
    r"\bahmedabad\b", r"\bjaipur\b", r"\blucknow\b", r"\bpatna\b", r"\branchi\b",
    r"\btier\s*[123]\b", r"\brural\b", r"\bindia\b", r"\bbihar\b", r"\bup\b",
    r"\bmaharashtra\b", r"\bkarnataka\b", r"\btamil nadu\b"
]

NUMBER_PATTERNS = [
    r"₹\s*\d+",
    r"rs\.?\s*\d+",
    r"\d+\s*%",
    r"\b\d+\s*(lakh|crore|k|cr|lakhs|crores)\b",
    r"\b\d+\s*(kg|tons?|litres?|liters?|hours?|hrs?|days?|months?|years?)\b",
    r"\b\d{2,}\b"
]

def calculate_pain_score(record: ProblemRecord, custom_pain_phrases: List[str] = None) -> float:
    """Calculate multi-dimensional pain score (0.0 to 10.0)."""
    text_lower = record.text.lower() + " " + record.title.lower()

    # 1. Pain signal score (0 to 1)
    pain_signal_sum = 0.0
    for phrase, weight in PAIN_PHRASES_WEIGHTS.items():
        if phrase in text_lower:
            pain_signal_sum += weight

    if custom_pain_phrases:
        for phrase in custom_pain_phrases:
            if phrase.lower() in text_lower:
                pain_signal_sum += 0.8

    pain_signal_norm = min(1.0, pain_signal_sum / 2.5)

    # 2. Engagement score (0 to 1)
    # log10(1 + score + 2 * num_comments)
    raw_eng = max(0, record.score) + 2 * max(0, record.num_comments)
    eng_log = math.log10(1 + raw_eng)
    engagement_norm = min(1.0, eng_log / 3.0)  # log10(1000) ~ 3.0

    # 3. Specificity score (0 to 1)
    has_persona = any(re.search(p, text_lower) for p in PERSONAS)
    has_place = any(re.search(p, text_lower) for p in PLACES)
    has_number = any(re.search(p, text_lower) for p in NUMBER_PATTERNS)

    specificity_norm = (0.4 * float(has_persona)) + (0.3 * float(has_place)) + (0.3 * float(has_number))

    # Combined composite (scaled 1.0 to 10.0)
    composite = (0.45 * pain_signal_norm) + (0.25 * engagement_norm) + (0.30 * specificity_norm)
    final_score = round(1.0 + (composite * 9.0), 2)  # maps to 1.0 - 10.0
    return final_score

def score_all_records(records: List[ProblemRecord], custom_pain_phrases: List[str] = None) -> List[ProblemRecord]:
    """Assign pain scores to all records."""
    for r in records:
        r.pain_score = calculate_pain_score(r, custom_pain_phrases)
    return records
