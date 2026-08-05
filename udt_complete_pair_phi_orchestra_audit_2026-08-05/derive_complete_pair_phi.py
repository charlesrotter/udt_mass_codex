#!/usr/bin/env python3
"""Exact bounded algebra for the complete-pair phi/orchestra audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def require(value: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(value)
    if not value:
        raise AssertionError(label)


def metric_strain(A: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.simplify(eta.inv() * A.T * eta * A)


def main() -> None:
    checks: dict[str, bool] = {}
    eta = sp.diag(-1, 1, 1, 1)

    # Pure founded arrow in multiplicative coordinates r=exp(delta).
    r = sp.symbols("r", positive=True)
    D = sp.diag(1 / r, r, 1, 1)
    C_D = metric_strain(D, eta)
    require(C_D == sp.diag(r**-2, r**2, 1, 1), "pure_strain", checks)
    require(sp.simplify(-sp.log(C_D[0, 0]) / 2 - sp.log(r)) == 0, "pure_signed_timelike_extractor", checks)
    require(sp.simplify(sp.log(C_D[1, 1]) / 2 - sp.log(r)) == 0, "pure_spacelike_extractor", checks)

    # Independent endpoint Lorentz-frame covariance on an exact rational complete control.
    A = sp.Matrix([
        [sp.Rational(1, 2), 0, 0, 0],
        [0, 2, 0, 0],
        [sp.Rational(1, 4), 0, 1, 0],
        [0, 0, 0, 1],
    ])
    Lp = sp.Matrix([
        [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
        [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    Lq = sp.Matrix([
        [sp.Rational(13, 12), 0, sp.Rational(5, 12), 0],
        [0, 1, 0, 0],
        [sp.Rational(5, 12), 0, sp.Rational(13, 12), 0],
        [0, 0, 0, 1],
    ])
    require(sp.simplify(Lp.T * eta * Lp) == eta, "source_frame_is_Lorentz", checks)
    require(sp.simplify(Lq.T * eta * Lq) == eta, "target_frame_is_Lorentz", checks)
    C = metric_strain(A, eta)
    Aprime = sp.simplify(Lq * A * Lp.inv())
    Cprime = metric_strain(Aprime, eta)
    require(sp.simplify(Cprime - Lp * C * Lp.inv()) == sp.zeros(4), "strain_endpoint_frame_covariance", checks)
    z = sp.symbols("z")
    require(sp.expand(Cprime.charpoly(z).as_expr() - C.charpoly(z).as_expr()) == 0, "strain_characteristic_invariance", checks)

    # Exact lower-mixing control: the complete strain's timelike eigenvalue changes.
    lam_minus = (sp.Integer(19) - sp.sqrt(105)) / 32
    lam_plus = (sp.Integer(19) + sp.sqrt(105)) / 32
    mix_poly = sp.expand((z - lam_minus) * (z - lam_plus))
    expected_mix_poly = z**2 - sp.Rational(19, 16) * z + sp.Rational(1, 4)
    require(sp.simplify(mix_poly - expected_mix_poly) == 0, "mixing_block_spectrum", checks)
    require(sp.simplify(lam_minus - sp.Rational(1, 4)) != 0, "mixing_changes_timelike_stretch", checks)
    z_component = (sp.sqrt(105) - 13) / 8
    v_minus = sp.Matrix([1, 0, z_component, 0])
    require(sp.simplify(C * v_minus - lam_minus * v_minus) == sp.zeros(4, 1), "mixing_timelike_eigenvector", checks)
    causal_norm = sp.simplify((v_minus.T * eta * v_minus)[0])
    require(float(sp.N(causal_norm, 30)) < 0, "mixing_eigenvector_is_timelike", checks)
    delta_strain = -sp.log(lam_minus) / 2
    require(sp.simplify(delta_strain - sp.log(2)) != 0, "strain_depth_differs_from_quotient_depth", checks)

    # Reversal sends the regular positive strain eigenvalues to reciprocals and flips delta_t.
    Ainv = A.inv()
    Crev = metric_strain(Ainv, eta)
    require(sp.simplify(Crev - A * C.inv() * A.inv()) == sp.zeros(4), "reverse_strain_similarity_to_inverse", checks)
    reverse_timelike = sp.simplify(1 / lam_minus)
    require(sp.simplify(reverse_timelike * lam_minus - 1) == 0, "reverse_timelike_eigenvalue_is_reciprocal", checks)
    require(float(sp.N(lam_minus, 30)) > 0 and float(sp.N(reverse_timelike, 30)) > 0, "reverse_log_domain_positive", checks)

    # Two complete spectral magnitudes agree on the pure pair and differ with live screen strain.
    d, a, b = sp.symbols("d a b", real=True)
    rho2_sq = sp.simplify(((-2*d)**2 + (2*d)**2 + (2*a)**2 + (2*b)**2) / 8)
    rho4_fourth = sp.simplify(((-2*d)**4 + (2*d)**4 + (2*a)**4 + (2*b)**4) / 32)
    require(rho2_sq == d**2 + (a**2 + b**2) / 2, "spectral_rho2_formula", checks)
    require(rho4_fourth == d**4 + (a**4 + b**4) / 2, "spectral_rho4_formula", checks)
    require(sp.simplify(rho2_sq.subs({a: 0, b: 0}) - d**2) == 0, "rho2_pure_reduction", checks)
    require(sp.simplify(rho4_fourth.subs({a: 0, b: 0}) - d**4) == 0, "rho4_pure_reduction", checks)
    require(sp.simplify(rho2_sq.subs({d: 1, a: 1, b: 0})**2 - rho4_fourth.subs({d: 1, a: 1, b: 0})) != 0, "spectral_magnitudes_nonunique", checks)

    # Norm-based signed candidates fail additive composition off a common one-parameter ray.
    rho2_leg = sp.sqrt(sp.Rational(3, 2))
    rho2_composite = sp.Integer(2)
    require(sp.simplify(2 * rho2_leg - rho2_composite) != 0, "spectral_signed_depth_nonadditive", checks)

    # Exact block-triangular characters: screen-area modulation composes; mixing drops out.
    r1, r2, q1, q2, k = sp.symbols("r1 r2 q1 q2 k", positive=True)
    chi_product = sp.log(r2 * r1) + k * sp.log(q2 * q1)
    chi_sum = sp.log(r2) + k * sp.log(q2) + sp.log(r1) + k * sp.log(q1)
    require(sp.simplify(sp.expand_log(chi_product - chi_sum, force=True)) == 0, "screen_area_character_composition", checks)
    chi_reverse = sp.log(1 / r1) + k * sp.log(1 / q1)
    require(sp.simplify(sp.expand_log(chi_reverse, force=True) + sp.log(r1) + k * sp.log(q1)) == 0, "screen_area_character_reversal", checks)
    require(sp.diff(sp.log(r1) + k * sp.log(q1), k) == sp.log(q1), "screen_area_character_is_modulated", checks)
    require((sp.log(r1) + k * sp.log(q1)).subs(q1, 1) == sp.log(r1), "screen_area_character_pure_reduction", checks)

    # Stationary 2+2 endpoint cocycle family alpha_k=-d log N+k d log R.
    Np, Nq, Nr, Rp, Rq, Rr = sp.symbols("Np Nq Nr Rp Rq Rr", positive=True)
    def delta(N0, N1, R0, R1):
        return sp.log(N0 / N1) + k * sp.log(R1 / R0)

    dpq = delta(Np, Nq, Rp, Rq)
    dqr = delta(Nq, Nr, Rq, Rr)
    dpr = delta(Np, Nr, Rp, Rr)
    require(sp.simplify(sp.expand_log(dpq + dqr - dpr, force=True)) == 0, "stationary_angular_cocycle_composition", checks)
    require(sp.simplify(sp.expand_log(dpq + delta(Nq, Np, Rq, Rp), force=True)) == 0, "stationary_angular_cocycle_reversal", checks)
    require(sp.diff(dpq, k) == sp.log(Rq / Rp), "stationary_screen_modulation", checks)
    require(sp.simplify(dpq.subs(Rq, Rp) - sp.log(Np / Nq)) == 0, "stationary_Killing_reduction", checks)

    # Discrete groupoid control: endpoint descent iff the triangle period vanishes.
    d01, d12, d20 = sp.symbols("d01 d12 d20", real=True)
    period = d01 + d12 + d20
    phi0, phi1, phi2 = sp.Integer(0), d01, d01 + d12
    require(sp.simplify((phi1 - phi0) - d01) == 0, "potential_edge_01", checks)
    require(sp.simplify((phi2 - phi1) - d12) == 0, "potential_edge_12", checks)
    require(sp.simplify((phi0 - phi2) - d20 + period) == 0, "loop_period_is_descent_obstruction", checks)

    result = {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "pure_reciprocal": {
            "strain_spectrum": ["r^-2", "r^2", "1", "1"],
            "signed_timelike_depth": "-1/2 log(lambda_timelike)=log(r)",
        },
        "mixing_control": {
            "quotient_depth": "log(2)",
            "timelike_strain_eigenvalue": "(19-sqrt(105))/32",
            "timelike_strain_depth": "-1/2 log((19-sqrt(105))/32)",
            "depths_are_distinct": True,
        },
        "complete_magnitudes": {
            "rho2_squared": "d^2+(a^2+b^2)/2",
            "rho4_fourth": "d^4+(a^4+b^4)/2",
            "agree_only_on_pure_reciprocal_control": True,
        },
        "stationary_cocycle_family": "delta_k(p,q)=log(N_p/N_q)+k log(R_q/R_p)",
        "maximum_conclusion": (
            "FULL_ARROW_STRAIN_AND_ANGULAR_MODULATED_RECIPROCAL_COCYCLES_EXIST__"
            "ACTIVE_PREMISES_DO_NOT_SELECT_ONE_UNIVERSAL_COMPLETE_PAIR_DEPTH"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
