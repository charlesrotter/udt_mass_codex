#!/usr/bin/env python3
"""V-BAO purity + correctness tests (M2 D4 wiring for the BAO leg).

Run: python3 -m pytest test_v_bao.py -q   (from this directory)
All tests are synthetic/offline except the loader tests, which touch only
file NAMES (nonexistent paths) -- the blacklist must fire BEFORE any I/O.
"""
import numpy as np
import pytest

import v_bao

RNG = np.random.default_rng(42)


def _uniform(n, tag="synthetic", rng=RNG):
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    return v_bao.Catalog(ra, dec, np.full(n, 0.45), np.ones(n), tag, "t")


# ---------------- F-IMPORT-LCDM machine wires ----------------
def test_blacklist_nx_raises_before_io():
    with pytest.raises(v_bao.BlacklistViolation):
        v_bao.load_columns("/nonexistent/file.fits", ["RA", "NX"])


def test_blacklist_fkp_raises_before_io():
    with pytest.raises(v_bao.BlacklistViolation):
        v_bao.load_columns("/nonexistent/file.fits", ["WEIGHT_FKP"])


def test_non_whitelisted_column_raises():
    with pytest.raises(v_bao.BlacklistViolation):
        v_bao.load_columns("/nonexistent/file.fits", ["WEIGHT"])  # composite


def test_rec_path_refused_before_io():
    # nonexistent path: BlacklistViolation (not FileNotFoundError) proves
    # the check fires before any file access
    with pytest.raises(v_bao.BlacklistViolation):
        v_bao.load_columns("/nonexistent/LRG_NGC_rec_clustering.dat.fits",
                           ["RA"])


def test_loader_has_no_nx_pathway():
    # the public loader builds its column list internally; assert the
    # frozen whitelist itself excludes the contaminated columns
    assert set(v_bao.BLACKLIST_COLUMNS).isdisjoint(v_bao.ALLOWED_COLUMNS)
    assert "NX" not in v_bao.ALLOWED_COLUMNS
    assert "WEIGHT_FKP" not in v_bao.ALLOWED_COLUMNS


# ---------------- M2 guard (F-PEEK wire) ----------------
def test_m2_guard_blocks_real_data():
    D = _uniform(200, tag="real")
    R = _uniform(400, tag="synthetic")
    with pytest.raises(v_bao.M2GuardViolation):
        v_bao.ls_w_theta(D, R)
    with pytest.raises(v_bao.M2GuardViolation):
        v_bao.ls_w_theta(R, D)


def test_smoke_cap_enforced():
    big = _uniform(60000, tag="smoke")
    with pytest.raises(v_bao.M2GuardViolation):
        v_bao.ls_w_theta(big, big)


def test_make_smoke_caps():
    c = _uniform(50000, tag="real")
    assert len(v_bao.make_smoke(c, "data")) <= v_bao.SMOKE_MAX["data"]
    assert v_bao.make_smoke(c, "data").tag == "smoke"


def test_smoke_data_cap_strict_per_role():
    # A7: a hand-tagged 'smoke' DATA catalog above the 2e4 data cap must be
    # caught even though it is below the 4e4 randoms cap
    D = _uniform(30000, tag="smoke")
    R = _uniform(10000, tag="smoke")
    with pytest.raises(v_bao.M2GuardViolation):
        v_bao.ls_w_theta(D, R)


# ---------------- estimator correctness ----------------
def test_weight_sensitivity_duplication_identity():
    """A1 (verifier amendment): the weighted pair-count path must be
    LOAD-BEARING. Position-dependent weights (w=2 on the northern points)
    vs the same points DUPLICATED at w=1 give EXACTLY identical binned
    ordered counts -- an identity that holds only if the weight product is
    actually applied. Dropping the weight product (the verifier's mutation
    probe 3) breaks it detectably."""
    rng = np.random.default_rng(12)
    n = 600
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    z = np.full(n, 0.45)
    w = np.where(dec > 0, 2.0, 1.0)          # position-dependent weights
    A = v_bao.Catalog(ra, dec, z, w, "synthetic", "A")
    dup = dec > 0
    ra_b = np.concatenate([ra, ra[dup]])
    dec_b = np.concatenate([dec, dec[dup]])
    B = v_bao.Catalog(ra_b, dec_b, np.full(ra_b.size, 0.45),
                      np.ones(ra_b.size), "synthetic", "B")
    regA = np.zeros(n, dtype=np.int64)
    regB = np.zeros(ra_b.size, dtype=np.int64)
    DD_A = v_bao.pair_count_blocks(A, A, regA, regA, nreg=1,
                                   auto=True).sum(axis=(0, 1))
    DD_B = v_bao.pair_count_blocks(B, B, regB, regB, nreg=1,
                                   auto=True).sum(axis=(0, 1))
    # power check first: weights must actually matter in this configuration
    # (unweighted counts of A differ from the weighted ones by ~2x in total)
    A_unw = v_bao.Catalog(ra, dec, z, np.ones(n), "synthetic", "A1")
    DD_unw = v_bao.pair_count_blocks(A_unw, A_unw, regA, regA, nreg=1,
                                     auto=True).sum(axis=(0, 1))
    assert DD_A.sum() > 1.5 * DD_unw.sum()
    # the exact identity: catches the drop-the-weight-product mutation,
    # under which DD_A -> DD_unw while DD_B stays (far) larger
    assert np.allclose(DD_A, DD_B, rtol=1e-9, atol=1e-7)


def test_ls_uniform_sphere_near_zero():
    rng = np.random.default_rng(7)
    D = _uniform(4000, rng=rng)
    R = _uniform(8000, rng=rng)
    res = v_bao.ls_w_theta(D, R)
    good = np.isfinite(res["w"]) & (res["sig"] > 0)
    pulls = res["w"][good] / res["sig"][good]
    assert np.nanmax(np.abs(pulls)) < 5.0
    assert abs(np.nanmean(res["w"][good])) < 0.02


def test_shell_floor_drops():
    n = 1000  # far below the 5e4 weighted floor
    c = _uniform(n)
    c.z[:] = 0.62  # inside LRG range
    kept, dropped = v_bao.bin_shells(c, "LRG")
    assert kept == [] and len(dropped) == 14


# ---------------- bump machinery ----------------
def test_bump_recovery_fast():
    theta = v_bao.theta_bin_centers()
    x = np.log(theta)
    sig = np.full(theta.size, 0.002)
    rng = np.random.default_rng(3)
    y = 0.01 - 0.004 * (x - x.mean()) + \
        0.015 * np.exp(-0.5 * ((x - np.log(3.0)) / 0.2) ** 2) + \
        rng.normal(0, sig)
    fit = v_bao.detect_bump(theta, y, sig)
    assert abs(np.log(fit["theta_b"] / 3.0)) < 0.15
    assert fit["dchi2"] > 25


def test_calibration_matches_grid_search():
    # the vectorized null-mock calibration must equal the refine=False
    # grid search dchi2 on identical noise draws
    theta = v_bao.theta_bin_centers()
    sig = np.full(theta.size, 0.002)
    dist = v_bao.calibrate_max_dchi2(sig, n_mocks=5, seed=9, theta=theta)
    rng = np.random.default_rng(9)
    Y = rng.normal(0.0, sig, size=(5, theta.size))
    ref = sorted(v_bao.detect_bump(theta, y, sig, refine=False)["dchi2"]
                 for y in Y)
    assert np.allclose(np.sort(dist), ref, rtol=1e-8, atol=1e-10)


# ---------------- profile predictions (D1 wiring) ----------------
def test_shape_limits_reduce_to_p2():
    L = np.linspace(0.05, 1.2, 7)
    for prof in ("P1", "P3"):
        assert np.allclose(v_bao.shape_g(prof, L, 1e-12), 2 * L, rtol=1e-9)


def test_theta_bao_lowz_universal():
    # theta -> s/(2 L) for every profile at low z (D1 KEY thetaBAO_*_lowz)
    z = 1e-4
    for prof, sh in (("P1", 0.7), ("P2", None), ("P3", 0.7)):
        t = v_bao.theta_bao_pred(z, prof, 1.0, sh)
        assert np.isclose(t, 1.0 / (2 * np.log1p(z)), rtol=1e-3)


def test_fsteer_no_privileged_shape_grid():
    # F-STEER: grid must not contain 1/n = 1 (n=1) or 1/alpha = 0.5 (alpha=2)
    assert not np.any(np.isclose(v_bao.SHAPE_GRID, 1.0))
    assert not np.any(np.isclose(v_bao.SHAPE_GRID, 0.5))


def test_joint_fit_recovers_clean_input():
    z = np.array([0.45, 0.65, 0.85, 1.05])
    s_true, sh_true = 3.0, 0.8
    th = v_bao.theta_bao_pred(z, "P1", s_true, sh_true)
    fit = v_bao.joint_shape_fit(z, th, 0.01 * th, "P1")
    lo, hi = fit["s_interval_dchi2_1"]
    assert lo <= s_true <= hi
    assert abs(np.log(fit["s_best"] / s_true)) < 0.05
