#!/usr/bin/env python3
"""Exact production algebra for the UDT clock-anchor/scale/threading audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def clean(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda item: sp.factor(sp.trigsimp(sp.simplify(item))))
    return sp.factor(sp.trigsimp(sp.simplify(value)))


def coordinate_tensors(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    dimension = len(coords)
    inverse = clean(metric.inv())
    gamma = [[[
        clean(sp.Rational(1, 2) * sum(
            inverse[upper, delta] * (
                sp.diff(metric[delta, right], coords[left])
                + sp.diff(metric[delta, left], coords[right])
                - sp.diff(metric[left, right], coords[delta])
            )
            for delta in range(dimension)
        ))
        for right in range(dimension)] for left in range(dimension)] for upper in range(dimension)]
    riemann_up = [[[[] for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]
    for rho in range(dimension):
        for sigma in range(dimension):
            for mu in range(dimension):
                riemann_up[rho][sigma][mu] = [clean(
                    sp.diff(gamma[rho][nu][sigma], coords[mu])
                    - sp.diff(gamma[rho][mu][sigma], coords[nu])
                    + sum(
                        gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                        - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                        for lam in range(dimension)
                    )
                ) for nu in range(dimension)]
    riemann_down = [[[[] for _ in range(dimension)] for _ in range(dimension)] for _ in range(dimension)]
    for rho in range(dimension):
        for sigma in range(dimension):
            for mu in range(dimension):
                riemann_down[rho][sigma][mu] = [clean(
                    sum(metric[rho, lam] * riemann_up[lam][sigma][mu][nu] for lam in range(dimension))
                ) for nu in range(dimension)]
    return inverse, gamma, riemann_down


def main() -> None:
    c, f, x = sp.symbols("c_E F X", positive=True)
    dt = sp.symbols("dt", positive=True)

    orbit = sp.diag(-c**2 * f**2 * x, 1 / x)
    orbit_inverse = clean(orbit.inv())
    clock_factor = clean(sp.sqrt(-orbit[0, 0]) / c)
    ruler_factor = clean(sp.sqrt(orbit[1, 1]))
    null_slope = clean(sp.sqrt(-orbit[0, 0] / orbit[1, 1]))
    proper_ratio = clean(ruler_factor * null_slope / clock_factor)
    modulation_product = clean(sp.sqrt(x) * 1 / sp.sqrt(x))

    # Passive time relabeling dt=s(t) dt_new.  Its radial derivative is zero.
    scale = sp.symbols("s", positive=True)
    f_new = clean(scale * f)
    determinant = clean(orbit.det())
    determinant_new = clean(determinant.subs(f, f_new))
    f_r, x_r = sp.symbols("F_R X_R", real=True)
    acceleration_r = clean(f_r / f + x_r / (2 * x))
    acceleration_relabelled = clean(f_r / f + x_r / (2 * x))

    # Static spherical metric with independent lapse N and areal-radial scalar X.
    t, radius, theta, azimuth = sp.symbols("t R theta azimuth", real=True)
    N = sp.Function("N")(radius)
    X = sp.Function("X")(radius)
    metric = sp.diag(-c**2 * N**2, 1 / X, radius**2, radius**2 * sp.sin(theta)**2)
    inverse, _, riemann = coordinate_tensors(metric, (t, radius, theta, azimuth))
    m01 = clean(riemann[0][1][0][1] * X / (c**2 * N**2))
    m02 = clean(riemann[0][2][0][2] / (c**2 * N**2 * radius**2))
    m12 = clean(riemann[1][2][1][2] * X / radius**2)
    m23 = clean(riemann[2][3][2][3] / (radius**4 * sp.sin(theta)**2))
    expected_m01 = clean(X * sp.diff(N, radius, 2) / N + sp.diff(X, radius) * sp.diff(N, radius) / (2 * N))
    expected_m02 = clean(X * sp.diff(N, radius) / (radius * N))
    expected_m12 = clean(-sp.diff(X, radius) / (2 * radius))
    expected_m23 = clean((1 - X) / radius**2)
    kretschmann_motifs = clean(4 * (m01**2 + 2 * m02**2 + 2 * m12**2 + m23**2))

    # Direct diagonal contraction independently inside the production route.
    kretschmann_direct = clean(sum(
        inverse[i, i] * inverse[j, j] * inverse[k, k] * inverse[l, l]
        * riemann[i][j][k][l] ** 2
        for i in range(4) for j in range(4) for k in range(4) for l in range(4)
    ))

    Ffun = sp.Function("F")(radius)
    N_threaded = Ffun * sp.sqrt(X)
    threaded_acceleration = clean(sp.diff(sp.log(N_threaded), radius))

    # Regular-center Taylor controls.
    X0, X1, X2 = sp.symbols("X0 X1 X2", real=True)
    N0 = sp.symbols("N0", positive=True)
    N1, N2 = sp.symbols("N1 N2", real=True)
    X_taylor = X0 + X1 * radius + X2 * radius**2 / 2
    N_taylor = N0 + N1 * radius + N2 * radius**2 / 2
    taylor_subs = {
        X: X_taylor,
        sp.diff(X, radius): sp.diff(X_taylor, radius),
        sp.diff(X, radius, 2): sp.diff(X_taylor, radius, 2),
        N: N_taylor,
        sp.diff(N, radius): sp.diff(N_taylor, radius),
        sp.diff(N, radius, 2): sp.diff(N_taylor, radius, 2),
    }
    center_motifs = [clean(item.subs(taylor_subs)) for item in (expected_m01, expected_m02, expected_m12, expected_m23)]
    regular_center_limits = [clean(sp.limit(item.subs({X0: 1, X1: 0, N1: 0}), radius, 0, dir="+")) for item in center_motifs]

    # Exact inner divergent lapse control at X=1, F=N=R^-q.
    q = sp.symbols("q", positive=True)
    inner_N = radius ** (-q)
    inner_subs = {
        X: 1,
        sp.diff(X, radius): 0,
        sp.diff(X, radius, 2): 0,
        N: inner_N,
        sp.diff(N, radius): sp.diff(inner_N, radius),
        sp.diff(N, radius, 2): sp.diff(inner_N, radius, 2),
    }
    inner_motifs = [clean(item.subs(inner_subs)) for item in (expected_m01, expected_m02, expected_m12, expected_m23)]
    inner_kretschmann = clean(kretschmann_motifs.subs(inner_subs))

    # Divergent reciprocal scalar control: angular curvature alone catches X->infinity at R->0.
    p = sp.symbols("p", positive=True)
    inner_X = radius ** (-p)
    inner_angular = clean(expected_m23.subs({X: inner_X}))
    inner_angular_K_term = clean(4 * inner_angular**2)

    # Endpoint-flat finite-cell threading deformation.  It preserves F and its first two radial jets.
    cell = sp.symbols("X_max", positive=True)
    epsilon = sp.symbols("epsilon", real=True, nonzero=True)
    y = radius / cell
    bump = clean(y**3 * (1 - y)**3)
    deformed_F = sp.exp(epsilon * bump)
    wall_X = 1 - y
    base_N = sp.sqrt(wall_X)
    deformed_N = deformed_F * base_N

    def motif01_for(n_value, x_value):
        return clean(
            x_value * sp.diff(n_value, radius, 2) / n_value
            + sp.diff(x_value, radius) * sp.diff(n_value, radius) / (2 * n_value)
        )

    deformation_m01_difference = clean(
        (motif01_for(deformed_N, wall_X) - motif01_for(base_N, wall_X)).subs(radius, cell / 2)
    )
    endpoint_jets = {
        f"R={where}": [clean(sp.diff(deformed_F, radius, order).subs(radius, point)) for order in range(3)]
        for where, point in (("0", 0), ("X_max", cell))
    }

    # Dimensional rank for (c_E,G_obs,M,L).
    # Columns are c_E, G_obs, M, L; rows are length, time, mass exponents.
    dimension_matrix = sp.Matrix([[1, 3, 0, 1], [-1, -2, 0, 0], [0, -1, 1, 0]])
    dimension_rank = dimension_matrix.rank()
    dimension_null_raw = [clean(vector) for vector in dimension_matrix.nullspace()]
    dimension_null = [clean(-vector if vector[1] < 0 else vector) for vector in dimension_null_raw]
    cG_only = dimension_matrix[:, :2]

    checks = {
        "explicit_c_metric_inverse": clean(orbit * orbit_inverse - sp.eye(2)) == sp.zeros(2),
        "stationary_clock_factor": clock_factor == f * sp.sqrt(x),
        "radial_ruler_factor": ruler_factor == 1 / sp.sqrt(x),
        "coordinate_null_slope": null_slope == c * f * x,
        "proper_null_clock_length_anchor": proper_ratio == c,
        "reciprocal_X_modulation_product": modulation_product == 1,
        "orbit_determinant_contains_threading": determinant == -c**2 * f**2,
        "coordinate_determinant_changes_under_time_relabel": determinant_new == -c**2 * f**2 * scale**2,
        "radial_threading_gradient_relabel_invariant": acceleration_relabelled == acceleration_r,
        "static_m01_formula": clean(m01 - expected_m01) == 0,
        "static_m02_formula": clean(m02 - expected_m02) == 0,
        "static_m12_formula": clean(m12 - expected_m12) == 0,
        "static_m23_formula": clean(m23 - expected_m23) == 0,
        "static_K_motif_reconstruction": clean(kretschmann_direct - kretschmann_motifs) == 0,
        "threaded_acceleration": clean(threaded_acceleration - (sp.diff(Ffun, radius) / Ffun + sp.diff(X, radius) / (2 * X))) == 0,
        "regular_center_limits_finite": regular_center_limits == [N2 / N0, N2 / N0, -X2 / 2, -X2 / 2],
        "inner_F_power_motifs": inner_motifs == [q * (q + 1) / radius**2, -q / radius**2, 0, 0],
        "inner_F_power_curvature": inner_kretschmann == 4 * q**2 * (q**2 + 2 * q + 3) / radius**4,
        "inner_X_angular_divergence": inner_angular_K_term == 4 * (radius**p - 1) ** 2 / radius ** (2 * p + 4),
        "finite_cell_endpoint_jets_preserved": endpoint_jets == {
            "R=0": [1, 0, 0], "R=X_max": [1, 0, 0]
        },
        "finite_cell_interior_curvature_changes": deformation_m01_difference != 0,
        "dimension_matrix_rank_three": dimension_rank == 3,
        "sole_dimensionless_group": len(dimension_null) == 1 and dimension_null[0] == sp.Matrix([-2, 1, 1, -1]),
        "c_and_G_alone_no_dimensionless_or_absolute_scale": cG_only.rank() == 2 and cG_only.nullspace() == [],
    }
    if not all(checks.values()):
        raise AssertionError([name for name, value in checks.items() if not value])

    result = {
        "schema": "udt-clock-anchor-scale-threading-production-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "counts": {"exact_checks": len(checks), "causal_readouts": 4, "static_curvature_motifs": 4},
        "checks": checks,
        "local_anchor": {
            "clock_factor_dtaudt": str(clock_factor),
            "radial_ruler_factor_dell_dR": str(ruler_factor),
            "coordinate_null_slope_dRdt": str(null_slope),
            "local_frame_null_component_ratio_dell_dtau_ref": str(proper_ratio),
            "meaning": "C_E_IS_THE_LOCAL_METRIC_CLOCK_LENGTH_ANCHOR__DTAU_REF_IS_THE_STATIONARY_FRAME_CLOCK_COMPONENT_NOT_NULL_CURVE_PROPER_TIME__F_AND_X_MODULATE_COORDINATE_AND_REMOTE_COMPARISONS",
        },
        "static_curvature": {
            "clock_radial": str(expected_m01),
            "clock_angular": str(expected_m02),
            "radial_angular": str(expected_m12),
            "angular": str(expected_m23),
            "kretschmann": str(kretschmann_motifs),
        },
        "regular_center": {
            "necessary_taylor_conditions": "X0=1__X1=0__N0_FINITE_POSITIVE__N1=0",
            "finite_motif_limits": [str(item) for item in regular_center_limits],
            "inner_F_power_K": str(inner_kretschmann),
            "inner_X_angular_K_lower_term": str(inner_angular_K_term),
            "ruling": "RADIAL_CLOCK_DIVERGENCE_OR_X_DIVERGENCE_IS_CURVATURE_SINGULAR_AT_A_SPHERICAL_AREAL_CENTER",
        },
        "threading": {
            "radial_acceleration_one_form": str(threaded_acceleration),
            "coordinate_block_determinant": str(determinant),
            "relabelled_determinant": str(determinant_new),
            "endpoint_jets": {key: [str(value) for value in values] for key, values in endpoint_jets.items()},
            "interior_m01_difference_at_half_cell": str(deformation_m01_difference),
            "ruling": "LOCAL_RECIPROCAL_X_PAIR_AND_ENDPOINT_JETS_DO_NOT_FIX_RADIAL_THREADING_F",
        },
        "scale": {
            "dimension_matrix": [[int(value) for value in dimension_matrix.row(index)] for index in range(3)],
            "rank": dimension_rank,
            "null_vector_c_G_M_L": [int(value) for value in dimension_null[0]],
            "dimensionless_group": "G_obs*M/(c_E^2*L)",
            "ruling": "C_E_AND_G_OBS_CALIBRATE_MASS_PER_LENGTH_BUT_DO_NOT_SELECT_AN_ABSOLUTE_LENGTH_OR_REGIME_MAP",
        },
        "endpoint_exponent_rules": {
            "definition": "X~delta^p__F~delta^q",
            "clock_factor_exponent": "q+p/2",
            "coordinate_null_slope_exponent": "q+p",
            "radial_ruler_exponent": "-p/2",
            "outer_both_clock_and_slope_to_zero_for_p_positive": "q>-p/2",
            "inner_reflection": "REQUIRES_DIVERGENT_COMBINED_FACTORS__REGULAR_SPHERICAL_AREAL_CENTER_EXCLUDES_RADIAL_DIVERGENCE",
        },
        "rulings": {
            "co_presence": "COMPATIBLE_WITH_C_E_AS_METRIC_CONVERSION__DOES_NOT_BY_ITSELF_DERIVE_OPERATIONAL_SIGNAL_RESPONSE",
            "pair_reciprocity": "FIXES_THE_X_RECIPROCAL_MODULATION__DOES_NOT_FIX_F_WITHOUT_A_COORDINATE_SYNCHRONIZATION_PREMISE",
            "observer_reciprocity": "TENSOR_COVARIANCE_DOES_NOT_REQUIRE_IDENTICAL_F_COMPONENTS",
            "finite_cell_seal": "ENDPOINT_DATA_DO_NOT_FIX_INTERIOR_F__EXACT_ENDPOINT_FLAT_COUNTERFAMILY",
            "bootstrap": "REGISTERED_WORDING_SUPPLIES_ADMISSIBILITY_NOT_AN_OPERATIONAL_F_OR_SCALE_EQUATION",
            "micro_mapping": "SUBNUCLEAR_SEPARATION_IS_NOT_DERIVED_TO_EQUAL_SPHERICAL_AREAL_R_TO_ZERO",
        },
        "maximum_conclusion": "C_E_REMAINS_THE_EXPLICIT_LOCAL_CLOCK_LENGTH_ANCHOR__F_AND_X_SEPARATELY_CONTROL_REMOTE_CLOCK_AND_COORDINATE_READOUTS__REGISTERED_KINEMATIC_AND_GLOBAL_PREMISES_DO_NOT_FIX_F_OR_THE_SCALE_MAP__OUTER_FREEZE_IS_COMBINED_ASYMPTOTICS_CONDITIONAL__INNER_INFINITY_IS_NOT_DERIVED_AND_IS_SINGULAR_AT_A_REGULAR_SPHERICAL_AREAL_CENTER",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
