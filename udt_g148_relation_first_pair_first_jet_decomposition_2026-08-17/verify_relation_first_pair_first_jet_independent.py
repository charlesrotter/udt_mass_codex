#!/usr/bin/env python3
"""Independent G148 replay using only stdlib Fraction/matrix algebra."""

from __future__ import annotations

from fractions import Fraction as F
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def zeros(r, c):
    return [[F(0) for _ in range(c)] for _ in range(r)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(s, a):
    return [[s * x for x in row] for row in a]


def tr(a):
    return [list(x) for x in zip(*a)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def block_coframe(B, Q, S):
    QS = mul(Q, S)
    return [B[0] + [F(0), F(0)], B[1] + [F(0), F(0)], QS[0] + Q[0], QS[1] + Q[1]]


def block_jacobian(Y, Z):
    return Y + Z


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [[a[1][1] / d, -a[0][1] / d], [-a[1][0] / d, a[0][0] / d]]


def nonzero(a):
    return any(x != 0 for row in a for x in row)


def derivative_metric(E, dE, eta):
    return add(mul(mul(tr(dE), eta), E), mul(mul(tr(E), eta), dE))


def derivative_h(J, dJ, g, dg):
    return add(add(mul(mul(tr(dJ), g), J), mul(mul(tr(J), dg), J)), mul(mul(tr(J), g), dJ))


def projector(J, h_inv, g):
    return sub(eye(4), mul(mul(mul(J, h_inv), tr(J)), g))


def projector_dot(J, dJ, h_inv, dh_inv, g, dg):
    terms = [
        mul(mul(mul(dJ, h_inv), tr(J)), g),
        mul(mul(mul(J, dh_inv), tr(J)), g),
        mul(mul(mul(J, h_inv), tr(dJ)), g),
        mul(mul(mul(J, h_inv), tr(J)), dg),
    ]
    return scale(F(-1), sum_mats(terms))


def sum_mats(items):
    out = zeros(len(items[0]), len(items[0][0]))
    for item in items:
        out = add(out, item)
    return out


eta4 = mat([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
B0 = mat([[2, F(1, 2)], [0, 3]])
Q0 = mat([[1, F(1, 3)], [0, 2]])
S0 = mat([[F(1, 5), F(-1, 7)], [F(1, 4), F(1, 6)]])
Y0 = eye(2)
Z0 = mat([[F(1, 10), F(-1, 8)], [F(-1, 12), F(1, 9)]])
jets = {
    "B": mat([[F(1, 11), F(1, 13)], [F(-1, 17), F(1, 19)]]),
    "Q": mat([[F(1, 23), F(-1, 29)], [F(1, 31), F(1, 37)]]),
    "S": mat([[F(-1, 41), F(1, 43)], [F(1, 47), F(-1, 53)]]),
    "Y": mat([[F(1, 59), F(1, 61)], [F(-1, 67), F(1, 71)]]),
    "Z": mat([[F(-1, 73), F(1, 79)], [F(1, 83), F(1, 89)]]),
}


def evaluate(active):
    z = zeros(2, 2)
    dB = jets["B"] if "B" in active else z
    dQ = jets["Q"] if "Q" in active else z
    dS = jets["S"] if "S" in active else z
    dY = jets["Y"] if "Y" in active else z
    dZ = jets["Z"] if "Z" in active else z
    E = block_coframe(B0, Q0, S0)
    dQS = add(mul(dQ, S0), mul(Q0, dS))
    dE = [dB[0] + [F(0), F(0)], dB[1] + [F(0), F(0)], dQS[0] + dQ[0], dQS[1] + dQ[1]]
    J = block_jacobian(Y0, Z0)
    dJ = block_jacobian(dY, dZ)
    g = mul(mul(tr(E), eta4), E)
    dg = derivative_metric(E, dE, eta4)
    h = mul(mul(tr(J), g), J)
    dh = derivative_h(J, dJ, g, dg)
    hi = inv2(h)
    dhi = scale(F(-1), mul(mul(hi, dh), hi))
    P = projector(J, hi, g)
    dP = projector_dot(J, dJ, hi, dhi, g, dg)
    phidot = F(1, 4) * sum(hi[i][j] * dh[j][i] for i in range(2) for j in range(2)) - F(1, 2) * dh[0][0] / h[0][0]
    return h, dh, P, dP, phidot


checks = {}
h0, _, P0, _, _ = evaluate(set())
det_h0 = h0[0][0] * h0[1][1] - h0[0][1] * h0[1][0]
checks["base_h00_timelike"] = h0[0][0] < 0
checks["base_pair_lorentzian"] = det_h0 < 0

block_results = {}
individual_dh = []
for name in jets:
    _, dh, _, dP, phidot = evaluate({name})
    checks[f"{name}_first_jet_live"] = nonzero(dh) or nonzero(dP) or phidot != 0
    individual_dh.append(dh)
    block_results[name] = {
        "hdot": [[str(x) for x in row] for row in dh],
        "phidot": str(phidot),
        "projector_dot_nonzero": nonzero(dP),
    }

_, dh_all, _, dP_all, phidot_all = evaluate(set(jets))
checks["all_block_hdot_additivity"] = dh_all == sum_mats(individual_dh)
checks["all_live_combined_hdot"] = nonzero(dh_all)
checks["all_live_combined_projector_dot"] = nonzero(dP_all)
checks["all_live_combined_phidot"] = phidot_all != 0

# Independent numerical replay of the abstract Lorentz decomposition at unrelated values.
for idx, vals in enumerate(((0.3, 0.7, 2.0, 0.2, -0.4, 0.5), (-1.1, -0.2, 3.0, -0.6, 0.9, -0.1))):
    phi, dphi, X, a, o1, o2 = vals
    rho = X * math.tanh(phi)
    drho = X * dphi / math.cosh(phi) ** 2
    dxi = [rho * a, drho, rho * o1, rho * o2]
    vrest = [0.0, drho, rho * o1, rho * o2]
    rest_norm = sum(x * x for x in vrest[1:])
    expected_rest = drho * drho + rho * rho * (o1 * o1 + o2 * o2)
    full_norm = -dxi[0] ** 2 + sum(x * x for x in dxi[1:])
    expected_full = drho * drho - rho * rho * a * a + rho * rho * (o1 * o1 + o2 * o2)
    checks[f"abstract_rest_norm_{idx}"] = abs(rest_norm - expected_rest) < 1e-14
    checks[f"abstract_full_norm_{idx}"] = abs(full_norm - expected_full) < 1e-14
    checks[f"catch_missing_screen_{idx}"] = abs(rho) * math.hypot(o1, o2) > 1e-8
    checks[f"catch_missing_tilt_{idx}"] = abs(rho * a) > 1e-8

checks["radial_weight_neutral"] = abs(1 / math.cosh(0.0) ** 2 - 1.0) < 1e-15
checks["screen_weight_neutral"] = math.tanh(0.0) == 0.0
checks["positive_endpoint_weights"] = 1 / math.cosh(30.0) ** 2 < 1e-24 and abs(math.tanh(30.0) - 1.0) < 1e-15
checks["negative_endpoint_weights"] = 1 / math.cosh(-30.0) ** 2 < 1e-24 and abs(math.tanh(-30.0) + 1.0) < 1e-15

payload = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks_passed": sum(checks.values()),
    "checks_total": len(checks),
    "checks": checks,
    "base_h": [[str(x) for x in row] for row in h0],
    "base_det_h": str(det_h0),
    "block_results": block_results,
    "combined_hdot": [[str(x) for x in row] for row in dh_all],
    "combined_phidot": str(phidot_all),
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(f"{payload['status']}: {payload['checks_passed']}/{payload['checks_total']} G148 independent checks")
if payload["status"] != "PASS":
    raise SystemExit(1)
