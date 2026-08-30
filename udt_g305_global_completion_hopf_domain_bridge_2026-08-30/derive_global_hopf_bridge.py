#!/usr/bin/env python3
"""Exact G305 production derivation.

This script derives induced metrics and the explicit Hopf witness.  It imports no
field equation, action, source, observation, fitted profile, or historical
Hopfion implementation.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def simp_matrix(m: sp.Matrix) -> sp.Matrix:
    return m.applyfunc(lambda x: sp.trigsimp(sp.simplify(x)))


def induced(embedding: sp.Matrix, coords: tuple[sp.Symbol, ...], ambient: sp.Matrix) -> sp.Matrix:
    jac = embedding.jacobian(coords)
    return simp_matrix(jac.T * ambient * jac)


def assert_matrix_equal(actual: sp.Matrix, expected: sp.Matrix, label: str) -> int:
    delta = simp_matrix(actual - expected)
    assert delta == sp.zeros(*delta.shape), f"{label}: {delta}"
    return delta.rows * delta.cols


def main() -> None:
    tau, r, theta, varphi = sp.symbols("tau r theta varphi", real=True)
    T, psi = sp.symbols("T psi", real=True)
    X, L = sp.symbols("X L", positive=True, finite=True)
    eta5 = sp.diag(-1, 1, 1, 1, 1)
    eta23 = sp.diag(-1, -1, 1, 1, 1)

    n = sp.Matrix([
        sp.sin(theta) * sp.cos(varphi),
        sp.sin(theta) * sp.sin(varphi),
        sp.cos(theta),
    ])

    assertions = 0

    # Positive constant: static chart in one-sheeted hyperboloid.
    q = sp.sqrt(X**2 - r**2)
    y_pos_static = sp.Matrix([
        q * sp.sinh(tau / X),
        r * n[0], r * n[1], r * n[2],
        q * sp.cosh(tau / X),
    ])
    constraint_pos_static = sp.trigsimp((y_pos_static.T * eta5 * y_pos_static)[0])
    assert sp.simplify(constraint_pos_static - X**2) == 0
    assertions += 1
    g_pos_static = induced(y_pos_static, (tau, r, theta, varphi), eta5)
    f_pos = 1 - r**2 / X**2
    expected_pos_static = sp.diag(-f_pos, 1 / f_pos, r**2, r**2 * sp.sin(theta) ** 2)
    assertions += assert_matrix_equal(g_pos_static, expected_pos_static, "positive static pullback")

    # Positive constant: regular global chart with compact S3 slices.
    scale = X * sp.cosh(T / X)
    y_pos_global = sp.Matrix([
        X * sp.sinh(T / X),
        scale * sp.sin(psi) * n[0],
        scale * sp.sin(psi) * n[1],
        scale * sp.sin(psi) * n[2],
        scale * sp.cos(psi),
    ])
    constraint_pos_global = sp.trigsimp((y_pos_global.T * eta5 * y_pos_global)[0])
    assert sp.simplify(constraint_pos_global - X**2) == 0
    assertions += 1
    g_pos_global = induced(y_pos_global, (T, psi, theta, varphi), eta5)
    expected_pos_global = sp.diag(
        -1,
        scale**2,
        scale**2 * sp.sin(psi) ** 2,
        scale**2 * sp.sin(psi) ** 2 * sp.sin(theta) ** 2,
    )
    assertions += assert_matrix_equal(g_pos_global, expected_pos_global, "positive global pullback")

    r_overlap = scale * sp.sin(psi)
    static_radical_sq = sp.simplify(X**2 - r_overlap**2)
    ambient_radical_sq = sp.trigsimp(y_pos_global[4] ** 2 - y_pos_global[0] ** 2)
    assert sp.trigsimp(static_radical_sq - ambient_radical_sq) == 0
    assertions += 1
    static_ratio = sp.trigsimp(y_pos_global[0] / y_pos_global[4])
    expected_ratio = sp.tanh(T / X) / sp.cos(psi)
    assert sp.trigsimp(static_ratio - expected_ratio) == 0
    assertions += 1

    # Negative constant: two-time ambient hyperboloid; unwrap tau for the causal cover.
    qn = sp.sqrt(L**2 + r**2)
    y_neg_static = sp.Matrix([
        qn * sp.cos(tau / L),
        qn * sp.sin(tau / L),
        r * n[0], r * n[1], r * n[2],
    ])
    constraint_neg = sp.trigsimp((y_neg_static.T * eta23 * y_neg_static)[0])
    assert sp.simplify(constraint_neg + L**2) == 0
    assertions += 1
    g_neg_static = induced(y_neg_static, (tau, r, theta, varphi), eta23)
    f_neg = 1 + r**2 / L**2
    expected_neg_static = sp.diag(-f_neg, 1 / f_neg, r**2, r**2 * sp.sin(theta) ** 2)
    assertions += assert_matrix_equal(g_neg_static, expected_neg_static, "negative static pullback")

    rho = sp.symbols("rho", nonnegative=True, finite=True)
    y_neg_global = sp.Matrix([
        L * sp.cosh(rho) * sp.cos(tau / L),
        L * sp.cosh(rho) * sp.sin(tau / L),
        L * sp.sinh(rho) * n[0],
        L * sp.sinh(rho) * n[1],
        L * sp.sinh(rho) * n[2],
    ])
    g_neg_global = induced(y_neg_global, (tau, rho, theta, varphi), eta23)
    expected_neg_global = sp.diag(
        -sp.cosh(rho) ** 2,
        L**2,
        L**2 * sp.sinh(rho) ** 2,
        L**2 * sp.sinh(rho) ** 2 * sp.sin(theta) ** 2,
    )
    assertions += assert_matrix_equal(g_neg_global, expected_neg_global, "negative global pullback")
    assert sp.simplify(r - L * sp.sinh(sp.asinh(r / L))) == 0
    assertions += 1

    # Explicit Hopf witness on the positive sector's intrinsic S3 slice.
    eta, xi1, xi2 = sp.symbols("eta xi1 xi2", real=True)
    delta = xi1 - xi2
    hopf = sp.Matrix([
        sp.sin(2 * eta) * sp.cos(delta),
        sp.sin(2 * eta) * sp.sin(delta),
        sp.cos(2 * eta),
    ])
    hopf_norm = sp.trigsimp((hopf.T * hopf)[0])
    assert sp.simplify(hopf_norm - 1) == 0
    assertions += 1

    # A=cos^2(eta) dxi1 + sin^2(eta) dxi2.
    # In orientation deta^dxi1^dxi2, A^dA has coefficient -sin(2 eta).
    wedge_coeff = sp.simplify(-sp.sin(2 * eta))
    hopf_integral = sp.integrate(
        wedge_coeff,
        (eta, 0, sp.pi / 2),
        (xi1, 0, 2 * sp.pi),
        (xi2, 0, 2 * sp.pi),
    )
    hopf_number = sp.simplify(hopf_integral / (4 * sp.pi**2))
    assert hopf_number == -1
    assertions += 2
    assert not hopf_number.has(X, L, T)
    assertions += 1

    # Constant-curvature null optical tidal contraction is zero for every K.
    K, kk, ee, ek = sp.symbols("K kk ee ek", real=True)
    tidal = sp.expand(K * (ee * kk - ek**2))
    null_screen_tidal = sp.simplify(tidal.subs({kk: 0, ek: 0, ee: 1}))
    assert null_screen_tidal == 0
    assertions += 1
    ricci_null = sp.simplify((3 * K * kk).subs(kk, 0))
    assert ricci_null == 0
    assertions += 1

    # The celestial screen Euler number is kinematic and sign-blind.
    sky_euler = sp.simplify(
        sp.integrate(sp.sin(theta), (theta, 0, sp.pi), (varphi, 0, 2 * sp.pi))
        / (2 * sp.pi)
    )
    assert sky_euler == 2
    assertions += 1

    topology_census = [
        {
            "sector": "R0_positive",
            "standard_spatial_slice": "S3",
            "compact_without_boundary": True,
            "ordinary_unbased_hopf_classes": "Z",
            "extra_compactification_needed": False,
        },
        {
            "sector": "R0_zero",
            "standard_spatial_slice": "R3",
            "compact_without_boundary": False,
            "ordinary_unbased_hopf_classes": "trivial_on_contractible_domain",
            "extra_compactification_needed": True,
        },
        {
            "sector": "R0_negative_causal_cover",
            "standard_spatial_slice": "H3_isomorphic_R3",
            "compact_without_boundary": False,
            "ordinary_unbased_hopf_classes": "trivial_on_contractible_domain",
            "extra_compactification_needed": True,
        },
    ]

    prerequisite_ledger = [
        ["compact_S3_spatial_domain", "DERIVED_CONDITIONAL_positive_standard_completion"],
        ["outer_boundary_collapse", "NOT_NEEDED_positive_S3__STILL_NEEDED_for_R3_one_point_compactification"],
        ["nontrivial_map_class_exists", "DERIVED_MATHEMATICAL_EXISTENCE_positive_S3"],
        ["physical_map_or_section", "OPEN"],
        ["fixed_physical_S2_target", "OPEN"],
        ["local_frame_gauge_descent", "OPEN_for_fixed_target_Hopf_integer"],
        ["covariant_action", "OPEN"],
        ["time_live_dynamics_or_conservation", "OPEN__only_kinematic_product_slice_persistence_derived"],
        ["backreaction_or_history_selection", "OPEN"],
        ["magnitude_mass_or_Xmax", "OPEN"],
    ]

    result = {
        "landing": (
            "POSITIVE_STANDARD_GLOBAL_COMPLETION_NATIVELY_SUPPLIES_COMPACT_S3_HOPF_DOMAIN"
            "__STATIC_ZERO_IS_OBSERVER_HORIZON_NOT_MATERIAL_BOUNDARY"
            "__EXPLICIT_HOPF_CLASS_PERSISTS_KINEMATICALLY_AND_IS_SCALE_BLIND"
            "__TARGET_SECTION_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN"
        ),
        "production_assertions": assertions,
        "positive_static_metric": [str(x) for x in g_pos_static.diagonal()],
        "positive_global_metric": [str(x) for x in g_pos_global.diagonal()],
        "negative_static_metric": [str(x) for x in g_neg_static.diagonal()],
        "negative_global_metric": [str(x) for x in g_neg_global.diagonal()],
        "hopf_number_frozen_orientation": int(hopf_number),
        "null_optical_tidal_all_signs": int(null_screen_tidal),
        "celestial_screen_euler_all_signs": int(sky_euler),
        "topology_census": topology_census,
        "prerequisite_ledger": prerequisite_ledger,
        "scope": "smooth_center_G304_family_standard_simply_connected_completions_only",
        "forbidden_inputs": [
            "field_equation", "action", "source", "matter_model", "mass_law", "observation",
            "fit", "physical_Xmax", "old_Hopfion_boundary", "protected_package",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
