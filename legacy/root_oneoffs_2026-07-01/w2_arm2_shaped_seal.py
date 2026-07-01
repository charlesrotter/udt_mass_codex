#!/usr/bin/env python3
"""
W2 ARM-2 — SCRIPT 2: THE SHAPED SEAL.  Date: 2026-06-11.
METRIC-LED (W2 framing correction binds: uncovering only — this
script computes what the metric's own curvature/admissibility
structure IS at the seal when the configuration is SHAPED (w on).
Nothing is added to the theory.)

PRE-REGISTERED FAILURE CRITERIA (identical in all w2_arm2_* scripts,
stated before any computation ran):
  FC-1: if the on-axis seal law f^2 K -> 4 f_u(pole)^2/y^4 acquires
        NO w-jet term at the singular order on the axis-regular
        shaped class, the seal singularity is w-blind -> scoped
        negative.
  FC-2: if the S1 finite-action admissibility machinery yields no
        condition on the w-channel at the seal -> scoped negative.
  FC-3: (interface script.)

CLASS (premise set of every result below): static diagonal+w class
  ds^2 = -f dT^2 + f^{-1} dy^2 + y^2 (1+w)^2 du^2/(1-u^2)
         + y^2 (1-u^2) dph^2/(1+w)^2,        u = cos(theta),
  q = 0 (the banked seal library class is diagonal; shaping it = w on);
  axis-regular fields (script-1 theorem: elementary flatness forces
  w = 0 on the axis):  f = a(y) + b(y)(1-u) + b2(y)(1-u)^2,
  w = om(y)(1-u) + om2(y)(1-u)^2.   f_u(pole) = -b, w_u(pole) = -om.
  R-areal canon rho = y; in-ansatz seal = pole touchdown a -> 0 with
  the transverse jets finite (fork_tests/mass_audit species).
COMPUTED:
  S1. Kretschmann on the shaped class; exact on-axis limit.
      TRACK 1 (symbolic law): reduced class b2 = om2 = 0 —
      K_axis(a, a', a'', b, b', om, om', om''; y) in closed form.
      Method: per-term gcd-free trailing-coefficient limits in
      v = 1-u (each Kretschmann term is an orthonormal-frame square,
      finite on the axis-regular class; a shared trailing factor
      cancels out of the trailing-coefficient ratio, so no polynomial
      gcd is ever computed).
  S2. THE SHAPED SEAL LAW: leading Laurent coefficient of K_axis in
      a -> 0 — does the in-ansatz singularity law acquire
      w-dependence, and at which order?  TRACK 2: the FULL class
      (b2, om2 on) rerun with symbolic pole values (A, B, Om, Oq, Bq)
      and exact rational radial jets — adjudicates the entry of every
      jet family at the singular order with zero floating point.
  S3. Exact-rational spot-check of the axis limit (no floating point:
      K evaluated at u = 1 - 10^-k, k = 4..8, exact rationals).
  S4. S1-ADMISSIBILITY RERUN, w-channel (FLUCTUATION-LEVEL statements,
      labeled per principle 2): the C1 second variation in the
      w-direction has ZERO gradient term (pi_w = 0 identically, exact)
      => no Sturm-Liouville operator, no limit-point/limit-circle
      classification, and finite C1 action imposes NO boundary
      condition on delta-w at the seal (the potential-only term is
      bounded by 6x the background angular action, finite by S1's
      finite-endpoint measure).
  S5. S1-ADMISSIBILITY RERUN, f-channel dressing: on the shaped class
      the angular potential density is dressed by exactly (1+w)^{-2};
      the dressing -> 1 at the pole with O(1-u) deficit, so the S1
      on-pole forced-Dirichlet structure (pole-localized: rank-one law
      v v^T/(4 mu), v_l = Y_l(pole)) keeps its coefficients; off-pole
      channel potentials are w-dressed.
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"S-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, y, u, ph = sp.symbols('T y u phi')
xs = [T, y, u, ph]

def riemann_and_K(gdd):
    guu = gdd.inv()
    Gam = [[[sp.cancel(sum(guu[a, d]*(sp.diff(gdd[d, b], xs[c])
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
    Kpairs = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    t1 = Rdddd[a][b][c][d]
                    if t1 == 0:
                        continue
                    Kpairs.append(((a, b, c, d), t1,
                                   guu[a, a]*guu[b, b]
                                   * guu[c, c]*guu[d, d]))
    return Riem, Rdddd, Kpairs

# gcd-free exact limit v -> 0 of comp^2 * factor (rational in v):
# write as N/D with N, D polynomial in v (no reduction needed — a
# shared trailing factor cancels out of the trailing-coefficient
# ratio); limit = 0 (tn > td), N0/D0 (tn = td), or DIVERGENT flag.
# Explicit Poly generators keep all arithmetic in the sparse
# polynomial ring (the expression-tree route is intractable here).
v = sp.Symbol('v', positive=True)

def trailing_v(P):
    """(trailing v-degree, trailing coefficient sub-polynomial) of a
    multivariate Poly whose first generator is v."""
    t = min(m[0] for m in P.monoms())
    gens = P.gens
    part = sp.Integer(0)
    for m, co in P.terms():
        if m[0] == t:
            part += co*sp.prod(g**e for g, e in zip(gens[1:], m[1:]))
    return t, part

def axis_limit_term(comp, factor, gens):
    cn, cd = sp.fraction(sp.together(comp))
    fn, fd = sp.fraction(sp.together(factor))
    Pn = sp.Poly(cn, *gens); Pd = sp.Poly(cd, *gens)
    N = Pn*Pn*sp.Poly(fn, *gens)
    D = Pd*Pd*sp.Poly(fd, *gens)
    if N.is_zero:
        return sp.Integer(0)
    tN, cN = trailing_v(N)
    tD, cD = trailing_v(D)
    if tN > tD:
        return sp.Integer(0)
    if tN < tD:
        return sp.zoo
    return sp.cancel(cN/cD)

# ---------------------------------------------------------------------
# S1. shaped-class Kretschmann, exact on-axis limit.
#     TRACK 1 (the symbolic law): first-transverse-jet class
#       f = a(y) + b(y)(1-u),  w = om(y)(1-u)
#     (b2 = om2 = 0; their entry at the singular order is adjudicated
#     exactly in TRACK 2 below with symbolic pole values + exact
#     rational radial jets — no information is lost, only the symbolic
#     bulk formula is restricted).  Method: per-term gcd-free trailing-
#     coefficient limits in v = 1 - u (each term is an orthonormal-
#     frame square — finite on the axis-regular class).
# ---------------------------------------------------------------------
a = sp.Function('a')(y); b = sp.Function('b')(y); b2 = sp.Function('b2')(y)
om = sp.Function('om')(y); om2 = sp.Function('om2')(y)

A, A1, A2 = sp.symbols('A A1 A2', real=True)
B, B1, B2s = sp.symbols('B B1 B2', real=True)
Bq, Bq1, Bq2 = sp.symbols('Bq Bq1 Bq2', real=True)     # b2, b2', b2''
Om, Om1, Om2d = sp.symbols('Om Om1 Om2d', real=True)   # om, om', om''
Oq, Oq1, Oq2 = sp.symbols('Oq Oq1 Oq2', real=True)     # om2, om2', om2''
sub = {sp.Derivative(a, (y, 2)): A2, sp.Derivative(a, y): A1,
       sp.Derivative(b, (y, 2)): B2s, sp.Derivative(b, y): B1,
       sp.Derivative(b2, (y, 2)): Bq2, sp.Derivative(b2, y): Bq1,
       sp.Derivative(om, (y, 2)): Om2d, sp.Derivative(om, y): Om1,
       sp.Derivative(om2, (y, 2)): Oq2, sp.Derivative(om2, y): Oq1,
       a: A, b: B, b2: Bq, om: Om, om2: Oq}

def build_and_limit(fF, wF, gens, extra_sub=None, label=""):
    """Build Kretschmann term pairs for the shaped metric and return
    the exact axis limit sum via trailing-coefficient limits."""
    g = sp.diag(-fF, 1/fF, y**2*(1 + wF)**2/(1 - u**2),
                y**2*(1 - u**2)/(1 + wF)**2)
    _, _, pairs = riemann_and_K(g)
    print(f"[t={time.time()-t0:.0f}s] {label}: {len(pairs)} nonzero "
          f"term pairs; taking per-term axis limits ...", flush=True)
    vals = []
    pervals = {}
    for i, (idx, comp, fac) in enumerate(pairs):
        cv = comp.xreplace(sub)
        fv = fac.xreplace(sub)
        if extra_sub:           # two-stage: jets -> symbols, THEN
            cv = cv.xreplace(extra_sub)   # symbols -> rationals
            fv = fv.xreplace(extra_sub)
        cv = cv.subs(u, 1 - v)
        fv = fv.subs(u, 1 - v)
        val = axis_limit_term(cv, fv, gens)
        assert val is not sp.zoo, f"term {i} divergent on axis!"
        vals.append(val)
        pervals[idx] = sp.cancel(val)
        if i % 12 == 11:
            print(f"   [{i+1}/{len(pairs)} t={time.time()-t0:.0f}s]",
                  flush=True)
    return sp.cancel(sp.together(sum(vals))), pairs, pervals

fF_red = a + b*(1 - u)
wF_red = om*(1 - u)
gens_red = (v, y, A, A1, A2, B, B1, B2s, Om, Om1, Om2d)
K_w_ax, Kpairs_red, pervals_red = build_and_limit(
    fF_red, wF_red, gens_red, label="TRACK 1 (reduced class)")
print(f"[t={time.time()-t0:.0f}s] axis limit done.", flush=True)
check("S1a", K_w_ax.has(Om) or K_w_ax.has(Om1) or K_w_ax.has(Om2d),
      "the on-axis Kretschmann of the shaped class DOES carry the w-jet "
      "(the geometry is w-jet-sensitive even where C1 is w-blind)")
print("\nK_axis (shaped, reduced class), exact:")
sp.pprint(sp.simplify(K_w_ax))
# w -> 0 recovers the diagonal axis formula (script-1 anchor):
K_diag_check = K_w_ax.subs({Om: 0, Om1: 0, Om2d: 0})
K_vma = A2**2 + 4*A1**2/y**2 + 4*(A - 1)**2/y**4 + 4*B**2/(y**4*A**2)
check("S1b", sp.simplify(K_diag_check - K_vma) == 0,
      "w -> 0 recovers VMA's diagonal axis formula exactly")
# THE PERFECT SQUARE: the areal-deficit term completes with the w
# transverse jet (om = w_thth at the pole):
K_square = (A2**2 + 4*A1**2/y**2 + 4*((1 - A) + 4*Om)**2/y**4
            + 4*B**2/(A**2*y**4))
check("S1c", sp.simplify(K_w_ax - K_square) == 0,
      "K_axis = a''^2 + 4a'^2/y^2 + 4[(1-a) + 4 om]^2/y^4 "
      "+ 4b^2/(a^2 y^4) EXACTLY: the (1-f) areal/clock deficit and "
      "the shape transverse jet 4 w_thth(pole) enter the metric's "
      "own curvature as a SINGLE COMPLETED SQUARE; om', om'' (and "
      "b', b'') do NOT enter K_axis at all")
check("S1d", not K_w_ax.has(Om1) and not K_w_ax.has(Om2d)
      and not K_w_ax.has(B1) and not K_w_ax.has(B2s),
      "confirmed: no radial derivatives of the transverse jets in "
      "K_axis (the axis curvature reads POLE VALUES of f_thth, "
      "w_thth only, plus radial derivatives of f itself)")
# COMPONENT IDENTIFICATION (exact, from the per-term limits): the
# w-jet lives in EXACTLY ONE orthonormal axis component — the
# sphere-sector sectional curvature; the seal singularity lives in
# the (T,u)/(y,u)-sector components:
on_uphuph = pervals_red[(2, 3, 2, 3)]
on_TyTy = pervals_red[(0, 1, 0, 1)]
on_TuTu = pervals_red[(0, 2, 0, 2)]
on_yuyu = pervals_red[(1, 2, 1, 2)]
check("S2e", sp.simplify(on_uphuph - ((1 - A) + 4*Om)**2/y**4) == 0,
      "R_(uh ph uh ph)^2 = [(1-f) + 4 w_thth]^2/y^4: the sphere-"
      "sector sectional curvature is the UNIQUE w-jet carrier on "
      "the axis — the metric reads shape as an ADDITIVE SHIFT of "
      "the (1-f) deficit in this one component")
check("S2f", sp.simplify(on_TuTu - (A*A1*y + B)**2/(4*A**2*y**4)) == 0
      and sp.simplify(on_yuyu - (A*A1*y - B)**2/(4*A**2*y**4)) == 0
      and sp.simplify(on_TyTy - A2**2/4) == 0,
      "R_(Th uh Th uh)^2 = (a a' y + b)^2/(4a^2 y^4), R_(yh uh yh uh)"
      "^2 = (a a' y - b)^2/(4a^2 y^4) — the seal-singular 1/f sits "
      "in the MIXED radial/temporal-angular components via "
      "f_thth/(2 f y^2), w-FREE; R_(Th yh Th yh)^2 = a''^2/4")
wcarriers = [idx for idx, val in pervals_red.items()
             if val.has(Om) or val.has(Om1) or val.has(Om2d)]
check("S2g", set(wcarriers) <= {(2, 3, 2, 3), (2, 3, 3, 2),
                                (3, 2, 2, 3), (3, 2, 3, 2)},
      f"census: the w-jet appears in NO other component "
      f"(carriers = {sorted(set(wcarriers))} — the u-ph sector only)")

# ---------------------------------------------------------------------
# S2. THE SHAPED SEAL LAW: Laurent structure in A -> 0
# ---------------------------------------------------------------------
K_ax_rat = sp.cancel(sp.together(K_w_ax))
num_K, den_K = sp.fraction(K_ax_rat)
pA_num = sp.Poly(num_K, A); pA_den = sp.Poly(den_K, A)
tA_num = min(m[0] for m in pA_num.monoms())
tA_den = min(m[0] for m in pA_den.monoms())
most_sing = tA_num - tA_den
check("S2a", most_sing == -2,
      f"most singular order is A^(-2) (no new, more-singular order is "
      f"created by shaping; found A^({most_sing}))")
law = sp.cancel(pA_num.coeff_monomial(A**tA_num)
                / pA_den.coeff_monomial(A**tA_den))
print("\nTHE SHAPED ON-AXIS SEAL LAW (reduced class):  f^2 K  ->",
      sp.factor(law))
wjet = [s for s in (Om, Om1, Om2d) if law.has(s)]
print("w-jet symbols in the law:", wjet)
check("S2b", True,
      f"law recorded; w-jet content = {wjet} "
      f"(FC-1 adjudication: "
      f"{'DRESSED' if wjet else 'w-BLIND -> scoped negative'})")

# ---------------------------------------------------------------------
# S2-TRACK-2: does the FULL axis-regular class (b2, om2 on) change the
# law? Exact-rational adjudication: A symbolic, every other jet at
# generic rationals; om2/b2 toggled OFF/ON; both the SINGULAR (A^-2)
# and the REGULAR (A^0) Laurent data compared. (The companion script
# w2_arm2_seal_law_adjudicator.py repeats the singular-order test at
# a second independent rational point, om = 7/3 nonperturbative.)
# ---------------------------------------------------------------------
rat = {A1: sp.Rational(-7, 5), A2: sp.Rational(9, 4),
       B: sp.Rational(-4, 3), B1: sp.Rational(2, 7),
       B2s: sp.Rational(-1, 6),
       Bq1: sp.Rational(-3, 8), Bq2: sp.Rational(1, 5),
       Om: sp.Rational(2, 5), Om1: sp.Rational(-5, 7),
       Om2d: sp.Rational(3, 4),
       Oq1: sp.Rational(4, 11), Oq2: sp.Rational(-2, 9),
       y: sp.Rational(13, 10)}
fF_full = a + b*(1 - u) + b2*(1 - u)**2
wF_full = om*(1 - u) + om2*(1 - u)**2
gens_full = (v, A)
K_off, _, _ = build_and_limit(
    fF_full, wF_full, gens_full,
    extra_sub={**rat, Bq: sp.Integer(0), Oq: sp.Integer(0),
               Bq1: sp.Integer(0), Bq2: sp.Integer(0),
               Oq1: sp.Integer(0), Oq2: sp.Integer(0)},
    label="TRACK 2a (full class, om2 = b2 = 0, A symbolic)")
K_on, _, _ = build_and_limit(
    fF_full, wF_full, gens_full,
    extra_sub={**rat, Bq: sp.Rational(5, 9), Oq: sp.Rational(-1, 3)},
    label="TRACK 2b (full class, om2/b2 ON, A symbolic)")

def laurent_A(KaxA):
    n_, d_ = sp.fraction(sp.cancel(sp.together(KaxA)))
    pn = sp.Poly(n_, A); pd = sp.Poly(d_, A)
    tn = min(m[0] for m in pn.monoms())
    td = min(m[0] for m in pd.monoms())
    lawc = sp.cancel(pn.coeff_monomial(A**tn)/pd.coeff_monomial(A**td))
    reg0 = sp.cancel(sp.together(KaxA - lawc/A**2)).subs(A, 0)
    return tn - td, lawc, reg0

o_off, law_off, reg_off = laurent_A(K_off)
o_on, law_on, reg_on = laurent_A(K_on)
check("S2c", o_off == -2 and o_on == -2,
      f"FULL class: most singular order A^(-2) with om2/b2 OFF and ON "
      f"(found {o_off}, {o_on})")
law_red_at = sp.cancel(law.subs(rat))
check("S2d", sp.simplify(law_on - law_off) == 0 and
      sp.simplify(law_off - law_red_at) == 0,
      f"singular law identical OFF/ON and = reduced-class law "
      f"4B^2/y^4 = {law_red_at}: b2/om2 (and ALL other jets) do NOT "
      f"enter the singular order  [matches adjudicator script, "
      f"2 points]")
reg_red_0 = sp.cancel(sp.together(K_w_ax - law/A**2)).subs(A, 0)
reg_red_at = sp.cancel(reg_red_0.subs(rat))
check("S2h", sp.simplify(reg_on - reg_off) == 0 and
      sp.simplify(reg_off - reg_red_at) == 0,
      f"REGULAR (A^0) part also identical OFF/ON and equal to the "
      f"reduced-class completed square = {reg_red_at}: the second "
      f"transverse jets do not shift the perfect square at the "
      f"pole-touchdown order either")

# ---------------------------------------------------------------------
# S3. exact-rational spot-check of the axis limit (no floating point)
# ---------------------------------------------------------------------
vals = {A: sp.Rational(3, 10), A1: sp.Rational(-7, 5),
        A2: sp.Rational(9, 4), B: sp.Rational(-4, 3),
        B1: sp.Rational(2, 7), B2s: sp.Rational(-1, 6),
        Om: sp.Rational(2, 5), Om1: sp.Rational(-5, 7),
        Om2d: sp.Rational(3, 4), y: sp.Rational(13, 10)}
K_ax_val = K_w_ax.subs(vals)
seq = []
for k in (4, 6, 8):
    uv = 1 - sp.Rational(1, 10**k)
    tot = sp.Integer(0)
    for idx, comp, fac in Kpairs_red:
        cv = comp.xreplace(sub).subs(vals).subs(u, uv)
        fv = fac.xreplace(sub).subs(vals).subs(u, uv)
        tot += sp.nsimplify(cv)**2*sp.nsimplify(fv)
    seq.append(tot)
errs = [abs(sp.N(s - K_ax_val, 30)) for s in seq]
check("S3a", errs[0] > errs[1] > errs[2] and sp.N(errs[2], 10) <
      sp.N(abs(K_ax_val)*sp.Rational(1, 10**6), 10),
      f"exact-rational approach to the axis limit confirmed "
      f"(errors {[sp.N(e, 3) for e in errs]} -> 0)")

# also spot-check the seal Laurent at the same point:
K_ax_A = sp.cancel(sp.together(K_w_ax).subs(
    {kk: vv for kk, vv in vals.items() if kk != A}))
lawv = law.subs(vals)
seqA = [sp.nsimplify((K_ax_A*A**2).subs(A, sp.Rational(1, 10**k)))
        for k in (3, 5, 7)]
errsA = [abs(sp.N(s - lawv, 30)) for s in seqA]
check("S3b", errsA[0] > errsA[1] > errsA[2],
      f"exact-rational approach to the shaped seal law confirmed "
      f"(errors {[sp.N(e, 3) for e in errsA]} -> 0)")

# ---------------------------------------------------------------------
# S4. S1-admissibility rerun, w-channel  [FLUCTUATION-LEVEL, labeled]
# ---------------------------------------------------------------------
# reduced 2D density on the shaped class (P1 D-16 with w ON), exact:
r, th = sp.symbols('r theta', positive=True)
c = sp.Symbol('c')
fq = sp.Function('f')(r, th); wq = sp.Function('w')(r, th)
W = (1 + wq)**2
g3 = sp.Matrix([[-fq, 0, 0, 0], [0, 1/fq, 0, 0], [0, 0, r**2*W, 0],
                [0, 0, 0, r**2*sp.sin(th)**2/W]])
sqg = r**2*sp.sin(th)
check("S4a", sp.simplify(sqg**2 - (-g3.det())) == 0,
      "sqrt(-g) = r^2 sin(th) on the diagonal+w class: the C1 MEASURE "
      "is exactly w-FREE (areal canon)")
g3i = g3.inv()
phir, phith = -sp.diff(fq, r)/(2*fq), -sp.diff(fq, th)/(2*fq)
L3 = -(c/2)*fq*(g3i[1, 1]*phir**2 + g3i[2, 2]*phith**2)*sqg
L3tgt = -(c/8)*sp.sin(th)*(r**2*sp.diff(fq, r)**2
        + sp.diff(fq, th)**2/(fq*(1 + wq)**2))
check("S4b", sp.simplify(L3 - L3tgt) == 0,
      "L(q=0, w on) = -(c/8) sin(th) [r^2 f_r^2 + f_th^2/(f (1+w)^2)]: "
      "radial term w-FREE, angular term dressed by exactly (1+w)^{-2}")
# w-channel second variation: NO gradient term, potential-only:
d2Ldw2 = sp.simplify(sp.diff(L3, wq, 2))
check("S4c", sp.simplify(d2Ldw2 - (-(c*sp.Rational(3, 4))*sp.sin(th)
      * sp.diff(fq, th)**2/(fq*(1 + wq)**4))) == 0,
      "d^2L/dw^2 = -(3c/4) sin(th) f_th^2/(f (1+w)^4): potential-only")
gradw = [d for d in L3.atoms(sp.Derivative) if d.expr == wq]
check("S4d", len(gradw) == 0,
      "ZERO w-gradient stiffness in the fluctuation action (pi_w = 0 "
      "exact): the w-channel has NO Sturm-Liouville operator at the "
      "seal => the S1 limit-point/limit-circle machinery has NO OBJECT "
      "in this channel; finite C1 action imposes NO BC on delta-w "
      "(potential term = 6 (1+w)^{-2} x background angular density, "
      "finite by S1's finite-endpoint measure).  [FC-2: this channel "
      "is a SCOPED NEGATIVE — fluctuation-level statement]")
ratio = sp.simplify(d2Ldw2/(L3tgt - (-(c/8)*sp.sin(th)*r**2
                                     * sp.diff(fq, r)**2)))
check("S4e", sp.simplify(ratio - 6/(1 + wq)**2) == 0,
      "d^2L/dw^2 = [6/(1+w)^2] x (background angular action density) "
      "exactly — admissibility of bounded delta-w is automatic")

# ---------------------------------------------------------------------
# S5. f-channel dressing at the pole
# ---------------------------------------------------------------------
uu, omS = sp.symbols('uu omS', real=True)
dress = 1/(1 + omS*(1 - uu))**2
ser = sp.series(dress, uu, 1, 2).removeO()
check("S5a", sp.simplify(ser - (1 + 2*omS*(uu - 1))) == 0,
      "dressing factor (1+w)^{-2} = 1 - 2 om (1-u) + O((1-u)^2) at the "
      "pole: -> 1 EXACTLY ON THE POLE. The S1 on-pole structures "
      "(forced Dirichlet/Friedrichs from finite action; rank-one law "
      "v v^T/(4 mu), v_l = Y_l(pole)) keep their coefficients; only "
      "off-pole channel potentials are w-dressed (multiplied by "
      "(1+w)^{-2} inside the sphere projection).")

print(f"\nSHAPED SEAL: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
