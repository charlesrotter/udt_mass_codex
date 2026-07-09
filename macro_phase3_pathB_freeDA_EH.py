#!/usr/bin/env python3
"""
PATH B vacuum: free D_A + EH bulk + R1 kinetic (no matter stand-in).
Phase 2 showed EH has bulk when D_A is varied. This writes the combined vacuum EL.
"""
from __future__ import annotations

import sympy as sp

r, th, c = sp.symbols("r theta c", positive=True)
Z = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
DA = sp.Function("D_A")
ph = phi(r)
D = DA(r)
php = sp.diff(ph, r)
phpp = sp.diff(ph, r, 2)
Dp = sp.diff(D, r)
Dpp = sp.diff(D, r, 2)

# R from Phase 2
R = (
    2
    * sp.exp(-2 * ph)
    / D**2
    * (
        -2 * D**2 * php**2
        + D**2 * phpp
        + 4 * D * Dp * php
        - 2 * D * Dpp
        + sp.exp(2 * ph)
        - Dp**2
    )
)
# Radial density ~ D^2 R  (drop overall constants c, 4π)
L_eh = sp.simplify(D**2 * R)
L_kin = (Z / 2) * D**2 * php**2
L = sp.simplify(L_eh + L_kin)


def el(L, f):
    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)
    return sp.simplify(
        sp.diff(L, f) - sp.diff(sp.diff(L, fp), r) + sp.diff(sp.diff(L, fpp), r, 2)
    )


print("=" * 70)
print("PATH B vacuum: L = D_A^2 R + (Z/2) D_A^2 (φ')^2")
print("=" * 70)
print("\nL =", L)

el_phi = el(L, ph)
el_D = el(L, D)
print("\nEL_φ =", el_phi)
print("EL_D =", el_D)

# Factor for readability
print("\nEL_φ simplified factors:", sp.factor(el_phi))
print("EL_D simplified factors:", sp.factor(el_D))

# Constant-φ slice
print("\n[const φ] set φ'=φ''=0:")
print("  EL_φ:", sp.simplify(el_phi.subs({php: 0, phpp: 0})))
print("  EL_D:", sp.simplify(el_D.subs({php: 0, phpp: 0})))

# D_A = r slice (should relate to Path A: EH total deriv + kinetic)
el_phi_r = sp.simplify(el_phi.subs(D, r).doit())
el_D_r = sp.simplify(el_D.subs(D, r).doit())
print("\n[on D_A=r]")
print("  EL_φ =", el_phi_r)
print("  EL_D =", el_D_r)
print("  EL_φ == d/dr(Z r^2 φ')? (Path A kinetic only)", 
      sp.simplify(el_phi_r - sp.diff(Z * r**2 * php, r)) == 0)

# Try power-law / Coulomb-like ansatz D=r, phi = phi0 - q/r already known for Path A
# For free D: try D = a*r, phi = const
print("\n[ansatz D=a r, φ=const]")
a = sp.symbols("a", positive=True)
subs = {
    D: a * r,
    Dp: a,
    Dpp: 0,
    php: 0,
    phpp: 0,
    ph: 0,  # gauge
}
# Need to substitute function properly
el_phi_ar = sp.simplify(el_phi.subs(ph, 0).subs(php, 0).subs(phpp, 0).subs(D, a*r).doit())
# Better: replace derivatives after assuming forms
phi0, q = sp.symbols("phi0 q")
# Numerical structure: EL_D at φ=0, D=a r
elD_test = el_D.subs({
    sp.diff(ph, r): 0,
    sp.diff(ph, r, 2): 0,
    ph: 0,
}).doit()
elD_test = sp.simplify(elD_test.subs(D, a*r).doit())
print("  EL_D (φ=0,D=ar) =", elD_test)

print("\nDONE Path B EL write")
