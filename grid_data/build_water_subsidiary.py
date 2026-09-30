"""
build_water_subsidiary.py - Generates water_cooling_subsidiary.csv
Lightweight subsidiary dataset mapping water stress, WUE basis, annual water demand,
and water-positive cooling priority across all 9 Indian data center clusters.
"""

import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_CSV_DATA = os.path.join(ROOT_DIR, "data", "water_cooling_subsidiary.csv")

def generate_water_subsidiary():
    # Sourced Demand GWh (from datacentre_RE_matching_model.xlsx / Demand_Supply_Model)
    # Low / High GWh computed via MW * 8760 * 0.65 / 1000
    # WUE Assumption: 1.25 L/kWh = 1.25 ML / GWh
    wue_factor = 1.25
    wue_basis_label = "Industry-standard assumption, applied uniformly (1.25 L/kWh for standard evaporative/chilled-water cooling; Uptime Institute / AWS / Microsoft reported range 1.0–1.8 L/kWh)"

    clusters_water = [
        {
            "cluster": "Delhi-NCR/Noida",
            "water_stress_level": "High",
            "water_stress_source": "CGWB Dynamic Ground Water Resources Assessment 2023 (Gautam Buddha Nagar / Gurugram Over-Exploited) / WRI Aqueduct 4.0 (Extremely High >80%)",
            "demand_gwh_low": 871.18,
            "demand_gwh_high": 2009.98,
            "priority_flag": "High Priority",
            "notes": "Critically over-exploited Yamuna floodplain aquifer; 2,512 ML/yr future draw creates severe municipal water conflict in Greater Noida."
        },
        {
            "cluster": "Bengaluru",
            "water_stress_level": "High",
            "water_stress_source": "CGWB Karnataka Ground Water Year Book 2023 (Bengaluru Urban & Rural Over-Exploited) / WRI Aqueduct 4.0 (Extremely High >80%)",
            "demand_gwh_low": 609.83,
            "demand_gwh_high": 1463.93,
            "priority_flag": "High Priority",
            "notes": "Severe municipal tanker water crisis & Cauvery Stage V deficits; 1,830 ML/yr draw makes urban freshwater cooling indefensible without recycled water mandate."
        },
        {
            "cluster": "Chennai",
            "water_stress_level": "High",
            "water_stress_source": "CGWB Tamil Nadu Ground Water Assessment (Kanchipuram/Tiruvallur Over-Exploited) / WRI Aqueduct 4.0 (Extremely High >80% / 2019 Day Zero)",
            "demand_gwh_low": 1089.54,
            "demand_gwh_high": 4019.63,
            "priority_flag": "High Priority",
            "notes": "Historical Day Zero reservoir vulnerability; 5,025 ML/yr pipeline demand must mandate 100% CMWSSB Tertiary Treated Reverse Osmosis (TTRO) effluent."
        },
        {
            "cluster": "Hyderabad",
            "water_stress_level": "Medium-High",
            "water_stress_source": "CGWB Telangana Dynamic Ground Water Assessment (Rangareddy Semi-Critical / Hyderabad Over-Exploited) / WRI Aqueduct 4.0 (High 40–80%)",
            "demand_gwh_low": 862.00,
            "demand_gwh_high": 4278.47,
            "priority_flag": "Medium Priority",
            "notes": "Semi-critical groundwater in Chandanvelly/Pharma City belt; requires HMWSSB treated industrial wastewater hookup for upcoming 400 MW AI clusters."
        },
        {
            "cluster": "Pune",
            "water_stress_level": "Medium",
            "water_stress_source": "CGWB Maharashtra Dynamic Ground Water Resources (Pune District Semi-Critical) / WRI Aqueduct 4.0 (Medium-High 20–40%)",
            "demand_gwh_low": 256.23,
            "demand_gwh_high": 825.63,
            "priority_flag": "Medium Priority",
            "notes": "Khadakwasla reservoir dependence with seasonal summer depletion; MIDC industrial recycled water sourcing recommended for Hinjewadi/Chakan."
        },
        {
            "cluster": "Mumbai/Navi Mumbai",
            "water_stress_level": "Medium",
            "water_stress_source": "CGWB Maharashtra Ground Water Year Book (Thane/Raigad Safe to Semi-Critical) / WRI Aqueduct 4.0 (Medium 20–40% / Bhatsa-Tansa Dams)",
            "demand_gwh_low": 4365.02,
            "demand_gwh_high": 13190.72,
            "priority_flag": "Medium Priority",
            "notes": "High absolute volume (16,488 ML/yr) cushioned by high monsoon rainfall and municipal reservoir infrastructure; NMMC/MIDC industrial effluent available."
        },
        {
            "cluster": "Vizag",
            "water_stress_level": "Medium",
            "water_stress_source": "CGWB Andhra Pradesh Ground Water Assessment (Visakhapatnam Semi-Critical Coastal) / WRI Aqueduct 4.0 (Medium-High 20–40%)",
            "demand_gwh_low": 5694.00,
            "demand_gwh_high": 5694.00,
            "priority_flag": "Low Priority (Coastal / Desal Option)",
            "notes": "1 GW AdaniConneX/Google hub; coastal location allows direct industrial intake and seawater reverse osmosis desalination, minimizing municipal freshwater clash."
        },
        {
            "cluster": "Kolkata",
            "water_stress_level": "Low",
            "water_stress_source": "CGWB West Bengal Ground Water Assessment (Kolkata / North 24 Parganas Safe) / WRI Aqueduct 4.0 (Low-Medium <20% / Hooghly River Basin)",
            "demand_gwh_low": 241.43,
            "demand_gwh_high": 383.78,
            "priority_flag": "Low Priority",
            "notes": "Abundant surface water and high alluvial water table in Gangetic delta; modest demand (<480 ML/yr) creates lowest national water conflict."
        },
        {
            "cluster": "Jamnagar",
            "water_stress_level": "High (Physical / Arid Saurashtra)",
            "water_stress_source": "CGWB Gujarat Ground Water Assessment 2023 (Saurashtra Semi-Critical/Arid) / Sourced Reliance-Meta Release (168 MW Anchor Desalination Only)",
            "demand_gwh_low": 5694.00,
            "demand_gwh_high": 17082.00,
            "priority_flag": "Medium-High Priority (Partial Desal / 832–2,832 MW Unconfirmed)",
            "notes": "Desalinated seawater cooling confirmed only for 168 MW Meta anchor (1,196 ML/yr mitigated); remaining 832 MW Phase 1 (5,922 ML/yr) and 2,832 MW Master Plan (20,157 ML/yr) not independently confirmed for desalinated cooling and sit in arid Saurashtra (CGWB Semi-Critical)."
        },
    ]

    fieldnames = [
        "cluster",
        "water_stress_level",
        "water_stress_source",
        "wue_basis",
        "demand_ml_low",
        "demand_ml_high",
        "priority_flag",
        "notes"
    ]

    rows = []
    for c in clusters_water:
        ml_low = round(c["demand_gwh_low"] * wue_factor, 1)
        ml_high = round(c["demand_gwh_high"] * wue_factor, 1)
        rows.append({
            "cluster": c["cluster"],
            "water_stress_level": c["water_stress_level"],
            "water_stress_source": c["water_stress_source"],
            "wue_basis": wue_basis_label,
            "demand_ml_low": ml_low,
            "demand_ml_high": ml_high,
            "priority_flag": c["priority_flag"],
            "notes": c["notes"]
        })

    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_CSV_DATA), exist_ok=True)

    with open(OUTPUT_CSV_DATA, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[>] Successfully generated: {OUTPUT_CSV_DATA}")

if __name__ == "__main__":
    generate_water_subsidiary()
