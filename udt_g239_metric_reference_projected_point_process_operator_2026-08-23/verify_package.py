#!/usr/bin/env python3
"""Package and semantic verifier for G239."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from derive_reference_operator import LANDING, compute
from run_catch_proofs import validate
from verify_sealed_premise_scope import compute as compute_sealed_premise_scope


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}
    required = (
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "OPERATOR_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REVIEW_REQUEST.md",
        "SEALED_PREMISE_SCOPE_RESULT.json",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "TRANSMISSION_RECORD.md",
        "derive_reference_operator.py",
        "build_review_intake.py",
        "run_catch_proofs.py",
        "verify_reference_operator_independent.py",
        "verify_sealed_premise_scope.py",
    )
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"missing files: {missing}")
    checks["required_files"] = True

    manifest = rows(ROOT / "SOURCE_MANIFEST.tsv")
    if len(manifest) != 12:
        raise AssertionError("source manifest count changed")
    for row in manifest:
        source = REPO / row["path"]
        if not source.is_file() or sha256(source) != row["sha256"]:
            raise AssertionError(f"source hash mismatch: {row['source_id']}")
    checks["twelve_source_hashes"] = True

    saved = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    fresh = compute()
    if saved != fresh:
        raise AssertionError("saved derivation differs from fresh computation")
    validate(saved)
    if saved["landing"] != LANDING:
        raise AssertionError("landing changed")
    checks["saved_equals_fresh"] = True
    checks["outcomes_closed"] = saved["boss_outcomes_opened"] is False
    checks["exact_cancellations"] = (
        saved["cancellation_controls"]["constant_response_landy_szalay"]["exact"] == "0/1"
        and saved["cancellation_controls"]["matched_reference_landy_szalay"]["exact"] == "0/1"
    )
    checks["nonzero_survival_witness"] = saved["factorized_witness"]["landy_szalay"]["exact"] == "-1/6"
    checks["metric_local_liveness"] = (
        saved["metric_local_jacobi_liveness"]["jacobi_determinant_lambda4_coefficient"]["exact"]
        == "-2/25"
    )
    checks["connected_decomposition"] = saved["connected_control"]["decomposition_exact"] is True
    checks["single_image_factorization_scope"] = (
        saved["branch_factorization"]["assumption"]
        == "ONE_OBSERVED_IMAGE_PER_SOURCE_EVENT__INDEPENDENT_SINGLE_BRANCH_MARK"
        and saved["branch_factorization"]["no_same_source_sibling_multiplicity"] is True
    )
    checks["same_source_sibling_gamma"] = (
        saved["sibling_image_control"]["factorization_false"] is True
        and saved["sibling_image_control"]["normalized_gamma_nonzero"] is True
        and saved["sibling_image_control"]["normalized_gamma"][0][1]["exact"] == "1/12"
    )

    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    if independent["status"] != "PASS" or independent["identity_cases"] < 1900:
        raise AssertionError("independent replay insufficient")
    if independent["g127_jacobi_determinant_lambda4_coefficient"] != "-2/25":
        raise AssertionError("independent metric witness changed")
    if independent["sibling_image_cases"] != 257:
        raise AssertionError("independent sibling-image coverage changed")
    if independent["branch_factorization_scope"] != "ONE_OBSERVED_IMAGE_PER_SOURCE_EVENT":
        raise AssertionError("independent factorization scope broadened")
    checks["independent_exact_replay"] = True

    sealed_premise_saved = json.loads((ROOT / "SEALED_PREMISE_SCOPE_RESULT.json").read_text())
    sealed_premise_fresh = compute_sealed_premise_scope()
    if sealed_premise_saved != sealed_premise_fresh:
        raise AssertionError("saved sealed premise audit differs from fresh computation")
    if sealed_premise_saved["status"] != "PASS" or sealed_premise_saved["registry_rows"] != 221:
        raise AssertionError("sealed premise audit failed")
    if set(sealed_premise_saved["dependencies_checked"]) != {
        "G126", "G127", "G188", "G221", "G226", "G238"
    }:
        raise AssertionError("sealed premise dependency set changed")
    checks["sealed_premise_scope_replay"] = True

    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    if catches["status"] != "PASS" or len(catches["cases"]) != 12:
        raise AssertionError("catch proof coverage changed")
    if not all(case["caught"] for case in catches["cases"]):
        raise AssertionError("hostile mutation escaped")
    if not any(case["mutation"] == "same_source_sibling_suppression" for case in catches["cases"]):
        raise AssertionError("sibling suppression catch absent")
    checks["twelve_hostile_mutations"] = True

    operator = rows(ROOT / "OPERATOR_LEDGER.tsv")
    status = rows(ROOT / "STATUS_LEDGER.tsv")
    if len(operator) != 17 or len(status) != 17:
        raise AssertionError("ledger cardinality changed")
    if not any(row["stage"] == "O16" and row["status"] == "OPEN" for row in operator):
        raise AssertionError("physical input gap hidden")
    if not any(
        row["stage"] == "O05" and row["status"] == "DERIVED_EXACT_CONTROL"
        for row in operator
    ):
        raise AssertionError("same-source sibling operator row absent")
    if not any(row["item"] == "BOSS_outcomes" and row["status"] == "CLOSED_NO_INSPECTION" for row in status):
        raise AssertionError("outcome gate absent")
    checks["typed_ledgers"] = True

    prereg = (ROOT / "PREREGISTRATION.md").read_text()
    exact_text = (ROOT / "EXACT_DERIVATION.md").read_text()
    for token in (
        "PREREGISTERED_BEFORE_OPERATOR_DERIVATION__BOSS_OUTCOMES_CLOSED",
        "CHOSE_OBSERVATIONAL_HYPOTHESIS",
        "No BOSS outcome",
        "exactly one observed image",
        "same-source image multiplicity",
    ):
        if token not in prereg + exact_text:
            raise AssertionError(f"scope token absent: {token}")
    checks["scope_and_provenance"] = True

    followup = (ROOT / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text()
    if "G239_R1_R2_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_RETAINED" not in followup:
        raise AssertionError("external repair-followup acceptance absent")
    checks["external_repair_followup_accepted"] = True

    result = {
        "audit": "G239_PACKAGE_VERIFICATION",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
