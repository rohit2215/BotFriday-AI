"""Shared base class and filtering helpers for ATS collectors."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

import requests

from src.config import (
    INDIA_LOCATION_KEYWORDS,
    REQUEST_TIMEOUT_SECONDS,
    SWE_EXCLUDE_KEYWORDS,
    SWE_TITLE_KEYWORDS,
    USER_AGENT,
)
from src.models import JobPosting


class BaseATSCollector(ABC):
    """Abstract base class for real-time ATS job board collectors."""

    provider_name: str = ""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def _get_json(self, url: str) -> Any:
        """Fetch JSON payload from a public ATS endpoint."""
        response = self.session.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def is_software_engineering_role(title: str) -> bool:
        """Return True if the job title represents a software engineering role."""
        normalized = title.lower()
        if any(excluded in normalized for excluded in SWE_EXCLUDE_KEYWORDS):
            return False
        return any(keyword in normalized for keyword in SWE_TITLE_KEYWORDS)

    @staticmethod
    def is_india_location(location: str) -> bool:
        """Return True if the job location is in India."""
        normalized = location.lower()
        return any(keyword in normalized for keyword in INDIA_LOCATION_KEYWORDS)

    @staticmethod
    def parse_iso_datetime(value: str) -> datetime:
        """Parse an ISO-8601 timestamp into a timezone-aware UTC datetime."""
        cleaned = value.strip()
        if cleaned.endswith("Z"):
            cleaned = cleaned[:-1] + "+00:00"
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @abstractmethod
    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        """Fetch all active software engineering jobs in India for a board."""

