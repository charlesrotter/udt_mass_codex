#!/usr/bin/env python3
"""Freeze the preregistered source scope at the exact pre-audit base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "06858a8e4f9fedfe3921b8083748193f24f945de"


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace"))
    return result.stdout


def main() -> int:
    scope = []
    for name in ("SOURCE_SCOPE.tsv", "SOURCE_SCOPE_SUPPLEMENT.tsv"):
        with (HERE / name).open(newline="", encoding="utf-8") as handle:
            scope.extend(csv.DictReader(handle, delimiter="\t"))
    rows = []
    for row in scope:
        path = row["path"]
        frozen = git_bytes("show", f"{BASE}:{path}")
        current = (ROOT / path).read_bytes()
        rows.append({"path": path, "role": row["role"], "frozen_blob": git_bytes("rev-parse", f"{BASE}:{path}").decode().strip(), "frozen_sha256": hashlib.sha256(frozen).hexdigest(), "frozen_size": len(frozen), "current_sha256": hashlib.sha256(current).hexdigest(), "unchanged_at_freeze": "YES" if frozen == current else "NO"})
    assert len(rows) == len({row["path"] for row in rows}) == 22
    assert all(row["unchanged_at_freeze"] == "YES" for row in rows)
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"PASS source freeze: {len(rows)} paths at {BASE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
