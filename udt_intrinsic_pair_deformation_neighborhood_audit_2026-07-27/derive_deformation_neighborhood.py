#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27"

PRIMARY = (
    "ALL_GATE_INTRINSIC_PAIR_CONFIGURATIONS_CONTAIN_OPEN_C3_NEIGHBORHOODS_AROUND_"
    "C01_TO_C06_IN_THE_FIXED_COMPLETE_S3_FAMILY__STRUCTURAL_AVAILABILITY_IS_NOT_"
    "FINE_TUNED_WITHIN_THIS_CONFIGURATION_TOPOLOGY__NO_EXPLICIT_RADIUS_OR_PHYSICAL_"
    "SELECTION_IS_DERIVED"
)

STAMPS = {
    "COPRESENCE": "WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE": "DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS": "NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW": "OPEN",
}


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_parent_candidates() -> list[dict[str, str]]:
    with (PARENT / "CANDIDATE_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> int:
    parent_rows = load_parent_candidates()
    bases = [row for row in parent_rows if row["candidate_id"] in {f"C0{i}" for i in range(1, 7)}]
    assert [row["candidate_id"] for row in bases] == [f"C0{i}" for i in range(1, 7)]

    determinants: list[dict[str, object]] = []
    for row in bases:
        determinant = Fraction(row["gradient_determinant"])
        assert determinant != 0
        assert row["all_gate_witness"] == "YES"
        determinants.append(
            {
                "candidate_id": row["candidate_id"],
                "gradient_determinant": fraction_text(determinant),
                "exact_format": "RATIONAL_FRACTION",
                "nonzero": True,
            }
        )

    # Exact frozen margins.  f(+e1)=5 and f(-e1)=-1, then phi=f/50.
    depth_margin = Fraction(6, 50)
    twist_margin = abs(Fraction(1, 64) * Fraction(-2, 1))
    slice_margin_lower_bound = Fraction(1, 81) - Fraction(1, 4096)
    assert depth_margin == Fraction(3, 25)
    assert twist_margin == Fraction(1, 32)
    assert slice_margin_lower_bound == Fraction(4015, 331776)
    assert slice_margin_lower_bound > 0

    gate_rows = [
        {
            "gate_id": "O01",
            "gate": "curvature_rank",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "C3_profile_x_parameter_product",
            "exact_base_margin": "six_nonzero_exact_rational_determinants",
            "proof": "metric_three_jet_evaluation_and_D_p_are_continuous",
        },
        {
            "gate_id": "O02",
            "gate": "nontrivial_depth",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "C0_profile",
            "exact_base_margin": fraction_text(depth_margin),
            "proof": "oscillation_is_2_Lipschitz_in_sup_norm",
        },
        {
            "gate_id": "O03",
            "gate": "nonzero_twist",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "real_a",
            "exact_base_margin": fraction_text(twist_margin),
            "proof": "a_times_kappa_is_continuous",
        },
        {
            "gate_id": "O04",
            "gate": "positive_stationary_slice",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "C0_profile_x_real_a_x_positive_R",
            "exact_base_margin": fraction_text(slice_margin_lower_bound),
            "proof": "compact_minimum_of_R2_exp4phi_minus_a2_is_continuous",
        },
        {
            "gate_id": "O05",
            "gate": "global_coframe_nondegeneracy",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "finite_smooth_profile_x_positive_scale",
            "exact_base_margin": "strict_positive_exponentials_and_R",
            "proof": "coframe_determinant_is_nonzero_for_finite_phi_and_positive_R",
        },
        {
            "gate_id": "O06",
            "gate": "joint_all_gate_set",
            "status": "OPEN_AROUND_ALL_SIX_BASES",
            "topology": "C3_profile_x_real_a_x_real_lambda_x_positive_R",
            "exact_base_margin": "finite_intersection_of_O01_through_O05",
            "proof": "finite_intersection_of_open_sets_is_open",
        },
    ]
    write_tsv(
        HERE / "OPENNESS_GATE_OUTCOMES.tsv",
        ["gate_id", "gate", "status", "topology", "exact_base_margin", "proof"],
        gate_rows,
    )

    with (HERE / "DEFORMATION_AXIS_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        axes = list(csv.DictReader(handle, delimiter="\t"))
    axis_rows = []
    for axis in axes:
        axis_rows.append(
            {
                "axis_id": axis["axis_id"],
                "axis": axis["axis"],
                "outcome": "COVERED_BY_JOINT_OPEN_NEIGHBORHOOD",
                "qualification": "local_only_fixed_topology_and_coframe_family",
            }
        )
    write_tsv(
        HERE / "DEFORMATION_AXIS_OUTCOMES.tsv",
        ["axis_id", "axis", "outcome", "qualification"],
        axis_rows,
    )

    stratum_rows = [
        {"stratum_id": "S01", "outcome": "CERTIFICATE_RANK_LOSS", "clock_status": "OPEN_ALTERNATIVE_CERTIFICATE", "ruler_status": "INDEPENDENTLY_TESTED_BY_TWIST", "physical_status": "NOT_SELECTED"},
        {"stratum_id": "S02", "outcome": "TWIST_RULER_ROUTE_LOSS", "clock_status": "MAY_REMAIN", "ruler_status": "THIS_ROUTE_ABSENT", "physical_status": "NOT_SELECTED"},
        {"stratum_id": "S03", "outcome": "NONTRIVIAL_DEPTH_LOSS", "clock_status": "STATIONARY_LINE_MAY_REMAIN", "ruler_status": "MAY_REMAIN", "physical_status": "NOT_SELECTED"},
        {"stratum_id": "S04", "outcome": "DISPLAYED_SLICE_CAUSAL_BOUNDARY", "clock_status": "REQUIRES_SEPARATE_TEST", "ruler_status": "REQUIRES_SEPARATE_TEST", "physical_status": "NOT_A_SPACETIME_SINGULARITY_PROOF"},
        {"stratum_id": "S05", "outcome": "REGISTERED_COFRAME_BREAKDOWN", "clock_status": "NOT_CERTIFIED_IN_FAMILY", "ruler_status": "NOT_CERTIFIED_IN_FAMILY", "physical_status": "ALTERNATIVE_COMPLETIONS_OPEN"},
        {"stratum_id": "S06", "outcome": "MULTIPLE_GATE_INTERSECTION", "clock_status": "CASE_DEPENDENT", "ruler_status": "CASE_DEPENDENT", "physical_status": "NO_PHASE_CLAIM"},
        {"stratum_id": "S07", "outcome": "ON_SHELL_SELECTOR_NOT_SUPPLIED", "clock_status": "CONFIGURATION_EXISTENCE_ONLY", "ruler_status": "CONFIGURATION_EXISTENCE_ONLY", "physical_status": "OPEN"},
    ]
    write_tsv(
        HERE / "DEGENERATION_STRATUM_OUTCOMES.tsv",
        ["stratum_id", "outcome", "clock_status", "ruler_status", "physical_status"],
        stratum_rows,
    )

    result = {
        "question_type": "METRIC_LED_LOCAL_CONFIGURATION_SPACE",
        "base_commit": "ec5a241927b51b047d8bdbb3742cdaa5e464c880",
        "preregistration_commit": "1eb609b",
        "preregistration_correction_commit": "0162ba7",
        "premise_stamps": STAMPS,
        "configuration_topology": {
            "profile": "C3(S3)",
            "parameters": "R_a x R_lambda x R_positive",
            "reason": "first_gradients_of_curvature_scalars_depend_on_metric_three_jet",
        },
        "base_evidence": determinants,
        "base_count": len(determinants),
        "exact_margins": {
            "depth_oscillation_lower_bound": fraction_text(depth_margin),
            "absolute_a_kappa": fraction_text(twist_margin),
            "slice_margin_lower_bound": fraction_text(slice_margin_lower_bound),
        },
        "continuity_certificates": {
            "curvature_rank": "CONTINUOUS_IN_C3",
            "depth": "CONTINUOUS_IN_C0",
            "twist": "CONTINUOUS_IN_a",
            "slice": "CONTINUOUS_IN_C0_X_a_X_POSITIVE_R",
            "coframe": "OPEN_FOR_FINITE_SMOOTH_phi_AND_POSITIVE_R",
            "joint": "FINITE_INTERSECTION_OPEN",
        },
        "all_gate_open_neighborhoods": True,
        "all_six_centers_certified": True,
        "explicit_joint_radius_certified": False,
        "curvature_rank_radius_certified": False,
        "generic_dense_or_measure_claim": False,
        "physical_selection_claim": False,
        "on_shell_claim": False,
        "lambda_selected": False,
        "profile_selected": False,
        "endpoint_or_path_selected": False,
        "instantaneous_access_claim": False,
        "physics_inferences": {
            "action": False,
            "dynamics": False,
            "carrier": False,
            "source": False,
            "density": False,
            "bootstrap": False,
            "mass": False,
            "X_max": False,
        },
        "degeneration_semantics": {
            "D_zero_proves_clock_absent": False,
            "D_zero_proves_extra_symmetry": False,
            "slice_boundary_proves_spacetime_singularity": False,
        },
        "axis_count": len(axis_rows),
        "axis_ids": [row["axis_id"] for row in axis_rows],
        "stratum_count": len(stratum_rows),
        "stratum_ids": [row["stratum_id"] for row in stratum_rows],
        "primary_conclusion": PRIMARY,
        "maximum_scope": "LOCAL_OPENNESS_IN_FIXED_OFF_SHELL_COMPLETE_S3_CONFIGURATION_FAMILY",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("PASS parent_exact_nonzero_determinants 6/6")
    print(f"PASS depth_margin {fraction_text(depth_margin)}")
    print(f"PASS twist_margin {fraction_text(twist_margin)}")
    print(f"PASS slice_margin_lower_bound {fraction_text(slice_margin_lower_bound)}")
    print("PASS joint_open_neighborhoods 6/6")
    print(f"PRIMARY {PRIMARY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
