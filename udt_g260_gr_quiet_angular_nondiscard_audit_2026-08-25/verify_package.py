#!/usr/bin/env python3
"""Verify the bounded G260 evidence package and source hashes."""

from __future__ import annotations

import csv
import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = "FULL_METRIC_CANCELLATION_WITH_ACTIVE_ANGULAR_SECTOR"
PRODUCTION_RESULT_SHA256 = "ddc9b6f0ef357cf433d171472e51d49ca7c87352d5464ec4cf2d3349aa429248"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = (
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "CONTROL_ATLAS.tsv",
        "SOURCE_MANIFEST.tsv",
        "REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "TRANSMISSION_RECORD.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_CERTIFICATION.json",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "derive_angular_nondiscard.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
    )
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert not missing, missing

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    repair = json.loads((ROOT / "REPAIR_CERTIFICATION.json").read_text())
    assert production["status"] == "PASS" and production["landing"] == LANDING
    assert all(production["checks"].values())
    assert production["angular_interlock"]["identity"] == "A_parallel+A_perp=E1-E0"
    assert production["vacuum_family"]["full_Ricci"] == "0"
    assert production["vacuum_family"]["A_parallel"] == "3*C/(2*r)"
    assert production["vacuum_family"]["A_perp"] == "-3*C/(2*r)"
    assert production["balanced_angular_trace_family"]["general_local_f"] == "1+a*r^2+b/r"
    assert production["corruption_controls"]["isolated_2d_Einstein_identically_zero"] is True
    assert production["corruption_controls"]["flat_k0_on_spherical_vacuum_family"] == "1"
    assert independent["status"] == "PASS"
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert independent["assertions"] == 10044
    assert independent["arbitrary_metric_jet_cases"] == 700
    assert independent["vacuum_family_cases"] == 446
    assert independent["balanced_trace_cases"] == 267
    assert catches["status"] == "PASS" and catches["caught_count"] == 8
    assert all(catches["caught"].values())
    assert digest(ROOT / "DERIVATION_RESULT.json") == PRODUCTION_RESULT_SHA256

    production_source = (ROOT / "derive_angular_nondiscard.py").read_text()
    production_tree = ast.parse(production_source)
    imported_roots = set()
    for node in ast.walk(production_tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
    assert imported_roots <= {"__future__", "json", "fractions", "pathlib"}
    assert "sympy" not in production_source.lower()
    assert "verify_independent" not in production_source
    assert ".read_text(" not in production_source
    assert repair["status"] == "PASS"
    assert repair["bounded_scientific_landing_changed"] is False
    assert repair["dependency_free_production"]["standard_library_only"] is True
    assert repair["dependency_free_production"]["result_sha256"] == PRODUCTION_RESULT_SHA256
    assert repair["independent_assertions"] == 10044
    assert repair["hostile_catches"] == 8
    assert repair["full_repository_tests"]["collected"] == 164
    assert repair["full_repository_tests"]["expected_xfail"] == 1
    assert repair["external_repair_followup"] == "ACCEPT_REPAIR"

    audit = (ROOT / "AUDIT_REPORT.md").read_text()
    exact = (ROOT / "EXACT_DERIVATION.md").read_text()
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text()
    external = (ROOT / "EXTERNAL_REVIEW_GPT54.md").read_text()
    external_followup = (ROOT / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md").read_text()
    repair_prereg = (ROOT / "REPAIR_PREREGISTRATION.md").read_text()
    assert "EXTERNALLY_VERIFIED_WITH_CAVEATS__R1_ACCEPTED" in audit
    assert "Vacuum Einstein remains an imported W3 comparator" in audit
    assert "does not derive the Einstein equation" in exact
    assert "vacuum_Einstein_residual\tIMPORTED_COMPARISON_ONLY" in ledger
    assert "screen_k0\tHOSTILE_CORRUPTION_CONTROL" in ledger
    assert "Disposition: `ACCEPT_WITH_REPAIRS`" in external
    assert "Disposition: `ACCEPT_REPAIR`" in external_followup
    assert "Exact remaining repair: none" in external_followup
    assert "R1 — dependency-free production replay" in repair_prereg

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 11
    for source in sources:
        path = REPO / source["path"]
        assert path.is_file(), source["path"]
        assert digest(path) == source["sha256"], source["path"]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "grade": "EXTERNALLY_VERIFIED_WITH_CAVEATS__R1_ACCEPTED",
        "source_hashes": len(sources),
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["caught_count"],
        "external_review": "ACCEPT_WITH_REPAIRS__R1_ACCEPTED",
        "repair": "R1_dependency_free_production_replay",
        "repair_status": "EXTERNALLY_ACCEPTED",
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(
        "PASS: G260 package, "
        f"{len(sources)} source hashes, {independent['assertions']} independent assertions, "
        f"{catches['caught_count']} hostile catches; R1 externally accepted"
    )


if __name__ == "__main__":
    main()
