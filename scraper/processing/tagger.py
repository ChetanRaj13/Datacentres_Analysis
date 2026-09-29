import os
import re
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

from .schema import ProblemRecord

load_dotenv()
logger = logging.getLogger(__name__)

THEME_KEYWORDS: Dict[str, List[str]] = {
    "Sustainability": [
        "food waste", "waste segregation", "recycl", "circular economy", "packaging",
        "post-harvest", "cold storage", "compost", "biodegradable", "upcycling",
        "energy cost", "solar", "renewable", "resource efficiency", "spoilage", "food surplus"
    ],
    "Environment": [
        "air pollution", "aqi", "smog", "water scarcity", "groundwater", "plastic",
        "e-waste", "toxic", "stubble burning", "climate", "carbon", "landfill",
        "river", "ocean", "heatwave", "dust", "effluent", "drainage", "sewage"
    ],
    "Social impact": [
        "mental health", "burnout", "student", "depression", "suicide", "coaching",
        "exam pressure", "gig worker", "delivery", "swiggy", "zomato", "driver",
        "public transport", "healthcare", "hospital", "tenant", "women safety", "poverty",
        "jobless", "unemployment", "wage", "harassment", "education"
    ],
    "Business": [
        "msme", "small business", "gst", "working capital", "cash flow", "credit",
        "invoice", "payment delay", "vendor", "retail", "supply chain", "logistics",
        "margin", "startup", "stock market", "compliance", "taxation", "inventory", "b2b"
    ]
}

def tag_record_rules(record: ProblemRecord) -> str:
    """Classify theme using keyword rules."""
    text_lower = f"{record.query} {record.title} {record.text}".lower()
    scores = {theme: 0.0 for theme in THEME_KEYWORDS}

    for theme, keywords in THEME_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                # Multi-word phrases carry more domain specificity
                word_factor = len(kw.split()) * 1.5
                pos_weight = 3.0 if kw in record.query.lower() else (2.0 if kw in record.title.lower() else 1.0)
                scores[theme] += pos_weight * word_factor

    # If no keyword matches, infer from topic/query default
    best_theme = max(scores, key=scores.get)
    if scores[best_theme] == 0:
        if any(w in text_lower for w in ["pollut", "water", "air", "green"]):
            return "Environment"
        elif any(w in text_lower for w in ["waste", "food", "energy", "solar"]):
            return "Sustainability"
        elif any(w in text_lower for w in ["money", "cost", "msme", "gst", "profit", "shop"]):
            return "Business"
        else:
            return "Social impact"

    return best_theme

def extract_rule_problem_statement(record: ProblemRecord) -> str:
    """Extract a concise one-line problem statement using pattern heuristics."""
    title = record.title.strip()
    if any(q in title.lower() for q in ["why", "how", "problem", "issue", "struggle", "crisis", "facing"]):
        return title[:120]
    
    # Fallback to topic + key observation
    return f"Issue regarding {record.query or 'real-world challenge'}: {title[:90]}"

def tag_and_extract_llm(records: List[ProblemRecord], api_key: Optional[str] = None) -> List[ProblemRecord]:
    """Tag records and extract problem statements using Anthropic API."""
    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        logger.warning("No ANTHROPIC_API_KEY found. Using rule-based tagger.")
        return [tag_record_with_rules(r) for r in records]

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        
        # Batch in chunks of 10 to minimize latency & token usage
        batch_size = 10
        for i in range(0, len(records), batch_size):
            chunk = records[i:i+batch_size]
            prompt_items = []
            for idx, r in enumerate(chunk):
                prompt_items.append(
                    f"[{idx+1}] Title: {r.title}\nText: {r.text[:250]}\nQuery: {r.query}"
                )
            
            prompt = (
                "You are an expert case competition researcher. For each item below, determine:\n"
                "1. Theme: Exactly one of [Sustainability, Environment, Social impact, Business]\n"
                "2. One-line Problem Statement (max 15 words describing root pain)\n\n"
                "Format strictly as JSON array of objects:\n"
                '[{"index": 1, "theme": "...", "problem_statement": "..."}]\n\n'
                + "\n\n".join(prompt_items)
            )

            try:
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    temperature=0.0,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
                import json
                # Extract json
                json_match = re.search(r"\[\s*\{.*\}\s*\]", content, re.DOTALL)
                if json_match:
                    items = json.loads(json_match.group(0))
                    for it in items:
                        c_idx = it.get("index", 1) - 1
                        if 0 <= c_idx < len(chunk):
                            theme_val = it.get("theme", "").strip()
                            if theme_val in THEME_KEYWORDS:
                                chunk[c_idx].theme = theme_val
                            chunk[c_idx].problem_statement = it.get("problem_statement")
                else:
                    for r in chunk:
                        tag_record_with_rules(r)
            except Exception as e:
                logger.warning(f"LLM tagging batch failed: {e}. Falling back to rules for batch.")
                for r in chunk:
                    tag_record_with_rules(r)

    except Exception as e:
        logger.warning(f"Anthropic SDK error: {e}. Falling back to rules.")
        for r in records:
            tag_record_with_rules(r)

    return records

def tag_record_with_rules(record: ProblemRecord) -> ProblemRecord:
    """Apply rule-based tagging and problem statement extraction."""
    record.theme = tag_record_rules(record)
    if not record.problem_statement:
        record.problem_statement = extract_rule_problem_statement(record)
    return record

def tag_all_records(records: List[ProblemRecord], use_llm: bool = False) -> List[ProblemRecord]:
    """Tag all records according to config or flag."""
    if use_llm:
        return tag_and_extract_llm(records)
    for r in records:
        tag_record_with_rules(r)
    return records
