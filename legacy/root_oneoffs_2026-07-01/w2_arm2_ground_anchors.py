#!/usr/bin/env python3
"""
W2 ARM-2 (interface/seal demands on the SHAPED class) — SCRIPT 1:
GROUNDING ANCHORS.  Date: 2026-06-11.  Driver: W2 arm-2 agent.
Declared METRIC-LED (w_stiffness_push_declaration.md, "W2 framing
correction": uncovering only; nothing added to the theory).

PRE-REGISTERED FAILURE CRITERIA for the whole arm (stated before any
computation ran; recorded identically in all three w2_arm2_* scripts):
  FC-1 (shaped seal law): if the on-axis seal law f^2 K -> 4 f_u^2/y^4
       (mass_audit_results.md erratum of record, = 24 a^2/y^4 under
       a = f_u/sqrt(6)), recomputed on the axis-regular shaped class
       (w on), contains NO w-jet term at the singular order, the seal
       singularity is w-blind -> scoped negative.
  FC-2 (S1 rerun): if the finite-action admissibility machinery
       (sealed_cavity_s1_results.md item 7 species) yields no
       condition on the w-channel at the seal -> scoped negative.
  FC-3 (interface jet): if the junction/continuation demands reduce
       to two-sided matching with no autonomous one-sided relation on
       (w, w_r, w_rr) beyond a clamp conditional on the spherical-tail
       premise, the "metric enforces a w-interface law" claim is
       downgraded to a conditional clamp; if the w_r-kink layer
       carries no distributional curvature at all, Part 2 is fully
       negative.

THIS SCRIPT: anchors only (no new claims):
  A. Curvature engine validation (Schwarzschild K = 48 M^2/y^6).
  B. Reproduce the diagonal-class on-axis seal law of record:
     K_axis = a''^2 + 4a'^2/y^2 + 4(a-1)^2/y^4 + 16 b^2/(y^4 a^2)
     for f = a(y) + b(y) th^2  (VMA formula, verify_mass/v_kretsch3),
     seal limit f^2 K -> 16 b^2/y^4 = 4 f_u(pole)^2/y^4.
  C. Reproduce the P1 closed-form C1 density (pde_p1 D-06) on the
     full shaped class and verify EXACT zeroth-jet structure in
     (q, w): no q_r, q_th, w_r, w_th anywhere => pi_w = pi_q = 0 and
     the first variation of S_C1 carries NO surface term in the w- or
     q-channels at any interface (the f-channel surface weight is
     nonzero — printed).  [Route A theorem anchor, w_stiffness_results]
  D. ELEMENTARY FLATNESS AT THE AXIS derives w = 0 on the axis:
     circumference/proper-radius -> 2 pi/(1+w0)^2; with w = c(y) th^2
     the deficit closes at O(th^2).  (The metric's own axis demand on
     the shape field — first metric-own w-condition, already implicit
     in VB's W1 amendment; here derived exactly.)
  E. The shaped sonic locus: on the w-on class the q*-eliminated
     metric degenerates EXACTLY on Delta_w = f r^2 (1+w)^2 f_r^2 -
     f_th^2 = 0 (the w-dressed static sonic locus; pde_p1 D-12/D-21
     generalized with w kept on).
Conventions: R-areal canon rho = r; signature (-,+,+,+); static
sector (the time row enters no anchor here); exact sympy throughout,
no linearization.
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"G-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, y, th, ph = sp.symbols('T y theta phi')
xs = [T, y, th, ph]

def riemann_dddd_and_K(gdd, simp=sp.simplify):
    """Generic curvature engine: Christoffel -> Riemann -> Kretschmann.
    Returns (Riem_uddd, Rdddd, K). Exact, no simplification shortcuts
    beyond the requested simp on Christoffels."""
    guu = gdd.inv()
    Gam = [[[simp(sum(guu[a, d]*(sp.diff(gdd[d, b], xs[c])
            + sp.diff(gdd[d, c], xs[b]) - sp.diff(gdd[b, c], xs[d]))
            for d in range(4))/2) for c in range(4)] for b in range(4)]
           for a in range(4)]
    Riem = [[[[sp.diff(Gam[a][b][d], xs[c]) - sp.diff(Gam[a][b][c], xs[d])
               + sum(Gam[a][e][c]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][c]
                     for e in range(4))
               for d in range(4)] for c in range(4)] for b in range(4)]
            for a in range(4)]
    Rdddd = [[[[sum(gdd[a, e]*Riem[e][b][c][d] for e in range(4))
                for d in range(4)] for c in range(4)] for b in range(4)]
             for a in range(4)]
    K = sp.Integer(0)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    t1 = Rdddd[a][b][c][d]
                    if t1 == 0:
                        continue
                    # all metrics used with this engine are DIAGONAL
                    K += t1**2*guu[a, a]*guu[b, b]*guu[c, c]*guu[d, d]
    return Riem, Rdddd, K

# ---------------------------------------------------------------------
# A. engine validation: Schwarzschild
# ---------------------------------------------------------------------
M = sp.symbols('M', positive=True)
fs = 1 - 2*M/y
g_s = sp.diag(-fs, 1/fs, y**2, y**2*sp.sin(th)**2)
_, _, K_s = riemann_dddd_and_K(g_s)
check("A1", sp.simplify(K_s - 48*M**2/y**6) == 0,
      "Schwarzschild Kretschmann = 48 M^2/y^6 (engine validated)")

# ---------------------------------------------------------------------
# B. diagonal-class on-axis seal law (the erratum of record), computed
#    in u = cos(theta) (rational metric — no trig; axis = u -> 1):
#    ds^2 = -f dT^2 + f^{-1} dy^2 + y^2 du^2/(1-u^2) + y^2 (1-u^2) dph^2
#    f = a(y) + b(y)(1-u)  =>  f_u(pole) = -b.
# ---------------------------------------------------------------------
u = sp.Symbol('u', real=True)
xs = [T, y, u, ph]      # rebind coordinate list for the engine
# engine validation in u-coordinates (Schwarzschild):
g_su = sp.diag(-fs, 1/fs, y**2/(1 - u**2), y**2*(1 - u**2))
_, _, K_su = riemann_dddd_and_K(g_su, simp=sp.cancel)
check("B0", sp.simplify(K_su - 48*M**2/y**6) == 0,
      "engine validated in u = cos(theta) coordinates (Schwarzschild)")
a = sp.Function('a')(y); b = sp.Function('b')(y)
fF = a + b*(1 - u)
g_d = sp.diag(-fF, 1/fF, y**2/(1 - u**2), y**2*(1 - u**2))
_, _, K_d = riemann_dddd_and_K(g_d, simp=sp.cancel)
print(f"[t={time.time()-t0:.0f}s] diagonal K built; taking axis limit ...",
      flush=True)
A, A1, A2, B, B1, B2 = sp.symbols('A A1 A2 B B1 B2', real=True)
sub = {sp.Derivative(a, (y, 2)): A2, sp.Derivative(a, y): A1,
       sp.Derivative(b, (y, 2)): B2, sp.Derivative(b, y): B1, a: A, b: B}
K_d_sym = sp.cancel(sp.together(K_d.xreplace(sub)))
K_d_axS = sp.simplify(K_d_sym.subs(u, 1))
K_vma = A2**2 + 4*A1**2/y**2 + 4*(A - 1)**2/y**4 + 4*B**2/(y**4*A**2)
# (VMA's 16 b^2 was in the th-jet convention f = a + b th^2, i.e.
#  f_u = -2b; here f = a + b(1-u) has f_u = -b, so the same law reads
#  4 b^2/(y^4 a^2) = 4 f_u^2/(y^4 a^2).)
check("B1", sp.simplify(K_d_axS - K_vma) == 0,
      "K_axis = a''^2 + 4a'^2/y^2 + 4(a-1)^2/y^4 + 4 f_u^2/(y^4 a^2) "
      "(VMA's exact diagonal axis formula reproduced; f_u = -b)")
lead = sp.limit(sp.expand(K_d_axS*A**2), A, 0)
check("B2", sp.simplify(lead - 4*B**2/y**4) == 0,
      "seal law: f^2 K -> 4 f_u(pole)^2/y^4 "
      "(= 24 a^2/y^4 under a = f_u/sqrt(6); mass_audit erratum of record)")

# ---------------------------------------------------------------------
# C. P1 closed form on the FULL shaped class + zeroth-jet in (q,w)
# ---------------------------------------------------------------------
r = sp.Symbol('r', positive=True); c = sp.Symbol('c')
fq = sp.Function('f')(r, th); qq = sp.Function('q')(r, th)
wq = sp.Function('w')(r, th)
W = (1 + wq)**2
gP = sp.Matrix([
    [-fq, 0, 0, 0],
    [0, 1/fq, qq, 0],
    [0, qq, r**2*W, 0],
    [0, 0, 0, r**2*sp.sin(th)**2/W]])
D2 = r**2*W - fq*qq**2
sqrtmg = r*sp.sin(th)*sp.sqrt(D2)/(1 + wq)
check("C1", sp.simplify(sqrtmg**2 - (-gP.det())) == 0,
      "sqrt(-g) = r sin(th) sqrt(r^2 W - f q^2)/(1+w)  [P1 D-03]")
gPi = gP.inv()
phir, phith = -sp.diff(fq, r)/(2*fq), -sp.diff(fq, th)/(2*fq)
Kkin = (gPi[1, 1]*phir**2 + 2*gPi[1, 2]*phir*phith + gPi[2, 2]*phith**2)
Lc1 = -(c/2)*fq*Kkin*sqrtmg
A_ = fq*r**2*W*sp.diff(fq, r)**2 + sp.diff(fq, th)**2
Lclosed = -(c/8)*r*sp.sin(th)*(A_ - 2*fq*qq*sp.diff(fq, r)*sp.diff(fq, th)) \
          / ((1 + wq)*fq*sp.sqrt(D2))
check("C2", sp.simplify(Lc1 - Lclosed) == 0,
      "C1 density closed form on the full shaped class [P1 D-06]")
derivs = Lc1.atoms(sp.Derivative)
bad = [d for d in derivs if d.expr in (qq, wq)]
check("C3", len(bad) == 0,
      "L_C1 contains NO derivative of q or w (exact atom census): "
      "pi_w = pi_q = 0; dL/d(w_r) == 0 IDENTICALLY")
# => first variation surface terms at an interface r = r0:
#    w-channel: dL/d(w_r) = 0  -> NO surface term, NO delta weight;
#    f-channel: dL/d(f_r) != 0 -> nonzero surface weight (the
#    fork_tests F-kink species).
dLdfr = sp.simplify(sp.diff(Lc1, sp.Derivative(fq, r)))
check("C4", sp.simplify(dLdfr) != 0,
      f"f-channel surface weight dL/df_r != 0 (nonzero; e.g. diagonal "
      f"point: {sp.simplify(dLdfr.subs([(qq, 0), (wq, 0)]).doit())})")
# exact diagonal-point value for the record:
dLdfr_diag = sp.simplify(dLdfr.subs([(qq, 0), (wq, 0)]))
check("C5", sp.simplify(dLdfr_diag
      - (-(c/4)*r**2*sp.sin(th)*sp.diff(fq, r))) == 0,
      "dL/df_r|_diag = -(c/4) r^2 sin(th) f_r  (the f-channel carries "
      "interface momentum; the w-channel carries NONE)")

# ---------------------------------------------------------------------
# D. elementary flatness at the axis => w(axis) = 0
# ---------------------------------------------------------------------
w0, c2 = sp.symbols('w0 c2', real=True)
wax = w0 + c2*th**2
circ = 2*sp.pi*sp.sqrt(r**2*sp.sin(th)**2/(1 + wax)**2)   # circumference
sqg_thth = sp.sqrt(r**2*(1 + wax)**2)
prop = sp.integrate(sqg_thth.series(th, 0, 3).removeO(), (th, 0, th))
ratio = sp.simplify(sp.series(circ/(2*sp.pi*prop), th, 0, 3).removeO())
ratio0 = sp.limit(ratio, th, 0)
check("D1", sp.simplify(ratio0 - 1/(1 + w0)**2) == 0,
      "circumference/(2 pi proper radius) -> 1/(1+w0)^2 at the axis: "
      "ELEMENTARY FLATNESS FORCES w = 0 ON THE AXIS (exact)")
ratio_reg = sp.simplify(ratio.subs(w0, 0))
check("D2", sp.limit(ratio_reg, th, 0) == 1 and
      sp.simplify(sp.diff(ratio_reg, th).subs(th, 0)) == 0,
      "with w = c2 th^2 the deficit closes (ratio = 1 + O(th^2)): "
      "w ~ th^2 is the axis-regular shape class")

# ---------------------------------------------------------------------
# E. the w-dressed static sonic locus (q* degeneracy on the shaped class)
# ---------------------------------------------------------------------
fsym, frs, fts, ws, qs2 = sp.symbols('f f_r f_theta w q', real=True)
Wsym = (1 + ws)**2
A_s = fsym*r**2*Wsym*frs**2 + fts**2
B_s = frs*fts
Delta_w = fsym*r**2*Wsym*frs**2 - fts**2
check("E1", sp.simplify((A_s**2 - 4*fsym*r**2*Wsym*B_s**2) - Delta_w**2) == 0,
      "A^2 - 4 f r^2 W (f_r f_th)^2 = Delta_w^2, "
      "Delta_w = f r^2 (1+w)^2 f_r^2 - f_th^2 [P1 D-12 with w ON]")
qstar = 2*r**2*Wsym*B_s/A_s
Dq = r**2*Wsym - fsym*qstar**2
check("E2", sp.simplify(Dq - r**2*Wsym*Delta_w**2/A_s**2) == 0,
      "metric degeneracy on the q* branch: D(q*) = r^2 W Delta_w^2/A^2 "
      ">= 0, degenerate EXACTLY on Delta_w = 0: the static sonic locus "
      "is w-DRESSED multiplicatively, (1+w)^2 on the f_r^2 term")

print(f"\nGROUND ANCHORS: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
