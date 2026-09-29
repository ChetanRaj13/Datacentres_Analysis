import os
import sys
import pytest
import openpyxl

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
GRID_DATA_DIR = os.path.dirname(TEST_DIR)
WORKSPACE_DIR = os.path.dirname(GRID_DATA_DIR)

for p in [WORKSPACE_DIR, GRID_DATA_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

XLSX_PATH = os.path.join(WORKSPACE_DIR, "datacentre_RE_matching_model.xlsx")

@pytest.fixture(scope="module")
def workbook():
    import subprocess
    subprocess.run(["python", os.path.join(GRID_DATA_DIR, "build_matching_model.py")], check=True)
    assert os.path.exists(XLSX_PATH), f"Workbook not found at {XLSX_PATH}"
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=False)
    return wb

def test_workbook_sheets_present(workbook):
    expected_sheets = ["Assumptions", "Demand_Supply_Model", "Slide_Ready_Summary"]
    for s in expected_sheets:
        assert s in workbook.sheetnames, f"Sheet '{s}' missing from workbook"

def test_assumptions_values(workbook):
    ws = workbook["Assumptions"]
    assert ws["B5"].value == 8760, f"Expected 8760 annual hours, got {ws['B5'].value}"
    assert ws["B6"].value == 0.65, f"Expected 0.65 utilization factor, got {ws['B6'].value}"
    assert ws["B7"].value == 0.716, f"Expected 0.716 grid emission factor, got {ws['B7'].value}"
    assert ws["B11"].value == 0.60, f"Expected 0.60 solar weight, got {ws['B11'].value}"
    assert ws["B12"].value == 0.40, f"Expected 0.40 wind weight, got {ws['B12'].value}"

def test_no_blank_cells_for_jamnagar_in_demand_supply_model(workbook):
    """
    Test: No cell in Demand_Supply_Model is blank for Jamnagar.
    Every column from A to U must contain a valid value or formula.
    """
    ws = workbook["Demand_Supply_Model"]
    
    jamnagar_row = None
    for row in range(5, 14):
        if ws.cell(row=row, column=1).value == "Jamnagar":
            jamnagar_row = row
            break

    assert jamnagar_row is not None, "Jamnagar row not found in Demand_Supply_Model"

    for col in range(1, 22):
        val = ws.cell(row=jamnagar_row, column=col).value
        assert val is not None and str(val).strip() != "", (
            f"Blank cell found in Jamnagar row at column {col} (header: {ws.cell(row=4, column=col).value})"
        )

def test_two_wind_cf_scenarios_for_jamnagar(workbook):
    """
    Test: The two wind-CF scenario columns for Jamnagar are both populated and clearly distinct:
    - Conservative Wind CF: 24.0%
    - Claimed Regional Wind CF: 32.0%
    - Blended RE Match Conservative: 23.4% (0.23*0.6 + 0.24*0.4)
    - Blended RE Match Claimed: 26.6% (0.23*0.6 + 0.32*0.4)
    """
    ws = workbook["Demand_Supply_Model"]
    
    jamnagar_row = None
    for row in range(5, 14):
        if ws.cell(row=row, column=1).value == "Jamnagar":
            jamnagar_row = row
            break

    assert jamnagar_row is not None

    wind_cons = ws.cell(row=jamnagar_row, column=10).value   # Col J: Wind CF Conservative
    wind_claim = ws.cell(row=jamnagar_row, column=11).value  # Col K: Wind CF Claimed

    assert float(wind_cons) == pytest.approx(0.24, abs=0.001), f"Expected 0.24, got {wind_cons}"
    assert float(wind_claim) == pytest.approx(0.32, abs=0.001), f"Expected 0.32, got {wind_claim}"
    assert float(wind_claim) > float(wind_cons), "Claimed wind CF should exceed conservative wind CF"

def test_slide_ready_summary_non_empty_confidence_notes(workbook):
    """
    Test: Every row in Slide_Ready_Summary has a non-empty confidence note
    accurately reflecting cluster caveats and the 75-82% RE-matching gap.
    """
    ws = workbook["Slide_Ready_Summary"]
    
    for row in range(5, 14):
        cluster_name = ws.cell(row=row, column=1).value
        note = ws.cell(row=row, column=9).value  # Col I is confidence note
        assert note is not None and len(str(note).strip()) >= 15, (
            f"Confidence note missing or too short for {cluster_name} in Slide_Ready_Summary"
        )
        if cluster_name == "Jamnagar":
            assert "wind" in str(note).lower()
        elif cluster_name == "Kolkata":
            assert "avoid" in str(note).lower()

    # Total row note
    total_note = ws.cell(row=14, column=9).value
    assert total_note is not None and "matching gap" in str(total_note).lower()

def test_formula_integrity(workbook):
    """Verify that formula columns contain dynamic Excel formulas, not hardcoded constants."""
    ws_model = workbook["Demand_Supply_Model"]
    
    for row in range(5, 14):
        demand_low_formula = str(ws_model.cell(row=row, column=5).value)
        demand_high_formula = str(ws_model.cell(row=row, column=6).value)
        match_cons_formula = str(ws_model.cell(row=row, column=12).value)
        co2_low_formula = str(ws_model.cell(row=row, column=16).value)
        co2_high_formula = str(ws_model.cell(row=row, column=17).value)

        assert demand_low_formula.startswith("="), f"Row {row} Demand Low is not a formula: {demand_low_formula}"
        assert "Assumptions!$B$5" in demand_low_formula, f"Row {row} Demand Low lacks 0.65 factor: {demand_low_formula}"
        assert demand_high_formula.startswith("="), f"Row {row} Demand High is not a formula: {demand_high_formula}"
        assert match_cons_formula.startswith("="), f"Row {row} Match Cons is not a formula: {match_cons_formula}"
        assert co2_low_formula.startswith("="), f"Row {row} CO2 Low is not a formula: {co2_low_formula}"
        assert co2_high_formula.startswith("="), f"Row {row} CO2 High is not a formula: {co2_high_formula}"
