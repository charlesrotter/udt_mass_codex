#!/usr/bin/env python3
"""Verify the additions-only G73 external-review adjudication."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_HASH = "ad05bd3309336d81a42ad64063960b4fc621b2964300a6f650fe523edde2ea6c"
TRANSCRIPT_HASH = "74c4cbb96561fc553292366a6379348504ebf4ba65694fdba437fb0ee4702f21"
REVIEW_HASH = "08c2fbdaedeae3aef8cd2d17dcece729ede05d1476138d80742753bb66c316a0"
PROTECTED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate_scope(rows: list[dict[str, str]]) -> bool:
    keyed = {row["case"]: row for row in rows}
    return (
        len(rows) == len(keyed) == 5
        and keyed["WHOLE_S2_SELF_MAP"]["singularity_requirement"] == "REQUIRED_FOR_NONTRIVIAL_REPEATED_SELF_IMAGE"
        and keyed["DIFFERENT_TOPOLOGY"]["singularity_requirement"] == "NOT_UNIVERSALLY_REQUIRED"
        and keyed["PARTIAL_OR_NONCOMPACT_SKY"]["singularity_requirement"] == "NOT_UNIVERSALLY_REQUIRED"
        and keyed["BRANCH_LABELLED_RELATION"]["regular_multiplicity_status"] == "REGULAR_MULTIBRANCH_SET_POSSIBLE"
        and keyed["BRANCH_LABELLED_RELATION"]["udt_owner_status"] == "COMBINATION_RULE_OPEN_NO_OWNER"
        and keyed["STRONG_SHEAR_SINGLE_BRANCH"]["regular_multiplicity_status"] == "NO_REPEATED_IMAGE"
    )


def main() -> None:
    review = table(HERE / "REVIEW_MANIFEST.tsv")
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    scope = table(HERE / "TOPOLOGY_SCOPE_LEDGER.tsv")
    checks = {
        "review_manifest_hash": digest(HERE / "REVIEW_MANIFEST.tsv") == REVIEW_HASH,
        "reviewed_paths": len(review) == 32 and all(digest(ROOT / row["path"]) == row["sha256"] for row in review),
        "protected_excluded": not any(row["path"].startswith(PROTECTED) for row in review),
        "raw_hash": digest(HERE / "EXTERNAL_REVIEW_RAW.md") == RAW_HASH,
        "transcript_hash": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == TRANSCRIPT_HASH,
        "external_landing": raw.startswith("`VERIFIED_WITH_CAVEATS`")
        and "regular noninjective covers can still occur" in raw,
        "core_science_upheld": "exact source-recovery theorem is correct" in raw
        and "weakly anisotropic, not a strong kaleidoscope" in raw,
        "topology_scope": validate_scope(scope),
        "g68_unchanged": abs(result["g68_control"]["max_singular_value_ratio"] - 1.0046584288394136) < 2e-14,
        "physical_owners_open": result["status"]["physical_cmb_source_and_observable"] == "OPEN_NO_OWNER"
        and result["status"]["multibranch_observable_combination"] == "OPEN_NO_OWNER",
    }
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        check=True, capture_output=True, text=True
    ).stdout.splitlines()
    checks["protected_metadata"] = len([line for line in status if line.startswith("?? " + PROTECTED)]) == 7
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g73-external-adjudication-v1",
        "status": "PASS",
        "external_landing": "VERIFIED_WITH_CAVEATS",
        "effective_state": "EXTERNALLY_VERIFIED_WITH_TOPOLOGY_SCOPE_CAVEAT_CLOSED_LOCALLY",
        "reviewed_manifest_rows": len(review),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "protected_draft_read": False,
    }
    (HERE / "EXTERNAL_REVIEW_LIVE_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
