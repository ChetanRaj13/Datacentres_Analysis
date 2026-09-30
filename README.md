# India AI & Data Center Decarbonization Roadmap (Case Competition)

This repository contains the complete quantitative research, data engineering pipelines, spatial siting optimization models, and an interactive web dashboard for decarbonizing India's AI and hyperscale data center infrastructure by 2030.

---

## 📁 Repository Directory Structure

```text
DUO - CASE COMP/
├── README.md                           # Master project documentation & execution guide
├── CASE_COMP_MASTER_CONTEXT.md         # Canonical project bible & locked quantitative context
├── CASE_COMP_CONTEXT.md                # Comprehensive problem formulation & session log
├── impact_explorer.html                # Interactive 24/7 Clean Energy & Siting Web Application
├── datacentre_RE_matching_model.xlsx   # Sited 24/7 Hourly Matching & Grid Supply Financial Model
│
├── data/                               # Clean Structured Datasets
│   ├── DataCentre/                     # Facilities, Capacity & Market Demand Data
│   │   ├── facilities_clean.csv        # Clean individual facility registry (30+ facilities)
│   │   ├── cluster_totals.csv          # 9-cluster capacity & demand totals (Low vs High MW)
│   │   └── city_market_totals.csv      # Metro-level capacity & market share baselines
│   ├── water_cooling_subsidiary.csv    # CGWB & WRI water stress + WUE demand dataset (9 clusters)
│   └── raw_test/                       # Test fixture payloads for scraper connectors
│
├── grid_data/                          # Grid Analytics & Spatial Siting Optimization Pipeline
│   ├── raw/                            # Baseline CEA, CERC, NIWE, SECI raw feeds
│   ├── output/                         # Processed supply datasets & relocation rankings
│   │   ├── cluster_supply_data.csv     # 9-cluster RE mix, CEA emission factors, solar/wind CF
│   │   ├── siting_relocation_candidates_v3.csv  # Sited alternate corridors (v3 audited)
│   │   ├── siting_relocation_candidates_v2.csv  # Siting candidates v2 dataset
│   │   ├── siting_relocation_candidates.csv     # Baseline candidate ranking dataset
│   │   ├── siting_relocation_report.md          # Spatial relocation analysis report
│   │   └── gaps.md                              # Data gap & proxy methodology documentation
│   ├── tests/                          # Grid model & supply unit test suite
│   │   ├── test_matching_model.py      # Unit tests for 24/7 RE matching model & formulas
│   │   ├── test_siting_candidates.py   # Unit tests for spatial siting & score formulas
│   │   ├── test_supply_data.py         # Unit tests for 9-cluster grid supply data
│   │   └── test_water_cooling.py       # Unit tests for water demand & cooling priority data
│   ├── build_matching_model.py         # Generates datacentre_RE_matching_model.xlsx
│   ├── build_table.py                  # Generates cluster_supply_data.csv
│   ├── build_water_subsidiary.py       # Generates water_cooling_subsidiary.csv
│   ├── fetch.py                        # Automated data fetching & extraction
│   └── siting_analysis.py              # Spatial relocation & sustainability scoring engine
│
├── scraper/                            # Problem Discovery & NLP Extraction Pipeline
│   ├── main.py                         # CLI entry point for problem mining
│   ├── config.yaml                     # Scraping keywords, limits & source toggles
│   ├── requirements.txt                # Python dependencies for scraper
│   ├── data/raw/                       # Ingested unstructured public forum data
│   ├── output/                         # Ranked sustainability problems & reports
│   │   ├── problems.csv                # Filtered problem candidate dataset
│   │   ├── problems.json               # Structured JSON export
│   │   ├── shortlist.md                # Curated shortlist of top problem vectors
│   │   └── report.html                 # HTML summary report
│   ├── processing/                     # NLP clustering, scoring & feasibility modules
│   ├── report/                         # Problem shortlist report generator
│   ├── sources/                        # News & community forum connectors (Reddit, News, HN)
│   └── tests/                          # Scraper unit & integration tests
│
├── tests/                              # Deliverable End-to-End Validation Suite
│   └── test_impact_explorer.py         # Playwright validation suite for impact_explorer.html
│
└── docs/                               # Design & Architecture Specifications
    └── DESIGN-apple.md                 # UI/UX Apple design system specification
```

---

## 🚀 Key Deliverables & How to Run

### 1. Interactive Web Application
Open [`impact_explorer.html`](impact_explorer.html) in any modern web browser to interactively explore:
- **Baseline 24/7 RE Deficit Calculator**: Dynamic live simulation of un-stored generation ceilings vs storage-backed deficits across all 9 clusters.
- **Interactive Spatial Siting & SSI Calculator**: Dynamic multi-criteria re-ranking of all 20 candidate relocation corridors.
- **Water Cooling Demand Simulator**: Dynamic cooling intensity assumptions and municipal water stress impact.
- **Accurate Vector India Map & State Breakdown**: High-precision SVG visualization of cluster power demand and solar/wind potential.

### 2. 24/7 RE Matching Model Build
Generates [`datacentre_RE_matching_model.xlsx`](datacentre_RE_matching_model.xlsx) with `Assumptions`, `Demand_Supply_Model`, and `Slide_Ready_Summary` sheets.
```bash
python grid_data/build_matching_model.py
```

### 3. Spatial Siting & Relocation Analysis
Evaluates 20 candidate corridors for batch AI compute vs latency-sensitive cloud workloads.
```bash
python grid_data/siting_analysis.py
```

### 4. Supply Table & Water Subsidiary Generators
Builds the 9-cluster state electricity supply dataset and water cooling subsidiary dataset:
```bash
python grid_data/build_table.py
python grid_data/build_water_subsidiary.py
```

### 5. Automated Test Suite (36 Automated Tests)
Validates schema integrity, financial formulas, Playwright UI rendering, and verification standards.
```bash
python -m pytest tests/ grid_data/tests/ -v
```

---

## 📊 Core Deliverables & Reference Index

| Deliverable | Location | Description |
|:---|:---|:---|
| **Interactive Explorer** | [`impact_explorer.html`](impact_explorer.html) | Standalone interactive web dashboard with live sensitivity sliders, vector map, and SSI model. |
| **Executive Matching Model** | [`datacentre_RE_matching_model.xlsx`](datacentre_RE_matching_model.xlsx) | 3-sheet financial/engineering model proving the **75%–82% RE-Matching Gap**. |
| **Master Canonical Context** | [`CASE_COMP_MASTER_CONTEXT.md`](CASE_COMP_MASTER_CONTEXT.md) | Canonical locked data bible, cluster totals, and verified citations. |
| **Project Research Context** | [`CASE_COMP_CONTEXT.md`](CASE_COMP_CONTEXT.md) | Chronological session log, research rationale, methodology, and team context. |
| **Siting Candidates Dataset** | [`grid_data/output/siting_relocation_candidates_v3.csv`](grid_data/output/siting_relocation_candidates_v3.csv) | Scored alternate sites (Neemrana, Kurnool, Tumakuru, Sri City, etc.). |
| **Strategic Siting Report** | [`grid_data/output/siting_relocation_report.md`](grid_data/output/siting_relocation_report.md) | In-depth spatial analysis of latency vs clean energy trade-offs. |
| **Water Cooling Dataset** | [`data/water_cooling_subsidiary.csv`](data/water_cooling_subsidiary.csv) | CGWB groundwater vulnerability & WUE demand projections across 9 clusters. |
