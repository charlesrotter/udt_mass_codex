#!/usr/bin/env python3
"""Build the deterministic ninety-slot G165--G254 primary-evidence census."""

from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
REGISTRY = ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv"


def registry_rows() -> dict[int, dict[str, str]]:
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    result: dict[int, dict[str, str]] = {}
    for row in rows:
        match = re.fullmatch(r"G(\d+)", row["premise_id"])
        if match and 165 <= int(match.group(1)) <= 254:
            result[int(match.group(1))] = row
    return result


def main() -> None:
    current = registry_rows()
    output: list[dict[str, str]] = []
    for number in range(165, 255):
        directories = sorted(path for path in ROOT.glob(f"udt_g{number}_*") if path.is_dir())
        assert len(directories) == 1, (number, [path.name for path in directories])
        directory = directories[0]
        report_candidates = [directory / "AUDIT_REPORT.md", directory / "WHITEBOARD_REPORT.md"]
        reports = [path for path in report_candidates if path.is_file()]
        assert len(reports) == 1, (number, [path.name for path in reports])
        exact = directory / "EXACT_DERIVATION.md"
        row = current.get(number)
        controlling = row["controlling_source"] if row else ""
        historical_report = reports[0].relative_to(ROOT).as_posix()
        output.append({
            "slot": f"G{number}",
            "directory": directory.name,
            "primary_report": historical_report,
            "exact_derivation": exact.relative_to(ROOT).as_posix() if exact.is_file() else "",
            "registry_row": "PRESENT" if row else "ABSENT_META_OR_CONTROL",
            "registry_term": row["term"] if row else "",
            "current_controlling_source": controlling,
            "historical_report_is_current_controller": str(controlling == historical_report).lower() if row else "false",
        })
    assert len(output) == 90
    assert [row["slot"] for row in output] == [f"G{number}" for number in range(165, 255)]
    destination = PACKAGE / "SLOT_CENSUS.tsv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(destination)


if __name__ == "__main__":
    main()
