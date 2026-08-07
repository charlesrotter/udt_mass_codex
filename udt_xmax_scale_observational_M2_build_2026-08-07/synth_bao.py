#!/usr/bin/env python3
"""V-BAO synthetic validation gates (M2, prereg section 4 'Synthetic
validation gate'). Runs on SYNTHETIC data only (tag='synthetic'); no real
catalog is touched here.

Gate JK: jackknife error validation -- mean jackknife sigma vs the empirical
         scatter of w(theta) across independent uniform mocks.
Gate A : bump injection into mock w(theta) vectors (noise at the
         jackknife-estimated level from synthetic) => recovery of center/width;
         false-positive rate on null mocks at the trials-calibrated threshold.
Gate B : end-to-end mini-mock -- synthetic RA/DEC/Z catalog via pair-splitting
         with theta_inj(z) = ell_inj/r(z) under a chosen truth profile =>
         full pipeline (shells -> LS+jackknife -> bump -> joint fit) recovers
         theta_BAO(z) in >=2 shells and s = ell/X_eff within intervals.

Validation-truth choices (arbitrary, documented, NOT privileged: F-STEER --
truth n=1.6 is neither n=1 nor the alpha=2 mirror):
  profile P1, n_truth=1.6 (shape=1/n=0.625), X_eff arbitrary units,
  s_truth = ell_inj/X_eff = 0.05 rad = 2.8648 deg.
"""
import json
import os
import time

import numpy as np

import v_bao

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "vbao_outputs")
os.makedirs(OUT, exist_ok=True)

PATCH = {"ra": (150.0, 190.0), "dec": (0.0, 30.0)}   # ~1160 deg^2 test patch
S_TRUTH_RAD = 0.05          # ell_inj / X_eff (the identified combination)
SHAPE_TRUTH = 0.625         # 1/n, n_truth = 1.6 (P1)
PROFILE_TRUTH = "P1"
Z_RANGE_B = (0.40, 0.50)    # two frozen LRG-width shells
N_DATA_PER_SHELL = 60000    # >= 5e4 weighted floor
RAN_FACTOR = 2


def uniform_patch(n, rng, tag="synthetic", z=None):
    ra = rng.uniform(*PATCH["ra"], n)
    smin, smax = np.sin(np.radians(PATCH["dec"][0])), np.sin(np.radians(PATCH["dec"][1]))
    dec = np.degrees(np.arcsin(rng.uniform(smin, smax, n)))
    if z is None:
        z = np.full(n, 0.45)
    w = rng.uniform(0.8, 1.2, n)     # exercise the weighted path
    return v_bao.Catalog(ra, dec, z, w, tag, "synthetic")


def gate_jackknife(n_real=8, n=8000, seed=11):
    """Jackknife sigma vs ensemble scatter on uniform mocks."""
    rng = np.random.default_rng(seed)
    ws, sigs = [], []
    for _ in range(n_real):
        D = uniform_patch(n, rng)
        R = uniform_patch(2 * n, rng)
        res = v_bao.ls_w_theta(D, R)
        ws.append(res["w"])
        sigs.append(res["sig"])
    ws = np.array(ws)
    emp = np.std(ws, axis=0, ddof=1)
    jk = np.mean(np.array(sigs), axis=0)
    ratio = jk / np.where(emp > 0, emp, np.nan)
    med = float(np.nanmedian(ratio))
    return {"median_jk_over_empirical": med,
            "pass": bool(0.6 <= med <= 1.8),
            "note": ("jackknife may be mildly conservative at patch scale; "
                     "acceptance band 0.6-1.8 on the median ratio, "
                     f"{n_real} realizations x {n} pts")}


def _true_null_curve(x):
    """Arbitrary smooth cubic in ln(theta) as the null background."""
    xc = x - x.mean()
    return 0.004 - 0.006 * xc + 0.001 * xc ** 2 - 0.0005 * xc ** 3

def gate_a(seed=21, n_inject=60, n_cal=400, n_fp=200):
    """Bump injection into mock w(theta) vectors + FP-rate calibration.

    Noise level: the jackknife sigma(theta) estimated from one synthetic
    uniform LS run at gate-B scale (the 'realistic level from synthetic')."""
    rng = np.random.default_rng(seed)
    D = uniform_patch(20000, rng)
    R = uniform_patch(40000, rng)
    sig = v_bao.ls_w_theta(D, R)["sig"]
    # scale jk sigma from 2e4 to the 6e4-per-shell regime: ~ 1/N in pair terms
    sig = sig * (20000.0 / N_DATA_PER_SHELL)
    theta = v_bao.theta_bin_centers()
    x = np.log(theta)
    null_curve = _true_null_curve(x)
    tb_true, sb_true = 2.0, 0.25
    A_true = 5.0 * float(np.median(sig))
    bump = A_true * np.exp(-0.5 * ((x - np.log(tb_true)) / sb_true) ** 2)

    null_dist = v_bao.calibrate_max_dchi2(sig, n_mocks=n_cal, seed=seed + 1)
    thresh = float(null_dist[int(0.95 * n_cal)])   # 95th pct of max-dchi2

    # recovery on injected mocks
    rec_tb, rec_sb, detected = [], [], 0
    for m in range(n_inject):
        y = null_curve + bump + rng.normal(0.0, sig)
        fit = v_bao.detect_bump(theta, y, sig, refine=True)
        rec_tb.append(fit["theta_b"])
        rec_sb.append(fit["sigma_b"])
        if fit["dchi2"] > thresh:
            detected += 1
    rec_tb, rec_sb = np.array(rec_tb), np.array(rec_sb)
    frac_center = float(np.mean(np.abs(np.log(rec_tb / tb_true)) < 0.25))
    med_sb = float(np.median(rec_sb))

    # false positives on independent null mocks at the calibrated threshold
    fp_dist = v_bao.calibrate_max_dchi2(sig, n_mocks=n_fp, seed=seed + 2)
    fp_rate = float(np.mean(fp_dist > thresh))
    fp_ok = abs(fp_rate - 0.05) <= 3.0 * np.sqrt(0.05 * 0.95 / n_fp)

    res = {"A_true": A_true, "theta_b_true": tb_true, "sigma_b_true": sb_true,
           "thresh_dchi2_95": thresh,
           "detection_rate": detected / n_inject,
           "frac_center_within_25pct": frac_center,
           "median_recovered_theta_b": float(np.median(rec_tb)),
           "median_recovered_sigma_b": med_sb,
           "fp_rate_at_thresh": fp_rate, "fp_expected": 0.05,
           "pass": bool(frac_center >= 0.9 and detected / n_inject >= 0.9
                        and fp_ok and 0.5 * sb_true <= med_sb <= 2 * sb_true)}
    return res


def uniform_sphere(n, rng, tag="synthetic", z=None):
    ra = rng.uniform(0.0, 360.0, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1.0, 1.0, n)))
    if z is None:
        z = np.full(n, 0.45)
    w = rng.uniform(0.8, 1.2, n)
    return v_bao.Catalog(ra, dec, z, w, tag, "synthetic-sphere")


F_COMPANION = 0.25   # fraction of mock points that are ring companions


def make_paired_catalog(n_total, zlo, zhi, rng):
    """Pair-splitting mock on the FULL SPHERE (edge-free by construction):
    a fraction F_COMPANION of points are companions placed at angular
    distance theta_inj(z) = s_truth/g(z) (truth profile), random bearing.

    Why full sphere (documented mock-design finding, first build iteration):
    on a finite patch, dropping out-of-patch companions imprints a REAL
    density gradient in the data that the uniform randoms do not share,
    producing a broad spurious w(theta)~0.007 that swamps a BAO-amplitude
    ring; on the sphere no such artifact exists and the gate tests the
    PIPELINE, not the mock's edges. Real DESI data has no such artifact
    (its randoms share the true footprint selection)."""
    n_comp = int(round(n_total * F_COMPANION))
    n_seed = n_total - n_comp
    seeds = uniform_sphere(n_seed, rng, z=None)
    z = rng.uniform(zlo, zhi, n_seed)
    zp = z[:n_comp]                       # parents = first n_comp seeds
    th = S_TRUTH_RAD / v_bao.shape_g(PROFILE_TRUTH, np.log1p(zp), SHAPE_TRUTH)
    p = v_bao._unit_vectors(seeds.ra[:n_comp], seeds.dec[:n_comp])
    # pole-safe local orthonormal basis at each parent
    a = np.zeros_like(p)
    polar = np.abs(p[:, 2]) > 0.9
    a[~polar, 2] = 1.0
    a[polar, 0] = 1.0
    e1 = np.cross(a, p)
    e1 /= np.linalg.norm(e1, axis=1)[:, None]
    e2 = np.cross(p, e1)
    psi = rng.uniform(0, 2 * np.pi, n_comp)
    q = (np.cos(th)[:, None] * p +
         np.sin(th)[:, None] * (np.cos(psi)[:, None] * e1 +
                                np.sin(psi)[:, None] * e2))
    ra_c = np.degrees(np.arctan2(q[:, 1], q[:, 0])) % 360.0
    dec_c = np.degrees(np.arcsin(np.clip(q[:, 2], -1, 1)))
    ra = np.concatenate([seeds.ra, ra_c])
    dec = np.concatenate([seeds.dec, dec_c])
    zz = np.concatenate([z, zp])
    w = rng.uniform(0.8, 1.2, ra.size)
    return v_bao.Catalog(ra, dec, zz, w, "synthetic", "paired-mock-sphere")

def _subset(cat, mask, tag=None):
    return v_bao.Catalog(cat.ra[mask], cat.dec[mask], cat.z[mask], cat.w[mask],
                         tag or cat.tag, cat.name)


def bump_center_error(theta, w, sig, fit):
    """Delta-chi2=1 half-width on ln(theta_b), amplitude refit, width fixed
    at the best fit (a conditional error; adequate for the joint-fit gate)."""
    x = np.log(theta)
    good = np.isfinite(w) & np.isfinite(sig) & (sig > 0)
    xg, yg = x[good], w[good]
    ivar = 1.0 / sig[good] ** 2
    Xn = v_bao._null_design(x)[good]
    xc0, sw = np.log(fit["theta_b"]), fit["sigma_b"]

    def c2(xc):
        g = np.exp(-0.5 * ((xg - xc) / sw) ** 2)
        _, c = v_bao._gls_lin(np.column_stack([Xn, g]), yg, ivar)
        return c

    scan = xc0 + np.linspace(-0.4, 0.4, 81)
    cs = np.array([c2(v) for v in scan])
    cmin = cs.min()
    inside = scan[cs <= cmin + 1.0]
    half = 0.5 * (inside.max() - inside.min()) if inside.size > 1 else 0.4
    return float(max(half, 1e-3))


def gate_b(seed=31, n_cal=300):
    """End-to-end mini-mock through the full pipeline."""
    rng = np.random.default_rng(seed)
    edges = v_bao.shell_edges("LRG")
    shells_gen = [(a, b) for a, b in zip(edges[:-1], edges[1:])
                  if a >= Z_RANGE_B[0] - 1e-9 and b <= Z_RANGE_B[1] + 1e-9]
    parts = [make_paired_catalog(N_DATA_PER_SHELL, a, b, rng)
             for a, b in shells_gen]
    data = v_bao.Catalog(*[np.concatenate([getattr(p, f) for p in parts])
                           for f in ("ra", "dec", "z", "w")],
                         "synthetic", "e2e-mock")
    nr = RAN_FACTOR * len(data)
    rand = uniform_sphere(nr, rng, z=rng.choice(data.z, nr))  # shuffled z

    kept, dropped = v_bao.bin_shells(data, "LRG")
    shells_out = []
    for sh in kept:
        D = _subset(data, sh["mask"])
        rmask = (rand.z >= sh["zlo"]) & (rand.z < sh["zhi"])
        R = _subset(rand, rmask)
        t0 = time.time()
        res = v_bao.ls_w_theta(D, R)
        t_ls = time.time() - t0
        fit = v_bao.detect_bump(res["theta"], res["w"], res["sig"], refine=True)
        null_dist = v_bao.calibrate_max_dchi2(res["sig"], n_mocks=n_cal,
                                              seed=seed + 5)
        pval = v_bao.bump_pvalue(fit["dchi2"], null_dist)
        zc = 0.5 * (sh["zlo"] + sh["zhi"])
        th_inj = np.degrees(S_TRUTH_RAD / v_bao.shape_g(
            PROFILE_TRUTH, np.log1p(zc), SHAPE_TRUTH))
        err = bump_center_error(res["theta"], res["w"], res["sig"], fit)
        shells_out.append({
            "z": [sh["zlo"], sh["zhi"]], "zc": zc, "N_D": len(D), "N_R": len(R),
            "t_ls_s": round(t_ls, 1), "theta_inj_deg": th_inj,
            "theta_b_rec": fit["theta_b"], "sigma_lnthb": err,
            "dchi2": fit["dchi2"], "p_trials": pval,
            "detected": bool(pval < 0.05),
            "center_ok": bool(abs(np.log(fit["theta_b"] / th_inj)) < 0.15)})
    zcs = np.array([s["zc"] for s in shells_out])
    thb = np.array([s["theta_b_rec"] for s in shells_out])
    sth = np.array([s["sigma_lnthb"] for s in shells_out]) * thb  # ln->abs
    joint = {p: v_bao.joint_shape_fit(zcs, thb, sth, p) for p in v_bao.PROFILES}
    s_truth_deg = np.degrees(S_TRUTH_RAD)
    jt = joint[PROFILE_TRUTH]
    lo1, hi1 = jt["s_interval_dchi2_1"]
    lo2, hi2 = jt["s_interval_dchi2_4"]   # coverage gated at 2-sigma (stated)
    n_det = sum(s["detected"] and s["center_ok"] for s in shells_out)
    res = {"shells": shells_out, "n_dropped_shells": len(dropped),
           "joint_fits": joint, "s_truth_deg": s_truth_deg,
           "s_interval_1sig": [lo1, hi1], "s_interval_2sig": [lo2, hi2],
           "s_covered_2sig": bool(lo2 <= s_truth_deg <= hi2),
           "pass": bool(n_det >= 2 and lo2 <= s_truth_deg <= hi2)}
    return res


if __name__ == "__main__":
    t0 = time.time()
    out = {}
    out["gate_jackknife"] = gate_jackknife()
    print("gate_jackknife:", "PASS" if out["gate_jackknife"]["pass"] else "FAIL",
          out["gate_jackknife"]["median_jk_over_empirical"])
    out["gate_a"] = gate_a()
    print("gate_a:", "PASS" if out["gate_a"]["pass"] else "FAIL",
          {k: out["gate_a"][k] for k in ("detection_rate",
           "frac_center_within_25pct", "fp_rate_at_thresh")})
    out["gate_b"] = gate_b()
    print("gate_b:", "PASS" if out["gate_b"]["pass"] else "FAIL",
          "s_truth=", out["gate_b"]["s_truth_deg"],
          "2sig_interval=", out["gate_b"]["s_interval_2sig"])
    out["total_runtime_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "synth_gate_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("total runtime %.0fs -> vbao_outputs/synth_gate_results.json"
          % out["total_runtime_s"])
