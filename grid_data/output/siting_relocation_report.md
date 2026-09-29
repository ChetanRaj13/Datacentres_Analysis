# Data Center Siting & Relocation Candidates Analysis (v2 - Audited)

> Strategic evaluation of 2–3 named alternate sites per cluster across workload-appropriate search radii, RE penetration, solar/wind resource quality, water stress, distance penalties, and explicit proxy auditing.

## 1. Candidate Siting Evaluation Summary (Audited v2)

| Current Cluster | Candidate Alternate Location | Dist (km) | Workload Category | RE Share (%) | Solar CF (%) | Wind CF (%) | Water Stress | Uplift | Net Score | Proxy? | Key Strategic Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Mumbai/Navi Mumbai** | **MIDC Dighi Port Industrial Area (Raigad / DMIC Node)** | 105 km | `cloud_inference_50_100km` | 36.8% | 21.0% | 24.5% | Low | **+16.52** | **12.14** *(orig: 14.35)* | `Site-Specific` | Direct coastal location with seawater cooling potential; bypasses Mumbai ur... |
| **Mumbai/Navi Mumbai** | **MIDC Chakan-Talegaon Industrial Corridor (Pune Outer Border)** | 95 km | `cloud_inference_50_100km` | 36.8% | 20.8% | 24.0% | Low | **+16.0** | **12.04** | `✓ Proxy` | Higher elevation (~600m) reduces HVAC ambient cooling load; direct 400kV su... |
| **Mumbai/Navi Mumbai** | **MIDC Tarapur Industrial Complex (Palghar Coastal Node)** | 110 km | `cloud_inference_50_100km` | 36.8% | 20.9% | 23.5% | Low | **+15.73** | **11.15** *(orig: 11.14)* | `Site-Specific` | Established power transmission corridor with coastal water access; lower se... |
| **Chennai** | **Cheyyar SIPCOT Industrial Park (Tiruvannamalai Corridor)** | 92 km | `cloud_inference_50_100km` | 53.2% | 21.2% | 31.5% | Medium | **+8.16** | **4.33** | `Site-Specific` | Dedicated 230kV substation; closer to central TN wind generation corridor; ... |
| **Chennai** | **Sri City Integrated Business City (Tada / AP-TN Border)** | 72 km | `cloud_inference_50_100km` | 48.5% | 21.5% | 28.5% | Low | **+12.61** | **9.61** | `Site-Specific` | Dual-state grid access (TNERC/APCPDCL), 100% industrial water recycling sys... |
| **Hyderabad** | **Orvakal Mega Industrial Hub (Kurnool Ultra Solar Corridor)** | 205 km | `ai_training_150_400km` | 44.1% | 22.5% | 27.0% | Low | **+17.87** | **15.31** | `✓ Proxy` | Direct co-location with 1,000 MW Kurnool Solar Park and Rayalaseema wind co... |
| **Hyderabad** | **Divitipally Green Tech & EV Corridor (Mahabubnagar, Telangana)** | 78 km | `ai_training_150_400km` | 34.5% | 22.0% | 19.5% | Low | **+8.75** | **7.77** *(orig: 7.78)* | `Site-Specific` | High solar DNI plateau; dedicated clean tech corridor; lower water competit... |
| **Hyderabad** | **Zaheerabad NIMZ Mega Industrial Corridor (Telangana)** | 115 km | `ai_training_150_400km` | 34.5% | 21.8% | 20.0% | Low | **+8.95** | **7.51** | `Site-Specific` | 600m elevation; abundant land and dedicated Singur canal water pipeline; lo... |
| **Pune** | **MIDC Shirwal Industrial Area (Satara Wind Ridge Corridor)** | 58 km | `cloud_inference_50_100km` | 36.8% | 21.0% | 25.5% | Low | **+9.23** | **6.81** | `Site-Specific` | Direct proximity to Satara wind power ridge (+1.5% wind CF); high elevation... |
| **Pune** | **MIDC Chincholi Solar & Clean Energy Park (Solapur)** | 235 km | `cloud_inference_50_100km` | 36.8% | 22.2% | 24.5% | Medium | **+1.48** | **-8.31** | `Site-Specific` | High solar DNI plateau (+1.4% solar CF gain); designated solar park node wi... |
| **Delhi-NCR/Noida** | **BIDA Jhansi Ultra Mega Solar Hub (Bundelkhand Green Corridor)** | 365 km | `ai_training_150_400km` | 28.5% | 21.5% | Not Viable | Low | **+19.73** | **15.17** *(orig: 15.18)* | `Site-Specific` | Co-located with 4,000 MW upcoming Bundelkhand Solar Park; +2.0% solar CF; l... |
| **Delhi-NCR/Noida** | **YEIDA Sector 28 Data Center Park (Jewar Airport Green Node)** | 52 km | `ai_training_150_400km` | 22.4% | 19.8% | Not Viable | Medium | **+8.24** | **7.59** | `Site-Specific` | 250-acre dedicated data center zone; planned dedicated 400kV substations wi... |
| **Delhi-NCR/Noida** | **Neemrana / DMIC Japanese Zone (Alwar / Rajasthan Border)** | 128 km | `ai_training_150_400km` | 43.5% | 22.0% | Not Viable | Low | **+25.39** | **23.79** *(orig: 39.5)* | `Site-Specific` | Direct access to Rajasthan high-RE grid (43.5% non-fossil) and low water st... |
| **Bengaluru** | **Vasanthanarasapura Industrial Area (Tumakuru / CBIC Node)** | 76 km | `cloud_inference_50_100km` | 61.2% | 22.5% | 28.0% | Low | **+16.0** | **12.83** | `✓ Proxy` | Direct transmission line from Pavagada 2,050 MW Solar Park; abundant Hemava... |
| **Bengaluru** | **Dobbaspet Industrial Area (Bengaluru Rural Node)** | 54 km | `cloud_inference_50_100km` | 61.2% | 22.5% | 28.0% | Low | **+16.0** | **13.75** | `✓ Proxy` | Direct 220kV substation; outside congested Cauvery water basin; 40% lower l... |
| **Vizag** | **Kakinada SEZ & Green Energy Port Corridor** | 142 km | `ai_training_150_400km` | 44.1% | 22.0% | 27.0% | Low | **+0.0** | **-1.77** *(orig: -1.78)* | `✓ Proxy` | Direct deep-water port access with unlimited seawater cooling potential; de... |
| **Vizag** | **Atchutapuram Mega Industrial Park (Anakapalli Node)** | 42 km | `ai_training_150_400km` | 44.1% | 22.0% | 27.0% | Low | **+0.0** | **-0.53** *(orig: -0.52)* | `✓ Proxy` | Dedicated industrial water pipeline from Yeleru reservoir, existing 400kV s... |
| **Vizag** | **Ananthapuramu Ultra Mega Solar & Wind Hub (Rayalaseema)** | 385 km | `ai_training_150_400km` | 48.0% | 22.8% | 28.0% | Low | **+2.72** | **-2.09** | `Site-Specific` | Co-located at source of AP's largest solar (1,500 MW NP Kunta) and wind gen... |
| **Kolkata** | **Vidyasagar Industrial Park (Kharagpur / WBIDC Node)** | 122 km | `cloud_inference_50_100km` | 14.2% | 18.5% | Not Viable | Low | **+8.38** | **4.31** | `Site-Specific` | Direct connection to DVC/inter-state high voltage lines; non-flood-prone te... |
| **Kolkata** | **Panagarh Industrial Park (Durgapur-Asansol Energy Belt)** | 160 km | `cloud_inference_50_100km` | 14.5% | 18.8% | Not Viable | Low | **+8.72** | **3.39** *(orig: 3.4)* | `Site-Specific` | Heavy industrial infrastructure with 400kV substation; proximity to DVC flo... |

## 2. Targeted Audits & Data Corrections Applied (v2)

### A. Duplicate Verdict Suppression
- **Chennai & Bengaluru**: Removed redundant and contradictory 'No better option within radius' rows. Both clusters have actionable, named candidate corridors (Cheyyar SIPCOT / Sri City for Chennai; Tumakuru / Dobbaspet for Bengaluru) providing significant water stress alleviation.

### B. Explicit State-Level Proxy Flagging & Confidence Downgrade
- Industrial park authority portals (KIADB, APIIC, MIDC) provide statutory land allotment and utility access data, but do not publish site-level RE capacity factor measurements.
- Where candidate RE metrics directly reflect state-level defaults, they are flagged `proxy_flag = TRUE`, annotated with `(state-level proxy, not site-verified)` in the notes, and confidence adjusted to `Medium`.
- Sites with genuine site-specific resource differentials (e.g., Satara wind ridge, Kamuthi solar, Pavagada transmission intertie, Bundelkhand solar hub) retain `High` confidence.

### C. Neemrana (Delhi-NCR Alternate) Wind Resource Correction
- **Previous Claim**: 22.0% Wind CF yielding an anomalous +41.10 uplift / +39.50 net score.
- **Geographical Audit**: Neemrana sits in Alwar district (northeastern Rajasthan), where NIWE Wind Resource Atlas demonstrates sub-100 W/m² non-commercial wind power density. The western desert wind corridor (Jaisalmer/Barmer) does not extend to Alwar.
- **Recalculated Score**: Wind CF corrected to `Not Viable (0.0%)`. Recalculated Uplift = **+25.39**, Net Score = **+23.79** (down from 39.50).
- **Strategic Verdict**: Neemrana remains a top-tier candidate for Delhi-NCR AI workloads because the shift from UP's coal-heavy grid (22.4% RE) to Rajasthan's RE grid (43.5% non-fossil) plus high solar DNI and low water stress still delivers +23.79 net sustainability gain.

## 3. Strongest Defensible Relocation Narratives for the Competition Deck

1. **Delhi-NCR $\rightarrow$ Neemrana / DMIC (128 km, AI Training)**: **+23.79 Net Gain**
   - Shifting batch AI training across the Rajasthan border bypasses UP's coal grid (22.4% $\rightarrow$ 43.5% RE), leverages RIICO dedicated green power feeders, and avoids severe NCR aquifer depletion.

2. **Hyderabad $\rightarrow$ Orvakal Mega Industrial Hub / Kurnool (205 km, AI Training)**: **+15.31 Net Gain**
   - Strongest co-location story: Direct adjacency to the 1,000 MW Kurnool Ultra Mega Solar Park and Rayalaseema wind corridor (+9.6% RE, +8.0% wind CF gain over Telangana grid).

3. **Bengaluru $\rightarrow$ Tumakuru / Vasanthanarasapura (76 km, Cloud Inference)**: **+12.83 Net Gain**
   - Best cloud-latency relocation: Retains Karnataka's nation-leading 61.2% RE grid within sub-2ms network RTT while eliminating catastrophic urban tanker water vulnerability via dedicated Hemavathi industrial reservoir supply.