"""Real-time Lever Postings API collector."""

from datetime import datetime, timezone

from src.collectors.base import BaseATSCollector
from src.models import JobPosting


class LeverCollector(BaseATSCollector):
    """Fetches live job postings from Lever's public Postings API."""

    provider_name = "lever"
    API_URL = "https://api.lever.co/v0/postings/{board_token}?mode=json"

    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        items = self._get_json(self.API_URL.format(board_token=board_token))
        postings: list[JobPosting] = []

        for item in items:
            title = (item.get("text") or "").strip()
            categories = item.get("categories") or {}
            location = (categories.get("location") or "").strip()
            created_ms = item.get("createdAt")
            job_url = (item.get("hostedUrl") or "").strip()

            if not (title and created_ms and job_url):
                continue
            if not self.is_software_engineering_role(title):
                continue
            if not self.is_india_location(location):
                continue

            posted_at = datetime.fromtimestamp(created_ms / 1000.0, tz=timezone.utc)
            postings.append(
                JobPosting(
                    title=title,
                    job_url=job_url,
                    location=location,
                    posted_at=posted_at,
                    ats_provider=self.provider_name,
                    department=(categories.get("department") or "").strip(),
                )
            )

        return postings

