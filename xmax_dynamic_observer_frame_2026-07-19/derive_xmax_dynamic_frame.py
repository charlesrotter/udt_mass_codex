#!/usr/bin/env python3
"""Exact CPU algebra for arbitrary time-dependent Xmax observer frames."""

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


def time_map_tile(checks: dict[str, str]) -> dict:
    beta = sp.symbols("beta", real=True)
    n = sp.symbols("n", positive=True)
    time_ratio = sp.exp(2 * beta) * n**2
    spatial_ratio = sp.exp(-2 * beta)
    solutions = sp.solve(sp.Eq(time_ratio, spatial_ratio), n)
    if solutions != [sp.exp(-2 * beta)]:
        raise AssertionError(f"positive time-map solution changed: {solutions}")
    checks["dynamic_time_scale_unique_positive_solution"] = "PASS"

    t = sp.symbols("t", real=True)
    b = sp.Function("beta")(t)
    naive_derivative = sp.diff(sp.exp(-2 * b) * t, t)
    correct_derivative = sp.exp(-2 * b)
    require_zero(
        "naive_time_product_rule_defect",
        naive_derivative - correct_derivative + 2 * t * sp.diff(b, t) * sp.exp(-2 * b),
        checks,
    )
    if sp.simplify(naive_derivative - correct_derivative) == 0:
        raise AssertionError("naive time product falsely valid for moving observer")
    checks["naive_time_product_rejected_when_beta_dot_nonzero"] = "PASS"

    return {
        "differential_map": "dT_beta=exp(-2 beta(t)) dt",
        "integrated_map": "T_beta(t)=T0+integral_from_t0_to_t exp(-2 beta(s)) ds",
        "uniqueness": "positive common-CSN-factor requirement fixes n_beta=exp(-2beta)",
        "monotonicity": "dT_beta/dt>0 for every finite real beta",
        "constant_limit": "beta constant gives T_beta=exp(-2beta)t plus an additive origin",
        "rejected_shortcut": "T=exp(-2beta(t))t has an extra -2t beta_dot term",
        "classification": "EXACT_DYNAMIC_TIME_MAP_IN_FIXED_F3_FRAME_FAMILY",
    }


def full_pullback_tile(checks: dict[str, str]) -> dict:
    phi, beta, v = sp.symbols("phi beta v", real=True)
    c0 = sp.symbols("c", positive=True)
    h11, h12, h13, h22, h23, h33 = sp.symbols("h11 h12 h13 h22 h23 h33", real=True)
    H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])
    target = sp.diag(-sp.exp(-2 * (phi - beta)) * c0**2, 1, 1, 1)
    target[1:4, 1:4] = sp.exp(2 * (phi - beta)) * H
    J = sp.Matrix([
        [sp.exp(-2 * beta), 0, 0, 0],
        [-v, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    pullback = sp.simplify(J.T * target * J)

    shift = sp.Matrix([
        [1, 0, 0, 0],
        [-v, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    source_seed = sp.diag(-sp.exp(-2 * phi) * c0**2, 1, 1, 1)
    source_seed[1:4, 1:4] = sp.exp(2 * phi) * H
    shifted_source = sp.simplify(shift.T * source_seed * shift)
    require_zero("dynamic_complete_metric_pullback", pullback - sp.exp(-2 * beta) * shifted_source, checks)

    if sp.simplify(pullback[0, 1]).equals(0):
        raise AssertionError("moving depth observer lost forced time-depth cross term")
    checks["dynamic_time_depth_cross_term_forced"] = "PASS"
    require_zero("dynamic_pullback_determinant", pullback.det() - sp.exp(-8 * beta) * source_seed.det(), checks)

    return {
        "frame_map": "T'=T_beta(t); phi'=phi-beta(t); y'=y",
        "forced_depth_one_form": "dphi'=dphi-beta_dot dt",
        "complete_pullback": "F_beta^*g0=exp(-2beta)[-exp(-2phi)c^2dt^2+exp(2phi)h_ij(dz^i-delta_phi^i beta_dot dt)(dz^j-delta_phi^j beta_dot dt)]",
        "diagonal_family": "not closed for beta_dot nonzero",
        "off_diagonal_orbit": "closed exactly, including time-depth and any h_phiA-induced time-transverse terms",
        "common_factor": "exp(-2beta(t))",
        "classification": "EXACT_DYNAMIC_FULL_METRIC_ORBIT_CLOSURE; STATIC_DIAGONAL_SUBFAMILY_NOT_CLOSED",
        "scope": "stationary F_beta-invariant spatial seed and fixed F3 time action",
    }


def connection_tile(checks: dict[str, str]) -> dict:
    t, x = sp.symbols("t x", real=True)
    beta = sp.Function("beta")(t, x)
    dbeta = sp.Matrix([sp.diff(beta, t), sp.diff(beta, x)])

    # Keep two conventions distinct. In the active connection convention,
    # phi'=phi-beta and a'=a+d beta make Dphi'=dphi'+a'=Dphi. In fixed
    # unprimed coordinates, the pulled-back coframe instead contains the
    # absorbed shift a_shift=-d beta.
    active_from_zero = dbeta
    pullback_shift = -dbeta
    require_zero("active_depth_connection_sign", -dbeta + active_from_zero, checks)
    require_zero("absorbed_pullback_shift_sign", pullback_shift + dbeta, checks)

    curvature_tx = sp.diff(pullback_shift[1], t) - sp.diff(pullback_shift[0], x)
    require_zero("exact_depth_connection_zero_curvature", curvature_tx, checks)

    return {
        "covariant_depth_coframe": "Dphi=dphi+a",
        "local_recenter": "phi->phi-beta(x); a->a+d beta keeps Dphi invariant",
        "active_transformed_connection": "from a=0, a_prime=+d beta",
        "absorbed_pullback_shift": "in fixed unprimed coordinates, dphi'=dphi+a_shift with a_shift=-d beta",
        "sign_convention": "a_prime and a_shift are different representations and must not be identified",
        "curvature": "da_prime=da_shift=0 identically for smooth beta",
        "classification": "METRIC_PULLBACK_FORCES_A_PURE_GAUGE_DEPTH_CONNECTION_ON_THE_OBSERVER_ORBIT",
        "not_claimed": "independent connection field, force, nonzero holonomy, or dynamics",
    }


def composition_tile(checks: dict[str, str]) -> dict:
    b1, b2 = sp.symbols("beta1 beta2", real=True)
    n1 = sp.exp(-2 * b1)
    n2 = sp.exp(-2 * b2)
    require_zero("dynamic_frame_composed_time_derivative", n1 * n2 - sp.exp(-2 * (b1 + b2)), checks)
    require_zero("dynamic_frame_composed_depth_shift", (sp.Symbol("phi") - b1) - b2 - (sp.Symbol("phi") - (b1 + b2)), checks)

    s = sp.symbols("s", real=True)
    gaussian_half_image = sp.integrate(sp.exp(-2 * s**2), (s, 0, sp.oo))
    require_zero("beta_t2_finite_time_map_image", gaussian_half_image - sp.sqrt(sp.pi / 8), checks)

    return {
        "first_map": "T1=T_beta1(t), phi1=phi-beta1(t)",
        "second_map": "T2=T_beta2(T1), phi2=phi1-beta2(T1)",
        "combined_parameter": "beta12(t)=beta1(t)+beta2(T_beta1(t))",
        "combined_time_derivative": "dT2/dt=exp(-2 beta12(t))",
        "inverse": "exists on the image of each chart interval because T_beta is strictly monotone; a global R-to-R inverse additionally requires surjectivity",
        "global_counterexample": "beta(t)=t^2 on R maps time only onto (-sqrt(pi/8),sqrt(pi/8))",
        "structure": "lifted composition law of orientation-preserving time diffeomorphisms; beta=-one_half log(T_prime) is constrained by T",
        "classification": "EXACT_LOCAL_DYNAMIC_FRAME_COMPOSITION_PSEUDOGROUP; GLOBAL_GROUP_REQUIRES_COMMON_DOMAINS_AND_SURJECTIVITY",
    }


def trajectory_tile(checks: dict[str, str]) -> dict:
    beta, v = sp.symbols("beta v", real=True)
    c0, L = sp.symbols("c L", positive=True)
    w = L * sp.exp(2 * beta) * v / c0
    tangent_norm = -c0**2 * sp.exp(-2 * beta) + L**2 * sp.exp(2 * beta) * v**2
    require_zero("trajectory_norm_factorization", tangent_norm + c0**2 * sp.exp(-2 * beta) * (1 - w**2), checks)
    proper_time_factor = sp.exp(-beta) * sp.sqrt(1 - w**2)
    require_zero(
        "trajectory_proper_time_factor",
        proper_time_factor**2 - (sp.exp(-2 * beta) - L**2 * sp.exp(2 * beta) * v**2 / c0**2),
        checks,
    )
    null_speed = c0 * sp.exp(-2 * beta) / L
    require_zero("trajectory_null_boundary", tangent_norm.subs(v, null_speed), checks)

    return {
        "trajectory": "phi=beta(t)",
        "dimensionless_local_depth_speed": "w=(L/c) exp(2beta) beta_dot",
        "proper_time": "d tau/dt=exp(-beta) sqrt(1-w^2) on the timelike branch",
        "timelike": "|w|<1 equivalently L|beta_dot|<c exp(-2beta)",
        "null": "|w|=1",
        "spacelike": "|w|>1",
        "classification": "EXACT_CONDITIONAL_CAUSAL_CLASSIFICATION_IN_DIAGONAL_RECIPROCAL_DEPTH_METRIC",
        "scope": "observer-trajectory tangent only; not a material speed law or derived light dynamics",
    }


def curvature_2d(metric: sp.Matrix, coords: tuple[sp.Symbol, sp.Symbol]):
    inverse = sp.simplify(metric.inv())
    n = 2
    Gamma = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for left in range(n):
            for right in range(n):
                Gamma[upper][left][right] = sp.simplify(sum(
                    inverse[upper, lower] * (
                        sp.diff(metric[lower, right], coords[left])
                        + sp.diff(metric[lower, left], coords[right])
                        - sp.diff(metric[left, right], coords[lower])
                    ) for lower in range(n)
                ) / 2)
    Ricci = sp.zeros(n)
    for left in range(n):
        for right in range(n):
            Ricci[left, right] = sp.simplify(sum(
                sp.diff(Gamma[upper][left][right], coords[upper])
                - sp.diff(Gamma[upper][left][upper], coords[right])
                + sum(
                    Gamma[upper][upper][lower] * Gamma[lower][left][right]
                    - Gamma[upper][right][lower] * Gamma[lower][left][upper]
                    for lower in range(n)
                ) for upper in range(n)
            ))
    scalar = sp.simplify(sum(inverse[i, j] * Ricci[i, j] for i in range(n) for j in range(n)))
    return Gamma, Ricci, scalar


def acceleration_tile(checks: dict[str, str]) -> dict:
    t, phi = sp.symbols("t phi", real=True)
    c0, L = sp.symbols("c L", positive=True)
    beta = sp.Function("beta")(t)
    velocity = sp.diff(beta, t)
    acceleration = sp.diff(beta, (t, 2))
    common = sp.exp(-2 * beta)
    metric = sp.Matrix([
        [common * (-c0**2 * sp.exp(-2 * phi) + L**2 * sp.exp(2 * phi) * velocity**2), -common * L**2 * sp.exp(2 * phi) * velocity],
        [-common * L**2 * sp.exp(2 * phi) * velocity, common * L**2 * sp.exp(2 * phi)],
    ])
    Gamma, _, scalar = curvature_2d(metric, (t, phi))
    expected = {
        (0, 0, 0): 0,
        (0, 0, 1): -1,
        (0, 1, 1): 0,
        (1, 0, 0): velocity**2 - acceleration - c0**2 * sp.exp(-4 * phi) / L**2,
        (1, 0, 1): -2 * velocity,
        (1, 1, 1): 1,
    }
    for (upper, left, right), value in expected.items():
        require_zero(f"dynamic_connection_{upper}{left}{right}", Gamma[upper][left][right] - value, checks)
    expected_scalar = -4 * sp.exp(-2 * (phi - beta)) / L**2
    require_zero("dynamic_scalar_curvature_pullback", scalar - expected_scalar, checks)
    if scalar.has(velocity) or scalar.has(acceleration):
        raise AssertionError("observer velocity/acceleration survived in scalar curvature")
    checks["dynamic_beta_derivatives_cancel_from_scalar_curvature"] = "PASS"

    v0, a0 = sp.symbols("v0 a0", real=True)
    uniform_connection = sp.simplify(expected[(1, 0, 0)].subs({velocity: v0, acceleration: 0}))
    accelerated_connection = sp.simplify(expected[(1, 0, 0)].subs({velocity: a0 * t, acceleration: a0}))

    return {
        "pullback_metric_1plus1": "exp(-2beta)[-exp(-2phi)c^2dt^2+exp(2phi)L^2(dphi-beta_dot dt)^2]",
        "nonzero_connection_components": {
            "Gamma^t_tphi": "-1",
            "Gamma^phi_tt": "beta_dot^2-beta_double_dot-(c^2/L^2)exp(-4phi)",
            "Gamma^phi_tphi": "-2 beta_dot",
            "Gamma^phi_phiphi": "1",
        },
        "scalar_curvature": "R=-4 exp(-2(phi-beta(t)))/L^2",
        "curvature_interpretation": "R is exactly the original scalar evaluated at phi'=phi-beta(t); beta_dot and beta_double_dot cancel",
        "uniform_witness_beta_vt_Gamma_phi_tt": str(uniform_connection),
        "accelerated_witness_beta_half_at2_Gamma_phi_tt": str(accelerated_connection),
        "classification": "VELOCITY_AND_ACCELERATION_ENTER_THE_METRIC_DERIVED_CONNECTION_BUT_ADD_NO_NEW_SCALAR_CURVATURE_ON_THE_PURE_GAUGE_OBSERVER_ORBIT",
        "scope": "coordinate/frame acceleration in the conditional 1+1 depth slice, not a force or equivalence principle",
    }


def main() -> None:
    checks: dict[str, str] = {}
    time_map = time_map_tile(checks)
    pullback = full_pullback_tile(checks)
    connection = connection_tile(checks)
    composition = composition_tile(checks)
    trajectory = trajectory_tile(checks)
    acceleration = acceleration_tile(checks)

    result = {
        "schema": "udt-xmax-dynamic-observer-frame-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "time_map": time_map,
        "full_metric_pullback": pullback,
        "depth_connection": connection,
        "dynamic_composition": composition,
        "trajectory_causality": trajectory,
        "acceleration_and_curvature": acceleration,
        "seal_and_action": {
            "seal": "time-dependent relational shift does not derive a map to the absolute static Phi=0 seal",
            "action": "not selected; covariance of an eventual action and boundary functional remains open",
            "classification": "OPEN_GLOBAL_FIELD_BOUNDARY_AND_DYNAMICAL_COMPLETION",
        },
        "adjudication": {
            "moving_observers": "EXACT_CONDITIONAL_DYNAMIC_FRAME_ORBIT_EXISTS_WITH_FORCED_OFF_DIAGONAL_SHIFT",
            "accelerating_observers": "ARBITRARY_SMOOTH_BETA_FRAME_PATHS_SUPPORTED KINEMATICALLY; PHYSICAL OBSERVER INTERPRETATION REQUIRES THE TIMELIKE BOUND; BETA_DOUBLE_DOT ENTERS LEVI_CIVITA_CONNECTION",
            "invariant_effect": "NO_NEW_SCALAR_CURVATURE_FROM_BETA_DERIVATIVES_ON_PURE_GAUGE_ORBIT",
            "frame_principle": "EXTENDS_BEYOND_STATIC_RECENTERING_BUT_CURRENT_DYNAMIC_CLOSURE_IS_METRIC_DIFFEO_COVARIANCE_NOT_YET_A_PHYSICAL_EQUIVALENCE_PRINCIPLE",
            "speed_bound": "CONDITIONAL_TIMELIKE_BOUND_ON_OBSERVER_DEPTH_TRAJECTORY_ONLY",
            "action": "NOT_SELECTED",
        },
        "maximum_conclusion": "THE_CONDITIONAL_XMAX_FRAME_EXTENDS_TO_ARBITRARY_SMOOTH_TIME_DEPENDENT_POSITIONAL_RECENTERINGS_WHEN_THE_FULL_OFF_DIAGONAL_METRIC_ORBIT_IS_RETAINED; ONLY_THE_TIMELIKE_SUBSET_QUALIFIES_AS_CONDITIONAL_OBSERVER_TRAJECTORIES; THE_METRIC_PULLBACK_FORCES_A_PURE_GAUGE_DEPTH_SHIFT_AND_LEVI_CIVITA_TERMS_CONTAINING_BETA_DOT_AND_BETA_DOUBLE_DOT; THE_CONDITIONAL_METRIC_SUPPLIES_AN_EXACT_TIMELIKE_BOUND; OBSERVER_DERIVATIVES_CANCEL_FROM_SCALAR_CURVATURE; COMPOSITION_IS_LOCAL_ON_COMPATIBLE_CHARTS_AND_IS_NOT_A_GLOBAL_GROUP_WITHOUT_ADDITIONAL_DOMAIN_AND_SURJECTIVITY_PREMISES; NO_EQUIVALENCE_PRINCIPLE_ACTION_MATTER_SPEED_LAW_OR_GLOBAL_SEAL_BRIDGE_IS_DERIVED",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
