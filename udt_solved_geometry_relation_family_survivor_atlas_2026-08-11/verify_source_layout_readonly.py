#!/usr/bin/env python3
"""Read-only source replay from a frozen Git snapshot or sealed sources/ layout."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02"
STOPPED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10"


with (HERE / "SOURCE_MANIFEST.tsv").open() as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
assert len(rows) == len({r['path'] for r in rows}) == 22

commit = (HERE / "SOURCE_BASE_COMMIT.txt").read_text().strip()
assert len(commit) == 40 and all(c in "0123456789abcdef" for c in commit)


def git_bytes(path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, check=False
    )
    return result.stdout if result.returncode == 0 else None


git_payloads = {r["path"]: git_bytes(r["path"]) for r in rows}
sealed = ROOT / "sources"
counts = {
    "REPOSITORY_GIT_SNAPSHOT": sum(v is not None for v in git_payloads.values()),
    "SEALED_SOURCES": sum((sealed / r["path"]).is_file() for r in rows),
}
complete = [name for name, count in counts.items() if count == 22]
assert len(complete) == 1, counts
assert all(count in (0, 22) for count in counts.values()), counts
chosen = complete[0]
for row in rows:
    payload = (
        git_payloads[row["path"]]
        if chosen == "REPOSITORY_GIT_SNAPSHOT"
        else (sealed / row["path"]).read_bytes()
    )
    assert payload is not None
    assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["path"]
    assert PROTECTED not in row["path"] and STOPPED not in row["path"]
print(json.dumps({"status":"PASS","layout":chosen,"sources":22,"layout_counts":counts}, indent=2, sort_keys=True))
