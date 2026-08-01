#!/usr/bin/env python3
"""Build the additions-only effective source inventory after cold-review discovery."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
ADDITIONS = [
    ("NEGATIVES_REGISTRY.md", "global negative-regrade registry"),
    ("udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md", "P4 census-domain relation"),
    ("udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", "P4 field-registration and fork status"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


def write_tsv(name: str, records: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    with (PKG / "SOURCE_INVENTORY.tsv").open(newline="", encoding="utf-8") as handle:
        original = list(csv.DictReader(handle, delimiter="\t"))
    if len(original) != 1605:
        raise RuntimeError("original source freeze changed")
    original_paths = {row["path"] for row in original}
    addendum = []
    for path, role in ADDITIONS:
        if path in original_paths:
            raise RuntimeError(f"source correction is not additions-only: {path}")
        full = ROOT / path
        if not full.is_file():
            raise RuntimeError(f"missing corrected source: {path}")
        addendum.append({
            "path": path,
            "git_blob": blob(path),
            "sha256": digest(full),
            "bytes": full.stat().st_size,
            "layer": "COLD_REVIEW_SOURCE_CORRECTION",
            "role": role,
        })
    addendum.sort(key=lambda row: str(row["path"]))
    write_tsv("SOURCE_ADDENDUM.tsv", addendum)
    combined = [dict(row, role="inherited frozen source") for row in original] + addendum
    combined.sort(key=lambda row: str(row["path"]))
    if len(combined) != 1608 or len({row["path"] for row in combined}) != 1608:
        raise RuntimeError("effective source correction census failed")
    write_tsv("EFFECTIVE_SOURCE_INVENTORY.tsv", combined)
    (PKG / "EFFECTIVE_SOURCE_MANIFEST.sha256").write_text(
        "\n".join(f"{row['sha256']}  ../{row['path']}" for row in combined) + "\n",
        encoding="utf-8",
    )
    print("PASS source correction build: original=1605 added=3 effective=1608")


if __name__ == "__main__":
    main()
