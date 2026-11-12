# AGENT.md — India AI Data Centre Sustainability Dashboard

## Context for the AI agent building this

This file is the complete handoff context for building a web dashboard. It was produced by Claude after an extensive data collection, verification, and research project. Everything described here is already done — your job is to **build the dashboard**, not collect new data, unless a gap is explicitly flagged below.

---

## 1. Project Background

A dissertation (TISS, B.S. Analytics and Sustainability Studies) is assessing whether India's AI data centre boom is sustainable, by comparing each data centre's power/water demand against the real capacity and stress level of the district it sits in. This dashboard is a deliverable of that project.

## 2. What to Build — TWO VIEWS, not just a map

This is a multi-section dashboard, not a single map page. Build it as two switchable views/tabs within one app (a sidebar or top-tab switcher is fine):

### View 1: Map
- **Background layer:** All of India, shaded by district, colored on a groundwater-stress gradient (color scale from the CGWB 4-category system — see Section 5). **Color the entire country**, not just the 29 districts that host data centres — the person has a nationwide groundwater dataset for this (see Section 3).
- **Foreground layer:** All 118 data centre campuses plotted as markers, sized/styled by live or planned MW capacity.
- **Marker confidence must be visually distinguishable.** A marker's `precision_tier` (Section 4) must be reflected in how it's drawn — e.g., solid fill for site-exact, hollow/outlined for district-centroid fallback — and this distinction must also appear in the tooltip/popup text in plain words (e.g., "Approximate — district-level only, exact site not located"). Do not let a placeholder coordinate look identical to a verified one.
- **Interactivity:** hover/click on a marker shows facility name, operator, district, state, live MW, planned MW, and precision tier. Filtering by state, by precision tier, or by live-vs-planned capacity is a nice-to-have.
- **A legend is required**, not optional: one for the groundwater color gradient, one for marker confidence (solid vs. hollow).

### View 2: Summary Dashboard
A KPI + charts page summarizing everything collected in this project so far. Use `summary_stats.json` (Section 4) directly — it already contains computed KPI values and chart-ready data arrays, no need to recompute from raw files.

- **KPI cards** (top of page, small stat cards): render every item in `summary_stats.json → kpi_cards` as its own card — label, value, unit if present, and the optional note/detail text shown as a smaller caption. There are 10 of these; lay them out in a responsive grid (e.g., 5x2 or 4x3).
- **Charts** (below the KPI cards): render every entry in `summary_stats.json → charts`. Suggested chart type per dataset:
  - `data_centres_by_state` → horizontal bar chart (14 states)
  - `mw_by_state` → grouped/stacked bar chart, two series (live_it_mw, planned_it_mw) per state
  - `verification_confidence` → donut/pie chart (4 categories)
  - `coordinate_precision_breakdown` → donut/pie chart
  - `groundwater_category_distribution` → bar chart (4 CGWB categories, Safe/Semi-critical/Critical/Over-exploited)
  - `groundwater_stress_ranked_all_districts` → horizontal bar chart, all 29 districts sorted by stage %, colored by category (this is the chart that visually tells the "which districts are already stressed" story — make it prominent)
  - `jjm_tap_coverage_ranked` → horizontal bar chart, sorted ascending (lowest coverage first)
- A charting library like Chart.js, Recharts, or similar is fine — pick whatever fits your stack; no specific library is mandated.
- Each chart should have a short one-line caption/title drawn from its own section name (e.g., "Groundwater stress by district (CGWB 2025)") — don't just show raw axis labels with no context.

**Tech stack requirement: plain HTML/CSS/JavaScript only — no React, Vue, or any framework requiring a build step.** The person specifically wants this dashboard easy to open and edit directly (open the HTML file, see the actual markup; open the JS file, see the actual logic — no compiling, no bundler, no node_modules). Use vanilla JS, with a lightweight library loaded via CDN script tag where genuinely useful (Leaflet.js for the map, a simple charting library like Chart.js for the Summary view) — but the core app itself must be plain HTML/CSS/JS.

**File structure for easy updates:** split into separate files rather than one giant self-contained HTML blob — e.g. `index.html`, `style.css`, `map.js`, `dashboard.js`, plus the JSON data files (Section 4) loaded via `fetch()`. This matters specifically because the person will be updating the underlying data (new coordinates, new facilities, updated KPIs) over the life of this dissertation project — the JSON files should be the only thing that needs to change for a data update; HTML/CSS/JS structure should not need to be touched just to reflect new numbers. Keep data-loading code cleanly separated from rendering code so this stays true as the project evolves.

The Map and Summary views can be two tabs within one `index.html` (toggled with JS, no page reload) or two separate HTML pages linked together — either is fine, but keep the switch between them obvious and immediate.

## 3. Inputs the person is providing directly (not in the files below)

1. **India district boundary GeoJSON** — the person is providing this.
1b. **`design.md`** — a separate design specification file the person is providing (colors, fonts, layout/branding preferences, and any other visual requirements). **Treat this as the authoritative source for all styling decisions** — where `design.md` specifies something (color palette, typography, card/chart styling, spacing, etc.), follow it exactly rather than improvising. Where `design.md` is silent on something this dashboard needs (e.g. it doesn't mention a specific chart type's styling), use sensible defaults consistent with the rest of its direction. The groundwater color gradient (Section 5) and marker-confidence styling (Section 2) still follow this document's specific requirements regardless of what `design.md` says about general palette — but apply `design.md`'s colors/fonts to the overall UI chrome (cards, backgrounds, text, buttons, legends) around them.
2. **CGWB National Compilation of Ground Water Resources (nationwide)** — the person has this as a PDF (the official national report). This covers far more districts than the 29 in this project's own `groundwater_districts.json`. **Extraction guidance:** the report's table structure should match the schema already used in `groundwater_districts.json` — per-district rows with columns for extractable groundwater resource, extraction by category (irrigation/domestic/industrial), stage of extraction %, and a derived category label. When parsing the PDF, validate extracted numbers against known values before trusting the extraction pipeline — e.g., Gurugram should show ~194.6% stage of extraction, Bengaluru Urban ~177.3% (see Section 5 for the full validation list). If parsed numbers don't match these reference points for districts already in this project's dataset, the table-extraction logic needs fixing before trusting it for the rest of India.

**Before writing any matching code:** inspect the GeoJSON's and groundwater file's actual district-name spelling and check them against the 29-district list in Section 6. Indian district names are inconsistently spelled across sources (e.g., "Bengaluru Urban" vs "Bangalore Urban", "Gautam Buddha Nagar" vs "Gautam Buddh Nagar"), and this applies to **state names too** (e.g., "Delhi" vs "NCT of Delhi"). A silent mismatch here shades the wrong district — this is the single highest-risk step in the whole build. Reconcile every name explicitly; don't assume a direct join will work.

## 4. Data files provided (ready to use directly)

All four files below are in the same folder as this one.

- **`data_centres.json`** — all 118 data centre campuses, each already joined with its best-available coordinate.
  - 90 of 118 have `has_verified_coordinate: true` with real `latitude`/`longitude` and a `precision_tier` (`Exact site`, `Plot or village`, `Locality or industrial area`, or `District only`) — each individually researched and cross-checked against the facility's operator name/code before being accepted, not blind geocoding.
  - The other 28 have `has_verified_coordinate: false`, `latitude`/`longitude` as `null`, and `precision_tier` set to `"No coordinate — use district centroid"` — for these, **compute that row's district centroid from the GeoJSON polygon** and use it as the marker position. This guarantees the dot lands in the correct district even with no exact address. These 28 are confirmed (across two independent research rounds) to have no public location data — early-stage MoU/land-acquisition-only projects or undisclosed pipeline announcements, not a research gap, so don't attempt to re-research them.
  - A few rows carry extra caveats worth surfacing in the tooltip if easy to do (read each row's `coordinate_note` field): e.g. one row has a flagged district conflict between the source and the original data file; a couple of rows share one coordinate across multiple nearby facilities in the same industrial park (building-level precision wasn't available).

- **`groundwater_districts.json`** — the 29 (+1 extra CGWB reporting unit) districts in this project's own research, each with `stage_of_extraction_pct` and `category` already computed using the CGWB 4-band system (Section 5). Use this directly for these districts; for the rest of India (from the nationwide PDF, Section 3), derive `category` the same way using the 70/90/100 cutoffs.

- **`summary_stats.json`** — pre-computed KPI values and chart-ready data arrays for the Summary Dashboard view (Section 2). No need to recompute anything from raw files — this is ready to render directly.

- **`manifest.json`** — a short index of the above three files, their row counts, join keys, and the color-gradient spec. Read this first.

## 5. Groundwater stress categorization (the color gradient)

India's official standard — CGWB 2025 Groundwater Resource Assessment — uses 4 categories based on `stage_of_extraction_pct` (extraction as % of sustainable yield):

| Category | Stage of extraction | Suggested color |
|---|---|---|
| Safe | < 70% | Green |
| Semi-critical | 70–90% | Yellow |
| Critical | 90–100% | Orange |
| Over-exploited | > 100% | Red |

This is the category system used throughout the project (not the WRI Aqueduct global 5-band system — CGWB was deliberately chosen as the India-appropriate standard, since it's the real regulatory basis for groundwater permit decisions). Apply this same 4-category scale to the nationwide file from Section 3.

**Validation reference points** (use these to sanity-check both the map gradient and the nationwide PDF extraction): Gurugram 194.6% (most severe, should render deep red), Bengaluru Urban 177.3%, Bengaluru Rural 146.8%, Chennai 121.7%, Indore 118.0%, Gandhinagar 111.3%, Sonipat 108.7%, Gautam Buddha Nagar 105.2% — these 8 districts are the current "over-exploited" set and should all render red if the gradient and data pipeline are working correctly.

## 6. The 29 original hosting districts (for name-reconciliation reference)

State → District pairs already confirmed in this project's data:
- Andhra Pradesh: Anakapalli, Guntur, Visakhapatnam, Vizianagaram
- Bihar: Patna
- Chhattisgarh: Raipur
- Delhi: South East Delhi
- Gujarat: Ahmedabad, Gandhinagar, Jamnagar
- Haryana: Gurugram, Panchkula, Sonipat
- Karnataka: Bengaluru Rural, Bengaluru Urban
- Madhya Pradesh: Indore
- Maharashtra: Mumbai Suburban, Pune, Raigad, Thane
- Odisha: Khordha, Puri
- Tamil Nadu: Chengalpattu, Chennai, Kanchipuram
- Telangana: Ranga Reddy
- Uttar Pradesh: Gautam Buddha Nagar
- West Bengal: Hooghly, North 24 Parganas

Note: `groundwater_districts.json` also contains a 30th row, "Bengaluru South," which is NOT one of the 29 official hosting districts — likely an adjacent/overlapping CGWB reporting unit. Don't be surprised if it appears in the nationwide file too; it's extra context, not an error.

## 7. Headline totals for context (already reflected in summary_stats.json)

- 114 data centre campuses (+ 4 nested construction-phase sub-rows), across 14 states, 29 hosting districts.
- Live capacity: 1,380.5 MW IT load / 37.0 MW facility load.
- Planned capacity: 9,362.9 MW IT load / 9,141.0 MW facility load (planned is ~6.8x live — most of the pipeline hasn't been built yet).
- **Important:** IT load and facility/grid load are two different measurement bases and must never be summed together — they're kept as separate totals throughout this project. `summary_stats.json` already respects this; don't merge them if computing any new figures.
- Verification confidence across the 114 campuses: 25 backed by 2+ independent sources, 40 backed by a primary source, 48 partially verified, 1 unverified.

## 8. Other project data (not needed for this dashboard, but may be relevant if scope grows later)

- Electricity grid, DISCOM rating, and state energy data exist in this project but are NOT part of either view described here — ignore unless the person explicitly asks to add a third "energy" view later.
- Risk-scoring formulas (water risk, energy risk, combined) have been designed for a separate part of this dissertation and are also out of scope for this dashboard.

## 9. Build conventions to follow

- Don't fabricate or silently "improve" precision on any coordinate — the whole point of the `precision_tier` system is to keep the dashboard honest about what's really known vs. approximated.
- Every data centre must get a marker on the Map view, even the 28 with no real coordinate — use the district centroid fallback, visually marked as approximate (Section 2).
- Validate every district name match between the GeoJSON and the groundwater file explicitly (state names too, see Section 3), and flag (console log or on-screen) any district that failed to match rather than silently dropping it.
- Use `summary_stats.json`'s pre-computed values for the Summary view rather than recomputing from `data_centres.json` — the pre-computed version already handles the IT-load-vs-facility-load separation correctly (Section 7), and re-deriving it risks accidentally re-introducing that mixing error.

