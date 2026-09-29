"""
build_matching_model.py - Generates datacentre_RE_matching_model.xlsx
with Assumptions, Demand_Supply_Model, and Slide_Ready_Summary sheets.
Implements the corrected 0.65 utilization factor, the established blended RE formula
(solar_cf * 0.6 + wind_cf * 0.4), and highlights the 75-82% RE-matching gap.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_XLSX = os.path.join(ROOT_DIR, "datacentre_RE_matching_model.xlsx")

def create_model_workbook():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # Remove default sheet

    # Typography & Colors
    font_title = Font(name="Calibri", size=14, bold=True, color="1B365D")
    font_section = Font(name="Calibri", size=11, bold=True, color="1B365D")
    font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_italic = Font(name="Calibri", size=9, italic=True, color="555555")

    fill_header = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_accent = PatternFill(start_color="E8F1F5", end_color="E8F1F5", fill_type="solid")
    fill_jamnagar = PatternFill(start_color="FFF8E7", end_color="FFF8E7", fill_type="solid")
    fill_total = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fill_highlight = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )
    total_border = Border(
        top=Side(style="thin", color="1B365D"),
        bottom=Side(style="double", color="1B365D")
    )

    # =========================================================================
    # SHEET 1: Assumptions
    # =========================================================================
    ws_assump = wb.create_sheet(title="Assumptions")
    ws_assump.views.sheetView[0].showGridLines = True

    ws_assump["A1"] = "India Data Center 24/7 Renewable Energy Matching Model — Model Assumptions"
    ws_assump["A1"].font = font_title
    ws_assump["A2"] = "Canonical parameters, regulatory references, and technical multipliers"
    ws_assump["A2"].font = font_italic

    assumptions_data = [
        ("Parameter", "Value", "Unit", "Source / Regulatory Reference", "Notes"),
        ("Annual Operating Hours", 8760, "hours/year", "Standard Calendar Year", "Base continuous 24/7 calendar hours"),
        ("Data Center Utilization Factor", 0.65, "ratio (65%)", "Industry Standard IT/Facility Load Factor", "Accounts for server idling, redundancy headroom, and realistic facility power draw"),
        ("Unified National Grid Emission Factor", 0.716, "tCO2/MWh", "CEA CO2 Baseline Database (Ver 19.0/20.0)", "National Weighted Average for synchronous grid"),
        ("Western Region Operating Margin Proxy", 0.820, "tCO2/MWh", "CEA CO2 Baseline Database (Ver 19.0/20.0)", "Sensitivity proxy for Western Region (MH/GJ)"),
        ("Northern Region Operating Margin Proxy", 0.785, "tCO2/MWh", "CEA CO2 Baseline Database (Ver 19.0/20.0)", "Sensitivity proxy for Northern Region (UP/NCR)"),
        ("Eastern Region Operating Margin Proxy", 0.890, "tCO2/MWh", "CEA CO2 Baseline Database (Ver 19.0/20.0)", "Sensitivity proxy for Eastern Region (WB/Kolkata)"),
        ("Blended RE Solar Weight", 0.60, "ratio (60%)", "Standard Solar-Wind Hybrid PPA Ratio", "Weight applied to Solar CF when wind is viable"),
        ("Blended RE Wind Weight", 0.40, "ratio (40%)", "Standard Solar-Wind Hybrid PPA Ratio", "Weight applied to Wind CF when wind is viable"),
        ("Jamnagar Conservative Wind CF", 0.240, "ratio (24.0%)", "GERC Historical Siting Filings", "Conservative coastal Gujarat empirical baseline"),
        ("Jamnagar Claimed Regional Wind CF", 0.320, "ratio (32.0%)", "NIWE 120m/150m Resource Atlas (Kutch Corridor)", "Claimed regional macro-corridor upside (unverified at site)"),
    ]

    for row_idx, row_data in enumerate(assumptions_data, start=4):
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws_assump.cell(row=row_idx, column=col_idx, value=val)
            if row_idx == 4:
                cell.font = font_header
                cell.fill = fill_header
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.font = font_data
                cell.border = thin_border
                if col_idx in [2, 3]:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    if isinstance(val, float):
                        cell.number_format = "0.000" if val < 1.0 else "0.00"

    # =========================================================================
    # SHEET 2: Demand_Supply_Model
    # =========================================================================
    ws_model = wb.create_sheet(title="Demand_Supply_Model")
    ws_model.views.sheetView[0].showGridLines = True

    ws_model["A1"] = "Data Center Electricity Demand, RE Resource Supply & 24/7 Matching Model (9 Clusters)"
    ws_model["A1"].font = font_title
    ws_model["A2"] = "Methodology: Demand = MW * 8760 * 0.65; Blended RE = Solar*0.6 + Wind*0.4 (or 100% Solar where Wind is Not Viable)"
    ws_model["A2"].font = font_italic

    headers_model = [
        "Cluster",                        # A
        "State",                          # B
        "Total Low MW",                   # C
        "Total High MW",                  # D
        "Demand GWh (Low)",               # E  formula: =C*8760*Assumptions!$B$5/1000
        "Demand GWh (High)",              # F  formula: =D*8760*Assumptions!$B$5/1000
        "Grid EF (tCO2/MWh)",             # G  
        "BAU Grid RE Share (%)",          # H
        "Solar CF (%)",                   # I
        "Wind CF Conservative (%)",       # J  
        "Wind CF Claimed (%)",            # K  
        "Blended RE Match Cons (%)",      # L  formula: =IF(J>0, I*Assumptions!$B$10 + J*Assumptions!$B$11, I*1.0)
        "Blended RE Match Claimed (%)",   # M  formula: =IF(K>0, I*Assumptions!$B$10 + K*Assumptions!$B$11, I*1.0)
        "24/7 RE Match Gap Cons (%)",     # N  formula: =1 - L
        "24/7 RE Match Gap Claimed (%)",  # O  formula: =1 - M
        "CO2 Avoided Low Cons (t/yr)",    # P  formula: =MAX(0, (E*1000)*G*(L-H))
        "CO2 Avoided High Cons (t/yr)",   # Q  formula: =MAX(0, (F*1000)*G*(L-H))
        "CO2 Avoided Low Claimed (t/yr)", # R  formula: =MAX(0, (E*1000)*G*(M-H))
        "CO2 Avoided High Claimed (t/yr)",# S  formula: =MAX(0, (F*1000)*G*(M-H))
        "BESS Tariff Signal",             # T
        "Confidence & Sourcing Status",   # U
    ]

    for col_idx, h in enumerate(headers_model, start=1):
        cell = ws_model.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    clusters_raw = [
        # (Cluster, State, Low_MW, High_MW, Grid_EF, RE_Share, Solar_CF, Wind_Cons, Wind_Claimed, BESS_Sig, Status)
        ("Mumbai/Navi Mumbai", "Maharashtra", 766.6, 2316.6, 0.716, 0.368, 0.208, 0.240, 0.240, "₹2.38–2.40 L/MW/mo (MSEDCL)", "High (Tier 2 Reports / Statutory RE)"),
        ("Chennai", "Tamil Nadu", 191.5, 706.5, 0.716, 0.532, 0.210, 0.315, 0.315, "₹3.15–3.16 L/MW/mo (TNGECL)", "High (Subsea Landing Hub / Statutory RE)"),
        ("Hyderabad", "Telangana", 151.4, 751.4, 0.716, 0.345, 0.215, 0.190, 0.190, "₹3.04–3.75 L/MW/mo (SECI ISTS)", "High (DISCOM & AI Roadmap Filings)"),
        ("Pune", "Maharashtra", 45.0, 145.0, 0.716, 0.368, 0.208, 0.240, 0.240, "₹2.38–2.40 L/MW/mo (MSEDCL)", "Medium (Colocation Hub / State Mix)"),
        ("Delhi-NCR/Noida", "Uttar Pradesh", 153.0, 353.0, 0.716, 0.224, 0.195, 0.000, 0.000, "₹3.04–3.75 L/MW/mo (SECI ISTS)", "High (Yotta D2 / Bundelkhand Solar)"),
        ("Bengaluru", "Karnataka", 107.1, 257.1, 0.716, 0.612, 0.225, 0.280, 0.280, "₹2.49–2.54 L/MW/mo (KPTCL)", "Medium (State-level RE Proxy / Pavagada)"),
        ("Vizag", "Andhra Pradesh", 1000.0, 1000.0, 0.716, 0.441, 0.220, 0.270, 0.270, "₹2.80–3.20 L/MW/mo (APGECL)", "High (AdaniConneX 1 GW AI Campus)"),
        ("Kolkata", "West Bengal", 42.4, 67.4, 0.716, 0.138, 0.182, 0.000, 0.000, "₹3.04–3.75 L/MW/mo (SECI ISTS)", "Medium (Facility Sum / Low Non-Fossil)"),
        ("Jamnagar", "Gujarat", 1000.0, 3000.0, 0.716, 0.574, 0.230, 0.240, 0.320, "₹2.10–2.32 L/MW/mo (GUVNL)", "Tiered (Meta 168MW Verified; 1GW Ph1; 3GW Master Plan; Wind 24% Cons/32% Claimed)"),
    ]

    for idx, data in enumerate(clusters_raw, start=5):
        r_num = idx
        c_name, state, low_mw, high_mw, ef, re_sh, sol_cf, w_cons, w_claim, bess_sig, conf = data

        ws_model[f"A{r_num}"] = c_name
        ws_model[f"B{r_num}"] = state
        ws_model[f"C{r_num}"] = low_mw
        ws_model[f"D{r_num}"] = high_mw
        ws_model[f"E{r_num}"] = f"=C{r_num}*Assumptions!$B$5*Assumptions!$B$6/1000"
        ws_model[f"F{r_num}"] = f"=D{r_num}*Assumptions!$B$5*Assumptions!$B$6/1000"
        ws_model[f"G{r_num}"] = ef
        ws_model[f"H{r_num}"] = re_sh
        ws_model[f"I{r_num}"] = sol_cf
        ws_model[f"J{r_num}"] = w_cons
        ws_model[f"K{r_num}"] = w_claim
        ws_model[f"L{r_num}"] = f"=IF(J{r_num}>0, I{r_num}*Assumptions!$B$11 + J{r_num}*Assumptions!$B$12, I{r_num}*1.0)"
        ws_model[f"M{r_num}"] = f"=IF(K{r_num}>0, I{r_num}*Assumptions!$B$11 + K{r_num}*Assumptions!$B$12, I{r_num}*1.0)"
        ws_model[f"N{r_num}"] = f"=1-L{r_num}"
        ws_model[f"O{r_num}"] = f"=1-M{r_num}"
        ws_model[f"P{r_num}"] = f"=MAX(0, (E{r_num}*1000)*G{r_num}*(L{r_num}-H{r_num}))"
        ws_model[f"Q{r_num}"] = f"=MAX(0, (F{r_num}*1000)*G{r_num}*(L{r_num}-H{r_num}))"
        ws_model[f"R{r_num}"] = f"=MAX(0, (E{r_num}*1000)*G{r_num}*(M{r_num}-H{r_num}))"
        ws_model[f"S{r_num}"] = f"=MAX(0, (F{r_num}*1000)*G{r_num}*(M{r_num}-H{r_num}))"
        ws_model[f"T{r_num}"] = bess_sig
        ws_model[f"U{r_num}"] = conf

        # Formatting
        for col_letter in [get_column_letter(i) for i in range(1, 22)]:
            cell = ws_model[f"{col_letter}{r_num}"]
            cell.font = font_data
            cell.border = thin_border
            if c_name == "Jamnagar":
                cell.fill = fill_jamnagar
            elif c_name == "Kolkata":
                cell.fill = fill_accent

        # Number formats
        for col_letter in ["C", "D", "E", "F"]:
            ws_model[f"{col_letter}{r_num}"].number_format = "#,##0.0"
        ws_model[f"G{r_num}"].number_format = "0.000"
        for col_letter in ["H", "I", "J", "K", "L", "M", "N", "O"]:
            ws_model[f"{col_letter}{r_num}"].number_format = "0.0%"
        for col_letter in ["P", "Q", "R", "S"]:
            ws_model[f"{col_letter}{r_num}"].number_format = "#,##0"

    # Total Row
    tot_row = 14
    ws_model[f"A{tot_row}"] = "Total National (All 9 Clusters)"
    ws_model[f"B{tot_row}"] = "India Synchronous Grid"
    ws_model[f"C{tot_row}"] = f"=SUM(C5:C13)"
    ws_model[f"D{tot_row}"] = f"=SUM(D5:D13)"
    ws_model[f"E{tot_row}"] = f"=SUM(E5:E13)"
    ws_model[f"F{tot_row}"] = f"=SUM(F5:F13)"
    ws_model[f"G{tot_row}"] = 0.716
    ws_model[f"H{tot_row}"] = f"=AVERAGE(H5:H13)"
    ws_model[f"I{tot_row}"] = f"=AVERAGE(I5:I13)"
    ws_model[f"J{tot_row}"] = f"=AVERAGE(J5:J13)"
    ws_model[f"K{tot_row}"] = f"=AVERAGE(K5:K13)"
    ws_model[f"L{tot_row}"] = f"=AVERAGE(L5:L13)"
    ws_model[f"M{tot_row}"] = f"=AVERAGE(M5:M13)"
    ws_model[f"N{tot_row}"] = f"=AVERAGE(N5:N13)"
    ws_model[f"O{tot_row}"] = f"=AVERAGE(O5:O13)"
    ws_model[f"P{tot_row}"] = f"=SUM(P5:P13)"
    ws_model[f"Q{tot_row}"] = f"=SUM(Q5:Q13)"
    ws_model[f"R{tot_row}"] = f"=SUM(R5:R13)"
    ws_model[f"S{tot_row}"] = f"=SUM(S5:S13)"
    ws_model[f"T{tot_row}"] = "National BESS Portfolio"
    ws_model[f"U{tot_row}"] = "Headline finding: 75-82% RE-matching gap across clusters"

    for col_letter in [get_column_letter(i) for i in range(1, 22)]:
        cell = ws_model[f"{col_letter}{tot_row}"]
        cell.font = font_bold
        cell.fill = fill_total
        cell.border = total_border

    for col_letter in ["C", "D", "E", "F"]:
        ws_model[f"{col_letter}{tot_row}"].number_format = "#,##0.0"
    ws_model[f"G{tot_row}"].number_format = "0.000"
    for col_letter in ["H", "I", "J", "K", "L", "M", "N", "O"]:
        ws_model[f"{col_letter}{tot_row}"].number_format = "0.0%"
    for col_letter in ["P", "Q", "R", "S"]:
        ws_model[f"{col_letter}{tot_row}"].number_format = "#,##0"

    # =========================================================================
    # SHEET 3: Slide_Ready_Summary
    # =========================================================================
    ws_slide = wb.create_sheet(title="Slide_Ready_Summary")
    ws_slide.views.sheetView[0].showGridLines = True

    ws_slide["A1"] = "Data Center 24/7 Renewable Energy & Decarbonization Roadmap — Slide-Ready Summary"
    ws_slide["A1"].font = font_title
    ws_slide["A2"] = "Executive deck summary: Un-stored dedicated RE buildout leaves a 75–82% matching gap across all clusters"
    ws_slide["A2"].font = font_italic

    headers_slide = [
        "Cluster",
        "Demand Today (GWh/yr - Low)",
        "Demand Future (GWh/yr - High)",
        "Current Grid RE Share (%)",
        "RE Matched Under Framework (%)",
        "24/7 RE Matching Gap (%)",
        "CO2 Avoided Today (Tonnes/yr)",
        "CO2 Avoided Future (Tonnes/yr)",
        "One-Line Confidence & Sourcing Note",
    ]

    for col_idx, h in enumerate(headers_slide, start=1):
        cell = ws_slide.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    slide_rows_data = [
        ("Mumbai/Navi Mumbai", "=ROUND(Demand_Supply_Model!E5, 0)", "=ROUND(Demand_Supply_Model!F5, 0)", "=Demand_Supply_Model!H5", "=Demand_Supply_Model!L5", "=Demand_Supply_Model!N5", "=ROUND(Demand_Supply_Model!P5, 0)", "=ROUND(Demand_Supply_Model!Q5, 0)", "77.9% matching gap; dedicated RE buildout CF (22.1%) is below Maharashtra grid mix (36.8%), yielding 0 avoided CO2 without storage."),
        ("Chennai", "=ROUND(Demand_Supply_Model!E6, 0)", "=ROUND(Demand_Supply_Model!F6, 0)", "=Demand_Supply_Model!H6", "=Demand_Supply_Model!L6", "=Demand_Supply_Model!N6", "=ROUND(Demand_Supply_Model!P6, 0)", "=ROUND(Demand_Supply_Model!Q6, 0)", "74.8% matching gap; top coastal wind corridor (31.5% CF) yields 25.2% blended match, below TN grid baseline (53.2%)."),
        ("Hyderabad", "=ROUND(Demand_Supply_Model!E7, 0)", "=ROUND(Demand_Supply_Model!F7, 0)", "=Demand_Supply_Model!H7", "=Demand_Supply_Model!L7", "=Demand_Supply_Model!N7", "=ROUND(Demand_Supply_Model!P7, 0)", "=ROUND(Demand_Supply_Model!Q7, 0)", "79.5% matching gap; un-stored solar+wind achieves 20.5% match vs 34.5% Telangana grid mix; requires BESS or interstate imports."),
        ("Pune", "=ROUND(Demand_Supply_Model!E8, 0)", "=ROUND(Demand_Supply_Model!F8, 0)", "=Demand_Supply_Model!H8", "=Demand_Supply_Model!L8", "=Demand_Supply_Model!N8", "=ROUND(Demand_Supply_Model!P8, 0)", "=ROUND(Demand_Supply_Model!Q8, 0)", "77.9% matching gap; secondary colocation cluster; benefits from Satara ridge wind but cannot match 24/7 load without storage."),
        ("Delhi-NCR/Noida", "=ROUND(Demand_Supply_Model!E9, 0)", "=ROUND(Demand_Supply_Model!F9, 0)", "=Demand_Supply_Model!H9", "=Demand_Supply_Model!L9", "=Demand_Supply_Model!N9", "=ROUND(Demand_Supply_Model!P9, 0)", "=ROUND(Demand_Supply_Model!Q9, 0)", "80.5% matching gap; zero local wind viability (<100 W/m²); 19.5% solar-only match is below UP grid mix (22.4%)."),
        ("Bengaluru", "=ROUND(Demand_Supply_Model!E10, 0)", "=ROUND(Demand_Supply_Model!F10, 0)", "=Demand_Supply_Model!H10", "=Demand_Supply_Model!L10", "=Demand_Supply_Model!N10", "=ROUND(Demand_Supply_Model!P10, 0)", "=ROUND(Demand_Supply_Model!Q10, 0)", "75.3% matching gap; state grid has India's highest RE share (61.2%); peri-urban relocation solves urban water crisis rather than grid mix."),
        ("Vizag", "=ROUND(Demand_Supply_Model!E11, 0)", "=ROUND(Demand_Supply_Model!F11, 0)", "=Demand_Supply_Model!H11", "=Demand_Supply_Model!L11", "=Demand_Supply_Model!N11", "=ROUND(Demand_Supply_Model!P11, 0)", "=ROUND(Demand_Supply_Model!Q11, 0)", "76.0% matching gap; 1 GW Google/AdaniConneX hub backed by 24.0% blended solar-wind resource, below 44.1% AP state grid."),
        ("Kolkata", "=ROUND(Demand_Supply_Model!E12, 0)", "=ROUND(Demand_Supply_Model!F12, 0)", "=Demand_Supply_Model!H12", "=Demand_Supply_Model!L12", "=Demand_Supply_Model!N12", "=ROUND(Demand_Supply_Model!P12, 0)", "=ROUND(Demand_Supply_Model!Q12, 0)", "81.8% matching gap; only cluster where dedicated RE (18.2%) beats low coal grid (13.8%), avoiding 7.6k–12.1k t CO2/yr."),
        ("Jamnagar", "=ROUND(Demand_Supply_Model!E13, 0)", "=ROUND(Demand_Supply_Model!F13, 0)", "=Demand_Supply_Model!H13", "=Demand_Supply_Model!L13", "=Demand_Supply_Model!N13", "=ROUND(Demand_Supply_Model!P13, 0)", "=ROUND(Demand_Supply_Model!Q13, 0)", "76.6% matching gap (conservative 24% wind CF yields 23.4% match; claimed 32% wind gives 26.6% match / 73.4% gap); captive giga-complex."),
    ]

    for idx, rdata in enumerate(slide_rows_data, start=5):
        r_num = idx
        for c_idx, val in enumerate(rdata, start=1):
            cell = ws_slide.cell(row=r_num, column=c_idx, value=val)
            cell.font = font_data
            cell.border = thin_border
            if rdata[0] == "Jamnagar":
                cell.fill = fill_jamnagar
            elif rdata[0] == "Kolkata":
                cell.fill = fill_accent

            if c_idx in [2, 3, 7, 8]:
                cell.number_format = "#,##0"
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif c_idx in [4, 5, 6]:
                cell.number_format = "0.0%"
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 9:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Slide Summary Total Row
    tot_slide_row = 14
    ws_slide[f"A{tot_slide_row}"] = "Total National Impact (9 Clusters)"
    ws_slide[f"B{tot_slide_row}"] = "=SUM(B5:B13)"
    ws_slide[f"C{tot_slide_row}"] = "=SUM(C5:C13)"
    ws_slide[f"D{tot_slide_row}"] = "=AVERAGE(D5:D13)"
    ws_slide[f"E{tot_slide_row}"] = "=AVERAGE(E5:E13)"
    ws_slide[f"F{tot_slide_row}"] = "=AVERAGE(F5:F13)"
    ws_slide[f"G{tot_slide_row}"] = "=SUM(G5:G13)"
    ws_slide[f"H{tot_slide_row}"] = "=SUM(H5:H13)"
    ws_slide[f"I{tot_slide_row}"] = "National headline: Un-stored dedicated RE leaves an average 77.8% 24/7 matching gap across India."

    for col_letter in [get_column_letter(i) for i in range(1, 10)]:
        cell = ws_slide[f"{col_letter}{tot_slide_row}"]
        cell.font = font_bold
        cell.fill = fill_total
        cell.border = total_border

    for col_letter in ["B", "C", "G", "H"]:
        ws_slide[f"{col_letter}{tot_slide_row}"].number_format = "#,##0"
        ws_slide[f"{col_letter}{tot_slide_row}"].alignment = Alignment(horizontal="right", vertical="center")
    for col_letter in ["D", "E", "F"]:
        ws_slide[f"{col_letter}{tot_slide_row}"].number_format = "0.0%"
        ws_slide[f"{col_letter}{tot_slide_row}"].alignment = Alignment(horizontal="center", vertical="center")

    # Auto-fit column widths
    for sheet in [ws_assump, ws_model, ws_slide]:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if not str(cell.value or "").startswith("="):
                    max_len = max(max_len, len(val_str))
                else:
                    max_len = max(max_len, 12)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # Save
    wb.save(OUTPUT_XLSX)
    print(f"[>] Successfully generated corrected 24/7 RE matching model: {OUTPUT_XLSX}")

if __name__ == "__main__":
    create_model_workbook()
