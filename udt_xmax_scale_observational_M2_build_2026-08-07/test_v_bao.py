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

try:
    import torch
    HAVE_GPU = torch.cuda.is_available()
except Exception:
    HAVE_GPU = False
BACKENDS = ["cpu"] + (["gpu"] if HAVE_GPU else [])


def _count(backend, *args, **kw):
    f = (v_bao.pair_count_blocks if backend == "cpu"
         else v_bao.pair_count_blocks_gpu)
    return f(*args, **kw)


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
@pytest.mark.parametrize("backend", BACKENDS)
def test_weight_sensitivity_duplication_identity(backend):
    """A1 (verifier amendment): the weighted pair-count path must be
    LOAD-BEARING. Position-dependent weights (w=2 on the northern points)
    vs the same points DUPLICATED at w=1 give EXACTLY identical binned
    ordered counts -- an identity that holds only if the weight product is
    actually applied. Dropping the weight product (the verifier's mutation
    probe 3) breaks it detectably. Parametrized over BOTH backends (GPU
    amendment #4)."""
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
    DD_A = _count(backend, A, A, regA, regA, nreg=1,
                  auto=True).sum(axis=(0, 1))
    DD_B = _count(backend, B, B, regB, regB, nreg=1,
                  auto=True).sum(axis=(0, 1))
    # power check first: weights must actually matter in this configuration
    # (unweighted counts of A differ from the weighted ones by ~2x in total)
    A_unw = v_bao.Catalog(ra, dec, z, np.ones(n), "synthetic", "A1")
    DD_unw = _count(backend, A_unw, A_unw, regA, regA, nreg=1,
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


# ---------------- GPU backend (Category-A amendment) ----------------
@pytest.mark.skipif(not HAVE_GPU, reason="no CUDA")
@pytest.mark.parametrize("n,block", [(500, 8192), (3000, 1024), (8000, 4096)])
def test_gpu_cpu_equivalence(n, block):
    """Soundness duty: GPU float64 binned counts must equal the CPU tree
    counts per bin (only fp accumulation-order differences allowed)."""
    rng = np.random.default_rng(100 + n)
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    w = np.where(dec > 0, 1.7, 0.6)          # position-dependent weights
    A = v_bao.Catalog(ra, dec, np.full(n, 0.45), w, "synthetic", "A")
    R = _uniform(2 * n, rng=rng)
    rm = v_bao.make_region_map(R.ra, R.dec, R.w)
    rA = v_bao.apply_region_map(rm, A.ra, A.dec)
    rR = v_bao.apply_region_map(rm, R.ra, R.dec)
    for args in ((A, A, rA, rA, 24, True), (A, R, rA, rR, 24, False)):
        cpu = v_bao.pair_count_blocks(*args)
        gpu = v_bao.pair_count_blocks_gpu(*args, block=block)
        assert np.isclose(cpu.sum(), gpu.sum(), rtol=1e-12)
        scale = max(cpu.max(), 1.0)
        assert np.abs(cpu - gpu).max() < 1e-9 * scale


@pytest.mark.skipif(not HAVE_GPU, reason="no CUDA")
def test_gpu_precision_guard_edge_binning():
    """PRECISION GUARD: pairs placed 1e-9 (relative) ABOVE selected bin edges
    must land in the UPPER bin. In float64 the cos-space margin (~1e-12) is
    resolvable; in float32 it collapses to a tie and bucketize misbins to the
    LOWER bin -- so this test FAILS if the GPU path runs float32."""
    edges = v_bao.theta_bin_edges()
    for k in (22, 30, 38):
        th = edges[k] * (1.0 + 1e-9)         # inside bin k (lower edge excl.)
        ra = np.array([10.0, 10.0 + th])
        dec = np.zeros(2)
        cat = v_bao.Catalog(ra, dec, np.full(2, 0.45), np.ones(2),
                            "synthetic", "edge")
        reg = np.zeros(2, dtype=np.int64)
        Cw = v_bao.pair_count_blocks_gpu(cat, cat, reg, reg, nreg=1,
                                         auto=True).sum(axis=(0, 1))
        assert Cw.dtype == np.float64
        assert Cw[k] == 2.0, f"edge {k}: expected upper-bin, got {Cw.nonzero()}"
        assert Cw.sum() == 2.0


@pytest.mark.skipif(not HAVE_GPU, reason="no CUDA")
def test_gpu_ls_end_to_end_matches_cpu():
    rng = np.random.default_rng(77)
    D = _uniform(3000, rng=rng)
    R = _uniform(6000, rng=rng)
    a = v_bao.ls_w_theta(D, R, backend="cpu")
    b = v_bao.ls_w_theta(D, R, backend="gpu")
    good = np.isfinite(a["w"])
    assert np.allclose(a["w"][good], b["w"][good], rtol=1e-9, atol=1e-12)


# ---------------- cap-combine option (#5; default OFF) ----------------
def test_capcombine_counts_equal_sum_of_caps():
    rng = np.random.default_rng(55)

    def patch(n, ra0):
        ra = rng.uniform(ra0, ra0 + 40, n)
        dec = np.degrees(np.arcsin(rng.uniform(0, 0.5, n)))
        w = rng.uniform(0.8, 1.2, n)
        return v_bao.Catalog(ra, dec, np.full(n, 0.45), w, "synthetic", "c")

    caps = [(patch(700, 0.0), patch(1400, 0.0)),
            (patch(600, 180.0), patch(1200, 180.0))]
    comb = v_bao.ls_w_theta_capcombine(caps)
    for key in ("DD", "DR", "RR"):
        per_cap = sum(v_bao.ls_w_theta(D, R)["counts"][key]
                      for D, R in caps)
        assert np.allclose(comb["counts"][key], per_cap, rtol=1e-12)
    assert comb["meta"]["combined"] and comb["meta"]["n_caps"] == 2


def test_capcombine_floor_per_tracer():
    # each cap is below the 5e4 weighted floor; combined they clear it
    rng = np.random.default_rng(66)

    def cap(n, wval):
        ra = rng.uniform(0, 360, n)
        dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
        return v_bao.Catalog(ra, dec, np.full(n, 0.62),
                             np.full(n, wval), "synthetic", "c")

    c1, c2 = cap(1000, 30.0), cap(1000, 30.0)   # 3e4 weighted each
    k1, _ = v_bao.bin_shells(c1, "LRG")
    assert k1 == []                              # per-cap: dropped
    kc, _ = v_bao.bin_shells_combined([c1, c2], "LRG")
    assert len(kc) == 1 and kc[0]["w_sum"] == pytest.approx(6e4)


# ---------------- M3-PREP additions (prereg SS5) ----------------
def test_split_rr_single_file_reduces_exactly():
    rng = np.random.default_rng(91)
    D = _uniform(1500, rng=rng)
    R = _uniform(3000, rng=rng)
    a = v_bao.ls_w_theta(D, R)
    b = v_bao.ls_w_theta_split(D, [R])
    g = np.isfinite(a["w"])
    assert np.allclose(a["w"][g], b["w"][g], rtol=1e-10, atol=1e-12)
    assert np.allclose(a["sig"][g], b["sig"][g], rtol=1e-10, atol=1e-12)


def test_split_rr_four_files_consistent():
    rng = np.random.default_rng(92)
    D = _uniform(3000, rng=rng)
    R_list = [_uniform(1500, rng=rng) for _ in range(4)]
    a = v_bao.ls_w_theta_split(D, R_list)
    b = v_bao.ls_w_theta(D, v_bao._concat_catalogs(R_list))
    g = np.isfinite(a["w"]) & np.isfinite(b["w"]) & (b["sig"] > 0)
    # same underlying data: conventions agree well within the noise scale
    assert np.nanmedian(np.abs(a["w"] - b["w"])[g] / b["sig"][g]) < 0.6


def test_capcombine_split_runs_and_reduces():
    rng = np.random.default_rng(93)

    def patch(n, ra0):
        ra = rng.uniform(ra0, ra0 + 40, n)
        dec = np.degrees(np.arcsin(rng.uniform(0, 0.5, n)))
        return v_bao.Catalog(ra, dec, np.full(n, 0.45),
                             rng.uniform(0.8, 1.2, n), "synthetic", "c")

    capsA = [(patch(600, 0.0), [patch(600, 0.0), patch(600, 0.0)]),
             (patch(500, 180.0), [patch(500, 180.0), patch(500, 180.0)])]
    r = v_bao.ls_w_theta_capcombine(capsA)
    assert r["meta"]["n_ran_files"] == 2 and r["meta"]["nreg_total"] == 48
    assert np.isfinite(r["w"]).any()


def test_authorize_m3_hash_gate():
    import v_bao as vb
    prev = vb.M3_REAL_RUN_AUTHORIZED
    try:
        with pytest.raises(vb.M2GuardViolation):
            vb.authorize_m3("wrong-hash")
        assert vb.M3_REAL_RUN_AUTHORIZED is prev  # unchanged on failure
        assert vb.authorize_m3(vb.M3_PREREG_COMMIT) is True
        assert vb.M3_REAL_RUN_AUTHORIZED is True
    finally:
        vb.M3_REAL_RUN_AUTHORIZED = prev          # restore for other tests


def test_look_elsewhere_deterministic_and_sane():
    import look_elsewhere as le
    rng = np.random.default_rng(94)
    theta = v_bao.theta_bin_centers()
    z = np.array([0.5, 0.6, 0.7])
    sig = [np.full(theta.size, 0.002)] * 3
    w = [rng.normal(0, s) for s in sig]
    r1 = le.analyze_shells(w, sig, z, n_mocks=40, seed=5)
    r2 = le.analyze_shells(w, sig, z, n_mocks=40, seed=5)
    assert r1["global_p"] == r2["global_p"]
    assert r1["joint"]["p"] == r2["joint"]["p"]
    assert 0.0 <= r1["global_p"] <= 1.0
    assert all(0.0 <= p <= 1.0 for p in r1["local_p"])


def test_look_elsewhere_detects_strong_coherent_injection():
    import look_elsewhere as le
    rng = np.random.default_rng(95)
    theta = v_bao.theta_bin_centers()
    x = np.log(theta)
    z = np.array([0.5, 0.6, 0.7, 0.8])
    sig = [np.full(theta.size, 0.002)] * 4
    shape_t = 0.7
    s = np.radians(4.0) * v_bao.shape_g("P1", np.log1p(0.65), shape_t)
    w = []
    for i, zi in enumerate(z):
        thb = np.degrees(s / v_bao.shape_g("P1", np.log1p(zi), shape_t))
        w.append(rng.normal(0, sig[i]) + 5 * 0.002 *
                 np.exp(-0.5 * ((x - np.log(thb)) / 0.2) ** 2))
    r = le.analyze_shells(w, sig, z, n_mocks=60, seed=6)
    assert r["joint"]["p"] <= 1.0 / 60 + 1e-12
    assert r["global_p"] <= 0.05
