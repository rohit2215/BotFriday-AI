"""Watchlist loader and lead enrichment."""

import json
from pathlib import Path

from src.models import CompanyTarget, DecisionMaker, EnrichedLead, JobPosting


def load_watchlist(path: Path) -> list[CompanyTarget]:
    """Load vetted Indian 50-500 employee companies from JSON watchlist."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    targets: list[CompanyTarget] = []

    for entry in raw:
        dm_raw = entry["decision_maker"]
        targets.append(
            CompanyTarget(
                name=entry["name"],
                website=entry["website"],
                ats_provider=entry["ats_provider"],
                ats_board_token=entry["ats_board_token"],
                employee_range=entry["employee_range"],
                hq_city=entry["hq_city"],
                decision_maker=DecisionMaker(
                    name=dm_raw["name"],
                    role=dm_raw["role"],
                    linkedin_url=dm_raw["linkedin_url"],
                ),
                hiring_signal=entry["hiring_signal"],
            )
        )
    return targets


def build_enriched_lead(
    company: CompanyTarget,
    posting: JobPosting,
    verified_status: int,
    total_open_swe_roles: int,
) -> EnrichedLead:
    """Combine verified company metadata and live job posting into a sheet row."""
    signal = company.hiring_signal
    if total_open_swe_roles > 1 and "open" not in signal.lower():
        signal = f"{signal} (currently {total_open_swe_roles} live SWE roles on {posting.ats_provider.title()})."

    return EnrichedLead(
        company_and_website=f"{company.name} ({company.website})",
        job_title_and_link=f"{posting.title} — {posting.job_url}",
        date_posted=posting.posted_at.strftime("%Y-%m-%d"),
        decision_maker=f"{company.decision_maker.name}, {company.decision_maker.role}",
        linkedin_profile=company.decision_maker.linkedin_url,
        why_hiring_help=signal,
        employee_range=company.employee_range,
        location=posting.location or company.hq_city,
        verified_http_status=verified_status,
    )

