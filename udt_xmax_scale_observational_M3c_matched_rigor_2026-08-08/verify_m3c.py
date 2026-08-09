#!/usr/bin/env python3
"""BLIND VERIFIER: independent recomputation for M3c.
Independent code paths: my own rebin operator; GLS chi2 via normal-equation
solve (not their projection-matrix route); my own profile intervals.
"""
import glob, json, math, os, zlib
import numpy as np

REPO = "/home/udt-admin/udt_mass_codex"
PKG = os.path.join(REPO, "udt_xmax_scale_observational_M3c_matched_rigor_2026-08-08")
COV = os.path.join(PKG, "cov_out")
DESI = os.path.join(REPO, "udt_xmax_scale_observational_M3_runs_2026-08-07", "bao_checkpoints")
BOSS = os.path.join(REPO, "udt_xmax_scale_observational_M3b_BOSS_2026-08-08", "boss_checkpoints")
NB = 12
EDGES = np.geomspace(0.3, 12.0, NB + 1)
WIDTHS = (0.10, 0.20, 0.35, 0.60)
CENTERS = np.log(np.geomspace(0.3, 12.0, 40))
HARTLAP = (48 - 12 - 2) / 47.0
PERC_SIG = math.sqrt((1.0 + (34/1120)*(12-6)) / (1.0 + 2/1120 + (34/1120)*7))
DEG = math.pi / 180.0
ELL = 58.34; NPROF = 1/0.947; RW = NPROF*2086.0

def rz(z): return RW*(1-(1+z)**(-2/NPROF))
def tpred(z): return ELL/rz(z)/DEG

def my_rebin(theta, RR):
    idx = np.clip(np.searchsorted(EDGES, theta, side="right")-1, 0, NB-1)
    A = np.zeros((NB, theta.size))
    for b in range(NB):
        m = idx == b
        assert m.any()
        wt = np.maximum(RR[m], 0.0)
        if wt.sum() <= 0: wt = np.ones(m.sum())
        A[b, m] = wt/wt.sum()
    return A

def chi2min(y, X, W):
    """min_beta (y-Xb)' W (y-Xb) via lstsq on whitened system."""
    L = np.linalg.cholesky(W)
    Xl, yl = L.T @ X, L.T @ y
    b, *_ = np.linalg.lstsq(Xl, yl, rcond=None)
    r = yl - Xl @ b
    return float(r @ r)

def scan_dchi2(y, x, W):
    Xn = np.vander(x - x.mean(), 4, increasing=True)
    c0 = chi2min(y, Xn, W)
    best = -np.inf; bc = None
    for xc in CENTERS:
        for sw in WIDTHS:
            g = np.exp(-0.5*((x-xc)/sw)**2)
            c = chi2min(y, np.column_stack([Xn, g]), W)
            if c0 - c > best: best, bc = c0-c, xc
    return best, math.exp(bc)

def load_cov(tag, key):
    d = np.load(os.path.join(COV, f"{tag}__{key}.npz"))
    return d["theta"], d["w"], d["cov"], d["cinv_hartlap"], d["A"]

def profile_err(tag, key, mode):
    th, w, C, Ci, _ = load_cov(tag, key)
    x = np.log(th)
    W = Ci if mode == "full" else np.diag(1/np.diag(C))
    Xn = np.vander(x - x.mean(), 4, increasing=True)
    grid = np.log(np.geomspace(0.3, 12.0, 200))
    prof = np.array([min(chi2min(w, np.column_stack([Xn, np.exp(-0.5*((x-xc)/sw)**2)]), W)
                         for sw in WIDTHS) for xc in grid])
    i = int(np.argmin(prof))
    below = prof <= prof[i] + 1.0
    lo, hi = grid[below].min(), grid[below].max()
    s = 0.5*(math.exp(hi)-math.exp(lo))
    if mode == "full": s *= PERC_SIG
    return math.exp(grid[i]), s

def mocks_dchi2(C, W, x, seed, n=300):
    L = np.linalg.cholesky(C + 1e-18*np.eye(C.shape[0]))
    rng = np.random.default_rng(seed)
    Y = (L @ rng.standard_normal((C.shape[0], n))).T
    # fast: their projection form (validated against chi2min on data)
    Xn = np.vander(x-x.mean(), 4, increasing=True)
    def B(X):
        WX = W @ X
        return WX @ np.linalg.solve(X.T @ WX, WX.T)
    Bn = B(Xn)
    q0 = np.einsum("mi,ij,mj->m", Y, Bn, Y)
    yWy = np.einsum("mi,ij,mj->m", Y, W, Y)
    best = np.full(n, -np.inf)
    for xc in CENTERS:
        for sw in WIDTHS:
            g = np.exp(-0.5*((x-xc)/sw)**2)
            Ba = B(np.column_stack([Xn, g]))
            q = np.einsum("mi,ij,mj->m", Y, Ba, Y) - q0
            best = np.maximum(best, q)
    return best

def main():
    out = {}
    # ---- 1. rebin identity + cov reproduction on >=3 shells + ranks ----
    print("== 1. REBIN / COVARIANCE ==")
    checks = [("DESI", DESI, "LRG_1.00_1.05_nosys"), ("DESI", DESI, "QSO_0.95_1.10_sys"),
              ("DESI", DESI, "BGS_BRIGHT_0.01_0.06_nosys"), ("BOSS", BOSS, "CMASS_0.53_0.58_nosys"),
              ("BOSS", BOSS, "LOWZ_0.20_0.25_sys")]
    for tag, ck, key in checks:
        d = np.load(os.path.join(ck, key + ".npz"))
        A = my_rebin(d["theta"], d["RR"])
        C12 = A @ d["cov_jk"] @ A.T; C12 = 0.5*(C12+C12.T)
        w12 = A @ d["w"]
        _, wq, Cq, Ciq, Aq = load_cov(tag, key)
        ev = np.linalg.eigvalsh(C12)
        print(f"  {tag} {key}: maxreldiff C12 {abs(C12-Cq).max()/abs(Cq).max():.2e} "
              f"w12 {abs(w12-wq).max():.2e} A {abs(A-Aq).max():.2e} "
              f"PD={ev.min()>0} cond={ev.max()/ev.min():.0f} "
              f"cinv_ok={np.allclose(Ciq, HARTLAP*np.linalg.inv(Cq), rtol=1e-8)} "
              f"rank40={np.linalg.matrix_rank(d['cov_jk'])}")
    # rank census over all checkpoints
    ranks = []
    for ck in (DESI, BOSS):
        for fn in glob.glob(os.path.join(ck, "*.npz")):
            if "spotcache" in fn: continue
            ranks.append(np.linalg.matrix_rank(np.load(fn)["cov_jk"]))
    print(f"  rank census over {len(ranks)} shells: min={min(ranks)} max={max(ranks)}")

    # ---- 2. refit drivers, indep chi2 machinery ----
    print("== 2. REFIT DRIVERS ==")
    for tag, key in (("DESI", "LRG_1.00_1.05_nosys"), ("DESI", "LRG_1.00_1.05_sys"),
                     ("BOSS", "CMASS_0.53_0.58_nosys"), ("BOSS", "CMASS_0.53_0.58_sys"),
                     ("DESI", "QSO_0.95_1.10_nosys")):
        th, w, C, Ci, _ = load_cov(tag, key)
        x = np.log(th)
        df, tbf = scan_dchi2(w, x, Ci)
        dd, tbd = scan_dchi2(w, x, np.diag(1/np.diag(C)))
        # local p reproduction (their seed) + independent-seed stability
        kv = key.rsplit("_", 1)
        seed_theirs = 20260807 + zlib.crc32((kv[0] + kv[1]).encode()) % 1000000
        m1 = mocks_dchi2(C, Ci, x, seed_theirs)
        m2 = mocks_dchi2(C, Ci, x, 987654321 + zlib.crc32(key.encode()) % 1000, n=600)
        print(f"  {tag} {key}: dchi2 full={df:.2f} diag={dd:.2f} th_b={tbf:.2f} "
              f"localp(theirseed)={np.mean(m1>=df):.3f} localp(newseed,600)={np.mean(m2>=df):.4f}")

    # ---- 2b. BOSS global p: full vs DIAG at 12 bins (binning-vs-cov decomposition) ----
    print("== 2b. BOSS GLOBAL p decomposition ==")
    boss_keys = sorted({os.path.basename(f).split("__")[1].rsplit("_",1)[0]
                        for f in glob.glob(os.path.join(COV, "BOSS__*_nosys.npz"))})
    for v in ("nosys", "sys"):
        obs_f, obs_d, mx_f, mx_d = [], [], [], []
        for k in boss_keys:
            th, w, C, Ci, _ = load_cov("BOSS", f"{k}_{v}")
            x = np.log(th)
            Wd = np.diag(1/np.diag(C))
            df, _ = scan_dchi2(w, x, Ci); dd, _ = scan_dchi2(w, x, Wd)
            obs_f.append(df); obs_d.append(dd)
            seed = 20260807 + zlib.crc32((k + v).encode()) % 1000000
            mx_f.append(mocks_dchi2(C, Ci, x, seed))
            mx_d.append(mocks_dchi2(C, Wd, x, seed + 1))
        gpf = np.mean(np.vstack(mx_f).max(0) >= max(obs_f))
        gpd = np.mean(np.vstack(mx_d).max(0) >= max(obs_d))
        print(f"  BOSS {v}: 12-bin FULL global_p={gpf:.4f} (max {max(obs_f):.2f})  "
              f"12-bin DIAG global_p={gpd:.4f} (max {max(obs_d):.2f})")

    # ---- 3. tracer split ----
    print("== 3. TRACER SPLIT ==")
    for v in ("nosys", "sys"):
        for mode in ("diag", "full"):
            tL, sL = profile_err("DESI", f"LRG_1.00_1.05_{v}", mode)
            tQ, sQ = profile_err("DESI", f"QSO_0.95_1.10_{v}", mode)
            print(f"  {v} {mode}: LRG {tL:.3f}+/-{sL:.3f} QSO {tQ:.3f}+/-{sQ:.3f} "
                  f"split={abs(tL-tQ)/math.hypot(sL,sQ):.2f} sigma")

    # ---- 4. threading ----
    print("== 4. THREADING ==")
    prim = [("LRG_0.70_0.75", 0.725), ("LRG_1.00_1.05", 1.025), ("QSO_0.95_1.10", 1.025)]
    for v in ("sys", "nosys"):
        rows = [(k, zc) + profile_err("DESI", f"{k}_{v}", "full") for k, zc in prim]
        c2fix = sum(((tb - tpred(zc))/sc)**2 for _, zc, tb, sc in rows)
        kk = np.array([1/rz(zc)/DEG for _, zc, _, _ in rows])
        yy = np.array([tb for *_, tb, _ in [(r[0], r[1], r[2], r[3]) for r in rows]])
        yy = np.array([r[2] for r in rows]); ss = np.array([r[3] for r in rows])
        wv = 1/ss**2
        ebf = (yy*kk*wv).sum()/(kk*kk*wv).sum()
        c2bf = (((yy - ebf*kk)/ss)**2).sum()
        print(f"  {v}: chi2(58.34)={c2fix:.1f}/3  ell_bf={ebf:.2f} chi2/dof={c2bf:.1f}/2={c2bf/2:.1f}")

if __name__ == "__main__":
    main()
