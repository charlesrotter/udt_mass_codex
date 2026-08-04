#!/usr/bin/env python3
"""Freeze the preregistered source set without importing project code."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    paths = [line.strip() for line in (PKG / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    rows = []
    for rel in paths:
        path = ROOT / rel
        if not path.is_file():
            raise SystemExit(f"missing preregistered source: {rel}")
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", rel],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if tracked.returncode:
            raise SystemExit(f"untracked preregistered source: {rel}")
        blob = subprocess.check_output(["git", "hash-object", "--", rel], cwd=ROOT, text=True).strip()
        rows.append((rel, blob, sha256(path), path.stat().st_size))

    with (PKG / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "git_blob", "sha256", "size"))
        writer.writerows(rows)
    manifest_hash = sha256(PKG / "SOURCE_MANIFEST.tsv")
    (PKG / "SOURCE_MANIFEST.sha256").write_text(
        f"{manifest_hash}  SOURCE_MANIFEST.tsv\n", encoding="utf-8"
    )
    print(f"sources={len(rows)}")
    print(f"manifest_sha256={manifest_hash}")


if __name__ == "__main__":
    main()
