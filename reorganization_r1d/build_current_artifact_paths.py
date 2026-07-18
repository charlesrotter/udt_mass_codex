#!/usr/bin/env python3
"""Build the current-path overlay from the immutable R1C root inventory."""

from __future__ import annotations

import csv
from pathlib import Path

SOURCE = "simple_metric_S8_action_provenance_note.md"
DESTINATION = "research/macro/simple_metric_S8_action_provenance_note.md"


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    source = repo / "reorganization_r1c/FROZEN_ROOT_INVENTORY.tsv"
    destination = repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv"
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 1114
    output = []
    for row in rows:
        original = row["path"]
        current = DESTINATION if original == SOURCE else original
        status = "MIGRATED_R1D" if original == SOURCE else "ROOT_RETAINED"
        output.append({
            "original_path": original,
            "current_path": current,
            "path_status": status,
            "fixed_base_blob_oid": row["git_blob_oid"],
            "fixed_base_sha256": row["sha256"],
        })
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(output[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
