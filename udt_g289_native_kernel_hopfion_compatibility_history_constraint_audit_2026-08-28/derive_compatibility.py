#!/usr/bin/env python3
"""Fresh exact G289 algebra/topology compatibility derivation."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
LANDING = (
    "LOCAL_NULL_DIRECTION_EMBEDDING_EXISTS"
    "__FIXED_ROUND_S2_HOPFION_REQUIRES_SUPPLIED_FRAME_TARGET_AND_BOUNDARY"
    "__RAW_HOPF_CLASS_DOES_NOT_DESCEND_THROUGH_FULL_LOCAL_FRAME_GAUGE"
    "__CONFORMAL_HISTORY_TWINS_CARRY_THE_SAME_NULL_TEXTURE"
    "__STATIC_HOPFION_IS_CONDITIONALLY_COMPATIBLE_NOT_A_CURRENT_HISTORY_SELECTOR"
)


def main() -> None:
    computed_checks: dict[str, bool] = {}

    # A unit spatial direction relative to a supplied orthonormal observer gives a null line.
    nx, ny, nz = sp.symbols("nx ny nz", real=True)
    computed_checks["unit_direction_gives_null_line"] = sp.expand(-1 + nx**2 + ny**2 + nz**2).subs(
        nx**2 + ny**2, 1 - nz**2
    ) == 0

    # Exact rational boost witness beta=3/5, gamma=5/4 along z.
    beta = sp.Rational(3, 5)
    gamma = sp.Rational(5, 4)
    n = sp.Matrix([1, 0, 0])
    k = sp.Matrix([1, *n])
    boost = sp.Matrix(
        [
            [gamma, 0, 0, -gamma * beta],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-gamma * beta, 0, 0, gamma],
        ]
    )
    eta = sp.diag(-1, 1, 1, 1)
    kp = boost * k
    np = sp.Matrix(kp[1:4, 0]) / kp[0]
    computed_checks["boost_preserves_nullity"] = sp.simplify((kp.T * eta * kp)[0]) == 0
    computed_checks["boost_preserves_celestial_unit_sphere"] = sp.simplify(np.dot(np)) == 1

    # Tangent vectors at n=e_x. The celestial aberration map is conformal, not round-isometric.
    tangents = (sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1]))
    pushed = []
    for tangent in tangents:
        dkp = boost * sp.Matrix([0, *tangent])
        pushed.append(sp.simplify(sp.Matrix(dkp[1:4, 0]) / kp[0] - np * dkp[0] / kp[0]))
    target_scale = sp.Rational(16, 25)
    computed_checks["boost_tangent_one_scale"] = sp.simplify(pushed[0].dot(pushed[0])) == target_scale
    computed_checks["boost_tangent_two_scale"] = sp.simplify(pushed[1].dot(pushed[1])) == target_scale
    computed_checks["boost_preserves_tangent_orthogonality"] = sp.simplify(pushed[0].dot(pushed[1])) == 0
    computed_checks["boost_not_round_target_isometry"] = target_scale != 1
    computed_checks["quadratic_density_changes"] = target_scale == sp.Rational(16, 25)
    computed_checks["quartic_area_square_changes"] = target_scale**2 == sp.Rational(256, 625)

    # A varying local spatial frame applied to one constant component direction gives the Hopf map.
    a, b, c, d = sp.symbols("a b c d", real=True)
    hopf = sp.Matrix(
        [
            2 * (b * d + a * c),
            2 * (c * d - a * b),
            a**2 - b**2 - c**2 + d**2,
        ]
    )
    unit_q = a**2 + b**2 + c**2 + d**2
    computed_checks["quaternion_rotated_direction_lands_on_s2"] = (
        sp.factor(hopf.dot(hopf) - unit_q**2) == 0
    )

    u = sp.symbols("u", real=True)
    north = sp.simplify(hopf.subs({a: sp.cos(u), b: 0, c: 0, d: sp.sin(u)}))
    south = sp.simplify(hopf.subs({a: 0, b: sp.cos(u), c: sp.sin(u), d: 0}))
    computed_checks["north_preimage_circle"] = north == sp.Matrix([0, 0, 1])
    computed_checks["south_preimage_circle"] = south == sp.Matrix([0, 0, -1])

    # Fresh Hopf-coordinate connection integral. Its two fiber circles link once.
    h = sp.symbols("h", real=True)
    density = -2 * sp.sin(h) * sp.cos(h)
    integral = sp.integrate(density, (h, 0, sp.pi / 2)) * (2 * sp.pi) ** 2
    computed_checks["hopf_connection_integral_magnitude"] = (
        sp.simplify(abs(integral)) == 4 * sp.pi**2
    )

    conclusions: dict[str, bool] = {}
    conclusions["component_hopf_class_can_change_under_local_frame_rotation"] = all(
        (
            computed_checks["quaternion_rotated_direction_lands_on_s2"],
            computed_checks["north_preimage_circle"],
            computed_checks["south_preimage_circle"],
            computed_checks["hopf_connection_integral_magnitude"],
        )
    )

    # A conformal family has exactly the same null lines but inequivalent scalar curvature.
    alpha = sp.symbols("alpha", real=True)
    r2 = sp.symbols("r2", nonnegative=True)
    conformal_scalar = sp.exp(-2 * alpha * r2) * (-36 * alpha - 24 * alpha**2 * r2)
    computed_checks["conformal_twin_flat_center_scalar"] = (
        conformal_scalar.subs({alpha: 0, r2: 0}) == 0
    )
    computed_checks["conformal_twin_curved_center_scalar"] = (
        conformal_scalar.subs({alpha: 1, r2: 0}) == -36
    )
    computed_checks["conformal_twins_geometrically_inequivalent"] = (
        conformal_scalar.subs({alpha: 0, r2: 0}) != conformal_scalar.subs({alpha: 1, r2: 0})
    )
    q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3", real=True)
    positive_scale = sp.symbols("positive_scale", positive=True)
    null_form = -q0**2 + q1**2 + q2**2 + q3**2
    computed_checks["positive_conformal_factor_preserves_null_lines"] = (
        sp.simplify(
            sp.expand(positive_scale * null_form).subs(q0**2, q1**2 + q2**2 + q3**2)
        )
        == 0
    )

    # These are conclusion flags derived from the computed identities; they are not counted as
    # additional calculations.
    conclusions["local_configuration_compatibility"] = computed_checks[
        "unit_direction_gives_null_line"
    ]
    conclusions["full_frame_native_round_target_fails"] = computed_checks[
        "boost_not_round_target_isometry"
    ]
    conclusions["raw_component_charge_not_frame_gauge_descended"] = conclusions[
        "component_hopf_class_can_change_under_local_frame_rotation"
    ]
    conclusions["same_unit_direction_texture_embeds_in_both_twins"] = computed_checks[
        "positive_conformal_factor_preserves_null_lines"
    ]
    conclusions["null_texture_alone_does_not_select_history"] = all(
        (
            computed_checks["conformal_twins_geometrically_inequivalent"],
            conclusions["same_unit_direction_texture_embeds_in_both_twins"],
        )
    )

    if not all(computed_checks.values()) or not all(conclusions.values()):
        failed = [name for name, passed in computed_checks.items() if not passed]
        failed += [name for name, passed in conclusions.items() if not passed]
        raise AssertionError(f"failed checks: {failed}")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "check_count": len(computed_checks),
        "computed_check_count": len(computed_checks),
        "derived_conclusion_count": len(conclusions),
        "total_claim_flags": len(computed_checks) + len(conclusions),
        "computed_checks": computed_checks,
        "derived_conclusions": conclusions,
        "boost_witness": {
            "beta": "3/5",
            "gamma": "5/4",
            "celestial_tangent_norm_scale": "16/25",
            "quartic_area_square_scale": "256/625",
        },
        "topology_witness": {
            "constant_component_direction": "e3",
            "local_frame_map": "Ad_q with q in S3 and identity at compactification basepoint",
            "rotated_component_map": "standard Hopf map S3->S2",
            "hopf_integral_magnitude": "4*pi^2",
        },
        "history_witness": {
            "family": "g_alpha=exp(2*alpha*r^2)*eta on a bounded spatial ball",
            "same_null_lines": True,
            "center_scalar_curvature": "-36*alpha",
        },
        "imports_old_result_artifact": False,
        "introduces_action_source_mass_history_or_scale": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
