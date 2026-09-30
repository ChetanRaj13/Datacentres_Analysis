# Master Context — India Data Centre Sustainability Case Competition

> Paste this whole file into a fresh chat for full continuity. Everything here is either a verified fact, a stated assumption, or an explicitly flagged caveat — nothing here is fabricated or unchecked unless labeled as such.

---

## TASK

Build a 3-5 slide case-competition synopsis (submitted via Unstop, BIT Mesra) on **sustainability of AI-driven data centres in India**, then a live final presentation. Need the deck content finished, Canva-ready (tight bullets, no fluff), fully cited (plagiarism/misrepresentation = disqualification), and analytically defensible for a judge panel Q&A.

---

## COMPETITION DETAILS

- **Host:** BIT Mesra, submissions via Unstop.
- **Round 2 (current):** 3-5 slide case synopsis. Window: **28-30 Sep 2026**.
- **Round 3 (final):** Live presentation + Q&A, **3 Oct 2026, CAT Hall, BIT Mesra**. Optional physical model/prototype.
- **Round 2 mandatory slide content:** chosen problem, key research & insights, analysis, proposed solution, expected impact.
- **Judged on:** Problem Understanding, Research & Analysis, Innovation, Feasibility, Sustainability & Impact, Communication & Presentation.
- **Hard rule:** no plagiarism/misrepresentation — every stat must trace to a real source, or it risks disqualification.

---

## CURRENT STATE — WORKSTREAM STATUS

| Workstream | Status | Notes |
|---|---|---|
| Idea + problem selection | **100%** | Locked: AI data-centre sustainability in India |
| Demand-side data (facility/cluster MW) | **~98%** | 9 clusters, verified; Jamnagar tiered-verified |
| Supply-side data (grid/RE) | **~97%** | 9 clusters have emission factor, RE share, solar/wind CF, storage signal |
| Core RE-matching model | **100%** | Corrected and independently hand-verified (see Methodology section) |
| Solution framework (siting + procurement) | **~80%** | Logic complete; siting-relocation candidates at v3, mostly clean |
| Water-positive cooling (subsidiary) | **0%** | Intentionally deferred — only add AFTER main framework slides are done |
| Slide deck | **In progress** | Slide 1 (Problem) drafted in this chat; slides 2-5 not yet drafted |
| Citation/plagiarism pass | Ongoing | Most headline numbers already spot-checked as they were built |

---

## SOLUTION DIRECTION (LOCKED)

- **Main solution:** Siting index (which cities/clusters are best positioned) + a 24×7 RE-matching procurement framework (how data centres should buy renewable power to actually match their continuous load, not just annual volume).
- **Subsidiary (deferred):** Water-positive cooling (recycled/treated wastewater for cooling) — add only as a small sub-point once the main framework is fully built out. Do not expand this into its own slide unless time allows after everything else is done.
- **Rejected alternative:** Waste-heat reuse — dropped early (weak fit for India's hot climate, little demand for reclaimed heat).

---

## VERIFIED DEMAND-SIDE DATA (9 clusters)

Source: cleaned, deduplicated facility-level dataset (aidatacenterindex.com, Wikipedia, JLL & CBRE India Data Centre Market Reports 2025), cross-checked against corporate filings, press, and government records. File: `datacentre_clusters_merged.xlsx` (Cluster_Model sheet).

| Cluster | State | Low MW (today: operational + under construction) | High MW (future: + announced/planned) |
|---|---|---|---|
| Mumbai / Navi Mumbai | Maharashtra | 766.6 | 2,316.6 |
| Chennai | Tamil Nadu | 191.5 | 706.5 |
| Hyderabad | Telangana | 151.4 | 751.4 |
| Pune | Maharashtra | 45 | 145 |
| Delhi NCR (Noida/Greater Noida/Gurugram) | UP / Haryana | 153 | 353 |
| Bengaluru | Karnataka | 107.1 | 257.1 |
| Kolkata | West Bengal | 42.4 | 67.4 |
| Visakhapatnam (Vizag) | Andhra Pradesh | 1,000 | 1,000 |
| Jamnagar | Gujarat | 1,000 | 3,000 |

**Jamnagar tiered verification (important — use this framing, not a flat number):**
- **168 MW Meta anchor facility** — fully verified via independent corporate/press cross-check (Meta, Reliance, The Hindu, ET). Contractual, built-to-suit.
- **1,000 MW Phase 1** — credible corporate roadmap, partially verified. Used as the "low" scenario.
- **3,000 MW master plan** — aspirational, post-2030, single-source (Reliance/NVIDIA announcement cycle). Used as the "high" scenario. **Do not present as an active/committed grid draw.**
- Nesting confirmed consistent: 168 MW nested in 1,000 MW nested in 3,000 MW; no double-counting.
- Remaining gap (statutory EIA/grid-connection filings) is explicitly unavailable publicly — legitimate stopping point.

---

## VERIFIED SUPPLY-SIDE DATA (9 clusters)

Source: CEA, MNRE, NIWE, CERC/SERC tariff orders, SECI/state DISCOM tender filings. National emission factor applies to all (India runs one synchronous grid). File: `grid_data/output/cluster_supply_data.csv`.

| Cluster | State | Emission factor (tCO₂/MWh) | RE share % (incl. large hydro) | Solar CF % | Wind CF % | Wind viable? | Storage/BESS signal |
|---|---|---|---|---|---|---|---|
| Mumbai/Navi Mumbai | Maharashtra | 0.716 | 36.8 (26.5 excl. hydro) | 20.8 | 24.0 | Yes | ₹2.38-2.40 Lakh/MW/mo (MSEDCL 2GW/4GWh) |
| Chennai | Tamil Nadu | 0.716 | 53.2 (48.6 excl.) | 21.0 | 31.5 | Yes | ₹3.15-3.16 Lakh/MW/mo (TNGECL 375MW) |
| Hyderabad | Telangana | 0.716 | 34.5 (23.8 excl.) | 21.5 | 19.0 | Yes | ₹3.04-3.75 Lakh/MW/mo (SECI ISTS proxy) |
| Pune | Maharashtra | 0.716 | 36.8 (26.5 excl.) | 20.8 | 24.0 | Yes | ₹2.38-2.40 Lakh/MW/mo (MSEDCL) |
| Delhi-NCR/Noida | UP | 0.716 | 22.4 (13.6 excl.) | 19.5 | 0.0 | **No** (<100 W/m², Gangetic plains) | ₹3.04-3.75 Lakh/MW/mo (SECI ISTS proxy) |
| Bengaluru | Karnataka | 0.716 | 61.2 (51.8 excl.) ⚠️ | 22.5 | 28.0 | Yes | ₹2.49-2.54 Lakh/MW/mo (KPTCL 500MW) |
| Kolkata | West Bengal | 0.716 | 13.8 (4.2 excl.) | 18.2 | 0.0 | **No** | SECI ISTS national proxy (no state tender found) |
| Visakhapatnam | Andhra Pradesh | 0.716 | 44.1 (36.2 excl.) | 22.0 | 27.0 | Yes | ₹2.80-3.20 Lakh/MW/mo (APGECL Hybrid) |
| Jamnagar | Gujarat | 0.716 | 57.4 (54.0 excl.) | 23.0 | **Dual scenario ⚠️ — see below** | Yes | ₹2.10-2.32 Lakh/MW/mo (GUVNL Phase VIII/IX) |

**⚠️ Jamnagar wind CF — use dual scenario, never a single bare number:**
- **Conservative (24.0%)** — site-specific historical figure from a real GERC filing (Jamnagar Coastal ~23.97%, Jamnagar Inland ~20.2%). Use this as the default/citable figure.
- **Claimed upside (32.0%)** — a regional claim ("highest nationally, beats Muppandal") that does NOT hold up against the site-specific GERC data. Present only as an unverified upside case, never as confirmed.

**⚠️ Bengaluru's RE share (61.2%) is likely stale, not wrong.** A Feb 2026 report (Renewable Watch, citing CEA) shows Karnataka's actual RE share (same definition, incl. large hydro) at ~70% (26,421 MW of 37,877 MW installed) — the 61.2% figure predates a 2024-2026 capacity surge. This is a conservative understatement, not an overstatement — safe to use as-is, but know the real number is higher if challenged in Q&A.

**Chennai's wind CF (31.5%) — spot-checked, reasonably close.** A 2018 TNERC tariff order sets the state's normative wind CUF at 29.15%; modern repowered turbines reach 25-30%. 31.5% is a mild optimistic rounding, not a fabrication. Safe to use as-is.

---

## CORE MODEL — METHODOLOGY (FINAL, CORRECTED, VERIFIED)

File: `datacentre_RE_matching_model_CORRECTED.xlsx` (Assumptions / Demand_Supply_Model / Slide_Ready_Summary sheets). Built with real Excel formulas (not hardcoded), independently hand-verified by Claude — matches exactly.

**Assumptions (labeled sourced vs. assumed):**
- Hours per year: 8,760 (constant)
- **Utilisation factor: 65%** (ASSUMPTION — share of contracted IT MW actually drawn on average)
- **Solar:wind blend: 60:40** (ASSUMPTION — when sizing a 1:1 nameplate dedicated RE buildout; 100% solar where wind is "Not viable")
- **National grid emission factor: 0.716 tCO₂/MWh** (SOURCED — CEA CO2 Baseline Database Ver 19.0/20.0, national synchronous-grid baseline)

**Formula chain (per cluster, per scenario):**
```
demand_mwh = MW × 8760 × 0.65
demand_gwh = demand_mwh / 1000
bau_co2_tonnes = demand_mwh × 0.716
blended_re_match_pct = solar_cf × 0.6 + wind_cf × 0.4   (or solar_cf × 1.0 if wind not viable)
incremental_re_gain_pct = blended_re_match_pct − current_grid_re_share_pct
co2_avoided_tonnes = demand_mwh × 0.716 × incremental_re_gain_pct / 100   (set to 0 if incremental_re_gain_pct ≤ 0)
unmatched_pct_gap = 100 − blended_re_match_pct
```

**Key methodological insight (this IS the deck's headline finding):** a dedicated 1:1 solar+wind buildout, limited by real-world capacity factors (~18-27%), is BELOW the current grid's RE share in 8 of 9 clusters. This means CO₂-avoided is correctly ~0 in those 8 clusters under this formula — **the real, presentable finding is the 75-82% unmatched RE-matching gap, not a large CO₂-avoided number.**

### FINAL CORRECTED RESULTS TABLE (use these numbers)

| Cluster | Demand today (GWh/yr) | Demand future (GWh/yr) | Current grid RE share % | Blended RE-match ceiling % | **RE-matching gap %** | CO₂ avoided today (t) | CO₂ avoided future (t) |
|---|---|---|---|---|---|---|---|
| Mumbai/Navi Mumbai | 4,365 | 13,191 | 36.8 | 22.1 | **77.9%** | 0 | 0 |
| Chennai | 1,090 | 4,023 | 53.2 | 25.2 | **74.8%** | 0 | 0 |
| Hyderabad | 862 | 4,279 | 34.5 | 20.5 | **79.5%** | 0 | 0 |
| Pune | 256 | 826 | 36.8 | 22.1 | **77.9%** | 0 | 0 |
| Delhi-NCR/Noida | 871 | 2,010 | 22.4 | 19.5 | **80.5%** | 0 | 0 |
| Bengaluru | 610 | 1,464 | 61.2 | 24.7 | **75.3%** | 0 | 0 |
| **Kolkata** | 241 | 384 | 13.8 | 18.2 | **81.8%** | **7,606** | **12,090** |
| Visakhapatnam | 5,694 | 5,694 | 44.1 | 24.0 | **76.0%** | 0 | 0 |
| Jamnagar (conservative, 24% wind) | 5,694 | 17,082 | 57.4 | 23.4 | **76.6%** | 0 | 0 |
| Jamnagar (claimed upside, 32% wind) | 5,694 | 17,082 | 57.4 | 26.6 | **73.4%** | 0 | 0 |

**National totals (9 clusters, using conservative Jamnagar case):**
- Total demand: **19,684 GWh/yr today → 48,952 GWh/yr future** (2.5× growth)
- Total genuine CO₂ avoided: **7,606 t/yr today → 12,090 t/yr future** — entirely from Kolkata; every other cluster is 0 under this methodology
- Average RE-matching gap across all 9 clusters: **~77.8%**

**Why Kolkata is the only positive case:** it's the one cluster where today's grid is dirty enough (13.8% RE) that even a modest dedicated solar buildout (18.2% CF) beats it. Everywhere else, the existing grid mix (with hydro/nuclear/broader RE) already outperforms what an on-site solar+wind build alone can match.

---

## ⚠️ CRITICAL: METHODOLOGY INTEGRITY / ERROR HISTORY

**A first "finalized" version of this model was WRONG and must never be used again.** It claimed 8.4-20.5 million tonnes CO₂ avoided/year nationally. Root causes:
1. The demand formula silently dropped the 65% utilisation factor entirely (computed `MW × 8760` with no `× 0.65`), inflating every demand figure by ~54%.
2. The "RE Matched Under Framework" percentages (76-92% per cluster) did not derive from the established blended-CF formula at all — they were disconnected, unexplained numbers.

**The corrected table above supersedes that version entirely.** If any file, prior chat, or agent memory references "8.4 million tonnes" or "20.5 million tonnes" CO₂ avoided, or RE-match percentages in the 76-92% range, **that is the superseded, incorrect version — discard it.**

This pattern (a suspiciously large/impressive/round number attached to a headline claim, later found to be fabricated, disconnected from the stated formula, or a mislabeled proxy) happened **repeatedly** in this project. Full list of caught errors, for future reference when evaluating any new agent output:

1. **First `cluster_totals.csv`** (grid_data agent run) — regenerated its own demand numbers instead of reading the verified ones (Vizag showed only 120 MW vs. the real, verified 1,000 MW). **Discarded.**
2. **First facilities dataset** — many mislabeled rows (wrong cities, city-market-totals conflated with facility-level figures, e.g. AWS ap-south-1 labeled as Hyderabad instead of Mumbai). Fixed via full cleaning pass with `capacity_basis` tagging (it_load / facility_power / not_specified) and a PUE multiplier (1.35-1.50) to reconcile IT load vs. total facility power.
3. **Siting-relocation v1** — (a) Chennai & Bengaluru each had both a named candidate row AND a contradictory "no better option" row; (b) several candidates (Bengaluru's Vasanthanarasapura/Dobbaspet, Hyderabad's Orvakal) had numbers that exactly matched state-level averages but were labeled "High confidence" citing industrial-park land-allotment URLs that don't actually publish renewable-capacity-factor data; (c) **Neemrana (Delhi-NCR candidate) claimed a 22% wind CF that was geographically implausible** — Neemrana sits in Alwar district, nowhere near Rajasthan's real wind corridor (Jaisalmer/Barmer, far west) — and this single number drove the largest uplift score in the entire table (+41.1).
4. **Siting v2** — fixed the duplicate rows; corrected Neemrana's wind CF to "Not Viable" via a genuine NIWE zone-specific check (net score dropped 39.50 → 23.79, correctly, with the original kept for traceability); flagged 6 rows as state-level proxies.
5. **Siting v3** — flagged Neemrana's RE-share (43.5%) as also a state-level proxy (same issue, different field, just not caught the first time since the fix prompt only scoped wind); audited Mumbai's near-match rows (Dighi Port, Tarapur — differed from the state average by only 0.1-0.5%, no distinct source found) and flagged them as proxies too. **Final: 9 of 20 candidate rows flagged `proxy_flag=TRUE`.**
6. **BIDA Jhansi candidate's "4,000 MW Bundelkhand Ultra Mega Solar Park" claim — independently verified WRONG.** The actual Jhansi-specific solar park (TUSCO/THDC-UPNEDA joint venture) is **600 MW**. The 4,000 MW figure is the combined total across ~10 separate solar plants spread across the entire Bundelkhand region (Jalaun 1,200 MW, Chhatarpur 950 MW, Chitrakoot 800 MW, etc.) — not one park at the Jhansi site. **Use 600 MW for this candidate, not 4,000 MW.**
7. **Kurnool Ultra Mega Solar Park (Hyderabad's headline candidate) — independently verified CORRECT.** Genuinely 1,000 MW, operational since 2017-2019, well documented across multiple sources. **This is the safest, most defensible headline relocation story — use it as the primary example.**
8. **Gujarat/Jamnagar wind CF (32% claim)** — see supply-side table above; resolved via dual-scenario labeling.

**Lesson for any future agent work on this project:** any claim that is (a) suspiciously round, (b) the single largest/most impressive number in a table, (c) attached to the exact location needed for a strong narrative, or (d) presented as "High confidence" without a visible site-specific citation — deserves a direct spot-check before it's trusted, let alone put on a slide.

---

## SOLUTION FRAMEWORK — SITING/RELOCATION CANDIDATES (v3, current)

File: `siting_relocation_candidates_v3.csv`. Workload-based search radius rule: cloud/inference facilities → ~50-100 km max; AI-training/LLM-supercomputing → ~150-400 km (assigned per cluster's dominant workload type).

**Strongest, safest stories for the deck (in order of defensibility):**

1. **Hyderabad → Orvakal/Kurnool (205 km, AI-training radius)** — **fully verified, use as PRIMARY headline.** Co-located with the real 1,000 MW Kurnool Ultra Mega Solar Park + Rayalaseema wind corridor. RE share 44.1%, solar CF 22.5%, wind CF 27.0%. Uplift +17.87, net score +15.31.
2. **Chennai → Sri City (72 km, cloud/inference radius)** — non-proxy, clean numbers (RE 48.5%, solar 21.5%, wind 28.5% — genuinely differ from Chennai's own figures, suggesting real site-specific data). Uplift +12.61, net score +9.61.
3. **Bengaluru → Tumakuru/Vasanthanarasapura (76 km) or Dobbaspet (54 km)** — water-stress-driven relocation. RE/solar/wind numbers stay flat (same state, proxy-flagged, honestly labeled) — the entire uplift comes from water-stress relief, which is a transparent, defensible claim. Uplift +16.0 both, net scores +12.83 and +13.75 respectively.
4. **Delhi-NCR → Neemrana/DMIC (128 km)** — usable as a SECONDARY example only, with caveat: wind CF corrected to "Not Viable," RE-share (43.5%) is a flagged Rajasthan state-average proxy, not site-verified. Net score (corrected) = +23.79 (down from an incorrect +39.5).
5. **Delhi-NCR → BIDA Jhansi (365 km)** — usable but **must correct the solar park capacity claim from 4,000 MW to 600 MW** before using. Net score +15.17 (based on the original claim; may need minor rework if you correct the number).
6. **Delhi-NCR → YEIDA Jewar (52 km)** — a dedicated data-centre zone near Jewar airport; smaller uplift (+8.24) but no proxy/correction issues.

---

## SLIDE 1 — DRAFTED CONTENT (PROBLEM)

### Headline (pick one)
- "India is racing to build AI infrastructure — but the energy, water, and siting decisions behind it are being made faster than the grid and water systems can support them."
- Alt: "India's AI boom runs on electricity that never sleeps — but the grid and water systems behind it are still catching up."

### Two-part problem
**⚡ Energy demand issue**
- AI data centres draw power continuously, 24×7 — unlike most industry.
- Even a fully dedicated solar+wind buildout covers only ~18-25% of that continuous load (capacity-factor ceiling).
- **75-82% of AI data-centre demand cannot be matched by on-site renewables alone**, across every major cluster studied.

**📍 Location issue**
- New AI capacity is concentrating in a handful of states (Gujarat, Andhra Pradesh, Telangana) chosen for land/power deals, not RE fit or water availability.
- Jamnagar + Vizag alone account for over half of India's future data-centre pipeline.
- Siting decisions rarely weigh local grid cleanliness or water stress upfront.

### Data snapshot table (Today vs Future Pipeline, 9 clusters)
| | Today (Operational + Under Construction) | Future Pipeline (+ Announced/Planned) |
|---|---|---|
| Total capacity | ~3,460 MW | ~8,600 MW (2.5× growth) |
| Explicitly AI-built capacity | Limited (early-stage) | ~4,460 MW — over half the future pipeline |
| Typical single-facility size | 20-150 MW | 400-3,000 MW (10-20× larger) |
| Confirmed/credible "mega" AI hubs (≥400 MW) | 0-1 | 4 (Jamnagar, Vizag, Hyderabad ×2) |

*Small-font source note (bottom of slide):* Figures from a facility-level dataset (aidatacenterindex.com, Wikipedia, JLL & CBRE India Data Centre Market Reports 2025), cross-checked against corporate filings, press, and government allotment records, covering 9 major clusters as of Sep 2026. "Today" = operational + under-construction; "Future" = additionally includes announced/planned (confidence varies; e.g., one mega-project's long-term target is aspirational, not committed). **AI data centre** = purpose-built for GPU-based AI training/inference (e.g., dedicated NVIDIA GPU clusters). **General-purpose/cloud data centre** = standard cloud regions/colocation that may run some AI workloads but weren't purpose-built for them — this distinction matters because AI facilities run at far higher power density per rack and are the primary driver of the demand surge.

### Closing "Our Goal" statement
"Quantify how much power these data centres actually consume, how clean the electricity behind them really is, and chart a realistic path for India to power its AI boom on clean energy — without draining city water supplies or falling back on coal."

### Suggested improvements (not yet implemented)
- Add one hook number at the top (e.g., "future pipeline = X million homes worth of power") — needs a disclosed assumption, trade impact vs. precision.
- Visual: simple India map with dots sized by cluster MW (Jamnagar, Vizag, Hyderabad) instead of a bullet, for the location point.
- Don't add a specific water number yet — no verified India-specific WUE data (deferred workstream).
- Consider trimming the data table to 3 rows if Canva space is tight; keep the "mega hubs" row if forced to cut.

---

## REMAINING SLIDES — NOT YET DRAFTED (content ready to pull from above)

- **Slide 2 — Research & Insights:** E/S/E (Environmental/Social/Economic) classification of issues, direct vs. systemic. Not yet written.
- **Slide 3 — Analysis:** headline = the 75-82% RE-matching gap (table above), cluster comparison, why only Kolkata shows positive CO₂-avoided. Not yet written.
- **Slide 4 — Solution:** siting index + 24×7 RE-matching procurement framework; feature Hyderabad→Kurnool as primary case study, Bengaluru/Chennai water-stress relocations as secondary, Neemrana/Jhansi as caveated tertiary examples. Not yet written.
- **Slide 5 — Impact & Roadmap:** genuine (small) CO₂-avoided figures, phased rollout, feasibility. Not yet written. Water-positive cooling subsidiary point can attach here as a small sub-bullet, only after everything else is locked.

---

## USER PREFERENCES (apply throughout)

- Prefers slide-ready pointer content over prose; no fluff or padding paragraphs.
- Prefers downloadable file outputs (HTML/markdown/xlsx) over inline code — EXCEPT Claude Code agent prompts, which should be given as plain text directly in chat, never as a file.
- Wants data-grounded feedback and iterative refinement — actively wants skepticism and fact-checking of agent output, not passive acceptance.
- For Claude Code agent prompts specifically: a single flowing "Read [canonical docs] first. Task: <numbered list>" style — each numbered item states the problem, an inline root-cause hypothesis, and a concrete test/verification requirement — closing with an instruction to write tests and append a session-log entry stating which items were real bugs vs. confirmed-working.
- For this deck: Canva-ready, content-rich but tight — headings + bullets only.
- Identity: goes by "Supreme Leader"; works as both a developer and a consultant/analyst across technical and analytical domains.

---

## WHAT TO IGNORE / SUPERSEDED (do not resurrect)

- The original scraper-based "problem discovery" pipeline and its shortlist (e-waste, food waste, student mental health, quick-commerce plastic packaging, groundwater depletion) — explored and explicitly rejected in favor of the data-centre topic.
- Water-positive cooling and waste-heat reuse as competing PRIMARY solutions — both dropped as primaries; water-cooling retained only as a tiny, deferred subsidiary.
- The first, error-riddled facility dataset (pre-cleaning) and the first grid_data-agent-regenerated `cluster_totals.csv` (wrong Vizag = 120 MW).
- **The first RE-matching model output claiming 8.4-20.5 million tonnes CO₂ avoided/year and 76-92% "RE Matched Under Framework" percentages — SUPERSEDED, incorrect, do not use.**
- Bare/unflagged versions of: Neemrana's 22% wind CF, Neemrana's unflagged 43.5% RE-share, Jhansi's "4,000 MW" solar park claim, Gujarat's unflagged 32% wind CF — all superseded by the corrected/flagged versions documented above.
- Siting-relocation v1 and v2 CSVs — superseded by v3.

---

## FILES REFERENCED (exist in the user's local project folder "DUO - CASE COMP", managed by their Claude Code agent; some also produced directly in Claude.ai chat)

- `CASE_COMP_CONTEXT.md` — master project doc with full decision log + session log (local copy is canonical/most complete)
- `datacentre_clusters_merged.xlsx` — Cluster_Model / Market_Context / Facilities_Reference sheets (demand-side)
- `datacentre_RE_matching_model_CORRECTED.xlsx` — Assumptions / Demand_Supply_Model / Slide_Ready_Summary (the corrected core model)
- `grid_data/output/cluster_supply_data.csv` — 9-row supply-side dataset
- `siting_relocation_candidates_v3.csv` — 20-row, 8-cluster siting/relocation analysis, proxy-flagged
- `jamnagar_facilities.csv` + `jamnagar_verification_notes.md` — Jamnagar tiered demand verification
