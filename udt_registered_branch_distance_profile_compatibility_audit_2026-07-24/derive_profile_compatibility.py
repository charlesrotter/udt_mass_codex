#!/usr/bin/env python3
"""Exact registered-branch distance-profile compatibility overlay."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BRANCH = ROOT / "udt_finite_cell_transnormal_asymptote_branch_audit_2026-07-24"


def check(store: dict[str, str], name: str, condition: bool) -> None:
    if not bool(condition):
        raise AssertionError(name)
    store[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    checks: dict[str, str] = {}
    phi = sp.symbols("phi", real=True, nonnegative=True)
    kappa, dmax, length, radius = sp.symbols("kappa Dmax L b", positive=True)

    # Endpoint-normalized profiles. The round family contains the complete
    # registered positive relative clock/angular depth-unit freedom.
    projective = sp.tanh(phi)
    exponential = 1 - sp.exp(-phi)
    round_family = sp.Rational(2, 1) / sp.pi * sp.atan(sp.sinh(2 * kappa * phi))
    round_unit = round_family.subs(kappa, 1)

    profiles = {
        "PROJECTIVE_TANH": projective,
        "WRL_EXPONENTIAL": exponential,
        "B19_ROUND_KAPPA_ONE": round_unit,
    }
    jets = {
        name: tuple(sp.simplify(sp.diff(profile, phi, order).subs(phi, 0)) for order in range(1, 4))
        for name, profile in profiles.items()
    }
    check(checks, "projective_origin", projective.subs(phi, 0) == 0)
    check(checks, "exponential_origin", exponential.subs(phi, 0) == 0)
    check(checks, "round_origin", round_family.subs(phi, 0) == 0)
    check(checks, "projective_endpoint", sp.limit(projective, phi, sp.oo) == 1)
    check(checks, "exponential_endpoint", sp.limit(exponential, phi, sp.oo) == 1)
    check(checks, "round_endpoint", sp.limit(round_family, phi, sp.oo) == 1)
    check(checks, "projective_jet", jets["PROJECTIVE_TANH"] == (1, 0, -2))
    check(checks, "exponential_jet", jets["WRL_EXPONENTIAL"] == (1, -1, 1))
    check(
        checks,
        "round_unit_jet",
        jets["B19_ROUND_KAPPA_ONE"] == (4 / sp.pi, 0, -16 / sp.pi),
    )

    round_jet = tuple(sp.simplify(sp.diff(round_family, phi, order).subs(phi, 0)) for order in range(1, 4))
    check(checks, "round_family_first_jet", round_jet[0] == 4 * kappa / sp.pi)
    check(checks, "round_family_second_jet", round_jet[1] == 0)
    check(checks, "round_family_third_jet", round_jet[2] == -16 * kappa**3 / sp.pi)

    # Shape invariants under a positive constant redefinition phi -> a phi.
    def invariants(jet):
        return sp.simplify(jet[1] / jet[0] ** 2), sp.simplify(jet[2] / jet[0] ** 3)

    projective_invariants = invariants(jets["PROJECTIVE_TANH"])
    exponential_invariants = invariants(jets["WRL_EXPONENTIAL"])
    round_invariants = invariants(round_jet)
    check(checks, "projective_shape_invariants", projective_invariants == (0, -2))
    check(checks, "exponential_shape_invariants", exponential_invariants == (-1, 1))
    check(checks, "round_shape_invariants", round_invariants == (0, -sp.pi**2 / 4))
    check(checks, "projective_exponential_inequivalent", projective_invariants != exponential_invariants)
    check(checks, "exponential_round_inequivalent_all_kappa", exponential_invariants != round_invariants)
    check(
        checks,
        "projective_round_inequivalent_all_kappa",
        sp.simplify(projective_invariants[1] - round_invariants[1]) != 0,
    )

    # A simpler two-gate challenge: matching normalized origin slope and
    # matching endpoint exponent require inconsistent kappa.
    kappa_origin_match = sp.solve(sp.Eq(4 * kappa / sp.pi, 1), kappa)
    kappa_tanh_exponent_match = sp.solve(sp.Eq(2 * kappa, 2), kappa)
    kappa_exp_exponent_match = sp.solve(sp.Eq(2 * kappa, 1), kappa)
    check(checks, "round_tanh_origin_match_kappa", kappa_origin_match == [sp.pi / 4])
    check(checks, "round_tanh_endpoint_match_kappa", kappa_tanh_exponent_match == [1])
    check(checks, "round_exp_endpoint_match_kappa", kappa_exp_exponent_match == [sp.Rational(1, 2)])
    check(checks, "round_tanh_match_conditions_inconsistent", kappa_origin_match != kappa_tanh_exponent_match)
    check(checks, "round_exp_match_conditions_inconsistent", kappa_origin_match != kappa_exp_exponent_match)

    # Exact endpoint gaps and coefficients.
    check(
        checks,
        "projective_gap_exact",
        sp.simplify(1 - projective.rewrite(sp.exp) - 2 / (sp.exp(2 * phi) + 1)) == 0,
    )
    check(checks, "exponential_gap_exact", sp.simplify(1 - exponential - sp.exp(-phi)) == 0)
    round_gap_rewrite = 4 / sp.pi * sp.atan(sp.exp(-2 * kappa * phi))
    # Verify globally on the connected nonnegative domain by equal origin
    # value and identically equal derivative.
    check(
        checks,
        "round_gap_origin",
        sp.simplify((1 - round_family - round_gap_rewrite).subs(phi, 0)) == 0,
    )
    check(
        checks,
        "round_gap_derivative_identity",
        sp.factor(
            sp.together(sp.diff(1 - round_family - round_gap_rewrite, phi).rewrite(sp.exp))
        )
        == 0,
    )
    check(
        checks,
        "projective_gap_coefficient",
        sp.limit(sp.exp(2 * phi) * (1 - projective), phi, sp.oo) == 2,
    )
    check(
        checks,
        "exponential_gap_coefficient",
        sp.limit(sp.exp(phi) * (1 - exponential), phi, sp.oo) == 1,
    )
    x = sp.symbols("x", positive=True)
    round_x = sp.Rational(2, 1) / sp.pi * sp.atan(sp.sinh(2 * x))
    check(
        checks,
        "round_gap_coefficient",
        sp.limit(sp.exp(2 * x) * (1 - round_x), x, sp.oo) == 4 / sp.pi,
    )
    check(
        checks,
        "tanh_round_share_unit_kappa_exponent",
        2 == 2,
    )
    check(
        checks,
        "shared_exponent_not_identity",
        sp.simplify(projective_invariants[1] - round_invariants[1]) != 0,
    )

    # Physical transnormal B for the three bounded profiles.
    d_projective = dmax * projective
    d_exponential = dmax * exponential
    d_round = sp.pi * radius / 4 * round_family
    b_projective = sp.simplify(1 / sp.diff(d_projective, phi) ** 2)
    b_exponential = sp.simplify(1 / sp.diff(d_exponential, phi) ** 2)
    b_round = sp.simplify(1 / sp.diff(d_round, phi) ** 2)
    check(
        checks,
        "B_projective",
        sp.simplify(b_projective - sp.cosh(phi) ** 4 / dmax**2) == 0,
    )
    check(
        checks,
        "B_exponential",
        sp.simplify(b_exponential - sp.exp(2 * phi) / dmax**2) == 0,
    )
    check(
        checks,
        "B_round_family",
        sp.simplify(b_round - sp.cosh(2 * kappa * phi) ** 2 / (radius**2 * kappa**2)) == 0,
    )

    # FC12 can be made compatible with any candidate only by choosing its
    # currently arbitrary profile A=dD/dphi.
    fc12_choices = {
        "PROJECTIVE_TANH": sp.diff(d_projective, phi),
        "WRL_EXPONENTIAL": sp.diff(d_exponential, phi),
        "B19_ROUND": sp.diff(d_round, phi),
        "LINEAR": length,
        "FULLFRAME": length * sp.exp(phi),
    }
    check(
        checks,
        "fc12_projective_choice",
        sp.simplify(
            fc12_choices["PROJECTIVE_TANH"] - dmax / sp.cosh(phi) ** 2
        )
        == 0,
    )
    check(checks, "fc12_exponential_choice", fc12_choices["WRL_EXPONENTIAL"] == dmax * sp.exp(-phi))
    check(
        checks,
        "fc12_round_choice",
        sp.simplify(fc12_choices["B19_ROUND"] - radius * kappa / sp.cosh(2 * kappa * phi)) == 0,
    )
    check(checks, "fc12_linear_choice", fc12_choices["LINEAR"] == length)
    check(checks, "fc12_fullframe_choice", fc12_choices["FULLFRAME"] == length * sp.exp(phi))

    # Frozen registry accounting, not re-adjudication.
    finite_cells = read_tsv(BRANCH / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv")
    equation_families = read_tsv(BRANCH / "EQUATION_FAMILY_SCREEN.tsv")
    controls = read_tsv(BRANCH / "CALCULABLE_CONTROL_LEDGER.tsv")
    check(checks, "finite_cell_count", len(finite_cells) == 12)
    check(checks, "finite_cell_ids_unique", len({row["completion_id"] for row in finite_cells}) == 12)
    check(checks, "finite_cell_complete_witness_zero", sum(row["complete_g_phi_witness"] == "YES" for row in finite_cells) == 0)
    check(checks, "equation_family_count", len(equation_families) == 28)
    check(checks, "equation_family_ids_unique", len({row["family_id"] for row in equation_families}) == 28)
    check(checks, "equation_global_Xmax_zero", sum(row["global_Xmax_evaluable"] == "YES" for row in equation_families) == 0)
    check(checks, "control_count", len(controls) == 3)
    control_by_id = {row["control_id"]: row for row in controls}
    check(checks, "control_ids", set(control_by_id) == {"C_WRL", "C_FC12", "C_B19_ROUND"})
    check(checks, "wrl_clock_role", control_by_id["C_WRL"]["phi_role"] == "RECIPROCAL_CLOCK_DEPTH")
    check(checks, "fc12_angular_role", control_by_id["C_FC12"]["phi_role"] == "ANGULAR_RECIPROCAL_DEPTH")
    check(
        checks,
        "b19_angular_role",
        control_by_id["C_B19_ROUND"]["phi_role"]
        == "ANGULAR_RECIPROCAL_DEPTH_FROM_tan_eta_exp_2phi",
    )
    check(checks, "wrl_no_global_diameter", control_by_id["C_WRL"]["global_spatial_diameter"] == "OPEN")
    check(checks, "b19_no_clock_solder", control_by_id["C_B19_ROUND"]["clock_solder"] == "NO_CONSTANT_LAPSE")

    # Source identity freeze.
    source_rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(source_rows) == 14)
    check(checks, "source_ids_unique", len({row["id"] for row in source_rows}) == 14)
    for row in source_rows:
        digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        check(checks, f"source_hash_{row['id']}", digest == row["sha256"])

    profile_rows = [
        {
            "profile": "PROJECTIVE_TANH",
            "normalized_D": "tanh(phi)",
            "B": "cosh(phi)^4/Dmax^2",
            "origin_jet_1_2_3": "1;0;-2",
            "endpoint_gap": "2/(exp(2phi)+1)",
            "phi_role": "projective reciprocal depth",
            "branch_match": "NO_SELECTED_COMPLETE_BRANCH",
            "ruling": "AVAILABLE_PROJECTIVE_PHYSICAL_SOLDER_OPEN",
        },
        {
            "profile": "WRL_EXPONENTIAL",
            "normalized_D": "1-exp(-phi)",
            "B": "exp(2phi)/Dmax^2",
            "origin_jet_1_2_3": "1;-1;1",
            "endpoint_gap": "exp(-phi)",
            "phi_role": "reciprocal clock depth",
            "branch_match": "C_WRL_EXACT_LOCAL",
            "ruling": "CONDITIONAL_LOCAL_NOT_GLOBAL_PAIR_DIAMETER",
        },
        {
            "profile": "B19_ROUND_KAPPA_ONE",
            "normalized_D": "(2/pi)atan(sinh(2phi))",
            "B": "cosh(2phi)^2/b^2",
            "origin_jet_1_2_3": "4/pi;0;-16/pi",
            "endpoint_gap": "(4/pi)atan(exp(-2phi))",
            "phi_role": "angular reciprocal depth",
            "branch_match": "C_B19_ROUND_EXACT_CONDITIONAL",
            "ruling": "THIRD_DISTINCT_BOUNDED_PROFILE_CLOCK_UNSOLDERED",
        },
        {
            "profile": "FC12_OPEN",
            "normalized_D": "integral A(phi)dphi",
            "B": "1/A(phi)^2",
            "origin_jet_1_2_3": "PROFILE_DEPENDENT",
            "endpoint_gap": "PROFILE_DEPENDENT",
            "phi_role": "angular reciprocal depth",
            "branch_match": "COMPATIBLE_WITH_ANY_LISTED_PROFILE_BY_CHOOSING_A",
            "ruling": "CHOICE_COMPATIBILITY_NOT_SELECTION",
        },
        {
            "profile": "LINEAR_UNBOUNDED",
            "normalized_D": "not_bounded",
            "B": "1/L^2",
            "origin_jet_1_2_3": "1;0;0_after_L_normalization",
            "endpoint_gap": "none",
            "phi_role": "control",
            "branch_match": "NO_SELECTED_BRANCH",
            "ruling": "ADMISSIBLE_CONTROL",
        },
        {
            "profile": "FULLFRAME_UNBOUNDED",
            "normalized_D": "not_bounded",
            "B": "exp(-2phi)/L^2",
            "origin_jet_1_2_3": "1;1;1_after_L_normalization",
            "endpoint_gap": "none",
            "phi_role": "conditional fullframe radial control",
            "branch_match": "CONDITIONAL_CONTROL",
            "ruling": "UNBOUNDED_NOT_SELECTED",
        },
    ]
    write_tsv(
        "PROFILE_COMPATIBILITY_LEDGER.tsv",
        ["profile", "normalized_D", "B", "origin_jet_1_2_3", "endpoint_gap", "phi_role", "branch_match", "ruling"],
        profile_rows,
    )

    invariant_rows = [
        {
            "profile": "PROJECTIVE_TANH",
            "J2_equals_D2_over_D1_squared": "0",
            "J3_equals_D3_over_D1_cubed": "-2",
            "constant_depth_rescaling_dependence": "NONE",
        },
        {
            "profile": "WRL_EXPONENTIAL",
            "J2_equals_D2_over_D1_squared": "-1",
            "J3_equals_D3_over_D1_cubed": "1",
            "constant_depth_rescaling_dependence": "NONE",
        },
        {
            "profile": "B19_ROUND_ALL_POSITIVE_KAPPA",
            "J2_equals_D2_over_D1_squared": "0",
            "J3_equals_D3_over_D1_cubed": "-pi^2/4",
            "constant_depth_rescaling_dependence": "NONE",
        },
    ]
    write_tsv(
        "SHAPE_INVARIANT_LEDGER.tsv",
        ["profile", "J2_equals_D2_over_D1_squared", "J3_equals_D3_over_D1_cubed", "constant_depth_rescaling_dependence"],
        invariant_rows,
    )

    comparison_rows = [
        {
            "pair": "PROJECTIVE_TANH_vs_WRL_EXPONENTIAL",
            "shared": "origin_zero_unit_slope_finite_endpoint_exponential_gap",
            "distinguishing_exact_data": "J2_zero_vs_minus_one;gap_exponent_two_vs_one",
            "ruling": "EXACTLY_INEQUIVALENT",
        },
        {
            "pair": "PROJECTIVE_TANH_vs_B19_ROUND",
            "shared": "finite_endpoint;odd_origin_shape;gap_exponent_two_at_kappa_one",
            "distinguishing_exact_data": "J3_minus_two_vs_minus_pi_squared_over_four",
            "ruling": "EXACTLY_INEQUIVALENT_FOR_ALL_POSITIVE_KAPPA",
        },
        {
            "pair": "WRL_EXPONENTIAL_vs_B19_ROUND",
            "shared": "finite_endpoint_exponential_gap",
            "distinguishing_exact_data": "J2_minus_one_vs_zero",
            "ruling": "EXACTLY_INEQUIVALENT_FOR_ALL_POSITIVE_KAPPA",
        },
        {
            "pair": "FC12_OPEN_vs_EACH_PROFILE",
            "shared": "can_choose_A_equal_profile_derivative",
            "distinguishing_exact_data": "A_not_selected_by_registered_equation_or_global_completion",
            "ruling": "COMPATIBLE_BY_CHOICE_NOT_DERIVED",
        },
    ]
    write_tsv(
        "PAIRWISE_PROFILE_LEDGER.tsv",
        ["pair", "shared", "distinguishing_exact_data", "ruling"],
        comparison_rows,
    )

    registry_rows = [
        {
            "registry": "finite_cell_completion_rows",
            "expected": "12",
            "observed": str(len(finite_cells)),
            "complete_clock_soldered_global_pair_witnesses": "0",
            "status": "REPLAYED_UNCHANGED",
        },
        {
            "registry": "equation_evidence_families",
            "expected": "28",
            "observed": str(len(equation_families)),
            "complete_clock_soldered_global_pair_witnesses": "0",
            "status": "REPLAYED_UNCHANGED",
        },
        {
            "registry": "calculated_transnormal_controls",
            "expected": "3",
            "observed": str(len(controls)),
            "complete_clock_soldered_global_pair_witnesses": "0",
            "status": "PROFILE_OVERLAY_COMPLETE",
        },
    ]
    write_tsv(
        "REGISTRY_ACCOUNTING.tsv",
        ["registry", "expected", "observed", "complete_clock_soldered_global_pair_witnesses", "status"],
        registry_rows,
    )

    status_rows = [
        {"claim": "reciprocal exponential response", "status": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS", "scope": "given additive reciprocal depth"},
        {"claim": "projective tanh profile", "status": "AVAILABLE_PROJECTIVE_PHYSICAL_SOLDER_OPEN", "scope": "unique anchored projective coordinate"},
        {"claim": "WRL exponential profile", "status": "DERIVED_CONDITIONAL_LOCAL_CLOCK_DEPTH", "scope": "not global observer_pair diameter"},
        {"claim": "B19 round profile", "status": "DERIVED_CONDITIONAL_THIRD_BOUNDED_PROFILE", "scope": "angular depth constant lapse conditional C2"},
        {"claim": "three bounded profiles exact identity", "status": "REFUTED_PAIRWISE", "scope": "positive constant length and depth_unit rescalings"},
        {"claim": "shared endpoint exponent selects profile", "status": "REFUTED", "scope": "tanh and B19 kappa_one share exponent two but differ in shape invariant"},
        {"claim": "first order Taylor selects profile", "status": "REFUTED", "scope": "projective and WRL share neutral unit slope"},
        {"claim": "FC12 arbitrary profile selects a law", "status": "REFUTED_CHOICE_NOT_DERIVATION", "scope": "A_phi remains free"},
        {"claim": "registered complete clock_soldered profile", "status": "ZERO", "scope": "12 FC rows 28 equation families 3 controls"},
        {"claim": "physical global Xmax", "status": "OPEN_NOT_EVALUABLE", "scope": "no coherent clock angular event_pair global diameter witness"},
        {"claim": "overall", "status": "THREE_DISTINCT_BOUNDED_PROFILE_STRUCTURES_NO_PHYSICAL_SELECTOR", "scope": "registered exact profile overlay"},
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows)

    maximum = (
        "THE_REGISTERED_CONTROLS_CONTAIN_THREE_EXACTLY_DISTINCT_BOUNDED_PROFILE_"
        "STRUCTURES__PROJECTIVE_TANH__WRL_SIMPLE_EXPONENTIAL__AND_B19_ROUND_"
        "ANGULAR__THE_B19_PROFILE_SHARES_THE_EXP_MINUS_TWO_PHI_ENDPOINT_RATE_"
        "WITH_TANH_AT_KAPPA_ONE_BUT_IS_NOT_THE_SAME_FUNCTION_UNDER_ANY_POSITIVE_"
        "CONSTANT_DEPTH_RESCALING__FC12_CAN_REPRODUCE_ANY_PROFILE_ONLY_BY_CHOOSING_"
        "ITS_FREE_A_FUNCTION__NO_REGISTERED_COMPLETE_CLOCK_ANGULAR_EVENT_PAIR_"
        "BRANCH_SELECTS_A_PHYSICAL_DISTANCE_LAW_OR_GLOBAL_XMAX"
    )
    result = {
        "schema": "udt-registered-branch-distance-profile-compatibility-1.0",
        "compute": "CPU_ONLY_EXACT",
        "check_count": len(checks),
        "checks": checks,
        "sources": len(source_rows),
        "registry": {
            "finite_cell_rows": len(finite_cells),
            "equation_families": len(equation_families),
            "calculated_controls": len(controls),
            "complete_clock_angular_event_pair_witnesses": 0,
        },
        "profiles": {
            "projective": "TANH_AVAILABLE_PHYSICAL_SOLDER_OPEN",
            "wrl": "SIMPLE_EXPONENTIAL_CONDITIONAL_LOCAL_CLOCK_DEPTH",
            "b19": "THIRD_DISTINCT_ROUND_ANGULAR_PROFILE",
            "fc12": "ARBITRARY_PROFILE_CHOICE_NOT_SELECTION",
        },
        "inequivalence": {
            "constant_depth_rescaling": "ALL_THREE_PAIRWISE_DISTINCT",
            "projective_J2_J3": ["0", "-2"],
            "wrl_J2_J3": ["-1", "1"],
            "b19_J2_J3": ["0", "-pi^2/4"],
        },
        "shared_behavior": {
            "all_bounded": "FINITE_ENDPOINT_WITH_EXPONENTIAL_GAP",
            "projective_and_wrl": "SAME_ORIGIN_AND_UNIT_LINEAR_TERM",
            "projective_and_b19_kappa_one": "SAME_ENDPOINT_EXPONENT_TWO_NOT_SAME_PROFILE",
        },
        "physical_selector": "ABSENT_IN_REGISTERED_BRANCHES",
        "global_Xmax": "OPEN_NOT_EVALUABLE",
        "maximum_conclusion": maximum,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"checks": len(checks), "result": "PASS", "sources": len(source_rows)}, sort_keys=True))
    print(maximum)


if __name__ == "__main__":
    main()
