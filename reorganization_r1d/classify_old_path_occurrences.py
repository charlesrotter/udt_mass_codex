#!/usr/bin/env python3
"""Classify every remaining textual occurrence of the R1D original path token."""

from __future__ import annotations

import csv
from pathlib import Path

TOKEN = "simple_metric_S8_action_provenance_note.md"


def classification(path: str, line: str) -> str:
    if path.startswith(("reorganization_r0/", "reorganization_r1a/", "reorganization_r1b/", "reorganization_r1c/")):
        return "HISTORICAL_R0_R1C_FIXED_RECORD"
    if path.startswith("research/_registry/") and path != "research/_registry/CURRENT_ARTIFACT_PATHS.tsv":
        return "HISTORICAL_R1C_FIXED_REGISTRY"
    if path == "research/_registry/CURRENT_ARTIFACT_PATHS.tsv":
        return "CURRENT_MAP_ORIGINAL_IDENTITY_AND_DESTINATION_SUFFIX"
    if path == "research/macro/ROOT_INVENTORY.tsv" and "research/macro/" + TOKEN in line:
        return "CURRENT_PATH_DESTINATION_SUFFIX"
    if path.startswith("reorganization_r1d/"):
        return "R1D_CONTROL_OR_AUDIT_RECORD"
    return "STALE_CURRENT_POINTER"


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    output = Path(__file__).resolve().parent / "OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv"
    rows = []
    for path in sorted(p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts):
        if path == output:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        relative = path.relative_to(repo).as_posix()
        for number, line in enumerate(text.splitlines(), 1):
            count = line.count(TOKEN)
            if count:
                rows.append({"source": relative, "line": number, "occurrences": count,
                             "classification": classification(relative, line)})
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("source", "line", "occurrences", "classification"),
                                delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    assert rows and not [row for row in rows if row["classification"] == "STALE_CURRENT_POINTER"]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
