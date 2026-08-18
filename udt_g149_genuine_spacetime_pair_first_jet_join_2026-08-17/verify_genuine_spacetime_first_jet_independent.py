#!/usr/bin/env python3
"""Independent float64 replay of G149; deliberately imports no production code."""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def a(rows):
    return np.array([[float(F(str(x))) for x in row] for row in rows], dtype=np.float64)


def v(items):
    return np.array([float(F(str(x))) for x in items], dtype=np.float64)


def assemble_E(B, Q, S):
    return np.block([[B, np.zeros((2, 2))], [Q @ S, Q]])


def data():
    B0 = a([[2, "1/2"], [0, 3]])
    Q0 = a([[1, "1/3"], [0, 2]])
    S0 = a([["1/5", "-1/7"], ["1/4", "1/6"]])
    dB = [
        a([["1/11", "1/13"], ["-1/17", "1/19"]]),
        a([["-1/23", "1/29"], ["1/31", "-1/37"]]),
        a([["1/41", "-1/43"], ["1/47", "1/53"]]),
        a([["-1/59", "-1/61"], ["1/67", "1/71"]]),
    ]
    dQ = [
        a([["1/73", "-1/79"], ["1/83", "1/89"]]),
        a([["-1/97", "1/101"], ["1/103", "1/107"]]),
        a([["1/109", "1/113"], ["-1/127", "1/131"]]),
        a([["1/137", "-1/139"], ["1/149", "-1/151"]]),
    ]
    dS = [
        a([["-1/157", "1/163"], ["1/167", "-1/173"]]),
        a([["1/179", "1/181"], ["-1/191", "1/193"]]),
        a([["1/197", "-1/199"], ["1/211", "1/223"]]),
        a([["-1/227", "1/229"], ["-1/233", "1/239"]]),
    ]
    J0 = v([1, 0, "1/10", "-1/12"])
    J1 = v([0, 1, "-1/8", "1/9"])
    Ftt = v(["1/59", "-1/67", "-1/73", "1/83"])
    Fts = v(["1/61", "1/71", "1/79", "1/89"])
    return B0, Q0, S0, dB, dQ, dS, J0, J1, Ftt, Fts


def inner(g, x, y):
    return float(x @ g @ y)


def evaluate(dB, dQ, dS, Ftt, Fts, with_identity=False):
    B0, Q0, S0, _, _, _, J0, J1, _, _ = data()
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    E0 = assemble_E(B0, Q0, S0)
    dE = []
    for mu in range(4):
        dE.append(np.block([
            [dB[mu], np.zeros((2, 2))],
            [dQ[mu] @ S0 + Q0 @ dS[mu], dQ[mu]],
        ]))
    g = E0.T @ eta @ E0
    dg = [de.T @ eta @ E0 + E0.T @ eta @ de for de in dE]
    gi = np.linalg.inv(g)
    Gamma = np.zeros((4, 4, 4))
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                Gamma[rho, mu, nu] = 0.5 * sum(
                    gi[rho, sig] * (dg[mu][sig, nu] + dg[nu][sig, mu] - dg[sig][mu, nu])
                    for sig in range(4)
                )

    def G(x, y):
        return np.einsum("rmn,m,n->r", Gamma, x, y)

    J = np.column_stack([J0, J1])
    Jtau = np.column_stack([Ftt, Fts])
    h = J.T @ g @ J
    gtau = sum(J0[mu] * dg[mu] for mu in range(4))
    htau = Jtau.T @ g @ J + J.T @ gtau @ J + J.T @ g @ Jtau
    T = math.sqrt(-h[0, 0])
    Ttau = -htau[0, 0] / (2 * T)
    beta = h[0, 1] / h[0, 0]
    betatau = (htau[0, 1] * h[0, 0] - h[0, 1] * htau[0, 0]) / h[0, 0] ** 2
    r = J1 - beta * J0
    rtau = Fts - betatau * J0 - beta * Ftt
    L = math.sqrt(inner(g, r, r))
    L2tau = 2 * inner(g, rtau, r) + inner(gtau, r, r)
    Ltau = L2tau / (2 * L)
    u = J0 / T
    utau = Ftt / T - J0 * Ttau / T**2
    n = r / L
    ntau = rtau / L - r * Ltau / L**2
    nabla_u_u = utau / T + G(u, u)
    nabla_u_n = ntau / T + G(u, n)
    an = inner(g, nabla_u_u, n)
    Omega = nabla_u_n + inner(g, nabla_u_n, u) * u - inner(g, nabla_u_n, n) * n
    phitau = 0.25 * np.trace(np.linalg.inv(h) @ htau) - 0.5 * htau[0, 0] / h[0, 0]
    dotphi = phitau / T

    out = {
        "g": g,
        "h": h,
        "u": u,
        "n": n,
        "dotphi": dotphi,
        "a_n": an,
        "Omega": Omega,
    }
    if with_identity:
        phi = 0.25 * math.log((-np.linalg.det(h)) / h[0, 0] ** 2)
        q = math.tanh(phi)
        rhotau = (1 - q*q) * phitau
        xi = q * n
        xitau = rhotau * n + q * ntau
        direct = xitau / T + G(u, xi)
        split = (1 - q*q) * dotphi * n + q * Omega + q * an * u
        out["identity_residual"] = direct - split
    return out


def main():
    B0, Q0, S0, dB, dQ, dS, J0, J1, Ftt, Fts = data()
    base = evaluate(dB, dQ, dS, Ftt, Fts, with_identity=True)
    zeros = [np.zeros((2, 2)) for _ in range(4)]
    Ftt_no_y, Fts_no_y = Ftt.copy(), Fts.copy()
    Ftt_no_y[:2] = 0.0
    Fts_no_y[:2] = 0.0
    Ftt_no_z, Fts_no_z = Ftt.copy(), Fts.copy()
    Ftt_no_z[2:] = 0.0
    Fts_no_z[2:] = 0.0
    controls = {
        "B": evaluate(zeros, dQ, dS, Ftt, Fts),
        "Q": evaluate(dB, zeros, dS, Ftt, Fts),
        "S": evaluate(dB, dQ, zeros, Ftt, Fts),
        "Y": evaluate(dB, dQ, dS, Ftt_no_y, Fts_no_y),
        "Z": evaluate(dB, dQ, dS, Ftt_no_z, Fts_no_z),
    }

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    comparisons = {
        "dotphi": abs(base["dotphi"] - production["derived_first_jet"]["dotphi_float"]),
        "a_n": abs(base["a_n"] - production["derived_first_jet"]["a_n_float"]),
        "Omega_max": float(np.max(np.abs(base["Omega"] - np.array(production["derived_first_jet"]["Omega_float"])))),
    }
    liveness = {}
    liveness_agreement = {}
    for name, control in controls.items():
        deltas = {
            "delta_dotphi": base["dotphi"] - control["dotphi"],
            "delta_a_n": base["a_n"] - control["a_n"],
            "delta_Omega": base["Omega"] - control["Omega"],
        }
        changed = max(
            abs(deltas["delta_dotphi"]),
            abs(deltas["delta_a_n"]),
            float(np.max(np.abs(deltas["delta_Omega"]))),
        ) > 1e-12
        liveness[name] = {
            "changed": bool(changed),
            "delta_dotphi": float(deltas["delta_dotphi"]),
            "delta_a_n": float(deltas["delta_a_n"]),
            "delta_Omega": deltas["delta_Omega"].tolist(),
        }
        prod_control = production["liveness"][name]
        liveness_agreement[name] = max(
            abs(deltas["delta_dotphi"] - prod_control["delta_dotphi_float"]),
            abs(deltas["delta_a_n"] - prod_control["delta_a_n_float"]),
            float(np.max(np.abs(deltas["delta_Omega"] - np.array(prod_control["delta_Omega_float"])))),
        )

    g, h, u, n, Omega = base["g"], base["h"], base["u"], base["n"], base["Omega"]
    residual = base["identity_residual"]
    gates = {
        "regular": bool(h[0, 0] < 0 and np.linalg.det(h) < 0),
        "orthonormal": bool(abs(inner(g, u, u) + 1) < 1e-12 and abs(inner(g, n, n) - 1) < 1e-12 and abs(inner(g, u, n)) < 1e-12),
        "screen": bool(abs(inner(g, Omega, u)) < 1e-12 and abs(inner(g, Omega, n)) < 1e-12),
        "identity": bool(np.max(np.abs(residual)) < 1e-12),
        "production_agreement": bool(max(comparisons.values()) < 1e-12),
        "all_BQS_gradient_and_clock_direction_YZ_families_live": bool(all(item["changed"] for item in liveness.values())),
        "liveness_deltas_agree": bool(max(liveness_agreement.values()) < 1e-12),
    }
    result = {
        "schema": "udt.g149.independent.v2",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "method": "independent NumPy float64 LC, pair-chain-rule, and five-control replay; no production import",
        "dotphi": base["dotphi"],
        "a_n": base["a_n"],
        "Omega": base["Omega"].tolist(),
        "identity_residual_max_abs": float(np.max(np.abs(residual))),
        "production_comparison_abs": comparisons,
        "liveness": liveness,
        "liveness_production_comparison_max_abs": liveness_agreement,
        "gates": gates,
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
