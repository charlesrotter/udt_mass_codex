#!/usr/bin/env python3
"""Freeze the exact preregistered source set before semantic adjudication."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SCOPE = PACKAGE / "SOURCE_SCOPE.tsv"
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"
DIGEST = PACKAGE / "SOURCE_MANIFEST.sha256"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with SCOPE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    records = []
    for row in rows:
        rel = row["path"]
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"missing preregistered source: {rel}")
        records.append(
            {
                "path": rel,
                "role": row["role"],
                "git_blob": git("hash-object", "--", rel),
                "sha256": sha256(path),
                "bytes": str(path.stat().st_size),
                "last_commit": git("log", "-1", "--format=%H", "--", rel),
            }
        )

    fieldnames = ["path", "role", "git_blob", "sha256", "bytes", "last_commit"]
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    manifest_digest = sha256(MANIFEST)
    DIGEST.write_text(f"{manifest_digest}  SOURCE_MANIFEST.tsv\n", encoding="utf-8")
    print(f"SOURCE_COUNT={len(records)}")
    print(f"SOURCE_BYTES={sum(int(row['bytes']) for row in records)}")
    print(f"SOURCE_MANIFEST_SHA256={manifest_digest}")


if __name__ == "__main__":
    main()
