#!/usr/bin/env python3
"""
W3 — THE CROSS-BLOCK RE-POSE: SCRIPT 1 (GROUND).  Date: 2026-06-12.
Driver: W3 agent.  Declared METRIC-LED (w_stiffness_push_declaration.md
W3 section; Charles's test-both protocol standing).

INDEPENDENT GROUNDING of VW2's cross-block discovery (registry #26
load-bearing caveat), from my OWN covariant construction (tie ->
metric -> inverse -> density; the banked closed form is a CHECK, not
an input), plus the exact structure W3 needs that VW2 did not compute:
the full dressed 3x3 quadratic form (both elimination orders), the
field-chart family law (off-shell Hessian non-tensoriality made
exact), the D_cell completion branch, the q-only/exact-q* consistency,
the seal-coefficient limits, and the time-row parity theorem (W_A
survives the completion).

PRE-REGISTERED FAILURE CRITERIA (hypothesis discipline; stated before
any computation ran; the HOPED-FOR outcome downstream is "the
completed problem selects the theta-dial"):
  F-1 If every non-forced seal channel of the dressed operator remains
      limit-circle/regular with both branches action-finite, the
      completed class supplies NO theta-selector -> first-class
      negative (owned by script 2).
  F-2 If the background tadpoles T_w, T_q are nonzero on the S1
      backgrounds AND the dressed coefficients depend on the field
      chart (the (alpha,beta) law below), then NO chart-invariant
      selector exists on the C1-only branch; any candidate h would be
      chart-conditional and cannot be banked as derived.
  F-3 If on the C1 + D_cell branch the cross blocks vanish
      identically, the dressing is zero there and S1/S2/theta-dial
      stand VERBATIM on that branch (the re-pose upholds, not
      replaces, the banked record).
Each of F-1..F-3 is a recordable outcome, not a failure of the push.

CONVENTIONS (binding): R-areal canon rho = r; signature (-,+,+,+);
P1 metric class g = diag(-f, 1/f, r^2 W, r^2 sin^2/W) + g_rtheta = q,
W = (1+w)^2; tie phi = -(1/2) ln f (R-stat, corpus-ranked; the tie
fork is NOT exercised here -- noted, not used); C1 density
L = -(c/2) f g^{ab} phi_a phi_b sqrt(-g).  Exact sympy throughout; jet
variables are SYMBOLS (the density is pointwise-algebraic in all
fields and first-jet in f only, so the Hessian in jet symbols IS the
second variation's coefficient table; no IBP is needed for any block
involving delta-w or delta-q since they never appear differentiated).
Wp = 1 + w is used as the shape variable (affine shift of w: identical
derivatives, d/dw = d/dWp); sn = sin(theta) > 0 on the open polar
interval (a positive symbol -- no theta-derivatives are ever taken).
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"W3G-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

r = sp.Symbol('r', positive=True)
sn = sp.Symbol('sn', positive=True)                 # sin(theta) in (0,1]
c = sp.Symbol('c')
f = sp.Symbol('f', positive=True)
fr, fth, fph, fT = sp.symbols('f_r f_th f_ph f_T', real=True)
q = sp.Symbol('q', real=True)
Wp = sp.Symbol('Wp', positive=True)                 # Wp = 1 + w

# ---------------------------------------------------------------
# A. my own covariant construction (static class, q on, w on)
# ---------------------------------------------------------------
W2_ = Wp**2
g4 = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1/f, q, 0],
    [0, q, r**2*W2_, 0],
    [0, 0, 0, r**2*sn**2/W2_]])
g4i = g4.inv()
detg = g4.det()
sqrtmg = sp.sqrt(sp.simplify(-detg))
phia = sp.Matrix([0, -fr/(2*f), -fth/(2*f), -fph/(2*f)])
K = sum(g4i[i, j]*phia[i]*phia[j] for i in range(4) for j in range(4))
L = sp.simplify(-(c/2)*f*K*sqrtmg)

D2 = r**2*W2_ - f*q**2
A_ = f*r**2*W2_*fr**2 + fth**2
Lclosed = -(c/8)*r*sn*(A_ - 2*f*q*fr*fth)/(Wp*f*sp.sqrt(D2))
check("A1", sp.simplify(sp.expand(L.subs(fph, 0) - Lclosed)) == 0,
      "own covariant construction reproduces the banked P1 closed "
      "form on the axisymmetric slice (f_ph = 0) -- independent route")
Lphi_atom = sp.simplify(L - L.subs(fph, 0))
check("A2", sp.simplify(Lphi_atom
      - (-(c/8))*Wp*fph**2*sp.sqrt(D2)/(f*sn*r)) == 0,
      "phi-gradient atom = -(c/8) Wp sqrt(D2) f_ph^2/(f sn r) "
      "(carries (1+w) with the OPPOSITE orientation to the theta atom)")

# ---------------------------------------------------------------
# B. the static Hessian blocks at q = 0 (w kept ON, then w = 0)
# ---------------------------------------------------------------
jets_f = [f, fr, fth]
L0 = L.subs(fph, 0)
def H(a, b_):
    return sp.simplify(sp.diff(L0, a, b_).subs(q, 0))
# VW2's four quoted entries (registry #26 / w2 results headline 6);
# d/dw == d/dWp:
Lww = H(Wp, Wp)
check("B1", sp.simplify(Lww + sp.Rational(3, 4)*c*sn*fth**2/(f*Wp**4)) == 0,
      "L_ww = -(3c/4) sn f_th^2/(f Wp^4)  (potential-only w-w block)")
ang_bg = -(c/8)*sn*fth**2/(f*Wp**2)
check("B2", sp.simplify(Lww - 6*ang_bg/Wp**2) == 0,
      "L_ww = [6/(1+w)^2] x background angular density (VW2 E1c)")
Lwfth = H(Wp, fth)
check("B3", sp.simplify(Lwfth - c*sn*fth/(2*f*Wp**3)) == 0,
      "L_wfth = (c/2) sn f_th/(f(1+w)^3)  (VW2 E3a, independent)")
Lwq = H(Wp, q)
check("B4", sp.simplify(Lwq + c*sn*fr*fth/(2*Wp**3)) == 0,
      "L_wq = -(c/2) sn f_r f_th/(1+w)^3  (VW2 E3c, independent)")
check("B5", sp.simplify(H(Wp, fr)) == 0, "L_wfr = 0 (VW2 E3b)")
Lwf = H(Wp, f); Lqq = H(q, q); Lqf = H(q, f)
Lqfr = H(q, fr); Lqfth = H(q, fth)
Lff = H(f, f); Lffr = H(f, fr); Lffth = H(f, fth)
Lfrfr = H(fr, fr); Lfrfth = H(fr, fth); Lfthfth = H(fth, fth)
check("B6", sp.simplify(Lqq + (c/8)*sn*(f*fr**2*W2_*r**2 + fth**2)
      / (Wp**4*r**2)) == 0,
      "L_qq = -(c/8) sn (f W r^2 f_r^2 + f_th^2)/(Wp^4 r^2) (exact)")
Tw = sp.simplify(sp.diff(L0, Wp).subs(q, 0))
Tq = sp.simplify(sp.diff(L0, q).subs(q, 0))
check("B7", sp.simplify(Tw - c*sn*fth**2/(4*f*Wp**3)) == 0 and
      sp.simplify(Tq - c*sn*fr*fth/(4*Wp**2)) == 0,
      "tadpoles: T_w = +(c/4) sn f_th^2/(f Wp^3), "
      "T_q = +(c/4) sn f_r f_th/Wp^2 (both NONZERO wherever "
      "f_th != 0: the S1 backgrounds are OFF-SHELL in the released "
      "directions -- pde_p1/registry #21; w_stiffness records the "
      "same pair with the opposite overall orientation convention)")
# THE TADPOLE-GRADIENT IDENTITY:
ok = True
for X_, TX in ((Wp, Tw), (q, Tq)):
    for j in jets_f:
        ok &= sp.simplify(H(X_, j) - sp.diff(TX, j)) == 0
check("B8", ok,
      "b_X[jet] == d T_X / d jet for X in {w,q}, jet in {f,f_r,f_th}: "
      "THE CROSS BLOCKS ARE EXACTLY THE f-JET GRADIENTS OF THE "
      "TADPOLES (the dressing exists iff the tadpoles are unfixed)")
bad = [d for d in L.atoms(sp.Derivative)]
check("B9", len(bad) == 0,
      "jet-symbol L contains no Derivative atoms; w and q enter as "
      "VALUES only => their fluctuations are pointwise-algebraic at "
      "every order (no IBP, no SL operator on delta-w/delta-q)")

# ---------------------------------------------------------------
# C. delta-w-only Schur elimination (variant V-w; w-chart), w bg -> 0
# ---------------------------------------------------------------
at0 = lambda e: sp.simplify(e.subs(Wp, 1))
bw = sp.Matrix([at0(H(Wp, j)) for j in jets_f])     # (f, fr, fth)
Lww0 = at0(Lww)
Hff = sp.Matrix(3, 3, lambda i, j: at0(H(jets_f[i], jets_f[j])))
Hw = sp.simplify(Hff - (bw*bw.T)/Lww0)
check("C1", sp.simplify(Hw[2, 2] - c*sn/(12*f)) == 0,
      "delta-w-only: [fth,fth] = -(c/4) sn/f -> +(c/12) sn/f "
      "(VW2's FLIP, my own elimination)")
check("C2", sp.simplify(Hw[0, 2] - c*sn*fth/(12*f**2)) == 0 and
      sp.simplify(Hw[0, 0] + c*sn*fth**2/(6*f**3)) == 0 and
      sp.simplify(Hw[1, 1] + c*sn*r**2/4) == 0 and
      sp.simplify(Hw[0, 1]) == 0 and sp.simplify(Hw[1, 2]) == 0,
      "delta-w-only dressed 3x3 (NEW, exact): [f,fth] = +(c/12)sn "
      "fth/f^2, [f,f] = -(c/6)sn fth^2/f^3, radial row UNTOUCHED "
      "([fr,fr] = -(c/4)sn r^2, [f,fr] = [fr,fth] = 0)")
df, dfr, dfth = sp.symbols('df dfr dfth')
vv = [df, dfr, dfth]
formC1 = sp.expand(sum(Hff[i, j]*vv[i]*vv[j]
                       for i in range(3) for j in range(3)))
formW = sp.expand(sum(Hw[i, j]*vv[i]*vv[j]
                      for i in range(3) for j in range(3)))
gsl = fth/f
sq1 = -(c/4)*sn*(r**2*dfr**2 + (dfth - gsl*df)**2/f)
check("C3", sp.simplify(formC1 - sp.expand(sq1)) == 0,
      "frozen-class form = -(c/4)sn[r^2 dfr^2 + (dfth - (fth/f)df)^2/f]"
      " (the S1/S2 perspective-convexity perfect square, my variables)")
sq2 = sq1 + (c/12)*(sn/f)*(2*dfth - gsl*df)**2
check("C4", sp.simplify(formW - sp.expand(sq2)) == 0,
      "dressed form (V-w) = frozen + (c/12)(sn/f)(2 dfth - (fth/f)df)^2"
      " EXACTLY (the elimination adds back a single rank-one square "
      "with coefficient -1/3 of the frozen angular square's)")

# ---------------------------------------------------------------
# D. joint (delta-w, delta-q) Schur (variant V-wq; w-chart) + q-only
#    + the exact q* consistency
# ---------------------------------------------------------------
bq = sp.Matrix([at0(H(q, j)) for j in jets_f])
Lqq0 = at0(Lqq); Lwq0 = at0(Lwq)
M2x2 = sp.Matrix([[Lww0, Lwq0], [Lwq0, Lqq0]])
Bv = sp.Matrix.hstack(bw, bq)                  # 3x2
Madj = sp.Matrix([[Lqq0, -Lwq0], [-Lwq0, Lww0]])
detM = sp.simplify(M2x2.det())
Hwq = sp.simplify(Hff - (Bv*Madj*Bv.T)/detM)
X = f*r**2*fr**2          # the sonic pair (w = 0 face)
Y = fth**2
Dlt = X - Y               # Delta_w at w = 0
DMw = 5*X - 3*Y           # the V-wq (w-chart) Schur-degeneracy locus
check("D1", sp.simplify(detM
      - c**2*sn**2*fth**2*(3*Y - 5*X)/(32*f*r**2)) == 0,
      "det M = (c^2 sn^2 fth^2/(32 f r^2)) (3Y - 5X): the joint "
      "algebraic block degenerates on D_M^w := 5X - 3Y = 0 (w-chart)")
check("D2", sp.simplify(Hwq[2, 2] - (c*sn/(4*f))*Dlt/DMw) == 0,
      "JOINT [fth,fth] = (c sn/(4f)) Delta_w/D_M^w -- numerator "
      "EXACTLY Delta_w = f r^2 fr^2 - fth^2 (VW2's E4j, exact closed "
      "form with the denominator now pinned)")
check("D3", sp.simplify(Hwq[1, 1] + (c*sn*r**2/4)*(5*X + 3*Y)/DMw) == 0
      and sp.simplify(Hwq[1, 2] - (c*sn*r**2/2)*fr*fth/DMw) == 0,
      "JOINT radial row IS dressed: [fr,fr] = -(c/4)sn r^2 (5X+3Y)/D_M,"
      " [fr,fth] = +(c/2)sn r^2 fr fth/D_M (radial stiffness flips "
      "sign across D_M = 0)")
discC1 = sp.simplify(Hff[1, 2]**2 - Hff[1, 1]*Hff[2, 2])
discW = sp.simplify(Hw[1, 2]**2 - Hw[1, 1]*Hw[2, 2])
discWQ = sp.simplify(Hwq[1, 2]**2 - Hwq[1, 1]*Hwq[2, 2])
check("D4", sp.simplify(discC1 + c**2*sn**2*r**2/(16*f)) == 0 and
      sp.simplify(discW - c**2*sn**2*r**2/(48*f)) == 0,
      "character: frozen class ELLIPTIC (disc = -c^2sn^2r^2/16f < 0); "
      "V-w HYPERBOLIC everywhere (disc = +c^2sn^2r^2/48f > 0)")
check("D5", sp.simplify(discWQ - (c**2*sn**2*r**2/(16*f))*(X + Y)/DMw)
      == 0,
      "V-wq: disc = (c^2sn^2r^2/16f)(X+Y)/D_M -- HYPERBOLIC where "
      "D_M > 0, ELLIPTIC where D_M < 0: the joint variant CHANGES "
      "CHARACTER on its Schur locus, not on Delta_w")
Hq = sp.simplify(Hff - (bq*bq.T)/Lqq0)
Aq = X + Y
check("D6", sp.simplify(Hq[2, 2] - (c*sn/(4*f))*Dlt/Aq) == 0 and
      sp.simplify(Hq[1, 1] + (c*sn*r**2/4)*Dlt/Aq) == 0,
      "V-q: [fth,fth] = (csn/4f) Delta_w/A, [fr,fr] = -(csn r^2/4) "
      "Delta_w/A, A = X+Y > 0: SAME Delta_w numerator, denominator "
      "positive-definite (no interior Schur locus)")
discQ = sp.simplify(Hq[1, 2]**2 - Hq[1, 1]*Hq[2, 2])
check("D7", sp.simplify(discQ - c**2*sn**2*r**2/(16*f)) == 0,
      "V-q disc = +c^2sn^2r^2/16f EXACTLY (= minus the frozen disc; "
      "the [fr,fth] cross entry +(c/2)sn r^2 fr fth/A keeps the "
      "symbol nondegenerate even ON Delta_w = 0): V-q is HYPERBOLIC "
      "EVERYWHERE -- the Class-B character at fluctuation level "
      "[driver note: my hand expectation Delta_w^2/A^2 dropped the "
      "cross entry; corrected by the machine]")
qstar = 2*r**2*W2_*fr*fth/A_
Lstar = sp.simplify(L0.subs(q, qstar))
Dlt_w = f*r**2*W2_*fr**2 - fth**2
Lstar_sub = -(c/8)*sn*Dlt_w/(f*W2_)
diffq = sp.simplify(sp.factor(Lstar - Lstar_sub))
spots = [{f: sp.Rational(1, 2), fr: 1, fth: sp.Rational(1, 10), r: 2,
          Wp: 1, sn: sp.Rational(1, 2)},
         {f: sp.Rational(1, 3), fr: 2, fth: sp.Rational(1, 7), r: 3,
          Wp: sp.Rational(6, 5), sn: sp.Rational(3, 4)}]
check("D8", all(sp.simplify(diffq.subs(sub)) == 0 for sub in spots),
      "EXACT q-eliminated density L(q*) = -(c/8) sn Delta_w/(f(1+w)^2)"
      " on the subsonic branch (rational spot checks; the P1 'perfect"
      " square flip' = the Class-B hyperbolic density, "
      "fluctuation-free derivation)")

# ---------------------------------------------------------------
# E. THE FIELD-CHART FAMILY (off-shell non-tensoriality, exact)
# ---------------------------------------------------------------
al, be = sp.symbols('alpha beta', real=True)        # w = al*v + be*v^2/2
Lvv = sp.simplify(al**2*Lww0 + be*at0(Tw))
bv = al*bw
Hv = sp.simplify(Hff - (bv*bv.T)/Lvv)
law = sp.simplify(Hv[2, 2] - (c*sn/(4*f))*(al**2 + be)/(3*al**2 - be))
check("E1", law == 0,
      "delta-v-only dressed [fth,fth] = (c/4)(sn/f)(al^2+be)/(3al^2-be)"
      " for ANY chart w = al v + (be/2) v^2 + ...: the dressing is "
      "CHART-CONDITIONAL because the expansion point is off-shell "
      "(T_w != 0) -- Hessians are non-tensorial off criticality. "
      "w-chart (1,0): +c/12; exp-chart W=e^{2s'}, i.e. (1,1): +c/4; "
      "be = -al^2: 0; be in (3al^2, oo) or (-oo, -al^2): NEGATIVE "
      "(no flip). F-2 PREMISE ESTABLISHED.")
Lss = sp.simplify(Lww0 + at0(Tw))                   # al=be=1
Ms = sp.Matrix([[Lss, Lwq0], [Lwq0, Lqq0]])
detMs = sp.simplify(Ms.det())
check("E2", sp.simplify(detMs
      - c**2*sn**2*fth**2*(Y - 3*X)/(16*f*r**2)) == 0,
      "exp-chart joint block: det ~ (Y - 3X): the Schur locus is "
      "Y = 3X -- EXACTLY the angular audit's 'canon-true areal "
      "scheme' twin locus (angular_completeness degeneracy row), now "
      "derived as the chart-image of the same off-shell ambiguity")
Msadj = sp.Matrix([[Lqq0, -Lwq0], [-Lwq0, Lss]])
Hwq_s = sp.simplify(Hff - (Bv*Msadj*Bv.T)/detMs)
check("E3", sp.simplify(Hwq_s[2, 2] - (c*sn/(4*f))*Dlt/(3*X - Y)) == 0,
      "exp-chart JOINT [fth,fth] = (csn/4f) Delta_w/(3X - Y): the "
      "NUMERATOR Delta_w is CHART-ROBUST (w-chart and exp-chart); "
      "only the denominator (Schur locus) moves")
aw, bw_, aq2, bq_ = sp.symbols('a_w b_w a_q b_q', real=True)
Lvv_w = aw**2*Lww0 + bw_*at0(Tw)
Lvv_q = aq2**2*Lqq0 + bq_*at0(Tq)
Lvq = aw*aq2*Lwq0
Mg = sp.Matrix([[Lvv_w, Lvq], [Lvq, Lvv_q]])
Mgadj = sp.Matrix([[Lvv_q, -Lvq], [-Lvq, Lvv_w]])
detMg = sp.simplify(sp.expand(Mg.det()))
Bg = sp.Matrix.hstack(aw*bw, aq2*bq)
Hg22 = sp.cancel(sp.together(
    Hff[2, 2] - sp.expand((Bg*Mgadj*Bg.T)[2, 2])/detMg))
num, den = sp.fraction(Hg22)
quo, rem = sp.div(sp.Poly(sp.expand(num), fth),
                  sp.Poly(f*r**2*fr**2 - fth**2, fth))
remx = sp.simplify(rem.as_expr())
print("   generic-chart joint [fth,fth] numerator mod Delta_w: "
      f"remainder = {remx}")
check("E4", sp.simplify(remx - 2*bq_*c*fr*fth*r**2*sn*(aw**2 + bw_))
      == 0 and sp.simplify(remx.subs(bq_, 0)) == 0,
      "GENERIC two-chart joint elimination: [fth,fth] numerator mod "
      "Delta_w has remainder 2 b_q c fr fth r^2 sn (a_w^2 + b_w): "
      "the Delta_w turning surface is INVARIANT UNDER ALL w-CHARTS "
      "(b_q = 0 => exact divisibility for every a_w, b_w) and is "
      "shifted only by QUADRATIC reparameterizations of the "
      "g_rtheta METRIC COMPONENT itself (b_q != 0), for which no "
      "corpus-used alternative chart exists. Scoped invariance: "
      "Delta_w is the chart-robust content on the corpus's charts; "
      "the denominator (locus, magnitude) is not chart-robust "
      "[driver note: my hand expectation 'all charts' was corrected "
      "by the machine to 'all w-charts at metric-component q']")

# ---------------------------------------------------------------
# F. seal-coefficient limits (the [f,f] 1/mu law dressing ratios)
# ---------------------------------------------------------------
ratio_w = sp.simplify(sp.limit((Hw[0, 0]/Hff[0, 0]), fth, 0))
ratio_wq = sp.simplify(sp.limit((Hwq[0, 0]/Hff[0, 0]), fth, 0))
Hs_only = sp.simplify(Hff - (bw*bw.T)/Lss)
ratio_s_only = sp.simplify(sp.limit(Hs_only[0, 0]/Hff[0, 0], fth, 0))
ratio_s_joint = sp.simplify(sp.limit((Hwq_s[0, 0]/Hff[0, 0]), fth, 0))
print(f"   seal [f,f] dressing ratios (fth->0 limit): V-w {ratio_w}, "
      f"V-wq {ratio_wq}, exp-chart only {ratio_s_only}, "
      f"exp-chart joint {ratio_s_joint}")
check("F1", (ratio_w, ratio_wq, ratio_s_only, ratio_s_joint) ==
      (sp.Rational(2, 3), sp.Rational(6, 5), sp.Rational(1, 2),
       sp.Rational(7, 6)),
      "the vv^T/(4 mu) seal law survives with renormalized "
      "coefficient: 2/3 (V-w), 6/5 (V-wq), 1/2 (exp V-w), 7/6 (exp "
      "V-wq) -- POSITIVE in every carried variant: the S1 forced "
      "Dirichlet's divergence mechanism is intact (magnitude "
      "chart-conditional, sign robust on the carried charts) "
      "[driver note: my hand value 4/5 for V-wq had a sign slip; "
      "the machine says 6/5 and the hand rederivation now agrees]")
ratio_gen = sp.simplify(sp.limit(Hv[0, 0]/Hff[0, 0], fth, 0))
check("F2", sp.simplify(ratio_gen - (2*al**2 - be)/(3*al**2 - be)) == 0,
      "generic-chart seal ratio = (2al^2-be)/(3al^2-be): vanishes "
      "only on the measure-zero chart be = 2al^2 (caveat recorded); "
      "Dirichlet-forcing needs only a NONZERO coefficient (action "
      "divergence is sign-blind)")

# ---------------------------------------------------------------
# G. THE D_CELL BRANCH (standing completion fork, #24): test-both
# ---------------------------------------------------------------
Dcell = -(c/4)*sn*((Wp - 1)*fth**2/f + q*fr*fth)
Ltot = L0 + Dcell
pt = [(q, 0), (Wp, 1)]
Tw_t = sp.simplify(sp.diff(Ltot, Wp).subs(pt))
Tq_t = sp.simplify(sp.diff(Ltot, q).subs(pt))
check("G1", Tw_t == 0 and Tq_t == 0,
      "C1 + D_cell: both tadpoles vanish identically on EVERY "
      "diagonal background (w_stiffness #24's defining property, my "
      "conventions: D_cell = -(c/4)sn[w fth^2/f + q fr fth])")
ok = True
for Xf in (Wp, q):
    for j in jets_f:
        ok &= sp.simplify(sp.diff(Ltot, Xf, j).subs(pt)) == 0
check("G2", ok,
      "C1 + D_cell: ALL six cross blocks (delta-w, delta-q) x "
      "(delta-f jets) vanish IDENTICALLY on diagonal backgrounds -- "
      "immediate from B8 (b = grad_jet T and T == 0 as a functional "
      "identity in f)")
ok = True
for a_, b_ in [(Wp, Wp), (Wp, q), (q, q)]:
    e1 = sp.simplify(sp.diff(Ltot, a_, b_).subs(pt))
    e0 = sp.simplify(sp.diff(L0, a_, b_).subs([(q, 0)]).subs(Wp, 1))
    ok &= sp.simplify(e1 - e0) == 0
for i in range(3):
    for j in range(3):
        e1 = sp.simplify(sp.diff(Ltot, jets_f[i], jets_f[j]).subs(pt))
        ok &= sp.simplify(e1 - Hff[i, j]) == 0
check("G3", ok,
      "C1 + D_cell: the (w,q) algebraic block and the f-block are "
      "both UNCHANGED (D_cell is linear in (w,q) and vanishes with "
      "them) => THE DRESSING IS IDENTICALLY ZERO ON THIS BRANCH: "
      "S1's frozen-delta-w operator is EXACT, not approximate; "
      "registry #26's caveat dissolves on the D_cell branch (F-3)")

# ---------------------------------------------------------------
# H. time-row parity: the completion never touches the W_A sector
# ---------------------------------------------------------------
a_, b2, p2 = sp.symbols('a_Tr b_Tth p_Tph', real=True)
g4t = sp.Matrix([
    [-f, a_, b2, p2],
    [a_, 1/f, q, 0],
    [b2, q, r**2*W2_, 0],
    [p2, 0, 0, r**2*sn**2/W2_]])
g4ti = g4t.inv()
detgt = g4t.det()
phiat = sp.Matrix([-fT/(2*f), -fr/(2*f), -fth/(2*f), -fph/(2*f)])
Kt = sum(g4ti[i, j]*phiat[i]*phiat[j]
         for i in range(4) for j in range(4))
Lt = -(c/2)*f*Kt*sp.sqrt(sp.simplify(-detgt))
statpt = [(q, 0), (a_, 0), (b2, 0), (p2, 0), (fT, 0), (fph, 0), (Wp, 1)]
ok = True
for Xf in (Wp, q):
    for Yf in (fT, a_, b2, p2):
        e = sp.simplify(sp.diff(Lt, Xf, Yf).subs(statpt))
        ok &= (e == 0)
check("H1", ok,
      "FULL TIME ROW ON: all eight cross blocks (delta-w, delta-q) x "
      "(delta-f_T, delta-g_Tr, delta-g_Tth, delta-g_Tph) VANISH at "
      "static diagonal backgrounds (T-parity + zeroth-jet): the "
      "static-block elimination and the time-row elimination COMMUTE "
      "-- the derived W_A time weight (measure fork) is UNTOUCHED by "
      "the completion; omega^2 = -sigma keeps its meaning")
ok = True
for Xf in (Wp, q):
    e = sp.simplify(sp.diff(Lt, Xf, fph).subs(statpt))
    ok &= (e == 0)
e2 = sp.simplify(sp.diff(Lt, fph, fph).subs(statpt)
                 - sp.diff(L, fph, fph).subs([(q, 0), (fph, 0)])
                 .subs(Wp, 1))
check("H2", ok and sp.simplify(e2) == 0,
      "m != 0 scope: b_w[f_ph] = b_q[f_ph] = 0 on axisymmetric "
      "backgrounds and [f_ph,f_ph] is NOT dressed by (delta-w, "
      "delta-q): the m^2 centrifugal entry keeps its frozen "
      "coefficient in every dressed variant (the axial u,v channels "
      "-- registry #20's dpv flip -- are OUTSIDE this completion and "
      "are carried as a named premise gap at m != 0)")

print(f"\nW3 GROUND: {npass} PASS / {nfail} FAIL ({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
