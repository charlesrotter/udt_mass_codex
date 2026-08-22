#!/usr/bin/env python3
"""Exact symbolic algebra for the G207 trace-free screen robustness tile."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "PRODUCTION_RESULT.json"


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, value: bool) -> None:
        checks[name] = bool(value)
        if not value:
            raise AssertionError(name)

    # Smooth Cartesian, frame-free trace-free screen tensor.
    x, y, z = sp.symbols("x y z", real=True)
    r2 = x**2 + y**2 + z**2
    rho2 = x**2 + y**2
    position = sp.Matrix([x, y, z])
    axis = sp.Matrix([0, 0, 1])
    u = axis.cross(position)
    v = position.cross(u)
    K = sp.simplify(v * v.T - r2 * u * u.T)
    kappa = sp.expand(r2 * rho2)
    check("K_polynomial_symmetric", K == K.T and all(entry.is_polynomial(x, y, z) for entry in K))
    check("u_tangent", sp.simplify((u.T * position)[0]) == 0)
    check("v_tangent", sp.simplify((v.T * position)[0]) == 0)
    check("u_v_orthogonal", sp.simplify((u.T * v)[0]) == 0)
    check("v_norm_relation", sp.simplify((v.T * v)[0] - r2 * (u.T * u)[0]) == 0)
    check("K_radial_kernel", all(sp.simplify(entry) == 0 for entry in K * position))
    check("K_tracefree", sp.simplify(sp.trace(K)) == 0)
    check("K_negative_screen_eigenvector", all(sp.simplify(entry) == 0 for entry in K * u + kappa * u))
    check("K_positive_screen_eigenvector", all(sp.simplify(entry) == 0 for entry in K * v - kappa * v))
    check("K_center_zero", K.subs({x: 0, y: 0, z: 0}) == sp.zeros(3))

    # Exact determinant and signature algebra in an h0-orthogonal eigenframe.
    F, R, P, Q, shear = sp.symbols("F R P Q shear", positive=True)
    g0 = sp.diag(-F, R, P, Q)
    screen_map = sp.diag(1, 1, sp.exp(shear), sp.exp(-shear))
    gS = sp.simplify(screen_map.T * g0 * screen_map)
    check("screen_map_radial_identity", screen_map[1, 1] == 1)
    check("screen_map_positive", screen_map[2, 2].is_positive is True and screen_map[3, 3].is_positive is True)
    check("screen_map_det_one", sp.simplify(screen_map.det() - 1) == 0)
    check("ambient_det_preserved", sp.simplify(gS.det() - g0.det()) == 0)
    check("spatial_principal_entries_positive", all(gS[i, i].is_positive is True for i in (1, 2, 3)))
    check("lorentz_time_entry_negative", (-gS[0, 0]).is_positive is True)

    # The bounded, center-regular time-live witness has screen eigenvalue below one in magnitude.
    r0 = sp.symbols("r0", positive=True)
    bounded_eigenvalue = sp.factor(kappa / (r0**4 + r2**2))
    positive_gap = sp.factor(r0**4 + r2**2 - kappa)
    check("bounded_eigenvalue_nonnegative", bounded_eigenvalue.is_nonnegative is True)
    check("bounded_witness_positive_gap", sp.expand(positive_gap - (r0**4 + r2 * z**2)) == 0)

    # Failure-witness radial profile and exact circular null orbit.
    X = sp.symbols("X", positive=True)
    profile = X**4 * sp.exp(2 * (1 - X**2))
    check("failure_profile_at_orbit", sp.simplify(profile.subs(X, 1) - 1) == 0)
    check("failure_profile_stationary_at_orbit", sp.simplify(sp.diff(profile, X).subs(X, 1)) == 0)

    t, t0, rc, fc, fp, J = sp.symbols("t t0 rc fc fp J", positive=True)
    tau2 = t**2 / t0**2
    gpp = rc**2 * sp.exp(-2 * tau2)
    tdot = J * sp.exp(tau2) / (rc * sp.sqrt(fc))
    phidot = J / gpp
    tddot = sp.diff(tdot, t) * tdot
    gamma_t_pp = sp.diff(gpp, t) / (2 * fc)
    null_norm = -fc * tdot**2 + gpp * phidot**2
    t_residual = sp.simplify(tddot + gamma_t_pp * phidot**2)
    radial_residual = sp.factor(fc * fp * tdot**2 / 2 - fc * rc * sp.exp(-2 * tau2) * phidot**2)
    circular_factor = sp.factor(radial_residual / (J**2 * sp.exp(2 * tau2) / (2 * rc**3)))
    check("failure_orbit_null", sp.simplify(null_norm) == 0)
    check("failure_orbit_t_geodesic", t_residual == 0)
    check("failure_orbit_radial_factor", sp.simplify(circular_factor - (rc * fp - 2 * fc)) == 0)
    check("failure_orbit_radial_geodesic_on_G205_circle", sp.simplify(radial_residual.subs(fp, 2 * fc / rc)) == 0)
    check("failure_orbit_polar_residual", sp.diff(sp.sin(sp.symbols("theta", real=True)) ** 2, sp.symbols("theta", real=True)).subs(sp.symbols("theta", real=True), sp.pi / 2) == 0)
    affine_future = sp.integrate(rc * sp.sqrt(fc) * sp.exp(-tau2) / J, (t, 0, sp.oo))
    affine_expected = sp.sqrt(sp.pi) * rc * sp.sqrt(fc) * t0 / (2 * J)
    check("failure_affine_gaussian_exact", sp.simplify(affine_future - affine_expected) == 0)
    check("failure_affine_future_finite", affine_expected.is_finite is True)

    # Complete pair pullback in a local h0-orthogonal eigenframe.
    alpha0, alpha1 = sp.symbols("alpha0 alpha1", real=True)
    r_0, p_0, q_0, r_1, p_1, q_1 = sp.symbols("r_0 p_0 q_0 r_1 p_1 q_1", real=True)
    Jpair = sp.Matrix(
        [
            [alpha0, alpha1],
            [r_0, r_1],
            [p_0, p_1],
            [q_0, q_1],
        ]
    )
    h_base = sp.simplify(Jpair.T * g0 * Jpair)
    h_shear = sp.simplify(Jpair.T * gS * Jpair)
    clock_base = sp.factor(-h_base[0, 0])
    clock_shear = sp.factor(-h_shear[0, 0])
    expected_clock_shear = sp.factor(
        F * alpha0**2 - R * r_0**2 - P * sp.exp(2 * shear) * p_0**2 - Q * sp.exp(-2 * shear) * q_0**2
    )
    check("pair_pullback_clock_formula", sp.simplify(clock_shear - expected_clock_shear) == 0)
    check("completed_phi_ratio_argument", sp.simplify(clock_shear / clock_base - expected_clock_shear / clock_base) == 0)
    check(
        "static_clock_completed_phi_blind",
        sp.simplify((clock_shear - clock_base).subs({r_0: 0, p_0: 0, q_0: 0})) == 0,
    )
    moving_clock_delta = sp.factor(clock_shear - clock_base)
    check("moving_clock_hears_screen_shear", moving_clock_delta != 0 and moving_clock_delta.has(shear))

    # A concrete regular pair proves that determinant-one ambient shear need not preserve pair area or beta.
    concrete = {
        F: 20,
        R: 2,
        P: 3,
        Q: 5,
        shear: sp.log(2),
        alpha0: 1,
        alpha1: 0,
        r_0: sp.Rational(1, 5),
        p_0: sp.Rational(1, 4),
        q_0: sp.Rational(1, 6),
        r_1: 1,
        p_1: sp.Rational(1, 3),
        q_1: sp.Rational(1, 2),
    }
    hb = sp.simplify(h_base.subs(concrete))
    hs = sp.simplify(h_shear.subs(concrete))
    check("concrete_pair_base_regular", hb[0, 0] < 0 and hb.det() < 0)
    check("concrete_pair_shear_regular", hs[0, 0] < 0 and hs.det() < 0)
    check("pair_area_not_blind", sp.simplify(hs.det() - hb.det()) != 0)
    check("pair_beta_not_blind", sp.simplify(hs[0, 1] / hs[0, 0] - hb[0, 1] / hb[0, 0]) != 0)
    check("completed_phi_not_blind", sp.simplify((-hs[0, 0]) / (-hb[0, 0]) - 1) != 0)

    landing = (
        "TRACEFREE_SCREEN_SHEAR_PRESERVES_AMBIENT_VOLUME_SIGNATURE_RADIAL_CAUSAL_BOUND_AND_G205_GLOBAL_HYPERBOLICITY__"
        "ALL_SMOOTH_STATIC_MEMBERS_AND_COMPACT_TIME_LIVE_WITNESSES_RETAIN_NULL_COMPLETENESS__"
        "UNRESTRICTED_SMOOTH_TIME_LIVE_SHEAR_CAN_AFFINELY_COMPRESS_A_G205_CIRCULAR_NULL_ORBIT_TO_FINITE_LENGTH__"
        "COMPLETED_PAIR_KERNEL_HEARS_SHEAR_EXACTLY_WHEN_THE_SUPPLIED_CLOCK_GERM_HAS_SCREEN_CONTENT__"
        "NO_PHYSICAL_S_HISTORY_OR_XMAX_SELECTION"
    )
    result = {
        "all_pass": all(checks.values()),
        "assertions": len(checks),
        "landing": landing,
        "mechanized_scope": [
            "smooth_frame_free_screen_tensor_algebra",
            "screen_and_ambient_determinant_signature_algebra",
            "bounded_witness_eigenvalue_bound",
            "time_live_circular_null_orbit_and_affine_integral",
            "local_complete_pair_pullback_and_completed_depth_argument",
        ],
        "analytic_theorems_recorded_not_mechanized": [
            "global_hyperbolicity_for_every_smooth_declared_S",
            "null_completeness_for_every_smooth_static_declared_S",
            "null_completeness_for_compact_time_supported_bounded_live_witness",
        ],
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
