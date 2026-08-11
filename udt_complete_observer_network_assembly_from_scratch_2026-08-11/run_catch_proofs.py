#!/usr/bin/env python3
"""Fail-closed semantic and algebraic catches for G62."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    next_step = (HERE / "NEXT_STEP.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    with (HERE / "OWNER_CLASSIFICATION.tsv").open(newline="", encoding="utf-8") as stream:
        owners = {row["owner_id"]: row for row in csv.DictReader(stream, delimiter="\t")}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))

    catches = {
        "F01_exact_network_algebra_complete": result["exact_check_count"] == 35,
        "F02_independent_implementation_complete": independent["total_exact_trials"] == 1500,
        "F03_associativity_not_descent": "coherence is not the same as\nflatness" in exact,
        "F04_nonzero_holonomy_retained": (
            "angular_triangle_holonomy_nontrivial" in result["exact_checks"]
            and result["exact_checks"]["angular_triangle_holonomy_nontrivial"]
            and owners["O04"]["history_restriction_status"] == "HOLONOMY_ALLOWED"
        ),
        "F05_four_face_identity_not_equation_or_novelty": (
            owners["O11"]["history_restriction_status"] == "IDENTITY_NOT_DYNAMICS"
            and "not a new\ncompatibility theorem" in exact
        ),
        "F06_cE_is_terminal_not_everywhere_equal": (
            "would set every `z_ij=1` and trivialize" in exact
            and "does not set every endpoint readout equal" in report
        ),
        "F07_shift_and_mixing_retained": "beta=-4/9" in exact and "L^2=112/27" in exact,
        "F08_time_live_arbitrary": (
            result["exact_checks"]["complete_frame_time_derivative_of_descent"]
            and independent["complete_time_live_frame_trials"] == 300
        ),
        "F09_flatness_is_conditional": (
            owners["O10"]["history_restriction_status"] == "CONDITIONAL_NONIDENTITY_FLAT_DESCENT"
            and "not currently owned universally" in report
        ),
        "F10_global_causality_remains_open": (
            owners["O09"]["current_ownership"] == "OPEN_POSSIBLE_FILTER"
            and "finite graph\ncannot manufacture" in exact
        ),
        "F11_scalar_additivity_not_arbitrary_distance": (
            "does not assert that scalar distances add" in exact
        ),
        "F12_relation_family_and_route_policy_are_next_not_formula": (
            "physical **calibrated relation family**" in next_step
            and "Route policy cannot be selected before the relation family is typed" in next_step
            and "Do not search for a generic global equation" in next_step
        ),
        "F13_no_bootstrap_or_downstream_promotion": (
            "Bootstrap, density, energy, curvature targets" in prereg
            and "No action, source, carrier, matter, mass, bootstrap rule" in report
        ),
        "F14_source_scope_exact_and_protected_absent": (
            len(sources) == 15
            and not any(
                "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in row["path"]
                or "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in row["path"]
                for row in sources
            )
        ),
        "F15_lay_machine_not_pile_but_not_score": (
            "pieces are not lying loose" in lay and "still does not dictate" in lay
        ),
        "F16_primary_landing_exact": (
            result["status"] == "ASSEMBLY_IDENTITIES_ONLY_WITH_ROUTE_DEPENDENCE_OPEN"
            and "Primary landing: `ASSEMBLY_IDENTITIES_ONLY_WITH_ROUTE_DEPENDENCE_OPEN`" in report
        ),
        "F17_continuum_flatness_hypotheses_explicit": (
            "chosen smooth local connection" in report
            and "contractible\nneighborhood" in report
            and "sufficiently small based contractible loop" in report
        ),
        "F18_external_grade_not_novelty": (
            "Fresh sealed-source grade: `VERIFIED_WITH_CORRECTIONS`" in report
        ),
    }
    failed = sorted(key for key, value in catches.items() if not value)
    output = {
        "schema_version": 1,
        "catch_count": len(catches),
        "caught_count": len(catches) - len(failed),
        "failed": failed,
        "catches": catches,
    }
    if not args.read_only:
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(output, indent=2, sort_keys=True))
    assert not failed, failed


if __name__ == "__main__":
    main()
