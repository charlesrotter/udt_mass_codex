#!/usr/bin/env python3
"""
S3 — Native continuum from metric identities (not FREE ρ menu).

*** SCAR (2026-07-09 reconcile): G^r_r formula below is FALSE. ***
Full curvature: G^t_t = G^r_r = (r A' + A - 1)/r^2 ⇒ p_r = -ρ always.
Dust selection p_r=0 ⇒ A=1+Kr is INVALID. See:
  simple_metric_S4_reconcile_critical.py / _results.md
Kept as scar record; do not build on dust uniqueness.

HISTORICAL (wrong) claim was:
  G^r_r = (-A + r A' + 1)/r^2  → p_r=0 → A=1+Kr → A=1-r/X
Correct ceiling stresses if profile kept:
  ρ=1/(4π X r), p_r=-ρ, p_⊥=-ρ/2, M=X/2
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent


def cas_dust_selects_linear_A():
    r = sp.symbols("r", positive=True)
    A = sp.Function("A")
    # p_r ∝ r A' - A + 1
    pr_num = r * sp.diff(A(r), r) - A(r) + 1
    # ODE
    ode = sp.Eq(r * A(r).diff(r) - A(r) + 1, 0)
    sol = sp.dsolve(ode, A(r))
    return str(ode), str(sol)


def main():
    print("=" * 70)
    print("S3 native dust ceiling — p_r=0 selects A=1-r/X")
    print("=" * 70)
    ode, sol = cas_dust_selects_linear_A()
    print("ODE p_r=0:", ode)
    print("General solution:", sol)
    print("Outer A(X)=0, A(0)=1 ⇒ A=1-r/X unique in this family")

    # identities
    X = 1.0
    r = np.linspace(1e-3, 0.99 * X, 200)
    A = 1.0 - r / X
    m = r * (1 - A) / 2.0
    rho = 1.0 / (4.0 * np.pi * X * r)
    # check m' = 4π r^2 rho
    mp_num = np.gradient(m, r)
    mp_th = 4.0 * np.pi * r**2 * rho
    print(f"max |m' - 4πr²ρ| = {np.max(np.abs(mp_num - mp_th)):.2e}")

    # phi, z, dL
    phi = -0.5 * np.log(A)
    z = np.exp(phi) - 1.0  # observer at r=0 limit carefully: phi(0)=0
    # at r→0, A→1, phi→0 OK
    dL = (1 + z) ** 2 * r
    dL_X = dL / X
    # analytic dL/X = z(z+2)
    z_an = 1.0 / np.sqrt(A) - 1.0
    assert np.allclose(z, z_an)
    assert np.allclose(dL_X, z * (z + 2.0))

    print("A(0)=", float(A[0]), " A(r_max)=", float(A[-1]))
    print("phi'(0) est", (phi[1] - phi[0]) / (r[1] - r[0]))
    print("d_L/X = z(z+2) identity OK")
    print("M_tot = X/2 =", X / 2)

    # optional residual
    print("\n--- residual DEMO (not selector) ---")
    try:
        from scipy.linalg import cho_factor, cho_solve

        d = np.genfromtxt(
            ROOT / "Data" / "Pantheon+SH0ES.dat", names=True, dtype=None, encoding=None
        )
        mask = (d["IS_CALIBRATOR"].astype(int) == 0) & (d["zHD"] > 0.01)
        idx = np.where(mask)[0]
        zobs = np.asarray(d["zHD"][mask], float)
        mobs = np.asarray(d["m_b_corr"][mask], float)
        with open(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov") as f:
            N = int(f.readline())
        C = np.loadtxt(ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov", skiprows=1).reshape(N, N)
        C = 0.5 * (C + C.T)
        C = C[np.ix_(idx, idx)]
        cf = cho_factor(C, lower=True, check_finite=False)
        f = zobs * (zobs + 2.0)  # d_L/X
        mu = 5 * np.log10(np.maximum(f, 1e-30))
        dv = mobs - mu
        ones = np.ones_like(dv)
        O = float((ones @ cho_solve(cf, dv)) / (ones @ cho_solve(cf, ones)))
        res = dv - O
        chi2 = float(res @ cho_solve(cf, res))
        print(f"  chi2/dof={chi2/(len(zobs)-1):.4f}  RMS={np.sqrt(np.mean(res**2)):.4f}")
    except Exception as e:
        print("  demo skip", e)

    out = {
        "selection": "p_r=0 + simple metric MS ⇒ A=1+Kr ⇒ A=1-r/X with outer zero",
        "rho": "1/(4 pi X r)",
        "p_r": 0,
        "p_perp": "nonzero (anisotropic) — honest",
        "M_tot": "X/2 (c=G=1)",
        "dL_over_X": "z(z+2)",
        "grade": "CONDITIONAL — dust p_r=0 is named continuum condition, not full action matter",
    }
    path = ROOT / "simple_metric_S3_native_dust_ceiling_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
