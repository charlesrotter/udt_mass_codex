#!/usr/bin/env python3
"""Freeze the preregistered source universe and unrelated dirt metadata."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def write_tsv(path: Path, names: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_paths = [
        line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(source_paths) != 31 or len(source_paths) != len(set(source_paths)):
        raise SystemExit("source universe must contain exactly 31 unique paths")
    source_rows: list[dict[str, object]] = []
    for relative in source_paths:
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"missing source: {relative}")
        source_rows.append(
            {
                "path": relative,
                "git_blob": git("hash-object", "--", relative),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
                "last_commit": git("log", "-1", "--format=%H", "--", relative),
            }
        )
    write_tsv(
        HERE / "SOURCE_MANIFEST.tsv",
        ["path", "git_blob", "sha256", "bytes", "last_commit"],
        source_rows,
    )

    prefix = HERE.name + "/"
    dirt_rows: list[dict[str, object]] = []
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=ROOT
    )
    for item in raw.split(b"\0"):
        if not item.startswith(b"?? "):
            continue
        relative = os.fsdecode(item[3:])
        if relative.startswith(prefix):
            continue
        stat = os.lstat(ROOT / relative)
        dirt_rows.append(
            {
                "path": relative,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "mode": oct(stat.st_mode),
                "inode": stat.st_ino,
            }
        )
    dirt_rows.sort(key=lambda row: str(row["path"]))
    if len(dirt_rows) != 83:
        raise SystemExit(f"expected 83 unrelated untracked paths, found {len(dirt_rows)}")
    write_tsv(
        HERE / "UNRELATED_UNTRACKED_METADATA.tsv",
        ["path", "bytes", "mtime_ns", "mode", "inode"],
        dirt_rows,
    )

    frozen = {
        "schema": "udt.founding_phi_ownership.frozen_universe.v1",
        "preregistration_commit": git("rev-parse", "HEAD"),
        "source_count": len(source_rows),
        "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
        "candidate_universe_sha256": digest(HERE / "CANDIDATE_UNIVERSE.tsv"),
        "premise_ledger_sha256": digest(HERE / "PREMISE_LEDGER.tsv"),
        "falsification_contract_sha256": digest(HERE / "FALSIFICATION_CONTRACT.tsv"),
        "unrelated_untracked_count": len(dirt_rows),
        "unrelated_untracked_metadata_sha256": digest(HERE / "UNRELATED_UNTRACKED_METADATA.tsv"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }
    (HERE / "FROZEN_UNIVERSE.json").write_text(
        json.dumps(frozen, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(frozen, sort_keys=True))


if __name__ == "__main__":
    main()
