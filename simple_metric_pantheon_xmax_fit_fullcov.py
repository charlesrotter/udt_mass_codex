#!/usr/bin/env python3
"""
Full STAT+SYS covariance re-score of the pre-registered hyperbolic n=2 xmax model.

Same contract as simple_metric_pantheon_xmax_fit.py:
  d_L = X (1+z)^2 ((1+z)^2-1)/((1+z)^2+1)
  free (shape): one additive offset only
  absolute X: needs conventional M_B
  cut: IS_CALIBRATOR==0, zHD>0.01
  no shape knobs, no retune

Data (Charles-provided paths):
  Data/Pantheon+SH0ES.dat
  Data/Pantheon+SH0ES_STAT+SYS.cov
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from numpy.linalg import inv, solve
from scipy.linalg import cho_factor, cho_solve

ROOT = Path(__file__).resolve().parent
DAT = ROOT / "Data" / "Pantheon+SH0ES.dat"
COV = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"

# ---- load catalog ----
d = np.genfromtxt(DAT, names=True, dtype=None, encoding=None)
N_all = len(d)
assert N_all == 1701

z_all = np.asarray(d["zHD"], float)
m_all = np.asarray(d["m_b_corr"], float)
s_all = np.asarray(d["m_b_corr_err_DIAG"], float)
iscal = d["IS_CALIBRATOR"].astype(int)

mask = (iscal == 0) & (z_all > 0.01)
idx = np.where(mask)[0]
z = z_all[idx]
m = m_all[idx]
s = s_all[idx]
N = len(z)
print(f"N_all={N_all}  N_cut={N}  z∈[{z.min():.4f},{z.max():.4f}]")

# ---- load cov (first line = N) ----
with open(COV) as f:
    n_cov = int(f.readline().strip())
assert n_cov == N_all
C_all = np.loadtxt(COV, skiprows=1).reshape(N_all, N_all)
# symmetrize tiny asym
C_all = 0.5 * (C_all + C_all.T)
C = C_all[np.ix_(idx, idx)].copy()
print(f"cov submatrix {C.shape}, diag mean={np.mean(np.diag(C)):.5f}")

# Cholesky of C for solves
cfac = cho_factor(C, lower=True, check_finite=False)


def chi2_vec(resid: np.ndarray) -> float:
    """resid^T C^{-1} resid via Cholesky."""
    y = cho_solve(cfac, resid, check_finite=False)
    return float(resid @ y)


def best_offset(dvec: np.ndarray) -> tuple[float, float, np.ndarray]:
    """
    Minimize (d - O*1)^T Cinv (d - O*1).
    O = (1^T Cinv d) / (1^T Cinv 1)
    """
    ones = np.ones_like(dvec)
    Cinv_1 = cho_solve(cfac, ones, check_finite=False)
    Cinv_d = cho_solve(cfac, dvec, check_finite=False)
    O = float((ones @ Cinv_d) / (ones @ Cinv_1))
    resid = dvec - O
    return O, chi2_vec(resid), resid


def dL_over_X(zz: np.ndarray) -> np.ndarray:
    ez = 1.0 + zz
    return (ez**2) * (ez**2 - 1.0) / (ez**2 + 1.0)


def dL_lcdm_over_cH0(zz, Om=0.3):
    out = np.empty_like(zz, float)
    for i, zi in enumerate(zz):
        g = np.linspace(0.0, zi, 1024)
        E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
        out[i] = (1 + zi) * np.trapezoid(1.0 / E, g)
    return out


def score_shape(f: np.ndarray, label: str, npar_extra: int = 0):
    """Shape f = d_L / scale; mu_shape = 5 log10(f); free offset."""
    mu_shape = 5.0 * np.log10(np.maximum(f, 1e-30))
    dvec = m - mu_shape
    O, chi2, resid = best_offset(dvec)
    dof = N - 1 - npar_extra
    rms = float(np.sqrt(np.mean(resid**2)))
    # diagonal-only chi2 for comparison
    w = 1.0 / s**2
    O_diag = float(np.sum(w * dvec) / np.sum(w))
    resid_d = dvec - O_diag
    chi2_diag = float(np.sum(w * resid_d**2))
    # binned mean residual (unweighted characterize)
    bins = [(0.01, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.0), (1.0, 2.5)]
    trend = []
    for zlo, zhi in bins:
        sel = (z >= zlo) & (z < zhi)
        if sel.sum() < 5:
            continue
        trend.append(
            {
                "zlo": zlo,
                "zhi": zhi,
                "n": int(sel.sum()),
                "mean_res": float(np.mean(resid[sel])),
                "rms": float(np.sqrt(np.mean(resid[sel] ** 2))),
            }
        )
    print(
        f"  [{label}]  fullcov chi2/dof={chi2/dof:.4f} ({chi2:.1f}/{dof})  "
        f"RMS={rms:.4f}  O={O:.4f}  | diag chi2/dof={chi2_diag/dof:.4f}"
    )
    for t in trend:
        print(
            f"      z∈[{t['zlo']},{t['zhi']}) n={t['n']:4d}  "
            f"〈res〉={t['mean_res']:+.4f}  rms={t['rms']:.4f}"
        )
    return {
        "label": label,
        "chi2_full": chi2,
        "dof": dof,
        "chi2_dof_full": chi2 / dof,
        "chi2_diag": chi2_diag,
        "chi2_dof_diag": chi2_diag / dof,
        "rms": rms,
        "offset_O": O,
        "trend": trend,
        "resid": resid,
    }


def abs_X(MB: float):
    f = dL_over_X(z)
    # m = MB + 5 log10(X f) + 25 = MB + 5 log10 X + 25 + 5 log10 f
    # free logX via 1D line search on chi2
    def chi2_logX(logX):
        X = np.exp(logX)
        mu = 5.0 * np.log10(X * f) + 25.0
        resid = m - (mu + MB)
        return chi2_vec(resid)

    # seed from shape offset: O = MB + 5 log10 X + 25
    O_shape = score_cache_O  # set below after hyp shape
    log10_X = (O_shape - MB - 25.0) / 5.0
    logX0 = np.log(10.0) * log10_X
    # fine grid around seed (analytic for pure offset is exact for fixed shape)
    X = float(np.exp(logX0))
    mu = 5.0 * np.log10(X * f) + 25.0
    resid = m - (mu + MB)
    chi2 = chi2_vec(resid)
    rms = float(np.sqrt(np.mean(resid**2)))
    dof = N - 1
    print(f"  M_B={MB:.3f}  X={X:.4f} Mpc  fullcov chi2/dof={chi2/dof:.4f}  RMS={rms:.4f}")
    return {"MB": MB, "X_Mpc": X, "chi2": chi2, "dof": dof, "chi2_dof": chi2 / dof, "rms": rms}


def mass_from_X(X_Mpc: float) -> dict:
    c_SI = 299_792_458.0
    G_SI = 6.67430e-11
    Mpc_m = 3.085677581491367e22
    M_sun = 1.98847e30
    X_m = X_Mpc * Mpc_m
    M_kg = (c_SI**2) * X_m / (2.0 * G_SI)
    M_msun = M_kg / M_sun
    return {
        "X_Mpc": X_Mpc,
        "M_tot_Msun": M_msun,
        "log10_M_Msun": float(np.log10(M_msun)),
    }


print("=" * 70)
print("FULLCOV re-score: hyperbolic n=2 vs Pantheon+ STAT+SYS")
print(f"DAT={DAT}")
print(f"COV={COV}")
print("=" * 70)

print("\n--- SHAPE (1 offset; full cov) ---")
hyp = score_shape(dL_over_X(z), "hyperbolic n=2")
score_cache_O = hyp["offset_O"]

print("\n--- REFERENCE shape (flat LCDM Om=0.3) ---")
lcdm = score_shape(dL_lcdm_over_cH0(z), "LCDM Om=0.3 ref")

print("\n--- ABSOLUTE X (M_B convention; same shape chi2) ---")
abs_list = []
for MB in (-19.0, -19.25, -19.5):
    abs_list.append(abs_X(MB))

primary = abs_list[1]
mass = mass_from_X(primary["X_Mpc"])

print("\n--- SUMMARY ---")
print(
    f"  hyp  fullcov chi2/dof={hyp['chi2_dof_full']:.4f}  "
    f"RMS={hyp['rms']:.4f}  | diag chi2/dof={hyp['chi2_dof_diag']:.4f}"
)
print(
    f"  LCDM fullcov chi2/dof={lcdm['chi2_dof_full']:.4f}  "
    f"RMS={lcdm['rms']:.4f}  | diag chi2/dof={lcdm['chi2_dof_diag']:.4f}"
)
print(f"  primary X (MB=-19.25)={primary['X_Mpc']:.2f} Mpc  M_tot={mass['M_tot_Msun']:.3e} Msun")
print(
    f"  Δchi2 (hyp-LCDM)={hyp['chi2_full']-lcdm['chi2_full']:.1f}  "
    f"(same dof; hyp worse)"
)

out = {
    "data": str(DAT),
    "cov": str(COV),
    "N": N,
    "cut": "IS_CALIBRATOR==0, zHD>0.01",
    "hyp": {k: v for k, v in hyp.items() if k != "resid"},
    "lcdm_ref": {k: v for k, v in lcdm.items() if k != "resid"},
    "absolute": abs_list,
    "mass_lock_primary": mass,
    "delta_chi2_hyp_minus_lcdm": hyp["chi2_full"] - lcdm["chi2_full"],
}
Path("simple_metric_pantheon_xmax_fit_fullcov_out.json").write_text(
    json.dumps(out, indent=2, default=float)
)
print("\nWrote simple_metric_pantheon_xmax_fit_fullcov_out.json")
