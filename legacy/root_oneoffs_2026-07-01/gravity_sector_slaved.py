#!/usr/bin/env python3
"""
gravity_sector_slaved.py

THE phi-SLAVED-TO-METRIC variation, done correctly.

Key subtlety: in UDT phi is the metric's own field (g_tt=-e^{-2phi}c0^2,
g_rr=e^{2phi}). When we vary the FULL action w.r.t. the metric, we must NOT
also independently impose a separate phi-equation. BUT the covariant metric
field equation  f G_mn + (g Box - nabla nabla) f = (1/2)T_mn  is derived by
varying g^{mn} FREELY (all 10 components), treating f(phi) as a fixed scalar
field. If phi is slaved to g, then varying g ALSO varies f, and the proper EOM
is obtained by the CHAIN RULE -- equivalently by reducing the action to the
single DOF phi(r) and varying THAT (minisuperspace), BUT keeping the lapse
free so the Hamiltonian constraint is not lost.

The clean, unambiguous resolution: a single covariant action S=int sqrt(-g) f(phi) R
with phi a genuine scalar gives, by general covariance + diffeomorphism
invariance, a CONSISTENT set: metric eqn + phi eqn, related by Bianchi. The
honest question is ONLY: is phi an independent field or a function of g?

CASE I -- phi is an INDEPENDENT scalar that merely HAPPENS to also be written
  into g_tt by a coordinate/gauge choice. Then vary g and phi separately:
    metric: f G_mn + (gBox-nablanabla)f = (1/2)T_mn
    scalar: f'(phi) R = 0            (no kinetic, no potential in this action)
  -> over-determined; new vacuum physics; Schwarzschild fails (shown).

CASE II -- phi is DEFINED as a function of the metric, phi := -1/2 ln(-g_tt/c0^2).
  Then it is NOT an independent field; f(phi)R is just f(g)R, a metric theory
  with a curvature Lagrangian that is a function of the metric and its
  derivatives (since g_tt and its derivs appear). This is an f(g_tt,...)-type
  HIGHER-DERIVATIVE gravity. Vary g freely -- the variation of f(g_tt) w.r.t.
  g contributes. We compute this honestly via the reduced action with the
  LAPSE KEPT FREE (two functions N(r), L(r)) so the (tt) Hamiltonian constraint
  survives, then impose the lock AFTER varying.

This script does CASE II correctly: 2-function reduced action, vary N and L
independently, get 2 EOMs (the constraint from N-variation, the dynamical from
L-variation), THEN substitute the B=1/A lock and the phi identification, and
ask whether Schwarzschild survives.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
th = sp.symbols('theta', real=True)
c0, G, rs = sp.symbols('c0 G r_s', positive=True)
N = sp.Function('N')(r)   # -g_tt
L = sp.Function('L')(r)   # g_rr

# Ricci scalar for diag(-N, L, r^2, r^2 sin^2 th)
def ricci(Nf,Lf):
    g=sp.diag(-Nf,Lf,r**2,r**2*sp.sin(th)**2)
    cl=[sp.symbols('t'),r,th,sp.symbols('p')]; gi=g.inv(); n=4
    Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
     for b in range(n):
      for c in range(n):
        s=0
        for d in range(n): s+=gi[a,d]*(sp.diff(g[d,b],cl[c])+sp.diff(g[d,c],cl[b])-sp.diff(g[b,c],cl[d]))
        Ga[a][b][c]=sp.simplify(s/2)
    Ric=sp.zeros(n,n)
    for b in range(n):
     for d in range(n):
      s=0
      for a in range(n):
        s+=sp.diff(Ga[a][b][d],cl[a])-sp.diff(Ga[a][b][a],cl[d])
        for e in range(n): s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
      Ric[b,d]=sp.simplify(s)
    return sp.simplify(sum(gi[a,b]*Ric[a,b] for a in range(n) for b in range(n))),g
R,g=ricci(N,L)
sqrtmg=sp.sqrt(sp.simplify(-g.det()))

# f as function of N (phi := -1/2 ln(N/c0^2) => e^{-8phi}=(N/c0^2)^4):
f = (N/c0**2)**4 * c0**4/(16*sp.pi*G)   # = N^4/(16 pi G)
Ldens = sp.simplify(sqrtmg*f*R)   # includes |sin th|; we treat sin th>0
Ldens = Ldens.rewrite(sp.Abs).subs(sp.Abs(sp.sin(th)),sp.sin(th))
print("Reduced Lagrangian density L(N,N',N'',L,L') built. Varying N and L freely.")

def EL(Ld,func):
    f1=sp.diff(func,r); f2=sp.diff(func,r,2)
    return sp.simplify(sp.diff(Ld,func)-sp.diff(sp.diff(Ld,f1),r)+sp.diff(sp.diff(Ld,f2),r,2))

EL_N=EL(Ldens,N)   # variation wrt lapse -> (tt) constraint
EL_L=EL(Ldens,L)   # variation wrt g_rr  -> (rr) dynamical
print("\nEL_N (constraint, =0):"); print(sp.simplify(EL_N/(sp.sin(th))))
print("\nEL_L (=0):"); print(sp.simplify(EL_L/(sp.sin(th))))

# Now impose the LOCK and Schwarzschild AFTER varying.
# Schwarzschild: N = (1-rs/r) c0^2,  L = 1/(1-rs/r)  (B=1/A: N*L=c0^2).
Nsch=(1-rs/r)*c0**2; Lsch=1/(1-rs/r)
sub={N:Nsch, sp.diff(N,r):sp.diff(Nsch,r), sp.diff(N,r,2):sp.diff(Nsch,r,2),
     L:Lsch, sp.diff(L,r):sp.diff(Lsch,r), sp.diff(L,r,2):sp.diff(Lsch,r,2)}
print("\n=== Schwarzschild (N=(1-rs/r)c0^2, L=1/(1-rs/r)) in the freely-varied EOMs ===")
print("EL_N(schw) =", sp.simplify(EL_N.subs(sub).doit()/sp.sin(th)))
print("EL_L(schw) =", sp.simplify(EL_L.subs(sub).doit()/sp.sin(th)))

# And flat space:
sub0={N:c0**2, sp.diff(N,r):0, sp.diff(N,r,2):0, L:sp.Integer(1), sp.diff(L,r):0, sp.diff(L,r,2):0}
print("\n=== Flat space (N=c0^2, L=1) ===")
print("EL_N(flat) =", sp.simplify(EL_N.subs(sub0).doit()/sp.sin(th)))
print("EL_L(flat) =", sp.simplify(EL_L.subs(sub0).doit()/sp.sin(th)))
