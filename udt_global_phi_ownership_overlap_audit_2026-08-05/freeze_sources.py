#!/usr/bin/env python3
"""Freeze source identities and unrelated untracked metadata without interpreting outcomes."""

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    paths = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    if len(paths) != len(set(paths)):
        raise SystemExit("duplicate source path")
    source_rows: list[dict[str, object]] = []
    for rel in paths:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"missing source: {rel}")
        source_rows.append(
            {
                "path": rel,
                "git_blob": git("hash-object", "--", rel),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "last_commit": git("log", "-1", "--format=%H", "--", rel),
            }
        )
    write_tsv(
        HERE / "SOURCE_MANIFEST.tsv",
        ["path", "git_blob", "sha256", "bytes", "last_commit"],
        source_rows,
    )

    prefix = f"{HERE.name}/"
    untracked_rows: list[dict[str, object]] = []
    for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines():
        if not line.startswith("?? "):
            continue
        rel = line[3:]
        if rel.startswith(prefix):
            continue
        stat = os.lstat(ROOT / rel)
        untracked_rows.append(
            {
                "path": rel,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "mode": oct(stat.st_mode),
                "inode": stat.st_ino,
            }
        )
    write_tsv(
        HERE / "UNRELATED_UNTRACKED_METADATA.tsv",
        ["path", "bytes", "mtime_ns", "mode", "inode"],
        untracked_rows,
    )

    frozen = {
        "candidate_universe_sha256": sha256(HERE / "CANDIDATE_UNIVERSE.tsv"),
        "falsification_contract_sha256": sha256(HERE / "FALSIFICATION_CONTRACT.tsv"),
        "premise_ledger_sha256": sha256(HERE / "PREMISE_LEDGER.tsv"),
        "preregistration_commit": git("rev-parse", "HEAD"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "source_count": len(source_rows),
        "source_adjudication_sha256": sha256(HERE / "SOURCE_ADJUDICATION.tsv"),
        "source_manifest_sha256": sha256(HERE / "SOURCE_MANIFEST.tsv"),
        "unrelated_untracked_count": len(untracked_rows),
        "unrelated_untracked_metadata_sha256": sha256(HERE / "UNRELATED_UNTRACKED_METADATA.tsv"),
    }
    (HERE / "FROZEN_UNIVERSE.json").write_text(json.dumps(frozen, indent=2, sort_keys=True) + "\n")
    print(json.dumps(frozen, sort_keys=True))


if __name__ == "__main__":
    main()
