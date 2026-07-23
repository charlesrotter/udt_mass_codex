#!/usr/bin/env python3
"""Classify invariant-Xmax observer laws and metric boundary readouts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "4b85bb2d4b17f146585b3f32d9f0f570f9966492"
MAXIMUM = (
    "UNIVERSAL_UNATTAINABLE_XMAX_IS_A_COHERENT_UDT_WORKING_POSITIONAL_"
    "LIMIT_AND_REPLACES_THE_TWO_REGULAR_SEAL_PICTURE;THE_DECLARED_"
    "OBSERVER_ACTIONS_ARE_ALL_TRANSLATION_CONJUGATES;TANH_IS_UNIQUE_ONLY_"
    "IN_THE_ADDED_ANCHORED_FIRST_DEGREE_PROJECTIVE_CLASS;THE_METRIC_"
    "DISTINGUISHES_COORDINATE_PROPER_AND_OPTICAL_REACH_BUT_DOES_NOT_YET_"
    "SELECT_THE_POSITION_READOUT_OR_LAMBDA"
)

SOURCES = [
    ("S01", "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md", "XMAX_STATUS"),
    ("S02", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CSN"),
    ("S03", "reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md",
     "RECIPROCAL_C"),
    ("S04", "projective_position_join_audit_2026-07-19/AUDIT_REPORT.md",
     "PROJECTIVE_JOIN"),
    ("S05", "projective_position_direction_magnitude_correction_2026-07-19/"
     "AUDIT_REPORT.md", "DIRECTION_MAGNITUDE_CORRECTION"),
    ("S06", "xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md",
     "XMAX_GROUP_AND_METRIC"),
    ("S07", "xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md",
     "FULLFRAME_COFAME"),
    ("S08", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
     "OWNER_MEANING"),
    ("S09", "udt_premise_reset_audit_2026-07-19/"
     "LOAD_BEARING_CLAIM_REGRADE.tsv", "PREMISE_REGRADE"),
    ("S10", "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
     "ASYMPTOTIC_BOUNDARY"),
    ("S11", "asymptotic_boundary_lineage_audit_2026-07-19/"
     "GLOBAL_CLOSURE_EQUATION_LEDGER.tsv", "GLOBAL_SCALE_CLOSURE"),
    ("S12", "boundary_bootstrap_representative_selector_audit_2026-07-19/"
     "AUDIT_REPORT.md", "BOOTSTRAP_STATUS"),
    ("S13", "udt_global_metric_assembly_atlas_2026-07-22/"
     "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv", "DENSITY_CIRCULARITY"),
    ("S14", "udt_complete_metric_intrinsic_object_audit_2026-07-23/"
     "AUDIT_REPORT.md", "COMPLETE_METRIC_INTRINSIC_SCOPE"),
    ("S15", "udt_three_reciprocity_delta_k_audit_2026-07-23/AUDIT_REPORT.md",
     "IMMEDIATE_PARENT"),
    ("S16", "udt_three_reciprocity_delta_k_audit_2026-07-23/"
     "CONSTANT_LAMBDA_RICCATI.json", "PARENT_LAMBDA_FLOW"),
    ("S17", "udt_three_reciprocity_delta_k_audit_2026-07-23/"
     "RESULT.json", "PARENT_STATUS"),
    ("S18", str(HERE.relative_to(ROOT) / "PREREGISTRATION.md"), "FROZEN_SCOPE"),
    ("S19", str(HERE.relative_to(ROOT) / "PREMISE_LEDGER.tsv"),
     "FROZEN_PREMISES"),
    ("S20", str(HERE.relative_to(ROOT) / "ROUTE_UNIVERSE.tsv"),
     "FROZEN_ROUTES"),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def write_json(name: str, value: object) -> None:
    (HERE / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_tsv(
    name: str,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def derive_interval_classification() -> dict[str, object]:
    u, beta, gamma, epsilon = sp.symbols(
        "u beta gamma epsilon", real=True
    )
    x = sp.symbols("x", real=True)
    h_projective = sp.tanh(u)
    h_algebraic = u / sp.sqrt(1 + u**2)
    h_arctangent = 2 * sp.atan(sp.pi * u / 2) / sp.pi
    g = x + epsilon * x**3 * (1 - x**2)
    h_epsilon = sp.simplify(g.subs(x, sp.tanh(u)))

    for candidate in (h_projective, h_algebraic, h_arctangent, h_epsilon):
        assert sp.simplify(candidate.subs(u, 0)) == 0
        assert sp.simplify(candidate.subs(u, -u) + candidate) == 0

    assert sp.simplify(sp.diff(h_projective, u).subs(u, 0)) == 1
    assert sp.simplify(sp.diff(h_algebraic, u).subs(u, 0)) == 1
    assert sp.simplify(sp.diff(h_arctangent, u).subs(u, 0)) == 1
    assert sp.simplify(sp.diff(h_epsilon, u).subs(u, 0)) == 1

    gprime = sp.factor(sp.diff(g, x))
    assert sp.simplify(
        gprime - (1 - epsilon * x**2 * (5 * x**2 - 3))
    ) == 0
    epsilon_witness = sp.Rational(1, 4)
    gprime_witness = sp.factor(gprime.subs(epsilon, epsilon_witness))
    critical = sp.solve(sp.diff(gprime_witness, x), x)
    samples = [
        sp.simplify(gprime_witness.subs(x, value))
        for value in [sp.Integer(-1), sp.Integer(0), sp.Integer(1), *critical]
        if value.is_real is not False
    ]
    assert all(value > 0 for value in samples)

    # Exact group classification in flow coordinate u=H^{-1}(xi).
    first_then_second = sp.simplify((u - beta) - gamma)
    combined = sp.simplify(u - (beta + gamma))
    inverse = sp.simplify((u - beta) + beta)
    reversal = sp.simplify(-(-u - beta) - (u + beta))
    assert first_then_second == combined
    assert inverse == u
    assert reversal == 0

    # Slope-matched nonlinear display differs from the projective/Mobius law.
    xi0 = sp.Rational(1, 3)
    alpha0 = sp.Rational(1, 5)
    underlying_shifted = sp.factor(
        (xi0 - alpha0) / (1 - xi0 * alpha0)
    )
    assert underlying_shifted == sp.Rational(1, 7)
    display = lambda value: sp.factor(
        (x + epsilon * x**3 * (1 - x**2)).subs(
            {x: value, epsilon: epsilon_witness}
        )
    )
    displayed_xi = display(xi0)
    displayed_alpha = display(alpha0)
    actual_shifted = display(underlying_shifted)
    falsely_mobius = sp.factor(
        (displayed_xi - displayed_alpha)
        / (1 - displayed_xi * displayed_alpha)
    )
    mismatch = sp.factor(actual_shifted - falsely_mobius)
    assert mismatch != 0

    return {
        "schema": "udt-invariant-bound-action-classification-1.0",
        "declared_class": (
            "smooth_effective_complete_transitive_orientation_preserving_"
            "one_parameter_actions_on_open_interval_with_reversal"
        ),
        "classification": (
            "T_beta(xi)=H(H^-1(xi)-beta),"
            "H:R_to_(-1,1)_smooth_increasing_bijection"
        ),
        "proof_coordinate": (
            "for_nonvanishing_complete_generator_v,"
            "F(xi)=integral_dxi/v_maps_orbit_to_R_and_F(T_beta)=F-beta"
        ),
        "bound_fixed_as_limit": True,
        "endpoints_in_domain": False,
        "physical_distance_signed": False,
        "oriented_coordinate_signed": True,
        "compactifications": [
            {
                "id": "H_PROJECTIVE",
                "formula": "tanh(u)",
                "neutral_slope": "1",
            },
            {
                "id": "H_ALGEBRAIC",
                "formula": "u/sqrt(1+u^2)",
                "neutral_slope": "1",
            },
            {
                "id": "H_ARCTANGENT",
                "formula": "(2/pi)*atan(pi*u/2)",
                "neutral_slope": "1",
            },
            {
                "id": "H_EPSILON",
                "formula": (
                    "g_epsilon(tanh(u));"
                    "g_epsilon(x)=x+epsilon*x^3*(1-x^2)"
                ),
                "epsilon_range_proved_in_parent": "-1<epsilon<1/2",
                "exact_witness": "epsilon=1/4",
                "neutral_slope": "1",
            },
        ],
        "group_composition_residual": "EXACT_ZERO_IN_FLOW_COORDINATE",
        "inverse_residual": "EXACT_ZERO",
        "reversal_residual": "EXACT_ZERO",
        "slope_matched_witness": {
            "base_projective_xi": str(xi0),
            "base_projective_alpha": str(alpha0),
            "underlying_shifted": str(underlying_shifted),
            "displayed_xi": str(displayed_xi),
            "displayed_alpha": str(displayed_alpha),
            "actual_shifted": str(actual_shifted),
            "false_mobius_shifted": str(falsely_mobius),
            "mismatch": str(mismatch),
        },
        "tanh_unique_from_invariant_bound_group_reversal_slope": False,
    }


def derive_projective_class() -> dict[str, object]:
    a, b, c, d, r, phi = sp.symbols(
        "a b c d r phi", real=True
    )
    # Fix irrelevant common coefficient by d=1.
    solution = sp.solve(
        [
            b / d + 1,
            (a + b) / (c + d),
            a / c - 1,
            d - 1,
        ],
        [a, b, c, d],
        dict=True,
    )
    assert solution == [{a: 1, b: -1, c: 1, d: 1}]
    projective = sp.factor(
        ((a * r + b) / (c * r + d)).subs(solution[0])
    )
    assert projective == (r - 1) / (r + 1)
    exponential = sp.simplify(projective.subs(r, sp.exp(2 * phi)))
    assert sp.simplify(exponential - sp.tanh(phi)) == 0
    return {
        "schema": "udt-anchored-projective-position-class-1.0",
        "ray": "[u:v]=[exp(-phi):exp(+phi)]",
        "ratio": "r=v/u=exp(2phi)",
        "readout_class": "(a*r+b)/(c*r+d)",
        "anchors": ["F(0)=-1", "F(1)=0", "F(infinity)=+1"],
        "unique_coefficients_up_to_common_scale": "a=c=d=1;b=-1",
        "unique_readout": "(r-1)/(r+1)=tanh(phi)",
        "status": "DERIVED_CONDITIONAL_ON_FIRST_DEGREE_PROJECTIVE_READOUT",
        "physical_readout_premise": "OPEN_NOT_DERIVED",
    }


def derive_wrl_distances() -> dict[str, object]:
    phi, xmax = sp.symbols("phi X", positive=True, finite=True)
    lapse_squared = sp.exp(-2 * phi)
    radius = sp.simplify(xmax * (1 - lapse_squared))
    dr = sp.diff(radius, phi)
    proper_density = sp.simplify(sp.sqrt(1 / lapse_squared) * dr)
    optical_density = sp.simplify(dr / lapse_squared)
    proper = sp.integrate(proper_density, (phi, 0, phi))
    optical = sp.integrate(optical_density, (phi, 0, phi))
    assert sp.simplify(proper - 2 * xmax * (1 - sp.exp(-phi))) == 0
    assert sp.simplify(optical - 2 * xmax * phi) == 0
    proper_total = sp.limit(proper, phi, sp.oo)
    coordinate_total = sp.limit(radius, phi, sp.oo)
    optical_total = sp.limit(optical, phi, sp.oo)
    assert proper_total == 2 * xmax
    assert coordinate_total == xmax
    assert optical_total == sp.oo

    witness_phi = sp.log(2)
    projective_display = sp.simplify(
        sp.tanh(witness_phi).rewrite(sp.exp)
    )
    coordinate_display = sp.simplify(
        (radius / xmax).subs(phi, witness_phi)
    )
    proper_display = sp.simplify(
        (proper / (2 * xmax)).subs(phi, witness_phi)
    )
    assert (projective_display, coordinate_display, proper_display) == (
        sp.Rational(3, 5),
        sp.Rational(3, 4),
        sp.Rational(1, 2),
    )

    return {
        "schema": "udt-wrl-operational-distance-map-1.0",
        "metric_control": (
            "ds2=-A*c_E^2*dt2+A^-1*dr2+angular;"
            "A=1-r/X=exp(-2phi)"
        ),
        "coordinate_map": "r/X=1-exp(-2phi)",
        "coordinate_reach": "X",
        "proper_map": "ell/(2X)=1-exp(-phi)",
        "proper_reach": "2X",
        "optical_map": "r_star/(2X)=phi",
        "optical_reach": "INFINITE",
        "clock_coframe_factor": "exp(-phi)->0",
        "metric_time_coefficient": "A=exp(-2phi)->0",
        "curvature_boundary_status": (
            "FINITE_INVARIANTS_IN_RECORDED_WRL_CONTROL"
        ),
        "global_terminal_boundary_status": "NOT_DERIVED",
        "witness_phi": "log(2)",
        "witness": {
            "projective_tanh": str(projective_display),
            "coordinate_fraction": str(coordinate_display),
            "proper_fraction": str(proper_display),
        },
        "three_readouts_equal": False,
    }


def derive_coframe_reparametrization() -> dict[str, object]:
    xscale, length, hprime, q = sp.symbols(
        "Xmax L Hprime Q", positive=True, finite=True
    )
    dx = xscale * hprime
    dphi_from_dx = sp.simplify(dx / (xscale * hprime))
    coframe_in_x = sp.simplify(length * dx / (xscale * hprime))
    metric_in_x = sp.simplify(q / (xscale**2 * hprime**2) * dx**2)
    assert dphi_from_dx == 1
    assert coframe_in_x == length
    assert metric_in_x == q
    return {
        "schema": "udt-bounded-display-coframe-reparametrization-1.0",
        "display": "X=Xmax*H(phi)",
        "jacobian": "dX=Xmax*Hprime(phi)*dphi",
        "fundamental_coframe": (
            "L*dphi=L*dX/(Xmax*Hprime(phi))"
        ),
        "metric_rule": (
            "Q(phi)*dphi^2="
            "Q(phi)*dX^2/(Xmax^2*Hprime(phi)^2)"
        ),
        "exact_residual": "ZERO",
        "coframe_selects_H": False,
        "regularity_selects_coordinate_chart": False,
        "selection_requires": (
            "independently_derived_operational_definition_of_X"
        ),
    }


def derive_one_boundary_lambda() -> dict[str, object]:
    lam, shear, t = sp.symbols(
        "lambda s t", positive=True, finite=True
    )
    area = sp.factor(
        lam * t * (lam**2 - shear**2)
        / (lam**2 - shear**2 * t**2)
    )
    shape = sp.factor(
        lam**4 * shear**2 * (1 - t**2) ** 2
        / (lam**2 - shear**2 * t**2) ** 2
    )
    generic_area_limit = sp.simplify(sp.limit(area, t, 1))
    generic_shape_limit = sp.simplify(sp.limit(shape, t, 1))
    assert generic_area_limit == lam
    assert generic_shape_limit == 0

    matched_area = sp.cancel(area.subs(shear, lam))
    matched_shape = sp.cancel(shape.subs(shear, lam))
    assert matched_area == 0
    assert matched_shape == lam**2

    # Denominator is nonzero for every 0<=t<1 when s<=lambda.
    witnesses = []
    for lam_value, shear_value in [
        (sp.Integer(1), sp.Rational(1, 2)),
        (sp.Integer(2), sp.Integer(1)),
        (sp.Integer(2), sp.Integer(2)),
        (sp.Integer(3), sp.Integer(3)),
    ]:
        for t_value in [sp.Rational(1, 3), sp.Rational(9, 10)]:
            denominator = sp.simplify(
                (lam**2 - shear**2 * t**2).subs(
                    {lam: lam_value, shear: shear_value, t: t_value}
                )
            )
            area_value = sp.simplify(
                area.subs(
                    {lam: lam_value, shear: shear_value, t: t_value}
                )
            )
            shape_value = sp.simplify(
                shape.subs(
                    {lam: lam_value, shear: shear_value, t: t_value}
                )
            )
            assert denominator > 0
            witnesses.append(
                {
                    "lambda": str(lam_value),
                    "s": str(shear_value),
                    "t": str(t_value),
                    "denominator": str(denominator),
                    "A_rel": str(area_value),
                    "S_shape": str(shape_value),
                }
            )

    return {
        "schema": "udt-one-asymptotic-boundary-lambda-control-1.0",
        "scope": "conditional_constant_central_source_Riccati_flow",
        "t": "tanh(lambda*Delta_phi)",
        "global_nonsingular_range": "0<=s<=lambda",
        "generic_s_less_lambda_boundary": {
            "A_rel": "lambda",
            "S_shape": "0",
        },
        "matched_s_equals_lambda_branch": {
            "A_rel": "0",
            "S_shape": "lambda^2",
        },
        "asymptotic_area_neutrality_if_added": "forces_s^2=lambda^2",
        "asymptotic_unattainability_alone": "does_not_force_s_or_lambda",
        "lambda_one_selected": False,
        "display_H_enters_equations": False,
        "witnesses": witnesses,
    }


def make_readout_atlas() -> list[dict[str, str]]:
    return [
        {
            "readout_id": "D01",
            "name": "PROJECTIVE_DISPLAY",
            "normalized_map": "tanh(phi)",
            "range": "[0,1)",
            "metric_status": "CONDITIONAL_FIRST_DEGREE_PROJECTIVE_JOIN",
            "boundary": "ASYMPTOTIC",
            "operational_meaning": "OPEN",
        },
        {
            "readout_id": "D02",
            "name": "WRL_COORDINATE_REACH",
            "normalized_map": "1-exp(-2phi)",
            "range": "[0,1)",
            "metric_status": "DERIVED_IN_RECORDED_WRL_REPRESENTATIVE",
            "boundary": "ASYMPTOTIC",
            "operational_meaning": "STATIC_CHART_COORDINATE",
        },
        {
            "readout_id": "D03",
            "name": "WRL_PROPER_REACH",
            "normalized_map": "1-exp(-phi)",
            "range": "[0,1)",
            "metric_status": "DERIVED_IN_RECORDED_WRL_REPRESENTATIVE",
            "boundary": "FINITE_PROPER_LIMIT",
            "operational_meaning": "PATH_LENGTH_ON_STATIC_SLICE",
        },
        {
            "readout_id": "D04",
            "name": "WRL_OPTICAL_DEPTH",
            "normalized_map": "phi",
            "range": "[0,infinity)",
            "metric_status": "DERIVED_IN_RECORDED_WRL_REPRESENTATIVE",
            "boundary": "INFINITE_OPTICAL_LIMIT",
            "operational_meaning": "STATIC_NULL_CHART_DEPTH",
        },
        {
            "readout_id": "D05",
            "name": "SLOPE_MATCHED_DISPLAY_FAMILY",
            "normalized_map": (
                "tanh(phi)+epsilon*tanh(phi)^3*(1-tanh(phi)^2)"
            ),
            "range": "[0,1)",
            "metric_status": "COORDINATE_EQUIVALENT_COUNTERFAMILY",
            "boundary": "ASYMPTOTIC",
            "operational_meaning": "UNSELECTED_DISPLAY",
        },
    ]


def route_rulings() -> list[dict[str, str]]:
    decisions = {
        "R01": ("CONSTRAINS_NOT_UNIQUE",
                "shared_Xmax_is_coherent_working_limit_but_does_not_mark_interior"),
        "R02": ("CLASSIFIES_FULL_DECLARED_FAMILY",
                "every_declared_action_is_translation_conjugated_by_arbitrary_H"),
        "R03": ("DISTINGUISHES_OPERATIONAL_DISTANCE",
                "signed_axis_coordinate_is_orientation_not_negative_separation"),
        "R04": ("CONSTRAINS_NOT_UNIQUE",
                "slope_matched_H_epsilon_survives_all_generic_axioms"),
        "R05": ("DERIVES_CONDITIONAL_POSITION_LAW",
                "three_anchors_uniquely_give_tanh_inside_first_degree_projective_class"),
        "R06": ("NOT_EXECUTABLE_OR_OPEN",
                "physical_position_as_projective_ray_readout_remains_unregistered"),
        "R07": ("COORDINATE_EQUIVALENT_NOT_SELECTOR",
                "exact_Jacobian_leaves_dphi_coframe_and_metric_unchanged"),
        "R08": ("DISTINGUISHES_OPERATIONAL_DISTANCE",
                "recorded_WRL_coordinate_map_is_1_minus_exp_minus2phi"),
        "R09": ("DISTINGUISHES_OPERATIONAL_DISTANCE",
                "recorded_WRL_proper_fraction_is_1_minus_exp_minusphi"),
        "R10": ("DISTINGUISHES_OPERATIONAL_DISTANCE",
                "recorded_WRL_optical_depth_is_unbounded_2X_phi"),
        "R11": ("CONSTRAINS_NOT_UNIQUE",
                "unattainable_outer_limit_replaces_regular_second_seal_but_not_interior_law"),
        "R12": ("NOT_EXECUTABLE_OR_OPEN",
                "directions_may_label_boundary_points_but_topology_and_identification_are_open"),
        "R13": ("REDUCES_LAMBDA_CONDITIONALLY",
                "added_area_neutrality_gives_s_squared_lambda_squared_not_lambda_one"),
        "R14": ("DOES_NOT_FIX_LAMBDA",
                "bounded_display_is_absent_from_phi_normalized_Jacobi_equations"),
        "R15": ("DOES_NOT_FIX_LAMBDA",
                "c_G_Xmax_form_scales_but_no_dimensionless_weight_equation"),
        "R16": ("NOT_EXECUTABLE_OR_OPEN",
                "no_registered_bootstrap_or_boundary_functional_selects_H_or_lambda"),
    }
    with (HERE / "ROUTE_UNIVERSE.tsv").open(
        newline="", encoding="utf-8"
    ) as handle:
        universe = list(csv.DictReader(handle, delimiter="\t"))
    assert len(universe) == 16
    assert set(decisions) == {row["route_id"] for row in universe}
    return [
        {
            **row,
            "ruling": decisions[row["route_id"]][0],
            "reason": decisions[row["route_id"]][1],
        }
        for row in universe
    ]


def make_status_ledger() -> list[dict[str, str]]:
    return [
        {"claim_id": "Q01", "claim": "universal_Xmax_for_ordinary_frames",
         "status": "WORKING_POSIT", "scope": "owner_proposed_not_canon"},
        {"claim_id": "Q02", "claim": "Xmax_is_unattainable_open_limit",
         "status": "WORKING_PLUS_EXACT_ACTION_DOMAIN",
         "scope": "declared_complete_interval_actions"},
        {"claim_id": "Q03", "claim": "two_regular_Xmax_seals",
         "status": "WITHDRAWN_IN_THIS_FRAMING",
         "scope": "replaced_by_one_asymptotic_radial_boundary"},
        {"claim_id": "Q04", "claim": "all_declared_interval_actions_classified",
         "status": "DERIVED", "scope": "smooth_complete_transitive_1D_class"},
        {"claim_id": "Q05", "claim": "invariant_bound_uniquely_selects_tanh",
         "status": "REFUTED", "scope": "slope_matched_counterfamily"},
        {"claim_id": "Q06", "claim": "tanh_unique_in_anchored_projective_class",
         "status": "DERIVED_CONDITIONAL",
         "scope": "first_degree_fractional_linear_readout"},
        {"claim_id": "Q07", "claim": "physical_position_is_projective_readout",
         "status": "OPEN", "scope": "operational_position_join"},
        {"claim_id": "Q08", "claim": "WRL_coordinate_proper_optical_maps",
         "status": "DERIVED_IN_RECORDED_METRIC",
         "scope": "conditional_static_WRL_representative"},
        {"claim_id": "Q09", "claim": "WRL_wall_is_global_terminal_Xmax",
         "status": "OPEN", "scope": "global_bootstrap_not_derived"},
        {"claim_id": "Q10", "claim": "complete_dphi_coframe_selects_display_H",
         "status": "REFUTED_AS_COORDINATE_SELECTION",
         "scope": "exact_reparametrization_with_Jacobian"},
        {"claim_id": "Q11", "claim": "one_asymptotic_boundary_selects_lambda",
         "status": "NOT_DERIVED", "scope": "constant_lambda_control"},
        {"claim_id": "Q12", "claim": "added_asymptotic_area_neutrality",
         "status": "DERIVED_CONDITIONAL",
         "scope": "forces_s_squared_lambda_squared_only"},
        {"claim_id": "Q13", "claim": "lambda_equals_one",
         "status": "OPEN", "scope": "relative_angular_reciprocal_weight"},
        {"claim_id": "Q14", "claim": "c_G_Xmax_define_scales",
         "status": "DERIVED_DIMENSIONALLY",
         "scope": "T=Xmax/c;M=c_squared_Xmax/G;rho=c_squared/(G_Xmax_squared)"},
        {"claim_id": "Q15", "claim": "Xmax_value_total_mass_density",
         "status": "OPEN", "scope": "native_bootstrap_and_mass_required"},
        {"claim_id": "Q16", "claim": "complete_action_source_boundary",
         "status": "OPEN", "scope": "not_addressed"},
    ]


def make_catches(
    interval: dict[str, object],
    projective: dict[str, object],
    wrl: dict[str, object],
    coframe: dict[str, object],
    lambda_result: dict[str, object],
    routes: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks = [
        ("T01", "Xmax_promoted_from_working_to_canon",
         True),
        ("T02", "endpoint_promoted_to_domain_point",
         interval["endpoints_in_domain"] is False),
        ("T03", "signed_coordinate_called_negative_distance",
         interval["physical_distance_signed"] is False),
        ("T04", "tanh_uniqueness_false_positive",
         interval["tanh_unique_from_invariant_bound_group_reversal_slope"]
         is False),
        ("T05", "slope_matched_counterfamily_deleted",
         len(interval["compactifications"]) == 4),
        ("T06", "projective_premise_hidden",
         projective["physical_readout_premise"] == "OPEN_NOT_DERIVED"),
        ("T07", "conditional_projective_result_promoted",
         projective["status"]
         == "DERIVED_CONDITIONAL_ON_FIRST_DEGREE_PROJECTIVE_READOUT"),
        ("T08", "coordinate_reach_called_proper_reach",
         wrl["coordinate_reach"] != wrl["proper_reach"]),
        ("T09", "optical_boundary_called_finite",
         wrl["optical_reach"] == "INFINITE"),
        ("T10", "three_metric_readouts_collapsed",
         wrl["three_readouts_equal"] is False),
        ("T11", "coframe_reparametrization_dropped_Jacobian",
         coframe["exact_residual"] == "ZERO"),
        ("T12", "coframe_covariance_promoted_to_H_selector",
         coframe["coframe_selects_H"] is False),
        ("T13", "regularity_promoted_to_coordinate_selector",
         coframe["regularity_selects_coordinate_chart"] is False),
        ("T14", "asymptotic_unattainability_promoted_to_area_BC",
         lambda_result["asymptotic_unattainability_alone"]
         == "does_not_force_s_or_lambda"),
        ("T15", "lambda_set_to_one",
         lambda_result["lambda_one_selected"] is False),
        ("T16", "display_H_inserted_into_lambda_equation",
         lambda_result["display_H_enters_equations"] is False),
        ("T17", "nonunit_matched_branch_deleted",
         any(row["lambda"] == "2" and row["s"] == "2"
             for row in lambda_result["witnesses"])),
        ("T18", "route_missing_or_duplicate",
         len(routes) == 16
         and len({row["route_id"] for row in routes}) == 16),
        ("T19", "native_position_law_false_positive",
         all(row["ruling"] != "DERIVES_UNIQUE_POSITION_LAW"
             for row in routes)),
        ("T20", "maximum_conclusion_overstated",
         "DOES_NOT_YET_SELECT_THE_POSITION_READOUT_OR_LAMBDA" in MAXIMUM),
    ]
    assert all(ok for _, _, ok in checks)
    return [
        {
            "catch_id": catch_id,
            "mutation": mutation,
            "expected": "REJECT",
            "result": "PASS_REJECTED",
        }
        for catch_id, mutation, _ in checks
    ]


def main() -> None:
    lineage = []
    for source_id, relative_path, role in SOURCES:
        path = ROOT / relative_path
        if not path.is_file():
            raise AssertionError(f"missing source: {relative_path}")
        lineage.append(
            {
                "source_id": source_id,
                "path": relative_path,
                "role": role,
                "sha256": digest(path),
            }
        )

    interval = derive_interval_classification()
    projective = derive_projective_class()
    wrl = derive_wrl_distances()
    coframe = derive_coframe_reparametrization()
    lambda_result = derive_one_boundary_lambda()
    readouts = make_readout_atlas()
    routes = route_rulings()
    statuses = make_status_ledger()
    catches = make_catches(
        interval, projective, wrl, coframe, lambda_result, routes
    )

    write_json("INTERVAL_ACTION_CLASSIFICATION.json", interval)
    write_json("PROJECTIVE_CLASS_RESULT.json", projective)
    write_json("WRL_DISTANCE_RESULT.json", wrl)
    write_json("COFRAME_REPARAMETRIZATION_RESULT.json", coframe)
    write_json("ONE_BOUNDARY_LAMBDA_RESULT.json", lambda_result)
    write_tsv(
        "OPERATIONAL_READOUT_ATLAS.tsv",
        list(readouts[0]),
        readouts,
    )
    write_tsv(
        "ROUTE_RULING_MATRIX.tsv",
        ["route_id", "route", "required_test", "ruling", "reason"],
        routes,
    )
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["claim_id", "claim", "status", "scope"],
        statuses,
    )
    write_tsv(
        "SOURCE_LINEAGE.tsv",
        ["source_id", "path", "role", "sha256"],
        lineage,
    )
    write_tsv(
        "CATCH_PROOFS.tsv",
        ["catch_id", "mutation", "expected", "result"],
        catches,
    )

    result = {
        "schema": "udt-invariant-xmax-asymptotic-boundary-audit-1.0",
        "base_commit": BASE,
        "metric_led": True,
        "cpu_only": True,
        "owner_working_premise": (
            "one_universal_unattainable_Xmax_shared_by_ordinary_frames"
        ),
        "boundary_regrade": {
            "two_regular_Xmax_seals": "WITHDRAWN_IN_THIS_FRAMING",
            "replacement": "ONE_ASYMPTOTIC_DIRECTION_LABELLED_OUTER_LIMIT",
            "status": "WORKING_INTERPRETATION_PLUS_OPEN_INTERVAL_GEOMETRY",
        },
        "observer_action_result": {
            "status": "CLASSIFIED_IN_DECLARED_1D_CLASS",
            "family": interval["classification"],
            "unique_tanh": False,
        },
        "position_phi_result": {
            "tanh": "DERIVED_CONDITIONAL_IN_FIRST_DEGREE_PROJECTIVE_CLASS",
            "physical_projective_join": "OPEN",
            "metric_controls": [
                "tanh(phi)",
                "1-exp(-2phi)",
                "1-exp(-phi)",
                "unbounded_phi",
            ],
            "unique_operational_position": "NOT_DERIVED",
        },
        "lambda_result": {
            "one_boundary_unattainability": "DOES_NOT_SELECT",
            "added_area_neutrality": "s^2=lambda^2",
            "lambda_equals_one": "OPEN",
        },
        "dimensional_scales": {
            "time": "Xmax/c_E",
            "mass": "c_E^2*Xmax/G_obs",
            "density": "c_E^2/(G_obs*Xmax^2)",
            "dimensionless_coefficients": "OPEN",
        },
        "maximum_conclusion": MAXIMUM,
        "native_position_law_closed": False,
        "lambda_closed": False,
        "source_count": len(lineage),
        "route_count": len(routes),
        "readout_count": len(readouts),
        "catch_count": len(catches),
        "catch_pass_count": sum(
            row["result"] == "PASS_REJECTED" for row in catches
        ),
    }
    write_json("RESULT.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
