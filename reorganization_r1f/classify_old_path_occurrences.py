#!/usr/bin/env python3
"""Classify retained old-basename occurrences after the B01 move."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CURRENT_NAV = {
    "README.md", "research/README.md", "research/_registry/README.md",
    "research/_registry/CURRENT_ARTIFACT_PATHS.tsv", "research/macro/ROOT_INVENTORY.tsv",
}


def tracked_and_new() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=REPO,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return sorted(set(result.stdout.splitlines()))


def classify(source: str, line: str, old: str, destination: str) -> str:
    if source == "research/_registry/CURRENT_ARTIFACT_PATHS.tsv":
        expected = f"{old}\t{destination}\tMIGRATED_R1F\t"
        return "CURRENT_MAP_ORIGINAL_IDENTITY_AND_DESTINATION_SUFFIX" if line.startswith(expected) else "STALE_CURRENT_POINTER"
    if source == "research/macro/ROOT_INVENTORY.tsv":
        return "CURRENT_DESTINATION_SUFFIX" if line.startswith(destination + "\t") else "STALE_CURRENT_POINTER"
    if source in CURRENT_NAV:
        return "CURRENT_DESTINATION_SUFFIX" if destination in line else "STALE_CURRENT_POINTER"
    if source.startswith(tuple(f"reorganization_r1{x}/" for x in ("0", "a", "b", "c", "d", "e"))):
        return "FIXED_HISTORICAL_OR_R1E_PLAN"
    if source.startswith("reorganization_r1f/"):
        return "R1F_PREMOVE_OR_MIGRATION_PROVENANCE"
    return "RETAINED_INFORMATIONAL_REFERENCE"


def main() -> int:
    with (REPO / "reorganization_r1f/PREREGISTERED_BATCH.tsv").open(encoding="utf-8", newline="") as handle:
        batch = list(csv.DictReader(handle, delimiter="\t"))
    files = tracked_and_new()
    records = []
    for item in batch:
        old, destination = item["current_path"], item["destination"]
        for source in files:
            if source == "reorganization_r1f/OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv":
                continue
            path = REPO / source
            if not path.is_file():
                continue
            payload = path.read_bytes()
            if b"\0" in payload:
                continue
            try:
                text = payload.decode("utf-8")
            except UnicodeDecodeError:
                continue
            for line_number, line in enumerate(text.splitlines(), 1):
                start = 0
                while True:
                    column = line.find(old, start)
                    if column < 0:
                        break
                    records.append({
                        "old_path": old, "current_path": destination, "source": source,
                        "line": line_number, "column": column + 1,
                        "classification": classify(source, line, old, destination),
                        "source_sha256": hashlib.sha256(payload).hexdigest(),
                    })
                    start = column + len(old)
    records.sort(key=lambda row: (row["old_path"], row["source"], int(row["line"]), int(row["column"])))
    fields = ["old_path", "current_path", "source", "line", "column", "classification", "source_sha256"]
    with (REPO / "reorganization_r1f/OLD_PATH_OCCURRENCE_CLASSIFICATION.tsv").open(
            "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    stale = [row for row in records if row["classification"] == "STALE_CURRENT_POINTER"]
    if stale:
        raise AssertionError(f"stale current navigation occurrences: {stale[:3]}")
    print(f"occurrences={len(records)} stale=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
