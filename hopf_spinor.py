#!/usr/bin/env python3
"""
hopf_spinor.py  --  Is UDT's winding unit-vector n the SQUARE of a FORCED spinor?

OBSERVE (gated, the LAST of three spinor-origin routes).
Substitute the Hopf map n_a = psi-dagger sigma_a psi (|psi|=1) into the SETTLED
native angular Lagrangian L = L2 + L4 (native_stabilizer_results.md, CANON
C-2026-06-14-1) and ask:

  Task 1 (KINEMATIC): does L2 = -(xi/2) d_m n . d^m n become the CP^1 model
          L2 = 2 xi |D_m psi|^2 with composite gauge A_m = -i psi-dagger d_m psi?
          Is the resulting psi a BOSONIC constrained scalar doublet (T^2=+1)
          or a genuine anticommuting Dirac fermion (T^2=-1)?

  Task 2 (L4 / TOPOLOGICAL): express L4 (the native Skyrme/winding-current term)
          in psi/CP^1 variables. Does it give a Hopf / Wess-Zumino TOPOLOGICAL
          term? Does that quantize the SOLITON as a fermion (Finkelstein-Rubinstein
          / Wilczek-Zee)?

  Tasks 3-5: anti-circularity gate, hbar honesty, sqrt(m) status.

sympy CPU primary.  DATA-BLIND: no mass / ratio / wall number.
"""
import sympy as sp

print("="*72)
print("HOPF-SPINOR ROUTE: is n the square of a forced spinor?")
print("="*72)

# ---------------------------------------------------------------------------
# Setup: 2-component complex spinor psi = (z0, z1), |psi|^2 = 1.
# Pauli matrices. Hopf map n_a = psi^dagger sigma_a psi.
# ---------------------------------------------------------------------------
# Real/imag parts so sympy can differentiate freely.
a0, b0, a1, b1 = sp.symbols('a0 b0 a1 b1', real=True)   # z0=a0+i b0, z1=a1+i b1
I = sp.I
z0 = a0 + I*b0
z1 = a1 + I*b1
psi = sp.Matrix([z0, z1])
psidag = psi.conjugate().T   # 1x2 row

sx = sp.Matrix([[0,1],[1,0]])
sy = sp.Matrix([[0,-I],[I,0]])
sz = sp.Matrix([[1,0],[0,-1]])
sig = [sx, sy, sz]

# Hopf map components
n = [sp.simplify((psidag*sig[a]*psi)[0,0]) for a in range(3)]
norm2 = sp.simplify(psidag.dot(psi))   # |psi|^2

print("\n[Hopf map]  n_a = psi^dagger sigma_a psi :")
for a,lab in enumerate(['n_x','n_y','n_z']):
    print(f"   {lab} = {n[a]}")
print("   |psi|^2 =", norm2)

# |n|^2 on the constraint surface |psi|^2 = 1
nsq = sp.simplify(n[0]**2 + n[1]**2 + n[2]**2)
print("\n[check] |n|^2 (unconstrained) =", sp.factor(nsq))
# substitute |psi|^2 = 1 :  a0^2+b0^2+a1^2+b1^2 = 1
nsq_constr = sp.simplify(nsq.subs(a1**2, 1 - a0**2 - b0**2 - b1**2))
print("[check] |n|^2 with |psi|^2=1  =", sp.simplify(nsq_constr),
      "  (=> |n|=1 on |psi|=1: TARGET S^2)")

# ===========================================================================
# TASK 1 -- KINEMATIC: L2 = -(xi/2) d_m n . d^m n  ->  CP^1 model.
# We prove the pointwise algebraic identity (independent of metric/coords):
#   (1/4) sum_a (d n_a)(d n_a)  =  (d psidag . d psi) - |psidag d psi|^2
#                                =  |D psi|^2 ,   A = -i psidag d psi.
# We verify it by giving psi a single-parameter dependence psi(s) (a generic
# tangent direction) and comparing the s-derivatives.  Because the identity is
# pointwise in the derivative d_m psi, one generic direction with arbitrary
# velocities suffices (the identity is quadratic in the SAME velocity vector).
# ===========================================================================
print("\n" + "="*72)
print("TASK 1 -- L2 -> CP^1  (the standard O(3)->CP^1 identity, native check)")
print("="*72)

s = sp.symbols('s', real=True)
# generic velocities of each real component
va0,vb0,va1,vb1 = sp.symbols('va0 vb0 va1 vb1', real=True)
subs_lin = {a0:a0+va0*s, b0:b0+vb0*s, a1:a1+vb1*0+va1*s, b1:b1+vb1*s}

def dds(expr):
    return sp.diff(expr.subs(subs_lin, simultaneous=True), s).subs(s,0)

# LHS: (1/4) sum_a (d n_a)^2   [d = d/ds]
dn = [dds(n[a]) for a in range(3)]
LHS = sp.simplify(sp.Rational(1,4)*sum(d**2 for d in dn))

# RHS pieces:
dpsi = sp.Matrix([dds(z0), dds(z1)])
dpsidag = dpsi.conjugate().T
# (d psidag . d psi)
T_kin = sp.simplify((dpsidag*dpsi)[0,0])
# A = -i psidag d psi  (composite U(1) connection, real because |psi|=1 mod gauge)
A = sp.simplify((-I*(psidag*dpsi))[0,0])
RHS = sp.simplify(T_kin - A*sp.conjugate(A))   # |D psi|^2 = |dpsi|^2 - |A|^2

# Enforce the constraint |psi|^2=1 AND its derivative d|psi|^2=0 (psidag dpsi + dpsi dag psi =0)
constr1 = a0**2+b0**2+a1**2+b1**2 - 1
# Re(psidag dpsi) = 0 on the constraint (norm preserved). Build that relation:
re_constraint = sp.simplify(sp.re((psidag*dpsi)[0,0]))   # must be 0 on |psi|=1 flow
print("\n  Re(psidag d psi) (the norm-preservation relation) =", sp.simplify(re_constraint))
print("  -> set =0 (the |psi|=1 constraint keeps the velocity tangent).")

diff = sp.simplify(LHS - RHS)
# reduce diff using constraints |psi|^2=1 and Re(psidag dpsi)=0
diff_red = sp.simplify(diff.subs(a1**2, 1 - a0**2 - b0**2 - b1**2))
# also impose Re(psidag dpsi)=0 : solve for one velocity
sol = sp.solve(re_constraint, va0, dict=True)
if sol:
    diff_red2 = sp.simplify(diff_red.subs(sol[0]).subs(a1**2, 1-a0**2-b0**2-b1**2))
else:
    diff_red2 = diff_red
print("\n  (1/4) sum_a (dn_a)^2  -  [ |dpsi|^2 - |psidag dpsi|^2 ]  on |psi|=1, tangent:")
print("     residual =", sp.simplify(diff_red2))
print("\n  =>  L2 = -(xi/2) d n . d n  =  -2 xi [ |dpsi|^2 - |A|^2 ] = -2 xi |D psi|^2,")
print("      with COMPOSITE connection A_m = -i psidag d_m psi  (the CP^1 model).")

# ---- The statistics question: is psi here bosonic or a Dirac fermion? ----
print("\n  [STATISTICS OF psi IN TASK 1]")
print("  - psi entered as a COMMUTING complex doublet (z0,z1 ordinary numbers).")
print("  - The action L2 is QUADRATIC in psi-bar, psi with NO gamma-matrix /")
print("    first-order Dirac operator: it is |D psi|^2 (second order, Klein-")
print("    Gordon/CP^1 form), the bosonic O(3) sigma-model in disguise.")
print("  - The global symmetry is psi -> e^{i alpha} psi (U(1) GAUGE redundancy):")
print("    psi and e^{i alpha}psi give the SAME n. So psi is a section of the")
print("    Hopf bundle / CP^1 = S^2, a CONSTRAINED BOSONIC field, T^2 = +1.")
print("  VERDICT Task 1: BOSONIC CP^1 re-encoding. NOT a forced Dirac fermion.")

# ===========================================================================
# TASK 2 -- L4 in CP^1 variables: the topological / Hopf term.
# Native L4 = -(kappa/4)(d_m n x d_n n)^2 = -(kappa/4)|omega_H1 current|^2_g.
# Key topological facts (reasoned, with the identity that makes them concrete):
#  (i) The skyrmion winding density n.(d_i n x d_j n) = 2 F_ij^A, the CURVATURE
#      of the composite connection A (Berry curvature of the CP^1 bundle).
#  We verify n.(dn x dn) = 2 (dA) for two independent tangent directions.
# ===========================================================================
print("\n" + "="*72)
print("TASK 2 -- L4 -> winding current; composite Berry curvature; Hopf term")
print("="*72)

s,tt = sp.symbols('s t', real=True)
# two independent velocity directions u (param s) and w (param t)
u = sp.symbols('ua0 ub0 ua1 ub1', real=True)
w = sp.symbols('wa0 wb0 wa1 wb1', real=True)
subs2 = {a0:a0+u[0]*s+w[0]*tt, b0:b0+u[1]*s+w[1]*tt,
         a1:a1+u[2]*s+w[2]*tt, b1:b1+u[3]*s+w[3]*tt}
def Ds(expr): return sp.diff(expr.subs(subs2,simultaneous=True), s).subs({s:0,tt:0})
def Dt(expr): return sp.diff(expr.subs(subs2,simultaneous=True), tt).subs({s:0,tt:0})

# skyrmion density: n . (d_s n x d_t n)
ns  = [Ds(n[a]) for a in range(3)]
nt  = [Dt(n[a]) for a in range(3)]
cross = [ns[1]*nt[2]-ns[2]*nt[1], ns[2]*nt[0]-ns[0]*nt[2], ns[0]*nt[1]-ns[1]*nt[0]]
skyrm = sp.simplify(sum(n[a]*cross[a] for a in range(3)))

# composite curvature F_st = d_s A_t - d_t A_s,  A_m = -i psidag d_m psi
psi_s = sp.Matrix([Ds(z0), Ds(z1)]); psi_t = sp.Matrix([Dt(z0), Dt(z1)])
# A_t at base point = -i psidag psi_t ; need d_s of A_t -> use bilinear:
# F_st = -i ( psi_s^dag psi_t - psi_t^dag psi_s )  (Berry curvature, std identity)
F_st = sp.simplify((-I*((psi_s.conjugate().T*psi_t) - (psi_t.conjugate().T*psi_s)))[0,0])

res = sp.simplify(skyrm - 2*F_st)
res = sp.simplify(res.subs(a1**2, 1-a0**2-b0**2-b1**2))
print("\n  n.(d_s n x d_t n)  -  2 F_st   (F_st = Berry curvature of A) =",
      sp.simplify(res))
print("  =>  the skyrmion winding 2-form (== omega_H1 current) IS 2x the")
print("      curvature dA of the COMPOSITE connection A = -i psidag d psi.")
print("\n  Consequence: L4 = -(kappa/4)|winding current|^2_g is, in CP^1 vars,")
print("  the squared Berry/composite-curvature |F(A)|^2_g  (a Maxwell-type term")
print("  for the COMPOSITE A) -- still MANIFESTLY BOSONIC and metric-dependent.")

print("\n  [IS THERE A HOPF/WESS-ZUMINO TERM?]  (reasoned, decisive)")
print("  - The Hopf invariant term is theta_H * INT A ^ dA  (a metric-FREE,")
print("    PARITY/T-ODD topological term).  L4 = -(kappa/4)|F|^2_g is")
print("    metric-dependent, even, second-order: it is the energy/Skyrme term,")
print("    NOT A^dA.  L2 and L4 are BOTH P- and T-EVEN and metric-contracted.")
print("  - A Hopf term A^dA is a SEPARATE term one would ADD. Neither L2 nor L4")
print("    contains it. UDT's settled L = L2+L4 does NOT generate a Hopf term.")
print("  - In 3+1 D the relevant skyrmion-statistics term is instead the")
print("    Wess-Zumino-Witten term tied to pi_4(S^2)=Z_2 (Finkelstein-Rubinstein).")
print("    Its COEFFICIENT (FR phase = 0 or pi, i.e. boson or fermion) is NOT")
print("    fixed by L2+L4: it is an INDEPENDENT theta-like topological choice,")
print("    a discrete Z_2 input, not forced by the energy functional.")

# ===========================================================================
# TASK 5 -- sqrt(m):  is any sqrt(m) amplitude native here?
# ===========================================================================
print("\n" + "="*72)
print("TASK 5 -- sqrt(m) status")
print("="*72)
print("  - L2, L4 are quadratic/quartic in d psi (bosonic energy densities).")
print("  - The soliton MASS = INT (E2+E4) is an ENERGY (linear in the energy")
print("    density), NOT a sqrt of one. No amplitude whose modulus-squared is")
print("    the energy appears: psi is normalized |psi|=1 (pure phase/direction),")
print("    carrying NO sqrt(energy) weight.  A Dirac sqrt(m) would come from a")
print("    FIRST-ORDER operator (psibar(i gamma.D - m)psi) -- absent here.")
print("  - Consistent with #45 / n3_direction_distribution: sqrt(m) is the")
print("    spinor INPUT, not an output of the bosonic winding sector.")
print("  VERDICT Task 5: NO native sqrt(m). Absent, consistent with #45.")

print("\n" + "="*72)
print("DONE.")
print("="*72)
