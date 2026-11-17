"""Real-time Workable Widget API collector."""

from src.collectors.base import BaseATSCollector
from src.models import JobPosting


class WorkableCollector(BaseATSCollector):
    """Fetches live job postings from Workable's public widget API."""

    provider_name = "workable"
    API_URL = "https://apply.workable.com/api/v1/widget/accounts/{board_token}"

    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        payload = self._get_json(self.API_URL.format(board_token=board_token))
        postings: list[JobPosting] = []

        for item in payload.get("jobs", []):
            title = (item.get("title") or "").strip()
            location = ", ".join(
                part for part in [item.get("city"), item.get("country")] if part
            )
            published_on = item.get("published_on")
            job_url = (item.get("url") or "").strip()

            if not (title and published_on and job_url):
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
                    posted_at=self.parse_iso_datetime(published_on),
                    ats_provider=self.provider_name,
                    department=(item.get("department") or "").strip(),
                )
            )

        return postings
