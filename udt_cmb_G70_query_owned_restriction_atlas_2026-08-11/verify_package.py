#!/usr/bin/env python3
"""Fail-closed verifier for the local G70 package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
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


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify() -> dict[str, bool]:
    source = table("SOURCE_MANIFEST.tsv")
    atlas = table("RESTRICTION_RANK_ATLAS.tsv")
    summary = table("MODEL_SUMMARY.tsv")
    owners = table("OWNERSHIP_LEDGER.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all"],
                            cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    untracked = {line[3:] for line in status if line.startswith("?? ")}
    counts = Counter(row["classification"] for row in atlas)
    r05 = [row for row in atlas if row["model_id"] == "R05_KNOWN_SOURCE_PLUS_CARRY"]
    checks = {
        "source_manifest": len(source) == 9 and all(digest(ROOT / row["path"]) == row["sha256"] for row in source),
        "atlas_census": len(atlas) == 285 and len({(r["model_id"], r["variant"], r["shape"], r["endpoint_x"]) for r in atlas}) == 285,
        "summary_census": len(summary) == 19,
        "ownership_census": len(owners) == 20,
        "rank_counts": counts == Counter({"RANK_DEFICIENT_OBSERVED": 224, "FULL_RANK_OBSERVED": 46,
                                           "RANK_NUMERICALLY_UNRESOLVED": 15}),
        "strict_landing": result["primary_landing"] == "IDENTIFIABILITY_NUMERICALLY_UNRESOLVED",
        "R05_subresult": len(r05) == 45 and all(row["classification"] == "FULL_RANK_OBSERVED" for row in r05),
        "independent": independent["status"] == "PASS" and independent["atlas_rows"] == 285 and not independent["imports_production_builder"],
        "matrix_replay": independent["maximum_matrix_relative"] <= 2e-10 and independent["maximum_logm_expm_reconstruction_relative"] <= 2e-12,
        "no_solve_or_anchor": result["new_ODE_solves"] == 0 and result["observational_anchors_used"] == 0,
        "no_owned_restriction": result["current_query_owned_identifiability_restrictions"] == 0,
        "scope": "not a physical CMB solution" in report and "cannot claim a unique" in exact,
        "external_status": "INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING" in report,
        "catches": catches["passed"] == catches["total"] == 14,
        "protected": PROTECTED <= untracked,
    }
    return checks


def main() -> None:
    checks = verify()
    payload = {"schema": "udt-cmb-g70-package-v1", "checks": checks,
               "passed": sum(checks.values()), "total": len(checks)}
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    assert all(checks.values()), [key for key, value in checks.items() if not value]


if __name__ == "__main__":
    main()
