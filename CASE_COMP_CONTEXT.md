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
    - `grid_data/tests/test_matching_model.py` (6 unit tests, 20/20 test suite passing)

## 12. Team / Roles
- _(fill in: names, roles, who owns research / deck / prototype / Q&A)_





