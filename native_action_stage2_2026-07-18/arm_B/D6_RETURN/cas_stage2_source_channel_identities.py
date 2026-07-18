#!/usr/bin/env python3
"""Stage-II source-channel audit for unrestricted metric vs reciprocal tangent variation.

This script checks only the finite algebra behind the two source combinations:
1. rho + S = 2 rho_4 under the conditional unrestricted metric / minimal carrier branch.
2. rho + p_parallel = 2 (rho_{2,parallel} + rho_{4,parallel}) for reciprocal tangent variation.

It does not certify the action branch that makes either source physically native.
"""

import sympy as sp


xi, kappa4 = sp.symbols("xi kappa4", real=True)
a, b, c = sp.symbols("a b c", nonnegative=True)          # |D_parallel n|^2, |D_perp1 n|^2, |D_perp2 n|^2
f12, f13, f23 = sp.symbols("f12 f13 f23", real=True)     # independent antisymmetric spatial F components

X = a + b + c
Y = 2 * (f12**2 + f13**2 + f23**2)  # ordered-index convention

rho2 = xi * X / 2
rho4 = kappa4 * Y / 4

S2_trace = -rho2
S4_trace = rho4

rho_plus_S = sp.simplify((rho2 + rho4) + (S2_trace + S4_trace))

p2_parallel = xi * (a - X / 2)
p4_parallel = kappa4 * ((f12**2 + f13**2) - Y / 4)

rho2_parallel = xi * a / 2
rho4_parallel = kappa4 * (f12**2 + f13**2) / 2
rho_plus_p_parallel = sp.simplify((rho2 + rho4) + (p2_parallel + p4_parallel))
rhs_parallel = sp.simplify(2 * (rho2_parallel + rho4_parallel))

print("Ordered-index convention: Y = F_ij F_ij = 2 (f12^2 + f13^2 + f23^2)")
print("rho + S =", rho_plus_S)
print("2 rho_4  =", sp.simplify(2 * rho4))
print("Identity 1 holds:", sp.simplify(rho_plus_S - 2 * rho4) == 0)
print()
print("rho + p_parallel =", rho_plus_p_parallel)
print("2 (rho2_parallel + rho4_parallel) =", rhs_parallel)
print("Identity 2 holds:", sp.simplify(rho_plus_p_parallel - rhs_parallel) == 0)
print()
print("Difference between the two source channels:")
print(sp.simplify(rho_plus_p_parallel - 2 * rho4))
print()
print("Load-bearing conclusion:")
print("Without an extra theorem equating directional and traced channels, reciprocal tangent variation and unrestricted lapse variation are algebraically distinct.")
