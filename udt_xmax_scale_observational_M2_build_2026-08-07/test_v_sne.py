"""D4-facing pytest gate for the V-SNe validator (hermetic: no real-data files read).

Covers: (1) M2_GUARD blocks non-synthetic fits; (2) the loader refuses non-whitelisted
columns per mode and refuses z-column swaps outside mode D; (3) P1 at n=1 reproduces the
banked d_L = R_w*z(z+2) numerically (KEY P1_n1_banked_dL_z_zplus2); (4) fast synthetic
injection-recovery, 1 truth point, modes A-analog and C-analog (diagonal mock noise).
"""
import io
import numpy as np
import pytest

import v_sne as V


def _fake_table(n=40):
    """Tiny synthetic table exercising the loader (NOT real data)."""
    rng = np.random.default_rng(7)
    z = np.round(np.sort(rng.uniform(0.005, 1.2, n)), 5)
    iscal = (np.arange(n) % 13 == 0).astype(int)
    hdr = ("CID zHD zCMB zHEL m_b_corr mB mBERR x1 x1ERR c cERR IS_CALIBRATOR "
           "m_b_corr_err_DIAG")
    rows = [hdr]
    for i in range(n):
        rows.append(
            f"SN{i} {z[i]:.5f} {z[i]:.5f} {z[i]:.5f} {18 + 5 * z[i]:.4f} "
            f"{18.4 + 5 * z[i]:.4f} 0.10 {rng.normal():.4f} 0.5 {0.1 * rng.normal():.4f} "
            f"0.03 {iscal[i]} 0.15")
    return np.genfromtxt(io.StringIO("\n".join(rows)), names=True, dtype=None,
                         encoding="utf-8")


def test_m2_guard_blocks_real_fit():
    z = np.linspace(0.05, 1.0, 50)
    dv = V.DataVector("A", z, y=np.zeros(50), cov=np.eye(50), synthetic=False)
    with pytest.raises(RuntimeError, match="F-PEEK"):
        V.fit_mode_A(dv, "P2")
    tr = {k: np.ones(50) for k in ("mB", "mBERR", "x1", "x1ERR", "c", "cERR")}
    dv_c = V.DataVector("C", z, tripp=tr, synthetic=False)
    with pytest.raises(RuntimeError, match="F-PEEK"):
        V.fit_mode_C(dv_c, "P2")
    assert V.M2_GUARD is True  # the M2 posture itself


def test_loader_whitelist_and_zcol_rules():
    tab = _fake_table()
    md = V.load_mode_data("A", table=tab, cov_full=np.eye(len(tab)))
    with pytest.raises(ValueError, match="not whitelisted"):
        md.col("x1")             # SALT2 columns are mode-C-only
    with pytest.raises(ValueError, match="not whitelisted"):
        md.col("m_b_corr_err_DIAG")
    assert md.col("m_b_corr").shape == (md.n,)
    md_c = V.load_mode_data("C", table=tab)
    with pytest.raises(ValueError, match="not whitelisted"):
        md_c.col("m_b_corr")     # BBC-corrected column is FORBIDDEN in mode C
    with pytest.raises(ValueError, match="mode D only"):
        V.load_mode_data("A", zcol="zHD", table=tab)
    md_d = V.load_mode_data("D", zcol="zHEL", table=tab, cov_full=np.eye(len(tab)))
    assert md_d.zcol == "zHEL"
    # cuts: z floor + calibrator exclusion actually applied
    assert (md.col("zCMB") > V.FROZEN_Z_CUT).all()
    assert (md.col("IS_CALIBRATOR") == 0).all()


def test_p1_n1_reproduces_banked_z_zplus2():
    z = np.concatenate([np.geomspace(1e-6, 0.02, 40), np.linspace(0.05, 2.5, 200)])
    Rw = 2.31459
    dL = (1 + z) ** 2 * V.r_of_z("P1", z, X_eff=Rw, shape=1.0)   # n=1 -> X_eff=R_w
    assert np.max(np.abs(dL / (Rw * z * (z + 2)) - 1)) < 1e-12


def test_p1_limit_is_p2():
    z = np.linspace(0.01, 2.0, 50)
    assert np.allclose(V.r_of_z("P1", z, 2.0, 1e-8), V.r_of_z("P2", z, 2.0), rtol=1e-6)


def test_fast_synthetic_recovery_mode_A_analog():
    rng = np.random.default_rng(11)          # frozen seed
    z = np.sort(rng.uniform(0.03, 1.5, 400))
    truth_s, truth_B = 0.6, 22.505           # inv_n (n=5/3, not n=1); B offset
    sig = 0.12
    y = V.mu_shape("P1", z, truth_s) + truth_B + rng.normal(0, sig, z.size)
    dv = V.DataVector("A", z, y=y, cov=np.diag(np.full(z.size, sig ** 2)), synthetic=True)
    r = V.fit_mode_A(dv, "P1")
    iv, ivB = r["shape_interval"], r["offset_interval"]
    hw = max(iv["hi"] - iv["best"], iv["best"] - iv["lo"])
    assert abs(r["shape"] - truth_s) < 4 * hw
    hwB = max(ivB["hi"] - ivB["best"], ivB["best"] - ivB["lo"])
    assert abs(r["offset_B"] - truth_B) < 4 * hwB
    assert 0.7 < r["chi2"] / r["ndof"] < 1.3


def test_fast_synthetic_recovery_mode_C_analog():
    rng = np.random.default_rng(23)          # frozen seed
    n = 400
    z = np.sort(rng.uniform(0.03, 1.2, n))
    x1, c = rng.normal(0, 1.0, n), rng.normal(0, 0.1, n)
    tr = {"x1": x1, "c": c, "mBERR": np.full(n, 0.08),
          "x1ERR": np.full(n, 0.4), "cERR": np.full(n, 0.03)}
    a_t, b_t, s_t, M0_t = 0.14, 3.0, 0.7, 3.2
    sig = np.sqrt(V._tripp_sigma2(tr, a_t, b_t))
    tr["mB"] = (V.mu_shape("P1", z, s_t) + M0_t - a_t * x1 + b_t * c
                + sig * rng.normal(0, 1.0, n))
    dv = V.DataVector("C", z, tripp=tr, synthetic=True)
    r = V.fit_mode_C(dv, "P1")
    for name, tv in (("alpha", a_t), ("beta", b_t)):
        iv = r[name + "_interval"]
        hw = max(iv["hi"] - iv["best"], iv["best"] - iv["lo"])
        assert abs(r[name] - tv) < 4 * hw, (name, r[name], tv, hw)
    ivs = r["shape_interval"]
    hws = max(ivs["hi"] - ivs["best"], ivs["best"] - ivs["lo"])
    assert abs(r["shape"] - s_t) < 4 * hws
