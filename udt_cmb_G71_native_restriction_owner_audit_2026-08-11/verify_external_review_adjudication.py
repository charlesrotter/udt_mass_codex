#!/usr/bin/env python3
"""Verify the additions-only G71 external-review adjudication layer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATUS_COLUMNS = (
    "source_shape", "source_normalization", "physical_endpoint",
    "physical_profile", "geometric_carry", "observable_carry",
)
RAW_HASH = "222f43b1348a33acd6db775f212dcc54e06d557c89ab0aa5c3a120154ed2065f"
TRANSCRIPT_HASH = "0e4672ecceb2a562b58ba09772307add30bd8431856c90033cac1bcbcb4650b1"
REVIEW_MANIFEST_HASH = "451d472956183346a145f2c2c2c2213b48194a4665556dcff97c14afa95b6e6b"
PROTECTED_PREFIX = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate_overlay(original: list[dict[str, str]], overlay: list[dict[str, str]]) -> bool:
    if len(original) != len(overlay) or len(overlay) != 21:
        return False
    if len({row["source_path"] for row in overlay}) != 21:
        return False
    for old, new in zip(original, overlay):
        if old["source_role"] != new["source_role"] or old["source_path"] != new["source_path"]:
            return False
        if any(old[column] != new[column] for column in STATUS_COLUMNS):
            return False
        try:
            line_number = int(new["line_number"])
            lines = (ROOT / new["source_path"]).read_text(encoding="utf-8", errors="replace").splitlines()
            if line_number < 1 or line_number > len(lines):
                return False
            if new["literal_token"] not in lines[line_number - 1]:
                return False
        except (ValueError, OSError):
            return False
    return True


def main() -> None:
    review = table(HERE / "REVIEW_MANIFEST.tsv")
    original = table(HERE / "SOURCE_TARGET_ATLAS.tsv")
    overlay = table(HERE / "SOURCE_TARGET_LITERAL_CITATION_OVERLAY.tsv")
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    checks = {
        "review_manifest_hash": digest(HERE / "REVIEW_MANIFEST.tsv") == REVIEW_MANIFEST_HASH,
        "reviewed_paths": len(review) == 44 and all(digest(ROOT / row["path"]) == row["sha256"] for row in review),
        "protected_excluded": not any(row["path"].startswith(PROTECTED_PREFIX) for row in review),
        "raw_hash": digest(HERE / "EXTERNAL_REVIEW_RAW.md") == RAW_HASH,
        "transcript_hash": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == TRANSCRIPT_HASH,
        "external_landing": raw.startswith("`VERIFIED_WITH_CAVEATS`") and "not mechanically self-citing" in raw,
        "overlay": validate_overlay(original, overlay),
        "science_unchanged": "Six-target census" in raw and "GEOMETRIC_CARRY_OWNER DERIVED_CONDITIONAL_ON_QUERY" in raw,
    }
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        check=True, capture_output=True, text=True
    ).stdout.splitlines()
    protected = [line for line in status if line.startswith("?? " + PROTECTED_PREFIX)]
    checks["protected_metadata"] = len(protected) == 7
    payload = {
        "schema": "udt-cmb-g71-external-adjudication-v1",
        "external_landing": "VERIFIED_WITH_CAVEATS",
        "effective_scientific_landing": "GEOMETRIC_CARRY_OWNED__OBSERVABLE_AND_SELECTION_OWNERS_OPEN",
        "reviewed_manifest_rows": len(review),
        "literal_overlay_rows": len(overlay),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
    }
    (HERE / "EXTERNAL_REVIEW_LIVE_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    assert all(checks.values()), [name for name, value in checks.items() if not value]


if __name__ == "__main__":
    main()
