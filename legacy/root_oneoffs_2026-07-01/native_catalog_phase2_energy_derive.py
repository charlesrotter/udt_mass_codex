#!/usr/bin/env python3
"""
native_catalog_phase2_energy_derive.py -- PHASE 2 setup (v2): EXACT L2+L4 energy
DENSITY for the GENUINE UNIT-S^2 degree-k field with G=G(r,theta) a general 2-D
function (azimuthal winding k).  2026-06-18.  Claude (Opus 4.8, 1M).  DATA-BLIND.
Category-A.  OBSERVE.

Field (genuine |n|=1, target S^2, pi_2 degree = k):
  n = ( sin G cos(k psi), sin G sin(k psi), cos G ),  G = G(r,theta).
The pi_2 area-form degree = k * (winding of G over theta:0..pi).  The RADIAL and
POLAR profile G(r,theta) is FREE (no Theta(core)=m*pi BC). Vacuum at the seal is
G->0 or G->pi (north/south pole, texture retracted).

We derive the static proper-energy density E_dens = (-L2 - L4) * sqrt(g3)/(sin th)
(the per-(r,theta) integrand after the trivial psi integral gives 2pi), as a
function of G, G_r, G_th, k, r, phi(r).  This is the integrand the 2-D solver
minimizes (phase2_solve.py imports these closed forms).

Metric ds^2=-e^{-2phi}dt^2+e^{2phi}dr^2+r^2 dOmega^2;  sqrt(g3)=e^{phi} r^2 sin th.
Native action L2=-(xi/2)g.dn.dn, L4=-(kap/4)(Lagrange-identity Skyrme).
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap = sp.symbols('xi kappa', positive=True)
k = sp.symbols('k', positive=True)
phi = sp.Symbol('phi', real=True)          # local value (background, treat as const here)
G = sp.Function('G')(r, th)
Gr = sp.diff(G, r); Gt = sp.diff(G, th)

n = sp.Matrix([sp.sin(G)*sp.cos(k*ps),
               sp.sin(G)*sp.sin(k*ps),
               sp.cos(G)])
coords = [t, r, th, ps]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()

def dot(a, b): return (a.T*b)[0]
dn = [sp.Matrix([sp.diff(n[i], c) for i in range(3)]) for c in coords]
gg = [[dot(dn[m], dn[l]) for l in range(4)] for m in range(4)]
L2 = -(xi/2)*sum(gi[m, m]*gg[m][m] for m in range(4))
L4 = -(kap/4)*sum(gi[m, m]*gi[l, l]*(gg[m][m]*gg[l][l]-gg[m][l]*gg[l][m])
                  for m in range(4) for l in range(4))
dens2 = sp.simplify(-L2)
dens4 = sp.simplify(-L4)

# substitute symbols for G, Gr, Gt to expose the closed form
Gs, Grs, Gts = sp.symbols('G Gr Gt', real=True)
sub = {sp.diff(G, r): Grs, sp.diff(G, th): Gts, G: Gs}
d2 = sp.simplify(dens2.subs(sub))
d4 = sp.simplify(dens4.subs(sub))
# proper-energy integrand over (r,theta) after psi-integral (factor 2pi):
meas = sp.exp(phi)*r**2*sp.sin(th)
I2 = sp.simplify(d2*meas)
I4 = sp.simplify(d4*meas)

print("="*74)
print("PHASE 2 setup v2: L2+L4 density for genuine unit-S^2 degree-k field")
print("="*74)
print("\n|n|^2 =", sp.simplify(dot(n, n)))
print("\n-L2 density (in G,Gr,Gt,k,r,phi):\n  ", d2)
print("\n-L4 density:\n  ", d4)
print("\nProper (r,theta) energy integrand I2 = -L2 * e^{phi} r^2 sin th:\n  ", sp.expand(I2))
print("\nProper (r,theta) energy integrand I4 = -L4 * e^{phi} r^2 sin th:\n  ", sp.expand(I4))

# Derrick check on the SEPARABLE harmonic profile G=G(theta) only (pure angular,
# Gr=0): does the k-dependence preserve a sized soliton, and how does energy scale
# with k? Pure-angular (texture filling the cell radially) energy per unit ln r:
print("\n--- pure-angular slice (Gr=0): k-scaling of the densities ---")
print("  I2(Gr=0) =", sp.simplify(I2.subs(Grs, 0)))
print("  I4(Gr=0) =", sp.simplify(I4.subs(Grs, 0)))
print("\nDONE_PHASE2_DERIVE_V2")
