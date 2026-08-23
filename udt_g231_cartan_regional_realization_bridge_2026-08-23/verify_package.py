#!/usr/bin/env python3
"""Aggregate G231 verifier with optional full exact production replay."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import hostile_mutation_tests as hostile
import derive_cartan_regional_bridge as production


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREREG_COMMIT = "a5cd16a9"


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def verify_hash_table(name: str, base: Path, order: str) -> bool:
    for line in (ROOT / name).read_text(encoding="utf-8").splitlines()[1:]:
        first, second = line.split("\t")
        path, digest = (first, second) if order == "path_hash" else (second, first)
        candidate = base / path
        if candidate.is_file() and hashlib.sha256(candidate.read_bytes()).hexdigest() == digest:
            continue
        if name != "SOURCE_MANIFEST.tsv":
            return False
        frozen = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{path}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        if hashlib.sha256(frozen).hexdigest() != digest:
            return False
    return True


def run_json(script: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), "--no-write"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="rerun exact production")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    exact = load("exact_results.json")
    independent_saved = load("independent_results.json")
    hostile_saved = load("hostile_results.json")
    independent_live = run_json("verify_cartan_bridge_independent.py")
    hostile_live = hostile.derive()
    report_text = " ".join((ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    next_text = " ".join((ROOT / "NEXT_GATE.md").read_text(encoding="utf-8").split())
    theorem_text = " ".join((ROOT / "THEOREM_SCOPE_AUDIT.md").read_text(encoding="utf-8").split())

    expected_ranks = {
        "algebraic_bianchi": 16,
        "differential_bianchi": 20,
        "differentiated_bianchi": 80,
        "commutator": 120,
        "combined_second_prolongation": 194,
    }
    checks: dict[str, bool] = {
        "preregistration_hashes_match": verify_hash_table(
            "PREREGISTRATION_HASHES.tsv", ROOT, "path_hash"
        ),
        "source_manifest_hashes_match": verify_hash_table(
            "SOURCE_MANIFEST.tsv", REPO, "hash_path"
        ),
        "production_saved_checks": exact["all_checks_pass"] is True
        and all(exact["checks"].values()),
        "production_saved_ranks": exact["ranks"] == expected_ranks,
        "production_saved_dimensions": exact["dimensions"]
        == {
            "cartan_curvature_source": 36,
            "algebraic_curvature_kernel": 20,
            "first_curvature_derivative": 80,
            "first_derivative_compatible": 60,
            "ordered_second_curvature_derivative": 320,
            "second_derivative_affine_translation": 126,
        },
        "production_input_trilemma": exact["input_trilemma"]
        == {
            "moving_frame_R_without_carry": "INCOMPLETE",
            "R_relative_to_supplied_coframe": "EVALUATIVE_ALREADY_HAS_METRIC",
            "R_plus_compatible_classifying_derivative_law": "TYPED_CARTAN_REALIZATION_PROBLEM",
        },
        "production_non_space_form_and_constant_controls": exact["nonlinear_witness"][
            "first_nonzero"
        ]
        == "-1"
        and exact["nonlinear_witness"]["commutator_rhs_nonzero_count"] > 0
        and exact["constant_curvature_control"]["commutator_rhs_nonzero_count"] == 0
        and all(
            count == 0
            for count in exact["constant_curvature_control"]["closure_residual_counts"].values()
        ),
        "production_vertical_action_nontrivial": all(
            count > 0
            for count in exact["vertical_frame_control"]["nonzero_counts_by_Lorentz_generator"]
        ),
        "independent_no_write_matches_saved": independent_live == independent_saved,
        "independent_checks_pass": independent_saved["all_checks_pass"] is True
        and all(independent_saved["checks"].values()),
        "independent_direct_metric_sign_anchor": independent_saved[
            "direct_polynomial_metric_sign_anchor"
        ]
        == {
            "correct_sign_residual_nonzero_count": 0,
            "differentiated_Bianchi_residual_nonzero_count": 0,
            "reversed_sign_residual_nonzero_count": 2,
        },
        "independent_vertical_action_anchor": all(
            independent_saved["independent_vertical_action"][field] is True
            for field in (
                "basis_kernel_preserved",
                "constant_annihilated",
                "explicit_transform_matches",
            )
        )
        and all(independent_saved["independent_vertical_action"]["eta_skew_generators"])
        and all(
            count > 0
            for count in independent_saved["independent_vertical_action"][
                "witness_nonzero_counts"
            ]
        ),
        "hostile_no_write_matches_saved": hostile_live == hostile_saved,
        "hostile_17_of_17": hostile_saved["all_caught"] is True
        and len(hostile_saved["catches"]) == 17
        and all(hostile_saved["catches"].values()),
        "theorem_scope_ceiling_present": all(
            phrase in report_text
            for phrase in (
                "does not supply curvature values",
                "does not claim generic smooth or global existence",
                "does not choose the curvature profile",
            )
        ),
        "next_gate_does_not_revert_to_jet_census": "Do not return to a mechanical fifth-derivative census"
        in next_text,
        "standard_theorem_hypotheses_are_explicit": all(
            phrase in theorem_text
            for phrase in (
                "fully regular",
                "analytic relative Lie algebroid",
                "both analytic regularity and formal integrability are hypotheses",
                "conditional local G-realization",
                "effective orbifold",
                "principal `SO(1,3)` descent",
            )
        ),
        "live_claim_scope_accepts_only_preregistered_ceiling": production.validate_claim_scope(
            production.BASELINE_SCOPE
        )
        and all(
            not production.validate_claim_scope(
                {**production.BASELINE_SCOPE, field: promoted}
            )
            for field, promoted in (
                ("curvature_values", "DERIVED"),
                ("classifying_law", "SELECTED"),
                ("generic_smooth", "DERIVED"),
                ("global", "DERIVED"),
                ("physical_history", "DERIVED"),
            )
        ),
        "saved_theorem_boundary_is_typed": exact["theorem_boundary"]
        == {
            "finite_type_classifying_data": "CONDITIONAL_LOCAL_G_REALIZATION_IF_FULL_SO13_G_STRUCTURE_ALGEBROID_HYPOTHESES_HOLD",
            "infinite_type_PDE_data": "ANALYTIC_LOCAL_COFRAME_REALIZATION_ONLY__PRINCIPAL_SO13_EQUIVARIANCE_AND_DESCENT_OPEN",
            "generic_smooth_local": "NOT_CLAIMED",
            "global_realization": "NOT_CLAIMED",
            "value_generation_or_history_selection": "NOT_DERIVED",
        },
    }

    if args.full:
        checks["full_production_no_write_matches_saved"] = production.derive() == exact

    result = {
        "landing": "G231_PACKAGE_VERIFIED",
        "preregistration_commit": PREREG_COMMIT,
        "full_production_replayed": args.full,
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_pass": all(checks.values()),
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "verification_results.json").write_text(text + "\n", encoding="utf-8")
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
