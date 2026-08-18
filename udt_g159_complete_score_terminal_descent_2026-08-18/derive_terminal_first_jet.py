#!/usr/bin/env python3
"""Exact G159 descent of the complete coframe score to terminal pair first jets."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "bd2ba87a"
LANDING = (
    "CALIBRATED_PAIR_FIRST_JET_DERIVED__COMPLETE_SCORE_DESCENDS_WITH_DOTJ_LIVE__"
    "H_AND_DOTH_LIVE_LORENTZ_COFRAME_GAUGE_INVARIANT__KAPPA_DENSITY_COEFFICIENT_"
    "AND_PHI_BETA_CEFF_REQUIRE_PAIR_CALIBRATION_CARRY__PHYSICAL_HISTORY_QUERY_"
    "LAMBDA_AND_GLOBAL_COMPLETION_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 7
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 8)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]
    return len(rows)


def terminal_rates(h: sp.Matrix, dh: sp.Matrix) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    kappa_dot = sp.simplify(sp.trace(h.inv() * dh) / 4)
    phi_dot = sp.simplify(kappa_dot - dh[0, 0] / (2 * h[0, 0]))
    beta_dot = sp.simplify(
        (dh[0, 1] * h[0, 0] - h[0, 1] * dh[0, 0]) / h[0, 0] ** 2
    )
    return kappa_dot, phi_dot, beta_dot


def exact_checks() -> dict[str, object]:
    checks: list[str] = []
    eta = sp.diag(-1, 1, 1, 1)

    # Score-to-pair descent with all metric and query change contained in P.
    v = sp.Matrix(4, 2, sp.symbols("v0:8", real=True))
    p = sp.Matrix(4, 2, sp.symbols("p0:8", real=True))
    h_from_v = sp.simplify(v.T * eta * v)
    dh_from_score = sp.simplify(p.T * eta * v + v.T * eta * p)
    assert dh_from_score == dh_from_score.T
    checks.append("complete_score_descends_to_symmetric_pair_first_jet")

    # Generic terminal coefficients, checked by differentiating an independent linear family.
    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True, nonzero=True)
    dh00, dh01, dh11 = sp.symbols("dh00 dh01 dh11", real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    dh = sp.Matrix([[dh00, dh01], [dh01, dh11]])
    kd, pd, bd = terminal_rates(h, dh)
    tt = sp.symbols("tt", real=True)
    ht = h + tt * dh
    kappa_t = sp.log(-ht.det()) / 4
    phi_t = sp.log((-ht.det()) / ht[0, 0] ** 2) / 4
    beta_t = ht[0, 1] / ht[0, 0]
    assert sp.simplify(sp.diff(kappa_t, tt).subs(tt, 0) - kd) == 0
    assert sp.simplify(sp.diff(phi_t, tt).subs(tt, 0) - pd) == 0
    assert sp.simplify(sp.diff(beta_t, tt).subs(tt, 0) - bd) == 0
    checks.append("independent_linear_family_kappa_phi_beta_differentiation")

    ceff_t = -ht[0, 0] / sp.sqrt(-ht.det())
    ceff_log_dot = sp.simplify((sp.diff(ceff_t, tt) / ceff_t).subs(tt, 0))
    assert sp.simplify(ceff_log_dot + 2 * pd) == 0
    checks.append("independent_conditional_ceff_log_rate")

    # Exact live Lorentz coframe-gauge cancellation: boost plus screen rotation.
    th, ps, dth, dps = sp.symbols("th ps dth dps", real=True)
    boost = sp.Matrix([[sp.cosh(th), sp.sinh(th)], [sp.sinh(th), sp.cosh(th)]])
    rotation = sp.Matrix([[sp.cos(ps), -sp.sin(ps)], [sp.sin(ps), sp.cos(ps)]])
    lam = sp.diag(1, 1, 1, 1)
    lam[:2, :2] = boost
    lam[2:, 2:] = rotation
    dlam = sp.diff(lam, th) * dth + sp.diff(lam, ps) * dps
    assert sp.simplify(lam.T * eta * lam - eta) == sp.zeros(4)
    assert sp.simplify(dlam.T * eta * lam + lam.T * eta * dlam) == sp.zeros(4)
    vp = sp.simplify(lam * v)
    pp = sp.simplify(dlam * v + lam * p)
    hp = sp.simplify(vp.T * eta * vp)
    dhp = sp.simplify(pp.T * eta * vp + vp.T * eta * pp)
    assert sp.simplify(hp - h_from_v) == sp.zeros(2)
    assert sp.simplify(dhp - dh_from_score) == sp.zeros(2)
    checks.append("live_lorentz_coframe_gauge_cancels_from_h_and_doth")

    # The inhomogeneous score law itself.
    omega = sp.Matrix(4, 4, sp.symbols("o0:16", real=True))
    omega_prime = sp.simplify(dlam * lam.inv() + lam * omega * lam.inv())
    assert sp.simplify(omega_prime * vp - (dlam * v + lam * omega * v)) == sp.zeros(4, 2)
    checks.append("inhomogeneous_score_gauge_law")

    # Arbitrary live GL+(2) recharting.
    a00, a01, a10, a11 = sp.symbols("a00 a01 a10 a11", real=True)
    da00, da01, da10, da11 = sp.symbols("da00 da01 da10 da11", real=True)
    a = sp.Matrix([[a00, a01], [a10, a11]])
    da = sp.Matrix([[da00, da01], [da10, da11]])
    h_a = sp.simplify(a.T * h * a)
    dh_a = sp.simplify(da.T * h * a + a.T * dh * a + a.T * h * da)
    assert sp.simplify(h_a.det() - a.det() ** 2 * h.det()) == 0
    kd_a, pd_a, bd_a = terminal_rates(h_a, dh_a)
    assert sp.simplify(kd_a - kd - sp.trace(a.inv() * da) / 2) == 0
    clock_norm_log_shift = sp.simplify(
        dh_a[0, 0] / h_a[0, 0] - dh[0, 0] / h[0, 0]
    )
    assert sp.simplify(
        pd_a - pd - sp.trace(a.inv() * da) / 2 + clock_norm_log_shift / 2
    ) == 0
    a0, a1 = a[:, 0], a[:, 1]
    da0, da1 = da[:, 0], da[:, 1]
    beta_num = sp.simplify((a0.T * h * a1)[0])
    beta_den = sp.simplify((a0.T * h * a0)[0])
    beta_num_dot = sp.simplify(
        (da0.T * h * a1 + a0.T * dh * a1 + a0.T * h * da1)[0]
    )
    beta_den_dot = sp.simplify(
        (da0.T * h * a0 + a0.T * dh * a0 + a0.T * h * da0)[0]
    )
    beta_rechart_dot = sp.simplify(
        (beta_num_dot * beta_den - beta_num * beta_den_dot) / beta_den**2
    )
    assert sp.simplify(bd_a - beta_rechart_dot) == 0
    checks.append("arbitrary_live_pair_rechart_density_and_terminal_laws")

    # Positive diagonal clock/ruler recalibration control.
    aa, bb = sp.symbols("aa bb", positive=True)
    daa, dbb = sp.symbols("daa dbb", real=True)
    ad = sp.diag(aa, bb)
    dad = sp.diag(daa, dbb)
    hd = sp.simplify(ad.T * h * ad)
    dhd = sp.simplify(dad.T * h * ad + ad.T * dh * ad + ad.T * h * dad)
    kdd, pdd, bdd = terminal_rates(hd, dhd)
    beta = h01 / h00
    assert sp.simplify(kdd - kd - (daa / aa + dbb / bb) / 2) == 0
    assert sp.simplify(pdd - pd - (dbb / bb - daa / aa) / 2) == 0
    assert sp.simplify(hd[0, 1] / hd[0, 0] - bb * beta / aa) == 0
    assert sp.simplify(
        bdd - bb / aa * (bd + beta * (dbb / bb - daa / aa))
    ) == 0
    ceff_ratio = -h[0, 0] / sp.sqrt(-h.det())
    ceff_ratio_d = -hd[0, 0] / sp.sqrt(-hd.det())
    assert sp.simplify(ceff_ratio_d - aa * ceff_ratio / bb) == 0
    assert sp.simplify(-2 * pdd - (-2 * pd + daa / aa - dbb / bb)) == 0
    checks.append("live_diagonal_clock_ruler_recalibration_control")

    # Query motion is load-bearing even for a fixed identity coframe.
    vw = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    pw = sp.Matrix([[0, 1], [0, 1], [0, 0], [0, 0]])
    hw = sp.simplify(vw.T * eta * vw)
    dhw = sp.simplify(pw.T * eta * vw + vw.T * eta * pw)
    kw, phiw, betaw = terminal_rates(hw, dhw)
    assert hw == sp.diag(-1, 1)
    assert dhw == sp.Matrix([[0, -1], [-1, 2]])
    assert (kw, phiw, betaw) == (sp.Rational(1, 2), sp.Rational(1, 2), 1)
    checks.append("nonzero_query_motion_changes_all_registered_terminal_rates")

    # Fixed A is covariance, not terminal-scalar invariance.
    ac = sp.diag(sp.Integer(2), sp.Integer(3))
    hc = sp.simplify(ac.T * hw * ac)
    assert hc != hw
    assert sp.simplify(sp.Rational(1, 4) * sp.log((-hc.det()) / hc[0, 0] ** 2)
                       - sp.Rational(1, 4) * sp.log((-hw.det()) / hw[0, 0] ** 2)
                       - sp.Rational(1, 2) * sp.log(sp.Rational(3, 2))) == 0
    checks.append("pair_chart_covariance_is_not_terminal_scalar_invariance")

    assert len(checks) == 9
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "terminal_rates": {
            "kappa_dot": "1/4*tr(h^-1*dh)",
            "phi_dot": "1/4*tr(h^-1*dh)-1/2*dh00/h00",
            "beta_dot": "(dh01*h00-h01*dh00)/h00^2",
            "log_ceff_ratio_dot": "-2*phi_dot",
        },
        "query_motion_frozen": False,
        "query_motion_witness": {
            "kappa_dot": "1/2", "phi_dot": "1/2", "beta_dot": "1"
        },
        "h_and_doth_lorentz_coframe_gauge_invariant": True,
        "terminal_coefficients_arbitrary_gl2_invariant": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
        "calibration_carry_derived": False,
    }


def main() -> None:
    result = {
        "status": "PASS",
        "registered_outcome_class": (
            "CALIBRATED_PAIR_FIRST_JET_DERIVED__H_DOTH_LORENTZ_GAUGE_INVARIANT__"
            "TERMINAL_COMPONENTS_REQUIRE_CALIBRATION_CARRY"
        ),
        "landing": LANDING,
        "source_count": verify_manifest(),
        **exact_checks(),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
