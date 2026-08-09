#!/usr/bin/env python3
"""M3c STEP 1-2: FULL bin-bin covariance from the BANKED M3/M3b checkpoints.

INVENTORY (STEP 1): the M3 (DESI) and M3b (BOSS) checkpoints bank, per (shell,
variant): theta(40), w(40), sig(40)=sqrt(diag), cov_jk(40,40) FULL, and TOTAL
DD/DR/RR(40).  They do NOT bank the region-blocked [T,T,40] count arrays nor the
per-region leave-one-out w_jk vectors.  BUT the banked cov_jk IS the full T=48
region jackknife covariance at 40 bins (cap-combine -> T = 2 caps x 24 regions;
verified numerically: rank 40, so T>40).  M3 USED ONLY ITS DIAGONAL (the flagged
M2 caveat).  At 40 bins with 48 regions the inverse is near-singular (Hartlap dof
48-40-2=6), which is exactly why M3 stayed diagonal.

FROZEN ROUTE (prereg SS1.1b): reduce N_theta_bins so C is well invertible, ZERO
recount, binning FROZEN to 12 log bins on [0.3,12] deg.  We rebin the banked full
40-bin cov to 12 bins with a FIXED linear operator A (12x40): w12 = A w40,
C12 = A C40 A^T.  This is mathematically IDENTICAL to forming the 12-bin jackknife
covariance from the (linearly-rebinned) per-region vectors, because
A(dev_k)=dev of (A w_jk_k) and cov = c*sum_k dev_k dev_k^T.  The only definitional
choice is that the coarse-bin estimator is the RR-pair-count-weighted average of
the fine-bin LS w's rather than a from-scratch coarse-bin LS -- a legitimate,
data-only estimator (RR = banked random-pair counts; no theory, no mocks, no
fiducial cosmology).  DISCLOSED.

N_reg = 48 (Hartlap/Percival), N_bins = 12.
"""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cov_out")
os.makedirs(OUT, exist_ok=True)

DESI_CKPT = os.path.join(os.path.dirname(HERE),
                         "udt_xmax_scale_observational_M3_runs_2026-08-07",
                         "bao_checkpoints")
BOSS_CKPT = os.path.join(os.path.dirname(HERE),
                         "udt_xmax_scale_observational_M3b_BOSS_2026-08-08",
                         "boss_checkpoints")

N_REG = 48                       # cap-combine T = 2 caps x 24 regions (verified)
N_COARSE = 12                    # FROZEN 12 log bins on [0.3,12] deg
THETA_MIN, THETA_MAX = 0.3, 12.0


def coarse_edges():
    return np.geomspace(THETA_MIN, THETA_MAX, N_COARSE + 1)


def build_operator(theta_fine, rr_fine):
    """A (12x40): RR-weighted average of fine bins within each coarse bin.
    Partition by fine-bin center into the 12 frozen coarse bins."""
    edges = coarse_edges()
    # assign each fine center to a coarse bin (right-open, last bin closed)
    idx = np.searchsorted(edges, theta_fine, side="right") - 1
    idx = np.clip(idx, 0, N_COARSE - 1)
    A = np.zeros((N_COARSE, theta_fine.size))
    theta_c = np.zeros(N_COARSE)
    for b in range(N_COARSE):
        m = idx == b
        if not m.any():
            raise RuntimeError(f"coarse bin {b} empty -- binning mismatch")
        wgt = np.where(rr_fine[m] > 0, rr_fine[m], 0.0)
        if wgt.sum() <= 0:
            wgt = np.ones(m.sum())
        wgt = wgt / wgt.sum()
        A[b, m] = wgt
        theta_c[b] = float((theta_fine[m] * wgt).sum())
    return A, theta_c, idx


def hartlap(n_reg, n_bins):
    return (n_reg - n_bins - 2.0) / (n_reg - 1.0)


def percival_m(n_reg, n_bins, n_par):
    """Percival+2014 parameter-covariance inflation factor m (variance)."""
    A = 2.0 / ((n_reg - n_bins - 1.0) * (n_reg - n_bins - 4.0))
    B = (n_reg - n_bins - 2.0) / ((n_reg - n_bins - 1.0) *
                                  (n_reg - n_bins - 4.0))
    return (1.0 + B * (n_bins - n_par)) / (1.0 + A + B * (n_par + 1.0))


def process(ckpt_dir, tag):
    rows = []
    for fn in sorted(glob.glob(os.path.join(ckpt_dir, "*.npz"))):
        base = os.path.basename(fn)
        if base.startswith("spotcache_"):
            continue
        key = base[:-4]
        d = np.load(fn)
        theta, w, C40, RR = d["theta"], d["w"], d["cov_jk"], d["RR"]
        A, theta_c, idx = build_operator(theta, RR)
        w12 = A @ w
        C12 = A @ C40 @ A.T
        C12 = 0.5 * (C12 + C12.T)                 # symmetrize fp
        ev = np.linalg.eigvalsh(C12)
        pd = bool(ev.min() > 0)
        cond = float(ev.max() / ev.min()) if pd else float("inf")
        h = hartlap(N_REG, N_COARSE)
        Cinv = h * np.linalg.inv(C12)
        sig12 = np.sqrt(np.diag(C12))
        np.savez(os.path.join(OUT, f"{tag}__{key}.npz"),
                 theta=theta_c, w=w12, cov=C12, cinv_hartlap=Cinv,
                 sig=sig12, A=A, hartlap=h)
        rows.append({"key": key, "cond": cond, "pd": pd,
                     "eig_min": float(ev.min()), "eig_max": float(ev.max())})
    return rows


def main():
    summary = {"n_reg": N_REG, "n_coarse": N_COARSE,
               "coarse_edges": coarse_edges().tolist(),
               "hartlap_factor": hartlap(N_REG, N_COARSE),
               "percival_m_np6": percival_m(N_REG, N_COARSE, 6)}
    summary["DESI"] = process(DESI_CKPT, "DESI")
    summary["BOSS"] = process(BOSS_CKPT, "BOSS")
    conds = [r["cond"] for r in summary["DESI"] + summary["BOSS"]]
    pds = [r["pd"] for r in summary["DESI"] + summary["BOSS"]]
    summary["all_pd"] = bool(all(pds))
    summary["cond_min"] = float(np.min(conds))
    summary["cond_max"] = float(np.max(conds))
    summary["cond_median"] = float(np.median(conds))
    with open(os.path.join(HERE, "cov_build_summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print("COV BUILD done. n_DESI=%d n_BOSS=%d all_PD=%s" %
          (len(summary["DESI"]), len(summary["BOSS"]), summary["all_pd"]))
    print("hartlap=%.4f  percival_m(np6)=%.4f" %
          (summary["hartlap_factor"], summary["percival_m_np6"]))
    print("cond: min=%.1f median=%.1f max=%.1f" %
          (summary["cond_min"], summary["cond_median"], summary["cond_max"]))


if __name__ == "__main__":
    main()
