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


def gate_jackknife(n_real=8, n=8000, seed=11, backend="cpu"):
    """Jackknife sigma vs ensemble scatter on uniform mocks."""
    rng = np.random.default_rng(seed)
    ws, sigs = [], []
    for _ in range(n_real):
        D = uniform_patch(n, rng)
        R = uniform_patch(2 * n, rng)
        res = v_bao.ls_w_theta(D, R, backend=backend)
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

def gate_a(seed=21, n_inject=60, n_cal=400, n_fp=200, backend="cpu"):
    """Bump injection into mock w(theta) vectors + FP-rate calibration.

    Noise level: the jackknife sigma(theta) estimated from one synthetic
    uniform LS run at gate-B scale (the 'realistic level from synthetic')."""
    rng = np.random.default_rng(seed)
    D = uniform_patch(20000, rng)
    R = uniform_patch(40000, rng)
    sig = v_bao.ls_w_theta(D, R, backend=backend)["sig"]
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


def gate_b(seed=31, n_cal=300, backend="cpu"):
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
        res = v_bao.ls_w_theta(D, R, backend=backend)
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



# ---------------------------------------------------------------------------
# M3-PREP gates (prereg SS5; synthetic only, deterministic seeds)
# ---------------------------------------------------------------------------
def gate_split_rr(seed=41, n_real=10, nd=8000, nr_per=5000):
    """SS5.1: split-averaged RR(4 files) vs full concatenated RR.
    PASS = the across-mocks BIAS of (w_split - w_full) is << the jackknife
    error (median |bias|/sig < 0.15) AND per-realization agreement is within
    noise (median per-bin RMS diff / sig < 0.6)."""
    rng = np.random.default_rng(seed)
    diffs, sigs = [], []
    for _ in range(n_real):
        D = uniform_sphere(nd, rng)
        R_list = [uniform_sphere(nr_per, rng) for _ in range(4)]
        a = v_bao.ls_w_theta_split(D, R_list)
        b = v_bao.ls_w_theta(D, v_bao._concat_catalogs(R_list))
        diffs.append(a["w"] - b["w"])
        sigs.append(b["sig"])
    diffs = np.array(diffs)
    sig = np.nanmean(np.array(sigs), axis=0)
    bias = np.nanmean(diffs, axis=0)
    rms = np.nanstd(diffs, axis=0)
    med_bias_ratio = float(np.nanmedian(np.abs(bias) / sig))
    med_rms_ratio = float(np.nanmedian(rms / sig))
    return {"median_abs_bias_over_sig": med_bias_ratio,
            "median_rms_over_sig": med_rms_ratio,
            "n_real": n_real,
            "pass": bool(med_bias_ratio < 0.15 and med_rms_ratio < 0.6)}


def gate_look_elsewhere(seed=51, ns=8, n_cal=300, n_trial=200):
    """SS5.2: (a) false-positive rate of the global and joint statistics at
    the frozen p<0.01 threshold on pure-null ensembles + global-p uniformity
    sanity; (b) a 3-shell injected feature tied to a truth profile yields the
    ordering local_p <= global_p (trials penalty) and joint_p <= global_p
    (coherence gain), with joint significant."""
    import look_elsewhere as le
    theta = v_bao.theta_bin_centers()
    z = np.linspace(0.45, 0.80, ns)
    sig = [np.full(theta.size, 0.002) for _ in range(ns)]
    rng = np.random.default_rng(seed)
    # (a) shared calibration ensemble + independent trial draws, per shell
    forms = [le._design_forms(s, theta) for s in sig]
    A_cal, A_tri = [], []
    for i in range(ns):
        g = forms[i]["good"]
        Y = rng.normal(0.0, sig[i][g], size=(n_cal + n_trial, int(g.sum())))
        A = le._a_matrix(Y, forms[i])
        A_cal.append(A[:n_cal])
        A_tri.append(A[n_cal:])
    cal_max = np.array([A.max(axis=1) for A in A_cal])   # (ns, n_cal)
    tri_max = np.array([A.max(axis=1) for A in A_tri])
    glob_cal = cal_max.max(axis=0)
    glob_tri = tri_max.max(axis=0)
    thr_glob = float(np.quantile(glob_cal, 0.99))
    fp_glob = float(np.mean(glob_tri > thr_glob))
    p_tri = np.array([np.mean(glob_cal >= t) for t in glob_tri])
    combos = le._joint_grid(z, theta)
    j_cal, _ = le._joint_stat(A_cal, combos)
    j_tri, _ = le._joint_stat(A_tri, combos)
    thr_j = float(np.quantile(j_cal, 0.99))
    fp_joint = float(np.mean(j_tri > thr_j))
    band = 0.01 + 3 * np.sqrt(0.01 * 0.99 / n_trial)
    ok_a = (fp_glob <= band and fp_joint <= band
            and 0.35 < float(np.mean(p_tri)) < 0.65)
    # (b) injection: truth P1, COHERENT WEAK signal in 6 shells (amp 1.8 sig
    # per shell) -- individually marginal, jointly strong: the regime the
    # joint statistic exists for. Ordering demanded: local <= global (the
    # trials penalty, non-saturated) and joint BEATS global (coherence gain),
    # joint significant at the frozen 0.01, truth profile recovered.
    shape_truth, inj_shells, amp = 0.625, range(1, 7), 1.8
    L = np.log1p(z)
    g_mid = v_bao.shape_g("P1", np.log1p(z[ns // 2]), shape_truth)
    s_truth = np.radians(4.0) * g_mid          # theta_b(z_mid) = 4 deg
    w_obs = []
    x = np.log(theta)
    for i in range(ns):
        y = rng.normal(0.0, sig[i])
        if i in inj_shells:
            thb = np.degrees(s_truth / v_bao.shape_g("P1", L[i], shape_truth))
            y = y + amp * 0.002 * np.exp(-0.5 * ((x - np.log(thb)) / 0.2) ** 2)
        w_obs.append(y)
    res = le.analyze_shells(w_obs, sig, z, n_mocks=n_cal, seed=seed + 7)
    min_local = min(res["local_p"][i] for i in inj_shells)
    ok_b = (min_local <= res["global_p"] + 1e-12
            and res["joint"]["p"] < res["global_p"]
            and res["joint"]["p"] < 0.01
            and res["joint"]["best_combo"].get("profile") == "P1")
    return {"fp_global_at_0.01": fp_glob, "fp_joint_at_0.01": fp_joint,
            "fp_band_3sig": band, "mean_null_global_p": float(np.mean(p_tri)),
            "inj_min_local_p": min_local, "inj_global_p": res["global_p"],
            "inj_joint_p": res["joint"]["p"],
            "inj_joint_best": res["joint"]["best_combo"].get("profile"),
            "pass": bool(ok_a and ok_b)}


def gate_jk_combined(seed=61, n_real=8, nd=6000):
    """SS5.3 (M2 verifier's owed item): union-region jackknife of the
    COMBINED-cap estimator vs empirical scatter (M2 JK band 0.6-1.8).
    Two disjoint synthetic caps separated far beyond theta_max."""
    rng = np.random.default_rng(seed)

    def cap_patch(n, ra0, dec0):
        ra = rng.uniform(ra0, ra0 + 60, n)
        smin, smax = np.sin(np.radians(dec0)), np.sin(np.radians(dec0 + 40))
        dec = np.degrees(np.arcsin(rng.uniform(smin, smax, n)))
        return v_bao.Catalog(ra, dec, np.full(n, 0.45),
                             rng.uniform(0.8, 1.2, n), "synthetic", "cap")

    ws, sigs = [], []
    for _ in range(n_real):
        caps = [(cap_patch(nd, 20.0, 5.0), cap_patch(2 * nd, 20.0, 5.0)),
                (cap_patch(nd, 200.0, -45.0), cap_patch(2 * nd, 200.0, -45.0))]
        r = v_bao.ls_w_theta_capcombine(caps)
        ws.append(r["w"])
        sigs.append(r["sig"])
    ws = np.array(ws)
    emp = np.std(ws, axis=0, ddof=1)
    jk = np.mean(np.array(sigs), axis=0)
    med = float(np.nanmedian(jk / np.where(emp > 0, emp, np.nan)))
    return {"median_jk_over_empirical": med, "n_real": n_real,
            "pass": bool(0.6 <= med <= 1.8)}


def run_gates(backend="cpu"):
    """Run all three synthetic gates on the chosen backend and write the
    backend-suffixed results json (B1 amendment: shipped provenance for the
    GPU results file). Same seeds; results differ only at fp-accumulation
    order between backends."""
    out = {}
    timings = {}
    t = time.time()
    out["gate_jackknife"] = gate_jackknife(backend=backend)
    timings["gate_jackknife"] = round(time.time() - t, 1)
    print("gate_jackknife:", "PASS" if out["gate_jackknife"]["pass"] else "FAIL",
          out["gate_jackknife"]["median_jk_over_empirical"])
    t = time.time()
    out["gate_a"] = gate_a(backend=backend)
    timings["gate_a"] = round(time.time() - t, 1)
    print("gate_a:", "PASS" if out["gate_a"]["pass"] else "FAIL",
          {k: out["gate_a"][k] for k in ("detection_rate",
           "frac_center_within_25pct", "fp_rate_at_thresh")})
    t = time.time()
    out["gate_b"] = gate_b(backend=backend)
    timings["gate_b"] = round(time.time() - t, 1)
    print("gate_b:", "PASS" if out["gate_b"]["pass"] else "FAIL",
          "s_truth=", out["gate_b"]["s_truth_deg"],
          "2sig_interval=", out["gate_b"]["s_interval_2sig"])
    out["timings_s"] = timings
    out["backend"] = backend
    out["total_runtime_s"] = round(sum(timings.values()), 1)
    suffix = "" if backend == "cpu" else "_" + backend
    fn = os.path.join(OUT, "synth_gate_results%s.json" % suffix)
    with open(fn, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("total runtime %.0fs -> %s" % (out["total_runtime_s"], fn))
    return out


if __name__ == "__main__":
    import sys
    be = "cpu"
    if "--backend" in sys.argv:
        be = sys.argv[sys.argv.index("--backend") + 1]
    run_gates(backend=be)
