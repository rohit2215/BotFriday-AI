# BotFriday-AI — Real-Time Indian Tech Hiring Pipeline

An automated, real-time lead discovery and verification pipeline that identifies **Indian companies (50–500 employees)** that have posted **Software Engineering** roles within the **last 14 days**, enriches them with verified decision makers and hiring signals, and exports the results to Google-Sheet-ready CSV, Markdown, or directly to Google Sheets.

## Features
- **Real-Time ATS Collectors**: Queries live public JSON APIs from **Ashby**, **Greenhouse**, and **Lever** — zero stale cached data.
- **Strict Filtering**: Filters for Indian locations (`India`, `Bengaluru`, `Bangalore`, `Mumbai`, `Delhi`, `Gurugram`, `Hyderabad`, `Pune`, `Chennai`, `Noida`, `Remote - India`), Software Engineering roles, and postings published/updated within the last 14 days.
- **Link & Freshness Verification**: Validates HTTP status codes on company websites and job post URLs so there are no dead links.
- **Decision Maker & Signal Enrichment**: Attaches verified Founder / CTO / HR Head names, roles, LinkedIn URLs, and evidence-backed hiring signals.
- **Multi-Format Export**: Outputs to `output/companies_hiring.csv`, `output/companies_hiring.md`, and optionally uploads directly to Google Sheets via `gspread`.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 main.py --limit 10 --days 14
```

See [IMPLEMENTATION_EXPLANATION.md](IMPLEMENTATION_EXPLANATION.md) for architecture details and the generated output.

