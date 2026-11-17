"""End-to-end CLI pipeline for real-time Indian SWE hiring intelligence."""

import argparse
import logging
from pathlib import Path

import requests

from src.collectors import get_collector
from src.config import (
    DEFAULT_LOOKBACK_DAYS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TARGET_COUNT,
    DEFAULT_WATCHLIST_PATH,
    USER_AGENT,
)
from src.enricher import build_enriched_lead, load_watchlist
from src.exporters.csv_exporter import export_csv
from src.exporters.markdown_exporter import export_markdown
from src.exporters.sheets_exporter import export_google_sheet
from src.models import EnrichedLead
from src.verifier import is_within_lookback, verify_url_live

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("botfriday")


def run_pipeline(
    watchlist_path: Path,
    output_dir: Path,
    lookback_days: int,
    limit: int,
    push_to_sheets: bool = False,
) -> list[EnrichedLead]:
    """Fetch live ATS postings, verify recency & links, enrich, and export."""
    companies = load_watchlist(watchlist_path)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    leads: list[EnrichedLead] = []

    for company in companies:
        if len(leads) >= limit:
            break

        logger.info("Querying %s (%s/%s)...", company.name, company.ats_provider, company.ats_board_token)
        try:
            collector = get_collector(company.ats_provider)
            postings = collector.fetch_jobs(company.ats_board_token)
        except Exception as exc:
            logger.warning("Skipping %s: ATS fetch failed (%s)", company.name, exc)
            continue

        recent_postings = [
            job for job in postings if is_within_lookback(job.posted_at, lookback_days)
        ]
        if not recent_postings:
            logger.info("No India SWE postings in last %d days for %s.", lookback_days, company.name)
            continue

        # Prefer the most recently posted SWE role
        recent_postings.sort(key=lambda j: j.posted_at, reverse=True)

        # Verify company website is live
        website_status = verify_url_live(company.website, session=session)
        if website_status is None:
            logger.warning("Skipping %s: website unreachable (%s)", company.name, company.website)
            continue

        verified_lead = None
        for job in recent_postings:
            job_status = verify_url_live(job.job_url, session=session)
            if job_status is not None:
                verified_lead = build_enriched_lead(
                    company=company,
                    posting=job,
                    verified_status=job_status,
                    total_open_swe_roles=len(recent_postings),
                )
                break

        if verified_lead is None:
            logger.warning("Skipping %s: no live job URLs returned HTTP < 400", company.name)
            continue

        leads.append(verified_lead)
        logger.info(
            "Verified [%d/%d]: %s -> %s (%s)",
            len(leads),
            limit,
            company.name,
            verified_lead.date_posted,
            verified_lead.verified_http_status,
        )

    csv_path = export_csv(leads, output_dir / "companies_hiring.csv")
    md_path = export_markdown(leads, output_dir / "companies_hiring.md")
    logger.info("Exported %d verified leads to %s and %s", len(leads), csv_path, md_path)

    if push_to_sheets:
        sheet_url = export_google_sheet(leads)
        logger.info("Uploaded leads to Google Sheet: %s", sheet_url)

    return leads


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find Indian companies (50-500 employees) hiring SWEs in real time."
    )
    parser.add_argument(
        "--watchlist",
        type=Path,
        default=DEFAULT_WATCHLIST_PATH,
        help="Path to companies watchlist JSON",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for CSV and Markdown outputs",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_LOOKBACK_DAYS,
        help="Lookback window in days (default: 14)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_TARGET_COUNT,
        help="Maximum number of verified companies to output (default: 10)",
    )
    parser.add_argument(
        "--sheets",
        action="store_true",
        help="Also upload results to Google Sheets (requires GOOGLE_SHEET_ID & service_account.json)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        watchlist_path=args.watchlist,
        output_dir=args.output_dir,
        lookback_days=args.days,
        limit=args.limit,
        push_to_sheets=args.sheets,
    )
