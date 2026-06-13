#!/usr/bin/env python3
"""Drill the gap-edge derivation carefully. The fold and gap MUST be
posed on the SAME operator and SAME domain for the ratio to be a
'same SL operator' statement. Resolve the a^2 vs a^3 discrepancy."""
import sympy as sp
a, au, u, kap, T0, m, t = sp.symbols('a a_u u kappa T0 m t', positive=True)

# Both fold and gap come from the SAME static EL:
#   (p v')' = (b/(8k))[(1-2k/f) e^-2v - beta e^v]   (prime = d/dt)
# p = a, b = b0 = (1-u^2)au^2/a  (C=0 member, gamma->1 truncation).
# DOMAIN in t: [0, T0] (Dirichlet v=0 both ends).
b0 = (1-u**2)*au**2/a
p = a

# ---- FOLD (OFF, beta=0): nonlinear (p v')' = (b0/8k) e^-2v ----
# Convert to m-chart, dm = dt/p, p=a const => m = t/a, domain m in [0, T0/a].
# v_mm = (p b0/8k) e^-2v = Phi e^-2v, Phi = a*b0/(8k) = (1-u^2)au^2/(8k).
# M_fold = T0/a.  Fold at s* with sqrt(Phi) M/2 = s* sech s*.
# Phi M^2/4 = (s* sech s*)^2 = G*/8.
# Phi = G*/(2 M^2):  (1-u^2)au^2/(8 ks) = G*/(2 (T0/a)^2)
#   => ks = (1-u^2)au^2 (T0/a)^2/(8) * 2/G* = (1-u^2)au^2 T0^2/(4 G* a^2 * ... )
Gs = sp.Symbol('Gstar', positive=True)
Phi = (1-u**2)*au**2/(8*kap)
M_f = T0/a
ks = sp.solve(sp.Eq(Phi, Gs/(2*M_f**2)), kap)[0]
print("fold ks =", sp.simplify(ks))   # expect (1-u^2)au^2 T0^2/(4 G* a^2)

# ---- GAP (ON, linearize about v=0): ----
# linearized source: d/dv[(b0/8k)((1-2k/f)e^-2v - e^v)]|_0, gamma->1:
#   (b0/8k) d/dv[e^-2v - e^v]|_0 = (b0/8k)(-2-1) = -3 b0/(8k).
# So EL linearized: (p psi')' = -3 b0/(8k) psi  (prime=d/dt), Dirichlet[0,T0].
# This is a t-chart SL problem: -(p psi_t)_t = (3 b0/(8k)) psi.
# p=a const: -a psi_tt = (3 b0/8k) psi.  Lowest Dirichlet on [0,T0]:
#   psi=sin(pi t/T0), eigenvalue a (pi/T0)^2 = 3 b0/(8 kc).
#   => kc = 3 b0 T0^2/(8 pi^2 a).   [t-chart, NO m-conversion needed!]
kc_tchart = sp.simplify(3*b0*T0**2/(8*sp.pi**2*a))
print("gap kc (t-chart) =", kc_tchart)
# = 3(1-u^2)au^2 T0^2/(8 pi^2 a^2)   -- matches COMMITTED script.

# Now do it in m-chart to be consistent with the fold:
# -(p psi_t)_t = lam psi  with p=a; in m-chart (p v_t)_t = (1/p)v_mm:
#  -(1/p) psi_mm = (3b0/8k) psi  => -psi_mm = p (3b0/8k) psi = a(3b0/8k)psi.
# Domain m in [0, M_f=T0/a]. Lowest eig: (pi/M_f)^2 = a 3b0/(8 kc).
#  (pi a/T0)^2 = 3 a b0/(8 kc) => kc = 3 a b0 T0^2/(8 pi^2 a^2) = 3 b0 T0^2/(8 pi^2 a)
kc_mchart = sp.solve(sp.Eq((sp.pi/M_f)**2, a*3*b0/(8*kap)), kap)[0]
print("gap kc (m-chart) =", sp.simplify(kc_mchart))
print("t-chart == m-chart:", sp.simplify(kc_tchart - kc_mchart)==0)

# RATIO:
ratio = sp.simplify(ks/kc_tchart)
print("\nratio ks/kc =", ratio)
print("target 2 pi^2/(3 G*) =", sp.simplify(2*sp.pi**2/(3*Gs)))
print("MATCH:", sp.simplify(ratio - 2*sp.pi**2/(3*Gs))==0)
print("free symbols of ratio:", sp.simplify(ratio).free_symbols)
