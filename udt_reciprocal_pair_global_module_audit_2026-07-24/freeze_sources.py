#!/usr/bin/env python3
"""Freeze exact source identities for the reciprocal-pair module audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "a93f928f66d260bee1df1a9c5156269afa1952b7"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise SystemExit(result.stderr)
    return result.stdout.strip()


def main() -> None:
    if git("rev-parse", "HEAD") != BASE:
        raise SystemExit("source freeze must run at exact preregistration base")
    paths = [
        line.strip()
        for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(paths) != len(set(paths)):
        raise SystemExit("duplicate source path")
    rows = []
    for path in paths:
        full = ROOT / path
        if not full.is_file():
            raise SystemExit(f"missing source: {path}")
        data = full.read_bytes()
        rows.append(
            {
                "path": path,
                "blob": git("rev-parse", f"{BASE}:{path}"),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
                "base": BASE,
            }
        )
    with (HERE / "SOURCE_MANIFEST.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "blob", "sha256", "size", "base"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)
    digest = hashlib.sha256((HERE / "SOURCE_MANIFEST.tsv").read_bytes()).hexdigest()
    print({"sources": len(rows), "manifest_sha256": digest, "base": BASE})


if __name__ == "__main__":
    main()
