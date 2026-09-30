# Case Competition — Project Context

> Canonical context for all agents/sessions. Read this first. Update the Decisions Log and Session Log as work progresses.

## 1. Competition Snapshot
- **Host / Venue:** BIT Mesra (submission via Unstop)
- **Task:** Pick a real-world problem (sustainability / business / social impact / environment) → research → analyse → propose innovative, feasible, sustainable solution
- **Round 2 (current):** 3–5 slide case synopsis submitted on Unstop
- **Round 3 (final):** Live presentation + Q&A before judges
- **Top teams from Round 2 qualify for the final**

## 2. Timeline
| Date | Milestone |
|---|---|
| 28–30 Sep 2026 | Round 2 — synopsis (3–5 slides) submission window |
| 3 Oct 2026 | Round 3 — live final, CAT Hall, BIT Mesra |

## 3. Round 2 — Mandatory Slide Content
- The chosen problem
- Key research & insights
- Analysis of the problem
- Proposed solution
- Expected impact

## 4. Evaluation Criteria (design every slide against these)
- **Problem Understanding** — clarity + depth
- **Research & Analysis** — data quality, insights, analytical approach
- **Innovation** — originality, creativity
- **Feasibility** — practicality, implementation, scalability
- **Sustainability & Impact** — environmental / social / economic, measurable
- **Communication & Presentation** — structure, clarity, visuals, delivery

## 5. Round 3 Notes
- Present solution to a panel, followed by Q&A
- Optional physical model / prototype / mock-up / visual display — must support the case, prove feasibility, or show impact
- Bring: research, data, case examples, implementation strategy

## 6. Hard Rules
- **No plagiarism / misrepresentation** → disqualification. Every stat needs a real, cited source.
- Primary and/or secondary research expected
- Keep the deck to 3–5 slides, pointer-style, visual

## 7. Working Plan (one step at a time)
1. **Idea discovery** — scrape real-world pain points (Python scraper) → shortlist problems
2. **Problem selection** — score candidates against the criteria in §4
3. **Research** — primary (survey/interviews) + secondary (reports, data)
4. **Analysis** — root causes, stakeholders, gaps in existing solutions
5. **Solution design** — innovation, feasibility, business/impact model
6. **Deck** — 5-slide synopsis
7. **Final prep** — prototype (optional), Q&A rehearsal

## 8. Suggested 5-Slide Skeleton
1. Problem — what, who, how big (hook stat)
2. Research & Insights — data + voice-of-people evidence
3. Analysis — root causes, gaps in current solutions
4. Solution — what it is, why it's novel, how it works, feasibility
5. Impact & Roadmap — measurable outcomes, scalability, next steps

## 9. Problem Shortlist Scorecard (1–5 each)
| Candidate | Depth of pain | Data available | Novel angle | Feasible in ~6 mo | Measurable impact | Total |
|---|---|---|---|---|---|---|
| **Informal E-Waste Processing & Kabadiwala Health Hazards** | 4 | 5 | 4 | 4 | 5 | **22/25** |
| **Urban Food Waste & Commercial Kitchen Surplus Redistribution** | 4 | 5 | 4 | 4 | 5 | **22/25** |
| **Student Mental Health, Burnout & Coaching Hub Isolation** | 4 | 5 | 3 | 4 | 4 | **20/25** |
| **10-Min Quick Commerce Plastic & Packaging Waste Surge** | 4 | 5 | 4 | 3 | 4 | **20/25** |
| **Decentralized Groundwater Depletion & Tanker Pricing Shocks** | 4 | 5 | 3 | 3 | 4 | **19/25** |

## 10. Decisions Log
| Date | Decision | Why |
|---|---|---|
| 28 Sep 2026 | Built custom multi-source scraper with zero-PII and offline HTML generator | Fast problem discovery with real-world public evidence and traceable URLs |
| 28 Sep 2026 | Used Reddit RSS feeds alongside PRAW and Hacker News/Google News | Reddit blocks anonymous JSON API (403), RSS feeds provide reliable real-time access |
| 28 Sep 2026 | SentenceTransformer (all-MiniLM-L6-v2) + KMeans deterministic clustering with <30% max size rule | Collapsed 800+ noisy social chatter posts into 12 structured, distinct problem candidates |
| 29 Sep 2026 | Sourced unified National Grid emission factor (0.716 tCO2/MWh) with regional operating margin proxies | CEA unified synchronous grid baseline avoids arbitrary state-by-state baseline discrepancies |
| 29 Sep 2026 | Captured dual RE share definitions (with/without large hydro) | Eliminates silent capacity definition mismatches across CEA vs MNRE datasets |
| 29 Sep 2026 | Differentiated search radii by workload (50–100 km Cloud/Inference vs 150–400 km AI-Training) | Reflects real latency constraints: cloud regions require sub-2ms network RTT while AI training can relocate to high-RE corridors |

## 11. Session Log
- **28 Sep 2026 — Problem Discovery Pipeline Built & Executed**:
  - **What was done**:
    - Created Python 3.11+ modular scraper in `/scraper` with `sources/`, `processing/`, `report/`, CLI `main.py`, and `config.yaml`.
    - Integrated Reddit (PRAW + RSS fallback for r/india, r/mumbai, r/bangalore, r/delhi, etc.), Hacker News (Algolia API), Google News RSS (India-focused), YouTube (yt-dlp/API), and disabled Quora/Twitter stubs.
    - Implemented normalization pipeline: URL + fuzzy title deduplication, bot/removed post removal, URL & noise stripping, zero-PII author SHA-256 hashing.
    - Built pain-point scoring (pain signals + log engagement + persona/metric/place specificity) and theme tagger (Sustainability, Environment, Social impact, Business) with 93.3% accuracy on 30 hand-labelled test cases.
    - Implemented deterministic clustering with `all-MiniLM-L6-v2` + KMeans with 30% max-cluster constraint and 3-quote citation extraction.
    - Built automated Section 9 scorecard generator (1-5 scale) and self-contained offline HTML dashboard.
    - Executed pipeline across all 11 seed topics.
  - **Confirmed-Working vs Bugs/Gaps**:
    - *Confirmed-Working*: Hacker News Algolia API, Google News RSS, YouTube comments scraper, sentence-transformer clustering, PII anonymization, HTML report generator, and full pytest suite (10/10 tests passed).
    - *Real Bugs/Gaps Found & Resolved*: Reddit anonymous `.json` endpoint returned 403 Forbidden due to platform bot restrictions; resolved by implementing official Reddit RSS search endpoints with exponential backoff. Windows terminal CP1252 character map errors resolved with clean ASCII formatting.
    - *Thin/Blocked Sources*: Quora and Twitter/X disabled as intended due to auth/login walls and ToS risk; Pullpush API returned 429 rate limit.
  - **Top 5 Candidate Problems Identified**:
    1. **Informal E-Waste Processing Hazards**: Over 95% of India's 3.2M tons of e-waste handled unscientifically by informal kabadiwalas using open acid baths and burning; massive opportunity for a decentralized aggregation + formalization model.
    2. **Urban Food & Commercial Surplus Waste**: Huge daily volume of banquet/restaurant surplus dumped into landfills despite local food insecurity; high feasibility for decentralized logistics / rapid donation platforms.
    3. **Student Mental Health & Coaching Pressure**: Extreme burnout and isolation among competitive exam aspirants and engineering freshers in hubs like Kota and tier-2 colleges.
    4. **Quick Commerce Packaging Overhead**: 10-minute delivery dark stores generating exponential single-use plastic, cardboard, and ice pack waste without reverse logistics.
    5. **Groundwater Depletion & Tanker Vulnerability**: Severe urban borewell failures in Bangalore/Chennai forcing dependence on unmonitored private water tankers.
  - **Outputs Produced**:
    - `scraper/output/report.html` (Self-contained, offline interactive visual report)
    - `scraper/output/shortlist.md` (Executive summary with citations and scorecards)
    - `scraper/output/problems.csv` & `scraper/output/problems.json` (Full dataset with 800+ traceable records)
    - `scraper/tests/` (10 unit tests for normalization, scoring, tagging, clustering)

- **29 Sep 2026 — Grid Electricity Supply & RE Resource Pipeline Built & Executed**:
  - **What was done**:
    - Built supply-side pipeline in `/grid_data` (`fetch.py`, `build_table.py`, `tests/test_supply_data.py`).
    - Gathered and vetted official power sector supply data for the 8 target data center clusters (Mumbai/Navi Mumbai, Chennai, Hyderabad, Pune, Delhi-NCR/Noida, Bengaluru, Vizag, Kolkata).
    - Produced clean output table [`grid_data/output/cluster_supply_data.csv`](file:///c:/Users/rajch/Desktop/AI/DUO%20-%20CASE%20COMP/grid_data/output/cluster_supply_data.csv) and detailed gaps report [`grid_data/output/gaps.md`](file:///c:/Users/rajch/Desktop/AI/DUO%20-%20CASE%20COMP/grid_data/output/gaps.md).
    - Added unit test suite verifying schema completeness, exact 8-cluster coverage, and strict non-empty number/source pairing rules.
  - **Sourcing Status across the 5 Supply Fields**:
    - **1. Grid Emission Factor (tCO₂/MWh)**: *Fully Sourced (Unified National)* — Central Electricity Authority (CEA) CO2 Baseline Database (Ver 19.0/20.0). Unified National Grid weighted baseline is **0.716 tCO₂/MWh** (Combined Margin: 0.718 tCO₂/MWh). Regional Operating Margins recorded for sensitivity (Western: 0.820, Northern: 0.785, Eastern: 0.890).
    - **2. State RE Share (%)**: *Fully Sourced* — CEA All India Installed Capacity Report. Dual definitions recorded: with Large Hydro (Karnataka 61.2%, TN 53.2%, AP 44.1%, Maharashtra 36.8%, Telangana 34.5%, UP 22.4%, WB 13.8%) and excluding Large Hydro (Karnataka 51.8%, TN 48.6%, AP 36.2%, Maharashtra 26.5%, Telangana 23.8%, UP 13.6%, WB 4.2%).
    - **3. Solar Capacity Factor (%)**: *Fully Sourced* — CERC RE Tariff Regulations, SERC Multi-Year Tariff Orders, and Ultra Mega Solar Park baselines (Pavagada: 22.5%, Kurnool: 22.0%, Southern Plateau/TS: 21.5%, TN/Kamuthi: 21.0%, Maharashtra: 20.8%, UP/NCR: 19.5%, WB/Gangetic: 18.2%).
    - **4. Wind Capacity Factor (%)**: *Fully Sourced with Feasibility Flags* — NIWE Wind Resource Assessment (120m/150m). High yield in TN (31.5% at Muppandal/Kayathar) and Karnataka (28.0% in Chitradurga/Gadag). Sourced and explicitly flagged **Not Viable** (0.0% / blank) for Delhi-NCR/UP and Kolkata/West Bengal due to sub-100 W/m² wind power density.
    - **5. Storage / BESS Cost Signal**: *Sourced (State Auctions + ISTS Benchmarks)* — MSEDCL (Maharashtra: ₹2.38–2.40 Lakh/MW/month), KPTCL (Karnataka: ₹2.49–2.54 Lakh/MW/month), TNGECL (Tamil Nadu: ₹3.15–3.16 Lakh/MW/month). Proxied to SECI National ISTS BESS Benchmark (₹3.04–3.75 Lakh/MW/month) for UP, Telangana, and West Bengal where dedicated standalone state DISCOM auctions have not yet concluded.
  - **Suspicious Numbers & Contradictions Investigated**:
    - *RE Capacity Definitions*: MNRE dashboard reported higher percentages for Karnataka/TN compared to CEA thermal baseline reports because MNRE includes rooftop solar estimates while CEA counts grid-connected generation capacity. Resolved by documenting exact CEA executive summary totals and explicitly reporting both with and without large hydro.
    - *BESS Quoting Metric*: Some general literature cited BESS in ₹/kWh (~₹8–10/kWh standalone), whereas Indian utility procurement contracts (SECI, MSEDCL, KPTCL) are universally awarded on fixed monthly availability charges (**₹/MW/month** or **₹ Lakh/MW/month**). Sourced the exact statutory bidding metrics from award filings.
  - **Outputs Produced**:
    - `grid_data/output/cluster_supply_data.csv` (17 columns, 8 clusters, 100% sourced numbers)
    - `grid_data/output/gaps.md` (Detailed field-by-field and cluster-by-cluster analysis)
    - `grid_data/tests/test_supply_data.py` (4 unit tests, all passed)

- **29 Sep 2026 — Data Center Siting & Relocation Analysis Executed**:
  - **What was done**:
    - Evaluated 2–3 real named alternate locations for all 8 clusters across workload-differentiated radii (50–100 km Cloud/Inference vs 150–400 km AI-training).
    - Added WRI Aqueduct / CGWB groundwater stress ratings and formulated composite sustainability scores (RE 35%, Solar 20%, Wind 25%, Water 20%).
    - Calculated Sustainability Uplift and Net Score after distance penalty: `Net = Uplift - (Distance / Radius Limit) * 5.0`.
    - Generated [`siting_relocation_candidates.csv`](file:///c:/Users/rajch/Desktop/AI/DUO%20-%20CASE%20COMP/siting_relocation_candidates.csv) and [`grid_data/output/siting_relocation_report.md`](file:///c:/Users/rajch/Desktop/AI/DUO%20-%20CASE%20COMP/grid_data/output/siting_relocation_report.md).
    - Built and verified test suite in [`grid_data/tests/test_siting_candidates.py`](file:///c:/Users/rajch/Desktop/AI/DUO%20-%20CASE%20COMP/grid_data/tests/test_siting_candidates.py) (all 9 supply/siting tests passed).
  - **Named Research vs Distance-Rule Fallback**:
    - *All 8 clusters* were successfully populated with real, statutory-backed named industrial corridors (`method: named_research`) including MIDC Dighi, SIPCOT Cheyyar, Kurnool Orvakal, BIDA Jhansi, YEIDA Jewar, KIADB Tumakuru, Kakinada SEZ, and WBIDC Kharagpur. Distance-rule fallback was not required.
  - **"No Better Option Nearby" as a Genuine Finding**:
    - **Chennai**: Tamil Nadu is already at 53.2% RE and 31.5% wind CF. Nearby sites (Cheyyar, Sri City) provide water stress mitigation, but cannot meaningfully outperform Chennai's existing grid mix and subsea cable proximity.
    - **Bengaluru**: Karnataka grid is already India's highest at 61.2% RE. Relocating to Tumakuru (76 km) or Dobbaspet (54 km) is strategically advantageous for urban water relief and land costs, but grid RE is already maximal.
  - **Data Quality & Deck Validation Notes**:
    - *Neemrana / Alwar (Delhi-NCR alternate)*: Relies on Rajasthan state grid mix (43.5% RE). While geographically close (128 km), crossing the UP/Haryana-Rajasthan state boundary requires inter-state open access or direct connectivity to RIICO industrial feeder.
    - *BIDA Jhansi (Noida alternate)*: High solar potential (Bundelkhand 4 GW park), but 365 km distance makes it strictly suitable for batch AI training, not low-latency cloud regions.
  - **Outputs Produced**:
    - `siting_relocation_candidates.csv` (14 columns, 22 candidate evaluations across 8 clusters)
    - `grid_data/output/siting_relocation_report.md` (Detailed strategic findings report)
    - `grid_data/tests/test_siting_candidates.py` (5 unit tests, all passed)

- **29 Sep 2026 — Siting Candidates Audit, Duplicate Suppression & Proxy Remediation (v2)**:
  - **What was done & What changed in the 3 targeted fixes**:
    - **Fix 1 (Duplicate Verdict Suppression)**: Eliminated the contradictory "No better option within radius" rows from Chennai and Bengaluru. Both clusters now consistently present their verified named candidate corridors (Cheyyar SIPCOT / Sri City for Chennai; Tumakuru / Dobbaspet for Bengaluru) that solve critical urban water stress without asserting conflicting 0.0 uplift verdicts. No cluster now has more than one verdict type.
    - **Fix 2 (Explicit State-Level Proxy Flagging & Confidence Downgrade)**: Added `proxy_flag` column (TRUE/FALSE) and audited all rows against parent state baselines. Identified 6 candidates (MIDC Chakan, Orvakal Hub, Tumakuru Vasanthanarasapura, Dobbaspet, Kakinada SEZ, Atchutapuram) whose RE metrics were unverified state-average copies. Appended `(state-level proxy, not site-verified)` to `notes` and downgraded confidence from High to `Medium`. High confidence is reserved strictly for locations with verified site-specific resource differentials.
    - **Fix 3 & 4 (Neemrana Wind CF Correction & Score Traceability)**: Audited Neemrana's headline 22.0% wind CF against NIWE Wind Resource Assessment. Confirmed Neemrana (Alwar district, NE Rajasthan) has non-commercial wind power density (<100 W/m²), disproving the application of western desert (Jaisalmer/Barmer) wind averages. Corrected Neemrana wind CF to `Not Viable (0.0%)`, added `original_net_score` column (recording previous `39.50`), and recomputed its net score to **+23.79** (uplift: +25.39, distance penalty: 1.60).
  - **Neemrana Credibility Assessment**:
    - *Verdict*: Neemrana **survived as a highly credible, defensible candidate** for batch AI training. Although its headline net score was trimmed from 39.50 to 23.79, crossing the UP border into Rajasthan's 43.5% non-fossil grid (+21.1% RE jump), combined with high solar DNI (22.0% CF) and low groundwater stress, still yields the single highest net sustainability gain in the dataset without relying on unviable local wind claims.
  - **Strongest Defensible Relocation Stories for the Competition Deck**:
    1. **Delhi-NCR $\rightarrow$ Neemrana / DMIC (128 km, AI Training)**: Highest net score gain (**+23.79**) via interstate grid decarbonization (22.4% $\rightarrow$ 43.5% RE) and relief from NCR's critical aquifer depletion.
    2. **Hyderabad $\rightarrow$ Orvakal Mega Industrial Hub / Kurnool (205 km, AI Training)**: Most defensible *resource co-location* narrative (**+15.31 net score**), co-locating batch AI compute directly adjacent to the 1,000 MW Kurnool Ultra Mega Solar Park and Rayalaseema wind corridor (+9.6% RE, +8.0% wind CF gain).
    3. **Bengaluru $\rightarrow$ Tumakuru / Vasanthanarasapura (76 km, Cloud/Inference)**: Best *low-latency cloud region* narrative (**+12.83 net score**), retaining Karnataka's peak 61.2% RE grid within sub-2ms network RTT while eliminating severe urban tanker water risks via statutory Hemavathi reservoir allocations.
  - **Outputs Produced & Verified**:
    - `siting_relocation_candidates_v2.csv` (16 columns, 20 clean rows, fully traceable)
    - `grid_data/output/siting_relocation_report.md` (Audited findings report)
    - `grid_data/tests/test_siting_candidates.py` (8 unit tests verifying duplicate suppression, proxy annotations, Neemrana wind correction, and scoring mechanics; 12/12 test suite passing)

## 12. Team / Roles
- _(fill in: names, roles, who owns research / deck / prototype / Q&A)_

    - **3. 3,000 MW Target Master Plan (`FAC-003a`)**: **Partially Verified / Aspirational Vision (Single-Source Corporate Announcement)**. Sourced from Reliance Chairman's AGM address. Widely re-reported across media, but lacks independent statutory filings (e.g. MoEFCC EIA clearances or CEA interconnection approvals) for the full 3 GW campus. Commissioning window: **post-2030 (multi-phase buildout)**. Capacity basis: **`facility_power`**.
  - **Can Jamnagar Demand-Side Data be Considered Fully Verified?**:
    - **Verdict**: **Tiered Verification Achieved**. The near-term anchor capacity (**168 MW Meta**) is **100% verified and contractual**. The **1,000 MW Phase 1** is a credible corporate roadmap (with initial 120 MW fleet online). The **3,000 MW Master Plan** must be presented as an *aspirational multi-gigawatt ceiling (post-2030)*, not an active or committed grid draw.
    - **What is still missing for statutory verification**: Official MoEFCC Environmental Impact Assessment (EIA) public hearings and statutory GETCO / CTU grid transmission evacuation clearances for the full 3,000 MW capacity.
  - **Nesting & Double-Count Integrity**:
    - Re-confirmed: `FAC-003c` (168 MW) is nested in `FAC-003b` (1,000 MW), which is nested in `FAC-003a` (3,000 MW). `is_nested = True` and `counts_toward_total = False` for nested rows guarantees zero double-counting. Low scenario = 1,000 MW; High scenario = 3,000 MW.
  - **Outputs Produced & Tested**:
    - `jamnagar_facilities.csv` (Same schema as Facilities_Reference + `commissioning_year_estimate`)
    - `jamnagar_verification_notes.md` (Executive audit, basis reconciliation, and slide presentation guide)
    - `grid_data/tests/test_jamnagar_facilities.py` (5 unit tests verifying capacity sources, nesting consistency, timeline fields, and verification status; full test suite 17/17 passing)

- **29 Sep 2026 — Gujarat (Jamnagar) Grid Electricity Supply Data Integrated**:
  - **Sourcing Status Across the 5 Supply Fields**:
    - **1. Grid Emission Factor (tCO₂/MWh)**: *Fully Sourced (Unified National)* — Central Electricity Authority (CEA) CO2 Baseline Database (Ver 19.0/20.0). Unified National Grid baseline is **0.716 tCO₂/MWh** (Combined Margin: 0.718 tCO₂/MWh; Western Region Operating Margin proxy: 0.820 tCO₂/MWh).
    - **2. State RE Share (%)**: *Fully Sourced* — CEA All India Installed Capacity Report. Dual definitions: **57.4% with Large Hydro >=25MW** (33,390 MW non-fossil / 58,220 MW total) and **54.0% excluding Large Hydro** (31,400 MW RES). Highest non-hydro RE share among all 9 clusters.
    - **3. Solar Capacity Factor (%)**: *Fully Sourced* — CERC / GERC Multi-Year Tariff Orders and Charanka / Coastal Saurashtra regional benchmark: **23.0% CUF** (highest among all 9 clusters, surpassing Pavagada 22.5% and Kurnool 22.0%).
    - **4. Wind Capacity Factor (%)**: *Fully Sourced* — National Institute of Wind Energy (NIWE) Wind Resource Assessment at 120m/150m Hub Height for the Coastal Saurashtra / Gulf of Kutch / Jamnagar Class I wind corridor: **32.0% CUF** (highest national yield, exceeding Tamil Nadu Muppandal Pass 31.5%).
    - **5. Storage / BESS Cost Signal**: *Fully Sourced (State Auction Awards)* — GUVNL Standalone BESS Auction Filings & GERC Tariff Orders: **₹2.10–2.32 Lakh/MW/month** (discovered in GUVNL Phase VIII/IX 450 MW / 900 MWh tenders with VGF support, lowest storage tariff nationally).
  - **Sanity-Check & Headline "Best Site" Caveats for the Deck**:
    - Coastal Gujarat emerges with India's highest combined RE resource metrics (23.0% solar CF, 32.0% wind CF, 57.4% state RE mix, ₹2.10 Lakh/MW/month BESS signal).
    - *Critical Distinction for Judges*: Reliance Jamnagar is an industrial **captive mega-complex** with dedicated on-site seawater desalination and private 5,000-acre solar/BESS generation. The headline narrative should celebrate its world-class resource endowment while clarifying that it operates on captive infrastructure rather than third-party utility DISCOM open-access.
  - **Outputs Produced & Verified**:
    - `grid_data/output/cluster_supply_data.csv` (17 columns, exactly 9 clusters, all 8 pre-existing rows byte-for-byte preserved)
    - `grid_data/output/gaps.md` (Updated comprehensive 9-cluster sourcing and gaps report)
    - `grid_data/tests/test_supply_data.py` (6 unit tests, 100% passing)

- **29 Sep 2026 — [SUPERSEDED - DO NOT USE] 24/7 RE Matching Model Finalization**:
  - *Superseded Status*: Output reported 8.41–20.50 Mt CO₂ avoided. Superseded due to two methodological errors: (1) dropped the 0.65 utilization factor inflating demand by ~54%, and (2) disconnected 76–92% RE-match percentages that bypassed the established blended formula. See corrected session log below.

- **29 Sep 2026 — 24/7 Renewable Energy Matching Model Correction & Strategic Gap Reframing**:
  - **Core Corrections Implemented**:
    - **1. Restored 0.65 Data Center Utilization Factor**: Demand formula now correctly evaluates $\text{Demand (GWh)} = \text{MW} \times 8,760 \times 0.65 / 1,000$ (referencing `Assumptions!$B$5` $\times$ `Assumptions!$B$6`). Corrects continuous load baselines to **19,684 GWh/yr (Low / Today)** and **48,952 GWh/yr (High / Future)** across the 9 clusters.
    - **2. Strict Blended RE Formula Enforcement**: RE match % is computed exclusively via the model's established formula: $\text{Blended RE \%} = \text{Solar\_CF} \times 0.6 + \text{Wind\_CF} \times 0.4$ (or $100\% \times \text{Solar\_CF}$ where wind is not viable). Un-stored blended generation yields realistic hourly matching ceilings between **18.2% and 26.6%**.
    - **3. Dual Parallel Jamnagar Scenarios Preserved & Labeled**:
      - *Conservative (Empirical Siting Baseline)*: Wind CF = 24.0% $\rightarrow$ **23.4% Blended Match** $\rightarrow$ **76.6% 24/7 Matching Gap** $\rightarrow$ **0 avoided CO₂**.
      - *Claimed Upside (Regional Macro-Corridor)*: Wind CF = 32.0% $\rightarrow$ **26.6% Blended Match** $\rightarrow$ **73.4% 24/7 Matching Gap** $\rightarrow$ **0 avoided CO₂**.
    - **4. Mathematical Reality of Avoided CO₂**: In 8 of 9 clusters, dedicated un-stored solar+wind generation (18.2%–26.6% blended CF) sits *below* the state grid's legacy non-fossil baseline mix (22.4%–61.2%). Under standard greenhouse gas accounting, un-stored procurement produces **0 avoided CO₂** against the state grid.
    - **5. Kolkata Positive Exception**: Kolkata is the sole cluster where dedicated RE (18.2% solar) outperforms the coal-dominant West Bengal grid (13.8% non-fossil share), delivering **7,606 t CO₂/yr (Low)** to **12,090 t CO₂/yr (High)** avoided.
  - **New Deck Headline Finding: The 75%–82% 24/7 RE-Matching Gap**:
    - *Strategic Thesis for Judges*: A pure un-stored solar+wind PPA buildout leaves an average **77.8% 24/7 deficit** across India's data centers. The true bottleneck in greening India's AI infrastructure is not generation capacity, but **temporal intermittency**—proving the indispensability of long-duration BESS (Battery Energy Storage Systems) and dynamic green grid orchestration.
  - **Clean Output Summary Across Clusters (Slide-Ready)**:
    - **Mumbai / Navi Mumbai**: 4,365 GWh (Low) | 13,191 GWh (High) | 36.8% Grid RE | 22.1% Matched | **77.9% Gap** | 0 CO₂ Avoided
    - **Chennai**: 1,090 GWh (Low) | 4,023 GWh (High) | 53.2% Grid RE | 25.2% Matched | **74.8% Gap** | 0 CO₂ Avoided
    - **Hyderabad**: 862 GWh (Low) | 4,279 GWh (High) | 34.5% Grid RE | 20.5% Matched | **79.5% Gap** | 0 CO₂ Avoided
    - **Pune**: 256 GWh (Low) | 826 GWh (High) | 36.8% Grid RE | 22.1% Matched | **77.9% Gap** | 0 CO₂ Avoided
    - **Delhi-NCR / Noida**: 871 GWh (Low) | 2,010 GWh (High) | 22.4% Grid RE | 19.5% Matched | **80.5% Gap** | 0 CO₂ Avoided
    - **Bengaluru**: 610 GWh (Low) | 1,464 GWh (High) | 61.2% Grid RE | 24.7% Matched | **75.3% Gap** | 0 CO₂ Avoided
    - **Vizag**: 5,694 GWh (Low) | 5,694 GWh (High) | 44.1% Grid RE | 24.0% Matched | **76.0% Gap** | 0 CO₂ Avoided
    - **Kolkata**: 241 GWh (Low) | 384 GWh (High) | 13.8% Grid RE | 18.2% Matched | **81.8% Gap** | **7,606–12,090 t CO₂ Avoided**
    - **Jamnagar (Cons)**: 5,694 GWh (Low) | 17,082 GWh (High) | 57.4% Grid RE | 23.4% Matched | **76.6% Gap** | 0 CO₂ Avoided
    - **National Total (Cons)**: **19,684 GWh (Low)** | **48,952 GWh (High)** | 40.0% Avg Grid RE | 22.2% Avg Matched | **77.8% Avg Gap** | **7,606–12,090 t CO₂ Avoided**
  - **Outputs Produced & Verified**:
    - `datacentre_RE_matching_model.xlsx` (`Assumptions`, `Demand_Supply_Model`, `Slide_Ready_Summary` with 100% dynamic formulas)
    - `grid_data/build_matching_model.py` (Fully automated model generation script)
- **30 Sep 2026 — Water Demand & Water-Positive Cooling Subsidiary Dataset Integrated**:
  - **What was done & Core Sourcing Standard**:
    - **1. Water Stress Classification per Cluster**: Sourced district-level groundwater categories from Central Ground Water Board (CGWB) Dynamic Ground Water Resources Assessments and WRI Aqueduct 4.0 Water Risk Atlas.
    - **2. WUE Assumption Transparency**: Applied a single, transparent industry-standard WUE factor of **1.25 L/kWh (1.25 ML/GWh)** across standard evaporative/chilled-water cooling architectures (matching Uptime Institute, AWS, and Microsoft disclosed 1.0–1.8 L/kWh benchmarks), avoiding false per-cluster precision.
    - **3. Annual Water Demand Estimation**: Converted verified GWh demand directly into annual Megalitres ($\text{Demand ML} = \text{Demand GWh} \times 1.25$), scaling from **24,605 ML/yr (Low / Today)** to **61,190 ML/yr (High / 2030 Pipeline)** nationally.
    - **4. 2x2 Priority Matrix Findings (Top 3 High-Priority Clusters)**:
      - **Bengaluru** (**High Priority**): CGWB Over-Exploited; acute municipal drinking water tanker crisis; 1,830 ML/yr future cooling draw creates direct citizen conflict.
      - **Delhi-NCR / Noida** (**High Priority**): CGWB Over-Exploited Yamuna basin; 2,512 ML/yr future draw in Greater Noida severely exacerbates critically depleted aquifers.
      - **Chennai** (**High Priority**): CGWB Over-Exploited / 2019 Day Zero legacy; 5,025 ML/yr pipeline demand requires strict municipal effluent substitution.
    - **5. Water-Positive Cooling Recommendation**:
      - **Precedent Grounding**: Sourced Chennai CMWSSB's operational 45 MLD Tertiary Treatment Reverse Osmosis (TTRO) industrial water pipeline and STT GDC / NTT municipal STP recycled water tie-ups.
      - **Proposed Policy Target**: 100% substitution of freshwater cooling with tertiary-treated municipal/industrial effluent for all new data center approvals in High water-stress districts.
    - **Scope Discipline**: Kept strictly to a single clean subsidiary table (`water_cooling_subsidiary.csv`) to serve as a focused slide bullet rather than expanding into a second parallel workstream.
  - **Outputs Produced & Verified**:
    - `data/water_cooling_subsidiary.csv` & `water_cooling_subsidiary.csv` (8 columns, 9 clusters, fully traceable)
    - `grid_data/build_water_subsidiary.py` (Deterministic generation script)
    - `grid_data/tests/test_water_cooling.py` (6 unit tests, full test suite 32/32 passing)

- **30 Sep 2026 — Jamnagar Water Desalination Scope Audit & Correction**:
  - **Scope Audit & Findings**:
    - *Overgeneralization Root Cause*: An earlier summary had extrapolated the confirmed **168 MW Meta anchor facility's** desalinated seawater cooling claim to the entire 1,000–3,000 MW Jamnagar campus, erroneously labeling the full multi-GW cluster as "100% Captive Desalination" and "Low Priority".
    - *What Was Verified vs. Corrected*:
      - **Confirmed Desalinated Scope**: 168 MW Meta anchor facility (`FAC-003c`, 956.6 GWh/yr $\rightarrow$ **1,195.8 ML/yr**) is explicitly confirmed via bilateral corporate releases to use desalinated seawater cooling.
      - **Unconfirmed Exposure Scope**: The remaining **832 MW in Phase 1** (4,737.4 GWh/yr $\rightarrow$ **5,921.8 ML/yr**) and up to **2,832 MW in the Master Plan** (16,125.4 GWh/yr $\rightarrow$ **20,156.8 ML/yr**) have not been independently confirmed with statutory seawater intake/EIA approvals.
    - *Priority Reclassification*: Jamnagar updated to **Medium-High Priority (Partial Desal / 832–2,832 MW Unconfirmed)**, situated in CGWB Semi-Critical arid Saurashtra.
    - *Integrity Check Across Dataset*: Audited all other 8 clusters; confirmed no other cluster makes an unverified campus-wide technology assumption.
  - **Outputs Updated & Tested**:
    - `data/water_cooling_subsidiary.csv` and `water_cooling_subsidiary.csv` (Jamnagar row updated)
    - `grid_data/tests/test_water_cooling.py` (Added `test_jamnagar_desal_scope_honesty`, 34/34 tests passing)

- **30 Sep 2026 — Interactive Impact & Siting Explorer Dashboard Built & Verified (`impact_explorer.html`)**:
  - **What was built**:
    - Created single, self-contained, offline-capable interactive HTML file (`impact_explorer.html`) allowing non-technical viewers and competition judges to explore the problem, model, and siting solution without opening slides.
    - Built comprehensive Playwright automated test suite in `test_impact_explorer.py` (5/5 unit tests passed in 8.5s).
  - **Build Status across the 6 Project Requirements (Clean vs. Rework)**:
    - **Item 1: Baseline View Without Intervention**: *Built Clean* — Interactive dashboard featuring all 9 clusters with live sliders for utilization (40%–95%), solar:wind blend (0:100 to 100:0), and WUE (0.5–2.5 L/kWh). Real-time mathematical recomputation perfectly matches the corrected core model (Kolkata gap = 81.8% at default, avoided CO₂ = 7,606–12,090 t/yr; other 8 clusters = 0 t/yr avoided CO₂ due to un-stored RE sitting below legacy state grid non-fossil shares).
    - **Item 2: Siting Relocation & Site Suitability Index (SSI) Calculator**: *Built Clean* — 4 adjustable weight multipliers (Grid Decarbonisation, Water Stress, RE Resource Quality, Land & Proximity Penalty) dynamically re-ranking all 20 candidate corridors from `siting_relocation_candidates_v3.csv`. Default weights exactly replicate the locked deck scores (Kurnool +15.31, Sri City +9.61, Tumakuru +12.83, Dobbaspet +13.75). Dedicated feature card explains why Kurnool wins (1,000 MW Ultra Mega Solar Park co-location, 44.1% RE, 27.0% wind CF) and separate card details the Bengaluru $\rightarrow$ Tumakuru water-only paradox ($\Delta\text{RE} = 0.0\%$, uplift driven 100% by municipal water conflict relief).
    - **Item 3: Before / After Comparison View**: *Built Clean* — Side-by-side cards for the 3 primary relocation cases (Hyderabad $\rightarrow$ Kurnool, Chennai $\rightarrow$ Sri City, Bengaluru $\rightarrow$ Tumakuru). Features prominent "The Honest Truth: What Doesn't Change" callout confirming the ~75%–80% deficit persists everywhere under un-stored RE and that siting cannot eliminate solar nighttime intermittency.
    - **Item 4: Interactive India Map View**: *Required Minor Rework* — SVG map of India with dynamically sized cluster nodes and animated curved relocation vectors. During automated testing, SVG background silhouette path intercepted pointer events on cluster nodes; resolved by assigning `pointer-events="none"` to background geometry and `pointer-events="all"` to interactive cluster nodes and arrows. Click drawer displays complete cluster dossier with statutory citations.
    - **Item 5: Methodology & Glossary Drawer**: *Built Clean* — Slide-out modal with 1-sentence plain-English definitions of all 7 core terms, exact mathematical derivation formulas, and full statutory source audit matrix (CEA, CERC, NIWE, CGWB, WRI, state DISCOM auctions).
    - **Item 6: Visual & Interaction Design System**: *Built Clean* — State-of-the-art dark slate palette (`#070B14`, `#0B1120`, `#111A2E`) with emerald/teal clean energy accents and amber gap indicators. Glassmorphic cards, custom slider controls, dual progress bars, and zero external CDN/font network dependencies (100% offline-functional).
- **30 Sep 2026 — Master Context Audit & Reconciliation (`CASE_COMP_MASTER_CONTEXT.md` vs `impact_explorer.html`)**:
  - **What was done**:
    - Conducted comprehensive audit of `impact_explorer.html` against newly available canonical `CASE_COMP_MASTER_CONTEXT.md`.
    - Applied surgical direct edits to `impact_explorer.html` without rebuilding from scratch.
    - Updated Playwright test suite `test_impact_explorer.py` with 6 rigorous assertions covering default-state math, Jhansi 600 MW correction, Jamnagar water split & dual wind scenarios, map distances, and methodology audit trail.
  - **Audit Status across the 5 Review Items (Real Drift vs. Already Correct)**:
    - **Item 1: Default/Baseline Numbers & Capacities**: *Already Correct* — All 9 clusters and national aggregates matched the master context table byte-for-byte at default settings (19,684 GWh Low / 48,952 GWh High demand, 77.8% national gap, Kolkata 81.8% gap and 7,606–12,090 t avoided CO₂, 0 avoided CO₂ in other 8 clusters). Enhanced UI by surfacing locked total capacity figures (3,457 MW Today $\rightarrow$ 8,597 MW 2030 Pipeline, 2.5× growth) in the hero and national summary strips.
    - **Item 2: Siting/SSI Section & Caveats**: *Real Drift Corrected* — Candidate BIDA Jhansi previously cited the regional aggregate "4,000 MW upcoming Bundelkhand Solar Park"; corrected to the site-specific **600 MW Jhansi Solar Park** (TUSCO/THDC-UPNEDA JV). Siting scores at default weights were verified already exact (Kurnool +15.31, Sri City +9.61, Tumakuru +12.83, Dobbaspet +13.75, Neemrana +23.79, Jhansi +15.17). Added interactive Jamnagar dual-scenario wind CF toggle (Conservative 24.0% GERC vs. Claimed 32.0% NIWE).
    - **Item 3: Jamnagar Water Desalination Scope**: *Real Drift Corrected* — The UI previously displayed aggregate water demand without breaking out the confirmed scope. Sourced the exact split: **Confirmed Desalinated** (168 MW Meta anchor = 1,196 ML/yr mitigated) vs. **Unconfirmed Exposure** (832 MW Phase 1 = 5,922 ML/yr to 2,832 MW Master Plan = 20,157 ML/yr in CGWB Semi-Critical arid Saurashtra). Explicitly labeled as **Medium-High Priority** across cards and map drawer (confirming "Low Priority" is never shown).
    - **Item 4: Map View Capacities & Relocation Distances**: *Already Correct* — All 9 cluster SVG dots scale proportionally to verified facility MW ($r \propto \sqrt{\text{MW}}$). Relocation vectors match locked distances exactly: Hyderabad $\rightarrow$ Kurnool (205 km), Chennai $\rightarrow$ Sri City (72 km), Bengaluru $\rightarrow$ Tumakuru (76 km), Delhi-NCR $\rightarrow$ Neemrana (128 km).
    - **Item 5: Methodology Panel & Superseded Claims Audit**: *Real Drift Corrected / Enhanced* — Added a dedicated red-alert card to the Methodology Panel: `⚠️ Audit Trail: Corrected & Superseded Claims`, explicitly warning against the discarded 8.4–20.5 Mt CO₂ model, unflagged 4,000 MW Jhansi claims, unflagged 22% Neemrana wind, unflagged 32% Jamnagar wind, and campus-wide desalination claims. Confirmed no superseded number remains anywhere in active code or calculations.
  - **Regression Test Verification**: Full test suite passed with 40/40 tests passing (6 browser tests in `test_impact_explorer.py` + 34 unit tests in `grid_data/tests/`).

- **30 Sep 2026 — UI & GIS Enhancements: Light/Dark Mode, Card Info Buttons, and Survey of India Boundary Fix**:
  - **What was done (UI-Only, Zero Data/Model Changes)**:
    - **1. Survey of India-Aligned Official Map Boundary Fix**:
      - Replaced the low-fidelity hand-approximated polygon with the verified official Survey of India boundary dataset across all **36 States and Union Territories** (including complete depictions of Ladakh, Jammu & Kashmir, Arunachal Pradesh, Andaman & Nicobar Islands, and Lakshadweep).
      - Added high-precision mainland outline (`#indiaOutline`, 1,006 points) and interactive state boundary paths (`.state-path`, 4,336 points across 36 entities).
      - Mathematically verified via Python point-in-polygon tests (`verify_clusters.py`) that all 9 data center cluster coordinates (Mumbai, Chennai, Hyderabad, Pune, Delhi-NCR, Bengaluru, Kolkata, Vizag, Jamnagar) and candidate relocation corridors (Kurnool, Sri City, Tumakuru, Neemrana, Dobbaspet, Jhansi) land precisely inside their correct state polygons.
      - Added dynamic state hover feedback (`#hoverStateName`) displaying the active state name and Survey of India alignment badge.
    - **2. Light / Dark Mode Theme Toggle**:
      - Built a header toggle button (`#themeToggleBtn`) with sun/moon icons seamlessly switching between Dark Slate (`#070B14`, `#111A2E`) and Clean Light (`#F8FAFC`, `#FFFFFF`) palettes.
      - Maintained identical clean-energy emerald/teal and amber accent colorways for continuity.
      - Ensured state persistence across tabs and page reloads via `localStorage` (`dc_impact_theme`).
    - **3. Contextual Card Info ("i") Buttons Across All Sections**:
      - Added non-intrusive, low-opacity info buttons (`.card-info-btn`) to every card across the application (Hero KPIs, Sensitivity Sliders, National Comparison Chart, 9 Cluster Cards, SSI Weights, Candidate Matrix Table, Deep Dives, Before/After Comparison Cards, Honest Truth box, Map Canvas, and Map Drawer).
      - Clicking any info icon opens a modal dialog (`#cardInfoModal`) with card-specific title, plain-English explanation, exact governing mathematical formula, and a direct link to the fuller methodology drawer.
      - Strict event decoupling (`event.stopPropagation()`) guarantees that opening info buttons never disrupts slider states, triggers recalculation, or mutates any displayed data.
  - **Test Suite Verification**:
    - Expanded Playwright test suite in `test_impact_explorer.py` to 9 comprehensive tests:
      - `test_accurate_india_map_and_survey_of_india_boundaries`: Asserts high-fidelity boundary paths (>5k chars), 36 state paths, presence of sensitive border territories, and interactive hover.
      - `test_light_dark_theme_toggle_and_persistence`: Asserts theme switching, contrast, and persistence across reloads.
      - `test_card_info_buttons_across_sections_no_data_alteration`: Asserts info button coverage, modal content fidelity, and zero data alteration.
    - Verified full workspace test suite: **43/43 tests passing** (9 in `test_impact_explorer.py` + 34 in `grid_data/tests/`).
    - Browser subagent visual inspection confirmed responsive, defect-free rendering in both light and dark modes.

## 12. Team / Roles
- _(fill in: names, roles, who owns research / deck / prototype / Q&A)_






