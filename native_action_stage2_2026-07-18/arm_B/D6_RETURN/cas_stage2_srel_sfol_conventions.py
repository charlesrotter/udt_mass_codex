#!/usr/bin/env python3
"""Stage-II convention audit for the illustrative S_rel / S_fol formulas.

This script checks only algebraic convention questions:
1. ADM/static decomposition of the covariant carrier action.
2. Ordered-index factor convention for F_{mu nu} F^{mu nu}.
3. Which sign/factor mapping matches the static E2+E4 energy.

It does not certify any action premise, boundary choice, or carrier ontology.
"""

import sympy as sp


N, sqrt_h = sp.symbols("N sqrt_h", positive=True)
xi, kappa4 = sp.symbols("xi kappa4", real=True)
Dt2, Xs, E0, Bm = sp.symbols("Dt2 Xs E0 Bm", real=True)
alpha, beta, gamma, delta = sp.symbols("alpha beta gamma delta", real=True)


def line(label, expr):
    print(f"{label}: {sp.simplify(expr)}")


print("Signature convention: (-,+,+,+)")
print("ADM convention: ds^2 = -N^2 dt^2 + h_ij dx^i dx^j, zero shift for the static audit")
print("Ordered-index convention: F_{mu nu} F^{mu nu} sums over all ordered pairs")
print()

# With zero shift, g^{00}=-1/N^2 and g^{ij}=h^{ij}.  Let:
# Dt2 = (D_t n)^2
# Xs  = h^{ij} \partial_i n . \partial_j n
# E0  = h^{ij} F_{0i} F_{0j}
# Bm  = h^{ik} h^{jl} F_{ij} F_{kl}
F_contract = -2 * E0 / N**2 + Bm
line("F_{mu nu} F^{mu nu}", F_contract)

L_rel_phys = -N * sqrt_h * (
    xi * (-Dt2 / N**2 + Xs) / 2
    + kappa4 * F_contract / 4
)
L_rel_phys = sp.expand(L_rel_phys)
line("Corrected covariant L_rel density", L_rel_phys)

L_rel_static = sp.simplify(L_rel_phys.subs({Dt2: 0, E0: 0}))
line("Corrected covariant L_rel density on a static slice", L_rel_static)

expected_static = -N * sqrt_h * (xi * Xs / 2 + kappa4 * Bm / 4)
line("Expected static density for positive E2+E4", expected_static)
print("Static-match check:", sp.simplify(L_rel_static - expected_static) == 0)
print()

# Stage-I illustrative sign pattern as written in D2.4 for S_rel lacked the
# overall minus sign:
L_rel_stage1 = N * sqrt_h * (
    xi * (-Dt2 / N**2 + Xs) / 2
    + kappa4 * F_contract / 4
)
L_rel_stage1_static = sp.simplify(L_rel_stage1.subs({Dt2: 0, E0: 0}))
line("Stage-I illustrative S_rel static density as written", L_rel_stage1_static)
print("Stage-I S_rel static sign matches expected:", sp.simplify(L_rel_stage1_static - expected_static) == 0)
print()

# Two foliation forms:
# 1. The sign pattern written in Stage-I D2.4.
# 2. The corrected sign pattern that matches the covariant decomposition above.
L_fol_stage1 = N * sqrt_h * (
    alpha * Dt2 / (2 * N**2)
    - beta * Xs / 2
    - gamma * E0 / (2 * N**2)
    - delta * Bm / 4
)
L_fol_corrected = N * sqrt_h * (
    alpha * Dt2 / (2 * N**2)
    - beta * Xs / 2
    + gamma * E0 / (2 * N**2)
    - delta * Bm / 4
)

match_stage1 = sp.simplify(
    L_fol_stage1.subs({alpha: xi, beta: xi, gamma: -kappa4, delta: kappa4}) - L_rel_phys
)
match_corrected = sp.simplify(
    L_fol_corrected.subs({alpha: xi, beta: xi, gamma: kappa4, delta: kappa4}) - L_rel_phys
)
line("Stage-I sign pattern difference with mapping alpha=beta=xi, gamma=-kappa4, delta=kappa4", match_stage1)
line("Corrected sign pattern difference with mapping alpha=beta=gamma=delta as xi,kappa4", match_corrected)
print()

L_fol_stage1_static = sp.simplify(L_fol_stage1.subs({Dt2: 0, E0: 0}))
line("Stage-I illustrative S_fol static density", L_fol_stage1_static)
print(
    "Stage-I S_fol static density matches expected with beta=xi, delta=kappa4:",
    sp.simplify(L_fol_stage1_static.subs({beta: xi, delta: kappa4}) - expected_static) == 0,
)
print()

print("Load-bearing conclusions:")
print("1. With (-,+,+,+), the covariant carrier action needs the overall minus sign to reduce to -N sqrt(h) (E2+E4) on a static slice.")
print("2. Using the Stage-I S_fol sign pattern, the off-static electric term matches the corrected covariant action only if gamma = -kappa4.")
print("3. If one wants gamma = +kappa4, the foliation action must use +gamma/(2N^2) h^{ij} F_{0i} F_{0j}, not the Stage-I minus sign.")
