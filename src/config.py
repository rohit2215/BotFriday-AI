"""Configuration constants and filtering rules for BotFriday-AI."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_WATCHLIST_PATH = BASE_DIR / "config" / "companies_watchlist.json"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"

DEFAULT_LOOKBACK_DAYS = 14
DEFAULT_TARGET_COUNT = 10
REQUEST_TIMEOUT_SECONDS = 15

USER_AGENT = (
    "BotFriday-AI-HiringPipeline/1.0 "
    "(+https://github.com/rohit2215/BotFriday-AI)"
)

SWE_TITLE_KEYWORDS = (
    "software engineer",
    "software developer",
    "backend engineer",
    "back-end engineer",
    "frontend engineer",
    "front-end engineer",
    "full stack",
    "fullstack",
    "full-stack",
    "sde",
    "platform engineer",
    "systems engineer",
    "distributed systems",
    "application engineer",
    "product engineer",
    "api platform",
    "founding engineer",
    "member of technical staff",
)

SWE_EXCLUDE_KEYWORDS = (
    "intern",
    "internship",
    "recruiter",
    "talent",
    "sales",
    "marketing",
    "designer",
    "product manager",
    "account executive",
    "customer success",
    "hr ",
    "finance",
)

INDIA_LOCATION_KEYWORDS = (
    "india",
    "bengaluru",
    "bangalore",
    "mumbai",
    "delhi",
    "ncr",
    "gurugram",
    "gurgaon",
    "noida",
    "hyderabad",
    "pune",
    "chennai",
    "kolkata",
    "ahmedabad",
)
