#!/usr/bin/env python3
"""Exact symbolic checks for UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md.

This script verifies algebra only.  It does not choose an action, variation class,
boundary ontology, or physical mass normalization.
"""

import sympy as sp


checks = []


def check(name, condition):
    ok = bool(condition)
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


# ---------------------------------------------------------------------------
# A. Boundary-object identity
A_fold = sp.exp(0)
eps = sp.symbols("epsilon", positive=True)
A_wall = eps
check("A1 odd fold has A=1", A_fold == 1)
check("A2 WR-L wall has A->0", sp.limit(A_wall, eps, 0, dir="+") == 0)


# ---------------------------------------------------------------------------
# B. Does the recorded round action descend under the odd depth mirror?
phi, phip, rho, rhop = sp.symbols("phi phip rho rhop", real=True)
Z, mu = sp.symbols("Z mu", real=True)

# Per-4pi first-order geometric representatives.  The general kinetic family is
# (Z/2) rho^2 phi'^2 + 2 mu rho rho' phi'.
L_P = Z * rho**2 * phip**2 / 2 + 2 - 2 * sp.exp(-2 * phi) * rhop**2 + 2 * mu * rho * rhop * phip
L_G = Z * rho**2 * phip**2 / 2 + 2 - 2 * rhop**2 + 2 * mu * rho * rhop * phip

# Odd depth mirror at the fixed surface:
# phi -> -phi, phi' -> +phi', rho -> rho, rho' -> -rho'.
mirror = {phi: -phi, phip: phip, rho: rho, rhop: -rhop}
dP = sp.simplify(L_P.xreplace(mirror) - L_P)
dG = sp.simplify(L_G.xreplace(mirror) - L_G)

check(
    "B1 Branch-P mirror defect",
    sp.simplify(
        (dP + 4 * sp.sinh(2 * phi) * rhop**2 + 4 * mu * rho * rhop * phip).rewrite(sp.exp)
    )
    == 0,
)
check(
    "B2 Branch-P does not descend for generic fields",
    sp.simplify(dP.subs({phi: 1, rhop: 1, phip: 0})) != 0,
)
check("B3 Branch-G mirror defect", sp.simplify(dG + 4 * mu * rho * rhop * phip) == 0)
check("B4 Branch-G descends on the mu=0 slice", sp.simplify(dG.subs(mu, 0)) == 0)
check(
    "B5 both defects vanish only at the pinned fold data phi=0,rho'=0",
    sp.simplify(dP.subs({phi: 0, rhop: 0})) == 0
    and sp.simplify(dG.subs({phi: 0, rhop: 0})) == 0,
)


# ---------------------------------------------------------------------------
# C. One-sided boundary variation versus a two-sided jump
p_phi_P = sp.diff(L_P, phip)
p_rho_P = sp.diff(L_P, rhop)
check("C1 canonical momenta", p_phi_P == Z * rho**2 * phip + 2 * mu * rho * rhop)
check(
    "C2 transverse momentum",
    sp.simplify(p_rho_P - (-4 * sp.exp(-2 * phi) * rhop + 2 * mu * rho * phip)) == 0,
)

p_phi_fold = sp.simplify(p_phi_P.subs({phi: 0, rhop: 0}))
p_rho_fold = sp.simplify(p_rho_P.subs({phi: 0, rhop: 0}))
check("C3 fold momenta", p_phi_fold == Z * rho**2 * phip and p_rho_fold == 2 * mu * rho * phip)

# On one copy, odd phi means delta phi=0 while even rho leaves delta rho free.
# With B=0, nonzero flux therefore requires mu=0.  This is variation-class
# dependent, not a universal selection, because a boundary functional may alter it.
check(
    "C4 one-copy B=0 natural rho condition couples mu to the free flux",
    sp.factor(p_rho_fold) == 2 * mu * rho * phip,
)

# On a matched mirror partner the mixing term cancels from the rho-momentum jump.
p_rho_mirror = p_rho_P.xreplace(mirror)
p_phi_mirror = p_phi_P.xreplace(mirror)
jump_rho = sp.simplify(p_rho_mirror - p_rho_P)
jump_phi = sp.simplify(p_phi_mirror - p_phi_P)
check(
    "C5 two-side rho-momentum jump is mu-independent",
    sp.simplify(jump_rho - 8 * sp.cosh(2 * phi) * rhop) == 0,
)
check("C6 two-side phi-momentum jump", sp.simplify(jump_phi + 4 * mu * rho * rhop) == 0)


# ---------------------------------------------------------------------------
# D. Total-derivative and moving-endpoint ambiguities
r = sp.symbols("r", real=True)
alpha, gamma = sp.symbols("alpha gamma", real=True)
q = sp.Function("q")(r)
L0 = sp.Function("L0")(q, sp.diff(q, r), r)

# Use the exact Euler operator on explicit representatives, avoiding assumptions
# about the opaque L0 function.
L_rep = sp.diff(q, r) ** 2 / 2 + q**2 / 2
L_alpha = L_rep + alpha * sp.diff(q, r)  # d(alpha q)/dr


def EL(L, field):
    return sp.simplify(sp.diff(L, field) - sp.diff(sp.diff(L, sp.diff(field, r)), r))


check("D1 d(alpha q)/dr leaves the bulk Euler equation unchanged", EL(L_alpha, q) == EL(L_rep, q))
check(
    "D2 d(alpha q)/dr shifts boundary momentum",
    sp.simplify(sp.diff(L_alpha, sp.diff(q, r)) - sp.diff(L_rep, sp.diff(q, r))) == alpha,
)

H_rep = sp.simplify(sp.diff(q, r) * sp.diff(L_rep, sp.diff(q, r)) - L_rep)
L_gamma = L_rep + gamma  # d(gamma r)/dr
H_gamma = sp.simplify(sp.diff(q, r) * sp.diff(L_gamma, sp.diff(q, r)) - L_gamma)
check("D3 d(gamma r)/dr leaves the bulk Euler equation unchanged", EL(L_gamma, q) == EL(L_rep, q))
check("D4 d(gamma r)/dr shifts the endpoint Hamiltonian", sp.simplify(H_gamma - H_rep) == -gamma)


# ---------------------------------------------------------------------------
# E. WR-L profile versus the live shift-clean radial action
X = sp.symbols("X", positive=True)
rpos = sp.symbols("r", positive=True)
A = 1 - rpos / X
phi_WR = -sp.log(A) / 2
phip_WR = sp.simplify(sp.diff(phi_WR, rpos))
residual_R1 = sp.simplify(sp.diff(rpos**2 * phip_WR, rpos))
check("E1 WR-L derivative", sp.simplify(phip_WR - 1 / (2 * (X - rpos))) == 0)
check(
    "E2 WR-L is not an R1-vacuum extremal",
    sp.simplify(residual_R1 - rpos * (2 * X - rpos) / (2 * (X - rpos) ** 2)) == 0,
)

Zp = sp.symbols("Z", positive=True)
Lkin_WR = sp.simplify(Zp * rpos**2 * phip_WR**2 / 2)
pmom_WR = sp.simplify(Zp * rpos**2 * phip_WR)
check(
    "E3 shift-clean action density has 1/epsilon^2 wall divergence",
    sp.limit(eps**2 * Lkin_WR.subs(rpos, X - eps), eps, 0, dir="+") == Zp * X**2 / 8,
)
check(
    "E4 shift-clean momentum has 1/epsilon wall divergence",
    sp.limit(eps * pmom_WR.subs(rpos, X - eps), eps, 0, dir="+") == Zp * X**2 / 2,
)

# Narrow inverse-variational diagnostic: within L=(Z/2)r^2 W(phi)phi'^2 only,
# demanding WR-L as an exact extremal gives W proportional to A^2/(1-A)^4.
W_WR = sp.simplify(A**2 / (1 - A) ** 4)
L_weighted = sp.simplify(Zp * rpos**2 * W_WR * phip_WR**2 / 2)

# Euler equation after substituting the profile and W(phi(r)).  For a kinetic
# weight W(phi), EL=0 is d(r^2 W phi')/dr - (r^2/2) W_phi phi'^2=0, with
# W_phi = (dW/dr)/phi'.
W_phi_on_profile = sp.simplify(sp.diff(W_WR, rpos) / phip_WR)
weighted_EL = sp.simplify(
    sp.diff(rpos**2 * W_WR * phip_WR, rpos)
    - rpos**2 * W_phi_on_profile * phip_WR**2 / 2
)
check("E5 inverse pure-kinetic weight makes WR-L an exact extremal", weighted_EL == 0)
check("E6 that exact weight produces a center-divergent density", L_weighted == Zp * X**2 / (8 * rpos**2))


if not all(ok for _, ok in checks):
    raise SystemExit("SYMBOLIC CHECK FAILURE")
print(f"ALL SYMBOLIC CHECKS PASS ({len(checks)}/{len(checks)})")
