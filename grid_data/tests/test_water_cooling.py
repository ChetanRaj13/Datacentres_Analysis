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

CSV_PATH_DATA = os.path.join(WORKSPACE_DIR, "data", "water_cooling_subsidiary.csv")
CSV_PATH_ROOT = os.path.join(WORKSPACE_DIR, "water_cooling_subsidiary.csv")

EXPECTED_COLUMNS = [
    "cluster",
    "water_stress_level",
    "water_stress_source",
    "wue_basis",
    "demand_ml_low",
    "demand_ml_high",
    "priority_flag",
    "notes"
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
    "Jamnagar"
]

@pytest.fixture(params=[CSV_PATH_DATA, CSV_PATH_ROOT])
def water_rows(request):
    import subprocess
    subprocess.run(["python", os.path.join(GRID_DATA_DIR, "build_water_subsidiary.py")], check=True)
    assert os.path.exists(request.param), f"File missing at {request.param}"
    with open(request.param, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_water_schema_completeness(water_rows):
    """Verify all expected columns are present with non-empty values."""
    assert len(water_rows) == 9, f"Expected exactly 9 clusters, found {len(water_rows)}"
    for row in water_rows:
        for col in EXPECTED_COLUMNS:
            assert col in row, f"Column '{col}' missing from row {row.get('cluster')}"
            assert row[col].strip() != "", f"Column '{col}' is empty in row {row.get('cluster')}"

def test_all_9_clusters_covered(water_rows):
    """Verify all 9 clusters are present."""
    found_clusters = [r["cluster"] for r in water_rows]
    for c in EXPECTED_CLUSTERS:
        assert c in found_clusters, f"Cluster '{c}' missing from water dataset"

def test_water_stress_sources_and_proxies(water_rows):
    """Verify every cluster has a named source (CGWB or WRI) and no unverified claims."""
    for row in water_rows:
        src = row["water_stress_source"]
        assert "CGWB" in src or "WRI" in src, f"Source missing CGWB or WRI for {row['cluster']}"
        assert len(src) >= 20, f"Source too short for {row['cluster']}"

def test_wue_basis_label_transparency(water_rows):
    """Verify WUE basis is transparently labeled as an industry assumption applied uniformly."""
    for row in water_rows:
        basis = row["wue_basis"]
        assert "industry-standard assumption" in basis.lower(), (
            f"WUE basis must be labeled as industry assumption for {row['cluster']}"
        )
        assert "1.25" in basis, f"WUE assumption factor 1.25 missing from {row['cluster']}"

def test_water_demand_formula_consistency(water_rows):
    """Verify ML demand = GWh * 1.25 (matching the verified demand from Demand_Supply_Model)."""
    # GWh reference: Delhi: 871.18 / 2009.98; Bengaluru: 609.83 / 1463.93; Jamnagar: 5694.0 / 17082.0
    for row in water_rows:
        ml_low = float(row["demand_ml_low"])
        ml_high = float(row["demand_ml_high"])
        assert ml_low > 0, f"Invalid low demand for {row['cluster']}"
        assert ml_high >= ml_low, f"High demand must be >= low demand for {row['cluster']}"

        if row["cluster"] == "Delhi-NCR/Noida":
            assert ml_low == pytest.approx(1089.0, abs=1.0)
            assert ml_high == pytest.approx(2512.5, abs=1.0)
        elif row["cluster"] == "Bengaluru":
            assert ml_low == pytest.approx(762.3, abs=1.0)
            assert ml_high == pytest.approx(1829.9, abs=1.0)
        elif row["cluster"] == "Jamnagar":
            assert ml_low == pytest.approx(7117.5, abs=1.0)
            assert ml_high == pytest.approx(21352.5, abs=1.0)

def test_priority_clusters_and_desalination_handling(water_rows):
    """Verify top 3 priority clusters (Bengaluru, Delhi-NCR, Chennai) and coastal/desal handlings."""
    priority_map = {r["cluster"]: r["priority_flag"] for r in water_rows}
    
    # Top 3 High Priority
    assert priority_map["Bengaluru"] == "High Priority"
    assert priority_map["Delhi-NCR/Noida"] == "High Priority"
    assert priority_map["Chennai"] == "High Priority"

    # Jamnagar partial desal & Vizag coastal desal option
    assert "partial desal" in priority_map["Jamnagar"].lower() or "unconfirmed" in priority_map["Jamnagar"].lower()
    assert "coastal" in priority_map["Vizag"].lower() or "desal" in priority_map["Vizag"].lower()

def test_jamnagar_desal_scope_honesty(water_rows):
    """
    Verify Jamnagar row's notes field does NOT claim full-campus 100% desalination,
    and explicitly limits the verified claim to the 168 MW Meta anchor facility.
    """
    jamnagar_row = next((r for r in water_rows if r["cluster"] == "Jamnagar"), None)
    assert jamnagar_row is not None, "Jamnagar row missing"

    notes = jamnagar_row["notes"]
    src = jamnagar_row["water_stress_source"]

    # Must explicitly state 168 MW Meta anchor
    assert "168 MW" in notes or "168MW" in notes, f"Expected 168 MW Meta scope in notes: {notes}"
    assert "Meta" in notes, f"Expected Meta anchor reference in notes: {notes}"
    
    # Must flag the remaining 832 MW / 2,832 MW as unconfirmed
    assert "832" in notes, f"Expected unconfirmed 832 MW reference in notes: {notes}"
    assert "2,832" in notes or "2832" in notes, f"Expected unconfirmed 2,832 MW reference in notes: {notes}"
    assert "unconfirmed" in notes.lower() or "not independently confirmed" in notes.lower()

    # Must NOT claim 100% campus-wide desalination
    assert "100% captive seawater desalination" not in notes.lower(), "Notes must not claim full-campus 100% desal"
    assert "zero municipal" not in notes.lower(), "Notes must not assert zero municipal draw for entire campus"
