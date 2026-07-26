#!/usr/bin/env python3
"""Independent Koszul/frame verifier; does not import production code."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as s


PKG = Path(__file__).resolve().parent
REPO = PKG.parent
eta = (-1, 1, 1, 1)
pairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]
u0, u1, s0, s1, a0, a1, h0, h1, f2, f3 = s.symbols(
    "u0 u1 s0 s1 a0 a1 h0 h1 f2 f3", real=True
)
channels = (u0, u1, s0, s1, a0, a1, h0, h1, f2, f3)
E = {(i, x): s.Symbol(f"E{i}_{x}", real=True) for i in (0, 1) for x in channels}

# k[a,b,c] is the coefficient of theta^b wedge theta^c in d theta^a, b<c.
k = {}


def put(a, b, c, value):
    k[a, b, c] = s.sympify(value)


put(0, 0, 1, u1)
put(1, 0, 1, u0)
put(2, 0, 1, f2)
put(2, 0, 2, s0 / 2 - a0)
put(2, 0, 3, h0)
put(2, 1, 2, s1 / 2 - a1)
put(2, 1, 3, h1)
put(3, 0, 1, f3)
put(3, 0, 3, s0 / 2 + a0)
put(3, 1, 3, s1 / 2 + a1)


def kval(a, b, c):
    if b == c:
        return s.S.Zero
    return k.get((a, b, c), 0) if b < c else -k.get((a, c, b), 0)


def C_up(a, b, c):
    return -kval(a, b, c)


def C_low(a, b, c):
    return eta[a] * C_up(a, b, c)


# Koszul: Gamma_{a b c}=<e_a,nabla_{e_c}e_b>.
Gamma_low = {}
for a in range(4):
    for b in range(4):
        for c in range(4):
            Gamma_low[a, b, c] = s.factor(
                (-C_low(c, b, a) + C_low(b, a, c) + C_low(a, c, b)) / 2
            )


def Gamma_up(a, b, c):
    return eta[a] * Gamma_low[a, b, c]


MC = {
    E[0, s1]: E[1, s0] - u1 * s0 - u0 * s1,
    E[0, a1]: E[1, a0] - u1 * a0 - u0 * a1,
    E[0, h1]: E[1, h0] - u1 * h0 - u0 * h1 - 2 * a0 * h1 + 2 * a1 * h0,
}


def frame_deriv(i, expression):
    if i > 1:
        return s.S.Zero
    return s.expand(sum(s.diff(expression, x) * E[i, x] for x in channels))


def R_up(a, b, c, d):
    value = frame_deriv(c, Gamma_up(a, b, d)) - frame_deriv(d, Gamma_up(a, b, c))
    value -= sum(C_up(e, c, d) * Gamma_up(a, b, e) for e in range(4))
    value += sum(
        Gamma_up(a, e, c) * Gamma_up(e, b, d)
        - Gamma_up(a, e, d) * Gamma_up(e, b, c)
        for e in range(4)
    )
    return s.factor(s.expand(value).subs(MC))


Rlow = {
    (a, b, c, d): s.factor(eta[a] * R_up(a, b, c, d))
    for a, b in pairs
    for c, d in pairs
}


def tab_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


local_channels = {str(x): x for x in channels}
conn_prod = {
    (int(row["lower_pair"][0]), int(row["lower_pair"][1]), int(row["basis_leg"])):
    s.sympify(row["coefficient"], locals=local_channels)
    for row in tab_rows(PKG / "CONNECTION_COEFFICIENTS.tsv")
}
conn_bad = []
for a, b in pairs:
    for c in range(4):
        delta = s.simplify(Gamma_low[a, b, c] - conn_prod[a, b, c])
        if delta != 0:
            conn_bad.append((a, b, c, delta))

local_all = dict(local_channels)
local_all.update({str(value): value for value in E.values()})
curv_prod = {
    (int(row["lower_pair"][0]), int(row["lower_pair"][1]),
     int(row["two_form_leg"][0]), int(row["two_form_leg"][1])):
    s.sympify(row["coefficient"], locals=local_all)
    for row in tab_rows(PKG / "CURVATURE_COMPONENTS.tsv")
}
curv_bad = []
for key, independent in Rlow.items():
    delta = s.simplify(independent - curv_prod[key])
    if delta != 0:
        curv_bad.append((key, delta))


def r_any(a, b, c, d):
    sign = 1
    if a == b or c == d:
        return s.S.Zero
    if a > b:
        a, b = b, a
        sign = -sign
    if c > d:
        c, d = d, c
        sign = -sign
    return sign * Rlow[a, b, c, d]


pair_exchange_bad = []
for a, b in pairs:
    for c, d in pairs:
        value = s.simplify(Rlow[a, b, c, d] - Rlow[c, d, a, b])
        if value != 0:
            pair_exchange_bad.append(((a, b, c, d), value))

first_bianchi_bad = []
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(c + 1, 4):
                if len({b, c, d}) < 3:
                    continue
                value = s.simplify(r_any(a, b, c, d) + r_any(a, c, d, b) + r_any(a, d, b, c))
                if value != 0:
                    first_bianchi_bad.append(((a, b, c, d), value))

Ric = [
    [s.factor(sum(eta[a] * r_any(a, b, a, d) for a in range(4))) for d in range(4)]
    for b in range(4)
]
Rscalar = s.factor(sum(eta[b] * Ric[b][b] for b in range(4)))
contract_prod = {
    row["contraction"]: s.sympify(row["expression"], locals=local_all)
    for row in tab_rows(PKG / "CURVATURE_CONTRACTIONS.tsv")
}
scalar_delta = s.simplify(Rscalar - contract_prod["scalar_curvature"])
ricci_bad = []
for b in range(4):
    for d in range(b, 4):
        value = s.simplify(Ric[b][d] - contract_prod[f"Ricci{b}{d}"])
        if value != 0:
            ricci_bad.append(((b, d), value))

# Independent neutral-jet bridge to the parent scalar formula.
names = [
    f"d{i}_{name}"
    for i in (0, 1)
    for name in ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")
]
rate = dict(zip(names, s.symbols(" ".join(names), real=True)))
neutral = {value: s.S.Zero for value in E.values()}
neutral.update({
    u0: rate["d0_phi"], u1: rate["d1_phi"],
    s0: rate["d0_sigma"], s1: rate["d1_sigma"],
    a0: rate["d0_alpha"], a1: rate["d1_alpha"],
    h0: rate["d0_k"], h1: rate["d1_k"],
    f2: rate["d0_S11"] - rate["d1_S10"],
    f3: rate["d0_S21"] - rate["d1_S20"],
    E[0, u0]: rate["d0_phi"] ** 2,
    E[1, u1]: -rate["d1_phi"] ** 2,
    E[0, s0]: rate["d0_phi"] * rate["d0_sigma"],
    E[1, s1]: -rate["d1_phi"] * rate["d1_sigma"],
})
parent = json.loads(
    (REPO / "udt_metric_orchestra_rehearsal_2026-07-25" / "ALGEBRA_RESULT.json")
    .read_text(encoding="utf-8")
)
parent_R = s.sympify(parent["exact_objects"]["scalar_curvature_rate_form"], locals=rate)
neutral_delta = s.simplify(Rscalar.subs(neutral) - parent_R)

# Reconstruct the family graph from the independently calculated polynomials.
family = {
    u0: "PHI_ANHOLONOMY", u1: "PHI_ANHOLONOMY",
    s0: "ANGULAR_COMMON", s1: "ANGULAR_COMMON",
    a0: "ANGULAR_RECIPROCAL", a1: "ANGULAR_RECIPROCAL",
    h0: "ANGULAR_SHEAR", h1: "ANGULAR_SHEAR",
    f2: "CONNECTION_CURVATURE_1", f3: "CONNECTION_CURVATURE_2",
}
quadratic = set()
derivative_families = set()
all_variables = channels + tuple(E.values())
for expression in Rlow.values():
    polynomial = s.Poly(s.expand(expression), *all_variables)
    for monomial, coefficient in polynomial.terms():
        if coefficient == 0:
            continue
        structural = []
        derivatives = []
        for variable, exponent in zip(all_variables, monomial):
            (derivatives if variable in E.values() else structural).extend([variable] * exponent)
        if len(derivatives) == 1 and not structural:
            channel = next(channel for (i, channel), value in E.items() if value == derivatives[0])
            derivative_families.add(family[channel])
        elif len(structural) == 2 and not derivatives:
            quadratic.add(tuple(sorted((family[structural[0]], family[structural[1]]))))
        else:
            raise AssertionError((expression, monomial, coefficient))

source_hash_bad = []
for row in tab_rows(PKG / "SOURCE_MANIFEST.tsv"):
    data = (REPO / row["path"]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != row["sha256"] or len(data) != int(row["size_bytes"]):
        source_hash_bad.append((row["source_id"], len(data), digest))

result = {
    "connection_rows": 24,
    "connection_mismatches": len(conn_bad),
    "curvature_rows": 36,
    "curvature_mismatches": len(curv_bad),
    "pair_exchange_mismatches": len(pair_exchange_bad),
    "first_bianchi_mismatches": len(first_bianchi_bad),
    "ricci_mismatches": len(ricci_bad),
    "scalar_delta": str(scalar_delta),
    "neutral_parent_delta": str(neutral_delta),
    "derivative_families": sorted(derivative_families),
    "quadratic_pairs": sorted("--".join(pair) for pair in quadratic),
    "quadratic_pair_count": len(quadratic),
    "phi_f1_present": tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_1"))) in quadratic,
    "phi_f2_present": tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_2"))) in quadratic,
    "source_hash_mismatches": source_hash_bad,
}
print(json.dumps(result, indent=2, sort_keys=True))
if any((
    conn_bad, curv_bad, pair_exchange_bad, first_bianchi_bad, ricci_bad,
    scalar_delta != 0, neutral_delta != 0, source_hash_bad,
)):
    raise SystemExit(1)
