# Grid Supply Data — Gaps & Sourcing Analysis

This report documents the coverage, proxies, and gaps encountered while compiling the electricity supply and renewable resource data for the 9 Indian Data Center clusters (including Jamnagar, Gujarat).

## 1. Summary of Sourcing by Field

| Supply Field | Sourcing Status | Core Primary Sources Used | Notes & Handling |
|---|---|---|---|
| **1. Grid Emission Factor (tCO₂/MWh)** | **Fully Sourced (Unified National)** | CEA CO2 Baseline Database for the Indian Power Sector (Ver 19.0/20.0) | India operates a single synchronized national grid. The national weighted average baseline is **0.716 tCO₂/MWh** (Combined Margin: 0.718 tCO₂/MWh). Regional operating margins (e.g. Eastern: 0.890, Western: 0.820, Northern: 0.785) are noted for sensitivity analysis. |
| **2. State RE Share (%)** | **Fully Sourced** | CEA All India Installed Capacity Report (Executive Summary) | Captured both definitions: **RE including Large Hydro (>=25MW)** and **RE excluding Large Hydro** to prevent silent definition mismatches. Karnataka leads at 61.2% (51.8% excl hydro), Gujarat is second at 57.4% (54.0% excl hydro), Tamil Nadu at 53.2% (48.6%), while West Bengal is lowest at 13.8% (4.2%). |
| **3. Solar Capacity Factor (%)** | **Fully Sourced (Park & State Benchmarks)** | CERC RE Tariff Regulations, GERC / SERC Multi-Year Tariff Orders, Ultra Mega Solar Park Baselines (Charanka, Pavagada, Kurnool, Sakri) | Mapped to nearest high-performance solar park benchmark (23.0% for Gujarat/Charanka & Saurashtra, 22.5% for Pavagada/Bengaluru, 22.0% for Kurnool/Vizag, 20.8% for Maharashtra, 19.5% for UP/NCR, 18.2% for West Bengal due to monsoon cloud attenuation). |
| **4. Wind Capacity Factor (%)** | **Fully Sourced with Explicit Feasibility Flags** | NIWE (National Institute of Wind Energy) Wind Resource Assessment at 120m/150m Hub Height | High coastal/pass wind in Gujarat (32.0% in Coastal Saurashtra / Gulf of Kutch), Tamil Nadu (31.5% at Muppandal/Kayathar) and Karnataka (28.0%). Explicitly marked **"not viable"** (0.0% / blank) for Delhi-NCR/UP and Kolkata/West Bengal due to sub-100 W/m² wind power density. |
| **5. Storage / BESS Cost Signal** | **Sourced (State Auctions + National Benchmarks)** | GUVNL (Gujarat), MSEDCL (Maharashtra), KPTCL (Karnataka), TNGECL (Tamil Nadu), SECI ISTS BESS Auctions | BESS tenders in India are awarded as monthly capacity availability charges (₹ Lakh/MW/month). Concluded tariffs range from **₹2.10–2.32 Lakh/MW/month** (Gujarat GUVNL Phase VIII/IX 2026) to **₹2.38–2.40 Lakh/MW/month** (Maharashtra MSEDCL 2GW/4GWh) and **₹3.15–3.16 Lakh/MW/month** (Tamil Nadu). For UP, Telangana, and West Bengal, the national SECI ISTS benchmark proxy (₹3.04–3.75 Lakh/MW/month) is provided. |

---

## 2. Cluster-by-Cluster Sourcing Detail & Edge Cases

### 1. Mumbai/Navi Mumbai (Maharashtra)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline; Western Region Operating Margin proxy: 0.820 tCO₂/MWh).
- **RE Share:** 36.8% with hydro / 26.5% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 20.8% (CERC / MERC Sakri Solar Park baseline).
- **Wind CF:** 24.0% (NIWE Satara/Sangli ridge zone).
- **Storage Signal:** ₹2.38–2.40 Lakh/MW/month (MSEDCL 2,000 MW / 4,000 MWh tender awarded Sep 2026).

### 2. Chennai (Tamil Nadu)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline; Southern Region proxy: 0.730 tCO₂/MWh).
- **RE Share:** 53.2% with hydro / 48.6% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 21.0% (Kamuthi Solar Park & TNERC normative).
- **Wind CF:** 31.5% (NIWE Muppandal / Kayathar Pass Zone I high-yield resource).
- **Storage Signal:** ₹3.15–3.16 Lakh/MW/month (TNGECL 375 MW / 1,500 MWh BESS tender).

### 3. Hyderabad (Telangana)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline).
- **RE Share:** 34.5% with hydro / 23.8% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 21.5% (CERC Southern Region plateau benchmark).
- **Wind CF:** 19.0% (NIWE assessment; marginal commercial onshore wind).
- **Storage Signal:** ₹3.04–3.75 Lakh/MW/month (SECI ISTS benchmark; no state standalone BESS tender).

### 4. Pune (Maharashtra)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline).
- **RE Share:** 36.8% with hydro / 26.5% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 20.8% (Western Maharashtra regional benchmark).
- **Wind CF:** 24.0% (Western Ghats ridge sites adjacent to Pune cluster).
- **Storage Signal:** ₹2.38–2.40 Lakh/MW/month (MSEDCL BESS auction).

### 5. Delhi-NCR/Noida (Uttar Pradesh)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline; Northern Region proxy: 0.785 tCO₂/MWh).
- **RE Share:** 22.4% with hydro / 13.6% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 19.5% (Bundelkhand regional solar park proxy; winter haze attenuation).
- **Wind CF:** **Not Viable** (Gangetic plains wind power density <100 W/m²; zero commercial potential).
- **Storage Signal:** ₹3.04–3.75 Lakh/MW/month (SECI National ISTS Storage benchmark).

### 6. Bengaluru (Karnataka)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline).
- **RE Share:** 61.2% with hydro / 51.8% excl. large hydro (CEA Installed Capacity; highest with hydro).
- **Solar CF:** 22.5% (Pavagada Ultra Mega Solar Park benchmark).
- **Wind CF:** 28.0% (Chitradurga / Gadag central Karnataka wind corridor).
- **Storage Signal:** ₹2.49–2.54 Lakh/MW/month (KPTCL 500 MW / 1,000 MWh BESS award).

### 7. Vizag (Andhra Pradesh)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline).
- **RE Share:** 44.1% with hydro / 36.2% excl. large hydro (CEA Installed Capacity).
- **Solar CF:** 22.0% (Kurnool / Ananthapuramu Ultra Mega Solar Park benchmark).
- **Wind CF:** 27.0% (Rayalaseema wind corridor).
- **Storage Signal:** ₹2.80–3.20 Lakh/MW/month (APTRANSCO / APGECL Storage Procurement Notices).

### 8. Kolkata (West Bengal)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline; Eastern Region Operating Margin: 0.890 tCO₂/MWh due to coal fleet).
- **RE Share:** 13.8% with hydro / 4.2% excl. large hydro (CEA Installed Capacity; lowest non-fossil penetration).
- **Solar CF:** 18.2% (Gangetic delta regional proxy; lower DNI & cloud cover attenuation).
- **Wind CF:** **Not Viable** (Gangetic delta wind power density <100 W/m²; non-commercial onshore resource).
- **Storage Signal:** No state tender data found; ISTS national benchmark (₹3.04–3.75 Lakh/MW/month) applicable.

### 9. Jamnagar (Gujarat)
- **Emission Factor:** 0.716 tCO₂/MWh (CEA National Baseline; Western Region Operating Margin proxy: 0.820 tCO₂/MWh).
- **RE Share:** 57.4% with hydro / 54.0% excl. large hydro (CEA Installed Capacity; highest non-hydro RE share nationally).
- **Solar CF:** 23.0% (Charanka Solar Park & Coastal Saurashtra / Kutch high-irradiance benchmark).
- **Wind CF:** 32.0% (Coastal Saurashtra / Gulf of Kutch / Jamnagar Class I wind corridor at 120m/150m hub height).
- **Storage Signal:** ₹2.10–2.32 Lakh/MW/month (GUVNL 450 MW / 900 MWh & 335 MW Standalone BESS, 2026).

---

## 3. Methodological Notes for 24x7 RE-Matching Model
1. **Grid Emission Baseline Application:** Use **0.716 tCO₂/MWh** for national BAU baseline GWh-to-carbon conversions. For localized grid sensitivity, apply Regional Operating Margins (Western: 0.820, Northern: 0.785, Eastern: 0.890).
2. **Solar-Wind Complementarity:** Coastal and Western clusters (Jamnagar, Chennai, Bengaluru, Vizag, Mumbai/Pune) exhibit strong diurnal solar-wind anti-correlation (wind peaks during evening/monsoon, solar peaks midday), requiring significantly smaller BESS capacity for 24x7 matching.
3. **Inland / Non-Wind Clusters (NCR, Kolkata):** Cannot achieve 24x7 RE matching locally without inter-state transmission system (ISTS) wind imports or heavy 8-12 hour BESS duration.
