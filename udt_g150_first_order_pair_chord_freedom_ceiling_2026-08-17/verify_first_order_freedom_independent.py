#!/usr/bin/env python3
"""Independent direct NumPy replay of the three frozen G150 targets."""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


CASES = [
    ("W1", F(3, 2), F(5, 4), F(2, 7), -F(3, 11), F(5, 13), -F(7, 17)),
    ("W2", F(4, 3), F(7, 5), -F(5, 19), F(11, 23), -F(13, 29), F(17, 31)),
    ("W3", F(5, 2), F(9, 7), F(0), F(0), F(19, 37), -F(23, 41)),
]


def fv(x):
    return float(x)


def inner(g, x, y):
    return float(x @ g @ y)


def direct_case(Tq, Lq, pq, aq, w2q, w3q):
    T, L, p, a, w2, w3 = map(fv, (Tq, Lq, pq, aq, w2q, w3q))
    g = np.diag([-1.0, 1.0, 1.0, 1.0])
    J0 = np.array([T, 0.0, 0.0, 0.0])
    J1 = np.array([0.0, L, 0.0, 0.0])
    A = np.array([0.0, a*T*T, 0.0, 0.0])
    B = np.array([0.0, 2*p*T*L, w2*T*L, w3*T*L])
    J = np.column_stack([J0, J1])
    Jtau = np.column_stack([A, B])
    h = J.T @ g @ J
    htau = Jtau.T @ g @ J + J.T @ g @ Jtau
    Tpair = math.sqrt(-h[0, 0])
    Ttau = -htau[0, 0] / (2*Tpair)
    beta = h[0, 1] / h[0, 0]
    betatau = (htau[0, 1]*h[0, 0] - h[0, 1]*htau[0, 0]) / h[0, 0]**2
    r = J1 - beta*J0
    rtau = B - betatau*J0 - beta*A
    Lpair = math.sqrt(inner(g, r, r))
    Ltau = (2*inner(g, rtau, r)) / (2*Lpair)
    u = J0 / Tpair
    n = r / Lpair
    utau = A/Tpair - J0*Ttau/Tpair**2
    ntau = rtau/Lpair - r*Ltau/Lpair**2
    nabla_u_u = utau/Tpair
    nabla_u_n = ntau/Tpair
    an = inner(g, nabla_u_u, n)
    Omega = nabla_u_n + inner(g, nabla_u_n, u)*u - inner(g, nabla_u_n, n)*n
    phitau = 0.25*np.trace(np.linalg.inv(h) @ htau) - 0.5*htau[0, 0]/h[0, 0]
    dotphi = phitau/Tpair
    return {
        "target": np.array([p, a, w2, w3]),
        "output": np.array([dotphi, an, Omega[2], Omega[3]]),
        "phi_tau_unormalized": phitau,
        "regular": bool(h[0, 0] < 0 and np.linalg.det(h) < 0),
        "orthonormal_error": max(abs(inner(g, u, u)+1), abs(inner(g, n, n)-1), abs(inner(g, u, n))),
        "screen_error": max(abs(inner(g, Omega, u)), abs(inner(g, Omega, n))),
    }


def main():
    rows = []
    for case in CASES:
        name, *values = case
        out = direct_case(*values)
        rows.append({
            "id": name,
            "target": out["target"].tolist(),
            "output": out["output"].tolist(),
            "max_abs_error": float(np.max(np.abs(out["output"] - out["target"]))),
            "regular": out["regular"],
            "orthonormal_error": out["orthonormal_error"],
            "screen_error": out["screen_error"],
        "wrong_clock_error": abs(out["phi_tau_unormalized"] - out["target"][0]),
        "missing_screen_error": max(abs(out["target"][2]), abs(out["target"][3])),
        "dotphi_equals_an_residual": abs(out["output"][0] - out["output"][1]),
        })
    gates = {
        "all_targets_recovered": max(row["max_abs_error"] for row in rows) < 1e-12,
        "all_regular": all(row["regular"] for row in rows),
        "all_orthonormal": max(row["orthonormal_error"] for row in rows) < 1e-12,
        "all_screen": max(row["screen_error"] for row in rows) < 1e-12,
        "mutation_unnormalized_clock_rejected": any(row["wrong_clock_error"] > 1e-6 for row in rows),
        "mutation_missing_screen_rejected": any(row["missing_screen_error"] > 1e-6 for row in rows),
        "counterexample_dotphi_equals_an": any(row["dotphi_equals_an_residual"] > 1e-6 for row in rows),
    }
    result = {
        "schema": "udt.g150.independent.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "method": "direct NumPy pullback and normalized-frame replay; no production import",
        "cases": rows,
        "gates": gates,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
