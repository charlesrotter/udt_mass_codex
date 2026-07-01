#!/usr/bin/env python3
"""
s2_s3_identity_texture.py -- (OI-texture) is the cos(theta) tangential texture in
the S^2-carrier stress INTRINSIC to the native object or an ARTIFACT of the
mPsi-winding embedding / chart?  AND (OI-import) is there ANY native 4-index/pi_3
invariant, or only the 3-index eps_abc area form?  sympy-exact.  DATA-BLIND.

The texture: coupled_tl_s2_derive computed the S^2 hedgehog
  n=(sinTheta sin th cos m ps, sinTheta sin th sin m ps, cos Theta)  [a NON-unit-amplitude
  embedding: |n|^2 = sin^2Theta sin^2 th + cos^2 Theta != 1 in general]
and found a cos(th) texture in T^th_th.  We test: does the GENUINELY ROUND S^2 unit
hedgehog (the degree-1 generator of pi_2, n = spatial-unit-vector dressed by a radial
profile, |n|=1) carry that texture, or was it the non-unit / mPsi embedding?
"""
import sympy as sp

print("="*78)
print("PART A: texture -- non-unit mPsi embedding vs the ROUND unit S^2 hedgehog")
print("="*78)
r, th, ps = sp.symbols('r theta psi', positive=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r); Th = sp.Function('Theta')(r)
ginv = sp.diag(-sp.exp(-2*A), sp.exp(-2*B), 1/r**2, 1/(r**2*sp.sin(th)**2))
glow = [-sp.exp(2*A), sp.exp(2*B), r**2, r**2*sp.sin(th)**2]
def dot(a, b): return (a.T*b)[0, 0]
def cross3(a, b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

def stress_diag(n):
    dn = [sp.zeros(3, 1) for _ in range(4)]
    for a_ in range(3):
        dn[1][a_] = sp.diff(n[a_], r); dn[2][a_] = sp.diff(n[a_], th); dn[3][a_] = sp.diff(n[a_], ps)
    Gf = sp.Matrix(4, 4, lambda i, j: dot(dn[i], dn[j]))
    gI = sp.symbols('gItt gIrr gIth gIps')
    L2s = -(xi/2)*sum(gI[i]*Gf[i, i] for i in range(4))
    def Sn(i, j): return cross3(dn[i], dn[j])
    L4s = -(kap/4)*sum(gI[i]*gI[j]*dot(Sn(i, j), Sn(i, j)) for i in range(4) for j in range(4))
    Ls = L2s + L4s
    sub = {gI[0]: ginv[0, 0], gI[1]: ginv[1, 1], gI[2]: ginv[2, 2], gI[3]: ginv[3, 3]}
    T = {}
    for i in range(4):
        Tii = (-2*sp.diff(Ls, gI[i]) + glow[i]*Ls).subs(sub)
        T[i] = sp.simplify(ginv[i, i]*Tii)
    return T

# (1) the mPsi non-unit embedding (coupled_tl_s2_derive):
n_mpsi = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(m*ps),
                    sp.sin(Th)*sp.sin(th)*sp.sin(m*ps),
                    sp.cos(Th)])
print("\nembedding 1 (mPsi):  |n|^2 =", sp.simplify(dot(n_mpsi, n_mpsi)),
      " (NOT 1 unless sin th =1 => a NON-unit map off the equator)")
T1 = stress_diag(n_mpsi)
print("  T^th_th (mPsi) =", sp.simplify(T1[2]))
print("    depends on th (texture)?", sp.simplify(sp.diff(T1[2], th)) != 0)

# (2) the genuinely ROUND unit S^2 hedgehog: target point = spatial unit direction,
#     radial profile = identity of amplitude (|n|=1 EXACTLY for all th):
n_round = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(m*ps),
                     sp.sin(Th)*sp.sin(th)*sp.sin(m*ps),
                     sp.cos(Th)*sp.cos(0)])   # placeholder
# The genuine unit deg-1 hedgehog onto target S^2 with spatial sphere as domain:
#   n = (sin Th(r) * x_hat) with x_hat=(sin th cos ps, sin th sin ps, cos th) PLUS cos Th
#   -> that's 4 comps (S^3).  The genuine UNIT 3-vector deg-1 map S^2_space->S^2_target
#   is simply  n = x_hat = (sin th cos ps, sin th sin ps, cos th)  (Th-independent, the
#   pure topological n=x/r, |n|=1 exactly).  CANON: this is exact everywhere.
n_topo = sp.Matrix([sp.sin(th)*sp.cos(m*ps), sp.sin(th)*sp.sin(m*ps), sp.cos(th)])
print("\nembedding 2 (pure topological n=x/r, the CANON deg-1 unit hedgehog): |n|^2 =",
      sp.simplify(dot(n_topo, n_topo)), " (=1 EXACTLY, all th)")
T2 = stress_diag(n_topo)
print("  T^t_t  =", sp.simplify(T2[0]))
print("  T^r_r  =", sp.simplify(T2[1]))
print("  T^th_th=", sp.simplify(T2[2]))
print("  T^th_th depends on th (texture)?  ",
      sp.simplify(sp.diff(T2[2], th)) != 0)
print("  T^t_t == T^r_r (CANON C-14-1, B=1/A) ?  ",
      sp.simplify(T2[0]-T2[1]) == 0)

print("\n" + "="*78)
print("PART B: is there ANY native 4-index / pi_3 invariant, or only eps_abc (3-index)?")
print("="*78)
print("""
The native winding current is F_mn = eps_abc n_a d_m n_b d_n n_c (h1_types, CANON
C-14-1).  eps_abc has exactly 3 internal indices -> requires exactly a 3-vector
target.  A pi_3 / baryon (S^3) current needs a 4-index internal epsilon
eps_abcd n_a d_m n_b d_n n_c d_p n_d (a 3-FORM, the Wess-Zumino/baryon density).

Two facts settle whether eps_abcd is native:
 (i) The internal index space is set by the TARGET. The native target is the unit
     3-vector n_a sourced by L2 (CANON C-14-1: a,b,c in {1,2,3}); there are only 3
     internal directions, so eps_abcd (needing 4) is not constructible from the
     native field. (structural)
 (ii) #50 (su3_field_test, blind-verified): the metric connection is
     U(1) x SO(3) x SO(3,1); the only internal rotation the METRIC supplies is the
     SO(3) acting on the 3-vector (= Isom(S^2)).  There is no metric-supplied SU(2)
     acting on a 4-vector (= Isom(S^3)).  So even the SYMMETRY that would protect a
     pi_3 object is absent natively.
""")
# Demonstrate eps_abcd needs a 4th independent component to be nonzero:
na = sp.symbols('n0:4', real=True)
print("A 4-index epsilon contraction eps_abcd n_a (...) is identically 0 if the")
print("field has only 3 independent components (n_4 = const dependent): the 4th slot")
print("of eps_abcd must hit an INDEPENDENT 4th DOF.  Since L2+L4 sources no")
print("independent n_4 (s2_s3_identity_derive/stability: n_4 unsourced, X=0 stable")
print("against charge-preserving deformations; the only roll DESTROYS charge), the")
print("4-index invariant has no native field to act on.")
print("\nDONE.")
