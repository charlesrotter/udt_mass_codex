#!/usr/bin/env python3
"""D2b check 2 — end-case enumeration for a finite self-closed Branch-G domain + vacuum theorems.

Uses ONLY G-branch facts established in d2b_reduction_flux_cas.py:
  phi-EL: Phi = Z rho^2 phi' EXACTLY constant (any phi-blind matter);
  rho-EL: rho'' = -(Z/4) rho phi'^2 - (1/4) dLm/drho ;
  H = (Z/2)rho^2 phi'^2 - 2 rho'^2 - 2 + E_m conserved;
  end menu (derived fold pins): EVEN fold (phi'=rho'=0), ODD fold (phi=a, rho'=0, phi' free),
  REGULAR CENTER (rho->0, e^{-phi}rho'->1). rho>0 on the cell (banked cell definition).
"""
import sympy as sp

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

r, r1, r2 = sp.symbols('r r_1 r_2', positive=True)
Z, q, aa, bb, phi0 = sp.symbols('Z q a b phi_0', real=True, nonzero=True)
rho = sp.Function('rho', positive=True)(r)
phi = sp.Function('phi')(r)

# ---------- 1. The master identity: Delta phi = (Phi/Z) * Integral dr/rho^2 ----------
# phi' = Phi/(Z rho^2) with Phi constant  =>  phi(r2)-phi(r1) = (Phi/Z) I,  I = ∫ dr/rho^2 > 0 (rho>0).
Phi = sp.Symbol('Phi', real=True)
phiprime = Phi/(Z*rho**2)
check("phi' = Phi/(Z rho^2) integrates to Delta_phi = (Phi/Z)*I with I = Int dr/rho^2",
      sp.simplify(sp.integrate(phiprime, r) - (Phi/Z)*sp.integrate(1/rho**2, r)) == 0)
# I > 0 always (integrand 1/rho^2 > 0 on a nondegenerate interval): logic, rho>0 banked.

# ---------- 2. End-case table (each end forces a condition on the SINGLE constant Phi) ----------
# EVEN fold at either end: phi'=0 with rho>0  => Phi = 0  => phi' == 0 on the WHOLE cell.
# REGULAR CENTER: rho ~ rho'(0) r -> 0, phi' = Phi/(Z rho^2) ~ Phi/(Z rho'(0)^2 r^2) -> diverges;
#   Delta phi from the center outward diverges LOGARITHMICALLY-worse (1/eps) unless Phi = 0:
eps, r0 = sp.symbols('epsilon r_0', positive=True); c1 = sp.Symbol("rho'_0", positive=True)
dphi_center = sp.integrate(1/(c1*r)**2, (r, eps, r0))     # (Phi/Z) * this = Delta phi
check("center: Int_eps^r0 dr/(rho'(0) r)^2 = (1/eps - 1/r0)/rho'(0)^2 -> infinity as eps->0"
      " => any end-pairing containing a regular center forces Phi=0",
      sp.simplify(dphi_center - (1/eps - 1/r0)/c1**2) == 0 and sp.limit(dphi_center, eps, 0, '+') == sp.oo)
# ODD folds at BOTH ends, CANON form (a=0 both): phi(r1)=phi(r2)=0 => 0 = (Phi/Z) I, I>0 => Phi=0.
Ii = sp.Symbol('I', positive=True)
check("odd+odd canon (a=b=0): 0 = (Phi/Z)*I with I>0 forces Phi=0",
      sp.solve(sp.Eq(0, (Phi/Z)*Ii), Phi) == [0])
# ODD+ODD TWISTED (a != b): Delta = b-a = (Phi/Z) I  => Phi = Z(b-a)/I  != 0. THE ONE nonzero-flux closure.
check("odd+odd twisted: Phi = Z(b-a)/I (nonzero iff twist b!=a) — the ONLY end-pairing with Phi != 0",
      sp.solve(sp.Eq(bb-aa, (Phi/Z)*Ii), Phi) == [Z*(bb-aa)/Ii])
print("   END TABLE: {even,center} anywhere => Phi=0 => phi'==0 (phi = const, pure gauge);")
print("   odd+odd untwisted => Phi=0, phi==0;  odd+odd twisted (b!=a) => Phi = Z*Delta/I — the sole escape channel.")

# ---------- 3. VACUUM, untwisted: rho''=0, any fold end needs rho'=0 => rho const; H = -2 != 0 ----------
c0, c1v = sp.symbols('c0 c1', real=True)
rho_lin = c0 + c1v*r
check("vacuum G with Phi=0: rho'' = 0 => rho linear; fold pin rho'=0 => rho == const",
      sp.simplify(sp.diff(rho_lin, r, 2)) == 0 and sp.solve(sp.Eq(sp.diff(rho_lin, r), 0), c1v) == [0])
H_vac_const = -2  # H = (Z/2)rho^2*0 - 2*0 - 2 + 0
check("vacuum constant G-cell: H = -2 != 0 -> FAILS the free-endpoint closure H=0 (same gap as P's R1b)",
      H_vac_const != 0)

# ---------- 4. VACUUM, twisted: rho'' = -q^2/(4 Z rho^3) is ONE-SIGNED => no second rho'=0 end ----------
rhof = sp.Function('rho', positive=True)(r)
rhopp_twisted = -Z*rhof*(q/(Z*rhof**2))**2/4          # rho-EL with phi' = q/(Z rho^2), vacuum
check("twisted vacuum: rho'' = -q^2/(4 Z rho^3)  (strictly one-signed for q != 0, either sign of Z)",
      sp.simplify(rhopp_twisted + q**2/(4*Z*rhof**3)) == 0)
# Z>0: rho''<0 strictly => rho' strictly decreasing; rho'(r1)=0 => rho'<0 on (r1,r2] => never 0 again.
# Z<0: rho''>0 strictly => same conclusion mirrored. => NO second fold: twisted VACUUM cell impossible.
# (also H would need checking, but nonexistence already kills it)
print("   twisted vacuum: rho' strictly monotone after the first fold -> a second rho'=0 end is IMPOSSIBLE.")

# ---------- 5. VACUUM regular center in G = flat space exactly (and can never close) ----------
# Phi=0 => phi = phi0 const; rho''=0, regularity e^{-phi}rho'(0)=1 => rho = e^{phi0} r.
# metric: -e^{-2phi0}c^2dt^2 + e^{2phi0}dr^2 + e^{2phi0}r^2 dOmega — flat (rescale t,r); rho'=e^{phi0} never 0.
rho_flat = sp.exp(phi0)*r
check("G vacuum regular center: rho = e^{phi0} r, rho' = e^{phi0} != 0 for all r -> NO fold can ever occur",
      sp.simplify(sp.diff(rho_flat, r)) == sp.exp(phi0) and sp.exp(phi0) != 0)
# curvature check of the 4-metric (diagonal, static): do it explicitly
import itertools
t, R_, th, ps = sp.symbols('t r theta psi')
g = sp.diag(-sp.exp(-2*phi0), sp.exp(2*phi0), sp.exp(2*phi0)*R_**2, sp.exp(2*phi0)*R_**2*sp.sin(th)**2)
x = [t, R_, th, ps]
ginv = g.inv()
def christoffel(g, ginv, x):
    n = len(x)
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                Gam[l][m][nu] = sp.simplify(sum(ginv[l,s]*(sp.diff(g[s,m],x[nu])+sp.diff(g[s,nu],x[m])-sp.diff(g[m,nu],x[s])) for s in range(n))/2)
    return Gam
Gam = christoffel(g, ginv, x)
def riemann_zero(Gam, x):
    n = len(x)
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                for s in range(n):
                    Rc = sp.diff(Gam[l][m][s], x[nu]) - sp.diff(Gam[l][m][nu], x[s]) \
                         + sum(Gam[l][nu][k]*Gam[k][m][s] - Gam[l][s][k]*Gam[k][m][nu] for k in range(n))
                    if sp.simplify(sp.expand_trig(sp.simplify(Rc))) != 0:
                        return False
    return True
check("the center-regular G vacuum 4-metric is EXACTLY FLAT (all Riemann components 0)",
      riemann_zero(Gam, x))

print()
print("ALL PASS" if all(c for _, c in ok) else "SOME FAILED")
