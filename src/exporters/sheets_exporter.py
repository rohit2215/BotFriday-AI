"""Optional Google Sheets uploader using gspread and a service account."""

import os
from pathlib import Path
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from src.exporters import SHEET_HEADERS
from src.models import EnrichedLead

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def export_google_sheet(
    leads: list[EnrichedLead],
    sheet_id: Optional[str] = None,
    service_account_path: Optional[Path] = None,
    worksheet_name: str = "Hiring Leads",
) -> str:
    """Upload verified leads to a Google Sheet and return its URL."""
    resolved_sheet_id = sheet_id or os.getenv("GOOGLE_SHEET_ID", "")
    resolved_creds = service_account_path or Path(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
    )

    if not resolved_sheet_id:
        raise ValueError("GOOGLE_SHEET_ID is required for Google Sheets export.")
    if not resolved_creds.exists():
        raise FileNotFoundError(
            f"Google service account JSON not found at {resolved_creds}"
        )

    credentials = Credentials.from_service_account_file(
        str(resolved_creds), scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(resolved_sheet_id)

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name, rows=100, cols=len(SHEET_HEADERS)
        )

    rows = [SHEET_HEADERS] + [lead.to_sheet_row() for lead in leads]
    worksheet.clear()
    worksheet.update(rows, value_input_option="USER_ENTERED")
    return spreadsheet.url
