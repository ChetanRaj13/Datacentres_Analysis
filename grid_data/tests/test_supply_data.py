import os
import csv
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_CSV = os.path.join(BASE_DIR, "output", "cluster_supply_data.csv")
GAPS_MD = os.path.join(BASE_DIR, "output", "gaps.md")

EXPECTED_COLUMNS = [
    "cluster",
    "state",
    "emission_factor_tco2_per_mwh",
    "emission_factor_source",
    "re_share_pct",
    "re_share_definition",
    "re_share_source",
    "solar_cf_pct",
    "solar_cf_basis",
    "solar_cf_source",
    "wind_cf_pct",
    "wind_cf_basis",
    "wind_cf_source",
    "storage_signal",
    "storage_source",
    "data_year",
    "confidence",
]

EXPECTED_CLUSTERS_9 = [
    "Mumbai/Navi Mumbai",
    "Chennai",
    "Hyderabad",
    "Pune",
    "Delhi-NCR/Noida",
    "Bengaluru",
    "Vizag",
    "Kolkata",
    "Jamnagar",
]

PRE_EXISTING_8_ROWS = [
    {
        "cluster": "Mumbai/Navi Mumbai",
        "state": "Maharashtra",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "36.8",
        "solar_cf_pct": "20.8",
        "wind_cf_pct": "24.0",
        "storage_signal": "₹2.38–2.40 Lakh/MW/month (MSEDCL 2,000 MW / 4,000 MWh Standalone BESS, Sep 2026)",
    },
    {
        "cluster": "Chennai",
        "state": "Tamil Nadu",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "53.2",
        "solar_cf_pct": "21.0",
        "wind_cf_pct": "31.5",
        "storage_signal": "₹3.15–3.16 Lakh/MW/month (TNGECL 375 MW / 1,500 MWh BESS Tender, 2026)",
    },
    {
        "cluster": "Hyderabad",
        "state": "Telangana",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "34.5",
        "solar_cf_pct": "21.5",
        "wind_cf_pct": "19.0",
        "storage_signal": "₹3.04–3.75 Lakh/MW/month (SECI ISTS National BESS Benchmark Proxy)",
    },
    {
        "cluster": "Pune",
        "state": "Maharashtra",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "36.8",
        "solar_cf_pct": "20.8",
        "wind_cf_pct": "24.0",
        "storage_signal": "₹2.38–2.40 Lakh/MW/month (MSEDCL 2,000 MW / 4,000 MWh Standalone BESS, Sep 2026)",
    },
    {
        "cluster": "Delhi-NCR/Noida",
        "state": "Uttar Pradesh",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "22.4",
        "solar_cf_pct": "19.5",
        "wind_cf_pct": "",
        "storage_signal": "₹3.04–3.75 Lakh/MW/month (SECI ISTS National BESS Benchmark Proxy)",
    },
    {
        "cluster": "Bengaluru",
        "state": "Karnataka",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "61.2",
        "solar_cf_pct": "22.5",
        "wind_cf_pct": "28.0",
        "storage_signal": "₹2.49–2.54 Lakh/MW/month (KPTCL 500 MW / 1,000 MWh Standalone BESS, 2026)",
    },
    {
        "cluster": "Vizag",
        "state": "Andhra Pradesh",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "44.1",
        "solar_cf_pct": "22.0",
        "wind_cf_pct": "27.0",
        "storage_signal": "₹2.80–3.20 Lakh/MW/month (APGECL Hybrid Pumped/Battery Storage Procurement Notices)",
    },
    {
        "cluster": "Kolkata",
        "state": "West Bengal",
        "emission_factor_tco2_per_mwh": "0.716",
        "re_share_pct": "13.8",
        "solar_cf_pct": "18.2",
        "wind_cf_pct": "",
        "storage_signal": "No state tender data found; ISTS national benchmark (₹3.04–3.75 Lakh/MW/month) applicable",
    },
]

@pytest.fixture(scope="module")
def supply_rows():
    import subprocess
    subprocess.run(["python", os.path.join(BASE_DIR, "fetch.py")], check=True)
    subprocess.run(["python", os.path.join(BASE_DIR, "build_table.py")], check=True)

    assert os.path.exists(OUTPUT_CSV), f"Output file missing at {OUTPUT_CSV}"
    with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows

def test_schema_completeness(supply_rows):
    with open(OUTPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    assert header == EXPECTED_COLUMNS, f"Header mismatch. Expected {EXPECTED_COLUMNS}, got {header}"

def test_exactly_9_rows_present(supply_rows):
    """(a) Test that the file has exactly 9 rows covering all 9 clusters."""
    assert len(supply_rows) == 9, f"Expected exactly 9 rows, got {len(supply_rows)}"
    clusters_found = [r["cluster"] for r in supply_rows]
    for exp_cluster in EXPECTED_CLUSTERS_9:
        assert exp_cluster in clusters_found, f"Missing cluster: {exp_cluster}"

def test_pre_existing_8_rows_preserved(supply_rows):
    """(b) Test that the 8 pre-existing cluster rows are preserved with matching values."""
    rows_by_cluster = {r["cluster"]: r for r in supply_rows}
    for expected in PRE_EXISTING_8_ROWS:
        c_name = expected["cluster"]
        assert c_name in rows_by_cluster, f"Pre-existing cluster missing: {c_name}"
        actual = rows_by_cluster[c_name]
        assert actual["state"] == expected["state"]
        assert actual["emission_factor_tco2_per_mwh"] == expected["emission_factor_tco2_per_mwh"]
        assert actual["re_share_pct"] == expected["re_share_pct"]
        assert actual["solar_cf_pct"] == expected["solar_cf_pct"]
        assert actual["wind_cf_pct"] == expected["wind_cf_pct"]
        assert actual["storage_signal"] == expected["storage_signal"]

def test_gujarat_jamnagar_row_integrity(supply_rows):
    """(c) Test that the new Gujarat/Jamnagar row has non-empty sources for every numeric field."""
    rows_by_cluster = {r["cluster"]: r for r in supply_rows}
    assert "Jamnagar" in rows_by_cluster, "Missing Jamnagar row in supply dataset"
    gj = rows_by_cluster["Jamnagar"]

    assert gj["state"] == "Gujarat"
    assert gj["emission_factor_tco2_per_mwh"] == "0.716"
    assert "CEA" in gj["emission_factor_source"]
    assert float(gj["re_share_pct"]) == pytest.approx(57.4, abs=0.5)
    assert "CEA" in gj["re_share_source"]
    assert "54.0%" in gj["re_share_definition"] or "57.4%" in gj["re_share_definition"]
    assert float(gj["solar_cf_pct"]) == pytest.approx(23.0, abs=0.5)
    assert "Saurashtra" in gj["solar_cf_basis"] or "Charanka" in gj["solar_cf_basis"]
    assert "GERC" in gj["solar_cf_source"] or "CERC" in gj["solar_cf_source"]
    assert float(gj["wind_cf_pct"]) == pytest.approx(32.0, abs=0.5)
    assert "Saurashtra" in gj["wind_cf_basis"] or "Kutch" in gj["wind_cf_basis"] or "Jamnagar" in gj["wind_cf_basis"]
    assert "NIWE" in gj["wind_cf_source"]
    assert "GUVNL" in gj["storage_signal"]
    assert "GUVNL" in gj["storage_source"]
    assert gj["confidence"].startswith("High")

def test_number_source_pairing_rule(supply_rows):
    """Every non-empty numeric field must have a matching non-empty source field."""
    for row in supply_rows:
        cluster = row["cluster"]
        
        # 1. Emission Factor
        if row["emission_factor_tco2_per_mwh"] != "":
            assert row["emission_factor_source"].strip() != "", f"Cluster {cluster} has emission factor but empty source!"
            val = float(row["emission_factor_tco2_per_mwh"])
            assert 0.4 <= val <= 1.5, f"Emission factor {val} out of plausible range in {cluster}"

        # 2. RE Share
        if row["re_share_pct"] != "":
            assert row["re_share_source"].strip() != "", f"Cluster {cluster} has RE share but empty source!"
            assert row["re_share_definition"].strip() != "", f"Cluster {cluster} has RE share but empty definition!"
            val = float(row["re_share_pct"])
            assert 1.0 <= val <= 100.0, f"RE share {val}% out of range in {cluster}"

        # 3. Solar CF
        if row["solar_cf_pct"] != "":
            assert row["solar_cf_source"].strip() != "", f"Cluster {cluster} has Solar CF but empty source!"
            assert row["solar_cf_basis"].strip() != "", f"Cluster {cluster} has Solar CF but empty basis!"
            val = float(row["solar_cf_pct"])
            assert 10.0 <= val <= 35.0, f"Solar CF {val}% out of range in {cluster}"

        # 4. Wind CF
        if row["wind_cf_pct"] != "":
            assert row["wind_cf_source"].strip() != "", f"Cluster {cluster} has Wind CF but empty source!"
            assert row["wind_cf_basis"].strip() != "", f"Cluster {cluster} has Wind CF but empty basis!"
            val = float(row["wind_cf_pct"])
            assert 10.0 <= val <= 50.0, f"Wind CF {val}% out of range in {cluster}"
        else:
            assert "not viable" in row["wind_cf_basis"].lower() or "negligible" in row["wind_cf_basis"].lower()
            assert row["wind_cf_source"].strip() != ""

        # 5. Storage Signal
        assert row["storage_source"].strip() != "", f"Cluster {cluster} lacks storage source!"

def test_gaps_documentation_exists():
    assert os.path.exists(GAPS_MD), "gaps.md report does not exist in output/"
    with open(GAPS_MD, "r", encoding="utf-8") as f:
        text = f.read()
    assert len(text) > 200, "gaps.md is empty or too short"
    for c in EXPECTED_CLUSTERS_9:
        assert c in text, f"gaps.md does not document cluster {c}"
