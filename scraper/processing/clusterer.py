import re
import math
import logging
from typing import Any, Dict, List, Tuple
from collections import Counter
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from .schema import ProblemRecord

logger = logging.getLogger(__name__)

class ProblemCandidate:
    def __init__(
        self,
        cluster_id: int,
        title: str,
        theme: str,
        size: int,
        distinct_sources: int,
        sources_breakdown: Dict[str, int],
        avg_pain_score: float,
        growth_over_time: str,
        top_terms: List[str],
        representative_quotes: List[Dict[str, Any]],
        rank_score: float,
        records: List[ProblemRecord],
    ):
        self.cluster_id = cluster_id
        self.title = title
        self.theme = theme
        self.size = size
        self.distinct_sources = distinct_sources
        self.sources_breakdown = sources_breakdown
        self.avg_pain_score = avg_pain_score
        self.growth_over_time = growth_over_time
        self.top_terms = top_terms
        self.representative_quotes = representative_quotes
        self.rank_score = rank_score
        self.records = records
        self.scorecard: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cluster_id": self.cluster_id,
            "title": self.title,
            "theme": self.theme,
            "size": self.size,
            "distinct_sources": self.distinct_sources,
            "sources_breakdown": self.sources_breakdown,
            "avg_pain_score": round(self.avg_pain_score, 2),
            "growth_over_time": self.growth_over_time,
            "top_terms": self.top_terms,
            "representative_quotes": self.representative_quotes,
            "rank_score": round(self.rank_score, 2),
            "scorecard": self.scorecard,
        }

def get_embeddings(texts: List[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """Get vector embeddings using sentence-transformers, or fallback to TF-IDF."""
    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading sentence-transformer: {model_name}")
        model = SentenceTransformer(model_name)
        embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        return np.array(embeddings)
    except Exception as e:
        logger.warning(f"SentenceTransformer embedding failed ({e}). Falling back to TF-IDF vectors.")
        tfidf = TfidfVectorizer(max_features=300, stop_words="english")
        vectors = tfidf.fit_transform(texts).toarray()
        # Normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms

def extract_cluster_terms(cluster_texts: List[str], top_n: int = 5) -> List[str]:
    """Extract top descriptive terms using TF-IDF."""
    if not cluster_texts:
        return ["problem"]
    try:
        tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=200,
            ngram_range=(1, 2)
        )
        matrix = tfidf.fit_transform(cluster_texts)
        scores = np.asarray(matrix.sum(axis=0)).flatten()
        terms = np.array(tfidf.get_feature_names_out())
        top_indices = scores.argsort()[::-1][:top_n]
        return [terms[i] for i in top_indices if len(terms[i]) > 2]
    except Exception:
        return ["issue", "challenge"]

def generate_cluster_title(cluster_records: List[ProblemRecord], top_terms: List[str]) -> str:
    """Generate a clean, descriptive title for the cluster."""
    # Filter candidates to avoid meta chatter
    meta_words = {"circlejerk", "reddit", "karma", "upvote", "downvote", "mods", "subreddit", "sub"}
    
    meaningful_records = []
    for r in cluster_records:
        title_words = set(re.findall(r"\w+", r.title.lower()))
        if not title_words.intersection(meta_words) and len(r.title) >= 20:
            meaningful_records.append(r)
            
    candidate_pool = meaningful_records if meaningful_records else cluster_records
    
    # Pick the most specific and high-pain item
    best_item = max(candidate_pool, key=lambda r: (r.pain_score * 1.5 + (1 if any(t in r.title.lower() for t in top_terms[:3]) else 0)))
    raw_title = best_item.title
    
    # Clean title
    clean_title = re.sub(r"^(ask\s*reddit|serious|rant|psa|question|discussion|unpopular\s*opinion):\s*", "", raw_title, flags=re.I).strip()
    clean_title = re.sub(r"\[.*?\]|\(.*?\)", "", clean_title).strip()
    
    if len(clean_title) > 85:
        clean_title = clean_title[:82] + "..."

    return clean_title

def compute_growth(records: List[ProblemRecord]) -> str:
    """Calculate temporal concentration of posts."""
    timestamps = [r.created_at for r in records if r.created_at > 0]
    if len(timestamps) < 4:
        return "Stable / Emerging"
    
    timestamps.sort()
    midpoint = len(timestamps) // 2
    median_time = timestamps[midpoint]
    total_span = timestamps[-1] - timestamps[0]
    if total_span <= 0:
        return "Recent Spike"

    # Fraction occurring in recent half of time span
    cutoff = timestamps[0] + (total_span * 0.5)
    recent_count = sum(1 for t in timestamps if t >= cutoff)
    recent_ratio = recent_count / len(timestamps)

    if recent_ratio > 0.65:
        return f"+{int((recent_ratio - 0.5)*200)}% Surge (Recent)"
    elif recent_ratio < 0.35:
        return "Chronic / Historic"
    else:
        return "Steady / High Recurrence"

def cluster_problems(
    records: List[ProblemRecord],
    config: Dict[str, Any] = None
) -> List[ProblemCandidate]:
    """Cluster records deterministically and enforce max cluster size constraint."""
    if not records:
        return []

    cfg = config.get("clustering", {}) if config else {}
    model_name = cfg.get("model_name", "all-MiniLM-L6-v2")
    random_state = cfg.get("random_state", 42)
    max_pct = cfg.get("max_cluster_percentage", 0.30)
    min_k = cfg.get("min_clusters", 4)
    max_k = cfg.get("max_clusters", 12)

    total_n = len(records)
    if total_n <= 3:
        # Trivial single candidate
        k = 1
    else:
        k = max(min_k, min(max_k, total_n // 15))

    texts = [f"{r.title}. {r.text[:300]}" for r in records]
    embeddings = get_embeddings(texts, model_name=model_name)

    # Initial clustering
    k_current = min(k, total_n)
    kmeans = KMeans(n_clusters=k_current, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # Enforce max cluster percentage constraint (<30% of total)
    max_allowed = max(4, int(total_n * max_pct))
    
    # Check for clusters exceeding max_allowed
    re_cluster_attempts = 0
    while re_cluster_attempts < 3:
        counts = Counter(labels)
        oversized = [cid for cid, cnt in counts.items() if cnt > max_allowed]
        if not oversized or k_current >= min(total_n, max_k + 4):
            break
        # Increase k and recluster
        k_current += len(oversized) + 1
        k_current = min(k_current, total_n)
        kmeans = KMeans(n_clusters=k_current, random_state=random_state + re_cluster_attempts, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        re_cluster_attempts += 1

    # Group records by cluster label
    clusters_dict: Dict[int, List[Tuple[ProblemRecord, np.ndarray]]] = {}
    for idx, (rec, emb) in enumerate(zip(records, embeddings)):
        cid = int(labels[idx])
        rec.cluster_id = cid
        if cid not in clusters_dict:
            clusters_dict[cid] = []
        clusters_dict[cid].append((rec, emb))

    candidates: List[ProblemCandidate] = []

    for cid, items in clusters_dict.items():
        c_records = [it[0] for it in items]
        c_embs = np.array([it[1] for it in items])
        c_size = len(c_records)
        if c_size == 0:
            continue

        centroid = c_embs.mean(axis=0)
        # Distance to centroid for picking central representative quotes
        dists = np.linalg.norm(c_embs - centroid, axis=1)

        # Sources stats
        sources = [r.source for r in c_records]
        sources_breakdown = dict(Counter(sources))
        distinct_sources = len(sources_breakdown)

        # Average pain score
        avg_pain = sum(r.pain_score for r in c_records) / c_size

        # Theme by majority
        theme_counts = Counter(r.theme for r in c_records)
        cluster_theme = theme_counts.most_common(1)[0][0]

        # Top descriptive terms
        c_texts = [f"{r.title} {r.text}" for r in c_records]
        top_terms = extract_cluster_terms(c_texts, top_n=5)

        # Cluster title
        cluster_title = generate_cluster_title(c_records, top_terms)

        # Growth / temporal spread
        growth_str = compute_growth(c_records)

        # Select top 3 representative quotes (prioritize high pain score + central)
        scored_items = []
        for r, dist in zip(c_records, dists):
            # Combined ranking for quotes: pain_score / (1.0 + dist)
            quote_metric = r.pain_score / (1.0 + float(dist))
            scored_items.append((quote_metric, r))
        
        scored_items.sort(key=lambda x: x[0], reverse=True)
        quotes = []
        for _, qr in scored_items[:3]:
            quotes.append({
                "quote": qr.text[:220] + "..." if len(qr.text) > 220 else qr.text,
                "url": qr.url,
                "source": qr.source,
                "score": qr.score,
                "pain_score": qr.pain_score
            })

        # Rank formula: recurrence x pain x source diversity
        # Recurrence (size) * avg_pain_score * (1 + log2(1 + distinct_sources))
        diversity_multiplier = 1.0 + math.log2(1.0 + distinct_sources)
        rank_score = (c_size ** 0.85) * avg_pain * diversity_multiplier

        candidates.append(
            ProblemCandidate(
                cluster_id=cid,
                title=cluster_title,
                theme=cluster_theme,
                size=c_size,
                distinct_sources=distinct_sources,
                sources_breakdown=sources_breakdown,
                avg_pain_score=avg_pain,
                growth_over_time=growth_str,
                top_terms=top_terms,
                representative_quotes=quotes,
                rank_score=rank_score,
                records=c_records,
            )
        )

    # Sort candidates by rank_score descending
    candidates.sort(key=lambda c: c.rank_score, reverse=True)
    return candidates
