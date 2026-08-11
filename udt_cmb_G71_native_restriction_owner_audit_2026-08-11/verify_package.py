#!/usr/bin/env python3
"""Fail-closed verifier for the local G71 package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
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
    targets = table("OWNER_TARGET_LEDGER.tsv")
    atlas = table("SOURCE_TARGET_ATLAS.tsv")
    graph = table("DEPENDENCY_GRAPH.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=ROOT,
        check=True, capture_output=True, text=True
    ).stdout.splitlines()
    untracked = {line[3:] for line in status if line.startswith("?? ")}
    checks = {
        "source_manifest": len(source) == 21 and len({r["path"] for r in source}) == 21
            and all(digest(ROOT / r["path"]) == r["sha256"] for r in source),
        "target_census": len(targets) == 6 and len({r["target"] for r in targets}) == 6,
        "source_atlas": len(atlas) == 21 and {r["source_path"] for r in atlas} == {r["path"] for r in source},
        "dependency_graph": len(graph) == 16,
        "strict_landing": result["primary_landing"] == "GEOMETRIC_CARRY_OWNED__OBSERVABLE_AND_SELECTION_OWNERS_OPEN",
        "no_native_owner": result["owned_native_targets"] == 0
            and not any(r["status"] == "OWNED_NATIVE" for r in targets),
        "conditional_carry_only": result["derived_conditional_targets"] == 1
            and next(r for r in targets if r["target"] == "GEOMETRIC_CARRY_OWNER")["status"] == "DERIVED_CONDITIONAL_ON_QUERY",
        "exact_replay": result["exact_source_congruence_trials"] == 12,
        "independent": independent["status"] == "PASS" and independent["numeric_trials"] == 200
            and not independent["imports_production_builder"],
        "numeric_gates": independent["maximum_congruence_relative"] <= 2e-12
            and independent["maximum_shape_coordinate_shift_under_amplitude"] <= 2e-11
            and independent["minimum_constructed_source_eigenvalue"] > 0,
        "semantic_catches": catches["passed"] == catches["total"] == 13,
        "no_solve_or_anchor": result["new_ODE_solves"] == 0 and result["observational_anchors_used"] == 0,
        "scope": "not a universal\nno-go" in exact and "does not prove" in exact,
        "external_status": "INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING" in report,
        "protected": PROTECTED <= untracked,
    }
    return checks


def main() -> None:
    checks = verify()
    payload = {"schema": "udt-cmb-g71-package-v1", "checks": checks,
               "passed": sum(checks.values()), "total": len(checks)}
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    assert all(checks.values()), [key for key, value in checks.items() if not value]


if __name__ == "__main__":
    main()
