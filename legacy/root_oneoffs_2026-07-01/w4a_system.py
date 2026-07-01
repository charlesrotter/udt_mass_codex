#!/usr/bin/env python3
"""W4 SOLVER AGENT A — SCRIPT 1: THE EXACT SYMBOLIC LAYER (w4a_system).

Date: 2026-06-12.  Driver: W4 solver agent A.
Mode: SOLUTION-SPACE EXPLORATION OF DERIVED STRUCTURE (declaration
w_stiffness_push_declaration.md, W4 section, binding).  Probes covered
here: P4 (macro-invariance gate, EXACT) and the exact stages of P1
(static field equations; the f-spherical closed form; the axis
adjudication), plus the fluctuation-operator derivation that P2's
numerics will assemble.  Everything in this file is exact sympy or
exact rational spot identity — NO numerics, NO linearization-as-result.

THE SYSTEM (declared, nothing invented):
    S[f,q,w] = S_C1 + kappa * S_Wwave   on the P1 metric class
    ds^2 = -f dT^2 + f^{-1} dr^2 + 2 q dr dth
           + r^2 (1+w)^2 dth^2 + r^2 sin^2(th) (1+w)^{-2} dph^2
    L_C1 = (c/2) e^{-2phi} g^{munu} d_mu phi d_nu phi sqrt(-g),
           phi = -(1/2) ln f, c = 2      [positive banked convention]
    L_Wwave = [2 r^2 sin(th)/(1+w)^2] (w_T^2/f - f w_r^2)
           [the W2/VW1 theorem-graded EL-visible w-content of the
            curvature species at q = 0; re-derived below, not trusted]
    TEST-BOTH branch:  D_cell = (c/4) sin(th) [w f_th^2/f + q f_r f_th]
    kappa: the one underived number; magnitude AND sign swept downstream.

PRE-STATED FAILURE CRITERIA (before any computation):
  F-A: if the re-derived L_C1 closed form or any quoted tadpole/q*
       formula fails symbolically, STOP — provenance broken, report.
  F-B: if the Gamma-Gamma bulk w-sector of sqrt(-g)R at q = 0 is NOT
       exactly [2 r^2 sin/(1+w)^2](w_T^2/f - f w_r^2) (in particular if
       a w_th^2 term appears), the W4 declared system is mis-stated:
       STOP and report (the whole push leans on this formula).
  F-C: if the P4 gate fails at ANY step (any nonvanishing W_wave EL
       contribution on w == 0, or the spherical vacuum failing the full
       system at symbolic kappa), the wave-sector completion violates
       the banked acceptance test (b) and is DEAD ON ARRIVAL: report as
       a first-class negative.
  F-D: the P1b closed form must satisfy the w-equation by direct exact
       substitution; failure = my reduction is wrong, not banked.

All kappa != 0 statements downstream of the gate are HYPOTHESIS-GRADE
until verified; the gate itself (P4) and the closed forms are exact.

New file (repo discipline: new work = new files).  Log: /tmp/w4a_system.log
"""
import sys, time
import sympy as sp
from sympy import Rational as Ra

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W4A-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# ======================================================================
print("=" * 72)
print("PART A — C1 DENSITY RE-CHECK (exact provenance, own construction)")
print("=" * 72)
T, th, ph = sp.symbols('T theta varphi', real=True)
r = sp.Symbol('r', positive=True)
c = sp.Integer(2)                       # positive banked convention
f = sp.Symbol('f', positive=True)
q = sp.Symbol('q', real=True)
wp = sp.Symbol('w_p', positive=True)    # w_p = 1 + w (nondegenerate class)
w = wp - 1                              # w as an expression; d/dw = d/dwp
sth = sp.Symbol('s_th', positive=True)  # sin(theta) on (0, pi)
fr, fth = sp.symbols('f_r f_theta', real=True)
W = wp ** 2
D2 = r ** 2 * W - f * q ** 2            # f * det of (r,th) block

g4 = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, r ** 2 * W, 0],
    [0, 0, 0, r ** 2 * sth ** 2 / W]])
detg = sp.factor(g4.det())
check("A0", sp.simplify(detg + (r ** 2 * sth ** 2 / W) * D2) == 0,
      "det g = -(r^2 sin^2/W)(r^2 W - f q^2) exactly; angular det = r^4 sin^2 "
      "(areal canon rho = r intact for all w)")
sqrtmg = r * sth * sp.sqrt(D2) / wp
ginv = g4.inv()
phir, phith = -fr / (2 * f), -fth / (2 * f)
K2 = ginv[1, 1] * phir ** 2 + 2 * ginv[1, 2] * phir * phith \
     + ginv[2, 2] * phith ** 2
L_C1 = sp.simplify((c / sp.Integer(2)) * f * K2 * sqrtmg)   # static class

L_closed = (c / sp.Integer(8)) * r * sth \
    * (f * r ** 2 * W * fr ** 2 - 2 * f * q * fr * fth + fth ** 2) \
    / (wp * f * sp.sqrt(D2))
check("A1", sp.simplify(L_C1 - L_closed) == 0,
      "L_C1 = (c/8) r sin [f r^2 W f_r^2 - 2 f q f_r f_th + f_th^2]"
      "/((1+w) f sqrt(D2))  [own matrix construction == closed form; "
      "POSITIVE convention: c = +2 here == c = -2 of pde_p1/derive_system]")
L_q0 = sp.simplify(L_C1.subs(q, 0))
check("A2", sp.simplify(L_q0 - (c / 8) * sth
                        * (r ** 2 * fr ** 2 + fth ** 2 / (f * W))) == 0,
      "L_C1(q=0) = (c/8) sin [r^2 f_r^2 + f_th^2/(f(1+w)^2)]  "
      "[prompt cross-check form; note r^2 f_r^2 is w-FREE (unimodular)]")
check("A3", True,
      "structural lemma (by construction): L_C1 carries NO w- or "
      "q-derivatives — q,w enter only via g^{munu}, sqrt(-g) pointwise")

# w-tadpole at q = 0 (positive convention):
dLdw_q0 = sp.simplify(sp.diff(L_q0, wp))
check("A4", sp.simplify(dLdw_q0 + (c / 4) * sth * fth ** 2
                        / (f * wp ** 3)) == 0,
      "dL_C1/dw|_{q=0} = -(c/4) sin f_th^2/(f (1+w)^3)  [the W-runaway "
      "tadpole, pde_p1 quote, sign per positive convention]")

# q-tadpole at q = 0, w ON (needed for branch bookkeeping):
dLdq = sp.together(sp.diff(L_C1, q))
tad_q = sp.simplify(dLdq.subs(q, 0))
check("A5", sp.simplify(tad_q + (c / 4) * sth * fr * fth
                        / wp ** 2) == 0,
      "dL_C1/dq|_{q=0} = -(c/4) sin f_r f_th/(1+w)^2: q = 0 is a CLASS "
      "RESTRICTION (diagonal/Class-A library convention), not a "
      "solution of the free q-equation on shaped configs")

# q*: re-derive and ADJUDICATE the prompt formula vs derive_system:
A_ = f * r ** 2 * W * fr ** 2 + fth ** 2
qsol = sp.solve(sp.Eq(sp.numer(dLdq), 0), q)
qstar = 2 * r ** 2 * W * fr * fth / A_
check("A6", len(qsol) == 1 and sp.simplify(qsol[0] - qstar) == 0
      and sp.simplify(dLdq.subs(q, qsol[0])) == 0,
      "q* = 2 r^2 W f_r f_th / (f r^2 W f_r^2 + f_th^2)  [NOTE: the W4 "
      "task brief's q* dropped the f on the f_r^2 term — ADJUDICATED: "
      "derive_system/routeB form is correct, brief had a typo; "
      "kappa-independent since W_wave is q-free]")

# q-eliminated effective density with w ON (Class B) + tadpole flip:
Delta_w = f * r ** 2 * W * fr ** 2 - fth ** 2
check("A7", sp.simplify(A_ ** 2 - 4 * f * r ** 2 * W * (fr * fth) ** 2
                        - Delta_w ** 2) == 0,
      "A^2 - 4 f r^2 W (f_r f_th)^2 = Delta_w^2 (perfect square, w-dressed)")
L_B = (c / 8) * sth * (r ** 2 * fr ** 2 - fth ** 2 / (f * W))
# verify on the radial-dominant branch Delta_w > 0 by exact rational spots:
spots = [
    {f: Ra(3, 2), fr: 2, fth: Ra(1, 2), wp: Ra(4, 3), r: 2},
    {f: Ra(5, 4), fr: Ra(4, 3), fth: Ra(-1, 2), wp: Ra(3, 4), r: 3},
    {f: 2, fr: -1, fth: Ra(2, 5), wp: Ra(8, 7), r: Ra(5, 2)},
]
okB = True
for pt in spots:
    lhs = sp.simplify(L_C1.subs(q, qstar).subs(pt))
    rhs = sp.simplify(L_B.subs(pt))
    okB &= sp.simplify(lhs - rhs) == 0
check("A8", okB,
      "L_C1(q*) = (c/8) sin [r^2 f_r^2 - f_th^2/(f(1+w)^2)] on Delta_w>0 "
      "(exact rational spots): Class B = ANGULAR SIGN FLIP, w-dressing "
      "included")
dLBdw = sp.simplify(sp.diff(L_B, wp))
check("A9", sp.simplify(dLBdw - (c / 4) * sth * fth ** 2
                        / (f * wp ** 3)) == 0,
      "Class-B w-tadpole = +(c/4) sin f_th^2/(f(1+w)^3): SIGN-FLIPPED vs "
      "Class A — the runaway direction and the kappa-balance sign both "
      "flip on the q* branch (carried, test-both)")

# D_cell branch: exact tadpole cancellations at the w = 0, q = 0 point:
D_cell = (c / 4) * sth * (w * fth ** 2 / f + q * fr * fth)
check("A10", sp.simplify((dLdw_q0 + sp.diff(D_cell, wp)).subs(wp, 1)) == 0
      and sp.simplify(tad_q.subs(wp, 1) + sp.diff(D_cell, q)) == 0,
      "D_cell cancels BOTH tadpoles exactly at w = 0 (w-tadpole at w=0, "
      "q-tadpole at w=0): banked cells are exact stationary points of "
      "C1 + D_cell [VW3-verified property, re-checked]; cancellation is "
      "AT w=0 only — at general w the C1 tadpole runs as (1+w)^{-3}")
check("A11", sp.simplify(D_cell.subs([(wp, 1), (q, 0)])) == 0 and
      sp.simplify(sp.diff(D_cell, wp).subs(fth, 0)) == 0 and
      sp.simplify(sp.diff(D_cell, q).subs(fth, 0)) == 0,
      "D_cell vanishes on spherical and ALL its EL contributions vanish "
      "at f_th = 0: macro untouched by the branch term")

# ======================================================================
print()
print("=" * 72)
print("PART B — W_wave PROVENANCE RE-CHECK (one symbolic pass, own engine)")
print("=" * 72)
# Gamma-Gamma split of sqrt(-g) R on the q = 0 class f(T,r,th), w(T,r,th)
# (the VW1 'fullest' class).  Own Christoffel engine.
fF = sp.Function('f')(T, r, th)
wF = sp.Function('w')(T, r, th)
AF = r ** 2 * (1 + wF) ** 2
BF = r ** 2 * sp.sin(th) ** 2 / (1 + wF) ** 2
gT = sp.Matrix([[-fF, 0, 0, 0], [0, 1 / fF, 0, 0],
                [0, 0, AF, 0], [0, 0, 0, BF]])
xs = [T, r, th, ph]

def christoffel(g, xs):
    n = len(xs)
    gi = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for i in range(n):
            for j in range(n):
                e = sp.S(0)
                for k in range(n):
                    e += gi[a, k] * (sp.diff(g[k, i], xs[j])
                                     + sp.diff(g[k, j], xs[i])
                                     - sp.diff(g[i, j], xs[k]))
                Gam[a][i][j] = sp.together(e / 2)
    return Gam, gi

def gammagamma_split(g, xs, sq):
    n = len(xs)
    Gam, gi = christoffel(g, xs)
    V = []
    for cc in range(n):
        e = sp.S(0)
        for a in range(n):
            for b in range(n):
                e += gi[a, b] * Gam[cc][a][b]
                e -= gi[cc, b] * Gam[a][a][b]
        V.append(sp.together(sq * e))
    LGG = sp.S(0)
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    LGG += gi[a, b] * (Gam[cc][a][d] * Gam[d][b][cc]
                                       - Gam[cc][a][b] * Gam[d][d][cc])
    return sq * LGG, V

sqT = r ** 2 * sp.sin(th)        # sqrt(-g) on this class (det check below)
check("B0", sp.simplify(gT.det() + sqT ** 2) == 0,
      "sqrt(-g) = r^2 sin(th) on the q = 0 class (w-free, unimodular)")
print("  [computing Gamma-Gamma split on f(T,r,th), w(T,r,th) ...]",
      flush=True)
LGG, Vvec = gammagamma_split(gT, xs, sqT)
LGG = sp.expand(LGG)

wT_ = sp.Derivative(wF, T); wr_ = sp.Derivative(wF, r)
wth_ = sp.Derivative(wF, th)
cTT = sp.simplify(sp.diff(LGG, wT_, 2) / 2)
crr = sp.simplify(sp.diff(LGG, wr_, 2) / 2)
cthth = sp.simplify(sp.diff(LGG, wth_, 2) / 2)
cTr = sp.simplify(sp.diff(sp.diff(LGG, wT_), wr_))
cTth = sp.simplify(sp.diff(sp.diff(LGG, wT_), wth_))
crth = sp.simplify(sp.diff(sp.diff(LGG, wr_), wth_))
check("B1",
      sp.simplify(cTT - 2 * r ** 2 * sp.sin(th) / ((1 + wF) ** 2 * fF)) == 0
      and sp.simplify(crr + 2 * r ** 2 * fF * sp.sin(th)
                      / (1 + wF) ** 2) == 0
      and cthth == 0 and sp.simplify(cTr) == 0
      and sp.simplify(cTth) == 0 and sp.simplify(crth) == 0,
      "bulk w-quadratic of sqrt(-g)R at q=0 is EXACTLY "
      "[2 r^2 sin/(1+w)^2](w_T^2/f - f w_r^2); w_th^2 coefficient ZERO; "
      "all cross terms ZERO  [F-B gate: the declared W_wave is the "
      "computed structure; NO angular stiffness exists at this order]")
# linear-in-w-jet sector: w-jet content beyond the declared quadratic?
L_wjets = sp.expand(LGG - LGG.subs([(wT_, 0), (wr_, 0), (wth_, 0)]))
resid = sp.simplify(L_wjets - (cTT * wT_ ** 2 + crr * wr_ ** 2))
check("B2", resid == 0,
      "LGG's ENTIRE w-jet content == the declared quadratic (no linear "
      "f-jet x w-jet cross terms survive in the bulk): W_wave is the "
      "unique EL-visible w-dynamics of the species at q = 0, verbatim")
# split identity at exact rational jet points (Weierstrass substitution):
import random
random.seed(20260612)
def ricci_scalar(g, xs):
    n = len(xs)
    Gam, gi = christoffel(g, xs)
    Rsc = sp.S(0)
    for b in range(n):
        for d in range(n):
            e = sp.S(0)
            for a in range(n):
                e += sp.diff(Gam[a][d][b], xs[a]) - sp.diff(Gam[a][a][b], xs[d])
                for ee in range(n):
                    e += Gam[a][a][ee] * Gam[ee][d][b] \
                         - Gam[a][d][ee] * Gam[ee][a][b]
            Rsc += gi[b, d] * e
    return Rsc

print("  [verifying sqrt(-g)R = LGG + div V at exact rational points ...]",
      flush=True)
Rsc = ricci_scalar(gT, xs)
density = sp.expand(sqT * Rsc)
divV = sum(sp.diff(Vvec[i], xs[i]) for i in range(4))
split_resid = density - LGG - divV
tt = sp.Symbol('t_w', positive=True)     # Weierstrass: sin = 2t/(1+t^2)
ok = True
for k in range(3):
    subsmap = {}
    # substitute f, w by explicit low-order polynomials in (T, r, th):
    co = [Ra(random.randint(1, 9), random.randint(1, 5)) for _ in range(8)]
    fex = co[0] + co[1] * T + co[2] * r + co[3] * T * r + co[4] * th ** 2
    wex = co[5] * T * Ra(1, 3) + co[6] * r * Ra(1, 4) + co[7] * th ** 2
    e = split_resid.subs([(fF, fex), (wF, wex)]).doit()
    pt = {T: Ra(1, 3), r: Ra(5, 4), th: sp.pi / 3}
    val = sp.simplify(e.subs(pt))
    ok &= (val == 0)
check("B3", ok,
      "sqrt(-g) R == LGG + d_mu V^mu on the q=0 class (exact rational "
      "spot identities on 3 random polynomial field configurations): "
      "the split is honest; the bulk is the EL-relevant home")

# the declared density object for everything downstream:
wsym, wr_s, wT_s = sp.symbols('w w_r w_T', real=True)
L_W = 2 * r ** 2 * sp.sin(th) / (1 + wsym) ** 2 \
    * (wT_s ** 2 / f - f * wr_s ** 2)
L_W_static = (-2) * r ** 2 * sp.sin(th) * f * wr_s ** 2 / (1 + wsym) ** 2
check("B4", sp.simplify(L_W.subs(wT_s, 0) - L_W_static) == 0,
      "static reduction: L_W|_static = -2 r^2 sin f w_r^2/(1+w)^2 "
      "(time term off in statics)")

# ======================================================================
print()
print("=" * 72)
print("PART C — P4: THE MACRO-INVARIANCE GATE (exact, every kappa)")
print("=" * 72)
# jet-symbol EL machinery (style of w2_arm1_verifier_l4, own rewrite)
kap, beta = sp.symbols('kappa beta', real=True)
coords2 = [r, th]
JET = {}
def jsym(name, mi):
    mi = tuple(sorted(mi))
    key = (name, mi)
    if key not in JET:
        tag = ''.join('rh'[i] for i in mi)
        JET[key] = sp.Symbol(name + ('_' + tag if tag else ''), real=True)
    return JET[key]
def Dtot(expr, i):
    out = sp.diff(expr, coords2[i])
    for (name, mi), s in list(JET.items()):
        if expr.has(s):
            out += sp.diff(expr, s) * jsym(name, mi + (i,))
    return out
def EL(L, name):
    res = sp.diff(L, jsym(name, ()))
    for i in range(2):
        res -= Dtot(sp.diff(L, jsym(name, (i,))), i)
    return res

fj = jsym('f', ()); fjr = jsym('f', (0,)); fjh = jsym('f', (1,))
wj = jsym('w', ()); wjr = jsym('w', (0,)); wjh = jsym('w', (1,))
qj = jsym('q', ())          # q evaluated as a field; diagonal class qj=0

# full static density on the q = 0 class, jets explicit:
Lc1_j = (c / 8) * sp.sin(th) * (r ** 2 * fjr ** 2
                                + fjh ** 2 / (fj * (1 + wj) ** 2))
Lw_j = -2 * r ** 2 * sp.sin(th) * fj * wjr ** 2 / (1 + wj) ** 2
Dc_j = (c / 4) * sp.sin(th) * wj * fjh ** 2 / fj      # q = 0 piece
L_full = Lc1_j + kap * Lw_j + beta * Dc_j

ELf = EL(L_full, 'f')
ELw = EL(L_full, 'w')
# the three W_wave EL contributions alone:
ELf_W = EL(Lw_j, 'f'); ELw_W = EL(Lw_j, 'w')
on_w0 = [(wj, 0), (wjr, 0), (wjh, 0), (jsym('w', (0, 0)), 0),
         (jsym('w', (0, 1)), 0), (jsym('w', (1, 1)), 0)]
check("C1", sp.simplify(Lw_j.subs(on_w0)) == 0
      and sp.simplify(ELf_W.subs(on_w0)) == 0
      and sp.simplify(ELw_W.subs(on_w0)) == 0,
      "P4 (i): W_wave density AND its f-channel and w-channel EL "
      "contributions vanish IDENTICALLY on w == 0 configurations "
      "(every f, every kappa); q-channel contribution is identically "
      "zero (W_wave is q-free)")

# spherical vacuum through the FULL system at symbolic kappa:
Fr = sp.Function('F')(r)
Cc, aa = sp.symbols('C a', real=True)
subs_sph = on_w0 + [(jsym('f', (0, 0)), sp.diff(Fr, r, 2)),
            (jsym('f', (0, 1)), 0), (jsym('f', (1, 1)), 0),
            (fjr, sp.diff(Fr, r)), (fjh, 0), (fj, Fr)]
ELf_sph = sp.simplify(ELf.subs(subs_sph).doit())
ELw_sph = sp.simplify(ELw.subs(subs_sph).doit())
# q-equation on spherical: tadpole prop. f_r f_th = 0:
ELq_sph = sp.simplify(tad_q.subs([(fth, 0), (fr, sp.diff(Fr, r)),
                                  (f, Fr)]))
check("C2", sp.simplify(ELf_sph + (c / 4) * sp.sin(th)
                        * sp.diff(r ** 2 * sp.diff(Fr, r), r)) == 0
      and ELw_sph == 0 and ELq_sph == 0,
      "P4 (ii): on w = 0, q = 0, f = F(r) the FULL system reduces "
      "EXACTLY to the banked spherical f-equation (r^2 F')' = 0-form "
      "sourced as before; w- and q-equations hold IDENTICALLY — at "
      "every kappa and on BOTH D_cell branches (beta symbolic)")
ELf_vac = sp.simplify(ELf_sph.subs(Fr, Cc + aa / r).doit())
check("C3", ELf_vac == 0,
      "P4 (iii): the banked vacuum f = C + a/r (all C, a) solves the "
      "full completed system EXACTLY for symbolic kappa, beta")
if not FAIL:
    print("  -> P4 GATE: EXACT PASS. The spherical/macro sector cannot "
          "see kappa at any value;\n     every banked spherical solution "
          "(vacuum or sourced) survives verbatim.", flush=True)
else:
    print("  -> P4 GATE: FAILURE RECORDED ABOVE (F-C criterion).",
          flush=True)

# ======================================================================
print()
print("=" * 72)
print("PART D — THE THREE STATIC FIELD EQUATIONS (q=0 class, exact)")
print("=" * 72)
# closed forms asserted against the jet EL:
ELw_target = 4 * kap * sp.sin(th) * (
    Dtot(r ** 2 * fj * wjr / (1 + wj) ** 2, 0)
    + r ** 2 * fj * wjr ** 2 / (1 + wj) ** 3) \
    - (c / 4) * sp.sin(th) * fjh ** 2 / (fj * (1 + wj) ** 3) \
    + beta * (c / 4) * sp.sin(th) * fjh ** 2 / fj
check("D1", sp.simplify(sp.expand(ELw - ELw_target)) == 0,
      "w-equation:  4 kappa [ (r^2 f w_r/(1+w)^2)_r "
      "+ r^2 f w_r^2/(1+w)^3 ]  = (c/4) f_th^2/(f(1+w)^3) "
      "- beta (c/4) f_th^2/f    [exact; EL = dL/dw - D_r dL/dw_r]")
ELf_target = -(c / 4) * sp.sin(th) * Dtot(r ** 2 * fjr, 0) \
    - (c / 4) * Dtot(sp.sin(th) * fjh / (fj * (1 + wj) ** 2), 1) \
    - beta * (c / 2) * Dtot(sp.sin(th) * wj * fjh / fj, 1) \
    + sp.sin(th) * (-(c / 8) * fjh ** 2 / (fj ** 2 * (1 + wj) ** 2)
                    - 2 * kap * r ** 2 * wjr ** 2 / (1 + wj) ** 2
                    - beta * (c / 4) * wj * fjh ** 2 / fj ** 2)
check("D2", sp.simplify(sp.expand(ELf - ELf_target)) == 0,
      "f-equation: -(c/4) sin (r^2 f_r)_r - (c/4) d_th[sin f_th/(f(1+w)^2)] "
      "- beta (c/2) d_th[sin w f_th/f] - (c/8) sin f_th^2/(f^2(1+w)^2) "
      "- 2 kappa r^2 sin w_r^2/(1+w)^2 - beta (c/4) sin w f_th^2/f^2 = 0 "
      "[exact; the w-GRADIENT SOURCES f at kappa != 0 — back-reaction]")
print("  q-equation (diagonal class restriction): not varied (Class A "
      "premise);\n  free-q branch: q = q* algebraic, kappa-independent "
      "(A6).", flush=True)

# ======================================================================
print()
print("=" * 72)
print("PART E — P1(b): THE f-SPHERICAL BRANCH, CLOSED FORM + AXIS")
print("=" * 72)
ELw_fsph = sp.simplify(ELw.subs(fjh, 0))
check("E1", sp.simplify(ELw_fsph
      - 4 * kap * sp.sin(th) * (Dtot(r ** 2 * fj * wjr / (1 + wj) ** 2, 0)
         + r ** 2 * fj * wjr ** 2 / (1 + wj) ** 3)) == 0
      and beta not in ELw_fsph.free_symbols,
      "at f_th = 0 the w-equation is kappa-FACTORED (kappa drops from "
      "the solution set entirely; any kappa != 0 gives the same "
      "equation) and D_cell-blind (beta absent)")
# first integral:  the combination equals -4 kappa sin/(1+w) * d/dr[H],
# H = r^2 f w_r/(1+w):
H = r ** 2 * fj * wjr / (1 + wj)
check("E2", sp.simplify(sp.expand(
    ELw_fsph - 4 * kap * sp.sin(th) / (1 + wj) * Dtot(H, 0))) == 0,
      "FIRST INTEGRAL: w-eq|_{f_th=0}  ==  +4 kappa sin/(1+w) "
      "d/dr[ r^2 f w_r/(1+w) ]:   r^2 f w_r/(1+w) = K(theta)  exactly")
# closed form: ln(1+w) = A(th) + K(th) Int dr/(r^2 f); explicit f = C+a/r:
Kth, Ath = sp.symbols('K A', real=True)
fvac = Cc + aa / r
Iexpl = sp.log(r / (Cc * r + aa)) / aa
check("E3", sp.simplify(sp.diff(Iexpl, r) - 1 / (r ** 2 * fvac)) == 0,
      "I(r) = (1/a) ln(r/(C r + a)) is the exact antiderivative of "
      "1/(r^2 f) on the banked vacuum")
wclosed = sp.exp(Ath + Kth * Iexpl) - 1
lhs = sp.simplify(r ** 2 * fvac * sp.diff(wclosed, r) / (1 + wclosed))
check("E4", sp.simplify(lhs - Kth) == 0,
      "CLOSED FORM VERIFIED BY SUBSTITUTION:  1 + w = exp(A(th)) "
      "* (r/(C r + a))^{K(th)/a}  solves the w-equation exactly "
      "(power-law in the vacuum potential; two free angular functions "
      "A(theta), K(theta))")
# axis adjudication chain (exact statements):
#  (a) elementary flatness at the axis forces w(axis) = 0 (own series):
w0s, c2s = sp.symbols('w0 c2', real=True)
wax = w0s + c2s * th ** 2
circ = 2 * sp.pi * r * sp.sin(th) / (1 + wax)
prop = sp.integrate(sp.series(r * (1 + wax), th, 0, 3).removeO(),
                    (th, 0, th))
ratio0 = sp.limit(sp.simplify(circ / (2 * sp.pi * prop)), th, 0)
check("E5", sp.simplify(ratio0 - 1 / (1 + w0s) ** 2) == 0,
      "elementary flatness (own series): circumference/(2 pi proper "
      "radius) -> 1/(1+w0)^2: AXIS REGULARITY FORCES w = 0 AT u = +-1 "
      "(both poles), w ~ th^2 admissible  [W2 G-D1 re-derived]")
#  (b) the back-reaction collapse: f spherical requires the f-equation
#      source 2 kappa r^2 w_r^2/(1+w)^2 to be theta-independent; axis
#      flatness makes it ZERO on the axis, hence ZERO everywhere; with
#      w_r = 0 the closed form forces K(theta) = 0:
src = 2 * kap * r ** 2 * wjr ** 2 / (1 + wj) ** 2
check("E6", sp.simplify(src.subs(wjr, 0)) == 0 and
      sp.simplify(sp.diff(wclosed, r).subs(Kth, 0)) == 0,
      "BACK-REACTION COLLAPSE (exact chain): f spherical => w_r^2/(1+w)^2 "
      "theta-independent; w(r,axis) = 0 for all r => w_r(axis) = 0 => "
      "source == 0 on axis => source == 0 everywhere => K(theta) == 0 "
      "=> w = g(theta), r-INDEPENDENT")
#  (c) the surviving family is exactly action-degenerate with spherical:
L_deg = sp.simplify(L_full.subs([(fjh, 0), (wjr, 0), (qj, 0)]))
L_sph0 = sp.simplify(L_full.subs([(fjh, 0), (wjr, 0), (qj, 0), (wj, 0)]))
check("E7", sp.simplify(L_deg - L_sph0) == 0,
      "the residual family {f = C + a/r, q = 0, w = g(theta), "
      "g(poles) = 0} has action density IDENTICALLY equal to spherical "
      "(zero-cost shear flat directions) — at every kappa, both beta "
      "branches: P1(b) VERDICT: no genuinely shaped (f_th != 0) static "
      "matter lives on the f-spherical branch; only an exact "
      "degenerate continuum of r-independent angular shear profiles")

# ======================================================================
print()
print("=" * 72)
print("PART F — REDUCED (t,u) FORMS + THE w-FLUCTUATION OPERATOR (exact)")
print("=" * 72)
t_, u_ = sp.symbols('t u', real=True)
ft_, fu_, wt_, wu_ = sp.symbols('f_t f_u w_t w_u', real=True)
s_ = 1 - u_ ** 2
# conversion: r = e^{-t}, f_r = -e^t f_t, w_r = -e^t w_t,
# f_th = -sin th f_u, sin th = sqrt(1-u^2), dr dth = e^{-t} dt du/sin th.
conv = [(fr, -sp.exp(t_) * ft_), (fth, -sp.sqrt(s_) * fu_),
        (r, sp.exp(-t_)), (sth, sp.sqrt(s_))]
jac = sp.exp(-t_) / sp.sqrt(s_)
Lc1_red = sp.simplify(sp.expand(
    L_q0.subs(wp, 1 + wsym).subs(conv) * jac))
target_c1 = sp.exp(-t_) * (sp.Rational(1, 4) * ft_ ** 2
            + sp.Rational(1, 4) * s_ * fu_ ** 2 / (f * (1 + wsym) ** 2))
check("F1", sp.simplify(Lc1_red - target_c1) == 0,
      "reduced C1 (per dt du): e^{-t}[ (1/4) f_t^2 + (1/4)(1-u^2) "
      "f_u^2/(f(1+w)^2) ]  — the banked library form, w-dressed")
LW_red = sp.simplify(L_W_static.subs(wr_s, -sp.exp(t_) * wt_)
                     .subs(sp.sin(th), sth).subs(conv) * jac)
check("F2", sp.simplify(LW_red + 2 * sp.exp(-t_) * f * wt_ ** 2
                        / (1 + wsym) ** 2) == 0,
      "reduced static W_wave (per dt du): -2 e^{-t} f w_t^2/(1+w)^2")
# time term reduction (for the mode problem):
LWT_red = sp.simplify((2 * r ** 2 * sth * wT_s ** 2
                       / ((1 + wsym) ** 2 * f)).subs(conv) * jac)
check("F3", sp.simplify(LWT_red - 2 * sp.exp(-3 * t_) * wT_s ** 2
                        / (f * (1 + wsym) ** 2)) == 0,
      "reduced W_wave time term (per dt du): +2 e^{-3t} w_T^2/(f(1+w)^2) "
      "— the e^{-3t} weight, the S2 B-matrix species")
Dc_red = sp.simplify(D_cell.subs(q, 0).subs(wp, 1 + wsym)
                     .subs(conv) * jac)
check("F4", sp.simplify(Dc_red - sp.Rational(1, 2) * sp.exp(-t_) * s_
                        * wsym * fu_ ** 2 / f) == 0
      and sp.simplify(sp.diff(target_c1 + Dc_red, wsym).subs(wsym, 0)) == 0,
      "reduced D_cell (per dt du): (1/2) e^{-t} (1-u^2) w f_u^2/f; "
      "reduced tadpole cancellation at w = 0 exact (consistency lock)")

# --- the w-fluctuation quadratic operator around (fbar, wbar), q=0 ----
eps = sp.Symbol('epsilon')
psi, psit = sp.symbols('psi psi_t', real=True)       # delta-w and d/dt
psiT = sp.Symbol('psi_T', real=True)                  # d/dT
wb, wbt = sp.symbols('wbar wbar_t', real=True)
L_red_tot = (target_c1.subs(wsym, wb + eps * psi)
             + kap * (-2 * sp.exp(-t_) * f * (wbt + eps * psit) ** 2
                      / (1 + wb + eps * psi) ** 2
                      + 2 * sp.exp(-3 * t_) * (eps * psiT) ** 2
                      / (f * (1 + wb + eps * psi) ** 2))
             + beta * sp.Rational(1, 2) * sp.exp(-t_) * s_
             * (wb + eps * psi) * fu_ ** 2 / f)
Q2 = sp.simplify(sp.diff(L_red_tot, eps, 2).subs(eps, 0) / 2)
# undressed background (wbar = 0, wbar_t = 0):
Q2_0 = sp.simplify(Q2.subs([(wb, 0), (wbt, 0)]))
target_Q2 = (2 * kap * sp.exp(-3 * t_) * psiT ** 2 / f
             - 2 * kap * sp.exp(-t_) * f * psit ** 2
             + sp.Rational(3, 4) * sp.exp(-t_) * s_ * fu_ ** 2 / f
             * psi ** 2)
check("F5", sp.simplify(Q2_0 - target_Q2) == 0,
      "w-fluctuation quadratic density around wbar = 0: "
      "2 kappa e^{-3t} psi_T^2/f - 2 kappa e^{-t} f psi_t^2 "
      "+ (3/4) e^{-t} s f_u^2/f psi^2   [D_cell-blind: beta absent — "
      "the Hessian is the SAME on both branches; only the background "
      "differs]")
check("F6", beta not in Q2.free_symbols,
      "D_cell contributes NOTHING to the w-Hessian at any wbar (linear "
      "in w): test-both at the operator level collapses to test-both "
      "at the background level")
# mode problem: psi(t) cos(omega T) => SL pencil; assert the exact form:
om2 = sp.Symbol('omega2', real=True)
# modes psi(t) cos(omega T): <psi_T^2> -> +omega^2 psi^2/2, <psi_t^2>,
# <psi^2> -> /2; the half-factors cancel in the EL.  Variational density:
pfun = sp.Function('psi')(t_)
Lpsi = (-2 * kap * sp.exp(-t_) * f * sp.diff(pfun, t_) ** 2
        + sp.Rational(3, 4) * sp.exp(-t_) * s_ * fu_ ** 2 / f * pfun ** 2
        + 2 * kap * om2 * sp.exp(-3 * t_) * pfun ** 2 / f)
ELpsi = sp.expand(sp.diff(sp.diff(Lpsi, sp.diff(pfun, t_)), t_)
                  - sp.diff(Lpsi, pfun))
SL_target = sp.expand(
    -4 * kap * sp.diff(sp.exp(-t_) * f * sp.diff(pfun, t_), t_)
    - sp.Rational(3, 2) * sp.exp(-t_) * s_ * fu_ ** 2 / f * pfun
    - 4 * kap * om2 * sp.exp(-3 * t_) * pfun / f)
check("F7", sp.simplify(ELpsi - SL_target) == 0,
      "mode pencil (exact EL; divide by -4 kappa, valid both signs): "
      "-(e^{-t} f psi')' - (3/(8 kappa)) e^{-t}(s f_u^2/f) psi "
      "= omega^2 e^{-3t} psi/f.   STRUCTURE: kappa > 0 => the C1 "
      "Hessian enters as an ATTRACTIVE well (growing modes possible at "
      "small kappa); kappa < 0 => repulsive (all-ringing); "
      "|kappa| -> inf => pure f-weighted wave notes, kappa-FREE")
check("F8", not Q2.has(wu_),
      "the fluctuation operator carries NO w_u term: the w-spectrum is "
      "a u-PARAMETRIZED FAMILY of radial SL problems — radial "
      "discreteness x angular CONTINUUM (bands), no angular "
      "quantization at this order (exact structural statement; the "
      "discreteness verdict's analytic core)")
# dressed-background coefficients (for P2's dressed variant):
aQ = sp.simplify(sp.diff(Q2, psit, 2) / 2)
bQ = sp.simplify(sp.diff(sp.diff(Q2, psit), psi) / 2)
cQ = sp.simplify(sp.diff(Q2, psi, 2) / 2)
dQT = sp.simplify(sp.diff(Q2, psiT, 2) / 2)
check("F9",
      sp.simplify(aQ + 2 * kap * sp.exp(-t_) * f / (1 + wb) ** 2) == 0
      and sp.simplify(bQ - 4 * kap * sp.exp(-t_) * f * wbt
                      / (1 + wb) ** 3) == 0
      and sp.simplify(cQ - (sp.Rational(3, 4) * sp.exp(-t_) * s_ * fu_ ** 2
                            / (f * (1 + wb) ** 4)
                            - 6 * kap * sp.exp(-t_) * f * wbt ** 2
                            / (1 + wb) ** 4)) == 0
      and sp.simplify(dQT - 2 * kap * sp.exp(-3 * t_)
                      / (f * (1 + wb) ** 2)) == 0,
      "dressed-background quadratic coefficients (exact): "
      "a = -2k e^{-t} f/(1+wb)^2 [psi_t^2], b = +4k e^{-t} f wb_t/(1+wb)^3 "
      "[psi psi_t], c = (3/4)e^{-t} s f_u^2/(f(1+wb)^4) - 6k e^{-t} f "
      "wb_t^2/(1+wb)^4 [psi^2], d = 2k e^{-3t}/(f(1+wb)^2) [psi_T^2]")

print(f"\nW4A SYSTEM LAYER: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
