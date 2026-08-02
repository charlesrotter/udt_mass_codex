#!/usr/bin/env python3
"""Freeze the cold review source universe before launching the reviewer."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        scope = list(csv.DictReader(handle, delimiter="\t"))
    assert len(scope) == len({row["path"] for row in scope}) == 20
    rows = []
    for row in scope:
        path = ROOT / row["path"]
        assert path.is_file()
        blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, check=True,
            text=True, capture_output=True,
        ).stdout.strip()
        rows.append({
            "path": row["path"], "role": row["role"], "git_blob": blob,
            "sha256": digest(path), "bytes": path.stat().st_size,
        })
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t",
            fieldnames=["path", "role", "git_blob", "sha256", "bytes"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"sources={len(rows)}")
    print(f"manifest_sha256={digest(HERE / 'SOURCE_MANIFEST.tsv')}")


if __name__ == "__main__":
    main()
