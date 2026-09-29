import os
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from processing.schema import ProblemRecord
from processing.scorer import score_all_records
from processing.tagger import tag_all_records
from processing.clusterer import cluster_problems
from processing.feasibility import evaluate_all_candidates

def generate_synthetic_records(count: int = 60):
    records = []
    topics = [
        ("food waste", "Bangalore marriage halls dump food waste and banquet surplus every night.", "Sustainability"),
        ("e-waste", "Informal e-waste recycling in Seelampur exposes workers to toxic fumes and acid burns.", "Environment"),
        ("air pollution", "Delhi severe AQI smog and vehicular pollution causing breathing difficulties in children.", "Environment"),
        ("water scarcity", "Bangalore tanker mafia charging exorbitant rates during acute groundwater scarcity.", "Environment"),
        ("student burnout", "Engineering students facing extreme pressure, lack of career counselling, and mental burnout.", "Social impact"),
        ("msme payment delays", "Small businesses and MSMEs suffering 90-day delayed payments on GST invoices.", "Business"),
    ]

    for i in range(count):
        t_idx = i % len(topics)
        t_name, t_desc, t_theme = topics[t_idx]
        rec = ProblemRecord(
            id=f"rec_syn_{i}",
            source="reddit" if i % 2 == 0 else "google_news",
            url=f"https://source.com/item/{i}",
            title=f"{t_name.title()} Issue #{i}: {t_desc[:40]}",
            text=f"{t_desc} Additional details on case #{i} affecting local community.",
            author_hash=f"user_{i}",
            score=10 + (i % 50),
            num_comments=i % 15,
            query=t_name,
            lang="en"
        )
        records.append(rec)
    return records

def test_clustering_deterministic_seed():
    records = generate_synthetic_records(60)
    score_all_records(records)
    tag_all_records(records)

    config = {
        "clustering": {
            "model_name": "all-MiniLM-L6-v2",
            "min_clusters": 4,
            "max_clusters": 8,
            "max_cluster_percentage": 0.30,
            "random_state": 42
        }
    }

    # Run twice with fixed seed 42
    candidates_1 = cluster_problems(records, config)
    candidates_2 = cluster_problems(records, config)

    assert len(candidates_1) == len(candidates_2)
    # Check that candidate titles and sizes match exactly
    for c1, c2 in zip(candidates_1, candidates_2):
        assert c1.size == c2.size
        assert c1.title == c2.title
        assert round(c1.rank_score, 2) == round(c2.rank_score, 2)

def test_no_cluster_exceeds_max_percentage():
    # 80 records where 50 are on same topic to test the re-split constraint
    records = generate_synthetic_records(40)
    # Add 40 heavily skewed records
    for i in range(40):
        records.append(
            ProblemRecord(
                id=f"skewed_{i}",
                source="reddit",
                url=f"https://source.com/skewed/{i}",
                title=f"Air pollution in Delhi smog #{i}",
                text=f"Severe air pollution smog in Delhi NCR affecting millions #{i}",
                author_hash=f"user_skew_{i}",
                score=20,
                num_comments=5,
                query="air pollution",
            )
        )
    
    total_posts = len(records)
    score_all_records(records)
    tag_all_records(records)

    config = {
        "clustering": {
            "model_name": "all-MiniLM-L6-v2",
            "min_clusters": 5,
            "max_clusters": 12,
            "max_cluster_percentage": 0.30,
            "random_state": 42
        }
    }

    candidates = cluster_problems(records, config)
    evaluate_all_candidates(candidates)

    print(f"\nTotal records: {total_posts}")
    for cand in candidates:
        pct = (cand.size / total_posts) * 100
        print(f"Cluster: '{cand.title[:35]}...' | Size: {cand.size} ({pct:.1f}%) | Theme: {cand.theme}")
        # Enforce max 30% (+ margin of 1 item for integer rounding on small sets)
        assert cand.size <= max(4, int(total_posts * 0.30) + 1), f"Cluster exceeded 30%: {cand.size}/{total_posts}"
        assert len(cand.representative_quotes) >= 1
        assert "Total" in cand.scorecard
        assert "Depth of pain" in cand.scorecard
