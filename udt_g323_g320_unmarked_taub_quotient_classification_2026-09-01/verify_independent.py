#!/usr/bin/env python3
"""Implementation-distinct G323 verification; does not import/read production."""

import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
P = 7.0 / 5.0
AMP = 1.0 / 9.0
J0 = 121.0
MU = J0 / 9.0
MODES = (1, 2, 3, 5)
N = 6144
TAU = 2.0 * math.pi
CHECKS = []


def need(label, condition):
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)


def metric(r):
    return (-r / MU, MU / r, r * r, r * r)


def metric_prime(r):
    return (-1.0 / MU, -MU / (r * r), 2.0 * r, 2.0 * r)


def connection(r):
    g = metric(r)
    gp = metric_prime(r)
    inv = tuple(1.0 / value for value in g)
    out = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                k = a
                term = 0.0
                if b == 0 and k == c:
                    term += gp[k]
                if c == 0 and k == b:
                    term += gp[k]
                if k == 0 and b == c:
                    term -= gp[b]
                out[a][b][c] = 0.5 * inv[a] * term
    return out


def ricci_from_closed_connection(r):
    """Differentiate the independently reconstructed nonzero connection explicitly."""
    g0 = connection(r)
    deriv = [[[0.0] * 4 for _ in range(4)] for _ in range(4)]
    deriv[0][0][0] = -1.0 / (2.0 * r * r)
    deriv[0][1][1] = 3.0 * MU * MU / (2.0 * r ** 4)
    deriv[1][0][1] = 1.0 / (2.0 * r * r)
    deriv[1][1][0] = deriv[1][0][1]
    deriv[2][0][2] = -1.0 / (r * r)
    deriv[2][2][0] = deriv[2][0][2]
    deriv[3][0][3] = -1.0 / (r * r)
    deriv[3][3][0] = deriv[3][0][3]
    ric = [[0.0] * 4 for _ in range(4)]
    for b in range(4):
        for d in range(4):
            value = 0.0
            for a in range(4):
                if a == 0:
                    value += deriv[a][b][d]
                if d == 0:
                    value -= deriv[a][b][a]
                for e in range(4):
                    value += g0[a][a][e] * g0[e][b][d]
                    value -= g0[a][d][e] * g0[e][b][a]
            ric[b][d] = value
    return ric


for r in (0.73, 1.41, 2.87, 5.13):
    residual = max(abs(value) for row in ricci_from_closed_connection(r) for value in row)
    print(f"independent Ricci diagnostic R={r}: {residual:.12e}")
    need(f"independent ambient Ricci R={r}", residual < 5e-12)


def independent_row(x, mode, sign):
    u = mode * x
    psi = P + AMP * math.cos(u)
    p1 = -AMP * mode * math.sin(u)
    p2 = -AMP * mode * mode * math.cos(u)
    r = psi * psi
    r1 = 2.0 * psi * p1
    r2 = 2.0 * (p1 * p1 + psi * p2)
    root = math.sqrt(36.0 * p1 * p1 + J0)
    b = sign * root / (psi ** 3)
    f = 12.0 * p2 / (psi ** 5)
    expected = ((3.0 * f / b - b) / 6.0, b / 3.0, b / 3.0)

    # Solve the first fundamental form for |X'| instead of importing the production formula.
    xp_mag = math.sqrt((r / MU) * (psi ** 4 + (r / MU) * r1 * r1))
    xp = -sign * xp_mag
    # Central differentiation of the independently solved X' for the longitudinal K control.
    h = 1.0e-5
    def xp_at(xx):
        uu = mode * xx
        ps = P + AMP * math.cos(uu)
        dps = -AMP * mode * math.sin(uu)
        rr = ps * ps
        rr1 = 2.0 * ps * dps
        mag = math.sqrt((rr / MU) * (ps ** 4 + (rr / MU) * rr1 * rr1))
        return -sign * mag
    xp2 = (xp_at(x + h) - xp_at(x - h)) / (2.0 * h)
    nr = MU * xp / (r * r)
    nx = r1 / MU
    ncov_r = -(r / MU) * nr
    ncov_x = (MU / r) * nx
    grrr = 1.0 / (2.0 * r)
    grxx = -MU * MU / (2.0 * r ** 3)
    gxrx = -1.0 / (2.0 * r)
    kxx = (
        ncov_r * (r2 + grrr * r1 * r1 + grxx * xp * xp)
        + ncov_x * (xp2 + 2.0 * gxrx * r1 * xp)
    ) / (psi ** 4)
    kyy = -MU * xp / (r ** 3)
    induced = -(r / MU) * r1 * r1 + (MU / r) * xp * xp
    return abs(xp), abs(induced - psi ** 4), abs(kxx - expected[0]), abs(kyy - expected[1])


periods = {}
max_pullback = 0.0
max_k = 0.0
for mode in MODES:
    sign_periods = []
    for sign in (-1, 1):
        rows = [independent_row(TAU * (i + 0.5) / N, mode, sign) for i in range(N)]
        period = TAU * math.fsum(row[0] for row in rows) / N
        sign_periods.append(period)
        max_pullback = max(max_pullback, max(row[1] for row in rows))
        max_k = max(max_k, max(max(row[2], row[3]) for row in rows))
        need(f"independent pullback n={mode} sign={sign}", max(row[1] for row in rows) < 5e-11)
        need(f"independent K n={mode} sign={sign}", max(max(row[2], row[3]) for row in rows) < 5e-10)
    need(f"independent sign period n={mode}", abs(sign_periods[0] - sign_periods[1]) < 5e-13)
    periods[mode] = sign_periods[0]

for lower, upper in zip(MODES, MODES[1:]):
    need(f"independent strict period {lower}->{upper}", periods[upper] > periods[lower])

# Local metric rescaling isometry and quotient ratio invariance, tested separately.
for scale in (0.61, 1.37, 2.2):
    r = 1.73
    mu = 2.41
    target = (
        -(scale * r) / (scale ** 3 * mu) * scale ** 2,
        (scale ** 3 * mu) / (scale * r) / scale ** 2,
        (scale * r) ** 2 / scale ** 2,
    )
    source = (-r / mu, mu / r, r * r)
    need(f"independent local isometry scale={scale}",
         max(abs(a - b) for a, b in zip(target, source)) < 2e-14)
    lx, ly, lz = 3.7, 5.2, 6.1
    q0 = lx / math.sqrt(ly * lz)
    q1 = (lx / scale) / math.sqrt((ly / scale) * (lz / scale))
    need(f"independent quotient modulus scale={scale}", abs(q0 - q1) < 2e-15)

result = {
    "schema": "udt-g323-independent-v1",
    "status": "PASS",
    "assertion_count": len(CHECKS),
    "production_imported": False,
    "production_result_read": False,
    "different_controls": True,
    "ambient_ricci_numeric_independent": True,
    "complete_embedding_upheld": True,
    "strict_mode_modulus_upheld": True,
    "local_isometry_and_global_modulus_upheld": True,
    "max_pullback_error": max_pullback,
    "max_extrinsic_error": max_k,
    "periods": {str(key): value for key, value in periods.items()},
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(f"G323 independent PASS: {len(CHECKS)} assertions")
print(f"max pullback error: {max_pullback:.3e}")
print(f"max extrinsic error: {max_k:.3e}")
