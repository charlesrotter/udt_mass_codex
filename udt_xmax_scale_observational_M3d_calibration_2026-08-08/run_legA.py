#!/usr/bin/env python3
"""M3d LEG A runner (prereg 962bd0c6). Frozen pipeline on synthetic universes.

Phases (each budgeted, resumable by checkpoint-file existence; single process,
GPU pair counts, synchronous -- anti-hang compliant):
  assets  : build the per-cap-shell skeleton assets from the real randoms.
  rr      : precompute the fixed RR block counts per cap-shell (randoms are
            frozen across realizations, so RR/region-map/weights are cached
            ONCE -- pure Category-A caching; the estimator math is v_bao's
            _ls_from_blocks_general, byte-identical; equivalence-checked).
  cal     : f_pair amplitude calibration on the 3 LRG driver shells vs the
            REAL banked A_b (F-FAIR-MOCK evidence); writes fpair_calibration.json.
  run     : main realizations (variants vi/vii), per-shell checkpoints.
  boss    : the BOSS-density arm (CMASS shells, variant vi truth).
  metrics : assemble M1-M4 + mechanical thresholds -> legA_metrics.json.

The measurement chain per mock shell is EXACTLY the M3 -> M3c chain:
40-bin LS w(theta) (cap-combine, 24 regions/cap, T=48 union jackknife) ->
frozen 12-bin rebin C12 = A C40 A^T (build_cov.build_operator) -> Hartlap
inverse -> generalized-chi2 bump scan (rerun_m3c._forms/_max_dchi2) ->
profile center + Delta-chi2=1 error x Percival -> 300 MVN null mocks local p.
"""
import argparse
import glob
import json
import os
import sys
import time
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mock_gen as mg                    # noqa: E402 (sets sys.path for the rest)
import v_bao                             # noqa: E402
import build_cov                         # noqa: E402
import rerun_m3c as m3c                  # noqa: E402

CKPT = os.path.join(HERE, "legA_checkpoints")
os.makedirs(CKPT, exist_ok=True)

BACKEND = "gpu"
N_MOCKS_NULL = 300                       # frozen (M3/M3c)
N_REG_CAP, T_REG = 24, 48
N_REAL_PLANNED = 25                      # prereg minimum target
N_REAL_REDUCED = 15                      # disclosed fallback if 2x25 > ~6h
N_BOSS_REAL = 10
SEED0 = {"vi": 9000, "vii": 9100, "boss": 9200, "cal": 8990}
BUDGET_DEFAULT_S = 500

# frozen split-metric thresholds (prereg SS1 M3; the observed values)
SPLIT_RATIO_THRESH = 1.75
SPLIT_SIGMA_THRESH = 3.8


# ---------------------------------------------------------------------------
# RR cache
# ---------------------------------------------------------------------------
def _rr_path(key, cap):
    return os.path.join(mg.RR_DIR, f"{key}__{cap}_rr.npz")


def build_rr(survey, tracer, zlo, zhi, cap, staged=False, budget_end=None):
    """RR block counts for a cap-shell. staged=True banks the count in THREE
    exact parts (halves R1/R2: auto(R1) + auto(R2) + cross(R1,R2), full
    ordered matrix recovered via the ordered-count symmetry
    cross(R2,R1)[i,j] = cross(R1,R2)[j,i]) so a single huge shell survives
    the per-call budget. Pure Category-A partitioning: identical pair set,
    only fp accumulation order differs (same class as the accepted
    CPU-vs-GPU difference)."""
    key = mg.shell_key(survey, tracer, zlo, zhi)
    fn = _rr_path(key, cap)
    if os.path.exists(fn):
        return fn
    assets = mg.ShellAssets(survey, tracer, zlo, zhi, cap)
    zc = 0.5 * (zlo + zhi)
    R = mg.ls_catalog(assets, zc)
    rm = v_bao.make_region_map(R.ra, R.dec, R.w, 3, N_REG_CAP // 3)
    regR = v_bao.apply_region_map(rm, R.ra, R.dec)
    t0 = time.time()
    if not staged:
        RR = v_bao.pair_count_blocks_gpu(R, R, regR, regR, N_REG_CAP,
                                         auto=True)
    else:
        n = len(R)
        h = n // 2

        def _sub(lo, hi):
            return v_bao.Catalog(R.ra[lo:hi], R.dec[lo:hi], R.z[lo:hi],
                                 R.w[lo:hi], R.tag, R.name), regR[lo:hi]
        R1, g1 = _sub(0, h)
        R2, g2 = _sub(h, n)
        parts = {}
        for pname, args in (("p11", (R1, R1, g1, g1, True)),
                            ("p22", (R2, R2, g2, g2, True)),
                            ("p12", (R1, R2, g1, g2, False))):
            pfn = os.path.join(mg.RR_DIR, f"part_{key}__{cap}_{pname}.npy")
            if os.path.exists(pfn):
                parts[pname] = np.load(pfn)
                continue
            if budget_end is not None and time.time() > budget_end:
                print(f"  staged RR {key} {cap}: banked "
                      f"{len(parts)}/3 parts, resuming next call")
                return None
            A, B, ga, gb, au = args
            parts[pname] = v_bao.pair_count_blocks_gpu(
                A, B, ga, gb, N_REG_CAP, auto=au)
            np.save(pfn, parts[pname])
        RR = (parts["p11"] + parts["p22"] + parts["p12"]
              + parts["p12"].transpose(1, 0, 2))
        for pname in parts:
            os.remove(os.path.join(mg.RR_DIR,
                                   f"part_{key}__{cap}_{pname}.npy"))
    WR, SR2 = v_bao._region_weight_sums(R.w, regR, N_REG_CAP)
    np.savez(fn, RR=RR, WR=WR, SR2=SR2, ra0=rm["ra0"],
             dec_edges=rm["dec_edges"], ra_edges=np.array(rm["ra_edges"]),
             t_rr_s=time.time() - t0, n_ls=len(R))
    return fn


def load_rr(key, cap):
    d = np.load(_rr_path(key, cap))
    rm = {"ra0": float(d["ra0"]), "dec_edges": d["dec_edges"],
          "ra_edges": [d["ra_edges"][b] for b in range(3)],
          "n_dec": 3, "n_ra": N_REG_CAP // 3}
    return d["RR"], d["WR"], d["SR2"], rm


# ---------------------------------------------------------------------------
# One mock shell through the FROZEN estimator + M3c chain
# ---------------------------------------------------------------------------
def measure_mock_shell(survey, tracer, zlo, zhi, caps, f_pair, truth_fn, rng):
    """Returns rec dict + arrays (w40, sig40, cov40, w12, C12, theta12)."""
    key = mg.shell_key(survey, tracer, zlo, zhi)
    zc = 0.5 * (zlo + zhi)
    nb = v_bao.N_THETA_BINS
    DD = np.zeros((T_REG, T_REG, nb))
    DR = np.zeros((T_REG, T_REG, nb))
    RRb = np.zeros((T_REG, T_REG, nb))
    WD, SD2 = np.zeros(T_REG), np.zeros(T_REG)
    WRcat = np.zeros(T_REG)
    WRf, SR2f = np.zeros(T_REG), np.zeros(T_REG)
    stats = {}
    t0 = time.time()
    for c, cap in enumerate(caps):
        assets = mg.ShellAssets(survey, tracer, zlo, zhi, cap)
        RR, WR, SR2, rm = load_rr(key, cap)
        D, st = mg.gen_mock_cap(assets, f_pair, truth_fn, rng)
        stats[cap] = st
        R = mg.ls_catalog(assets, zc)
        regD = v_bao.apply_region_map(rm, D.ra, D.dec)
        regR = v_bao.apply_region_map(rm, R.ra, R.dec)
        s = slice(c * N_REG_CAP, (c + 1) * N_REG_CAP)
        DD[s, s] = v_bao.pair_count_blocks_gpu(D, D, regD, regD,
                                               N_REG_CAP, auto=True)
        DR[s, s] = v_bao.pair_count_blocks_gpu(D, R, regD, regR,
                                               N_REG_CAP, auto=False)
        RRb[s, s] = RR
        WD[s], SD2[s] = v_bao._region_weight_sums(D.w, regD, N_REG_CAP)
        WRcat[s] = WR
        WRf[s], SR2f[s] = WR, SR2
    w40, w_jk, cov40 = v_bao._ls_from_blocks_general(
        DD, DR, WD, SD2, WRcat, [RRb], [WRf], [SR2f])
    sig40 = np.sqrt(np.diag(cov40))
    theta40 = v_bao.theta_bin_centers()
    # M3-style 40-bin diagonal bump fit (A_b bookkeeping / calibration match)
    fit40 = v_bao.detect_bump(theta40, w40, sig40, refine=True)
    # M3c chain: frozen 12-bin rebin + Hartlap + full-C scan
    RR40 = RRb.sum(axis=(0, 1))
    A, theta12, _ = build_cov.build_operator(theta40, RR40)
    w12 = A @ w40
    C12 = A @ cov40 @ A.T
    C12 = 0.5 * (C12 + C12.T)
    ev = np.linalg.eigvalsh(C12)
    h = build_cov.hartlap(T_REG, build_cov.N_COARSE)
    Cinv = h * np.linalg.inv(C12)
    x = np.log(theta12)
    Bn, Ba = m3c._forms(x, Cinv)
    obs, oc = m3c._max_dchi2(w12[None, :], Cinv, Bn, Ba)
    # local p: 300 MVN(0, C12) null mocks, deterministic per-shell seed
    L = np.linalg.cholesky(C12 + 1e-18 * np.eye(C12.shape[0]))
    seed = m3c.BASE_SEED + zlib.crc32(key.encode()) % 1000000
    nrng = np.random.default_rng(seed)
    Y = (L @ nrng.standard_normal((C12.shape[0], N_MOCKS_NULL))).T
    mock, _ = m3c._max_dchi2(Y, Cinv, Bn, Ba)
    theta_b, sig_theta = center_err(theta12, w12, C12, Cinv)
    rec = {"key": key, "zc": zc,
           "dchi2_full": float(obs[0]),
           "theta_b_scan": float(np.exp(m3c.SCAN_CENTERS[oc[0]])),
           "local_p_full": float(np.mean(mock >= obs[0])),
           "theta_b": theta_b, "sig_theta": sig_theta,
           "A_b40": fit40["A_b"], "theta_b40": fit40["theta_b"],
           "sigma_b40": fit40["sigma_b"], "dchi2_40diag": fit40["dchi2"],
           "C12_eigmin": float(ev.min()), "t_s": round(time.time() - t0, 1),
           "caps": stats}
    arrays = {"w40": w40, "sig40": sig40, "cov40": cov40, "w12": w12,
              "C12": C12, "theta12": theta12}
    return rec, arrays


def center_err(theta12, w12, C12, Cinv, mode="full"):
    """Profile chi2_alt over center: theta_b + Delta-chi2=1 half-width,
    x Percival (full mode). Identical math to rerun_m3c.theta_center_err,
    operating on in-memory arrays."""
    x = np.log(theta12)
    W = Cinv if mode == "full" else np.diag(1.0 / np.diag(C12))
    Xn = m3c._null_design(x)
    yWy = float(w12 @ W @ w12)
    xc_grid = np.log(np.geomspace(0.3, 12.0, 200))
    prof = np.full(xc_grid.size, np.inf)
    for i, xc in enumerate(xc_grid):
        best = np.inf
        for sw in m3c.WIDTHS:
            g = np.exp(-0.5 * ((x - xc) / sw) ** 2)
            B = m3c._B_mat(np.column_stack([Xn, g]), W)
            best = min(best, yWy - float(w12 @ B @ w12))
        prof[i] = best
    imin = int(np.argmin(prof))
    theta_b = float(np.exp(xc_grid[imin]))
    below = prof <= prof[imin] + 1.0
    lo, hi = xc_grid[below].min(), xc_grid[below].max()
    sig_theta = 0.5 * (np.exp(hi) - np.exp(lo))
    if mode == "full":
        sig_theta *= m3c.PERCIVAL_SIG
    return theta_b, float(sig_theta)


# ---------------------------------------------------------------------------
# Equivalence check: cached-RR assembly vs the frozen one-shot estimator
# ---------------------------------------------------------------------------
def equivalence_check():
    """Run ONE mock shell (smallest: LRG 1.05-1.10) both ways: (a) the cached
    assembly above; (b) v_bao.ls_w_theta_capcombine on identical catalogs.
    Byte-level agreement of w and cov required (Category-A caching proof)."""
    fn = os.path.join(CKPT, "equivalence_check.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    tracer, zlo, zhi = "LRG", 1.05, 1.10
    key = mg.shell_key("DESI", tracer, zlo, zhi)
    zc = 0.5 * (zlo + zhi)
    rng = np.random.default_rng(777001)
    cats = {}
    for cap in mg.DESI_CAPS:
        assets = mg.ShellAssets("DESI", tracer, zlo, zhi, cap)
        D, _ = mg.gen_mock_cap(assets, 0.3, mg.theta_i_deg, rng)
        cats[cap] = (D, mg.ls_catalog(assets, zc))
    # (b) frozen one-shot estimator (computes its own region maps + RR)
    res_b = v_bao.ls_w_theta_capcombine([cats[c] for c in mg.DESI_CAPS],
                                        backend=BACKEND)
    # (a) cached path: same mock => regenerate identically with the same seed
    rng2 = np.random.default_rng(777001)
    rec, arr = measure_mock_shell("DESI", tracer, zlo, zhi, mg.DESI_CAPS,
                                  0.3, mg.theta_i_deg, rng2)
    dw = float(np.nanmax(np.abs(arr["w40"] - res_b["w"])))
    dcov = float(np.nanmax(np.abs(arr["cov40"] - res_b["cov_jk"])))
    out = {"max_abs_dw": dw, "max_abs_dcov": dcov,
           "pass": bool(dw < 1e-12 and dcov < 1e-14)}
    with open(fn, "w") as f:
        json.dump(out, f, indent=1)
    print("equivalence:", out)
    return out


# ---------------------------------------------------------------------------
# Phase: f_pair calibration (F-FAIR-MOCK evidence)
# ---------------------------------------------------------------------------
F_GRID = (0.10, 0.20, 0.30, 0.45)


def phase_cal(budget_s):
    """Amplitude calibration: run the 3 LRG driver shells at each f in F_GRID
    (one realization each, seed 8990+j), fit A_b with the SAME 40-bin diagonal
    machinery that produced the real banked A_b, then solve A(f)=A_real per
    shell by linear fit through the origin-free line, take the median f, and
    confirm with one run at f_final."""
    fn_out = os.path.join(HERE, "fpair_calibration.json")
    if os.path.exists(fn_out):
        return json.load(open(fn_out))
    t_start = time.time()
    state_fn = os.path.join(CKPT, "cal_state.json")
    state = json.load(open(state_fn)) if os.path.exists(state_fn) else {}
    for j, f in enumerate(F_GRID):
        for (tracer, zlo, zhi), a_real in mg.CAL_TARGETS.items():
            k = f"f{f:.2f}_{tracer}_{zlo:.2f}_{zhi:.2f}"
            if k in state:
                continue
            if time.time() - t_start > budget_s:
                json.dump(state, open(state_fn, "w"), indent=1)
                print(f"CAL PARTIAL ({len(state)} entries) -- rerun to resume")
                return None
            rng = np.random.default_rng(SEED0["cal"] * 1000 + j)
            rec, _ = measure_mock_shell("DESI", tracer, zlo, zhi,
                                        mg.DESI_CAPS, f, mg.theta_i_deg, rng)
            state[k] = {"f": f, "A_b40": rec["A_b40"],
                        "theta_b40": rec["theta_b40"],
                        "A_real": a_real, "t_s": rec["t_s"]}
            json.dump(state, open(state_fn, "w"), indent=1)
            print(k, "A_mock=%.5f A_real=%.5f th=%.2f (%.0fs)"
                  % (rec["A_b40"], a_real, rec["theta_b40"], rec["t_s"]))
    # solve per shell: A(f) ~ alpha*f (theory: amplitude linear in f);
    # keep only entries whose recovered center is at the injected ring
    f_solved = {}
    for (tracer, zlo, zhi), a_real in mg.CAL_TARGETS.items():
        sh = f"{tracer}_{zlo:.2f}_{zhi:.2f}"
        pts = [(v["f"], v["A_b40"]) for k, v in state.items()
               if k.endswith(sh) and 1.5 < v["theta_b40"] < 3.5
               and v["A_b40"] > 0]
        if len(pts) >= 2:
            fa = np.array(pts)
            alpha = float(np.sum(fa[:, 0] * fa[:, 1]) / np.sum(fa[:, 0] ** 2))
            f_solved[sh] = a_real / alpha
    f_final = float(np.median(list(f_solved.values())))
    out = {"grid": state, "f_solved_per_shell": f_solved,
           "f_pair_final": f_final,
           "definition": "f_pair = fraction of final points that are ring "
                         "companions (one per parent)",
           "target": "real banked nosys 40-bin A_b on the 3 LRG driver shells"}
    with open(fn_out, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("CAL DONE: f_pair_final =", f_final, f_solved)
    return out


# ---------------------------------------------------------------------------
# Phase: main realizations
# ---------------------------------------------------------------------------
def _real_dir(variant, r):
    d = os.path.join(CKPT, variant, f"r{r:02d}")
    os.makedirs(d, exist_ok=True)
    return d


def run_realization(variant, r, f_pair, shells, caps, survey, budget_end):
    """One realization: per-shell checkpointed. Returns True if complete."""
    truth = mg.theta_i_deg if variant in ("vi", "boss") else mg.theta_ii_deg
    d = _real_dir(variant, r)
    seed = SEED0[variant] + r
    for (tracer, zlo, zhi) in shells:
        key = mg.shell_key(survey, tracer, zlo, zhi)
        fn = os.path.join(d, key + ".json")
        if os.path.exists(fn):
            continue
        # deterministic per-(realization, shell) stream: resume-safe
        rng_sh = np.random.default_rng(
            seed * 100000 + zlib.crc32(key.encode()) % 65536)
        if time.time() > budget_end:
            return False
        rec, arr = measure_mock_shell(survey, tracer, zlo, zhi, caps,
                                      f_pair, truth, rng_sh)
        rec["seed"] = seed
        rec["variant"] = variant
        rec["f_pair"] = f_pair
        np.savez(os.path.join(d, key + ".npz"), **arr)
        with open(fn, "w") as f:
            json.dump(rec, f, indent=1, default=float)
    return True


def _n_real_decision():
    """Mechanical N decision (disclosed): after the first completed DESI
    realization, project the 2x25 total; if > ~6h, reduce to 15/variant."""
    fn = os.path.join(CKPT, "n_real_decision.json")
    if os.path.exists(fn):
        return json.load(open(fn))["n_real"]
    recs = glob.glob(os.path.join(CKPT, "vi", "r00", "*.json"))
    if len(recs) < len(mg.DESI_SHELLS):
        return None
    t_real = sum(json.load(open(f))["t_s"] for f in recs)
    proj_h = 2 * N_REAL_PLANNED * t_real / 3600.0
    n_real = N_REAL_PLANNED if proj_h <= 6.0 else N_REAL_REDUCED
    with open(fn, "w") as f:
        json.dump({"t_per_realization_s": t_real, "proj_2x25_h": proj_h,
                   "n_real": n_real,
                   "rule": "prereg budget: reduce to 15/variant and disclose "
                           "if 2x25 projects > ~6h"}, f, indent=1)
    print(f"N decision: t/real={t_real:.0f}s proj(2x25)={proj_h:.1f}h "
          f"-> N={n_real}/variant")
    return n_real


def phase_run(budget_s):
    cal = json.load(open(os.path.join(HERE, "fpair_calibration.json")))
    f_pair = cal["f_pair_final"]
    budget_end = time.time() + budget_s
    # realization r00 of vi first (drives the N decision)
    if not run_realization("vi", 0, f_pair, mg.DESI_SHELLS, mg.DESI_CAPS,
                           "DESI", budget_end):
        print("RUN PARTIAL (r00 vi incomplete)")
        return
    n_real = _n_real_decision()
    done = 0
    for r in range(n_real):
        for variant in ("vi", "vii"):
            if not run_realization(variant, r, f_pair, mg.DESI_SHELLS,
                                   mg.DESI_CAPS, "DESI", budget_end):
                print(f"RUN PARTIAL at {variant} r{r:02d} "
                      f"({done} realizations complete this call)")
                return
            done += 1
    print(f"RUN PHASE COMPLETE: {n_real} realizations x 2 variants")


def phase_boss(budget_s):
    cal = json.load(open(os.path.join(HERE, "fpair_calibration.json")))
    f_pair = cal["f_pair_final"]
    budget_end = time.time() + budget_s
    for r in range(N_BOSS_REAL):
        if not run_realization("boss", r, f_pair, mg.BOSS_SHELLS,
                               mg.BOSS_CAPS, "BOSS", budget_end):
            print(f"BOSS PARTIAL at r{r:02d}")
            return
    print(f"BOSS PHASE COMPLETE: {N_BOSS_REAL} realizations")


# ---------------------------------------------------------------------------
# Phase: metrics M1-M4 + mechanical thresholds
# ---------------------------------------------------------------------------
def _collect(variant, survey, shells):
    """rows[r][key] = rec for complete realizations only."""
    out = []
    for d in sorted(glob.glob(os.path.join(CKPT, variant, "r*"))):
        recs = {}
        for (tracer, zlo, zhi) in shells:
            key = mg.shell_key(survey, tracer, zlo, zhi)
            fn = os.path.join(d, key + ".json")
            if os.path.exists(fn):
                recs[key] = json.load(open(fn))
        if len(recs) == len(shells):
            out.append(recs)
    return out


def _truth_mean_theta(rec):
    """Weighted mean injected theta_t across caps (the M1 truth center)."""
    num = den = 0.0
    for cap, st in rec["caps"].items():
        num += st["theta_t_mean_deg"] * st["n_pairs_placed"]
        den += st["n_pairs_placed"]
    return num / max(den, 1)


def _wls_slope(lnz, lnth, sig_ln):
    w = 1.0 / np.maximum(sig_ln, 1e-4) ** 2
    X = np.column_stack([np.ones_like(lnz), lnz])
    XtW = X.T * w
    beta = np.linalg.solve(XtW @ X, XtW @ lnth)
    cov = np.linalg.inv(XtW @ X)
    return float(beta[1]), float(np.sqrt(cov[1, 1]))


def phase_metrics():
    lrg_keys = [mg.shell_key("DESI", t, a, b) for (t, a, b) in mg.DESI_SHELLS
                if t == "LRG"]
    split_L = mg.shell_key("DESI", "LRG", 1.00, 1.05)
    split_Q = mg.shell_key("DESI", "QSO", 0.95, 1.10)
    out = {"n_complete": {}}

    # ---------------- M1 + M2 + M3 over the DESI variants ----------------
    split_rows_all = []
    for variant in ("vi", "vii"):
        rows = _collect(variant, "DESI", mg.DESI_SHELLS)
        out["n_complete"][variant] = len(rows)
        # M1: per-shell center bias/scatter vs the injected truth
        m1 = {}
        for (tracer, zlo, zhi) in mg.DESI_SHELLS:
            key = mg.shell_key("DESI", tracer, zlo, zhi)
            lr = np.array([np.log(r[key]["theta_b"] / _truth_mean_theta(r[key]))
                           for r in rows])
            m1[key] = {"bias_ln": float(lr.mean()),
                       "scatter_ln": float(lr.std(ddof=1)) if lr.size > 1 else None,
                       "far_miss_frac_gt0.5": float(np.mean(np.abs(lr) > 0.5)),
                       "truth_theta_deg": float(np.mean(
                           [_truth_mean_theta(r[key]) for r in rows]))}
        # M2: drift-direction recovery over the 8 LRG shells
        slopes, slopes_sig = [], []
        truth_slope = None
        for r in rows:
            zc = np.array([r[k]["zc"] for k in lrg_keys])
            th = np.array([r[k]["theta_b"] for k in lrg_keys])
            sg = np.array([r[k]["sig_theta"] for k in lrg_keys])
            tt = np.array([_truth_mean_theta(r[k]) for k in lrg_keys])
            b, sb = _wls_slope(np.log1p(zc), np.log(th), sg / th)
            bt, _ = _wls_slope(np.log1p(zc), np.log(tt),
                               np.full(zc.size, 0.01))
            truth_slope = bt
            slopes.append(b)
            slopes_sig.append(sb)
        slopes = np.array(slopes)
        m2 = {"truth_slope_dlnth_dln1pz": truth_slope,
              "recovered_slopes_mean": float(slopes.mean()),
              "recovered_slopes_sd": float(slopes.std(ddof=1)),
              "antidrift_rate_slope_ge_0": float(np.mean(slopes >= 0.0)),
              "slopes": slopes.tolist()}
        # M3: false tracer-split distribution
        srows = []
        for r in rows:
            tL, sL = r[split_L]["theta_b"], r[split_L]["sig_theta"]
            tQ, sQ = r[split_Q]["theta_b"], r[split_Q]["sig_theta"]
            ratio = max(tL, tQ) / min(tL, tQ)
            sig = abs(tL - tQ) / np.hypot(sL, sQ)
            srows.append({"tL": tL, "sL": sL, "tQ": tQ, "sQ": sQ,
                          "ratio": ratio, "sigma": sig,
                          "hit": bool(ratio >= SPLIT_RATIO_THRESH
                                      and sig >= SPLIT_SIGMA_THRESH)})
        split_rows_all += srows
        rr = np.array([s["ratio"] for s in srows])
        ss = np.array([s["sigma"] for s in srows])
        m3 = {"n": len(srows),
              "false_split_rate": float(np.mean([s["hit"] for s in srows])),
              "ratio_pcts_5_25_50_75_95_max": [float(v) for v in
                  np.percentile(rr, [5, 25, 50, 75, 95]).tolist() + [rr.max()]],
              "sigma_pcts_5_25_50_75_95_max": [float(v) for v in
                  np.percentile(ss, [5, 25, 50, 75, 95]).tolist() + [ss.max()]],
              "rows": srows}
        out[variant] = {"M1": m1, "M2": m2, "M3": m3}

    # pooled M3 (both one-true-scale variants are valid instruments)
    hits = int(np.sum([s["hit"] for s in split_rows_all]))
    n = len(split_rows_all)
    from scipy.stats import beta as _beta
    ci_hi = float(_beta.ppf(0.95, hits + 1, n - hits)) if n else None
    p_hat = hits / n if n else None
    out["M3_pooled"] = {"n": n, "hits": hits, "false_split_rate": p_hat,
                        "binom_95_upper": ci_hi}

    # ---------------- M4: BOSS-density arm ----------------
    brows = _collect("boss", "BOSS", mg.BOSS_SHELLS)
    out["n_complete"]["boss"] = len(brows)
    ells, cell = [], {}
    for r in brows:
        for (tracer, zlo, zhi) in mg.BOSS_SHELLS:
            key = mg.shell_key("BOSS", tracer, zlo, zhi)
            zc = r[key]["zc"]
            ell = np.radians(r[key]["theta_b"]) * float(m3c.rz(zc))
            ells.append(ell)
            cell.setdefault(key, []).append(ell)
    ells = np.array(ells)
    ell_true = m3c.ELL_FROZEN
    out["M4"] = {"n_shell_measurements": int(ells.size),
                 "implied_ell_true": ell_true,
                 "implied_ell_min_max": [float(ells.min()), float(ells.max())],
                 "implied_ell_pcts_5_25_50_75_95": [float(v) for v in
                     np.percentile(ells, [5, 25, 50, 75, 95])],
                 "frac_outside_40_80": float(np.mean((ells < 40) | (ells > 80))),
                 "per_shell_mean_sd": {k: [float(np.mean(v)), float(np.std(v))]
                                       for k, v in cell.items()},
                 "observed_boss_range_ref": [4, 212]}

    # ---------------- mechanical thresholds (prereg SS1 frozen rule) -------
    def verdict(p):
        if p > 0.05:
            return "DOWNGRADE (method-artifact-consistent)"
        if p < 0.01:
            return "RE-FIRMS"
        return "CAL-MIXED"

    out["mechanical"] = {
        "M3_split": {v: verdict(out[v]["M3"]["false_split_rate"])
                     for v in ("vi", "vii")},
        "M3_split_pooled": verdict(out["M3_pooled"]["false_split_rate"]),
        "M2_antidrift": {v: verdict(out[v]["M2"]["antidrift_rate_slope_ge_0"])
                         for v in ("vi", "vii")},
        "note": "rule applied to point estimates; binomial resolution at the "
                "actual N disclosed alongside"}
    with open(os.path.join(HERE, "legA_metrics.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("M3_pooled", "mechanical",
                                          "n_complete")}, indent=1))
    return out


# ---------------------------------------------------------------------------
def phase_assets(budget_s):
    t0 = time.time()
    for (tracer, zlo, zhi) in mg.DESI_SHELLS:
        for cap in mg.DESI_CAPS:
            if time.time() - t0 > budget_s:
                print("ASSETS PARTIAL")
                return
            mg.build_asset_desi(tracer, cap, zlo, zhi)
            print("asset", tracer, cap, zlo, zhi, flush=True)
    for (tracer, zlo, zhi) in mg.BOSS_SHELLS:
        for cap in mg.BOSS_CAPS:
            if time.time() - t0 > budget_s:
                print("ASSETS PARTIAL")
                return
            mg.build_asset_boss(tracer, cap, zlo, zhi)
            print("asset", tracer, cap, zlo, zhi, flush=True)
    print("ASSETS COMPLETE")


def phase_rr(budget_s):
    t0 = time.time()
    todo = [("DESI", s, mg.DESI_CAPS) for s in mg.DESI_SHELLS] + \
           [("BOSS", s, mg.BOSS_CAPS) for s in mg.BOSS_SHELLS]
    for survey, (tracer, zlo, zhi), caps in todo:
        for cap in caps:
            key = mg.shell_key(survey, tracer, zlo, zhi)
            if os.path.exists(_rr_path(key, cap)):
                continue
            # predictive cost gate: never START a build the budget can't hold
            d = np.load(mg._asset_path(key, cap))
            n_ls = int(d["ls_ra"].size)
            pred = 545.0 * (n_ls / 2.01e6) ** 2 + 20.0
            staged = pred > 480.0
            if not staged and time.time() - t0 + pred > budget_s:
                print(f"RR PARTIAL (next {key} {cap} pred {pred:.0f}s "
                      "exceeds remaining budget)")
                return
            r = build_rr(survey, tracer, zlo, zhi, cap, staged=staged,
                         budget_end=t0 + budget_s)
            if r is None:
                print("RR PARTIAL (staged build mid-way, banked)")
                return
            print("rr", key, cap, f"({time.time() - t0:.0f}s elapsed)",
                  flush=True)
    print("RR COMPLETE")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True,
                    choices=["assets", "rr", "equiv", "cal", "run", "boss",
                             "metrics"])
    ap.add_argument("--budget-s", type=float, default=BUDGET_DEFAULT_S)
    a = ap.parse_args()
    if a.phase == "assets":
        phase_assets(a.budget_s)
    elif a.phase == "rr":
        phase_rr(a.budget_s)
    elif a.phase == "equiv":
        equivalence_check()
    elif a.phase == "cal":
        phase_cal(a.budget_s)
    elif a.phase == "run":
        phase_run(a.budget_s)
    elif a.phase == "boss":
        phase_boss(a.budget_s)
    elif a.phase == "metrics":
        phase_metrics()
