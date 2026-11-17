"""Data models for company targets, live job postings, and verified leads."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class DecisionMaker:
    """Verified founder, CTO, or HR head at a target company."""

    name: str
    role: str
    linkedin_url: str


@dataclass(frozen=True)
class CompanyTarget:
    """A vetted Indian company (50-500 employees) tracked on an ATS."""

    name: str
    website: str
    ats_provider: str  # "ashby" | "greenhouse" | "lever"
    ats_board_token: str
    employee_range: str
    hq_city: str
    decision_maker: DecisionMaker
    hiring_signal: str


@dataclass(frozen=True)
class JobPosting:
    """A real-time software engineering job posting fetched from an ATS."""

    title: str
    job_url: str
    location: str
    posted_at: datetime
    ats_provider: str
    department: str = ""


@dataclass(frozen=True)
class EnrichedLead:
    """Final verified row matching the Google Sheet output schema."""

    company_and_website: str
    job_title_and_link: str
    date_posted: str
    decision_maker: str
    linkedin_profile: str
    why_hiring_help: str
    employee_range: str
    location: str
    verified_http_status: Optional[int] = None

    def to_sheet_row(self) -> list[str]:
        """Return the exact 6-column row required by the Google Sheet."""
        return [
            self.company_and_website,
            self.job_title_and_link,
            self.date_posted,
            self.decision_maker,
            self.linkedin_profile,
            self.why_hiring_help,
        ]

    def to_dict(self) -> dict[str, str]:
        """Return dictionary representation for CSV/JSON serialization."""
        return asdict(self)
