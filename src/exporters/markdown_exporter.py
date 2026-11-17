"""Markdown table exporter for human-readable reports."""

from datetime import datetime, timezone
from pathlib import Path

from src.exporters import SHEET_HEADERS
from src.models import EnrichedLead


def _escape_md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def export_markdown(leads: list[EnrichedLead], output_path: Path) -> Path:
    """Write enriched leads to a Markdown table with generation timestamp."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Indian Companies (50–500 Employees) Hiring Software Engineers",
        "",
        f"_Generated from live ATS APIs on {generated_at}._",
        "",
        "| " + " | ".join(SHEET_HEADERS) + " |",
        "| " + " | ".join("---" for _ in SHEET_HEADERS) + " |",
    ]

    for lead in leads:
        row = [_escape_md(cell) for cell in lead.to_sheet_row()]
        lines.append("| " + " | ".join(row) + " |")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path

