# India AI & Data Center Decarbonization Roadmap (Case Competition)

This repository contains the complete research, data pipelines, geographic siting analysis, and 24/7 renewable energy matching model for decarbonizing India's AI and data center infrastructure by 2030.

---

## 📁 Repository Directory Structure

```text
DUO - CASE COMP/
├── CASE_COMP_CONTEXT.md                # Master project context, audit history & session logs
├── README.md                           # Repository architecture, module map & execution guide
├── datacentre_RE_matching_model.xlsx   # Executive 24/7 RE Matching Excel Model (3 sheets)
│
├── data/                               # Cleaned and categorized input datasets
│   ├── DataCentre/
│   │   ├── facilities_clean.csv        # Audited facility-level data (30 facilities across India)
│   │   ├── cluster_totals.csv          # Sourced cluster capacity (9 clusters, Low vs High MW)
│   │   └── city_market_totals.csv      # Metro-level capacity baselines
│   ├── clean/
│   │   └── cluster_totals.csv          # Clean cluster baseline reference
│   └── water_cooling_subsidiary.csv    # Water stress, WUE & demand dataset (9 clusters)
│
├── grid_data/                          # Electricity supply, siting & RE matching pipelines
│   ├── fetch.py                        # Automated data fetching & extraction
│   ├── build_table.py                  # Generates cluster-level supply dataset (9 states)
│   ├── siting_analysis.py              # Spatial relocation & sustainability scoring engine
│   ├── build_matching_model.py         # Builds datacentre_RE_matching_model.xlsx
│   ├── build_water_subsidiary.py       # Builds water_cooling_subsidiary.csv
│   ├── output/
│   │   ├── cluster_supply_data.csv     # Sourced grid emission factors, RE shares, solar/wind CF
│   │   ├── siting_relocation_candidates_v3.csv  # Sited alternate corridors (v3 audited)
│   │   ├── siting_relocation_report.md # Strategic relocation findings report
│   │   └── gaps.md                     # Supply-side sourcing methodology & gaps documentation
│   └── tests/
│       ├── test_supply_data.py         # Unit tests for 9-cluster grid supply data
│       ├── test_siting_candidates.py   # Unit tests for spatial siting & score formulas
│       ├── test_matching_model.py      # Unit tests for 24/7 RE matching model & formulas
│       └── test_water_cooling.py       # Unit tests for water demand & cooling priority data
│
└── scraper/                            # Problem-discovery scraping pipeline (Reddit/News/HN)
    ├── main.py                         # CLI entry point for problem mining
    ├── config.yaml                     # Scraping keywords, limits & source toggles
    ├── requirements.txt                # Python dependencies for scraper
    ├── sources/                        # Scraping connectors (Reddit, News, HN, Forums)
    ├── processing/                     # Keyword filtering, deduplication & scoring
    ├── report/                         # HTML report generation
    └── tests/                          # Automated tests for scraper connectors
```

---

## 🚀 Key Pipelines & How to Run

### 1. 24/7 RE Matching Model Build
Generates [`datacentre_RE_matching_model.xlsx`](datacentre_RE_matching_model.xlsx) with `Assumptions`, `Demand_Supply_Model`, and `Slide_Ready_Summary` sheets.
```bash
python grid_data/build_matching_model.py
```

### 2. Siting & Relocation Analysis
Evaluates 20+ candidate corridors for batch AI compute vs cloud region relocation.
```bash
python grid_data/siting_analysis.py
```

### 3. Supply Table Generator
Builds the 9-cluster state electricity supply dataset.
```bash
python grid_data/build_table.py
```

### 4. Run Test Suite (20 Automated Tests)
Validates schema integrity, formulas, and verification standards.
```bash
pytest grid_data/tests/ -v
```

---

## 📊 Core Presentation Outputs

| Deliverable | File Path | Description |
|:---|:---|:---|
| **Executive Matching Model** | [`datacentre_RE_matching_model.xlsx`](datacentre_RE_matching_model.xlsx) | 3-sheet financial/engineering model proving the **75%–82% RE-Matching Gap**. |
| **Siting Candidates Dataset** | [`grid_data/output/siting_relocation_candidates_v3.csv`](grid_data/output/siting_relocation_candidates_v3.csv) | Scored alternate sites (Neemrana, Kurnool, Tumakuru, etc.). |
| **Strategic Siting Report** | [`grid_data/output/siting_relocation_report.md`](grid_data/output/siting_relocation_report.md) | In-depth spatial analysis of latency vs clean energy trade-offs. |
| **Project Master Bible** | [`CASE_COMP_CONTEXT.md`](CASE_COMP_CONTEXT.md) | Chronological session log, research rationale, and team context. |
