#!/usr/bin/env python3
"""Exact production algebra for the preregistered two-frame metric-limit audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def require(name: str, condition: bool, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def classify_power_at_infinity(power: sp.Expr) -> str:
    if power.is_positive:
        return "INFINITE"
    if power.is_zero:
        return "FINITE_NONZERO"
    if power.is_negative:
        return "ZERO"
    return "SIGN_DEPENDENT"


def classify_power_at_zero(power: sp.Expr) -> str:
    if power.is_positive:
        return "ZERO"
    if power.is_zero:
        return "FINITE_NONZERO"
    if power.is_negative:
        return "INFINITE"
    return "SIGN_DEPENDENT"


def main() -> None:
    checks: dict[str, bool] = {}

    c, N, H = sp.symbols("c N H", positive=True, finite=True)
    B = sp.symbols("B", real=True, finite=True)
    v = sp.symbols("v", real=True)

    # Effective stationary one-dimensional connector. B is a signed shift.
    g = sp.Matrix(
        [
            [c**2 * (-N**2 + H**2 * B**2), c * H**2 * B],
            [c * H**2 * B, H**2],
        ]
    )
    require("stationary_connector_determinant", sp.simplify(g.det() + c**2 * N**2 * H**2) == 0, checks)

    null_poly = sp.expand(g[0, 0] + 2 * g[0, 1] * v + g[1, 1] * v**2)
    roots = [sp.simplify(root) for root in sp.solve(null_poly, v)]
    expected_roots = [sp.simplify(c * (-B - N / H)), sp.simplify(c * (-B + N / H))]
    require("stationary_connector_null_roots", set(roots) == set(expected_roots), checks)

    # The speed relative to the orthogonal clock/ruler frame is exactly c.
    local_ratios = [sp.simplify(H * (root / c + B) / N) for root in roots]
    require("local_orthonormal_ratios_are_plus_minus_one", set(local_ratios) == {-1, 1}, checks)

    D, F = sp.symbols("D F", positive=True, finite=True)
    reciprocal_subs = {N: F * D, H: 1 / D, B: 0}
    reciprocal_roots = sorted(
        [sp.simplify(root.subs(reciprocal_subs)) for root in roots], key=sp.default_sort_key
    )
    require(
        "reciprocal_coordinate_slopes",
        set(reciprocal_roots) == {-c * F * D**2, c * F * D**2},
        checks,
    )
    require("reciprocal_clock_factor", sp.simplify((F * D) - N.subs(reciprocal_subs)) == 0, checks)
    require("reciprocal_ruler_factor", sp.simplify((1 / D) - H.subs(reciprocal_subs)) == 0, checks)

    # Constant-regime rates relative to an ordinary anchor N0=1.
    chi_proper = sp.simplify(F * D)
    chi_coordinate = sp.simplify(F * D**2)
    require("proper_rate_is_lapse_ratio", chi_proper == F * D, checks)
    require("coordinate_rate_is_F_D_squared", chi_coordinate == F * D**2, checks)
    require("local_rate_remains_one", sp.simplify(chi_coordinate / (D * chi_proper)) == 1, checks)

    # Two frames at the same stationary lapse compare clocks at unit ratio.
    N_A, N_B = sp.symbols("N_A N_B", positive=True)
    clock_ratio = sp.simplify(N_A / N_B)
    require("same_regime_mutual_clock_ratio", clock_ratio.subs({N_A: N, N_B: N}) == 1, checks)

    # A shrinking family keeps L/sigma=lambda nonzero and finite.
    sigma, lam, p, alpha = sp.symbols("sigma lambda p alpha", positive=True)
    D_sigma = sigma ** (-p)
    F_sigma = D_sigma**alpha
    N_sigma = sp.simplify(F_sigma * D_sigma)
    L_sigma = lam * sigma
    T_anchor_sigma = sp.simplify(L_sigma / (c * N_sigma))
    T_micro_sigma = sp.simplify(L_sigma / c)
    require("nontrivial_adjacency_ratio", sp.simplify(L_sigma / sigma - lam) == 0, checks)
    require("micro_normalized_rate", sp.simplify(L_sigma / (c * T_anchor_sigma) - N_sigma) == 0, checks)
    require("micro_local_normalized_rate", sp.simplify(L_sigma / (c * T_micro_sigma) - 1) == 0, checks)

    # Asymptotic exponent atlas. F~D^alpha.
    exponent_rows = []
    for label, probe_alpha in [
        ("ALPHA_GT_MINUS_ONE", sp.Integer(0)),
        ("ALPHA_EQ_MINUS_ONE", sp.Integer(-1)),
        ("BETWEEN_MINUS_TWO_AND_MINUS_ONE", sp.Rational(-3, 2)),
        ("ALPHA_EQ_MINUS_TWO", sp.Integer(-2)),
        ("ALPHA_LT_MINUS_TWO", sp.Integer(-3)),
    ]:
        proper_power = sp.simplify(probe_alpha + 1)
        coordinate_power = sp.simplify(probe_alpha + 2)
        exponent_rows.append(
            {
                "class": label,
                "alpha_probe": str(probe_alpha),
                "proper_D_power": str(proper_power),
                "coordinate_D_power": str(coordinate_power),
                "micro_D_to_infinity_proper": classify_power_at_infinity(proper_power),
                "outer_D_to_zero_proper": classify_power_at_zero(proper_power),
                "micro_D_to_infinity_coordinate": classify_power_at_infinity(coordinate_power),
                "outer_D_to_zero_coordinate": classify_power_at_zero(coordinate_power),
            }
        )
    require(
        "F_equal_one_has_two_ended_proper_rate",
        exponent_rows[0]["micro_D_to_infinity_proper"] == "INFINITE"
        and exponent_rows[0]["outer_D_to_zero_proper"] == "ZERO",
        checks,
    )
    require(
        "F_equal_D_inverse_cancels_proper_wings",
        exponent_rows[1]["micro_D_to_infinity_proper"] == "FINITE_NONZERO"
        and exponent_rows[1]["outer_D_to_zero_proper"] == "FINITE_NONZERO",
        checks,
    )
    require(
        "coordinate_and_proper_thresholds_differ",
        exponent_rows[2]["micro_D_to_infinity_proper"] == "ZERO"
        and exponent_rows[2]["micro_D_to_infinity_coordinate"] == "INFINITE",
        checks,
    )

    # Static zero-shift path: the effective proper-distance/anchor-time rate is
    # the proper-length-weighted harmonic mean of N.
    L1, L2, n1, n2 = sp.symbols("L1 L2 n1 n2", positive=True)
    chi_path = sp.simplify((L1 + L2) / (L1 / n1 + L2 / n2))
    require("uniform_connector_rate", sp.simplify(chi_path.subs({n1: N, n2: N}) - N) == 0, checks)
    require(
        "one_micro_one_ordinary_equal_lengths_bounded",
        sp.limit(chi_path.subs({L1: 1, L2: 1, n1: D, n2: 1}), D, sp.oo) == 2,
        checks,
    )
    eps = sp.symbols("epsilon", positive=True)
    endpoint_micro_with_ordinary_middle = sp.simplify((1 + 2 * eps) / (1 + 2 * eps / D))
    require(
        "micro_endpoints_do_not_force_micro_connector",
        sp.limit(endpoint_micro_with_ordinary_middle, D, sp.oo) == 1 + 2 * eps,
        checks,
    )
    require(
        "whole_micro_connector_diverges",
        sp.limit(chi_path.subs({n1: D, n2: D}), D, sp.oo) == sp.oo,
        checks,
    )

    # Angular/transverse geometry enters the proper-length weights H_i. It
    # cancels for a uniform N and remains in a nonuniform path.
    h1, h2, dl1, dl2 = sp.symbols("h1 h2 dl1 dl2", positive=True)
    weighted_path = sp.simplify((h1 * dl1 + h2 * dl2) / (h1 * dl1 / n1 + h2 * dl2 / n2))
    require(
        "angular_path_weights_cancel_for_uniform_lapse",
        sp.simplify(weighted_path.subs({n1: N, n2: N}) - N) == 0,
        checks,
    )
    require(
        "angular_path_weights_survive_for_nonuniform_lapse",
        sp.diff(weighted_path, h1) != 0,
        checks,
    )

    # Shift and reversal controls in a stationary effective connector.
    s = sp.symbols("s", real=True)
    forward_rate = sp.simplify(N - H * B)
    backward_rate = sp.simplify(N + H * B)
    roundtrip_rate = sp.simplify((N**2 - H**2 * B**2) / N)
    coordinate_static_clock = sp.sqrt(N**2 - H**2 * B**2)
    require("reversal_swaps_one_way_rates", forward_rate.xreplace({B: -B}) == backward_rate, checks)
    require(
        "roundtrip_rate_from_two_legs",
        sp.simplify(2 / (1 / forward_rate + 1 / backward_rate) - roundtrip_rate) == 0,
        checks,
    )
    require(
        "bounded_shift_fraction_preserves_N_scaling",
        sp.simplify(roundtrip_rate.subs(B, s * N / H) - N * (1 - s**2)) == 0,
        checks,
    )
    require(
        "near_null_shift_can_cancel_forward_divergence",
        sp.simplify(forward_rate.subs(B, (N - 1) / H) - 1) == 0,
        checks,
    )
    require(
        "coordinate_static_clock_norm",
        sp.simplify(g[0, 0] + c**2 * coordinate_static_clock**2) == 0,
        checks,
    )

    # Passive time rescaling preserves rates normalized to an ordinary anchor.
    kappa, N0 = sp.symbols("kappa N0", positive=True)
    normalized_forward = sp.simplify(forward_rate / N0)
    rescaled_forward = sp.simplify(
        forward_rate.subs({N: N / kappa, B: B / kappa}) / (N0 / kappa)
    )
    require("time_rescaling_invariant_normalized_rate", sp.simplify(rescaled_forward - normalized_forward) == 0, checks)

    # Noncentral regularity controls. A constant reciprocal plateau is flat;
    # a smooth transition has curvature set by its independently free width.
    t, x = sp.symbols("t x", real=True)
    A0, w = sp.symbols("A0 w", positive=True)
    A_fun = sp.Function("A")(x)
    plane_metric = sp.diag(-c**2 * A_fun, 1 / A_fun)
    plane_inverse = sp.simplify(plane_metric.inv())
    plane_coords = (t, x)
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                plane_inverse[a, d]
                * (
                    sp.diff(plane_metric[d, b], plane_coords[cc])
                    + sp.diff(plane_metric[d, cc], plane_coords[b])
                    - sp.diff(plane_metric[b, cc], plane_coords[d])
                )
                for d in range(2)
            )
        )
        for cc in range(2)] for b in range(2)] for a in range(2)]
    ricci = sp.MutableDenseMatrix(2, 2, [0] * 4)
    for a in range(2):
        for b in range(2):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(gamma[cc][a][b], plane_coords[cc])
                    - sp.diff(gamma[cc][a][cc], plane_coords[b])
                    + sum(
                        gamma[cc][cc][d] * gamma[d][a][b]
                        - gamma[cc][b][d] * gamma[d][a][cc]
                        for d in range(2)
                    )
                    for cc in range(2)
                )
            )
    scalar_curvature = sp.simplify(
        sum(plane_inverse[a, b] * ricci[a, b] for a in range(2) for b in range(2))
    )
    require("direct_planar_scalar_curvature", sp.simplify(scalar_curvature + sp.diff(A_fun, x, 2)) == 0, checks)
    # A direct product with a flat transverse plane has the same nonzero Riemann
    # block. In two dimensions R_abcd R^abcd=R^2 exactly.
    kretschmann = sp.simplify(scalar_curvature**2)
    require("constant_plateau_scalar_flat", scalar_curvature.subs(A_fun, A0).doit() == 0, checks)
    require("constant_plateau_kretschmann_flat", kretschmann.subs(A_fun, A0).doit() == 0, checks)

    y = sp.symbols("y", real=True)
    f = 3 * y**2 - 2 * y**3
    A_transition = 1 + (D**2 - 1) * f
    Axx_transition = sp.simplify(sp.diff(A_transition, y, 2) / w**2)
    K_transition = sp.simplify(Axx_transition**2)
    require("transition_endpoint_values", A_transition.subs(y, 0) == 1 and A_transition.subs(y, 1) == D**2, checks)
    require("transition_endpoint_first_jets", sp.diff(A_transition, y).subs(y, 0) == 0 and sp.diff(A_transition, y).subs(y, 1) == 0, checks)
    require(
        "transition_curvature_width_dependence",
        sp.simplify(K_transition.subs(y, 0) - 36 * (D**2 - 1) ** 2 / w**4) == 0,
        checks,
    )
    require(
        "transition_fixed_width_diverges",
        sp.limit(K_transition.subs({y: 0, w: 1}), D, sp.oo) == sp.oo,
        checks,
    )
    require(
        "transition_width_proportional_D_bounded",
        sp.limit(K_transition.subs({y: 0, w: D}), D, sp.oo) == 36,
        checks,
    )

    # In proper spatial coordinate x, a general static clock factor has
    # ds^2=-c^2 n(x)^2 dt^2+dx^2 and R=-2 n_xx/n.
    n_fun = sp.Function("n")(x)
    proper_metric = sp.diag(-c**2 * n_fun**2, 1)
    proper_inverse = sp.simplify(proper_metric.inv())
    proper_gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                proper_inverse[a, d]
                * (
                    sp.diff(proper_metric[d, b], plane_coords[cc])
                    + sp.diff(proper_metric[d, cc], plane_coords[b])
                    - sp.diff(proper_metric[b, cc], plane_coords[d])
                )
                for d in range(2)
            )
        )
        for cc in range(2)] for b in range(2)] for a in range(2)]
    proper_ricci = sp.MutableDenseMatrix(2, 2, [0] * 4)
    for a in range(2):
        for b in range(2):
            proper_ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(proper_gamma[cc][a][b], plane_coords[cc])
                    - sp.diff(proper_gamma[cc][a][cc], plane_coords[b])
                    + sum(
                        proper_gamma[cc][cc][d] * proper_gamma[d][a][b]
                        - proper_gamma[cc][b][d] * proper_gamma[d][a][cc]
                        for d in range(2)
                    )
                    for cc in range(2)
                )
            )
    proper_scalar = sp.simplify(
        sum(proper_inverse[a, b] * proper_ricci[a, b] for a in range(2) for b in range(2))
    )
    require("direct_proper_coordinate_curvature", sp.simplify(proper_scalar + 2 * sp.diff(n_fun, x, 2) / n_fun) == 0, checks)

    lam_coord = sp.symbols("lambda_coord", real=True)
    D_fun = sp.Function("D")(lam_coord)
    F_fun = sp.Function("F")(lam_coord)
    N_fun = F_fun * D_fun
    reciprocal_planar_scalar = sp.simplify(
        -2 * D_fun / N_fun * sp.diff(D_fun * sp.diff(N_fun, lam_coord), lam_coord)
    )
    reciprocal_planar_expected = sp.simplify(
        -2
        * (
            D_fun**2 * sp.diff(F_fun, lam_coord, 2) / F_fun
            + 3 * D_fun * sp.diff(D_fun, lam_coord) * sp.diff(F_fun, lam_coord) / F_fun
            + sp.diff(D_fun, lam_coord) ** 2
            + D_fun * sp.diff(D_fun, lam_coord, 2)
        )
    )
    require("reciprocal_planar_curvature_expansion", sp.simplify(reciprocal_planar_scalar - reciprocal_planar_expected) == 0, checks)
    require("arbitrary_D_F_inverse_flat", sp.simplify(reciprocal_planar_scalar.subs(F_fun, 1 / D_fun).doit()) == 0, checks)

    # Positive oscillatory threading counterclass: F=D^-1(2+sin(log D))
    # makes the proper anchor rate 2+sin(log D), which has no wing limit.
    z = sp.symbols("z", real=True)
    oscillatory_rate = 2 + sp.sin(z)
    require("oscillatory_threading_positive", sp.simplify(oscillatory_rate.subs(z, sp.pi / 2) - 3) == 0, checks)
    require("oscillatory_threading_distinct_subsequence", sp.simplify(oscillatory_rate.subs(z, 3 * sp.pi / 2) - 1) == 0, checks)

    result = {
        "schema": "udt-two-frame-regime-metric-limit-derivation-1.0",
        "base": "73b33e2c9f11e897976d571810a8e98dc3a2e644",
        "preregistration_commit": "e14bd4a",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "formulas": {
            "stationary_connector_metric": "ds^2=-c_E^2*N^2*dt^2+H^2*(dlambda+c_E*B*dt)^2",
            "null_coordinate_rates": "dlambda/dt=c_E*(-B +/- N/H)",
            "local_orthonormal_rate": "H*(dlambda/dt/c_E+B)/N=+/-1",
            "reciprocal_definition": "D=exp(-phi); N=F*D; H_parallel=1/D",
            "reciprocal_coordinate_rate": "abs(dlambda/dt)/c_E=F*D^2",
            "proper_distance_anchor_rate": "dell/(c_E*dt_anchor)=F*D=N/N0 for N0=1",
            "same_regime_clock_ratio": "N_A/N_B=1 when N_A=N_B",
            "static_path_rate": "chi=L_total/integral(dell/N)",
            "shift_one_way_rates": "chi_plus=N-H*B; chi_minus=N+H*B",
            "shift_roundtrip_rate": "chi_round=(N^2-H^2*B^2)/N",
            "coordinate_static_clock_factor": "sqrt(N^2-H^2*B^2)",
            "micro_family": "D=sigma^(-p); F=D^alpha; L_AB=lambda*sigma",
            "micro_anchor_time": str(T_anchor_sigma),
            "micro_local_time": str(T_micro_sigma),
            "planar_reciprocal_curvature": "R=-A''; K=(A'')^2 for A=D^2",
            "transition_A": "A=1+(D^2-1)*(3y^2-2y^3)",
            "transition_K_at_ordinary_end": "36*(D^2-1)^2/w^4",
            "proper_coordinate_curvature": "R=-2*n_xx/n",
            "general_reciprocal_planar_curvature": "R=-2[D^2 F''/F+3 D D' F'/F+(D')^2+D D'']",
            "flat_variable_reciprocal_counterclass": "F=1/D gives n=F*D=1 and R=0 for arbitrary smooth positive D",
            "oscillatory_threading_counterclass": "F=D^-1*(2+sin(log D)) gives positive nonconvergent proper rate",
        },
        "asymptotic_atlas": exponent_rows,
        "bounded_classifications": {
            "recorded_diagonal_F1_zero_shift": "EXACT_TWO_ENDED_RELATIVE_ACCESSIBILITY_CONTROL",
            "arbitrary_F": "THREE_PROPER_RATE_CLASSES_WITH_THRESHOLD_ALPHA_MINUS_ONE",
            "arbitrary_shift": "ONE_WAY_AND_ROUNDTRIP_LIMITS_SHIFT_DEPENDENT",
            "uniform_micro_connector": "DIVERGES_RELATIVE_TO_ORDINARY_ANCHOR_IF_N_MIN_TO_INFINITY",
            "micro_endpoints_only": "INSUFFICIENT",
            "same_micro_regime_mutual_clock_ratio": "UNITY",
            "local_orthonormal_metric_rate": "C_E",
            "constant_noncentral_plateau": "FLAT_FOR_EACH_FINITE_D",
            "transition_to_ordinary_region": "PROFILE_AND_WIDTH_DEPENDENT_REGULARITY",
            "arbitrary_D_with_F_inverse": "FLAT_BUT_FIXED_CHART_DETERMINANT_TENDS_TO_ZERO_ON_EXTREME_WINGS",
            "oscillatory_F": "POSITIVE_NO_LIMIT_CLASS",
            "physical_sigma_to_phi_map": "NOT_SUPPLIED",
            "material_information_transfer": "NOT_TESTED",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS {len(checks)}/{len(checks)} exact checks")
    print(OUT)


if __name__ == "__main__":
    main()
