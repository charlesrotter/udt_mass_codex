#!/usr/bin/env python3
"""Fail-closed package verifier for G85."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script: str) -> dict[str, object]:
    process = subprocess.run(
        ["python3", str(HERE / script)], cwd=ROOT, text=True, capture_output=True, timeout=60, check=False,
    )
    assert process.returncode == 0, process.stdout + process.stderr
    return json.loads(process.stdout)


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 11
    assert all(sha(ROOT / row["path"]) == row["sha256"] for row in manifest)
    production = run("derive_completion_atlas.py")
    independent = run("verify_independent.py")
    catches = run("run_catch_proofs.py")
    atlas = table(HERE / "PROFILE_ARCHETYPE_ATLAS.tsv")
    channels = table(HERE / "SEAM_CHANNEL_ATLAS.tsv")
    premises = table(HERE / "PREMISE_LEDGER.tsv")
    falsification = table(HERE / "FALSIFICATION_CONTRACT.tsv")
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["mixed_profile_rows"] == 196
    assert len(atlas) == len(set((row["profile_id"], row["archetype_id"]) for row in atlas)) == 980
    assert len(channels) == 8 and len(premises) == 15 and len(falsification) == 14
    assert catches["catch_count"] == 10 and catches["all_hostile_mutations_rejected"] is True
    counts = Counter(row["classification"] for row in atlas)
    assert dict(sorted(counts.items())) == production["classification_counts"]
    assert independent["saved_artifacts"]["classification_counts"] == production["classification_counts"]
    assert production["landing"] in (HERE / "AUDIT_REPORT.md").read_text()
    assert production["maximum_conclusion"] in (HERE / "AUDIT_REPORT.md").read_text()
    prereg = subprocess.run(
        ["git", "show", "473cf4a1:udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/PREREGISTRATION.md"],
        cwd=ROOT, text=True, capture_output=True, timeout=30, check=False,
    )
    assert prereg.returncode == 0 and prereg.stdout.encode() == (HERE / "PREREGISTRATION.md").read_bytes()
    payload = {
        "schema": "udt-cmb-g85-package-verification-v1",
        "status": "PASS",
        "preregistration_commit": "473cf4a1",
        "preregistration_preserved": True,
        "source_manifest_rows": len(manifest),
        "profile_archetype_rows": len(atlas),
        "unique_profile_archetype_pairs": len(set((row["profile_id"], row["archetype_id"]) for row in atlas)),
        "classification_counts": dict(sorted(counts.items())),
        "seam_channel_rows": len(channels),
        "premise_rows": len(premises),
        "falsification_rows": len(falsification),
        "independent_verification": independent["status"],
        "catch_proofs": catches["catch_count"],
        "all_passed": True,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "PACKAGE_VERIFICATION.json").write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
