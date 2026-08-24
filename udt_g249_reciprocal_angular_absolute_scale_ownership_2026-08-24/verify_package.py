#!/usr/bin/env python3
"""No-write verifier for the bounded G249 evidence package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
LANDING = (
    "CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH"
    "__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED"
    "__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE"
    "__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY"
    "__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE"
)
HOSTILE_MUTATION_KEYS = frozenset({
    "area_squared_shape_normalization_rejected",
    "caustic_position_inverse_rejected",
    "clock_ratio_ell_mutation_rejected",
    "clock_ratio_invariance_control",
    "coarea_invariance_mutation_rejected",
    "coarea_inverse_square_control",
    "correct_scaled_ode_is_zero_control",
    "invariant_area_scaling_rejected",
    "inverse_anchor_recovery_mutation_rejected",
    "ivp_cubic_coefficient_control",
    "ivp_cubic_coefficient_mutation_rejected",
    "jacobi_exponent_two_breaks_vertex_derivative",
    "jacobi_exponent_zero_breaks_vertex_derivative",
    "linear_anchor_recovery_mutation_rejected",
    "linear_area_scaling_rejected",
    "noninjective_phi_single_area_mutation_rejected",
    "positive_square_root_anchor_control",
    "quadratic_area_scaling_control",
    "same_phi_forced_angular_equality_rejected",
    "signed_determinant_o2_scalar_rejected",
    "tidal_exponent_minus_one_breaks_ode",
    "tidal_exponent_minus_three_breaks_ode",
    "unit_determinant_shape_invariance_control",
})


def hostile_ledger_valid(result: dict) -> bool:
    mutations = result.get("mutations", {})
    return (
        result.get("implementation") == "formula_level_mutation_tests_no_phrase_matching"
        and result.get("total") == 23
        and result.get("caught") == 23
        and result.get("missed") == []
        and frozenset(mutations) == HOSTILE_MUTATION_KEYS
        and len(mutations) == 23
        and all(mutations.values())
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def matches_frozen_source(path: Path, expected: str, relative: str) -> bool:
    """Permit the append-only G249 registry row after integration."""
    if sha256(path) == expected:
        return True
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return False
    lines = path.read_bytes().splitlines(keepends=True)
    rows = [index for index, line in enumerate(lines) if line.startswith(b"G249\t")]
    if len(rows) != 1 or not lines or not lines[0].startswith(b"premise_id\t"):
        return False
    historical = lines[0] + b"".join(lines[rows[0] + 1 :])
    return hashlib.sha256(historical).hexdigest() == expected


def replay(script: str, *arguments: str) -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(PKG / script), *arguments],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    required = [
        "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_COMMIT.md",
        "SOURCE_MANIFEST.tsv", "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "COMMANDS.md", "REVIEW_REQUEST.md",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_RAW.md", "TRANSMISSION_RECORD.md",
        "REPAIR_PREREGISTRATION.md", "REPAIR_PREREGISTRATION_COMMIT.md", "REPAIR_RESULT.md",
        "REPAIR_FOLLOWUP_REQUEST.md", "REPAIR_FOLLOWUP.md", "REPAIR_FOLLOWUP_RAW.md",
        "REPAIR_FOLLOWUP_TRANSMISSION_RECORD.md", "SECOND_REPAIR_PREREGISTRATION.md",
        "SECOND_REPAIR_PREREGISTRATION_COMMIT.md", "SECOND_REPAIR_RESULT.md",
        "SECOND_REPAIR_FOLLOWUP_REQUEST.md",
        "derive_reciprocal_angular_scale.py", "verify_reciprocal_angular_scale_independent.py",
        "run_catch_proofs.py", "verify_package.py", "build_review_intake.py",
    ]
    missing = [name for name in required if not (PKG / name).is_file()]
    if missing:
        raise SystemExit(f"missing package files: {missing}")

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        if not source.is_file() or not matches_frozen_source(source, row["sha256"], row["path"]):
            raise SystemExit(f"source freeze mismatch: {row['path']}")

    saved_production = json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    saved_independent = json.loads(
        (PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    saved_catches = json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    live_production = replay("derive_reciprocal_angular_scale.py", "--cases", "4096")
    live_independent = replay(
        "verify_reciprocal_angular_scale_independent.py", "--cases", "10000"
    )
    live_catches = replay("run_catch_proofs.py")
    deleted_ledger = dict(saved_catches)
    deleted_mutations = dict(saved_catches.get("mutations", {}))
    deleted_mutations.pop("same_phi_forced_angular_equality_rejected")
    deleted_ledger["mutations"] = deleted_mutations
    deleted_ledger["total"] = 22
    deleted_ledger["caught"] = 22
    renamed_ledger = dict(saved_catches)
    renamed_mutations = dict(saved_catches.get("mutations", {}))
    renamed_mutations["same_phi_forced_response_equality_rejected"] = renamed_mutations.pop(
        "same_phi_forced_angular_equality_rejected"
    )
    renamed_ledger["mutations"] = renamed_mutations

    checks = {
        "source_manifest_rows": len(rows) == 9,
        "saved_production_pass": saved_production.get("status") == "PASS",
        "saved_independent_pass": saved_independent.get("status") == "PASS",
        "saved_catch_pass": saved_catches.get("status") == "PASS",
        "production_landing": saved_production.get("landing") == LANDING,
        "independent_landing": saved_independent.get("expected_landing") == LANDING,
        "production_replay_exact": live_production == saved_production,
        "independent_replay_exact": live_independent == saved_independent,
        "catch_replay_exact": live_catches == saved_catches,
        "production_floor": saved_production.get("cases", 0) >= 4096
        and saved_production.get("assertions", 0) >= 60000,
        "independent_floor": saved_independent.get("cases", 0) >= 10000
        and saved_independent.get("assertions", 0) >= 240000,
        "offdiagonal_floor": saved_production.get("offdiagonal_cases", 0) >= 3000
        and saved_independent.get("offdiagonal_cases", 0) >= 8000,
        "nonunit_scale_floor": saved_production.get("nonunit_scale_cases", 0) >= 3500
        and saved_independent.get("nonunit_scale_area_changes", 0) >= 9000,
        "hostile_exact_ledger": hostile_ledger_valid(saved_catches),
        "hostile_deleted_entry_rejected": not hostile_ledger_valid(deleted_ledger),
        "hostile_renamed_entry_rejected": not hostile_ledger_valid(renamed_ledger),
        "claim_directed_independent": saved_independent.get("implementation")
        == "claim_directed_standard_library_fraction_no_sympy_no_production_import_or_output_read"
        and all(saved_independent.get("claim_checks", {}).values())
        and len(saved_independent.get("claim_checks", {})) == 6,
        "homothety_claim_floor": saved_independent.get("homothety_scaling_cases", 0) >= 10000,
        "same_phi_claim_floor": saved_independent.get("same_phi_jet_cases", 0) >= 10000,
        "same_phi_two_witness_contract": saved_independent.get("same_phi_witness")
        == "two_explicit_phi_zero_witnesses_with_distinct_jets_and_angular_outputs",
        "noninjective_claim_floor": saved_independent.get("noninjective_branch_cases", 0) >= 10000,
        "ivp_uniqueness_claim_floor": saved_independent.get("ivp_uniqueness_cases", 0) >= 512
        and saved_independent.get("ivp_series_degree", 0) >= 16,
        "anchor_claim_floor": saved_independent.get("anchor_recovery_cases", 0) >= 10000,
        "formula_level_mutations": hostile_ledger_valid(saved_catches),
        "outcomes_closed": saved_production.get("observational_outcomes") == "CLOSED_AND_UNREAD"
        and saved_independent.get("observational_outcomes") == "CLOSED_AND_UNREAD",
        "zero_fitted_coefficients": saved_production.get("fitted_coefficients") == 0,
        "external_scientific_acceptance": "G249_ACCEPTED_AFTER_SPECIFIED_REPAIRS"
        in (PKG / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8"),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {"checks": checks, "failed": failed, "status": "PASS" if not failed else "FAIL"}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
