#!/usr/bin/env python3
"""Package and semantic verifier for G239."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from derive_reference_operator import LANDING, compute
from run_catch_proofs import validate


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
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "OPERATOR_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REVIEW_REQUEST.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "derive_reference_operator.py",
        "build_review_intake.py",
        "run_catch_proofs.py",
        "verify_reference_operator_independent.py",
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

    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    if independent["status"] != "PASS" or independent["identity_cases"] < 1900:
        raise AssertionError("independent replay insufficient")
    if independent["g127_jacobi_determinant_lambda4_coefficient"] != "-2/25":
        raise AssertionError("independent metric witness changed")
    checks["independent_exact_replay"] = True

    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    if catches["status"] != "PASS" or len(catches["cases"]) != 11:
        raise AssertionError("catch proof coverage changed")
    if not all(case["caught"] for case in catches["cases"]):
        raise AssertionError("hostile mutation escaped")
    checks["eleven_hostile_mutations"] = True

    operator = rows(ROOT / "OPERATOR_LEDGER.tsv")
    status = rows(ROOT / "STATUS_LEDGER.tsv")
    if len(operator) != 16 or len(status) != 16:
        raise AssertionError("ledger cardinality changed")
    if not any(row["stage"] == "O15" and row["status"] == "OPEN" for row in operator):
        raise AssertionError("physical input gap hidden")
    if not any(row["item"] == "BOSS_outcomes" and row["status"] == "CLOSED_NO_INSPECTION" for row in status):
        raise AssertionError("outcome gate absent")
    checks["typed_ledgers"] = True

    prereg = (ROOT / "PREREGISTRATION.md").read_text()
    exact_text = (ROOT / "EXACT_DERIVATION.md").read_text()
    for token in (
        "PREREGISTERED_BEFORE_OPERATOR_DERIVATION__BOSS_OUTCOMES_CLOSED",
        "CHOSE_OBSERVATIONAL_HYPOTHESIS",
        "No BOSS outcome",
    ):
        if token not in prereg + exact_text:
            raise AssertionError(f"scope token absent: {token}")
    checks["scope_and_provenance"] = True

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
