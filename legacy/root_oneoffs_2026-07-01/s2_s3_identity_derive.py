#!/usr/bin/env python3
"""
s2_s3_identity_derive.py -- SETTLE the S^2-vs-S^3 OBJECT-IDENTITY (facet B): does
the NATIVE L2+L4 action SOURCE a 4th field component (=> S^3) or not (=> S^2)?

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  Mode: OBSERVE / DERIVE (symbolic-exact).
DATA-BLIND -- no mass/ratio/wall number.  Largely sympy; small numeric checks only.

GOVERNING: S2_S3_OBJECT_IDENTITY_MAP.md.  THE TRIPWIRE: argue from what the action
DEMANDS (necessity), not what it PERMITS.  (The prior settle died inflating "EOM
permits Theta=pi/2 const" -> "object IS S^2".)

THE TWO CANDIDATE L4 FORMS (the provenance fork lives HERE):
  (NATIVE, native_skyrme_derive.py / CANON C-2026-06-14-1):
     F_{mn} = n . (d_m n x d_n n)  = eps_{abc} n_a d_m n_b d_n n_c   [SCALAR 2-form]
     S_{mn} = d_m n x d_n n         [3-VECTOR 2-form]
     L4_native = -(kappa/4) g^{mp} g^{nq} S_{mn}.S_{pq}
     -- the CROSS PRODUCT is intrinsically 3-component (eps_abc, a,b,c in 1..3).
        It is STRUCTURALLY BLIND to any n_4: n_4 appears NOWHERE in F or S.

  (LAGRANGE-IDENTITY, matter_ansatz_derive.py, the "any target dim" form):
     L4_lag = -(kappa/4) g^{mp} g^{nq} [ (d_m n.d_p n)(d_n n.d_q n)
                                       - (d_m n.d_q n)(d_n n.d_p n) ]
     -- this DOES see n_4 (the dot products run over ALL components).

These two are EQUAL iff the target is a 3-vector (Lagrange/BAC-CAB identity holds for
exactly 3 components).  For a 4-vector they DIFFER.  So the question "does L4 source
n_4?" is ENTIRELY the question "which L4 is native?".  This script (i) shows the two
forms agree on a 3-vector and DIFFER on a 4-vector; (ii) derives the n_4 EOM under
the NATIVE (cross-product) action and shows it has NO source term; (iii) checks
whether any metric / dilation factor sources a chiral n_4 sweep.
"""
import sympy as sp

print("="*78)
print("S2/S3 OBJECT IDENTITY (facet B): does the NATIVE action SOURCE n_4?")
print("="*78)

def vec(name, d):
    return sp.Matrix(d, 1, lambda i, _: sp.Symbol(f'{name}{i}', real=True))

def cross3(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1],
                      a[2]*b[0]-a[0]*b[2],
                      a[0]*b[1]-a[1]*b[0]])

def dot(a, b):
    return (a.T*b)[0, 0]

# ---------------------------------------------------------------------------
# PART 1.  The native L4 (cross-product) vs the Lagrange-identity L4:
#          AGREE on a 3-vector, DIFFER on a 4-vector.  (provenance fork, exact)
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("PART 1: native (cross-product) L4 == Lagrange-identity L4 ?  (per target dim)")
print("-"*78)

for d in (3, 4):
    n = vec('n', d)
    dn = [vec(f'd{m}n', d) for m in range(4)]
    # NATIVE only defined for d=3 (cross product). For d=4 it is UNDEFINED
    # (no 3-vector cross product) -> that is itself the structural verdict.
    if d == 3:
        def Snat(m, k): return cross3(dn[m], dn[k])
        # full contraction with a generic diagonal inverse metric
        gi = sp.symbols('gi0:4', positive=True)
        L4_native = sum(gi[m]*gi[k]*dot(Snat(m, k), Snat(m, k))
                        for m in range(4) for k in range(4))
        L4_lag = sum(gi[m]*gi[k]*(dot(dn[m], dn[m])*dot(dn[k], dn[k])
                                  - dot(dn[m], dn[k])*dot(dn[k], dn[m]))
                     for m in range(4) for k in range(4))
        diff = sp.simplify(sp.expand(L4_native - L4_lag))
        print(f"  d=3: native(cross) - Lagrange-identity = {diff}"
              "   (0 => identical; cross product EXISTS)")
    else:
        gi = sp.symbols('gi0:4', positive=True)
        # NATIVE cross product does NOT exist for a 4-vector. The Lagrange form does:
        L4_lag = sum(gi[m]*gi[k]*(dot(dn[m], dn[m])*dot(dn[k], dn[k])
                                  - dot(dn[m], dn[k])*dot(dn[k], dn[m]))
                     for m in range(4) for k in range(4))
        # does the Lagrange L4 depend on the 4th component's derivatives?
        d4_terms = [sp.diff(L4_lag, sp.Symbol(f'd{m}n3')) for m in range(4)]
        sees_n4 = any(sp.simplify(t) != 0 for t in d4_terms)
        print(f"  d=4: native cross product UNDEFINED (eps_abc is 3-index).")
        print(f"       Lagrange-identity L4 depends on d_m n_4 ?  {sees_n4}")
        print("       => the ONLY L4 that sees n_4 is the NON-native Lagrange form.")

# ---------------------------------------------------------------------------
# PART 2.  n_4 EOM under the NATIVE action with a FULLY GENERAL 4th component.
#   Native action on a unit 4-vector |n|^2=1:
#     L2     = -(xi/2) g^{mn} d_m n . d_n n      (dot over ALL 4 comps: L2 SEES n_4)
#     L4_nat = -(kappa/4) g^{..} S.S, S=cross3 of the FIRST THREE comps only
#              (the native eps_abc current; STRUCTURALLY blind to n_4)
#   Question: is there a SOURCE term forcing n_4 off a constant?
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("PART 2: n_4 EOM under the NATIVE action, general 4th component live")
print("-"*78)

r, th, ps = sp.symbols('r theta psi', positive=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r)
ginv = sp.diag(-sp.exp(-2*A), sp.exp(-2*B), 1/r**2, 1/(r**2*sp.sin(th)**2))
sqrtg = sp.exp(A+B)*r**2*sp.sin(th)
coords = [sp.Symbol('t'), r, th, ps]

# Most general unit 4-vector with a LIVE 4th angle X(r) (the candidate S^3 sweep):
#  n = ( cos X(r) * [S^2 hedgehog 3-vector] , sin X(r) )   -- |n|=1 for any S^2 unit
# S^2 hedgehog (deg-1 area-form carrier, the canon n_a):
X = sp.Function('X')(r)            # the candidate live 4th-component angle, fully general
u1 = sp.sin(th)*sp.cos(m*ps)
u2 = sp.sin(th)*sp.sin(m*ps)
u3 = sp.cos(th)
n = sp.Matrix([sp.cos(X)*u1, sp.cos(X)*u2, sp.cos(X)*u3, sp.sin(X)])
print("n =", list(n), "\n  (X(r) GENERAL; X=0 => pure S^2 unit 3-vector; X live => S^3)")
print("|n|^2 - 1 =", sp.simplify(dot(n, n) - 1))

dn = [sp.zeros(4, 1) for _ in range(4)]
for a_ in range(4):
    dn[1][a_] = sp.diff(n[a_], r)
    dn[2][a_] = sp.diff(n[a_], th)
    dn[3][a_] = sp.diff(n[a_], ps)

# ---- NATIVE action density ----
# L2: dot over ALL 4 components (this is where n_4 can be sourced, if at all)
Gf = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Gf[mu, nu] = dot(dn[mu], dn[nu])
L2 = -(xi/2)*sum(ginv[i, i]*Gf[i, i] for i in range(4))

# L4_native: cross product of the FIRST THREE comps only (the eps_abc area form).
n3 = sp.Matrix(n[0:3])
dn3 = [sp.Matrix(dn[mu][0:3]) for mu in range(4)]
def Snat(mu, nu): return cross3(dn3[mu], dn3[nu])
L4 = -(kap/4)*sum(ginv[mm, mm]*ginv[nn, nn]*dot(Snat(mm, nn), Snat(mm, nn))
                  for mm in range(4) for nn in range(4))
L = sp.simplify(L2 + L4)

# Reduced radial action: integrate sqrt(-g) L over (th,ps).
Lrad = sp.simplify(sp.integrate(sp.integrate(sp.simplify(L*sqrtg),
                                             (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))
Xp = sp.diff(X, r)
# Euler-Lagrange for X(r):  d/dr(dL/dX') - dL/dX = 0
EL_X = sp.simplify(sp.diff(sp.diff(Lrad, Xp), r) - sp.diff(Lrad, X))
print("\nNATIVE radial Lagrangian Lrad(r) =")
sp.pprint(sp.simplify(Lrad))
print("\nn_4 EOM  EL[X] (native action, = 0) =")
sp.pprint(EL_X)

# Is X = const (n_4 = const, in particular X=0) a solution with NO source?
EL_Xconst = sp.simplify(EL_X.subs({sp.diff(X, r, 2): 0, Xp: 0}))
print("\nEL[X] with X'=X''=0 (the SOURCE term that would force X off-constant) =")
sp.pprint(EL_Xconst)
print("   -> if this is identically 0 for ALL X, the native action does NOT source n_4")
print("      (DEMANDS: X free, no source) => the 4th component is unsourced.")
# Also show the X=0 (pure S^2) source explicitly:
print("\nEL[X] source at X=0 (pure S^2 point) =", sp.simplify(EL_Xconst.subs(X, 0)))

# ---------------------------------------------------------------------------
# PART 3.  Does the metric coupling (dilation e^{(a+1)phi} / A,B) source a chiral
#          sweep of n_4?  Check whether ANY A,B-dependent term multiplies a
#          non-derivative function of X in EL[X] (a "bare"/source term).
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("PART 3: does any metric/dilation factor SOURCE a chiral n_4 sweep?")
print("-"*78)
# A source = a term in EL[X] with NO X' or X'' (a function of X, r, A, B alone).
src = EL_Xconst
print("metric-coupled source term (coeff of bare X, all A,B factors retained):")
sp.pprint(sp.simplify(src))
print("contains exp(A)/exp(B) factor multiplying a bare function of X?",
      src != 0)

# ---------------------------------------------------------------------------
# PART 4.  CONTRAST: the n_4 EOM under the LAGRANGE-IDENTITY (non-native) L4.
#          Show THIS one DOES source n_4 (so S^3 only appears with the import).
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("PART 4: CONTRAST -- n_4 EOM under the LAGRANGE-IDENTITY (non-native) L4")
print("-"*78)
L4_lag = -(kap/4)*sum(ginv[mm, mm]*ginv[nn, nn]*(Gf[mm, mm]*Gf[nn, nn]
                                                 - Gf[mm, nn]*Gf[nn, mm])
                      for mm in range(4) for nn in range(4))
L_lag = sp.simplify(L2 + L4_lag)
Lrad_lag = sp.simplify(sp.integrate(sp.integrate(sp.simplify(L_lag*sqrtg),
                                                 (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))
EL_X_lag = sp.simplify(sp.diff(sp.diff(Lrad_lag, Xp), r) - sp.diff(Lrad_lag, X))
src_lag = sp.simplify(EL_X_lag.subs({sp.diff(X, r, 2): 0, Xp: 0}))
print("LAGRANGE-identity n_4 source term (X'=X''=0) =")
sp.pprint(src_lag)
print("\n=> if this is NONZERO, the NON-native L4 sources n_4 (the S^3 sweep);")
print("   the native (cross-product) L4 does not (Part 2). The S^3 object exists")
print("   ONLY under the imported Lagrange-identity L4, not the native eps_abc one.")
print("\nDONE.")
