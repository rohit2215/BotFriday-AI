"""Real-time SmartRecruiters Postings API collector."""

from src.collectors.base import BaseATSCollector
from src.models import JobPosting


class SmartRecruitersCollector(BaseATSCollector):
    """Fetches live job postings from SmartRecruiters' public Postings API."""

    provider_name = "smartrecruiters"
    API_URL = "https://api.smartrecruiters.com/v1/companies/{board_token}/postings"
    JOB_URL = "https://jobs.smartrecruiters.com/{board_token}/{job_id}"

    def fetch_jobs(self, board_token: str) -> list[JobPosting]:
        payload = self._get_json(self.API_URL.format(board_token=board_token))
        postings: list[JobPosting] = []

        for item in payload.get("content", []):
            title = (item.get("name") or "").strip()
            loc_obj = item.get("location") or {}
            location = ", ".join(
                part for part in [loc_obj.get("city"), loc_obj.get("country")] if part
            )
            released_date = item.get("releasedDate")
            job_id = item.get("id")
            dept = ((item.get("department") or {}).get("label") or "").strip()

            if not (title and released_date and job_id):
                continue
            if not self.is_software_engineering_role(title):
                continue
            if not self.is_india_location(location):
                continue

            postings.append(
                JobPosting(
                    title=title,
                    job_url=self.JOB_URL.format(board_token=board_token, job_id=job_id),
                    location=location,
                    posted_at=self.parse_iso_datetime(released_date),
                    ats_provider=self.provider_name,
                    department=dept,
                )
            )

        return postings

