#!/usr/bin/env python3
"""Exact G160 three-observer time-live pair-first-jet carry derivation."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
SOURCE_SNAPSHOT = "4a89d922"
LANDING = (
    "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_PULLBACK_AND_"
    "RIGHT_CONNECTION_COMPOSITION_EXACT__CARRY_CLOSURE_SUFFICIENT_NOT_"
    "NECESSARY_DUE_TO_LORENTZ_STABILIZER__ONLY_COMBINED_CARRIED_FIRST_JET_"
    "IS_LIVE_SOURCE_GAUGE_COVARIANT__JOINED_TOTAL_RATE_IS_LIVE_ENDPOINT_"
    "GAUGE_INVARIANT__KAPPA_HAS_UNIVERSAL_"
    "DETERMINANT_RATE__NO_PHI_BETA_CARRY_ONLY_LAW_ON_UNRESTRICTED_GLPLUS2__"
    "BPLUS2_SUFFICIENT_NOT_NECESSARY_FOR_EXACT_CHARACTER_LAWS__SCALAR_RATE_"
    "CLOSURE_WEAKER_THAN_MATRIX_RATE_CLOSURE__PHYSICAL_"
    "CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 10
    assert [row["source_id"] for row in rows] == [f"S{i:02d}" for i in range(1, 11)]
    for row in rows:
        payload = subprocess.run(
            ["git", "show", f"{SOURCE_SNAPSHOT}:{row['path']}"],
            cwd=ROOT, check=True, stdout=subprocess.PIPE,
        ).stdout
        assert len(payload) == int(row["bytes"]), row["source_id"]
        assert hashlib.sha256(payload).hexdigest() == row["sha256"], row["source_id"]
    return len(rows)


def matrix_symbols(prefix: str, rows: int = 2, cols: int = 2) -> sp.Matrix:
    return sp.Matrix(rows, cols, sp.symbols(f"{prefix}0:{rows * cols}", real=True))


def assert_zero(value: sp.Matrix | sp.Expr) -> None:
    if isinstance(value, sp.MatrixBase):
        assert all(sp.factor(sp.cancel(entry)) == 0 for entry in value)
    else:
        assert sp.factor(sp.cancel(value)) == 0


def pull_first_jet(h: sp.Matrix, dh: sp.Matrix, m: sp.Matrix, dm: sp.Matrix):
    hbar = m.T * h * m
    dhbar = dm.T * h * m + m.T * dh * m + m.T * h * dm
    return hbar, dhbar


def terminal_rates(h: sp.Matrix, dh: sp.Matrix):
    det = h.det()
    det_dot = (
        dh[0, 0] * h[1, 1] + h[0, 0] * dh[1, 1]
        - 2 * h[0, 1] * dh[0, 1]
    )
    kd = sp.cancel(det_dot / (4 * det))
    pd = sp.cancel(kd - dh[0, 0] / (2 * h[0, 0]))
    bd = sp.cancel((dh[0, 1] * h[0, 0] - h[0, 1] * dh[0, 0]) / h[0, 0] ** 2)
    return kd, pd, bd


def exact_checks() -> dict[str, object]:
    checks: list[str] = []

    h00, h01, h11 = sp.symbols("h00 h01 h11", real=True)
    d00, d01, d11 = sp.symbols("d00 d01 d11", real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    dh = sp.Matrix([[d00, d01], [d01, d11]])
    m, dm = matrix_symbols("m"), matrix_symbols("dm")
    k = dm * m.inv()
    hbar, dhbar = pull_first_jet(h, dh, m, dm)

    # One-carry tensor/connection law.
    assert_zero(dhbar - m.T * (dh + k.T * h + h * k) * m)
    checks.append("general_glplus2_pullback_first_jet_connection_law")

    # Only the h-self-adjoint part of K reaches the carried metric first jet.
    kdag = h.inv() * k.T * h
    sym_h = (k + kdag) / 2
    assert_zero(k.T * h + h * k - 2 * h * sym_h)
    raw = matrix_symbols("raw")
    skew_h = (raw - h.inv() * raw.T * h) / 2
    assert_zero(skew_h.T * h + h * skew_h)
    checks.append("metric_self_adjoint_carry_rate_only_reaches_doth")

    # Three-observer staged/direct equality and right-rate composition.
    mba, dmba = matrix_symbols("mba"), matrix_symbols("dmba")
    mcb, dmcb = matrix_symbols("mcb"), matrix_symbols("dmcb")
    mca = mcb * mba
    dmca = dmcb * mba + mcb * dmba
    hb, dhb = pull_first_jet(h, dh, mcb, dmcb)
    h_staged, dh_staged = pull_first_jet(hb, dhb, mba, dmba)
    h_direct, dh_direct = pull_first_jet(h, dh, mca, dmca)
    assert_zero(h_staged - h_direct)
    assert_zero(dh_staged - dh_direct)
    kba, kcb, kca = dmba * mba.inv(), dmcb * mcb.inv(), dmca * mca.inv()
    assert_zero(kca - kcb - mcb * kba * mcb.inv())
    checks.append("closed_three_observer_staged_direct_and_right_rate_composition")

    # The pair first jet is not a faithful detector of carry closure. A nonidentity
    # Lorentz stabilizer can differ from the staged carry while preserving (h, dh),
    # and an infinitesimal h-skew rate can be nonzero while contributing zero dh.
    eta = sp.diag(-1, 1)
    lorentz = sp.Matrix([[sp.Rational(5, 3), sp.Rational(4, 3)],
                         [sp.Rational(4, 3), sp.Rational(5, 3)]])
    assert lorentz != sp.eye(2)
    assert_zero(lorentz.T * eta * lorentz - eta)
    boost_rate = sp.Matrix([[0, 1], [1, 0]])
    assert boost_rate != sp.zeros(2)
    assert_zero(boost_rate.T * eta + eta * boost_rate)
    checks.append("pair_first_jet_nonfaithful_to_finite_and_rate_carry_closure")

    # Independently supplied direct route: finite and first-order defect law.
    mca_free, dmca_free = matrix_symbols("mcaf"), matrix_symbols("dmcaf")
    defect = mcb * mba * mca_free.inv()
    ddefect = (
        dmcb * mba * mca_free.inv()
        + mcb * dmba * mca_free.inv()
        - defect * dmca_free * mca_free.inv()
    )
    kdefect = ddefect * defect.inv()
    kca_free = dmca_free * mca_free.inv()
    predicted = kcb + mcb * kba * mcb.inv() - defect * kca_free * defect.inv()
    assert_zero(kdefect - predicted)
    checks.append("finite_direct_route_defect_right_rate_law")

    # Live independent endpoint gauges: target gauge cancels; source gauge remains covariantly.
    pa, dpa = matrix_symbols("pa"), matrix_symbols("dpa")
    pb, dpb = matrix_symbols("pb"), matrix_symbols("dpb")
    hp = pb.T * h * pb
    dhp = dpb.T * h * pb + pb.T * dh * pb + pb.T * h * dpb
    mp = pb.inv() * m * pa
    dmp = (
        -pb.inv() * dpb * pb.inv() * m * pa
        + pb.inv() * dm * pa
        + pb.inv() * m * dpa
    )
    hbarp, dhbarp = pull_first_jet(hp, dhp, mp, dmp)
    assert_zero(hbarp - pa.T * hbar * pa)
    assert_zero(dhbarp - (dpa.T * hbar * pa + pa.T * dhbar * pa + pa.T * hbar * dpa))
    checks.append("live_endpoint_gauge_covariance_of_combined_carried_first_jet")

    # Universal common-scale density-rate character; general phi/beta retain clock-column data.
    kd, pd, bd = terminal_rates(h, dh)
    kdb, pdb, bdb = terminal_rates(hbar, dhbar)
    assert_zero(kdb - kd - sp.trace(k) / 2)
    m0, m1 = m[:, 0], m[:, 1]
    dm0, dm1 = dm[:, 0], dm[:, 1]
    n = (m0.T * h * m1)[0]
    d = (m0.T * h * m0)[0]
    ndot = (dm0.T * h * m1 + m0.T * dh * m1 + m0.T * h * dm1)[0]
    ddot = (dm0.T * h * m0 + m0.T * dh * m0 + m0.T * h * dm0)[0]
    assert_zero(bdb - (ndot * d - n * ddot) / d**2)
    clock_shift = dhbar[0, 0] / hbar[0, 0] - dh[0, 0] / h[0, 0]
    assert_zero(pdb - pd - sp.trace(k) / 2 + clock_shift / 2)
    checks.append("general_terminal_rate_and_clock_flag_boundary")

    # Same non-flag-preserving carry gives history-dependent phi/beta shifts: no carry-only law.
    mlower = sp.Matrix([[1, 0], [sp.Rational(1, 2), 1]])
    hflat = sp.diag(-1, 1)
    hscaled = sp.diag(-4, 1)
    flatbar = mlower.T * hflat * mlower
    scaledbar = mlower.T * hscaled * mlower
    flat_clock_ratio = sp.cancel((-flatbar[0, 0]) / (-hflat[0, 0]))
    scaled_clock_ratio = sp.cancel((-scaledbar[0, 0]) / (-hscaled[0, 0]))
    assert flat_clock_ratio == sp.Rational(3, 4)
    assert scaled_clock_ratio == sp.Rational(15, 16)
    assert flat_clock_ratio != scaled_clock_ratio
    assert sp.cancel(flatbar[0, 1] / flatbar[0, 0]) != sp.cancel(
        scaledbar[0, 1] / scaledbar[0, 0]
    )
    checks.append("general_glplus2_phi_beta_shift_not_carry_only_counterwitness")

    # Exact flag-preserving B+(2) terminal characters and normalized shift.
    t, ell, beta = sp.symbols("t ell beta", positive=True)
    dt, dell, dbeta = sp.symbols("dt dell dbeta", real=True)
    aa, bb, dd = sp.symbols("aa bb dd", positive=True)
    daa, dbb, ddd = sp.symbols("daa dbb ddd", real=True)
    rfac = sp.Matrix([[t, t * beta], [0, ell]])
    drfac = sp.Matrix([[dt, dt * beta + t * dbeta], [0, dell]])
    mt = sp.Matrix([[aa, bb], [0, dd]])
    dmt = sp.Matrix([[daa, dbb], [0, ddd]])
    kt = dmt * mt.inv()
    product, dproduct = rfac * mt, drfac * mt + rfac * dmt
    tbar, lbar = product[0, 0], product[1, 1]
    betabar = sp.cancel(product[0, 1] / product[0, 0])
    dtbar, dlbar = dproduct[0, 0], dproduct[1, 1]
    dbetabar = sp.cancel(
        (dproduct[0, 1] * product[0, 0] - product[0, 1] * dproduct[0, 0])
        / product[0, 0] ** 2
    )
    kappadot, phidot = (dt / t + dell / ell) / 2, (dell / ell - dt / t) / 2
    kappadot_bar = (dtbar / tbar + dlbar / lbar) / 2
    phidot_bar = (dlbar / lbar - dtbar / tbar) / 2
    ratio, shift = dd / aa, bb / aa
    assert_zero(kappadot_bar - kappadot - sp.trace(kt) / 2)
    assert_zero(phidot_bar - phidot - (kt[1, 1] - kt[0, 0]) / 2)
    assert_zero(betabar - shift - ratio * beta)
    assert_zero(dbetabar - ratio * (dbeta + kt[0, 1] + (kt[1, 1] - kt[0, 0]) * beta))
    checks.append("bplus2_kappa_phi_beta_and_conditional_ceff_rate_characters")

    # B+(2) is a sufficient regular class, not a necessity theorem. The
    # orientation-preserving clock-and-ruler sign reversal lies outside positive B+(2)
    # and leaves every pair metric and terminal coefficient unchanged.
    sign_reversal = -sp.eye(2)
    assert sign_reversal.det() == 1
    assert_zero(sign_reversal.T * h * sign_reversal - h)
    checks.append("bplus2_sufficient_not_necessary_for_phi_beta_character_laws")

    # Total carried comparison rate is gauge-invariant and composes semidirectly.
    ra, dra = matrix_symbols("ra"), matrix_symbols("dra")
    rb, drb = matrix_symbols("rb"), matrix_symbols("drb")
    cba = rb * m * ra.inv()
    dcba = (
        drb * m * ra.inv() + rb * dm * ra.inv()
        - cba * dra * ra.inv()
    )
    gamma = dcba * cba.inv()
    omega_a, omega_b = dra * ra.inv(), drb * rb.inv()
    assert_zero(gamma - omega_b - rb * k * rb.inv() + cba * omega_a * cba.inv())
    rap, rbp = ra * pa, rb * pb
    drap, drbp = dra * pa + ra * dpa, drb * pb + rb * dpb
    cbap = rbp * mp * rap.inv()
    dcbap = (
        drbp * mp * rap.inv() + rbp * dmp * rap.inv()
        - cbap * drap * rap.inv()
    )
    assert_zero(cbap - cba)
    assert_zero(dcbap - dcba)
    assert_zero(dcbap * cbap.inv() - gamma)
    checks.append("total_transition_rate_decomposition_and_live_endpoint_gauge_invariance")

    # Total comparison rates obey the same right-rate semidirect composition law.
    c1, dc1 = matrix_symbols("ca_"), matrix_symbols("dca_")
    c2, dc2 = matrix_symbols("cb_"), matrix_symbols("dcb_")
    c21 = c2 * c1
    dc21 = dc2 * c1 + c2 * dc1
    gamma1, gamma2 = dc1 * c1.inv(), dc2 * c2.inv()
    gamma21 = dc21 * c21.inv()
    assert_zero(gamma21 - gamma2 - c2 * gamma1 * c2.inv())
    checks.append("total_transition_right_rate_composition")

    # Strictly upper-triangular rate defect is invisible to determinant and reciprocal diagonals.
    shear = sp.Matrix([[0, 1], [0, 0]])
    assert sp.trace(shear) == 0
    assert shear[1, 1] - shear[0, 0] == 0
    assert shear != sp.zeros(2)
    checks.append("scalar_scale_and_reciprocal_rate_closure_miss_shift_defect")

    assert len(checks) == 13
    return {
        "exact_checks": len(checks),
        "exact_check_names": checks,
        "general_glplus2_tensor_carry_derived": True,
        "right_connection_rate_composition_derived": True,
        "combined_first_jet_live_endpoint_gauge_covariant": True,
        "intrinsic_connection_split_gauge_independent": False,
        "universal_terminal_character": "kappa_dot_plus_half_trace_K",
        "phi_beta_carry_only_law_exists_on_full_glplus2": False,
        "bplus2_sufficient_for_phi_beta_character_laws": True,
        "bplus2_necessary_for_every_phi_beta_character_law": False,
        "pair_first_jet_faithfully_detects_carry_closure": False,
        "lorentz_stabilizer_invisible_to_pair_first_jet": True,
        "scalar_rate_closure_implies_matrix_rate_closure": False,
        "physical_carry_derived": False,
        "physical_history_derived": False,
        "physical_lambda_owned": False,
    }


def main() -> None:
    result = {
        "status": "PASS",
        "registered_outcome_class": (
            "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_TENSOR_AND_"
            "CONNECTION_COMPOSITION__TERMINAL_CHARACTER_BOUNDARY_CLASSIFIED"
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
