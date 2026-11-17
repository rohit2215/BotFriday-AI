# Implementation Explanation — BotFriday-AI

## Overview
`BotFriday-AI` is an end-to-end, real-time hiring intelligence pipeline that discovers **Indian companies (50–500 employees)** actively hiring for **Software Engineering** roles within the **last 14 days**, verifies that every company website and job posting URL is live (HTTP `< 400`), enriches each record with verified decision-maker details and real hiring signals, and exports the output to a Google-Sheets-ready CSV (`output/companies_hiring.csv`), a Markdown report (`output/companies_hiring.md`), and optionally directly to Google Sheets via `gspread`.

## Architecture & Pipeline Flow

```
config/companies_watchlist.json
        │
        ▼
src/collectors/ (Ashby, Greenhouse, Lever, SmartRecruiters, Workable)
        │  ──► Live ATS JSON APIs (no stale caches)
        ▼
src/verifier.py
        │  ──► Filters postings to last 14 days + HTTP 200 verification
        ▼
src/enricher.py
        │  ──► Attaches verified Founder/CEO/COO, LinkedIn URL, hiring signal
        ▼
src/exporters/ (CSV, Markdown, Google Sheets)
        │
        ▼
output/companies_hiring.csv  &  output/companies_hiring.md
```

### Key Modules
1. **Configuration & Models (`src/config.py`, `src/models.py`)**
   - Defines `CompanyTarget`, `DecisionMaker`, `JobPosting`, and `EnrichedLead` dataclasses.
   - Configures Indian location keywords (`India`, `Bengaluru`, `Bangalore`, `Hyderabad`, `Mumbai`, `Gurugram`, `Pune`, `Chennai`, `Noida`, etc.) and Software Engineering title filters.
2. **Real-Time ATS Collectors (`src/collectors/`)**
   - `AshbyCollector`: `https://api.ashbyhq.com/posting-api/job-board/{board_token}`
   - `GreenhouseCollector`: `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=false`
   - `LeverCollector`: `https://api.lever.co/v0/postings/{board_token}?mode=json`
   - `SmartRecruitersCollector`: `https://api.smartrecruiters.com/v1/companies/{board_token}/postings`
   - `WorkableCollector`: `https://apply.workable.com/api/v1/widget/accounts/{board_token}`
3. **Recency & Link Verifier (`src/verifier.py`)**
   - `is_within_lookback()` enforces the 14-day window (`2026-11-03` to `2026-11-17` UTC on run date).
   - `verify_url_live()` performs live HTTP checks (with browser User-Agent fallback for WAF-protected sites) to guarantee zero dead links.
4. **Exporters (`src/exporters/`)**
   - `csv_exporter.py`: Writes the exact 6-column Google Sheets CSV (`output/companies_hiring.csv`).
   - `markdown_exporter.py`: Writes a formatted Markdown table (`output/companies_hiring.md`).
   - `sheets_exporter.py`: Optional `gspread` integration to push directly to a Google Sheet using a service account (`GOOGLE_SHEET_ID` & `service_account.json`).

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Generate CSV & Markdown from live ATS APIs
python3 main.py --limit 10 --days 14

# Optional: also push directly to Google Sheets
# export GOOGLE_SHEET_ID="your-sheet-id"
# python3 main.py --limit 10 --days 14 --sheets
```

## Desired Output (Live Run on 2026-11-17)

| Company and its website | Job title and a link to the job post | Date posted | Decision maker | LinkedIn profile link | Why they might need hiring help |
| --- | --- | --- | --- | --- | --- |
| Sarvam AI (https://www.sarvam.ai) | SDE2 - Full Stack — https://jobs.ashbyhq.com/sarvam/fa96b55d-0c77-423d-8eef-f579c8496adb | 2026-11-17 | Dr. Pratyush Kumar, Co-Founder & CEO | https://www.linkedin.com/company/sarvamai | Scaling sovereign Indian-language foundation models and Samvaad voice/agentic AI platform with 48 open roles on Ashby. |
| AiPrise (https://www.aiprise.com) | Software Engineer I, Full Stack (Frontend Focused) (Bangalore, India) — https://jobs.ashbyhq.com/aiprise/41af4efa-a550-484e-afde-a9f5f3807eca | 2026-11-11 | Chaitanya Sarda, Co-Founder & CEO | https://www.linkedin.com/in/chaitanyasarda/ | YC-backed Series A compliance startup expanding its Bengaluru engineering hub across Frontend, Full-Stack, and HR roles. (currently 2 live SWE roles on Ashby). |
| Bureau (https://www.bureau.id) | Senior DevOps Engineer — https://jobs.ashbyhq.com/bureau/54c0efa8-d02e-4565-9a3b-83753b07fad0 | 2026-11-04 | Ranjan Reddy, Founder & CEO | https://www.linkedin.com/in/ranjanready/ | Post-Series B fraud-prevention platform scaling cloud infrastructure and identity decisioning engineering in Bengaluru. |
| CertifyOS (https://www.certifyos.com) | Staff Data Platform Engineer — https://jobs.ashbyhq.com/certifyos/dc312473-7dd8-449c-b707-a8c3231bca56 | 2026-11-05 | Anshul Rathi, Founder & CEO | https://www.linkedin.com/company/certifyos | Post-Series B healthcare credentialing platform hiring simultaneously for Staff Data Platform, SDET, and Data roles in Bengaluru. (currently 2 live SWE roles on Ashby). |
| Enterpret (https://www.enterpret.com) | Staff Database Engineer, ClickHouse — https://job-boards.greenhouse.io/enterpret/jobs/8200143003 | 2026-11-10 | Varun Sharma, Co-Founder & CEO | https://www.linkedin.com/company/enterpret | AI customer-intelligence platform scaling ClickHouse and high-throughput analytics infrastructure onsite in Bengaluru. |
| Fortanix (https://www.fortanix.com) | Senior Software Engineer - Backend — https://apply.workable.com/j/99549EF3C5 | 2026-11-06 | Anand Kashyap, Co-Founder & CEO | https://www.linkedin.com/company/fortanix | Confidential computing & data-security firm actively recruiting Senior Backend engineers in Bengaluru. |
| AbhiBus (https://www.abhibus.com) | Software Engineer - I / II(Java) — https://jobs.smartrecruiters.com/abhibus/744000161056750 | 2026-11-11 | Rohit Sharma, COO | https://www.linkedin.com/company/abhibus | Expanding SRTC & private bus GDS integrations and AI-driven tracking out of its Hyderabad engineering center. |
| Certa (https://www.certa.ai) | Solutions Engineer — https://jobs.ashbyhq.com/certa/2eee37a0-31f5-4302-bbaf-0e729b61c9e2 | 2026-11-15 | Jagmeet Lamba, Founder & CEO | https://www.linkedin.com/in/jlamba/ | AI-first third-party risk management platform hiring technical Solutions Engineers across India for enterprise rollouts. |
| SuperApp (https://superapp.chat) | Solution Engineer (Early to Mid Level) — https://job-boards.greenhouse.io/superapp/jobs/8930209002 | 2026-11-04 | Anant Bhardwaj, Founder & CEO | https://www.linkedin.com/in/anant | Rebranded from Instabase in Aug 2026 to launch its multiplayer AI workspace, hiring technical engineers in Bengaluru. |
| Encord (https://encord.com) | DevOps Engineer — https://jobs.ashbyhq.com/encord/4028d589-6973-42ab-919d-4b8e625b4913 | 2026-11-13 | Eric Landau, Co-Founder & Co-CEO | https://www.linkedin.com/in/eric-landau-40992ab0/ | Physical-AI data infrastructure startup scaling distributed DevOps & cloud reliability engineering in India. |
