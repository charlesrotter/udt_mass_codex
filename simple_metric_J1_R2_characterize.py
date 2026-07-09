#!/usr/bin/env python3
"""
R2 CHARACTERIZE — J1 + full light hyperbolic residual (no retune, no join shopping).

Pre-registered:
  - Model fixed: simple_metric_hyperbolic_J1 (Charles J1 posture)
  - Free: one additive magnitude offset only (X degenerate with M_B in shape score)
  - NOT free: shape, Om, w, switching to P_ell
  - LCDM Om=0.3: residual REFERENCE only, not a target to optimize toward
  - Observing residual structure; not claiming win/loss on multi-tension yet
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve

from simple_metric_hyperbolic_J1 import (
    DA_of_z,
    DM_of_z,
    M_sun_from_X_Mpc,
    dL_of_z,
    dL_over_X,
    x_of_z,
)

ROOT = Path(__file__).resolve().parent
DAT = ROOT / "Data" / "Pantheon+SH0ES.dat"
COV = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"


def load_pantheon(cut: str = "cosmo"):
    d = np.genfromtxt(DAT, names=True, dtype=None, encoding=None)
    z = np.asarray(d["zHD"], float)
    m = np.asarray(d["m_b_corr"], float)
    iscal = d["IS_CALIBRATOR"].astype(int)
    if cut == "cosmo":
        idx = np.where((iscal == 0) & (z > 0.01))[0]
    elif cut == "full":
        idx = np.arange(len(z))
    else:
        raise ValueError(cut)
    with open(COV) as f:
        N = int(f.readline())
    C = np.loadtxt(COV, skiprows=1).reshape(N, N)
    C = 0.5 * (C + C.T)
    return z[idx], m[idx], C[np.ix_(idx, idx)], idx


def dL_lcdm_shape(z, Om=0.3):
    """Shape only (units c/H0); offset absorbs scale. SCAFFOLD reference."""
    z = np.atleast_1d(z)
    out = np.empty_like(z, float)
    for i, zi in enumerate(z):
        g = np.linspace(0.0, float(zi), 1024)
        E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
        out[i] = (1 + zi) * np.trapezoid(1.0 / E, g)
    return out


def score_shape(dL, m, C):
    """One free offset on distance modulus shape."""
    cf = cho_factor(C, lower=True, check_finite=False)
    mu = 5.0 * np.log10(np.maximum(dL, 1e-30))
    dv = m - mu
    ones = np.ones_like(dv)
    O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
    res = dv - O
    chi2 = float(res @ cho_solve(cf, res))
    n = len(m)
    return {
        "offset_O": O,
        "chi2": chi2,
        "dof": n - 1,
        "chi2_dof": chi2 / (n - 1),
        "rms": float(np.sqrt(np.mean(res**2))),
        "resid": res,
    }


def binned_resid(z, res, bins):
    out = []
    for zlo, zhi in bins:
        sel = (z >= zlo) & (z < zhi)
        if sel.sum() < 5:
            continue
        out.append(
            {
                "zlo": zlo,
                "zhi": zhi,
                "n": int(sel.sum()),
                "mean_res": float(np.mean(res[sel])),
                "rms": float(np.sqrt(np.mean(res[sel] ** 2))),
            }
        )
    return out


def main():
    print("=" * 70)
    print("R2 CHARACTERIZE — J1 + full light (Charles posture)")
    print("No retune; LCDM = reference only")
    print("=" * 70)

    z, m, C, idx = load_pantheon("cosmo")
    print(f"N={len(z)}  z∈[{z.min():.4f},{z.max():.4f}]  cut=IS_CALIBRATOR==0 & zHD>0.01")

    # Shape score X free via offset
    hyp = score_shape(dL_over_X(z), m, C)
    lcdm = score_shape(dL_lcdm_shape(z), m, C)
    print(f"\n  J1 full light:  chi2/dof={hyp['chi2_dof']:.4f}  RMS={hyp['rms']:.4f}")
    print(f"  LCDM Om=0.3 ref: chi2/dof={lcdm['chi2_dof']:.4f}  RMS={lcdm['rms']:.4f}")
    print(f"  Δchi2 (J1-LCDM)={hyp['chi2']-lcdm['chi2']:.1f}  (same dof; not a verdict on multi-tension)")

    bins = [(0.01, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.0), (1.0, 2.5)]
    print("\n  residual bins (m_obs - m_model), J1:")
    trend = binned_resid(z, hyp["resid"], bins)
    for t in trend:
        print(f"    z∈[{t['zlo']},{t['zhi']}) n={t['n']:4d}  〈res〉={t['mean_res']:+.4f}  rms={t['rms']:.4f}")

    # Shape ratio vs LCDM (norm at z=0.05)
    zs = np.array([0.05, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0])
    h = dL_over_X(zs)
    L = dL_lcdm_shape(zs)
    h0, L0 = h[0], L[0]
    print("\n  d_L shape ratio J1/LCDM (norm z=0.05) and Δμ:")
    ratios = []
    for i, zz in enumerate(zs):
        ratio = (h[i] / h0) / (L[i] / L0)
        dmu = 5 * np.log10(ratio)
        ratios.append({"z": float(zz), "ratio": float(ratio), "dmu": float(dmu)})
        print(f"    z={zz:.2f}  ratio={ratio:.4f}  dmu={dmu:+.3f}")

    # Conventional absolute X (CHOSE M_B) — calibration label only
    # O = M_B + 5 log10(X) + 25 when mu = 5 log10(dL/X * X) ... same as before
    # m = M_B + 5 log10(X * f) + 25 with f=dL/X, O_shape from score used mu=5log10(f)
    # so O = M_B + 5 log10 X + 25
    O = hyp["offset_O"]
    abs_X = {}
    for MB in (-19.0, -19.25, -19.5):
        X = 10 ** ((O - MB - 25.0) / 5.0)
        abs_X[str(MB)] = {
            "X_Mpc": float(X),
            "M_tot_Msun": float(M_sun_from_X_Mpc(X)),
            "log10_M_Msun": float(np.log10(M_sun_from_X_Mpc(X))),
        }
        print(f"\n  calib M_B={MB:.2f} (CONVENTION) => X={X:.1f} Mpc  "
              f"M_tot={M_sun_from_X_Mpc(X):.3e} M_sun  [J1 mass lock]")

    # Geometric diagnostics at sample z (X=1 units)
    print("\n  geometric (X=1): z, x/X=D_A/X, D_M/X, d_L/X, A")
    for zz in zs:
        x = float(np.asarray(x_of_z(zz, 1.0)).reshape(-1)[0])
        dL = float(np.asarray(dL_of_z(zz, 1.0)).reshape(-1)[0])
        print(
            f"    z={zz:.2f}  x={x:.4f}  DM={(1+zz)*x:.4f}  "
            f"dL={dL:.4f}  A={(1-x)/(1+x):.4e}"
        )

    out = {
        "model": "J1 + full light hyperbolic (Charles posture)",
        "N": len(z),
        "cut": "IS_CALIBRATOR==0, zHD>0.01",
        "hyp": {k: v for k, v in hyp.items() if k != "resid"},
        "lcdm_ref": {k: v for k, v in lcdm.items() if k != "resid"},
        "delta_chi2_J1_minus_lcdm": hyp["chi2"] - lcdm["chi2"],
        "trend_J1": trend,
        "shape_ratio_vs_lcdm": ratios,
        "absolute_X_convention_MB": abs_X,
        "notes": [
            "Shape score free=1 offset only",
            "LCDM is SCAFFOLD residual reference not target",
            "Absolute X is calibration not pure prediction",
            "P_ell not used",
        ],
    }
    path = ROOT / "simple_metric_J1_R2_characterize_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
