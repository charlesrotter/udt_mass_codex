#!/usr/bin/env python3
"""
OBSERVE — Split hyp PATH from AREAL (drop J1 as default).

Held:
  Full light: d_L = (1+z)^2 D_A
  PATH composition (xmax):  phi = arctanh(x/X),  1+z = e^phi
                            x/X = ((1+z)^2-1)/((1+z)^2+1)

Joins (tagged):
  J1  (old): D_A = x                    PATH label = areal radius
  P_ell     : x = proper radial length
              dx = e^phi dr  =>  dr/dx = e^{-phi} = sqrt((X-x)/(X+x))
              D_A = r(x) = int_0^x sqrt((X-u)/(X+u)) du

P_ell is a NAMED join (path = proper 1D), not a free D_A(r) fit.
Characterize shapes + optional Pantheon demo (1 offset; not a fit campaign).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, quad
from scipy.linalg import cho_factor, cho_solve

ROOT = Path(__file__).resolve().parent


def xi_of_z(z):
    """x/X from 1+z = e^phi, phi=arctanh(x/X)."""
    ez2 = (1.0 + z) ** 2
    return (ez2 - 1.0) / (ez2 + 1.0)


def r_over_X_from_xi(xi):
    """D_A/X = r/X for P_ell join; xi = x/X in [0,1)."""
    xi = np.asarray(xi, float)
    scalar = xi.ndim == 0
    xi = np.atleast_1d(xi)
    out = np.empty_like(xi)
    for i, x in enumerate(xi):
        if x <= 0:
            out[i] = 0.0
        elif x >= 1:
            out[i] = np.nan
        else:
            val, _ = quad(lambda u: np.sqrt((1.0 - u) / (1.0 + u)), 0.0, float(x), epsabs=1e-12)
            out[i] = val
    return float(out[0]) if scalar else out


def dL_over_X_J1(z):
    return (1.0 + z) ** 2 * xi_of_z(z)


def dL_over_X_Pell(z):
    z = np.asarray(z, float)
    xi = xi_of_z(z)
    return (1.0 + z) ** 2 * r_over_X_from_xi(xi)


def dL_lcdm(z, Om=0.3):
    z = np.atleast_1d(z)
    out = np.empty_like(z, float)
    for i, zi in enumerate(z):
        g = np.linspace(0.0, float(zi), 1024)
        E = np.sqrt(Om * (1 + g) ** 3 + (1 - Om))
        out[i] = (1 + zi) * np.trapezoid(1.0 / E, g)
    return out


def main():
    print("=" * 70)
    print("PATH–AREAL split: J1 (D_A=x) vs P_ell (x=proper, D_A=r(x))")
    print("Full light d_L=(1+z)^2 D_A; xmax hyp for PATH only")
    print("=" * 70)

    # Build r(x)/X table
    xg = np.linspace(0.0, 0.999, 500)
    rg = r_over_X_from_xi(xg)
    print("\n--- r(x)/X vs x/X (P_ell) ---")
    for xi in (0.01, 0.1, 0.3, 0.5, 0.8, 0.95):
        print(f"  x/X={xi:.2f}  r/X={r_over_X_from_xi(xi):.5f}  r/x={r_over_X_from_xi(xi)/xi:.5f}")

    # Near x->X: r stays finite?
    print(f"  x/X->1: r/X -> {rg[-1]:.5f} (finite; proper path to bound diverges as phi->inf)")
    # Actually x is proper distance and x->X finite, so proper distance to bound is finite X!
    # Wait: x max is X, and x = proper length, so proper distance to bound is X (finite).
    # dr/dx = e^{-phi} -> 0 as x->X, so r approaches finite limit.

    r_inf = r_over_X_from_xi(0.999999)
    print(f"  r_max/X (xi=1-1e-6) ≈ {r_inf:.5f}")

    zs = np.array([0.05, 0.1, 0.3, 0.5, 1.0, 1.5, 2.0])
    print("\n--- shapes normalized at z=0.05 ---")
    j = dL_over_X_J1(zs)
    p = dL_over_X_Pell(zs)
    L = dL_lcdm(zs)
    j0, p0, L0 = j[0], p[0], L[0]
    print(f"{'z':>5} {'dL_J1':>8} {'dL_Pell':>8} {'dL_LCDM':>8} {'dmu P-J':>9} {'dmu P-L':>9} {'DA_P/DA_J1':>10}")
    for i, z in enumerate(zs):
        xi = xi_of_z(z)
        da_j, da_p = xi, r_over_X_from_xi(xi)
        dmu_pj = 5 * np.log10((p[i] / p0) / (j[i] / j0))
        dmu_pl = 5 * np.log10((p[i] / p0) / (L[i] / L0))
        print(
            f"{z:5.2f} {j[i]/j0:8.4f} {p[i]/p0:8.4f} {L[i]/L0:8.4f} "
            f"{dmu_pj:+9.3f} {dmu_pl:+9.3f} {da_p/da_j:10.4f}"
        )

    # low-z series numerical
    zg = np.linspace(1e-3, 0.05, 20)
    jg, pg = dL_over_X_J1(zg), dL_over_X_Pell(zg)
    # fit d_L ~ c * z
    c_j = np.mean(jg / zg)
    c_p = np.mean(pg / zg)
    print(f"\n--- low-z d_L/(X z) mean on (0.001,0.05): J1={c_j:.4f}  Pell={c_p:.4f}  (want ~1) ---")

    # Pantheon demo
    dat = ROOT / "Data" / "Pantheon+SH0ES.dat"
    covp = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"
    scores = {}
    if dat.is_file() and covp.is_file():
        d = np.genfromtxt(dat, names=True, dtype=None, encoding=None)
        mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
        idx = np.where(mask)[0]
        z = np.asarray(d["zHD"][mask], float)
        m = np.asarray(d["m_b_corr"][mask], float)
        with open(covp) as f:
            Nall = int(f.readline())
        C = np.loadtxt(covp, skiprows=1).reshape(Nall, Nall)
        C = 0.5 * (C + C.T)
        C = C[np.ix_(idx, idx)]
        cf = cho_factor(C, lower=True, check_finite=False)

        def score(dL, label):
            mu = 5.0 * np.log10(np.maximum(dL, 1e-30))
            dv = m - mu
            ones = np.ones_like(dv)
            O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
            res = dv - O
            chi2 = float(res @ cho_solve(cf, res))
            dof = len(z) - 1
            rms = float(np.sqrt(np.mean(res**2)))
            print(f"  [{label:42s}] chi2/dof={chi2/dof:.4f}  RMS={rms:.4f}")
            return {"chi2_dof": chi2 / dof, "rms": rms}

        print("\n--- Pantheon DEMO (scale free via 1 offset; NOT a fit campaign) ---")
        # unit X=1 shapes; offset absorbs X and M_B
        scores["J1"] = score(dL_over_X_J1(z), "J1: D_A=x")
        # Pell via interp table
        xi = xi_of_z(z)
        DA = np.interp(xi, xg, rg, left=0.0, right=rg[-1])
        scores["Pell"] = score((1 + z) ** 2 * DA, "P_ell: D_A=r(x), x=proper")
        scores["LCDM"] = score(dL_lcdm(z), "LCDM Om=0.3 ref")
    else:
        print("\n(No Pantheon files — skip demo)")

    out = {
        "joins": {
            "J1": "D_A = x (PATH=AREAL)",
            "P_ell": "x=proper radial; D_A=r=int e^{-phi} dx",
        },
        "r_over_X_at_xi": {f"{xi:.2f}": r_over_X_from_xi(xi) for xi in (0.1, 0.5, 0.9, 0.99)},
        "scores": scores,
        "note": "P_ell is a named dimensional join, not free D_A fit; full light held",
    }
    path = ROOT / "simple_metric_path_areal_split_out.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
