#!/usr/bin/env python3
"""Freeze source identities and preregistration hashes without reading outcomes."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "3edcad2592e8e4053e88a1e7f646cb9d8a660871"
PREREG_FILES = [
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "PREMISE_LEDGER.tsv",
    "CANDIDATE_UNIVERSE.tsv",
    "OWNERSHIP_AXES.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "COMPLETENESS_MAP.md",
    "build_preregistration.py",
    "verify_preregistration.py",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> int:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    assert len(candidates) == 36
    assert len({row["candidate_id"] for row in candidates}) == 36
    rows = []
    for row in candidates:
        rel = row["frozen_source"]
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        rows.append(
            {
                "candidate_id": row["candidate_id"],
                "path": rel,
                "source_ref": f"{BASE}:{rel}",
                "git_blob": git("rev-parse", f"{BASE}:{rel}"),
                "sha256": sha(path),
                "size": path.stat().st_size,
            }
        )
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    snapshot = {
        "schema": "udt-native-reset-prereg-v1",
        "base": BASE,
        "candidate_count": 36,
        "axis_count": 8,
        "falsification_count": 15,
        "files": {name: sha(HERE / name) for name in PREREG_FILES},
        "source_manifest_sha256": sha(HERE / "SOURCE_MANIFEST.tsv"),
    }
    (HERE / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: froze 36 candidates, 8 axes, 15 falsification tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
