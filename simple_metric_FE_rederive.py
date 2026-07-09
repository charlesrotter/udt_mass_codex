#!/usr/bin/env python3
"""
Re-derive bulk EL for phi ONLY on the simple metric:

  ds^2 = -e^{-2 phi} c^2 dt^2 + e^{2 phi} dr^2 + r^2 dOmega^2

No free D_A. No freeze-after-general.
"""
from __future__ import annotations

import sympy as sp

r, th, c, Z = sp.symbols("r theta c Z", positive=True)
phi = sp.Function("phi")
ph = phi(r)
phr = sp.diff(ph, r)

ok = fail = 0


def check(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  PASS  {name}" + (f"  {detail}" if detail else ""))
    else:
        fail += 1
        print(f"  FAIL  {name}" + (f"  {detail}" if detail else ""))


print("=== Simple metric phi-only rederive ===")

# Measure
g = sp.diag(
    -sp.exp(-2 * ph) * c**2,
    sp.exp(2 * ph),
    r**2,
    (r * sp.sin(th)) ** 2,
)
sqrtmg = c * r**2 * sp.sin(th)
check("det gives measure c r^2 sin(th)", sp.simplify((-g.det()) - sqrtmg**2) == 0)

# R1 kinetic density
gi = g.inv()
dens = sp.simplify(sqrtmg * sp.exp(2 * ph) * gi[1, 1] * phr**2)
check("R1 kinetic = sqrt(-g) (phi')^2", sp.simplify(dens - sqrtmg * phr**2) == 0)

# Kcal on D=r
Kcal = -2 * sp.exp(-2 * ph) / r**2
R2 = 2 / r**2
check("flat R2+Kcal at phi=0", sp.simplify((R2 + Kcal).subs(ph, 0)) == 0)
check("compensated R2+e^{2phi}Kcal=0", sp.simplify(R2 + sp.exp(2 * ph) * Kcal) == 0)

# Reduced L for phi (radial), vacuum
# L_comp = (Z/2) r^2 (phi')^2   [angular cancelled]
L_comp = (Z / 2) * r**2 * phr**2
EL_comp = sp.simplify(sp.diff(sp.diff(L_comp, phr), r) - sp.diff(L_comp, ph))
check("compensated EL = d/dr(Z r^2 phi')", sp.simplify(EL_comp - sp.diff(Z * r**2 * phr, r)) == 0)

# L_uncomp: (Z/2) r^2 (phi')^2 + r^2 * Kcal = (Z/2)r^2 phr^2 - 2 e^{-2phi}
# (because r^2 * (-2 e^{-2phi}/r^2) = -2 e^{-2phi})
L_un = (Z / 2) * r**2 * phr**2 - 2 * sp.exp(-2 * ph)
EL_un = sp.simplify(sp.diff(sp.diff(L_un, phr), r) - sp.diff(L_un, ph))
# d/dr(Z r^2 phi') - 4 e^{-2phi} = 0 for EL set to 0
# EL = d/dr(Z r^2 phi') - 4 e^{-2phi}
claim = sp.diff(Z * r**2 * phr, r) - 4 * sp.exp(-2 * ph)
check("uncompensated EL = d/dr(Z r^2 phi') - 4 e^{-2phi}", sp.simplify(EL_un - claim) == 0)

# Dilated dust L_m = -rho r^2 e^{-2phi}
rho = sp.symbols("rho", positive=True)
L_m = L_un - rho * r**2 * sp.exp(-2 * ph)
EL_m = sp.simplify(sp.diff(sp.diff(L_m, phr), r) - sp.diff(L_m, ph))
claim_m = sp.diff(Z * r**2 * phr, r) - 4 * sp.exp(-2 * ph) - 2 * rho * r**2 * sp.exp(-2 * ph)
check("uncomp+dilated dust EL", sp.simplify(EL_m - claim_m) == 0)

L_cm = L_comp - rho * r**2 * sp.exp(-2 * ph)
EL_cm = sp.simplify(sp.diff(sp.diff(L_cm, phr), r) - sp.diff(L_cm, ph))
claim_cm = sp.diff(Z * r**2 * phr, r) - 2 * rho * r**2 * sp.exp(-2 * ph)
check("comp+dilated dust EL", sp.simplify(EL_cm - claim_cm) == 0)

# Coulomb
q, pinf = sp.symbols("q phi_inf")
phi_c = pinf - q / r
check("Coulomb solves (r^2 phi')'=0", sp.simplify(sp.diff(r**2 * sp.diff(phi_c, r), r)) == 0)

print(f"\nRESULT: {ok} passed, {fail} failed")
if fail:
    raise SystemExit(1)
print(
    """
SIMPLE METRIC FE (phi only):
  W = e^{2phi}:  (r^2 phi')' = 0  ->  phi = phi_inf - q/r
  W = 1:         Z (r^2 phi')' = 4 e^{-2 phi}
  W = 1 + dilated dust: Z (r^2 phi')' = 4 e^{-2phi} + 2 rho r^2 e^{-2phi}
  W = e^{2phi} + dilated dust: Z (r^2 phi')' = 2 rho r^2 e^{-2phi}
"""
)
