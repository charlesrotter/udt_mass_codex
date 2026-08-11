#!/usr/bin/env python3
"""Fail-closed verification of the additions-only G75 external-review layer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> None:
    expected = {
        "REVIEW_MANIFEST.tsv": "917ddad22fd5885e0d8a1e52305c88dacbffb2fb35316fef6636c19c2c0bee71",
        "EXTERNAL_REVIEW_RAW.md": "d4b0a0a8529b08930d180eee010edd9060bd43e0d72460cf82d29b482d14dde8",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt": "506245bd94ecdd5e23f11bfc9600413167203eb0381011e9d8a3dbdb8c4a9e21",
        "SHAPE_ATLAS.tsv": "28350686758d735635e963bea7ebc0435ff335b929db6116dfd3ef44b1bcd912",
        "PROFILE_ATLAS.tsv": "c45f96312b7a89dcd8797a0ccac8c8506e69bd454bfb119acf34c43149af57c7",
    }
    checks = {f"hash_{name}": digest(HERE / name) == value for name, value in expected.items()}

    fixed = subprocess.run(
        ["python3", str(HERE / "verify_hash_manifest.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    checks["fixed_23_file_package_unchanged"] = fixed.returncode == 0 and "PASS: 23" in fixed.stdout

    corrected_replay = load_json("CORRECTED_INDEPENDENT_VERIFICATION_RESULT.json")
    corrected_catches = load_json("CORRECTED_CATCH_PROOF_RESULTS.json")
    review = load_json("EXTERNAL_REVIEW_RESULT.json")
    checks.update({
        "corrected_replay_16_of_16": corrected_replay["status"] == "PASS" and corrected_replay["passed"] == corrected_replay["total"] == 16,
        "corrected_catches_16_of_16": corrected_catches["status"] == "PASS" and corrected_catches["passed"] == corrected_catches["total"] == 16,
        "external_landing": review["external_landing"] == "VERIFIED_WITH_CAVEATS",
        "external_zero_shape_mismatches": review["shape_row_mismatches"] == 0,
        "external_zero_profile_mismatches": review["profile_row_mismatches"] == 0,
        "external_counts": review["shape_count"] == 49 and review["profile_count"] == 591,
        "protected_draft_unread": review["protected_draft_read"] is False,
        "adjudication_status_present": "EXTERNALLY_VERIFIED_BOUNDED_FAMILY" in (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8"),
    })

    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(newline="", encoding="utf-8") as stream:
        rows = {row["premise_id"]: row for row in csv.DictReader(stream, delimiter="\t")}
    checks["current_G75_overlay"] = (
        rows["G75"]["current_status"].startswith("EXTERNALLY_VERIFIED_BOUNDED_FAMILY")
        and rows["G75"]["controlling_source"].endswith("EXTERNAL_REVIEW_ADJUDICATION.md")
    )

    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g75-external-review-verification-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "fixed_package_hashes": 23,
        "protected_draft_read": False,
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
