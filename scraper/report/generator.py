import os
import csv
import json
import logging
from typing import Any, Dict, List
from collections import Counter

try:
    from processing.clusterer import ProblemCandidate
    from processing.schema import ProblemRecord
except ImportError:
    from ..processing.clusterer import ProblemCandidate
    from ..processing.schema import ProblemRecord

logger = logging.getLogger(__name__)

def generate_csv(candidates: List[ProblemCandidate], output_path: str):
    """Write comprehensive problems CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "rank", "cluster_id", "candidate_title", "theme", "rank_score",
            "avg_pain_score", "cluster_size", "distinct_sources",
            "scorecard_total", "depth_of_pain", "data_available", "novel_angle",
            "feasible_6mo", "measurable_impact", "record_id", "source",
            "url", "record_title", "record_pain_score", "engagement_score",
            "num_comments"
        ])
        for rank, cand in enumerate(candidates, 1):
            sc = cand.scorecard
            for r in cand.records:
                writer.writerow([
                    rank,
                    cand.cluster_id,
                    cand.title,
                    cand.theme,
                    cand.rank_score,
                    cand.avg_pain_score,
                    cand.size,
                    cand.distinct_sources,
                    sc.get("Total", 0),
                    sc.get("Depth of pain", 0),
                    sc.get("Data available", 0),
                    sc.get("Novel angle", 0),
                    sc.get("Feasible in ~6 mo", 0),
                    sc.get("Measurable impact", 0),
                    r.id,
                    r.source,
                    r.url,
                    r.title,
                    r.pain_score,
                    r.score,
                    r.num_comments
                ])
    logger.info(f"Generated CSV report: {output_path}")

def generate_json(candidates: List[ProblemCandidate], output_path: str):
    """Write comprehensive problems JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = [cand.to_dict() for cand in candidates]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Generated JSON report: {output_path}")

def generate_shortlist_markdown(candidates: List[ProblemCandidate], output_path: str):
    """Write top shortlist summary in markdown formatted for case comp context."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    top_cands = candidates[:10]
    
    lines = [
        "# Case Competition Problem Discovery — Top Candidate Shortlist",
        "",
        "> Generated automatically by the Problem Discovery Pipeline. Every statistic and quote is traceable to a real public discussion.",
        "",
        "## 1. Shortlist Scorecard (1–5 Scale)",
        "",
        "| Rank | Candidate | Theme | Depth of pain | Data available | Novel angle | Feasible in ~6 mo | Measurable impact | Total |",
        "|---|---|---|---|---|---|---|---|---|"
    ]
    
    for rank, cand in enumerate(top_cands, 1):
        sc = cand.scorecard
        lines.append(
            f"| {rank} | **{cand.title}** | `{cand.theme}` | {sc.get('Depth of pain', 0)}/5 | {sc.get('Data available', 0)}/5 | {sc.get('Novel angle', 0)}/5 | {sc.get('Feasible in ~6 mo', 0)}/5 | {sc.get('Measurable impact', 0)}/5 | **{sc.get('Total', 0)}/25** |"
        )
    
    lines.extend([
        "",
        "## 2. Deep Dive: Top 5 High-Potential Problems for Slide Deck",
        ""
    ])

    for rank, cand in enumerate(top_cands[:5], 1):
        sc = cand.scorecard
        lines.extend([
            f"### #{rank}. {cand.title}",
            f"- **Theme:** {cand.theme}",
            f"- **Evidence Volume:** {cand.size} verified mentions across {cand.distinct_sources} sources ({', '.join(cand.sources_breakdown.keys())})",
            f"- **Pain Intensity:** {cand.avg_pain_score:.1f}/10.0 | **Temporal Signal:** {cand.growth_over_time}",
            f"- **Key Terms:** `{', '.join(cand.top_terms)}`",
            f"- **Scorecard Rating:** {sc.get('Total', 0)}/25 (Pain: {sc.get('Depth of pain', 0)}/5, Data: {sc.get('Data available', 0)}/5, Novelty: {sc.get('Novel angle', 0)}/5, 6-Mo Feasibility: {sc.get('Feasible in ~6 mo', 0)}/5)",
            "",
            "**Voice of the People (Traceable Quotes):**"
        ])
        for q in cand.representative_quotes:
            quote_text = q['quote'].replace('\n', ' ').strip()
            lines.append(f"> \"{quote_text}\" — *[{q['source'].title()} Source]({q['url']}) (Score: {q['score']}, Pain: {q['pain_score']})*")
        lines.append("")

    lines.extend([
        "## 3. Recommended Selection for Round 2 Synopsis",
        "Based on balanced feasibility (6-month execution horizon) and high measurable impact with ample secondary research data, the top recommendation is candidate #1 or #2.",
        ""
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info(f"Generated shortlist markdown: {output_path}")

def generate_html_report(
    candidates: List[ProblemCandidate],
    all_records: List[ProblemRecord],
    output_path: str
):
    """Generate a self-contained offline HTML report with pointer-style slide layout and visuals."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    top_candidates = candidates[:15]
    total_records = len(all_records)
    total_candidates = len(candidates)
    
    # Theme stats
    theme_counts = Counter(r.theme for r in all_records)
    source_counts = Counter(r.source for r in all_records)

    # HTML building with embedded CSS
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Problem Discovery Report — Case Competition</title>
<style>
  :root {{
    --bg-primary: #0b0f19;
    --bg-card: #151d2e;
    --bg-card-hover: #1c273c;
    --accent-blue: #3b82f6;
    --accent-teal: #10b981;
    --accent-purple: #8b5cf6;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #26334d;
  }}
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-main);
    line-height: 1.5;
    padding: 24px 16px;
  }}
  .container {{
    max-width: 1200px;
    margin: 0 auto;
  }}
  header {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
  }}
  .badge-tag {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}
  .tag-sustainability {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
  .tag-environment {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
  .tag-social {{ background: rgba(139, 92, 246, 0.15); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.3); }}
  .tag-business {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
  
  h1 {{
    font-size: 2rem;
    font-weight: 800;
    margin: 12px 0 6px 0;
    background: linear-gradient(to right, #60a5fa, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .subtitle {{
    color: var(--text-muted);
    font-size: 1rem;
    max-width: 800px;
  }}
  
  /* Stats Grid */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }}
  .stat-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
  }}
  .stat-val {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-main);
  }}
  .stat-label {{
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 4px;
  }}

  /* Charts Container */
  .visuals-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
  }}
  .chart-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
  }}
  .chart-title {{
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 16px;
  }}
  .bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    font-size: 0.875rem;
  }}
  .bar-label {{
    width: 120px;
    color: var(--text-muted);
    font-weight: 500;
  }}
  .bar-track {{
    flex: 1;
    height: 10px;
    background: #1e293b;
    border-radius: 6px;
    margin: 0 12px;
    overflow: hidden;
  }}
  .bar-fill {{
    height: 100%;
    border-radius: 6px;
  }}
  .bar-val {{
    width: 40px;
    text-align: right;
    font-weight: 700;
  }}

  /* Candidates Section */
  .section-title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .candidate-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.15s ease, border-color 0.15s ease;
  }}
  .candidate-card:hover {{
    border-color: #3b82f6;
  }}
  .card-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 16px;
  }}
  .cand-rank {{
    font-size: 1.25rem;
    font-weight: 800;
    color: #60a5fa;
    margin-right: 8px;
  }}
  .cand-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-main);
  }}
  .meta-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0 16px 0;
  }}
  .pill {{
    background: #1e293b;
    border: 1px solid #334155;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 0.8rem;
    color: #cbd5e1;
  }}
  
  /* Scorecard Table */
  .scorecard-mini {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 8px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 16px;
    text-align: center;
  }}
  .sc-item-label {{
    font-size: 0.72rem;
    color: var(--text-muted);
    text-transform: uppercase;
  }}
  .sc-item-val {{
    font-size: 1.1rem;
    font-weight: 800;
    color: #38bdf8;
    margin-top: 2px;
  }}
  .sc-total {{
    color: #4ade80 !important;
  }}

  /* Quotes Box */
  .quotes-container {{
    border-top: 1px solid #1e293b;
    padding-top: 14px;
    margin-top: 14px;
  }}
  .quotes-heading {{
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
  }}
  .quote-item {{
    background: #0f172a;
    border-left: 3px solid #3b82f6;
    border-radius: 4px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #e2e8f0;
  }}
  .quote-author-link {{
    margin-top: 6px;
    font-size: 0.78rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .quote-link {{
    color: #60a5fa;
    text-decoration: none;
    font-weight: 600;
  }}
  .quote-link:hover {{
    text-decoration: underline;
  }}
  footer {{
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85rem;
    padding: 40px 0 20px 0;
    border-top: 1px solid var(--border-color);
    margin-top: 40px;
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <div style="display: flex; gap: 8px; align-items: center;">
      <span class="badge-tag tag-sustainability">BIT Mesra Case Comp</span>
      <span class="badge-tag tag-social">Round 2 Problem Discovery</span>
    </div>
    <h1>Real-World Problem Discovery Engine</h1>
    <p class="subtitle">
      Automated multi-source intelligence pipeline synthesizing public discussions across Reddit India communities, Hacker News, Google News, and YouTube.
    </p>
  </header>

  <!-- Key Metrics -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-val">{total_records}</div>
      <div class="stat-label">Verified Posts Mined</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{total_candidates}</div>
      <div class="stat-label">Distinct Problem Clusters</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{len(source_counts)}</div>
      <div class="stat-label">Active Public Sources</div>
    </div>
    <div class="stat-card">
      <div class="stat-val">{round(sum(c.avg_pain_score for c in top_candidates)/max(1, len(top_candidates)), 1)} / 10</div>
      <div class="stat-label">Top Candidates Avg Pain Score</div>
    </div>
  </div>

  <!-- Visual Breakdowns -->
  <div class="visuals-grid">
    <!-- Theme Breakdown -->
    <div class="chart-card">
      <div class="chart-title">Topic Distribution by Theme</div>
"""
    # Render Theme Bars
    theme_colors = {
        "Sustainability": "#10b981",
        "Environment": "#3b82f6",
        "Social impact": "#8b5cf6",
        "Business": "#f59e0b"
    }
    for theme_name, col in theme_colors.items():
        cnt = theme_counts.get(theme_name, 0)
        pct = (cnt / max(1, total_records)) * 100
        html += f"""
      <div class="bar-row">
        <div class="bar-label">{theme_name}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: {pct:.1f}%; background-color: {col};"></div>
        </div>
        <div class="bar-val">{cnt}</div>
      </div>
"""
    html += """
    </div>

    <!-- Source Breakdown -->
    <div class="chart-card">
      <div class="chart-title">Data Source Diversity</div>
"""
    source_colors = {
        "reddit": "#ff4500",
        "google_news": "#4285f4",
        "hackernews": "#ff6600",
        "youtube": "#ff0000"
    }
    for src_name, col in source_colors.items():
        cnt = source_counts.get(src_name, 0)
        pct = (cnt / max(1, total_records)) * 100
        html += f"""
      <div class="bar-row">
        <div class="bar-label">{src_name.replace('_', ' ').title()}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width: {pct:.1f}%; background-color: {col};"></div>
        </div>
        <div class="bar-val">{cnt}</div>
      </div>
"""
    html += f"""
    </div>
  </div>

  <!-- Candidates List -->
  <div class="section-title">
    <span>🏆 Ranked Problem Candidates for 3-5 Slide Deck</span>
  </div>
"""

    for rank, cand in enumerate(top_candidates, 1):
        theme_tag_class = {
            "Sustainability": "tag-sustainability",
            "Environment": "tag-environment",
            "Social impact": "tag-social",
            "Business": "tag-business"
        }.get(cand.theme, "tag-social")

        sc = cand.scorecard

        html += f"""
  <div class="candidate-card" id="candidate-{rank}">
    <div class="card-top">
      <div>
        <span class="cand-rank">#{rank}</span>
        <span class="cand-title">{cand.title}</span>
      </div>
      <span class="badge-tag {theme_tag_class}">{cand.theme}</span>
    </div>

    <div class="meta-pills">
      <span class="pill">📊 <strong>{cand.size}</strong> mentions</span>
      <span class="pill">🌐 <strong>{cand.distinct_sources}</strong> sources</span>
      <span class="pill">🔥 Pain Score: <strong>{cand.avg_pain_score:.1f}/10</strong></span>
      <span class="pill">📈 Trend: <strong>{cand.growth_over_time}</strong></span>
      <span class="pill">🏷️ {', '.join(cand.top_terms[:3])}</span>
    </div>

    <!-- Section 9 Scorecard Mini -->
    <div class="scorecard-mini">
      <div>
        <div class="sc-item-label">Depth of Pain</div>
        <div class="sc-item-val">{sc.get("Depth of pain", 0)}/5</div>
      </div>
      <div>
        <div class="sc-item-label">Data Avail.</div>
        <div class="sc-item-val">{sc.get("Data available", 0)}/5</div>
      </div>
      <div>
        <div class="sc-item-label">Novel Angle</div>
        <div class="sc-item-val">{sc.get("Novel angle", 0)}/5</div>
      </div>
      <div>
        <div class="sc-item-label">6-Mo Feas.</div>
        <div class="sc-item-val">{sc.get("Feasible in ~6 mo", 0)}/5</div>
      </div>
      <div>
        <div class="sc-item-label">Impact</div>
        <div class="sc-item-val">{sc.get("Measurable impact", 0)}/5</div>
      </div>
      <div>
        <div class="sc-item-label">Total Score</div>
        <div class="sc-item-val sc-total">{sc.get("Total", 0)}/25</div>
      </div>
    </div>

    <!-- Quotes & Traceability -->
    <div class="quotes-container">
      <div class="quotes-heading">Voice of the People (Traceable Citations)</div>
"""
        for q in cand.representative_quotes:
            q_text = q["quote"].replace("<", "&lt;").replace(">", "&gt;")
            html += f"""
      <div class="quote-item">
        "{q_text}"
        <div class="quote-author-link">
          <span style="color: var(--text-muted);">{q['source'].replace('_', ' ').title()} • Score: {q['score']}</span>
          <a href="{q['url']}" target="_blank" rel="noopener noreferrer" class="quote-link">View Source ↗</a>
        </div>
      </div>
"""
        html += """
    </div>
  </div>
"""

    html += """
  <footer>
    <p>Generated for BIT Mesra Case Competition 2026 • Problem Discovery Pipeline</p>
    <p style="margin-top: 4px; font-size: 0.75rem;">100% Offline Compatible • Zero PII Stored • Fully Attributed</p>
  </footer>
</div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Generated HTML report: {output_path}")
