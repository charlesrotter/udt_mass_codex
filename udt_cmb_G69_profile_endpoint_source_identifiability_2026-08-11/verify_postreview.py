#!/usr/bin/env python3
"""Fail-closed verifier for the additions-only G69 external-review layer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REVIEW_MANIFEST_SHA = "c7fd475ec49d672375b0908fba5829a4521f59c85e28fb74ea0533bf3554b20e"
RAW_SHA = "9bce4184e8e25029eb37ba4a8c726964c7d435a4ad980096443d00d444e59596"
TRANSCRIPT_SHA = "c3d8687a20680dd50f5769f682eb1cb9ee2a21bdb3b52d37b618ba1857d7ffc5"
PROTECTED = {
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/CANDIDATE_LAW_MAP.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/DERIVATION_RESULT.json",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/EQUATION_OWNERSHIP_ATLAS.tsv",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/SOURCE_SCOPE_CLARIFICATION.md",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/derive_owner_atlas.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/run_catch_proofs.py",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/verify_owner_independent.py",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with (HERE / "REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        reviewed = list(csv.DictReader(stream, delimiter="\t"))
    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    historical_report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    navigation = [
        ROOT / "LIVE.md",
        ROOT / "HANDOFF.md",
        ROOT / "README.md",
        ROOT / "INDEX.md",
        ROOT / "CURRENT_RESEARCH_PROGRAM.md",
        ROOT / "CURRENT_SCIENTIFIC_PREMISES.md",
        ROOT / "MEMORY.md",
        ROOT / "INFLIGHT_STATE.md",
        ROOT / "research/README.md",
        ROOT / "research/_registry/README.md",
    ]
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    untracked = {line[3:] for line in status if line.startswith("?? ")}
    checks = {
        "review_manifest_sha": digest(HERE / "REVIEW_MANIFEST.tsv") == REVIEW_MANIFEST_SHA,
        "review_manifest_rows": len(reviewed) == 37,
        "reviewed_files_unchanged": all(digest(ROOT / row["path"]) == row["sha256"] for row in reviewed),
        "raw_sha": digest(HERE / "EXTERNAL_REVIEW_RAW.md") == RAW_SHA,
        "transcript_sha": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == TRANSCRIPT_SHA,
        "external_landing": raw.lstrip().startswith("VERIFIED_AS_BOUNDED"),
        "no_external_correction": "Exact correction: none." in raw,
        "historical_pending_preserved": "INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING" in historical_report,
        "effective_status": "EXTERNALLY_VERIFIED_AS_BOUNDED" in adjudication,
        "scope_guard": "not a full-CMB no-go" in adjudication and "selects\nno physical model" in adjudication,
        "independence_guard": "not independent geodesic or Jacobi path integration" in adjudication,
        "navigation_updated": all("EXTERNALLY_VERIFIED_AS_BOUNDED" in path.read_text(encoding="utf-8") for path in navigation),
        "protected_paths_present": PROTECTED <= untracked,
    }
    payload = {
        "schema": "udt-cmb-g69-postreview-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "review_manifest_rows": len(reviewed),
        "protected_untracked_paths": len(PROTECTED & untracked),
    }
    (HERE / "POSTREVIEW_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    assert all(checks.values()), [key for key, value in checks.items() if not value]


if __name__ == "__main__":
    main()
