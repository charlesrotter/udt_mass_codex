#!/usr/bin/env python3
"""Freeze the preregistered source scope from the exact base commit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "4fa6de0d52b0be976cb39a5b91ab49cd33164c66"


def run_bytes(command: list[str]) -> bytes:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def main() -> int:
    with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
        scope = list(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in scope:
        path = row["path"]
        frozen = run_bytes(["git", "show", f"{BASE}:{path}"])
        blob = run_bytes(["git", "rev-parse", f"{BASE}:{path}"]).decode().strip()
        current = (ROOT / path).read_bytes()
        rows.append(
            {
                "path": path,
                "role": row["role"],
                "frozen_blob": blob,
                "frozen_sha256": hashlib.sha256(frozen).hexdigest(),
                "frozen_size": len(frozen),
                "current_at_freeze_sha256": hashlib.sha256(current).hexdigest(),
                "unchanged_at_freeze": "YES" if current == frozen else "NO",
            }
        )
    assert len(rows) == len({row["path"] for row in rows}) == 15
    assert all(row["unchanged_at_freeze"] == "YES" for row in rows)
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS source freeze: {len(rows)} paths at {BASE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

