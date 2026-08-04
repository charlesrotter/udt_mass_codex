#!/usr/bin/env python3
"""Build the frozen tracked-source manifest for the preregistered audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parent


def git_blob(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
    ).strip()


paths = [line.strip() for line in (AUDIT / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
if paths != sorted(set(paths), key=paths.index) or len(paths) != len(set(paths)):
    raise SystemExit("SOURCE_PATHS.txt contains a duplicate")

rows = []
for rel in paths:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"missing source: {rel}")
    data = path.read_bytes()
    rows.append((rel, git_blob(rel), str(len(data)), hashlib.sha256(data).hexdigest()))

with (AUDIT / "SOURCE_MANIFEST.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("path", "git_blob", "bytes", "sha256"))
    writer.writerows(rows)

print(f"wrote {len(rows)} tracked source rows")
