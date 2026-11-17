"""Real-time Ashby Posting API collector."""

from src.collectors.base import BaseATSCollector
from src.models import JobPosting


class AshbyCollector(BaseATSCollector):
    """Fetches live job postings from Ashby's public posting API."""

    provider_name = "ashby"
    API_URL = "https://api.ashbyhq.com/posting-api/job-board/{board_token}"

    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        payload = self._get_json(self.API_URL.format(board_token=board_token))
        postings: list[JobPosting] = []

        for item in payload.get("jobs", []):
            if item.get("isListed") is False:
                continue

            title = (item.get("title") or "").strip()
            location = (item.get("location") or "").strip()
            published_at = item.get("publishedAt")
            job_url = (item.get("jobUrl") or "").strip()

            if not (title and published_at and job_url):
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
                    posted_at=self.parse_iso_datetime(published_at),
                    ats_provider=self.provider_name,
                    department=(item.get("department") or "").strip(),
                )
            )

        return postings

