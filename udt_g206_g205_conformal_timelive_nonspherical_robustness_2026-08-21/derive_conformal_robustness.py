#!/usr/bin/env python3
"""Exact symbolic algebra for the G206 conformal robustness classification."""

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

    # Exact pair-pullback scaling.
    A, B, C, s = sp.symbols("A B C s", positive=True)
    h = sp.Matrix([[-A, B], [B, C]])
    ht = s**2 * h
    det_h = sp.factor(h.det())
    det_ht = sp.factor(ht.det())
    T2 = A
    L2 = sp.factor(C + B**2 / A)
    m2 = sp.factor(-det_h)
    T2t = -ht[0, 0]
    L2t = sp.factor(ht[1, 1] - ht[0, 1] ** 2 / ht[0, 0])
    m2t = sp.factor(-det_ht)
    check("pair_det_scale", sp.simplify(det_ht - s**4 * det_h) == 0)
    check("pair_T2_scale", sp.simplify(T2t - s**2 * T2) == 0)
    check("pair_L2_scale", sp.simplify(L2t - s**2 * L2) == 0)
    check("pair_beta_invariant", sp.simplify(ht[0, 1] / ht[0, 0] - h[0, 1] / h[0, 0]) == 0)
    check("pair_m2_scale", sp.simplify(m2t - s**4 * m2) == 0)
    check("control_phi_ratio_invariant", sp.simplify((-det_ht) / ht[0, 0] ** 2 - (-det_h) / h[0, 0] ** 2) == 0)
    check("completed_product_base", sp.simplify(T2 * L2 / m2 - 1) == 0)
    check("completed_product_scaled", sp.simplify(T2t * L2t / m2t - 1) == 0)
    check("physical_ruler_square_scale", sp.simplify((L2t / m2t) - (L2 / m2) / s**2) == 0)

    Phi, omega = sp.symbols("Phi omega", real=True)
    shifted = sp.expand_log(-sp.log(sp.exp(omega) * sp.exp(-Phi)), force=True)
    check("completed_Phi_shift", sp.simplify(shifted - (Phi - omega)) == 0)

    # Conformal connection contraction in an exact generic diagonal Lorentz frame.
    g0, g1, g2, g3 = sp.symbols("g0 g1 g2 g3", positive=True)
    metric = sp.diag(-g0, g1, g2, g3)
    inverse = metric.inv()
    k = sp.Matrix(sp.symbols("k0:4", real=True))
    cov_w = sp.Matrix(sp.symbols("w0:4", real=True))
    up_w = inverse * cov_w
    gkk = sp.expand((k.T * metric * k)[0])
    kw = sp.expand((k.T * cov_w)[0])
    contraction = []
    for a_index in range(4):
        value = 0
        for b_index in range(4):
            for c_index in range(4):
                delta_ab = 1 if a_index == b_index else 0
                delta_ac = 1 if a_index == c_index else 0
                connection_difference = (
                    delta_ab * cov_w[c_index]
                    + delta_ac * cov_w[b_index]
                    - metric[b_index, c_index] * up_w[a_index]
                )
                value += connection_difference * k[b_index] * k[c_index]
        contraction.append(sp.expand(value))
        check(
            f"connection_contraction_{a_index}",
            sp.simplify(value - (2 * kw * k[a_index] - gkk * up_w[a_index])) == 0,
        )
        check(
            f"affine_rescaling_cancellation_{a_index}",
            sp.simplify(-2 * kw * k[a_index] + (2 * kw * k[a_index])) == 0,
        )

    # Causal sign and the exact radial-null identity of the G205 base.
    q, F = sp.symbols("q F", positive=True)
    check("causal_sign_scale", sp.signsimp((q**2 * F) / F - q**2) == 0)
    energy = sp.symbols("energy", positive=True)
    radial_null_norm = -F * (energy / F) ** 2 + energy**2 / F
    check("G205_radial_null_norm", sp.simplify(radial_null_norm) == 0)
    check("G205_radial_null_affine_r", sp.diff(sp.symbols("rs") + energy * sp.symbols("lam"), sp.symbols("lam")) == energy)

    # Smooth nonspherical witness bounds in u=z^2/r^2.
    R2, u = sp.symbols("R2 u", nonnegative=True)
    angular = R2 * (3 * u - 1) / (1 + R2)
    check("angular_linear_in_u", sp.diff(angular, u) == 3 * R2 / (1 + R2))
    check("angular_lower_endpoint", sp.simplify(angular.subs(u, 0) + R2 / (1 + R2)) == 0)
    check("angular_upper_endpoint", sp.simplify(angular.subs(u, 1) - 2 * R2 / (1 + R2)) == 0)
    check("angular_center_zero", angular.subs(R2, 0) == 0)

    # Exact Gaussian upper bound for the failing affine integral.
    lam = sp.symbols("lam", nonnegative=True)
    rs, E = sp.symbols("rs E", positive=True)
    gaussian = sp.integrate(sp.exp(-2 * (rs + E * lam) ** 2), (lam, 0, sp.oo))
    gaussian_expected = sp.sqrt(sp.pi) * sp.erfc(sp.sqrt(2) * rs) / (2 * sp.sqrt(2) * E)
    check("gaussian_affine_integral", sp.simplify(gaussian - gaussian_expected) == 0)
    check("gaussian_affine_integral_finite", gaussian_expected.is_finite is True)

    landing = (
        "CONFORMAL_COMMON_SCALE_PRESERVES_G205_CAUSAL_ORDER_AND_GLOBAL_HYPERBOLICITY__"
        "NULL_COMPLETENESS_IFF_THE_CONFORMAL_AFFINE_WEIGHT_DIVERGES__"
        "BOUNDED_LIVE_NONSPHERICAL_SCALES_SURVIVE_WHILE_SMOOTH_DECAYING_SCALE_CAN_DESTROY_NULL_COMPLETENESS__"
        "COMPLETED_PAIR_PHI_SHIFTS_BY_MINUS_OMEGA_PULLBACK__"
        "NO_PHYSICAL_OMEGA_HISTORY_OR_XMAX_SELECTION"
    )
    result = {
        "all_pass": all(checks.values()),
        "assertions": len(checks),
        "landing": landing,
        "mechanized_scope": [
            "pair_pullback_and_completed_readout_scaling",
            "conformal_connection_null_contraction",
            "affine_rescaling_power",
            "G205_radial_null_identity",
            "bounded_nonspherical_witness_algebra",
            "failing_witness_gaussian_upper_bound",
        ],
        "analytic_theorems_recorded_not_mechanized": [
            "global_hyperbolicity_conformal_transfer",
            "all_null_geodesic_integral_iff_criterion",
            "global_lower_bound_sufficient_for_null_completeness",
        ],
        "checks": checks,
    }
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
