import os
import sys
import argparse
import logging
import yaml
from typing import Any, Dict, List

# Ensure scraper dir is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from sources.reddit import RedditSource
from sources.hackernews import HackerNewsSource
from sources.google_news import GoogleNewsSource
from sources.youtube import YouTubeSource
from sources.stubs import QuoraStubSource, TwitterStubSource

from processing.cleaner import clean_and_normalize
from processing.scorer import score_all_records
from processing.tagger import tag_all_records
from processing.clusterer import cluster_problems
from processing.feasibility import evaluate_all_candidates

from report.generator import (
    generate_csv,
    generate_json,
    generate_shortlist_markdown,
    generate_html_report,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("problem_discovery")

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration YAML file."""
    if not os.path.exists(config_path):
        # Fallback to local config.yaml
        alt_path = os.path.join(SCRIPT_DIR, "config.yaml")
        if os.path.exists(alt_path):
            config_path = alt_path
        else:
            raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_pipeline(
    topics: List[str],
    config: Dict[str, Any],
    limit_per_topic: int = 100,
    use_llm: bool = False,
    disabled_sources: List[str] = None,
    output_dir: str = "output",
    raw_data_dir: str = "data/raw",
    dry_run: bool = False,
):
    """Run the entire problem discovery pipeline."""
    if disabled_sources is None:
        disabled_sources = []

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(raw_data_dir, exist_ok=True)

    pain_phrases = config.get("pain_phrases", [])
    src_cfg = config.get("sources", {})

    # Check active sources
    active_sources = []
    
    if "reddit" not in disabled_sources and src_cfg.get("reddit", {}).get("enabled", True):
        active_sources.append(RedditSource(config, raw_cache_dir=raw_data_dir))
    
    if "hackernews" not in disabled_sources and src_cfg.get("hackernews", {}).get("enabled", True):
        active_sources.append(HackerNewsSource(config, raw_cache_dir=raw_data_dir))

    if "google_news" not in disabled_sources and src_cfg.get("google_news", {}).get("enabled", True):
        active_sources.append(GoogleNewsSource(config, raw_cache_dir=raw_data_dir))

    if "youtube" not in disabled_sources and src_cfg.get("youtube", {}).get("enabled", True):
        active_sources.append(YouTubeSource(config, raw_cache_dir=raw_data_dir))

    # Stubs
    if "quora" not in disabled_sources and src_cfg.get("quora", {}).get("enabled", False):
        active_sources.append(QuoraStubSource(config, raw_cache_dir=raw_data_dir))
    if "twitter" not in disabled_sources and src_cfg.get("twitter", {}).get("enabled", False):
        active_sources.append(TwitterStubSource(config, raw_cache_dir=raw_data_dir))

    logger.info(f"Initialized {len(active_sources)} active sources: {[s.name for s in active_sources]}")

    if dry_run or not active_sources:
        logger.info("[DRY RUN] Exiting cleanly as requested or all sources disabled.")
        return [], []

    # Step 2: Data Collection
    raw_records: List[Dict[str, Any]] = []
    source_limit = max(10, limit_per_topic // max(1, len(active_sources)))

    for topic in topics:
        logger.info(f"=== Mining Topic: '{topic}' ===")
        for source in active_sources:
            try:
                records = source.search(topic=topic, pain_phrases=pain_phrases, limit=source_limit)
                raw_records.extend(records)
                logger.info(f"  Source '{source.name}' retrieved {len(records)} records.")
            except Exception as e:
                logger.error(f"  Source '{source.name}' failed on topic '{topic}': {e}")

    logger.info(f"Total raw items collected: {len(raw_records)}")

    # Step 3: Normalisation & Cleaning
    cleaned_records = clean_and_normalize(raw_records)
    logger.info(f"Total cleaned & deduplicated records: {len(cleaned_records)}")

    if not cleaned_records:
        logger.warning("No records passed cleaning and deduplication.")
        return [], []

    # Step 4: Pain-Point Scoring & Theme Tagging
    scored_records = score_all_records(cleaned_records, custom_pain_phrases=pain_phrases)
    tagged_records = tag_all_records(scored_records, use_llm=use_llm)

    # Step 5: Clustering
    candidates = cluster_problems(tagged_records, config=config)
    logger.info(f"Formed {len(candidates)} problem candidates.")

    # Step 6: Feasibility Scorecard (Section 9)
    evaluated_candidates = evaluate_all_candidates(candidates)

    # Step 7: Output Generation
    csv_path = os.path.join(output_dir, "problems.csv")
    json_path = os.path.join(output_dir, "problems.json")
    html_path = os.path.join(output_dir, "report.html")
    shortlist_path = os.path.join(output_dir, "shortlist.md")

    generate_csv(evaluated_candidates, csv_path)
    generate_json(evaluated_candidates, json_path)
    generate_html_report(evaluated_candidates, tagged_records, html_path)
    generate_shortlist_markdown(evaluated_candidates, shortlist_path)

    # Console Summary Table
    print("\n" + "=" * 90)
    print(" [*] PROBLEM DISCOVERY PIPELINE - TOP CANDIDATES SUMMARY")
    print("=" * 90)
    print(f"{'Rank':<5} | {'Candidate Title':<42} | {'Theme':<15} | {'Size':<5} | {'Pain':<6} | {'Score/25':<8}")
    print("-" * 90)
    for idx, c in enumerate(evaluated_candidates[:10], 1):
        sc_total = c.scorecard.get("Total", 0)
        title_disp = (c.title[:39] + "...") if len(c.title) > 42 else c.title
        print(f"#{idx:<4} | {title_disp:<42} | {c.theme:<15} | {c.size:<5} | {c.avg_pain_score:<6.1f} | {sc_total:<8}/25")
    print("=" * 90)
    print(f"[>] Reports written to: {os.path.abspath(output_dir)}")
    print(f"   - HTML Report:      {os.path.abspath(html_path)}")
    print(f"   - Shortlist MD:     {os.path.abspath(shortlist_path)}")
    print(f"   - Problems CSV:     {os.path.abspath(csv_path)}")
    print(f"   - Problems JSON:    {os.path.abspath(json_path)}")
    print("=" * 90 + "\n")

    return evaluated_candidates, tagged_records

def main():
    parser = argparse.ArgumentParser(
        description="Real-World Problem Discovery Pipeline for Case Competition (BIT Mesra)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Single search topic (e.g. 'food waste', 'e-waste')",
    )
    parser.add_argument(
        "--topics",
        type=str,
        default=None,
        help="Comma-separated list of topics",
    )
    parser.add_argument(
        "--all-topics",
        action="store_true",
        help="Run all seed topics defined in config.yaml",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=150,
        help="Target number of records to collect per topic",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save generated reports and data",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use Anthropic Claude API for classification and problem extraction (requires ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--disable-sources",
        type=str,
        default="",
        help="Comma-separated list of sources to disable (e.g., 'youtube,quora')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform configuration check and exit without fetching data",
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    # Determine topic list
    topics = []
    if args.topic:
        topics.append(args.topic)
    elif args.topics:
        topics.extend([t.strip() for t in args.topics.split(",") if t.strip()])
    elif args.all_topics:
        topics.extend(config.get("topics", ["food waste"]))
    else:
        # Default topic
        topics.append("food waste")

    disabled = [s.strip().lower() for s in args.disable_sources.split(",") if s.strip()]

    # Run pipeline
    run_pipeline(
        topics=topics,
        config=config,
        limit_per_topic=args.limit,
        use_llm=args.use_llm,
        disabled_sources=disabled,
        output_dir=args.output_dir,
        raw_data_dir=config.get("output", {}).get("raw_data_dir", "data/raw"),
        dry_run=args.dry_run,
    )

if __name__ == "__main__":
    main()
