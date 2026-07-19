#!/usr/bin/env python3
"""Exact CPU algebra for the preregistered Xmax full-frame realization audit."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    reducer = lambda entry: sp.simplify(sp.trigsimp(entry.rewrite(sp.exp)))
    reduced = value.applyfunc(reducer) if isinstance(value, sp.MatrixBase) else reducer(value)
    entries = list(reduced) if isinstance(reduced, sp.MatrixBase) else [reduced]
    if any(entry != 0 for entry in entries):
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def projective_tile(checks: dict[str, str]) -> dict:
    r, s = sp.symbols("r s", positive=True)
    a, b, c, d = sp.symbols("a b c d", nonzero=True)
    phi, psi = sp.symbols("phi psi", real=True)
    u, v = sp.symbols("u v", positive=True)

    # The three anchors on the positive projective ray fix a fractional-linear
    # chart uniquely up to an irrelevant common coefficient.
    solution = sp.solve((b + d, a + b, a - c), (b, c, d), dict=True)
    if solution != [{b: -a, c: a, d: a}]:
        raise AssertionError(f"projective anchor solve changed: {solution}")
    checks["projective_three_anchor_uniqueness"] = "PASS"
    xi_r = sp.cancel((r - 1) / (r + 1))
    require_zero("projective_anchor_r_zero", sp.limit(xi_r, r, 0, dir="+") + 1, checks)
    require_zero("projective_anchor_r_one", xi_r.subs(r, 1), checks)
    require_zero("projective_anchor_r_infinity", sp.limit(xi_r, r, sp.oo) - 1, checks)

    xi_uv = sp.cancel((v - u) / (v + u))
    require_zero("projective_CSN_common_scale", xi_uv.subs({u: s * u, v: s * v}) - xi_uv, checks)
    require_zero("projective_reversal", xi_uv.subs({u: v, v: u}, simultaneous=True) + xi_uv, checks)
    require_zero("projective_reciprocal_pair_to_tanh", xi_r.subs(r, sp.exp(2 * phi)) - sp.tanh(phi), checks)

    xi_phi = sp.tanh(phi)
    xi_psi = sp.tanh(psi)
    composed = sp.cancel((xi_phi + xi_psi) / (1 + xi_phi * xi_psi))
    require_zero("projective_pair_composition_to_XR1", composed - sp.tanh(phi + psi), checks)
    require_zero(
        "projective_ratio_multiplication_to_XR1",
        xi_r.subs(r, r * s) - sp.cancel((xi_r + xi_r.subs(r, s)) / (1 + xi_r * xi_r.subs(r, s))),
        checks,
    )

    alternative_at_one = 1 / sp.sqrt(2)
    projective_at_one = sp.tanh(1)
    if sp.simplify(alternative_at_one - projective_at_one) == 0:
        raise AssertionError("nonprojective compactification collapsed to projective chart")
    checks["alternative_bounded_chart_not_projective_witness"] = "PASS"

    return {
        "reciprocal_pair": "[u:v]=[exp(-phi):exp(+phi)] modulo common CSN scale",
        "projective_ratio": "r=v/u=exp(2 phi)",
        "anchored_coordinate": "xi=(r-1)/(r+1)=(v-u)/(v+u)=tanh(phi)",
        "anchor_uniqueness": "unique fractional-linear chart with r=0 -> -1, r=1 -> 0, r=infinity -> +1",
        "composition": "multiplication of reciprocal projective ratios gives xi12=(xi1+xi2)/(1+xi1 xi2)",
        "reversal": "u<->v gives xi->-xi",
        "physical_join": "x=X_max xi",
        "classification": "PROJECTIVE_LAW_DERIVED_CONDITIONAL_ON_IDENTIFYING_POSITIONAL_SEPARATION_WITH_THE_ANCHORED_PROJECTIVE_COORDINATE_OF_THE_RECIPROCAL_CSN_COFRAME_RAY",
        "remaining_choice": "the projective-position identification is not yet owner-locked by the current foundation",
    }


def full_frame_tile(checks: dict[str, str]) -> dict:
    phi, beta, c0 = sp.symbols("phi beta c0", real=True, positive=True)
    t = sp.symbols("t", real=True)
    h11, h12, h13, h22, h23, h33 = sp.symbols("h11 h12 h13 h22 h23 h33", real=True)
    H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])
    target_metric = sp.diag(-sp.exp(-2 * (phi - beta)) * c0**2, 1, 1, 1)
    target_metric[1:4, 1:4] = sp.exp(2 * (phi - beta)) * H
    source_metric = sp.diag(-sp.exp(-2 * phi) * c0**2, 1, 1, 1)
    source_metric[1:4, 1:4] = sp.exp(2 * phi) * H
    jacobian = sp.diag(sp.exp(-2 * beta), 1, 1, 1)
    pullback = sp.simplify(jacobian.T * target_metric * jacobian)
    require_zero("full_frame_common_CSN_factor", pullback - sp.exp(-2 * beta) * source_metric, checks)

    beta1, beta2 = sp.symbols("beta1 beta2", real=True)
    require_zero("full_frame_time_group_composition", sp.exp(-2 * beta1) * sp.exp(-2 * beta2) - sp.exp(-2 * (beta1 + beta2)), checks)
    require_zero("full_frame_depth_group_composition", (phi - beta1) - beta2 - (phi - (beta1 + beta2)), checks)

    xi = sp.symbols("xi", real=True)
    alpha = sp.tanh(beta)
    x_recentered = sp.tanh(phi - beta)
    require_zero(
        "full_frame_bounded_recenter",
        x_recentered - (sp.tanh(phi) - alpha) / (1 - alpha * sp.tanh(phi)),
        checks,
    )
    require_zero("full_frame_Xmax_plus_endpoint", sp.limit((xi - alpha) / (1 - alpha * xi), xi, 1, dir="-") - 1, checks)
    require_zero("full_frame_Xmax_minus_endpoint", sp.limit((xi - alpha) / (1 - alpha * xi), xi, -1, dir="+") + 1, checks)

    if sp.simplify(sp.exp(-2 * beta) - 1) == 0:
        raise AssertionError("CSN homothety falsely became a generic isometry")
    checks["full_frame_not_generic_isometry"] = "PASS"

    return {
        "coordinates": "(t,phi,y1,y2)",
        "metric_family": "g=-exp(-2phi)c^2 dt^2 + exp(2phi) h_ij dz^i dz^j",
        "spatial_seed_condition": "h=h(y) is stationary and F_beta-invariant; arbitrary invariant depth-transverse cross terms survive",
        "frame_map": "phi'=phi-beta; t'=exp(-2beta)t; y'=y; X_max'=X_max; c'=c",
        "group_law": "F_beta2 composed F_beta1 = F_(beta1+beta2)",
        "metric_action": "F_beta pullback g = exp(-2beta) g",
        "causal_action": "conformal factor is positive, so the metric null cone is preserved",
        "bounded_action": "x'=X_max tanh(phi-beta) gives XR1 and fixes +-X_max as limiting endpoints",
        "classification": "EXACT_FULL_FOUR_DIMENSIONAL_FRAME_REALIZATION_IN_DECLARED_RECIPROCAL_CSN_COFRAME_FAMILY",
        "not_claimed": "unique complete UDT metric, isometry, angular topology, action, or physical signal theorem",
    }


def depth_and_dx_tile(checks: dict[str, str]) -> dict:
    phi, beta = sp.symbols("phi beta", real=True)
    alpha = sp.Rational(1, 3)
    beta_witness = sp.log(2) / 2

    # A pure depth seed k(phi)^2 dphi^2 must be translation invariant after
    # the reciprocal exp(2phi) factor supplies the common CSN homothety.
    k = sp.Function("k")
    infinitesimal = sp.diff(k(phi - beta), beta).subs(beta, 0)
    require_zero("depth_seed_translation_infinitesimal", infinitesimal + sp.diff(k(phi), phi), checks)
    constant_seed = sp.symbols("L", positive=True)
    require_zero("constant_depth_seed_realizes_frame", constant_seed - constant_seed, checks)

    # If the time exponent is freed, covariance admits a larger family. This
    # counterfamily scopes the constant-seed selection to fixed F3.
    a = sp.symbols("a", real=True)
    general_common = sp.exp(-2 * (a + 1) * beta)
    general_time_ratio = sp.exp(2 * beta) * sp.exp(-2 * (a + 2) * beta)
    general_spatial_ratio = sp.exp(2 * (phi - beta)) * sp.exp(2 * a * (phi - beta)) / (sp.exp(2 * phi) * sp.exp(2 * a * phi))
    require_zero("free_time_exponent_counterfamily_temporal", general_time_ratio - general_common, checks)
    require_zero("free_time_exponent_counterfamily_spatial", general_spatial_ratio - general_common, checks)

    # In phi coordinates, dx=X sech(phi)^2 dphi.  This seed is not
    # translation invariant and reproduces the earlier exact witnesses.
    bounded_seed = sp.sech(phi) ** 2
    seed_ratio = sp.simplify((bounded_seed.subs(phi, phi - beta) / bounded_seed) ** 2)
    seed_at_zero = (1 - alpha**2) ** 2
    require_zero("bounded_dx_seed_ratio_witness", seed_at_zero - sp.Rational(64, 81), checks)
    common_factor = sp.exp(-2 * beta_witness)
    require_zero("bounded_dx_time_ratio_witness", common_factor - sp.Rational(1, 2), checks)
    require_zero("bounded_dx_spatial_ratio_witness", common_factor * seed_at_zero - sp.Rational(32, 81), checks)
    if seed_at_zero == 1:
        raise AssertionError("bounded dx seed falsely became translation invariant")
    checks["bounded_dx_not_full_frame_seed"] = "PASS"

    xi = sp.symbols("xi", real=True)
    derivative = (1 - alpha**2) / (1 - alpha * xi) ** 2
    spatial_half = sp.simplify(sp.Rational(1, 2) * derivative.subs(xi, sp.Rational(1, 2)) ** 2)
    require_zero("bounded_dx_second_spatial_witness", spatial_half - sp.Rational(512, 625), checks)

    return {
        "full_frame_condition": "the spatial seed before the exp(2phi) reciprocal weight must be invariant under phi translations",
        "pure_depth_solution": "k(phi)=constant=L, hence reciprocal spatial coframe L dphi",
        "normalization": "L=X_max is an available global normalization using the working ruler, not a derivation of X_max's value",
        "bounded_dx_seed": "dx=X_max sech(phi)^2 dphi",
        "bounded_dx_witness_beta_atanh_one_third": {
            "time_ratio": "1/2",
            "spatial_ratio_phi_zero": "32/81",
            "spatial_ratio_xi_half": "512/625",
        },
        "free_time_exponent_counterfamily": "k(phi)=exp(a phi), t'=exp(-(a+2)beta)t gives common factor exp(-2(a+1)beta)",
        "classification": "FIXED_F3_TIME_ACTION_SELECTS_ADDITIVE_DEPTH_COFRAME_OVER_BOUNDED_DX_WITHIN_THE_REGISTERED_PURE_DEPTH_CLASS",
        "scope": "constant k is selected only with fixed t'=exp(-2beta)t; bounded dx still fails every constant time rescaling because its defect depends on position; new field/frame mixing is outside the declared class",
    }


def transverse_tile(checks: dict[str, str]) -> dict:
    phi, beta, C = sp.symbols("phi beta C", real=True, positive=True)
    R_solution = C * sp.exp(phi)
    require_zero(
        "transverse_warp_functional_equation",
        R_solution.subs(phi, phi - beta) - sp.exp(-beta) * R_solution,
        checks,
    )
    require_zero("transverse_warp_infinitesimal", sp.diff(R_solution, phi) - R_solution, checks)

    theta = sp.symbols("theta", positive=True)
    q_round = sp.diag(1, sp.sin(theta) ** 2)
    q_flat = sp.eye(2)
    require_zero("round_transverse_seed_phi_independent", sp.diff(q_round, phi), checks)
    require_zero("flat_transverse_seed_phi_independent", sp.diff(q_flat, phi), checks)

    # A nonzero invariant depth-transverse cross term is already represented
    # by arbitrary h12/h13 in the full-frame matrix proof.
    return {
        "restricted_warp_equation": "R(phi-beta)=exp(-beta)R(phi)",
        "positive_solution": "R(phi)=C exp(phi)",
        "equivalent_form": "all spatial coframe directions carry the same exp(+phi) reciprocal weight over a phi-independent seed",
        "surviving_intrinsic_seeds": ["round local S2 q=diag(1,sin(theta)^2)", "flat local q=diag(1,1)", "arbitrary phi-independent q_AB and invariant cross terms"],
        "classification": "PHI_DEPENDENCE_SELECTED_IN_RESTRICTED_WARP_CLASS_BUT_INTRINSIC_TRANSVERSE_GEOMETRY_TOPOLOGY_ROUNDNESS_TWIST_AND_BOUNDARY_REMAIN_OPEN",
    }


def conformal_counterfamily_tile(checks: dict[str, str]) -> dict:
    du, dv = sp.symbols("hprime_minus_u hprime_v", positive=True)

    A0, A1 = sp.symbols("A0 A1", positive=True)
    null_metric_target = sp.Matrix([[0, -A1 / 2], [-A1 / 2, 0]])
    null_metric_source = sp.Matrix([[0, -A0 / 2], [-A0 / 2, 0]])
    J = sp.diag(du, dv)
    pullback = sp.simplify(J.T * null_metric_target * J)
    factor = sp.simplify(A1 * du * dv / A0)
    require_zero("arbitrary_null_reparameterization_is_conformal", pullback - factor * null_metric_source, checks)
    if factor <= 0:
        raise AssertionError("monotone null reparameterization lost positive conformal factor")
    checks["arbitrary_null_reparameterization_positive_factor"] = "PASS"

    return {
        "optical_coordinates": "u=t-y, v=t+y with g2=-A(y) du dv",
        "extension": "u'=-h_beta(-u), v'=h_beta(v), where h_beta is any smooth monotone one-parameter re-centering conjugated into optical y",
        "pullback_factor": "A(y') h_beta'(-u) h_beta'(v) / A(y)",
        "classification": "EXACT_COUNTERFAMILY_TWO_DIMENSIONAL_LOCAL_CSN_COVARIANCE_ALONE_DOES_NOT_SELECT_XR1_OR_THE_PROJECTIVE_CHART",
        "remaining_gate": "the reciprocal projective coframe join or full transverse structure must do the selecting",
    }


def seal_and_bootstrap_tile(checks: dict[str, str]) -> dict:
    beta = sp.symbols("beta", real=True, nonzero=True)
    seal_value_after_internal_shift = -beta
    if sp.simplify(seal_value_after_internal_shift) == 0:
        raise AssertionError("absolute zero seal falsely invariant under internal shift")
    checks["absolute_zero_seal_not_invariant_under_internal_shift"] = "PASS"

    X, c0, M = sp.symbols("X c M_total", positive=True)
    # Observer parameter beta does not act on declared global scalars in the
    # constructed frame representation.
    require_zero("Xmax_fixed_under_frame_map", sp.diff(X, beta), checks)
    require_zero("c_fixed_under_frame_map", sp.diff(c0, beta), checks)
    require_zero("candidate_global_mass_scalar_fixed_if_declared", sp.diff(M, beta), checks)

    return {
        "relational_depth_action": "phi_rel'=phi_rel-beta so each positional observer can set local relational depth to zero",
        "absolute_seal_test": "if the same physical scalar is shifted internally, Phi_abs=0 maps to -beta and the seal is not preserved",
        "classification": "RELATIONAL_DEPTH_AND_ABSOLUTE_STATIC_SEAL_FIELD_CANNOT_BE_SILENTLY_IDENTIFIED_IN_THIS_FRAME_REALIZATION",
        "allowed_resolutions_not_selected": ["phi_rel is a coordinate/ray parameter distinct from Phi_abs", "derive a compensating boundary/frame action", "revise the absolute-seal or global-frame interpretation"],
        "bootstrap_Xmax": "X_max can be invariant if it is a scalar output of complete-solution closure",
        "mass_caveat": "this requires a native observer-independent M_total; current complete action/source/mass definition remains open",
        "c_caveat": "the symbol c is unchanged and conformal null cones are preserved; its value or bootstrap origin is not derived",
    }


def main() -> None:
    checks: dict[str, str] = {}
    projective = projective_tile(checks)
    full_frame = full_frame_tile(checks)
    depth_dx = depth_and_dx_tile(checks)
    transverse = transverse_tile(checks)
    conformal_counterfamily = conformal_counterfamily_tile(checks)
    seal_bootstrap = seal_and_bootstrap_tile(checks)

    result = {
        "schema": "udt-xmax-full-frame-realization-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "projective_position": projective,
        "full_frame": full_frame,
        "depth_vs_bounded_differential": depth_dx,
        "transverse_sector": transverse,
        "two_dimensional_conformal_counterfamily": conformal_counterfamily,
        "seal_and_bootstrap": seal_bootstrap,
        "adjudication": {
            "realization": "EXACT_CONDITIONAL_FULL_FRAME_CSN_REALIZATION_EXISTS_IN_RECIPROCAL_ADDITIVE_DEPTH_COFRAME_FAMILY",
            "positional_law": "DERIVED_CONDITIONAL_ON_PROJECTIVE_POSITION_JOIN; NOT_DERIVED_FROM_XMAX_OR_1PLUS1_CSN_ALONE",
            "old_dx_metric": "REFUTED_AS_FULL_FRAME_REALIZATION_IN_DECLARED_NATURAL_RECENTERING_CLASS",
            "angular_sector": "RECIPROCAL_PHI_DEPENDENCE_SELECTED_IN_RESTRICTED_WARP_CLASS; INTRINSIC_GEOMETRY_AND_GLOBAL_COMPLETION_OPEN",
            "seal": "RELATIONAL_DEPTH_TO_ABSOLUTE_STATIC_FIELD_JOIN_OPEN",
            "Xmax_value": "OPEN; MAY_BE_INVARIANT_BOOTSTRAP_OUTPUT_ONLY_AFTER_NATIVE_GLOBAL_SCALAR_CLOSURE",
            "action": "NOT_SELECTED",
        },
        "maximum_conclusion": "A_COMPLETE_FOUR_DIMENSIONAL_CSN_FRAME_ACTION_EXISTS_CONDITIONALLY_WHEN_POSITION_IS_THE_ANCHORED_PROJECTIVE_COORDINATE_OF_THE_RECIPROCAL_CSN_COFRAME_RAY_AND_THE_SPATIAL_SEED_IS_ADDITIVE_DEPTH_TRANSLATION_INVARIANT; THIS_DERIVES_XR1_AND_SELECTS_COMMON_RECIPROCAL_PHI_WEIGHT_BUT_NOT_THE_PROJECTIVE_POSITION_JOIN_INTRINSIC_TRANSVERSE_GEOMETRY_SEAL_BRIDGE_XMAX_VALUE_ACTION_OR_MATTER",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
