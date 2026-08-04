#!/usr/bin/env python3
"""Build the tracked source manifest for the Phase-A skeleton audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True).strip()


paths = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
if len(paths) != len(set(paths)):
    raise SystemExit("duplicate source path")

rows = []
for relative in paths:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing source: {relative}")
    data = path.read_bytes()
    rows.append((relative, git_blob(relative), str(len(data)), hashlib.sha256(data).hexdigest()))

with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("path", "git_blob", "bytes", "sha256"))
    writer.writerows(rows)

print(f"wrote {len(rows)} tracked sources")
