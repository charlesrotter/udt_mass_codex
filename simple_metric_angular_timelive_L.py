#!/usr/bin/env python3
"""
Time-live multipoles on L background: FD eigen + optical infinity.
Re-run: python3 simple_metric_angular_timelive_L.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parent


def spectrum(ell: int, N: int = 500, eps: float = 2e-3) -> np.ndarray:
    xi = np.linspace(eps, 1 - eps, N)
    dxi = xi[1] - xi[0]
    A = 1 - xi
    p = xi**2 * A
    M = N - 2
    Lmat = np.zeros((M, M))
    Bmat = np.zeros((M, M))
    for i in range(M):
        j = i + 1
        p_ph = 0.5 * (p[j] + p[j + 1])
        p_mh = 0.5 * (p[j] + p[j - 1])
        c_m = -p_mh / dxi**2
        c_p = -p_ph / dxi**2
        c_0 = (p_mh + p_ph) / dxi**2 + ell * (ell + 1)
        for offset, c in [(-1, c_m), (0, c_0), (1, c_p)]:
            jj = j + offset
            if jj in (0, N - 1):
                continue
            ii = jj - 1
            if 0 <= ii < M:
                Lmat[i, ii] += c
        Bmat[i, i] = (xi[j] ** 2) / max(A[j], 1e-30)
    evals, _ = eigh(Lmat, Bmat, subset_by_index=[0, min(12, M - 1)])
    return np.array([float(np.sqrt(ev)) for ev in evals if ev > 1e-8][:8])


def main():
    out = {"ell": {}, "eps_scan_ell1": []}
    print("Ω = ω X multipole towers (eps=2e-3)")
    for ell in range(1, 6):
        oms = spectrum(ell)
        out["ell"][str(ell)] = oms.tolist()
        print(f"  ℓ={ell}: {oms}")

    print("eps scan ℓ=1:")
    for eps in [1e-2, 1e-3, 1e-4]:
        oms = spectrum(1, N=800, eps=eps)
        gap = float(np.mean(np.diff(oms[:6])))
        Lopt = -np.log(eps)
        rec = {
            "eps": eps,
            "mean_dOmega": gap,
            "pi_over_Lopt": float(np.pi / Lopt),
            "Omega1": float(oms[0]),
        }
        out["eps_scan_ell1"].append(rec)
        print(f"  {rec}")

    out["conclusion"] = (
        "Finite proper size 2X but infinite optical depth to wall; "
        "Dirichlet tower densifies as eps→0."
    )
    print(out["conclusion"])
    (ROOT / "simple_metric_angular_timelive_L_out.json").write_text(
        json.dumps(out, indent=2)
    )
    print("DONE")


if __name__ == "__main__":
    main()
