#!/usr/bin/env python3
"""M3c STEP 3: re-fit under the proper FULL bin-bin covariance (12-bin frozen).

For every shell/variant we replace the M3 DIAGONAL weighting with the full
Hartlap-corrected inverse covariance C^-1 (built by build_cov.py from the banked
region jackknife).  We recompute, at MATCHED 12-bin binning, both:
  BEFORE = diagonal-only weighting (M2/M3 condition, no off-diagonals);
  AFTER  = full C^-1 (Hartlap on the inverse) + Percival on parameter errors.
So the before/after isolates EXACTLY the effect of proper covariance.

(a) per-shell bump dchi2 + local p (null mocks drawn under C12) + global
    trials-corrected p (per survey), DESI + BOSS.
(b) THE tracer split: LRG 1.00-1.05 vs QSO 0.95-1.10 at zc~1.02 -- theta_b and
    its center error before vs after; split significance in sigma.
(c) ell=58.34 threading chi2/dof on the DESI PRIMARY SKY-ROBUST set + BOSS,
    with center errors from the full-C fit.
Frozen scan: 40 fine log-centers x width grid (0.10,0.20,0.35,0.60) in ln-theta,
identical trials to M3; null recalibrated by drawing y~MVN(0,C12) (seed 20260807).
"""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COV = os.path.join(HERE, "cov_out")
N_REG, N_BINS = 48, 12
N_MOCKS = 300
BASE_SEED = 20260807
WIDTHS = (0.10, 0.20, 0.35, 0.60)
SCAN_CENTERS = np.log(np.geomspace(0.3, 12.0, 40))    # frozen full-window scan
DEG = math.pi / 180.0

# --- Percival parameter-error factor (variance), n_par=6 (cubic4+A+center) ---
_A = 2.0 / ((N_REG - N_BINS - 1.0) * (N_REG - N_BINS - 4.0))
_B = (N_REG - N_BINS - 2.0) / ((N_REG - N_BINS - 1.0) * (N_REG - N_BINS - 4.0))
PERCIVAL_M = (1.0 + _B * (N_BINS - 6)) / (1.0 + _A + _B * (6 + 1))
PERCIVAL_SIG = math.sqrt(PERCIVAL_M)

# --- frozen ruler (measure_ell.py / FROZEN_PREDICTION.md) ---
ELL_FROZEN = 58.34
INV_N, XEFF = 0.947, 2086.0
N_PROF = 1.0 / INV_N
RW = N_PROF * XEFF


def rz(z):
    return RW * (1.0 - (1.0 + z) ** (-2.0 / N_PROF))


def theta_pred_deg(z):
    return ELL_FROZEN / rz(z) / DEG


def load(tag, key):
    d = np.load(os.path.join(COV, f"{tag}__{key}.npz"))
    return d["theta"], d["w"], d["cov"], d["cinv_hartlap"]


def _null_design(x):
    return np.vander(x - x.mean(), 4, increasing=True)


def _B_mat(X, W):
    WX = W @ X
    return WX @ np.linalg.solve(X.T @ WX, WX.T)


def _forms(x, W):
    """B_null and B_alt[c][w] projection matrices for chi2 = yWy - yBy."""
    Xn = _null_design(x)
    Bn = _B_mat(Xn, W)
    Ba = []
    for xc in SCAN_CENTERS:
        row = []
        for sw in WIDTHS:
            g = np.exp(-0.5 * ((x - xc) / sw) ** 2)
            row.append(_B_mat(np.column_stack([Xn, g]), W))
        Ba.append(row)
    return Bn, Ba


def _max_dchi2(Y, W, Bn, Ba):
    """Y: (m, nbin). Returns (m,) max dchi2 over the scan and per-mock argmax."""
    q0 = np.einsum("mi,ij,mj->m", Y, Bn, Y)
    best = np.full(Y.shape[0], -np.inf)
    argc = np.zeros(Y.shape[0], dtype=int)
    for ci, row in enumerate(Ba):
        for B in row:
            q = np.einsum("mi,ij,mj->m", Y, B, Y) - q0
            upd = q > best
            best[upd] = q[upd]
            argc[upd] = ci
    return best, argc


def fit_shell(tag, key, variant, mode):
    """mode='full' or 'diag'. Returns dict with dchi2, theta_b, local_p, mocks."""
    theta, w, C, Cinv = load(tag, f"{key}_{variant}")
    x = np.log(theta)
    if mode == "full":
        W = Cinv
    else:
        W = np.diag(1.0 / np.diag(C))
    Bn, Ba = _forms(x, W)
    obs, oc = _max_dchi2(w[None, :], W, Bn, Ba)
    obs_dchi2 = float(obs[0])
    theta_b = float(np.exp(SCAN_CENTERS[oc[0]]))
    # null mocks ~ MVN(0, C); per-shell INDEPENDENT deterministic seed so the
    # global trials-corrected max is over independent shells (crc32, stable).
    import zlib
    L = np.linalg.cholesky(C + 1e-18 * np.eye(C.shape[0]))
    seed = BASE_SEED + zlib.crc32((key + variant).encode()) % 1000000
    rng = np.random.default_rng(seed)
    Y = (L @ rng.standard_normal((C.shape[0], N_MOCKS))).T
    mock, _ = _max_dchi2(Y, W, Bn, Ba)
    local_p = float(np.mean(mock >= obs_dchi2))
    return {"key": key, "variant": variant, "mode": mode,
            "dchi2": obs_dchi2, "theta_b": theta_b, "local_p": local_p,
            "mock_max": mock}


def theta_center_err(tag, key, variant, mode):
    """Profile chi2_alt over center -> theta_b and Delta-chi2=1 half-width."""
    theta, w, C, Cinv = load(tag, f"{key}_{variant}")
    x = np.log(theta)
    W = Cinv if mode == "full" else np.diag(1.0 / np.diag(C))
    Xn = _null_design(x)
    yWy = float(w @ W @ w)
    # fine center grid for a smooth profile
    xc_grid = np.log(np.geomspace(0.3, 12.0, 200))
    prof = np.full(xc_grid.size, np.inf)
    for i, xc in enumerate(xc_grid):
        best = np.inf
        for sw in WIDTHS:
            g = np.exp(-0.5 * ((x - xc) / sw) ** 2)
            B = _B_mat(np.column_stack([Xn, g]), W)
            best = min(best, yWy - float(w @ B @ w))
        prof[i] = best
    imin = int(np.argmin(prof))
    chi2min = prof[imin]
    theta_b = float(np.exp(xc_grid[imin]))
    thr = chi2min + 1.0
    below = prof <= thr
    lo = xc_grid[below].min()
    hi = xc_grid[below].max()
    sig_theta = 0.5 * (math.exp(hi) - math.exp(lo))
    if mode == "full":
        sig_theta *= PERCIVAL_SIG
    return theta_b, float(sig_theta)


def detection(tag, keys, variants=("nosys", "sys")):
    out = {}
    for v in variants:
        rows = {}
        for k in keys:
            rf = fit_shell(tag, k, v, "full")
            rd = fit_shell(tag, k, v, "diag")
            rows[k] = {"dchi2_diag": rd["dchi2"], "dchi2_full": rf["dchi2"],
                       "theta_b_full": rf["theta_b"],
                       "local_p_diag": rd["local_p"],
                       "local_p_full": rf["local_p"],
                       "mock_full": rf["mock_max"]}
        # global trials-corrected p (full), per survey
        obs = np.array([rows[k]["dchi2_full"] for k in keys])
        M = np.vstack([rows[k]["mock_full"] for k in keys])     # (nshell, nmock)
        gdist = M.max(axis=0)
        gp = float(np.mean(gdist >= obs.max()))
        for k in keys:
            rows[k].pop("mock_full")
        out[v] = {"global_p_full": gp, "glob_max_full": float(obs.max()),
                  "shells": rows}
    return out


def main():
    log = []

    def P(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.append(s)

    P("M3c RE-FIT under FULL covariance (12 bins, N_reg=48)")
    P(f"Hartlap=0.7234  Percival_m={PERCIVAL_M:.4f} (sig x{PERCIVAL_SIG:.4f})")

    desi_keys = sorted({os.path.basename(f).split("__")[1].rsplit("_", 1)[0]
                        for f in glob.glob(os.path.join(COV, "DESI__*_nosys.npz"))})
    boss_keys = sorted({os.path.basename(f).split("__")[1].rsplit("_", 1)[0]
                        for f in glob.glob(os.path.join(COV, "BOSS__*_nosys.npz"))})

    # ---- (a) detection ----
    P("\n== (a) DETECTION: global trials-corrected p (full C) ==")
    det = {"DESI": detection("DESI", desi_keys),
           "BOSS": detection("BOSS", boss_keys)}
    for tag in ("DESI", "BOSS"):
        for v in ("nosys", "sys"):
            d = det[tag][v]
            P(f"  {tag} {v}: global_p_full={d['global_p_full']:.4f}  "
              f"glob_max_full={d['glob_max_full']:.2f}  "
              f"detected(<0.01)={d['global_p_full']<0.01}")

    # strong driver shells: before/after
    P("\n  driver shells (nosys) dchi2 diag->full, local_p diag->full:")
    for k in ["LRG_0.90_0.95", "LRG_0.95_1.00", "LRG_1.00_1.05",
              "LRG_1.05_1.10", "QSO_0.95_1.10", "LRG_0.70_0.75"]:
        r = det["DESI"]["nosys"]["shells"][k]
        P(f"    {k:16s} dchi2 {r['dchi2_diag']:6.2f}->{r['dchi2_full']:6.2f}  "
          f"localp {r['local_p_diag']:.3f}->{r['local_p_full']:.3f}  "
          f"th_b={r['theta_b_full']:.2f}")
    for k in ["CMASS_0.53_0.58", "CMASS_0.48_0.53", "CMASS_0.43_0.48"]:
        r = det["BOSS"]["nosys"]["shells"][k]
        P(f"    {k:16s} dchi2 {r['dchi2_diag']:6.2f}->{r['dchi2_full']:6.2f}  "
          f"localp {r['local_p_diag']:.3f}->{r['local_p_full']:.3f}  "
          f"th_b={r['theta_b_full']:.2f}")

    # ---- (b) tracer split ----
    P("\n== (b) TRACER SPLIT: LRG_1.00_1.05 vs QSO_0.95_1.10 (zc~1.02) ==")
    split = {}
    for v in ("nosys", "sys"):
        res = {}
        for mode in ("diag", "full"):
            tL, sL = theta_center_err("DESI", "LRG_1.00_1.05", v, mode)
            tQ, sQ = theta_center_err("DESI", "QSO_0.95_1.10", v, mode)
            dsig = abs(tL - tQ) / math.sqrt(sL**2 + sQ**2)
            res[mode] = dict(tL=tL, sL=sL, tQ=tQ, sQ=sQ, split_sigma=dsig)
            P(f"  {v} {mode}: LRG th={tL:.3f}+/-{sL:.3f}  "
              f"QSO th={tQ:.3f}+/-{sQ:.3f}  -> split={dsig:.2f} sigma")
        split[v] = res
    P(f"  (M3 original 40-bin diagonal: LRG th=2.44, QSO th=1.39)")

    # ---- (c) threading ----
    P("\n== (c) THREADING ell=58.34 on DESI PRIMARY SKY-ROBUST set (full C) ==")
    prim = ["LRG_0.70_0.75", "LRG_1.00_1.05", "QSO_0.95_1.10"]
    thread = {}
    for v in ("sys", "nosys"):
        rows = []
        for k in prim:
            zc = {"LRG_0.70_0.75": 0.725, "LRG_1.00_1.05": 1.025,
                  "QSO_0.95_1.10": 1.025}[k]
            tb, sc = theta_center_err("DESI", k, v, "full")
            rows.append((k, zc, tb, sc))
        # chi2 at fixed frozen ell
        chi2_fixed = sum(((tb - theta_pred_deg(zc)) / sc) ** 2
                         for _, zc, tb, sc in rows)
        # best-fit ell threading
        kk = np.array([1.0 / rz(zc) / DEG for _, zc, _, _ in rows])
        yy = np.array([tb for _, _, tb, _ in rows])
        ss = np.array([sc for _, _, _, sc in rows])
        wv = 1.0 / ss**2
        ell_bf = float(np.sum(yy * kk * wv) / np.sum(kk * kk * wv))
        chi2_bf = float(np.sum(((yy - ell_bf * kk) / ss) ** 2))
        dof = len(rows) - 1
        thread[v] = dict(chi2_fixed=float(chi2_fixed), ell_bf=ell_bf,
                         chi2_bf=chi2_bf, dof=dof,
                         rows=[(k, zc, tb, sc) for k, zc, tb, sc in rows])
        P(f"  {v}: chi2(ell=58.34 fixed)={chi2_fixed:.1f}/{len(rows)}   "
          f"best-fit ell={ell_bf:.2f}  chi2/dof={chi2_bf:.1f}/{dof}="
          f"{chi2_bf/dof:.1f}   (M3b diag PRIMARY sys: 288.4/2=144.2)")

    # BOSS threading: within test with full-C center errors
    P("\n  BOSS prediction 'within' test (full-C center errors):")
    boss_within = {}
    for v in ("sys", "nosys"):
        nwin = 0
        rws = []
        for k in boss_keys:
            zc = float(k.split("_")[1]) + 0.025  # bin low edge +half of 0.05
            zc = {"CMASS_0.43_0.48": 0.455, "CMASS_0.48_0.53": 0.505,
                  "CMASS_0.53_0.58": 0.555, "CMASS_0.58_0.63": 0.605,
                  "CMASS_0.63_0.68": 0.655, "LOWZ_0.20_0.25": 0.225,
                  "LOWZ_0.25_0.30": 0.275, "LOWZ_0.30_0.35": 0.325,
                  "LOWZ_0.35_0.40": 0.375}[k]
            tb, sc = theta_center_err("BOSS", k, v, "full")
            within = abs(tb - theta_pred_deg(zc)) <= sc
            nwin += int(within)
            rws.append((k, zc, tb, sc, theta_pred_deg(zc), bool(within)))
        boss_within[v] = dict(n_within=nwin, n_shells=len(boss_keys), rows=rws)
        P(f"  {v}: n_within(frozen ell, full-C err)={nwin}/{len(boss_keys)}")

    out = {"hartlap": 0.7234, "percival_m": PERCIVAL_M,
           "detection": {t: {v: {kk: vv for kk, vv in det[t][v].items()
                                 if kk != "shells"} | {"shells": det[t][v]["shells"]}
                             for v in det[t]} for t in det},
           "tracer_split": split, "threading_desi": thread,
           "boss_within": {v: {"n_within": boss_within[v]["n_within"],
                               "n_shells": boss_within[v]["n_shells"]}
                           for v in boss_within}}
    with open(os.path.join(HERE, "m3c_refit_results.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    with open(os.path.join(HERE, "run_output.txt"), "w") as f:
        f.write("\n".join(log) + "\n")
    P("\nDONE -> m3c_refit_results.json, run_output.txt")


if __name__ == "__main__":
    main()
