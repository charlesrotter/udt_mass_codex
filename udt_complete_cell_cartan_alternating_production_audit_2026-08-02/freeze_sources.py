#!/usr/bin/env python3
"""Freeze the preregistered load-bearing source universe deterministically."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCOPE = HERE / "SOURCE_SCOPE.tsv"
OUTPUT = HERE / "SOURCE_MANIFEST.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob(relative: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main() -> None:
    with SCOPE.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    paths = [row["path"] for row in rows]
    assert len(paths) == len(set(paths)), "duplicate source path"

    frozen = []
    for row in rows:
        relative = row["path"]
        path = ROOT / relative
        assert path.is_file(), f"missing source: {relative}"
        frozen.append(
            {
                "path": relative,
                "role": row["role"],
                "git_blob": git_blob(relative),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "role", "git_blob", "sha256", "bytes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(frozen)

    print(f"frozen_sources={len(frozen)}")
    print(f"manifest_sha256={sha256(OUTPUT)}")


if __name__ == "__main__":
    main()
