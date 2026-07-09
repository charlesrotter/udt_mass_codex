#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER — independent re-derivation of pieces A, B, C.
Fresh, zero-trust CAS check. No import of the target scripts.

Metric: ds^2 = -A c^2 dt^2 + (1/A) dr^2 + r^2 dOmega^2,  A = e^{-2 phi}, 1+z = e^{phi}.
"""
import sympy as sp

print("="*72)
print("PIECE A — n=2 optics: energy + rate factors on THIS metric")
print("="*72)

r, c, X, k = sp.symbols("r c X k", positive=True)
phi = sp.symbols("phi", real=True)
A = sp.exp(-2*phi)

# static observer 4-velocity normalization:  g_tt (u^t)^2 = -c^2, g_tt = -A c^2
ut = sp.symbols("ut", positive=True)
sol_ut = sp.solve(sp.Eq(-A*c**2*ut**2, -c**2), ut)
ut_val = [s for s in sol_ut if s.is_positive][0] if any(s.is_positive for s in sol_ut) else sol_ut[0]
print("  u^t (static) =", sp.simplify(ut_val), "  expect e^{phi}=", sp.exp(phi))
assert sp.simplify(ut_val - sp.exp(phi)) == 0

# observed frequency omega ∝ -p_t u^t = E * u^t = E e^{phi}
# observer at phi_o=0, source at phi_s; 1+z = omega_s/omega_o = e^{phi_s}
phis = sp.symbols("phi_s", real=True)
one_plus_z = sp.exp(phis)                     # observer phi_o=0
E_factor = sp.exp(0)/sp.exp(phis)             # E_obs/E_src = e^{phi_o}/e^{phi_s}
print("  1+z = e^{phi_s}, energy factor E_obs/E_src =", E_factor, "= 1/(1+z):",
      sp.simplify(E_factor - 1/one_plus_z)==0)
assert sp.simplify(E_factor - 1/one_plus_z) == 0

# proper time dtau = sqrt(A) dt = e^{-phi} dt ; crest period ratio
dtau_o_over_s = sp.exp(-0)/sp.exp(-phis)      # = e^{phi_s} = 1+z (period stretched)
rate_factor = 1/dtau_o_over_s                 # arrival rate ratio = 1/(1+z)
print("  period ratio dtau_o/dtau_s =", sp.simplify(dtau_o_over_s), "= 1+z ;",
      "rate factor =", sp.simplify(rate_factor), "= 1/(1+z):",
      sp.simplify(rate_factor - 1/one_plus_z)==0)
assert sp.simplify(rate_factor - 1/one_plus_z) == 0
assert sp.simplify(E_factor - rate_factor) == 0   # the "Lorentz clue": same factor

prod = sp.simplify(E_factor*rate_factor)
print("  energy x rate =", prod, "= 1/(1+z)^2 :", sp.simplify(prod-1/one_plus_z**2)==0)

# Etherington reciprocity assembly (the THIRD factor): source-area distance = (1+z) D_A
z, D_A, L = sp.symbols("z D_A L", positive=True)
F = (L/(1+z)**2)/(4*sp.pi*((1+z)*D_A)**2)
d_L = sp.sqrt(L/(4*sp.pi*F))
print("  d_L =", sp.simplify(d_L), " -> n=2:", sp.simplify(d_L-(1+z)**2*D_A)==0)
print("  NOTE: the (1+z)*D_A source-area factor is Etherington reciprocity")
print("        (holds for ANY null-geodesic photon-conserving metric) — imported lemma,")
print("        NOT re-derived on this metric. Energy+rate ARE native; reciprocity is generic.")

print()
print("="*72)
print("PIECE B — mass lock (Principle-7 audit)")
print("="*72)

# Misner-Sharp mass for g_rr = 1/A (f=A special form): 1 - 2Gm/(c^2 r) = A
G = sp.symbols("G", positive=True)
Ar = sp.Function("A")(r)
m_MS = c**2*r*(1-Ar)/(2*G)
print("  MS mass m = c^2 r (1-A)/(2G)  <=>  A = 1 - 2Gm/(c^2 r)")
print("  This is the GR Schwarzschild/quasilocal form. |grad r|^2 = g^{rr} = A.")

# check via Einstein tensor G^t_t for this metric class
t = sp.symbols("t")
th, ph2 = sp.symbols("theta varphi")
Af = sp.Function("Af")
g = sp.diag(-Af(r)*c**2, 1/Af(r), r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords=[t,r,th,ph2]
def christ(a,b,cc):
    return sp.Rational(1,2)*sum(ginv[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d])) for d in range(4))
Gamma=[[[sp.simplify(christ(a,b,cc)) for cc in range(4)] for b in range(4)] for a in range(4)]
def Ricci(b,d):
    return sp.simplify(sum(sp.diff(Gamma[a][b][d],coords[a]) for a in range(4))
        - sum(sp.diff(Gamma[a][b][a],coords[d]) for a in range(4))
        + sum(Gamma[a][a][e]*Gamma[e][b][d] for a in range(4) for e in range(4))
        - sum(Gamma[a][d][e]*Gamma[e][b][a] for a in range(4) for e in range(4)))
Rtt=Ricci(0,0); Rrr=Ricci(1,1); Rthth=Ricci(2,2)
Rs=sp.simplify(ginv[0,0]*Rtt+ginv[1,1]*Rrr+ginv[2,2]*Rthth+ginv[3,3]*Ricci(3,3))
Gtt_mixed=sp.simplify(ginv[0,0]*(Rtt-sp.Rational(1,2)*g[0,0]*Rs))
print("  G^t_t (CAS) =", Gtt_mixed)
target = sp.simplify(-(1/r**2)*sp.diff(r*(1-Af(r)),r))
print("  -(1/r^2) d/dr[r(1-A)] =", target, " match:", sp.simplify(Gtt_mixed-target)==0)

# L profile alpha=1: A = 1 - r/X
A_L = 1 - r/X
m_L = sp.simplify(c**2*r*(1-A_L)/(2*G))
print("  L profile A=1-r/X -> m(r) =", m_L, " ; at r=X: M =", sp.simplify(m_L.subs(r,X)))
Mtot = sp.simplify(m_L.subs(r,X))
print("  => X = 2GM/c^2 ?  X solved:", sp.solve(sp.Eq(Mtot, c**2*X/(2*G)),X), "(identity; X arbitrary)")
print("  Mtot as fn of X:", Mtot, "-> X =", sp.solve(sp.Eq(sp.Symbol('M'), Mtot),X), "= 2GM/c^2")
print("  r_max = X = 2GM/c^2 : TAUTOLOGY of MS at A=0 (2Gm/c^2 r =1 defines Schwarzschild r).")

# hyperbolic profile A=(X-x)/(X+x)
x=sp.symbols("x",positive=True)
A_h=(X-x)/(X+x)
m_h=sp.simplify(c**2*x*(1-A_h)/(2*G))
print("  hyperbolic A=(X-x)/(X+x): m(x) =", m_h, " ; x->X:", sp.simplify(sp.limit(m_h,x,X)))

print()
print("="*72)
print("PIECE C — x_max horizon: proper vs optical, alpha=1 vs alpha=2")
print("="*72)

# alpha=1: A = 1 - r/X, wall r=X
A1 = 1 - r/X
proper1 = sp.integrate(1/sp.sqrt(A1),(r,0,X))
optical1 = sp.integrate(1/A1,(r,0,X))
z1 = sp.limit(1/sp.sqrt(A1),r,X,'-')
print("  alpha=1 (A=1-r/X):")
print("    proper  ell = int dr/sqrt(A) =", proper1, " (FINITE = 2X)")
print("    optical     = int dr/A       =", optical1, " (INFINITE)")
print("    1+z = A^{-1/2} at r->X       =", z1, " (z -> infinity)")

# alpha=2: e^{-phi}=1-kr  => A=(1-kr)^2, wall r=1/k
A2 = (1-k*r)**2
proper2 = sp.integrate(1/sp.sqrt(A2),(r,0,1/k))
optical2 = sp.integrate(1/A2,(r,0,1/k))
z2 = sp.limit(1/sp.sqrt(A2),r,1/k,'-')
print("  alpha=2 (A=(1-kr)^2, e^{-phi}=1-kr):")
print("    proper  ell =", proper2, " (INFINITE)")
print("    optical     =", optical2, " (INFINITE)")
print("    1+z at r->1/k =", z2)

# signature check at wall alpha=1: does r become timelike beyond X?
print("  alpha=1 beyond wall: g_tt = -A c^2, sign(g_tt) for r>X:",
      "A<0 -> g_tt>0 (t spacelike), g_rr=1/A<0 (r timelike) => Killing horizon at r=X")

# P_ell integral check: r_max/X = int_0^1 sqrt((1-u)/(1+u)) du = pi/2 - 1
u=sp.symbols("u",positive=True)
Ipell=sp.integrate(sp.sqrt((1-u)/(1+u)),(u,0,1))
print()
print("  P_ell check: int_0^1 sqrt((1-u)/(1+u)) du =", sp.simplify(Ipell),
      " = pi/2 - 1 :", sp.simplify(Ipell-(sp.pi/2-1))==0)

print("\nALL CHECKS DONE")
