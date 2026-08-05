#!/usr/bin/env python3
"""Freeze generated regrade universes and unrelated dirt metadata before adjudication."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = "616c7bce"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unrelated_rows() -> list[dict[str, str]]:
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT
    )
    rows: list[dict[str, str]] = []
    for item in raw.split(b"\0"):
        if not item.startswith(b"?? "):
            continue
        relative = os.fsdecode(item[3:])
        if relative.startswith(HERE.name + "/"):
            continue
        stat = os.lstat(ROOT / relative)
        rows.append({
            "path": relative,
            "bytes": str(stat.st_size),
            "mtime_ns": str(stat.st_mtime_ns),
            "mode": oct(stat.st_mode),
            "inode": str(stat.st_ino),
        })
    return sorted(rows, key=lambda row: row["path"])


def main() -> None:
    rows = unrelated_rows()
    with (HERE / "UNRELATED_UNTRACKED_METADATA.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t", lineterminator="\n",
            fieldnames=["path", "bytes", "mtime_ns", "mode", "inode"],
        )
        writer.writeheader()
        writer.writerows(rows)
    summary = json.loads((HERE / "UNIVERSE_SUMMARY.json").read_text(encoding="utf-8"))
    frozen = {
        "schema": "udt.relational_phi_regrade.freeze.v1",
        "freeze_parent": PARENT,
        "base": summary["base"],
        "full_exposure_count": summary["full_exposure_count"],
        "active_regrade_count": summary["active_regrade_count"],
        "active_identity_sha256": summary["active_identity_sha256"],
        "unrelated_untracked_count": len(rows),
        "hashes": {
            name: digest(HERE / name) for name in [
                "PREREGISTRATION.md", "CLASSIFICATION_SCHEMA.tsv", "PREMISE_LEDGER.tsv",
                "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md", "build_candidate_universe.py",
                "FULL_EXPOSURE_CENSUS.tsv", "ACTIVE_REGRADE_UNIVERSE.tsv", "UNIVERSE_SUMMARY.json",
                "UNRELATED_UNTRACKED_METADATA.tsv",
            ]
        },
    }
    (HERE / "FROZEN_UNIVERSE.json").write_text(json.dumps(frozen, indent=2, sort_keys=True) + "\n")
    print(json.dumps(frozen, sort_keys=True))


if __name__ == "__main__":
    main()
