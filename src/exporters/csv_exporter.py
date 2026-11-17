"""CSV exporter formatted for direct Google Sheets import."""

import csv
from pathlib import Path

from src.exporters import SHEET_HEADERS
from src.models import EnrichedLead


def export_csv(leads: list[EnrichedLead], output_path: Path) -> Path:
    """Write enriched leads to a UTF-8 CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(SHEET_HEADERS)
        for lead in leads:
            writer.writerow(lead.to_sheet_row())
    return output_path

