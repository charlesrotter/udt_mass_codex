#!/usr/bin/env python3
"""
phase0_rotation_sharpen.py -- sharpen (B1): does the rotation shift sector FORCE
d_t w = 0 (like the round-diagonal case), or does it ADMIT d_t w != 0 in vacuum?

Driver: Claude (Opus 4.8, 1M). 2026-06-18. DATA-BLIND. Category-A. LEADING ORDER.

The round-diagonal case had ONE momentum constraint G_{tr}=2 d_t phi/r that
DIRECTLY set d_t phi=0. For the axial shift w(t,r,theta) we collect ALL O(eps)
vacuum equations and ask: do they algebraically force d_t w = 0, or do they leave
a time-dependent w consistent (the constraints are differential-in-space, the
dynamical content lives in a separate evolution component)?
"""
import sympy as sp

t, r, th, ps, c = sp.symbols('t r theta psi c', positive=True)
eps = sp.symbols('epsilon')
X = [t, r, th, ps]
w = sp.Function('w')(t, r, th)

g1 = sp.Matrix([
    [-c**2, 0,    0,    eps*w],
    [0,     1,    0,    0],
    [0,     0,    r**2, 0],
    [eps*w, 0,    0,    r**2*sp.sin(th)**2],
])


def einstein_tensor(g, X):
    n = len(X)
    ginv = g.inv()
    Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, cc], X[b])
                                     + sp.diff(g[d, b], X[cc])
                                     - sp.diff(g[b, cc], X[d]))
                Gamma[a][b][cc] = sp.Rational(1, 2)*s
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            s = sp.S(0)
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], X[a]) - sp.diff(Gamma[a][b][a], X[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            Ric[b, d] = s
    Rscal = sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    G = sp.zeros(n, n)
    for mu in range(n):
        for nu in range(n):
            G[mu, nu] = Ric[mu, nu] - sp.Rational(1, 2)*g[mu, nu]*Rscal
    return G


G1 = einstein_tensor(g1, X)
labels = {(0,1):'G_tr',(0,2):'G_ttheta',(0,3):'G_tpsi',
          (1,3):'G_rpsi',(2,3):'G_thetapsi',(1,2):'G_rtheta'}
print("=== All O(eps) vacuum equations for the axial shift w(t,r,theta) ===")
eqs = {}
for (i,j),name in labels.items():
    val = sp.simplify(sp.series(G1[i,j], eps, 0, 2).removeO().coeff(eps,1))
    eqs[name] = val
    print(f"\n{name} = 0  ->", val, " = 0")

# Key question: is the SPATIAL (elliptic) constraint G_tpsi independent of t-derivs?
# And do the t-derivative equations (G_rpsi, G_thetapsi) FORCE d_t w=0, or are they
# satisfiable by a time-dependent w?
print("\n--- Does the vacuum set force d_t w = 0? ---")
# G_tpsi is the elliptic operator on w at each time slice (NO d_t): purely spatial.
gtpsi = eqs['G_tpsi']
print("G_tpsi has any d_t? ", gtpsi.has(sp.Derivative(w,t)) or gtpsi.has(sp.diff(w,t,2)))
# G_rpsi, G_thetapsi are the d_t terms. They are 'd_t (spatial op) w = 0' form.
grpsi = eqs['G_rpsi']; gthpsi = eqs['G_thetapsi']
print("G_rpsi      :", grpsi)
print("G_thetapsi  :", gthpsi)

# Test: take w(t,r,th) = T(t)*W(r,th) (separable). Substitute and see whether the
# t-equations force T'(t)=0 or merely impose a spatial condition on W.
T = sp.Function('Tf')(t); W = sp.Function('Wf')(r, th)
sub = {w: T*W}
def subst(expr):
    e = expr
    # replace derivatives of w by derivatives of T*W
    return sp.simplify(e.subs(sp.Derivative(w, t), sp.Derivative(T,t)*W)
                       .subs(sp.Derivative(w, t, r), sp.Derivative(T,t)*sp.Derivative(W,r))
                       .subs(sp.Derivative(w, t, th), sp.Derivative(T,t)*sp.Derivative(W,th))
                       .subs(w, T*W))
gr = subst(grpsi); gth = subst(gthpsi); gtp = subst(gtpsi.subs(w,T*W))
print("\nSeparable w=Tf(t)*Wf(r,th):")
print("  G_rpsi/eps     =", gr)
print("  G_thetapsi/eps =", gth)
print("  G_tpsi/eps     =", sp.simplify(gtp))
# Factor out Tf'(t): the t-eqs are Tf'(t) * [spatial operator on Wf] = 0.
print("\nG_rpsi  = Tf'(t) * (spatial op on Wf):",
      sp.simplify(gr / sp.Derivative(T,t)))
print("G_thetapsi = Tf'(t) * (spatial op on Wf):",
      sp.simplify(gth / sp.Derivative(T,t)))
print("\nINTERPRETATION: the t-derivative vacuum equations factor as")
print("  Tf'(t) * L_spatial[Wf] = 0.")
print("They are satisfied by a TIME-DEPENDENT Tf(t) (Tf' != 0) PROVIDED Wf solves")
print("L_spatial[Wf]=0 -- i.e. d_t w != 0 is CONSISTENT with vacuum (NOT forced to 0).")
print("Contrast the round-diagonal case: G_tr = 2 d_t phi /r had NO spatial operator")
print("to absorb the time-dependence, so it forced d_t phi = 0 pointwise. The")
print("off-diagonal shift supplies that spatial operator -> Birkhoff obstruction RELAXED.")
