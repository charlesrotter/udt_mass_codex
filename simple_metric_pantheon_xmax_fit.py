#!/usr/bin/env python3
"""
PRE-REGISTERED one-fit: Pantheon+ calibration of x_max under simple-metric
hyperbolic cascade + n=2 optics.

CONTRACT (frozen before run — 2026-07-08):
  Model (THEORY under J1 + xmax postulate + n=2):
      d_L(z) = X * (1+z)^2 * ((1+z)^2 - 1) / ((1+z)^2 + 1)
  Free parameters ONLY:
      X   = x_max  [Mpc]   — one absolute ruler (scale pin)
      M_B = absolute magnitude offset of SNe Ia (nuisance; every SNe law needs this)
  NOT free: shape parameters, Om, w, H0 language, free D_A, 1101.
  Data: Pantheon+SH0ES diagonal errors; cut IS_CALIBRATOR==0, zHD>0.01
        (same cut as prior repo SNe scripts).
  Scoring: weighted least-squares on m_b_corr; report RMS, chi2/dof, residual
           trend vs z (characterize, not filter).
  Label: "Pantheon-calibrated x_max" — NOT a pure prediction of X.
  Downstream consilience (after fit, not inside fit):
      M_tot = c^2 X / (2G) under J1 mass lock
      optional: x/X at z~1100 as kinematic check only

Reference (shape quality only; not UDT language): flat LCDM Om=0.3 with free
scale+offset — Category-A comparison of residual size.

Mode: OBSERVE one calibration + consilience check. No mechanism patches.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

# ---- data ----
DATA_CANDIDATES = [
    Path("/mnt/d/UDTDATA/SNe/Pantheon_SH0ES.dat"),
    Path("/home/udt-admin/UDT/data/Pantheon+SH0ES.dat"),
    Path("Pantheon_SH0ES.dat"),
]
DATA = next((p for p in DATA_CANDIDATES if p.is_file()), None)
if DATA is None:
    raise SystemExit("Pantheon+ data not found")

d = np.genfromtxt(DATA, names=True, dtype=None, encoding=None)
mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
z = np.asarray(d["zHD"][mask], float)
m = np.asarray(d["m_b_corr"][mask], float)
s = np.asarray(d["m_b_corr_err_DIAG"][mask], float)
w = 1.0 / s**2
N = len(z)

# ---- constants (SI + Mpc) ----
c_SI = 299_792_458.0
G_SI = 6.67430e-11
Mpc_m = 3.085677581491367e22
M_sun = 1.98847e30
pc_m = 3.085677581491367e16

# ---- model ----
def dL_over_X(zz: np.ndarray) -> np.ndarray:
    """d_L / X for hyperbolic + n=2 under J1. Dimensionless."""
    ez = 1.0 + zz
    return (ez**2) * (ez**2 - 1.0) / (ez**2 + 1.0)


def mu_from_dL_Mpc(dL_Mpc: np.ndarray) -> np.ndarray:
    """Distance modulus: mu = 5 log10(d_L/Mpc) + 25."""
    return 5.0 * np.log10(np.maximum(dL_Mpc, 1e-30)) + 25.0


def score_two_param(dL_shape: np.ndarray, label: str, n_shape_par: int = 0):
    """
    Fit free log-scale a and M_B:
        d_L = exp(a) * dL_shape   (dL_shape already absolute if a absorbed differently)
    Actually we use:
        m = M_B + mu(X * dL_over_X) = M_B + 5 log10(X * f(z)) + 25
          = (M_B + 5 log10 X + 25) + 5 log10 f(z)
    So for FIXED shape f=dL_over_X, X and M_B are degenerate in ONE offset if we only
    care about shape — BUT for absolute X we need a conventional M_B OR we report
    the product only.

    For absolute X we need an external absolute-magnitude anchor OR we report
    X only as a length scale once M_B is fixed to a conventional value.

    HONEST approach (pre-registered):
      (A) SHAPE-ONLY: fit one offset O = M_B + 5 log10(X) + 25 against mu_shape = 5 log10 f(z).
          Reports shape quality; X not separated from M_B.
      (B) ABSOLUTE with conventional M_B: fix M_B = -19.25 (common SN Ia ballpark) and fit X.
          Tagged FREE/CONVENTION for M_B — scale is Pantheon+convention calibrated.
      (C) Joint free (X, M_B): mathematically degenerate for pure m = M + 5log d_L;
          only one combination is constrained. DO NOT claim both free independently
          without absolute calibrators.

    We run (A) for shape residual and (B) for a conventional absolute X, and also
    report the constrained combination O = M_B + 5 log10(X_Mpc) + 25.
    """
    f = dL_shape
    # (A) shape: mu_shape = 5 log10(f); offset absorbs M_B + 5log X + 25
    mu_shape = 5.0 * np.log10(np.maximum(f, 1e-30))
    dd = m - mu_shape
    O = np.sum(w * dd) / np.sum(w)  # best offset
    res = dd - O
    rms = float(np.sqrt(np.mean(res**2)))
    chi2 = float(np.sum(w * res**2))
    dof = N - 1 - n_shape_par
    # residual trend: mean residual in z bins
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
                "mean_res": float(np.average(res[sel], weights=w[sel])),
                "rms": float(np.sqrt(np.mean(res[sel] ** 2))),
            }
        )
    print(
        f"  [{label}]  shape+1offset  RMS={rms:.4f} mag  chi2/dof={chi2/dof:.4f}  "
        f"({chi2:.1f}/{dof})  O={O:.4f}"
    )
    for t in trend:
        print(
            f"      z∈[{t['zlo']},{t['zhi']}) n={t['n']:4d}  "
            f"〈res〉={t['mean_res']:+.4f}  rms={t['rms']:.4f}"
        )
    return {
        "label": label,
        "rms": rms,
        "chi2": chi2,
        "dof": dof,
        "chi2_dof": chi2 / dof,
        "offset_O": O,
        "trend": trend,
        "resid": res,
    }


def fit_X_given_MB(MB: float, label: str):
    """Absolute X with fixed conventional M_B (CHOSE convention, tagged)."""
    f = dL_over_X(z)  # d_L/X

    def chi2_of_logX(logX):
        X = np.exp(logX)
        mu = mu_from_dL_Mpc(X * f)
        res = m - (mu + MB)
        return float(np.sum(w * res**2))

    # seed from low-z: d_L ~ X*z roughly at leading order (actually d_L/X = z + 1.5 z^2)
    # rough: mu ~ 5 log10(X z) + 25; m ~ MB + mu
    z_med = np.median(z[(z > 0.02) & (z < 0.1)])
    m_med = np.median(m[(z > 0.02) & (z < 0.1)])
    # m ≈ MB + 5 log10(X * z) + 25  => log10(X) ≈ (m-MB-25)/5 - log10(z)
    log10_X0 = (m_med - MB - 25.0) / 5.0 - np.log10(z_med)
    logX0 = np.log(10.0) * log10_X0

    opt = minimize_scalar(
        chi2_of_logX, bounds=(logX0 - 3, logX0 + 3), method="bounded", options={"xatol": 1e-12}
    )
    logX = float(opt.x)
    X = float(np.exp(logX))
    mu = mu_from_dL_Mpc(X * f)
    res = m - (mu + MB)
    rms = float(np.sqrt(np.mean(res**2)))
    chi2 = float(np.sum(w * res**2))
    dof = N - 1  # one free: X (MB fixed by convention)
    print(
        f"  [{label}]  M_B={MB:.3f} (CONVENTION)  X={X:.4f} Mpc  "
        f"RMS={rms:.4f}  chi2/dof={chi2/dof:.4f}"
    )
    return {
        "MB_convention": MB,
        "X_Mpc": X,
        "rms": rms,
        "chi2": chi2,
        "dof": dof,
        "chi2_dof": chi2 / dof,
        "resid": res,
    }


def dL_lcdm_over_cH0(zz, Om=0.3):
    out = np.empty_like(zz, float)
    for i, zi in enumerate(zz):
        g = np.linspace(0.0, zi, 1024)
        E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
        out[i] = (1 + zi) * np.trapezoid(1.0 / E, g)
    return out


def mass_from_X(X_Mpc: float) -> dict:
    """M_tot = c^2 X / (2G) under J1."""
    X_m = X_Mpc * Mpc_m
    M_kg = (c_SI**2) * X_m / (2.0 * G_SI)
    M_msun = M_kg / M_sun
    return {
        "X_Mpc": X_Mpc,
        "X_m": X_m,
        "M_tot_kg": M_kg,
        "M_tot_Msun": M_msun,
        "log10_M_Msun": float(np.log10(M_msun)),
    }


def shell_check(z_shell: float = 1100.0) -> dict:
    """Kinematic only: fractional reach x/X at given z (not foundation)."""
    ez = 1.0 + z_shell
    x_over_X = (ez**2 - 1.0) / (ez**2 + 1.0)
    phi = np.log(ez)
    return {
        "z": z_shell,
        "phi": float(phi),
        "x_over_X": float(x_over_X),
        "A": float((1.0 - x_over_X) / (1.0 + x_over_X)),
        "note": "kinematic check only; 1101 not used in fit or derivation",
    }


def main():
    print("=" * 70)
    print("PRE-REGISTERED: hyperbolic n=2 xmax fit vs Pantheon+")
    print(f"DATA: {DATA}")
    print(f"N SNe (IS_CALIBRATOR==0, zHD>0.01): {N}")
    print(f"z range: {z.min():.4f} .. {z.max():.4f}")
    print("Model: d_L = X (1+z)^2 ((1+z)^2-1)/((1+z)^2+1)")
    print("Free in shape score: 1 offset. Absolute X needs M_B convention.")
    print("=" * 70)

    # --- Hyperbolic n=2 shape ---
    print("\n--- SHAPE (offset free; X degenerate with M_B) ---")
    f_hyp = dL_over_X(z)
    hyp = score_two_param(f_hyp, "hyperbolic n=2 (J1+xmax)")

    # --- Reference LCDM shape (Category-A comparison) ---
    print("\n--- REFERENCE shape (flat LCDM Om=0.3; free scale+offset) ---")
    f_lcdm = dL_lcdm_over_cH0(z, Om=0.3)
    lcdm = score_two_param(f_lcdm, "flat LCDM Om=0.3 ref", n_shape_par=0)

    # --- Absolute X with conventional M_B ---
    print("\n--- ABSOLUTE X (M_B conventional; CHOSE — not derived) ---")
    abs_fits = []
    for MB in (-19.0, -19.25, -19.5):
        abs_fits.append(fit_X_given_MB(MB, f"hyp n=2 abs"))

    # Primary absolute report uses M_B=-19.25 (common mid convention)
    primary = abs_fits[1]
    X = primary["X_Mpc"]
    mass = mass_from_X(X)
    shell = shell_check(1100.0)
    shell_z2 = shell_check(2.0)

    # Also invert: from shape offset O = M_B + 5 log10(X) + 25
    # => for each MB, X = 10**((O - MB - 25)/5) but wait: mu_shape used f = dL/X so
    # m = O + 5 log10(f) = M_B + 5 log10(X f) + 25
    # => O = M_B + 5 log10(X) + 25  => X = 10**((O - M_B - 25)/5)
    O = hyp["offset_O"]
    print("\n--- X from shape offset + M_B convention (cross-check) ---")
    for MB in (-19.0, -19.25, -19.5):
        X_from_O = 10 ** ((O - MB - 25.0) / 5.0)
        print(f"  M_B={MB:.2f}  =>  X={X_from_O:.4f} Mpc  (from O={O:.4f})")

    # Mean density proxy if volume ~ (4/3)pi X^3 (characterize only; not imposed)
    X_m = mass["X_m"]
    vol = (4.0 / 3.0) * np.pi * X_m**3
    rho = mass["M_tot_kg"] / vol
    rho_c_proxy = 3.0 * (c_SI / X_m) ** 2 / (8.0 * np.pi * G_SI)  # NOT H0; scale c/X only as length/time
    print("\n--- DOWNSTREAM CONSILENCE (J1 mass lock) ---")
    print(f"  X (primary M_B=-19.25) = {X:.4f} Mpc")
    print(f"  M_tot = c^2 X / (2G) = {mass['M_tot_Msun']:.4e} M_sun")
    print(f"  log10(M/M_sun) = {mass['log10_M_Msun']:.3f}")
    print(f"  mean rho if ball R=X: {rho:.4e} kg/m^3")
    print(f"  (c/X)-scale density proxy 3(c/X)^2/(8pi G): {rho_c_proxy:.4e} kg/m^3  [units only]")
    print(f"  shell z=1100: x/X={shell['x_over_X']:.6f}  A={shell['A']:.3e}  (check only)")
    print(f"  at z=2: x/X={shell_z2['x_over_X']:.4f}")

    # Residual comparison
    drms = hyp["rms"] - lcdm["rms"]
    print("\n--- SHAPE VERDICT (scoped) ---")
    print(f"  hyp RMS={hyp['rms']:.4f}  LCDM-ref RMS={lcdm['rms']:.4f}  Δ={drms:+.4f} mag")
    print(f"  hyp chi2/dof={hyp['chi2_dof']:.4f}  LCDM-ref chi2/dof={lcdm['chi2_dof']:.4f}")
    if hyp["rms"] < 0.2 and abs(drms) < 0.05:
        shape_tag = "SHAPE competitive with LCDM-ref (provisional, diagonal)"
    elif hyp["rms"] < 0.25:
        shape_tag = "SHAPE ok-ish but residual excess vs LCDM-ref (provisional)"
    else:
        shape_tag = "SHAPE poor vs data (provisional, diagonal)"
    print(f"  tag: {shape_tag}")

    # High-z systematic: does hyp run bright/faint?
    print("\n--- residual polarity (characterize) ---")
    for t in hyp["trend"]:
        print(f"  hyp  z∈[{t['zlo']},{t['zhi']}) 〈res〉={t['mean_res']:+.4f}")

    out = {
        "contract": {
            "model": "d_L=X*(1+z)^2*((1+z)^2-1)/((1+z)^2+1)",
            "free_shape": "1 offset (M_B + 5 log10 X degenerate)",
            "free_absolute": "X with M_B convention",
            "data": str(DATA),
            "N": N,
            "cut": "IS_CALIBRATOR==0, zHD>0.01",
            "errors": "diagonal m_b_corr_err_DIAG",
        },
        "shape_hyp": {k: v for k, v in hyp.items() if k != "resid"},
        "shape_lcdm_ref": {k: v for k, v in lcdm.items() if k != "resid"},
        "absolute": [
            {k: v for k, v in a.items() if k != "resid"} for a in abs_fits
        ],
        "primary_MB": -19.25,
        "mass_lock": mass,
        "shell_z1100": shell,
        "shell_z2": shell_z2,
        "shape_tag": shape_tag,
        "delta_rms_hyp_minus_lcdm": drms,
    }
    out_path = Path("simple_metric_pantheon_xmax_fit_out.json")
    out_path.write_text(json.dumps(out, indent=2, default=float))
    print(f"\nWrote {out_path}")
    return out


if __name__ == "__main__":
    main()
