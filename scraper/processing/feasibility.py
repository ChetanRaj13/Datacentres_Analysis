import re
from typing import List
from .clusterer import ProblemCandidate

SATURATED_SOLUTIONS = [
    "swiggy", "zomato", "uber", "ola", "amazon", "flipkart", "cred",
    "paytm", "zepto", "blinkit", "urban company", "cult.fit"
]

INFRASTRUCTURE_HEAVY = [
    "dam", "nuclear", "highway", "metro", "airport", "coal plant", "satellite", "railway network"
]

def score_candidate_feasibility(candidate: ProblemCandidate) -> ProblemCandidate:
    """Generate 1-5 scorecard aligned to Section 9 of CASE_COMP_CONTEXT.md."""
    cluster_text = " ".join([f"{r.title} {r.text}" for r in candidate.records]).lower()

    # 1. Depth of pain (1-5)
    # avg_pain_score is on a 1-10 scale
    depth_pain = min(5, max(1, round(candidate.avg_pain_score / 2.0)))

    # 2. Data available (1-5)
    # High if covered by Google News, HN, multiple sources
    news_count = candidate.sources_breakdown.get("google_news", 0)
    if candidate.distinct_sources >= 3 or news_count >= 3:
        data_avail = 5
    elif candidate.distinct_sources >= 2 or news_count >= 1:
        data_avail = 4
    else:
        data_avail = 3

    # 3. Novel angle (1-5)
    # Fewer mentions of saturated tech giants = higher novelty
    saturated_hits = sum(1 for brand in SATURATED_SOLUTIONS if brand in cluster_text)
    if saturated_hits == 0:
        novel_angle = 5
    elif saturated_hits <= 2:
        novel_angle = 4
    else:
        novel_angle = 3

    # 4. Feasible in ~6 mo (1-5)
    # Software, aggregation, decentralized or campus/SME pilots score higher than heavy civil infra
    is_heavy_infra = any(kw in cluster_text for kw in INFRASTRUCTURE_HEAVY)
    if is_heavy_infra:
        feasibility_6mo = 2
    else:
        # Default high feasibility for agile / intervention-based solutions
        feasibility_6mo = 4 if candidate.size >= 5 else 3

    # 5. Measurable impact (1-5)
    # Presence of quantifiable metrics (%, kg, ₹, time, people)
    has_metrics = len(re.findall(r"(₹|\bkg\b|\btons?\b|%|\blakhs?\b|\bcrores?\b|\bhours?\b)", cluster_text))
    if has_metrics >= 5:
        measurable_impact = 5
    elif has_metrics >= 2:
        measurable_impact = 4
    else:
        measurable_impact = 3

    total_score = depth_pain + data_avail + novel_angle + feasibility_6mo + measurable_impact

    candidate.scorecard = {
        "Candidate": candidate.title,
        "Depth of pain": depth_pain,
        "Data available": data_avail,
        "Novel angle": novel_angle,
        "Feasible in ~6 mo": feasibility_6mo,
        "Measurable impact": measurable_impact,
        "Total": total_score,
    }

    return candidate

def evaluate_all_candidates(candidates: List[ProblemCandidate]) -> List[ProblemCandidate]:
    """Evaluate feasibility scorecard for all candidates."""
    for cand in candidates:
        score_candidate_feasibility(cand)
    return candidates
