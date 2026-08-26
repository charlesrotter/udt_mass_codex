#!/usr/bin/env python3
"""Verify the complete bounded G261 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
LANDING = (
    "W4_OWNS_UNIVERSAL_METRIC_COUPLING__PRIMARY_METRIC_UNCHANGED__"
    "G259_CLASS_STILL_UNOWNED__ONE_DYNAMICS_GENERATOR_PREMISE_REMAINS"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = {
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "REPAIR_PREREGISTRATION.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "TRANSMISSION_RECORD.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "derive_w4_ownership.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "DERIVATION_RESULT.json",
        "OWNERSHIP_ATLAS.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
    }
    missing = sorted(name for name in required if not (PACKAGE / name).is_file())
    assert not missing, missing

    manifest_rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    assert len(manifest_rows) == 10
    for row in manifest_rows:
        source = REPO / row["path"]
        assert source.is_file(), row["path"]
        assert digest(source) == row["sha256"], row["path"]

    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == "PASS"
    assert production["landing"] == LANDING
    assert production["W4_status"] == "WORKING_POSIT_NOT_CANON"
    assert production["counts"] == {
        "DERIVED_FROM_W4": 1,
        "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY": 1,
        "NOT_DERIVED_FROM_W4": 7,
        "SUPPORTED_ACCEPTANCE_REQUIREMENT": 1,
    }
    assert production["classification_method"] == (
        "FROZEN_SOURCE_DRIVEN_RULES_PLUS_EXPLICIT_SEPARATORS"
    )
    assert production["source_gates"]["manifest_rows_verified"] == 10
    assert all(
        value is True
        for key, value in production["source_gates"].items()
        if key != "manifest_rows_verified"
    )
    assert production["metric_effect"]["F1_F4_implication_changed"] is False
    assert production["metric_effect"]["coefficient_changes"] == 0
    assert production["metric_effect"]["new_metric_components"] == 0
    assert production["metric_effect"]["primary_metric_form"] == "UNCHANGED"
    assert production["primary_metric_checks"]["arbitrary_positive_profile_event_cases"] == 257
    assert production["primary_metric_checks"]["exact_signature_and_determinant_assertions"] == 1285
    assert production["primary_metric_checks"]["determinant_depends_on_f_or_phi"] is False
    assert len(production["separating_witnesses"]) == 6
    assert all(witness["W4"] for witness in production["separating_witnesses"])
    assert all("separator" in witness["role"] for witness in production["separating_witnesses"])
    assert production["remaining_premise_type"] == (
        "NONIDENTITY_DYNAMICS_GENERATOR_SELECTING_A_PROPER_SUBSPACE_OF_COMPLETE_METRICS"
    )
    assert production["remaining_premise_scope"] == "BROAD_FAMILY_NOT_UNIQUE_SPECIFIC_MECHANISM"
    assert production["G259_specific_candidate_not_adopted"].startswith("NOT_ADOPTED__")
    assert production["observational_values_used"] == 0
    assert production["fit_coefficients"] == 0
    assert production["gpu_used"] is False
    assert production["protected_inputs_used"] == 0

    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert independent["status"] == "PASS"
    assert independent["verified_landing"] == LANDING
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert independent["ownership_items"] == 10
    assert independent["separator_count"] == 7
    assert independent["arbitrary_profile_jet_cases"] == 2000
    assert independent["assertions"] == 12041
    assert independent["epistemically_independent"] is False
    assert independent["external_adjudication_is_independence_gate"] is True
    assert independent["verification_scope"].endswith("NOT_LOGICALLY_OR_EPISTEMICALLY_INDEPENDENT")
    independent_code = (PACKAGE / "verify_independent.py").read_text(encoding="utf-8")
    assert "derive_w4_ownership" not in independent_code
    assert 'ROOT / "DERIVATION_RESULT.json"' not in independent_code

    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert catches["status"] == "PASS"
    assert catches["baseline_valid"] is True
    assert catches["mutation_count"] == 10
    assert catches["rejected_mutation_count"] == 10
    assert len(catches["rejected"]) == 10
    assert all(catches["rejected"].values())
    assert catches["evidence_scope"] == "ARTIFACT_GUARD_REGRESSION_NOT_SCIENTIFIC_PROOF"

    atlas = list(csv.DictReader((PACKAGE / "OWNERSHIP_ATLAS.tsv").open(encoding="utf-8"), delimiter="\t"))
    assert len(atlas) == 10
    assert sum(row["classification"] == "DERIVED_FROM_W4" for row in atlas) == 1
    assert sum(
        row["classification"] == "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY"
        for row in atlas
    ) == 1
    assert sum(row["classification"] == "SUPPORTED_ACCEPTANCE_REQUIREMENT" for row in atlas) == 1
    assert sum(row["classification"] == "NOT_DERIVED_FROM_W4" for row in atlas) == 7

    result = {
        "status": "PASS",
        "grade": "EXTERNAL_ACCEPT_WITH_REPAIRS__REPAIRS_IMPLEMENTED__FOLLOWUP_REQUIRED",
        "landing": LANDING,
        "source_manifest_rows": len(manifest_rows),
        "production_exact_assertions": 1285,
        "structural_crosscheck_assertions": independent["assertions"],
        "rejected_artifact_mutations": catches["rejected_mutation_count"],
        "external_fresh_verdict": "ACCEPT_WITH_REPAIRS",
        "observations_fits_gpu_protected_inputs": 0,
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
