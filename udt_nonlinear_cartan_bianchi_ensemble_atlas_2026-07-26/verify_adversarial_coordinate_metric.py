#!/usr/bin/env python3
"""Independent coordinate-metric two-jet control at an all-sector rational jet."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as s


PKG = Path(__file__).resolve().parent
t, x, y, z = s.symbols("t x y z", real=True)
coords = (t, x, y, z)
origin = {t: 0, x: 0, y: 0, z: 0}
Q = s.Rational

# Distinct nonzero first and second jets in every registered amplitude. All
# values vanish at the point, so coordinate and orthonormal frames coincide
# there without a frame-transform shortcut.
phi = Q(1, 3) * t + Q(2, 5) * x + Q(1, 7) * t * t + Q(1, 11) * t * x - Q(1, 13) * x * x
sig = -Q(2, 7) * t + Q(3, 8) * x + Q(1, 9) * t * t - Q(1, 10) * t * x + Q(1, 12) * x * x
alp = Q(1, 5) * t - Q(1, 6) * x - Q(1, 8) * t * t + Q(1, 14) * t * x + Q(1, 15) * x * x
kk = -Q(1, 4) * t + Q(2, 9) * x + Q(1, 10) * t * t + Q(1, 16) * t * x - Q(1, 18) * x * x
S10 = Q(1, 7) * t + Q(1, 3) * x + Q(1, 11) * t * t - Q(1, 17) * t * x + Q(1, 19) * x * x
S11 = -Q(2, 9) * t + Q(1, 5) * x - Q(1, 12) * t * t + Q(1, 13) * t * x + Q(1, 20) * x * x
S20 = Q(3, 10) * t - Q(1, 8) * x + Q(1, 14) * t * t + Q(1, 15) * t * x - Q(1, 21) * x * x
S21 = -Q(1, 6) * t - Q(2, 11) * x + Q(1, 16) * t * t - Q(1, 18) * t * x + Q(1, 22) * x * x

r = s.exp(sig / 2 - alp)
q = s.exp(sig / 2 + alp)
D = s.Matrix([[r, kk * r], [0, q]])
coframe = s.Matrix([
    [s.exp(-phi), 0, 0, 0],
    [0, s.exp(phi), 0, 0],
    [r * (S10 + kk * S20), r * (S11 + kk * S21), r, kk * r],
    [q * S20, q * S21, 0, q],
])
eta = s.diag(-1, 1, 1, 1)
g = s.simplify(coframe.T * eta * coframe)


def at(expression):
    return s.simplify(expression.subs(origin))


g0 = s.Matrix(4, 4, lambda i, j: at(g[i, j]))
gi0 = g0.inv()
dg = [s.Matrix(4, 4, lambda i, j: at(s.diff(g[i, j], coords[k]))) for k in range(4)]
ddg = [
    [s.Matrix(4, 4, lambda i, j: at(s.diff(g[i, j], coords[k], coords[l]))) for l in range(4)]
    for k in range(4)
]
dgi = [-gi0 * dg[k] * gi0 for k in range(4)]


def A(lam, mu, nu):
    return dg[nu][lam, mu] + dg[mu][lam, nu] - dg[lam][mu, nu]


def dA(kdir, lam, mu, nu):
    return ddg[kdir][nu][lam, mu] + ddg[kdir][mu][lam, nu] - ddg[kdir][lam][mu, nu]


Gamma = {}
dGamma = {}
for rho in range(4):
    for mu in range(4):
        for nu in range(4):
            Gamma[rho, mu, nu] = s.factor(
                sum(gi0[rho, lam] * A(lam, mu, nu) for lam in range(4)) / 2
            )
            for kdir in range(4):
                dGamma[kdir, rho, mu, nu] = s.factor(sum(
                    dgi[kdir][rho, lam] * A(lam, mu, nu)
                    + gi0[rho, lam] * dA(kdir, lam, mu, nu)
                    for lam in range(4)
                ) / 2)


def Rcoord_up(rho, sigidx, mu, nu):
    return s.factor(
        dGamma[mu, rho, nu, sigidx] - dGamma[nu, rho, mu, sigidx]
        + sum(
            Gamma[rho, mu, k] * Gamma[k, nu, sigidx]
            - Gamma[rho, nu, k] * Gamma[k, mu, sigidx]
            for k in range(4)
        )
    )


def Rcoord_low(rho, sigidx, mu, nu):
    return s.factor(sum(g0[rho, k] * Rcoord_up(k, sigidx, mu, nu) for k in range(4)))


E0 = lambda expression: s.exp(phi) * s.diff(expression, t)
E1 = lambda expression: s.exp(-phi) * s.diff(expression, x)
Fbase = s.Matrix([s.diff(S11, t) - s.diff(S10, x), s.diff(S21, t) - s.diff(S20, x)])
fvec = D * Fbase
channel_expr = {
    "u0": E0(phi), "u1": E1(phi), "s0": E0(sig), "s1": E1(sig),
    "a0": E0(alp), "a1": E1(alp),
    "h0": s.exp(-2 * alp) * E0(kk), "h1": s.exp(-2 * alp) * E1(kk),
    "f2": fvec[0], "f3": fvec[1],
}
substitutions = {s.Symbol(name): at(expression) for name, expression in channel_expr.items()}
for name, expression in channel_expr.items():
    substitutions[s.Symbol("E0_" + name)] = at(E0(expression))
    substitutions[s.Symbol("E1_" + name)] = at(E1(expression))

with (PKG / "CURVATURE_COMPONENTS.tsv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
bad = []
comparisons = []
for row in rows:
    a, b = map(int, row["lower_pair"])
    c, d = map(int, row["two_form_leg"])
    production = s.sympify(row["coefficient"]).subs(substitutions)
    coordinate = Rcoord_low(a, b, c, d)
    delta = s.simplify(production - coordinate)
    comparisons.append((a, b, c, d, production, coordinate))
    if delta != 0:
        bad.append((a, b, c, d, str(delta), str(production), str(coordinate)))

Rscalar_coordinate = s.factor(sum(
    gi0[i, j] * sum(gi0[a, c] * Rcoord_low(c, i, a, j) for a in range(4) for c in range(4))
    for i in range(4)
    for j in range(4)
))
with (PKG / "CURVATURE_CONTRACTIONS.tsv").open(newline="", encoding="utf-8") as handle:
    contractions = {row["contraction"]: row["expression"] for row in csv.DictReader(handle, delimiter="\t")}
Rscalar_production = s.factor(s.sympify(contractions["scalar_curvature"]).subs(substitutions))

result = {
    "comparison_point": "all amplitude values zero; all first/second base jets nonzero rational controls",
    "metric_at_point": str(g0.tolist()),
    "curvature_components_compared": len(comparisons),
    "curvature_mismatches": len(bad),
    "coordinate_scalar": str(Rscalar_coordinate),
    "production_scalar": str(Rscalar_production),
    "scalar_delta": str(s.simplify(Rscalar_coordinate - Rscalar_production)),
    "selected_exact_components": [
        {"component": f"R{a}{b}{c}{d}", "value": str(value)}
        for a, b, c, d, value, other in comparisons
        if (a, b, c, d) in ((0, 1, 0, 1), (0, 2, 0, 3), (0, 2, 1, 2), (2, 3, 2, 3))
    ],
}
print(json.dumps(result, indent=2, sort_keys=True))
if bad:
    raise SystemExit(1)
