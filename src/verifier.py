"""Real-time recency and HTTP link verification utilities."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from src.config import REQUEST_TIMEOUT_SECONDS, USER_AGENT


def is_within_lookback(
    posted_at: datetime,
    lookback_days: int = 14,
    reference_now: Optional[datetime] = None,
) -> bool:
    """Return True if posted_at falls within [now - lookback_days, now]."""
    now = reference_now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=lookback_days)
    return cutoff <= posted_at <= now + timedelta(days=1)


def verify_url_live(url: str, session: Optional[requests.Session] = None) -> Optional[int]:
    """Check whether a URL is live (HTTP < 400). Returns status code or None on error."""
    client = session or requests.Session()
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = client.head(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
        if resp.status_code == 405 or resp.status_code >= 400:
            resp = client.get(
                url,
                headers=headers,
                timeout=REQUEST_TIMEOUT_SECONDS,
                allow_redirects=True,
                stream=True,
            )
        return resp.status_code if resp.status_code < 400 else None
    except requests.RequestException:
        return None
