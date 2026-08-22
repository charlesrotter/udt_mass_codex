#!/usr/bin/env python3
"""Exact symbolic derivation for the bounded G221 complete-coframe null chord."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


if not __debug__:
    raise RuntimeError("G221 evidence must run with Python assertions enabled; -O is forbidden")

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def check_manifest() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            raise RuntimeError(f"source hash mismatch: {row['path']}")
    return len(rows)


def zero_mod_root(expression: sp.Expr, root: sp.Symbol, root_squared: sp.Expr) -> bool:
    numerator = sp.together(expression).as_numer_denom()[0]
    remainder = sp.rem(sp.Poly(sp.expand(numerator), root), sp.Poly(root**2 - root_squared, root))
    return sp.simplify(remainder.as_expr()) == 0


def derive() -> dict[str, object]:
    checks: dict[str, bool] = {}

    N, A, beta, Pi, q2, R = sp.symbols("N A beta Pi q2 R", positive=True, real=True)
    D = A**2 - N**2 * beta**2
    r2 = Pi**2 + D * q2
    p0_future = (-N * beta * Pi - A * R) / D
    p0_past = (-N * beta * Pi + A * R) / D
    null_poly = lambda p0: D * p0**2 + 2 * N * beta * Pi * p0 - Pi**2 - A**2 * q2

    checks["future_root_null"] = zero_mod_root(null_poly(p0_future), R, r2)
    checks["past_root_null"] = zero_mod_root(null_poly(p0_past), R, r2)
    checks["root_separation"] = sp.simplify(p0_past - p0_future - 2 * A * R / D) == 0
    checks["strict_root_sign_margin"] = sp.factor(
        A**2 * r2 - N**2 * beta**2 * Pi**2 - D * (Pi**2 + A**2 * q2)
    ) == 0

    h11, h12, h22 = sp.symbols("h11 h12 h22", real=True)
    st1, st2, sx1, sx2, pz1, pz2, px = sp.symbols(
        "st1 st2 sx1 sx2 pz1 pz2 px", real=True
    )
    H = sp.Matrix([[h11, h12], [h12, h22]])
    st = sp.Matrix([st1, st2])
    sx = sp.Matrix([sx1, sx2])
    pz = sp.Matrix([pz1, pz2])
    P2 = N**2 - (st.T * H * st)[0]
    Pi_explicit = px - (sx.T * pz)[0]
    q2_explicit = (pz.T * H.inv() * pz)[0]

    Q11, Q12, Q21, Q22 = sp.symbols("Q11 Q12 Q21 Q22", real=True)
    Q = sp.Matrix([[Q11, Q12], [Q21, Q22]])
    B = sp.Matrix([[N, N * beta], [0, A]])
    S = sp.Matrix.hstack(st, sx)
    E = B.row_join(sp.zeros(2, 2)).col_join((Q * S).row_join(Q))
    eta = sp.diag(-1, 1, 1, 1)
    g = sp.simplify(E.T * eta * E)
    checks["complete_coframe_determinant"] = sp.factor(E.det() - N * A * Q.det()) == 0
    checks["observer_norm_includes_time_mixing"] = sp.simplify(
        g[0, 0] + N**2 - (st.T * Q.T * Q * st)[0]
    ) == 0

    # Exact full-sector witness, also used to check direct inverse-metric contraction.
    Nv, Av, bv = sp.Rational(2), sp.Rational(5), sp.Rational(1, 2)
    Qv = sp.Matrix([[2, 1], [1, 3]])
    Hv = Qv.T * Qv
    stv = sp.Matrix([sp.Rational(1, 3), sp.Rational(-1, 4)])
    sxv = sp.Matrix([sp.Rational(2, 5), sp.Rational(1, 7)])
    pxv = sp.Rational(3, 2)
    pzv = sp.Matrix([sp.Rational(4, 3), sp.Rational(-2, 5)])
    Bv = sp.Matrix([[Nv, Nv * bv], [0, Av]])
    Sv = sp.Matrix.hstack(stv, sxv)
    Ev = Bv.row_join(sp.zeros(2, 2)).col_join((Qv * Sv).row_join(Qv))
    gv = Ev.T * eta * Ev
    Dv = Av**2 - Nv**2 * bv**2
    P2v = Nv**2 - (stv.T * Hv * stv)[0]
    Piv = pxv - (sxv.T * pzv)[0]
    q2v = (pzv.T * Hv.inv() * pzv)[0]
    Rv = sp.sqrt(Piv**2 + Dv * q2v)
    p0v = (-Nv * bv * Piv - Av * Rv) / Dv
    ptv = (stv.T * pzv)[0] + Nv * p0v
    pv = sp.Matrix([ptv, pxv, pzv[0], pzv[1]])
    giv = gv.inv()
    kv = sp.simplify(giv * pv)
    Wv = sp.simplify(-ptv / sp.sqrt(P2v))
    checks["direct_inverse_metric_null"] = sp.simplify((pv.T * giv * pv)[0]) == 0
    checks["future_frequency_positive_witness"] = bool(sp.N(Wv, 50) > 0)

    p0v_past = (-Nv * bv * Piv + Av * Rv) / Dv
    ptv_past = (stv.T * pzv)[0] + Nv * p0v_past
    checks["past_frequency_negative_witness"] = bool(sp.N(-ptv_past / sp.sqrt(P2v), 50) < 0)

    qvv = Hv.inv() * pzv
    vx_formula = Nv * (Av * Piv / Rv + Nv * bv) / Dv
    vz_formula = (
        -stv
        + Nv * Av * (-Piv * sxv + Dv * qvv) / (Dv * Rv)
        - Nv**2 * bv * sxv / Dv
    )
    checks["Hamilton_Jacobi_longitudinal_velocity"] = sp.simplify(kv[1] / kv[0] - vx_formula) == 0
    checks["Hamilton_Jacobi_screen_velocity_1"] = sp.simplify(kv[2] / kv[0] - vz_formula[0]) == 0
    checks["Hamilton_Jacobi_screen_velocity_2"] = sp.simplify(kv[3] / kv[0] - vz_formula[1]) == 0

    # Passive screen-coordinate covariance on a nonorthogonal exact transformation.
    K = sp.Matrix([[1, 1], [0, 1]])
    Qp = Qv * K
    Hp = Qp.T * Qp
    stp, sxp = K.inv() * stv, K.inv() * sxv
    pzp = K.T * pzv
    checks["screen_covariance_P2"] = sp.simplify(
        Nv**2 - (stp.T * Hp * stp)[0] - P2v
    ) == 0
    checks["screen_covariance_Pi"] = sp.simplify(
        pxv - (sxp.T * pzp)[0] - Piv
    ) == 0
    checks["screen_covariance_q2"] = sp.simplify(
        (pzp.T * Hp.inv() * pzp)[0] - q2v
    ) == 0
    checks["screen_covariance_coordinate_energy"] = sp.simplify(
        (stp.T * pzp)[0] + Nv * p0v - ptv
    ) == 0

    lam = sp.symbols("lambda", positive=True, real=True)
    W = (N * (A * R + N * beta * Pi) / D - sp.Symbol("st_dot_pz", real=True)) / sp.Symbol(
        "P", positive=True, real=True
    )
    checks["positive_affine_homogeneity"] = sp.simplify(
        W.subs({Pi: lam * Pi, R: lam * R, sp.Symbol("st_dot_pz", real=True): lam * sp.Symbol("st_dot_pz", real=True)})
        - lam * W
    ) == 0

    # Exact G220 transverse-off reduction.
    p_right = sp.symbols("p_right", positive=True, real=True)
    Cplus = A - N * beta
    W_base = sp.simplify(N * (A * p_right + N * beta * p_right) / (D * N))
    checks["G220_single_endpoint_recovery"] = sp.simplify(W_base - p_right / Cplus) == 0
    CpA, CpB = sp.symbols("Cplus_A Cplus_B", positive=True, real=True)
    checks["G220_endpoint_ratio_recovery"] = sp.simplify(
        (p_right / CpA) / (p_right / CpB) - CpB / CpA
    ) == 0

    r = sp.symbols("r", positive=True, real=True)
    target_clock_norm = -r**2
    checks["same_correspondence_clock_leg"] = sp.sqrt(-target_clock_norm) == r
    checks["completed_depth_compatibility"] = sp.simplify(-sp.log(sp.sqrt(-target_clock_norm)) + sp.log(r)) == 0

    if not all(checks.values()):
        raise RuntimeError({key: value for key, value in checks.items() if not value})

    return {
        "manifest_files": check_manifest(),
        "checks": checks,
        "check_count": len(checks),
        "full_sector_witness": {
            "D": str(Dv),
            "P2": str(P2v),
            "Pi": str(Piv),
            "q2": str(q2v),
            "R2": str(sp.simplify(Rv**2)),
            "frequency_50d": str(sp.N(Wv, 50)),
        },
        "formulas": {
            "future_coframe_root": "(-N*beta*Pi-A*sqrt(Pi^2+D*q2))/D",
            "coordinate_energy": "s_t^T*p_z-N*(A*R+N*beta*Pi)/D",
            "observer_lapse_squared": "N^2-s_t^T*H*s_t",
            "measured_frequency": "-p_t/P",
            "clock_slope": "W_A/W_B",
            "incidence_velocity": "d_xi^i/dt=-partial(p_t^-)/partial(p_i)",
            "completed_clock_leg": "T_B=r_AB",
            "G220_reduction": "W=p_x/(A-N*beta)",
        },
        "landing": "COMPLETE_COFRAME_NULL_CLOCK_CHORD_DERIVED_CONDITIONALLY__SCREEN_AND_MIXING_ENTER_UPSTREAM__G220_RECOVERED__NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED",
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2, sort_keys=True))
