"""Real-time Greenhouse Boards API collector."""

from src.collectors.base import BaseATSCollector
from src.models import JobPosting


class GreenhouseCollector(BaseATSCollector):
    """Fetches live job postings from Greenhouse's public Job Board API."""

    provider_name = "greenhouse"
    API_URL = "https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=false"

    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        payload = self._get_json(self.API_URL.format(board_token=board_token))
        postings: list[JobPosting] = []

        for item in payload.get("jobs", []):
            title = (item.get("title") or "").strip()
            location = ((item.get("location") or {}).get("name") or "").strip()
            updated_at = item.get("updated_at")
            job_url = (item.get("absolute_url") or "").strip()
            departments = item.get("departments") or []
            dept_name = (departments[0].get("name") or "").strip() if departments else ""

            if not (title and updated_at and job_url):
                continue
            if not self.is_software_engineering_role(title):
                continue
            if not self.is_india_location(location):
                continue

            postings.append(
                JobPosting(
                    title=title,
                    job_url=job_url,
                    location=location,
                    posted_at=self.parse_iso_datetime(updated_at),
                    ats_provider=self.provider_name,
                    department=dept_name,
                )
            )

        return postings

