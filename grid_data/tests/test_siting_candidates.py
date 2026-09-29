import os
import sys
import csv
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
GRID_DATA_DIR = os.path.dirname(TEST_DIR)
WORKSPACE_DIR = os.path.dirname(GRID_DATA_DIR)

for p in [WORKSPACE_DIR, GRID_DATA_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from siting_analysis import evaluate_all_candidates, calculate_sustainability_score, CURRENT_CLUSTERS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_V2_PATH_1 = os.path.join(BASE_DIR, "output", "siting_relocation_candidates_v2.csv")
CSV_V2_PATH_ROOT = os.path.join(os.path.dirname(BASE_DIR), "siting_relocation_candidates_v2.csv")
CSV_V1_PATH_1 = os.path.join(BASE_DIR, "output", "siting_relocation_candidates.csv")
CSV_V1_PATH_ROOT = os.path.join(os.path.dirname(BASE_DIR), "siting_relocation_candidates.csv")

EXPECTED_COLUMNS_V2 = [
    "current_cluster",
    "candidate_name",
    "distance_km_approx",
    "workload_radius_category",
    "method",
    "re_share_pct",
    "solar_cf_pct",
    "wind_cf_pct",
    "water_stress_level",
    "sustainability_uplift_score",
    "net_score_after_distance_penalty",
    "source_url",
    "confidence",
    "notes",
    "proxy_flag",
    "original_net_score",
]

EXPECTED_CLUSTERS = [
    "Mumbai/Navi Mumbai",
    "Chennai",
    "Hyderabad",
    "Pune",
    "Delhi-NCR/Noida",
    "Bengaluru",
    "Vizag",
    "Kolkata",
]

@pytest.fixture(scope="module")
def candidates_v2_csv():
    import subprocess
    subprocess.run(["python", os.path.join(BASE_DIR, "siting_analysis.py")], check=True)
    assert os.path.exists(CSV_V2_PATH_1), f"Missing CSV at {CSV_V2_PATH_1}"
    assert os.path.exists(CSV_V2_PATH_ROOT), f"Missing CSV at {CSV_V2_PATH_ROOT}"
    with open(CSV_V2_PATH_1, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_schema_completeness_v2(candidates_v2_csv):
    with open(CSV_V2_PATH_1, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    assert header == EXPECTED_COLUMNS_V2, f"Header mismatch. Expected {EXPECTED_COLUMNS_V2}, got {header}"

def test_all_8_clusters_covered(candidates_v2_csv):
    clusters_found = set(r["current_cluster"] for r in candidates_v2_csv)
    for exp_cluster in EXPECTED_CLUSTERS:
        assert exp_cluster in clusters_found, f"Missing cluster {exp_cluster}"
        c_count = sum(1 for r in candidates_v2_csv if r["current_cluster"] == exp_cluster)
        assert c_count >= 2, f"Cluster {exp_cluster} has fewer than 2 candidate sites ({c_count})"

def test_no_duplicate_verdict_types(candidates_v2_csv):
    """
    Test (a): No cluster has both a named candidate and a 'no better option' row.
    Either a cluster has 1-3 named candidate rows, or exactly one 'no better option' row, never both.
    """
    for exp_cluster in EXPECTED_CLUSTERS:
        cluster_rows = [r for r in candidates_v2_csv if r["current_cluster"] == exp_cluster]
        has_named = any("no better option" not in r["candidate_name"].lower() for r in cluster_rows)
        has_no_better = any("no better option" in r["candidate_name"].lower() for r in cluster_rows)
        
        # Must not have both
        assert not (has_named and has_no_better), (
            f"Cluster {exp_cluster} contains both named candidate(s) and a 'no better option' row!"
        )

def test_proxy_flag_notes_and_confidence(candidates_v2_csv):
    """
    Test (b): Every row with proxy_flag=TRUE has '(state-level proxy...' in its notes,
    and confidence is downgraded from High to Medium.
    """
    for r in candidates_v2_csv:
        if r["proxy_flag"] == "TRUE":
            assert "(state-level proxy, not site-verified)" in r["notes"], (
                f"Row {r['candidate_name']} has proxy_flag=TRUE but lacks proxy disclaimer in notes: {r['notes']}"
            )
            assert not r["confidence"].startswith("High"), (
                f"Row {r['candidate_name']} has proxy_flag=TRUE but claims High confidence: {r['confidence']}"
            )
            assert "Medium" in r["confidence"], (
                f"Row {r['candidate_name']} has proxy_flag=TRUE but confidence is not Medium: {r['confidence']}"
            )

def test_neemrana_wind_cf_correction(candidates_v2_csv):
    """
    Test (c): The Neemrana row's wind_cf_pct is no longer a bare unflagged copy of a state average.
    Wind CF is Not Viable / 0.0%, original_net_score (39.50) is retained for traceability,
    and new net score is recomputed (~23.79).
    """
    neemrana_rows = [r for r in candidates_v2_csv if "Neemrana" in r["candidate_name"]]
    assert len(neemrana_rows) == 1, "Expected exactly 1 Neemrana candidate row"
    neemrana = neemrana_rows[0]

    # Wind CF check
    assert neemrana["wind_cf_pct"] in ["Not Viable", "0.0", "0"], (
        f"Neemrana wind_cf_pct should be Not Viable or 0.0, got {neemrana['wind_cf_pct']}"
    )
    
    # Traceability check
    assert float(neemrana["original_net_score"]) == pytest.approx(39.50, abs=0.1), (
        f"Expected original_net_score ~39.50, got {neemrana['original_net_score']}"
    )
    assert float(neemrana["net_score_after_distance_penalty"]) == pytest.approx(23.79, abs=0.1), (
        f"Expected recalculated net score ~23.79, got {neemrana['net_score_after_distance_penalty']}"
    )
    assert "corrected" in neemrana["notes"].lower() or "not viable" in neemrana["notes"].lower()

def test_source_and_method_integrity(candidates_v2_csv):
    for r in candidates_v2_csv:
        method = r["method"]
        assert method in ["named_research", "distance_rule_fallback"], f"Invalid method: {method}"
        if "no better option" not in r["candidate_name"].lower():
            assert r["source_url"].startswith("http"), f"Missing source URL for candidate: {r['candidate_name']}"
            assert r["confidence"].strip() != "", f"Missing confidence for candidate: {r['candidate_name']}"
        assert len(r["notes"]) >= 15, f"Notes too short for {r['candidate_name']}"

def test_distance_penalty_behavior():
    """Verify that changing penalty weight behaves monotonically and adjusts ranking."""
    results_zero = evaluate_all_candidates(penalty_weight=0.0)
    results_high = evaluate_all_candidates(penalty_weight=10.0)

    for r0, rh in zip(results_zero, results_high):
        assert r0["sustainability_uplift_score"] == rh["sustainability_uplift_score"]
        if r0["distance_km_approx"] > 0:
            assert r0["net_score_after_distance_penalty"] > rh["net_score_after_distance_penalty"], \
                f"Distance penalty failed to decrease net score for {r0['candidate_name']}"
        else:
            assert r0["net_score_after_distance_penalty"] == rh["net_score_after_distance_penalty"]

def test_water_stress_scoring():
    # Low water stress gets 20 pts, Medium 12 pts, High 4 pts
    score_low = calculate_sustainability_score(re_share_pct=50, solar_cf_pct=20, wind_cf_pct=20, water_stress="Low")
    score_med = calculate_sustainability_score(re_share_pct=50, solar_cf_pct=20, wind_cf_pct=20, water_stress="Medium")
    score_high = calculate_sustainability_score(re_share_pct=50, solar_cf_pct=20, wind_cf_pct=20, water_stress="High")
    assert score_low > score_med > score_high
    assert round(score_low - score_med, 2) == 8.0
    assert round(score_med - score_high, 2) == 8.0
