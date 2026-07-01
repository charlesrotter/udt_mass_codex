#!/usr/bin/env python3
"""BLIND ADVERSARIAL VERIFIER (W4 Agent-A claims) — SCRIPT 1: SYMBOLIC.

Date: 2026-06-12.  Verifier agent (independent machinery; no w4a_* code
imported or trusted).  Targets: claim 1 (P4 gate), claim 2 (static
system + zero-cost shear continuum), claim 5 (q* erratum), the SIGN
CHAIN (priority attack A), and the cross-block / bands-vs-lines
adjudication (priority attack C).

Own machinery: sympy Function-based EL (not the agent's jet symbols),
own Christoffel/Ricci/Einstein engine, and the EINSTEIN-TENSOR
variational route E_w[sqrt(-g)R] = -sqrt(-g) G^{munu} dg_{munu}/dw for
W_wave provenance — split-free (the agent used a Gamma-Gamma split;
this route never constructs a split, so it cannot inherit one).
Log: /tmp/w4a_verifier1.log
"""
import sys, time
import sympy as sp
from sympy import Rational as Ra

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"V1-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th = sp.symbols('T r theta', positive=True)
kap, beta = sp.symbols('kappa beta', real=True)

# ===================================================================
print("=" * 70)
print("PART 1 — CONVENTION LOCK + SIGN-CHAIN ANCHORS (own construction)")
print("=" * 70)
f_, q_ = sp.symbols('f q', real=True)
wp_ = sp.Symbol('w_p', positive=True)        # w_p = 1 + w (nondegenerate)
w_ = wp_ - 1
fr_, fth_, fT_ = sp.symbols('f_r f_theta f_T', real=True)
W_ = wp_ ** 2
g4 = sp.Matrix([[-f_, 0, 0, 0],
                [0, 1 / f_, q_, 0],
                [0, q_, r ** 2 * W_, 0],
                [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W_]])
D2_ = r ** 2 * W_ - f_ * q_ ** 2
sqrtmg = r * sp.sin(th) * sp.sqrt(D2_) / (1 + w_)
check("00", sp.simplify(sqrtmg ** 2 + g4.det()) == 0,
      "sqrt(-g) = r sin sqrt(r^2 W - f q^2)/(1+w) (own determinant)")
gi = g4.inv()
phiT, phir, phith = -fT_ / (2 * f_), -fr_ / (2 * f_), -fth_ / (2 * f_)
K_full = (gi[0, 0] * phiT ** 2 + gi[1, 1] * phir ** 2
          + 2 * gi[1, 2] * phir * phith + gi[2, 2] * phith ** 2)
# corpus form (derive_system.py:75): Lc1 = -(c/2) e^{-2phi}(dphi)^2 sqrt(-g),
# banked c = -2 (derive_system check-17 lock)  =>  prefactor +1:
L_C1_banked = sp.simplify(-(sp.Integer(-2) / 2) * f_ * K_full * sqrtmg)
# agent form: +(c/2) with c = +2  =>  prefactor +1:
L_C1_agent = sp.simplify((sp.Integer(2) / 2) * f_ * K_full * sqrtmg)
check("01", sp.simplify(L_C1_banked - L_C1_agent) == 0,
      "CONVENTION LOCK: corpus -(c/2)|_{c=-2} == agent +(c/2)|_{c=+2} "
      "identically (incl. time row): NO kappa relabel enters via C1")
L_q0 = sp.simplify(L_C1_banked.subs([(q_, 0), (fT_, 0)]))
tgt = Ra(1, 4) * sp.sin(th) * (r ** 2 * fr_ ** 2 + fth_ ** 2 / (f_ * W_))
check("02", sp.simplify(L_q0 - tgt) == 0,
      "L_C1(q=0,static) = (1/4) sin [r^2 f_r^2 + f_th^2/(f(1+w)^2)] "
      "(the banked library density, w-dressed; A2 confirmed)")
# SIGN ANCHOR (a): C1's f time-kinetic coefficient (q=0):
cfT2 = sp.simplify(sp.diff(L_C1_banked.subs(q_, 0), fT_, 2) / 2)
cfT2_w0 = sp.simplify(cfT2.subs(wp_, 1))
check("03", sp.simplify(cfT2_w0 + r ** 2 * sp.sin(th) / (4 * f_ ** 2)) == 0
      and sp.simplify(cfT2 * 4 * f_ ** 2 / (r ** 2 * sp.sin(th))
                      + 1) == 0,
      "banked C1 f_T^2 coefficient = -r^2 sin/(4 f^2): STRICTLY "
      "NEGATIVE (C1's f time-kinetic is negative in the banked "
      "convention; the density is prop. to the sonic g = f f_r^2 "
      "- f_T^2/f)")

# ===================================================================
print()
print("=" * 70)
print("PART 2 — W_wave PROVENANCE: EINSTEIN-TENSOR ROUTE (split-free)")
print("=" * 70)
fF = sp.Function('f')(T, r, th)
wF = sp.Function('w')(T, r, th)
ph = sp.Symbol('varphi')
gT = sp.diag(-fF, 1 / fF, r ** 2 * (1 + wF) ** 2,
             r ** 2 * sp.sin(th) ** 2 / (1 + wF) ** 2)
xs = [T, r, th, ph]

def chr2(g, xs):
    n = 4
    giL = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for i in range(n):
            for j in range(i, n):
                e = sum(giL[a, k] * (sp.diff(g[k, i], xs[j])
                                     + sp.diff(g[k, j], xs[i])
                                     - sp.diff(g[i, j], xs[k]))
                        for k in range(n))
                Gam[a][i][j] = Gam[a][j][i] = sp.cancel(e / 2)
    return Gam, giL

def ricci(g, xs):
    n = 4
    Gam, giL = chr2(g, xs)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            e = sp.S(0)
            for a in range(n):
                e += sp.diff(Gam[a][i][j], xs[a]) \
                    - sp.diff(Gam[a][i][a], xs[j])
                for b in range(n):
                    e += (Gam[a][a][b] * Gam[b][i][j]
                          - Gam[a][j][b] * Gam[b][i][a])
            Ric[i, j] = Ric[j, i] = sp.together(e)
    return Ric, giL

print("  [own Ricci on the q=0 (T,r,th) class ...]", flush=True)
Ric, giT = ricci(gT, xs)
Rsc = sp.together(sum(giT[i, i] * Ric[i, i] for i in range(4)))
Gthth = giT[2, 2] ** 2 * (Ric[2, 2] - Rsc / 2 * gT[2, 2])
Gphph = giT[3, 3] ** 2 * (Ric[3, 3] - Rsc / 2 * gT[3, 3])
sq = r ** 2 * sp.sin(th)
# variational identity (own sign derivation):
#   delta(sqrt(-g) R) = -sqrt(-g) G^{munu} delta g_{munu} + div
Ew_curv = -sq * (Gthth * 2 * r ** 2 * (1 + wF)
                 - Gphph * 2 * r ** 2 * sp.sin(th) ** 2 / (1 + wF) ** 3)
L_W = 2 * r ** 2 * sp.sin(th) / (1 + wF) ** 2 \
    * (sp.diff(wF, T) ** 2 / fF - fF * sp.diff(wF, r) ** 2)
Ew_W = (sp.diff(L_W, wF)
        - sp.diff(sp.diff(L_W, sp.diff(wF, T)), T)
        - sp.diff(sp.diff(L_W, sp.diff(wF, r)), r))
# engine sanity: Schwarzschild Ricci == 0 (own engine):
m_ = sp.Symbol('m', positive=True)
gS = sp.diag(-(1 - 2 * m_ / r), 1 / (1 - 2 * m_ / r), r ** 2,
             r ** 2 * sp.sin(th) ** 2)
RicS, _ = ricci(gS, xs)
check("04a", all(sp.simplify(RicS[i, j]) == 0
                 for i in range(4) for j in range(4)),
      "engine sanity: Schwarzschild Ricci == 0 (own Christoffel/Ricci)")
# THE REMAINDER (the finding):
rem = sp.expand(sp.together(Ew_curv - Ew_W))
rem0 = rem
for d in (sp.Derivative(wF, (T, 2)), sp.Derivative(wF, (r, 2)),
          sp.Derivative(wF, (th, 2)), sp.Derivative(wF, T, r),
          sp.Derivative(wF, T, th), sp.Derivative(wF, r, th),
          sp.Derivative(wF, T), sp.Derivative(wF, r),
          sp.Derivative(wF, th)):
    rem0 = rem0.subs(d, 0)
tgt_rem = sp.sin(th) * sp.Derivative(fF, th) ** 2 \
    / ((1 + wF) ** 3 * fF ** 2)
check("04b", sp.simplify(sp.expand(rem - rem0)) == 0
      and sp.simplify(rem0 - tgt_rem) == 0,
      "FINDING (Einstein-tensor route): E_w[sqrt(-g)R] = EL_w[W_wave] "
      "+ sin(th) f_th^2/((1+w)^3 f^2) — the curvature species carries "
      "an EL-visible ALGEBRAIC w-tadpole beyond the declared W_wave "
      "(w-jet-free, so B1/B2's literal jet claims survive; the 'unique "
      "EL-visible w-CONTENT' framing does NOT)")
# independent second route: direct higher-order EL of the full density
# (sympy euler_equations; no Einstein identity, no split):
L_full_density = r ** 2 * sp.sin(th) * Rsc
eqs = sp.calculus.euler.euler_equations(L_full_density, [wF],
                                        [T, r, th])
Ew_direct = eqs[0].lhs - eqs[0].rhs
rem2 = sp.simplify(sp.expand(Ew_direct - Ew_W))
check("04c", sp.simplify(rem2 - tgt_rem) == 0,
      "remainder CONFIRMED by a second independent route (direct "
      "higher-order EL of sqrt(-g)R itself): the algebraic species "
      "tadpole sin f_th^2/((1+w)^3 f^2) is real; it vanishes on "
      "spherical (P4 unaffected) but is NONZERO at w=0 on shaped "
      "cells, and equals -(2/f) dL_C1/dw exactly — the declared "
      "system S = C1 + kappa W_wave TRUNCATES the species' w-sector "
      "(jets kept, algebraic force dropped, truncation never named)")
wTT = sp.Derivative(wF, (T, 2))
cwTT = sp.expand(Ew_W).coeff(wTT)
check("05", sp.simplify(cwTT + 4 * r ** 2 * sp.sin(th)
                        / (fF * (1 + wF) ** 2)) == 0,
      "w_TT coefficient of E_w = -4 r^2 sin/(f(1+w)^2)  <=>  density "
      "w_T^2 coefficient +2 r^2 sin/((1+w)^2 f): POSITIVE under "
      "+sqrt(-g)R (right-sign standalone)")
print("   SIGN-CHAIN SETTLEMENT (V1-01 + V1-03 + V1-05, all exact):")
print("   in the single banked convention, C1's f_T^2 coefficient is")
print("   NEGATIVE while kappa*W_wave's w_T^2 coefficient carries")
print("   sign(kappa).  Hence the agent's kappa>0 branch (attractive")
print("   well, growing modes) is the branch where the w time-kinetic")
print("   is OPPOSITE-signed to f's (relative-ghost pairing), and the")
print("   kinetic-MATCHED branch kappa<0 is the all-ringing one.")
print("   The agent's kappa-map and labels are convention-locked and")
print("   internally correct; no kappa relabel error exists.  But the")
print("   reading 'kappa>0 = right-sign kinetic' is STANDALONE-only —")
print("   relative to C1's own time row it is the ghost pairing.",
      flush=True)

# ===================================================================
print()
print("=" * 70)
print("PART 3 — q* ERRATUM (claim 5) + tadpole signs, own route")
print("=" * 70)
dLdq = sp.together(sp.diff(L_C1_banked.subs(fT_, 0), q_))
num = sp.numer(sp.cancel(dLdq))
qroots = sp.solve(sp.Eq(num, 0), q_)
qstar = 2 * r ** 2 * W_ * fr_ * fth_ / (f_ * r ** 2 * W_ * fr_ ** 2
                                        + fth_ ** 2)
qbrief = 2 * r ** 2 * W_ * fr_ * fth_ / (r ** 2 * W_ * fr_ ** 2
                                         + fth_ ** 2)
spot = {f_: Ra(3, 2), fr_: 2, fth_: Ra(1, 2), wp_: Ra(4, 3), r: 2,
        th: sp.pi / 3}
check("06", len(qroots) == 1 and sp.simplify(qroots[0] - qstar) == 0,
      "dL/dq = 0 has the UNIQUE root q* = 2 r^2 W f_r f_th /"
      "(f r^2 W f_r^2 + f_th^2) — WITH the f: claim-5 erratum CONFIRMED")
v_brief = sp.simplify(dLdq.subs(q_, qbrief).subs(spot))
check("07", v_brief != 0,
      "the brief's f-less q* FAILS dL/dq = 0 at a rational spot: "
      "typo adjudication correct (the f is load-bearing)")
tw = sp.simplify(sp.diff(L_q0, wp_))
check("08", sp.simplify(tw + Ra(1, 2) * sp.sin(th) * fth_ ** 2
                        / (f_ * wp_ ** 3)) == 0,
      "w-tadpole dL/dw|_{q=0} = -(1/2) sin f_th^2/(f(1+w)^3) "
      "[= -(c/4), c=2: agent A4 sign confirmed in the banked convention]")

# ===================================================================
print()
print("=" * 70)
print("PART 4 — P4 GATE (claim 1) + STATIC SYSTEM (claim 2), own EL")
print("=" * 70)
fS = sp.Function('f')(r, th)
wS = sp.Function('w')(r, th)
Dc = Ra(1, 2) * sp.sin(th) * wS * sp.diff(fS, th) ** 2 / fS
Lst = (Ra(1, 4) * sp.sin(th) * (r ** 2 * sp.diff(fS, r) ** 2
       + sp.diff(fS, th) ** 2 / (fS * (1 + wS) ** 2))
       - 2 * kap * r ** 2 * sp.sin(th) * fS * sp.diff(wS, r) ** 2
       / (1 + wS) ** 2
       + beta * Dc)

def EL(L, F):
    e = sp.diff(L, F)
    for x in (r, th):
        e -= sp.diff(sp.diff(L, sp.diff(F, x)), x)
    return e

ELf = EL(Lst, fS)
ELw = EL(Lst, wS)

def zero_w_jets(e):
    for d in (sp.Derivative(wS, (r, 2)), sp.Derivative(wS, (th, 2)),
              sp.Derivative(wS, r, th), sp.Derivative(wS, r),
              sp.Derivative(wS, th)):
        e = e.subs(d, 0)
    return e.subs(wS, 0)

def zero_fth(e):
    for d in (sp.Derivative(fS, (th, 2)), sp.Derivative(fS, r, th),
              sp.Derivative(fS, th)):
        e = e.subs(d, 0)
    return e

ELw_w0 = sp.simplify(zero_fth(zero_w_jets(ELw)))
check("09", ELw_w0 == 0,
      "P4: the full w-equation holds IDENTICALLY on {w == 0, f "
      "spherical} at symbolic kappa AND beta (both D_cell branches)")
ELf_sph = sp.simplify(zero_fth(zero_w_jets(ELf)))
vac = sp.Symbol('C') + sp.Symbol('a') / r
ELf_vac = sp.simplify(ELf_sph
                      .subs(sp.Derivative(fS, (r, 2)), sp.diff(vac, r, 2))
                      .subs(sp.Derivative(fS, r), sp.diff(vac, r))
                      .subs(fS, vac))
check("10", ELf_vac == 0 and kap not in ELf_sph.free_symbols
      and beta not in ELf_sph.free_symbols,
      "P4: the f-equation on {w=0, spherical} is kappa- AND beta-free; "
      "f = C + a/r solves it for all C, a — the macro sector cannot "
      "see kappa (claim 1 CONFIRMED, own EL)")
# static w-equation closed form (claim 2; c=2 => c/4 = 1/2):
ELw_target = (4 * kap * sp.sin(th) * (
    sp.diff(r ** 2 * fS * sp.diff(wS, r) / (1 + wS) ** 2, r)
    + r ** 2 * fS * sp.diff(wS, r) ** 2 / (1 + wS) ** 3)
    - Ra(1, 2) * sp.sin(th) * sp.diff(fS, th) ** 2 / (fS * (1 + wS) ** 3)
    + beta * Ra(1, 2) * sp.sin(th) * sp.diff(fS, th) ** 2 / fS)
check("11", sp.simplify(sp.expand(ELw - ELw_target)) == 0,
      "claim-2 static w-equation confirmed exactly (own EL): "
      "4 kappa[(r^2 f w_r/(1+w)^2)_r + r^2 f w_r^2/(1+w)^3] "
      "= (1/2) f_th^2/(f(1+w)^3) - beta (1/2) f_th^2/f")
src = sp.simplify(sp.diff(ELf, kap))
check("12", sp.simplify(src + 2 * r ** 2 * sp.sin(th)
                        * sp.diff(wS, r) ** 2 / (1 + wS) ** 2) == 0,
      "f-equation back-reaction source = -2 kappa r^2 sin w_r^2/(1+w)^2 "
      "(claim 2 confirmed; motion of w sources f at kappa != 0)")
# first integral at f_th = 0 for GENERAL f (vacuum NOT assumed):
H = r ** 2 * fS * sp.diff(wS, r) / (1 + wS)
fi = sp.simplify(sp.expand(
    zero_fth(ELw) - 4 * kap * sp.sin(th) / (1 + wS) * sp.diff(H, r)))
fi = sp.simplify(zero_fth(fi))
check("13", fi == 0,
      "FIRST INTEGRAL at f_th=0, GENERAL f: w-eq == 4 kappa sin/(1+w) "
      "d_r[r^2 f w_r/(1+w)]  =>  r^2 f w_r/(1+w) = K(theta) exactly")
# closed form for general spherical f via symbolic antiderivative:
KK, AA = sp.symbols('K A', real=True)
Fg = sp.Function('F')(r)
J = sp.Function('J')(r)
wcl = sp.exp(AA + KK * J) - 1
expr = (r ** 2 * Fg * sp.diff(wcl, r) / (1 + wcl)).subs(
    sp.Derivative(J, r), 1 / (r ** 2 * Fg))
check("14", sp.simplify(expr - KK) == 0,
      "closed form 1+w = e^{A(th)} e^{K(th) J(r)}, J' = 1/(r^2 f): "
      "verified by substitution for GENERAL spherical f (the agent's "
      "vacuum power law is the special case)")
# K != 0 family without axis flatness (numeric exhibit):
import numpy as np
from scipy.integrate import solve_ivp
def rhsK(rr, y):
    F, Fp = y           # (r^2 F')' = -4 kap K0^2/(r^2 F^2), kap=1, K0=0.3
    return [Fp, (-4 * 1.0 * 0.09 / (rr ** 2 * F ** 2) - 2 * rr * Fp)
            / rr ** 2]
solK = solve_ivp(rhsK, (1.0, 2.0), [1.0, -0.5], rtol=1e-10, atol=1e-12)
check("15", solK.success and np.all(solK.y[0] > 0),
      f"K0 != 0 EXHIBIT (axis flatness dropped): the sourced "
      f"f-spherical system (r^2 F')' = -4 kappa K0^2/(r^2 F^2) with "
      f"w from the closed form has a genuine positive-f solution on "
      f"r in [1,2] (F(2) = {solK.y[0, -1]:.4f}): the K == 0 collapse "
      f"is LOAD-BEARING on elementary flatness — claim 2's 'complete "
      f"set' is correctly premise-scoped (it names that premise)")
# zero-cost family solves both equations + action degeneracy:
gth = sp.Function('g')(th)
sub_fam = [(sp.Derivative(wS, (r, 2)), 0), (sp.Derivative(wS, r), 0),
           (sp.Derivative(wS, (th, 2)), sp.diff(gth, th, 2)),
           (sp.Derivative(wS, th), sp.diff(gth, th)), (wS, gth),
           (sp.Derivative(fS, (th, 2)), 0),
           (sp.Derivative(fS, r, th), 0), (sp.Derivative(fS, th), 0),
           (sp.Derivative(fS, (r, 2)), sp.diff(vac, r, 2)),
           (sp.Derivative(fS, r), sp.diff(vac, r)), (fS, vac)]
ELw_fam = sp.simplify(ELw.subs(sub_fam))
ELf_fam = sp.simplify(ELf.subs(sub_fam))
Lfam = sp.simplify(Lst.subs(sub_fam))
Lsph = sp.simplify(Lfam.subs(gth, 0))
check("16", ELw_fam == 0 and ELf_fam == 0
      and sp.simplify(Lfam - Lsph) == 0,
      "zero-cost shear continuum {f = C+a/r, q=0, w = g(theta)}: solves "
      "BOTH static equations at symbolic kappa, beta AND is exactly "
      "action-degenerate with spherical (claim-2 final clause confirmed "
      "on its premise set)")
# elementary flatness, own route (no series engine):
w0s, c2s, x_ = sp.symbols('w0 c2 x', positive=True)
circ = 2 * sp.pi * r * sp.sin(th) / (1 + w0s + c2s * th ** 2)
prop = sp.integrate(r * (1 + w0s + c2s * x_ ** 2), (x_, 0, th))
ratio = sp.limit(circ / (2 * sp.pi * prop), th, 0)
check("17", sp.simplify(ratio - 1 / (1 + w0s) ** 2) == 0,
      "elementary flatness (own integral): circ/(2 pi proper radius) "
      "-> 1/(1+w0)^2  =>  axis regularity forces w(poles) = 0 "
      "(E5 confirmed)")

# ===================================================================
print()
print("=" * 70)
print("PART 5 — PENCIL + CROSS BLOCKS (priority C: BANDS vs LINES)")
print("=" * 70)
t_, u_ = sp.symbols('t u', real=True)
fv, ft, fu, wv, wt, wT = sp.symbols('f f_t f_u w w_t w_T', real=True)
s_ = 1 - u_ ** 2
# own reduction of the full time-dependent density (r = e^{-t}, u = cos th):
red_chk = sp.simplify(L_q0.subs([(fr_, -sp.exp(t_) * ft),
                                 (fth_, -sp.sqrt(s_) * fu),
                                 (r, sp.exp(-t_)),
                                 (sp.sin(th), sp.sqrt(s_)),
                                 (wp_, 1 + wv)]) * sp.exp(-t_)
                      / sp.sqrt(s_))
tgt_red = sp.exp(-t_) * (Ra(1, 4) * ft ** 2
                         + Ra(1, 4) * s_ * fu ** 2 / (fv * (1 + wv) ** 2))
check("18", sp.simplify(red_chk - tgt_red) == 0,
      "own reduction reproduces the reduced C1 density "
      "e^{-t}[(1/4)f_t^2 + (1/4)s f_u^2/(f(1+w)^2)] exactly "
      "(agent F1 confirmed)")
Lred = (tgt_red
        + kap * (-2 * sp.exp(-t_) * fv * wt ** 2 / (1 + wv) ** 2
                 + 2 * sp.exp(-3 * t_) * wT ** 2 / (fv * (1 + wv) ** 2))
        + beta * Ra(1, 2) * sp.exp(-t_) * s_ * wv * fu ** 2 / fv)
on0 = [(wv, 0), (wt, 0), (wT, 0)]
H_ww = sp.simplify(sp.diff(Lred, wv, 2).subs(on0) / 2)
H_wtwt = sp.simplify(sp.diff(Lred, wt, 2).subs(on0) / 2)
H_wTwT = sp.simplify(sp.diff(Lred, wT, 2).subs(on0) / 2)
check("19", sp.simplify(H_ww - Ra(3, 4) * sp.exp(-t_) * s_ * fu ** 2
                        / fv) == 0
      and beta not in H_ww.free_symbols
      and sp.simplify(H_wtwt + 2 * kap * sp.exp(-t_) * fv) == 0
      and sp.simplify(H_wTwT - 2 * kap * sp.exp(-3 * t_) / fv) == 0,
      "w-w DIAGONAL block at w=0: +(3/4)e^{-t} s f_u^2/f psi^2 "
      "- 2k e^{-t} f psi_t^2 + 2k e^{-3t} psi_T^2/f; beta-blind "
      "(F5 confirmed)")
# pencil from scratch with t-dependent background:
om2 = sp.Symbol('omega2', real=True)
fb = sp.Function('fbar')(t_)
psi = sp.Function('psi')(t_)
Lpen = (-2 * kap * sp.exp(-t_) * fb * sp.diff(psi, t_) ** 2
        + Ra(3, 4) * sp.exp(-t_) * s_ * fu ** 2 / fb * psi ** 2
        + 2 * kap * om2 * sp.exp(-3 * t_) * psi ** 2 / fb)
ELpen = sp.diff(sp.diff(Lpen, sp.diff(psi, t_)), t_) - sp.diff(Lpen, psi)
tgt_pen = -4 * kap * (
    sp.diff(sp.exp(-t_) * fb * sp.diff(psi, t_), t_)
    + Ra(3, 8) / kap * sp.exp(-t_) * s_ * fu ** 2 / fb * psi
    + om2 * sp.exp(-3 * t_) * psi / fb)
check("20", sp.simplify(sp.expand(ELpen - tgt_pen)) == 0,
      "SL pencil re-derived from scratch: -(e^{-t} fbar psi')' "
      "- (3/(8 kappa)) e^{-t} s fbar_u^2/fbar psi = omega^2 e^{-3t} "
      "psi/fbar  [3/(8 kappa) coefficient + e^{-3t}/f weight EXACT; "
      "kappa>0 attractive, kappa<0 repulsive — F7 confirmed]")
# ---- CROSS BLOCKS at w = 0 (the load-bearing attack) ----
Xwf = sp.simplify(sp.diff(sp.diff(Lred, wv), fv).subs(on0))
Xwfu = sp.simplify(sp.diff(sp.diff(Lred, wv), fu).subs(on0))
Xwft = sp.simplify(sp.diff(sp.diff(Lred, wv), ft).subs(on0))
Xwtf = sp.simplify(sp.diff(sp.diff(Lred, wt), fv).subs(on0))
Xwtft = sp.simplify(sp.diff(sp.diff(Lred, wt), ft).subs(on0))
XwTf = sp.simplify(sp.diff(sp.diff(Lred, wT), fv).subs(on0))
print(f"   L_wf|0  = {Xwf}")
print(f"   L_wfu|0 = {Xwfu}")
print(f"   L_wft|0 = {Xwft}, L_wtf|0 = {Xwtf}, L_wtft|0 = {Xwtft}, "
      f"L_wTf|0 = {XwTf}", flush=True)
tgt_Xwf = Ra(1, 2) * sp.exp(-t_) * s_ * fu ** 2 / fv ** 2 * (1 - beta)
tgt_Xwfu = sp.exp(-t_) * s_ * fu / fv * (beta - 1)
check("21", sp.simplify(Xwf - tgt_Xwf) == 0
      and sp.simplify(Xwfu - tgt_Xwfu) == 0
      and Xwft == 0 and Xwtf == 0 and Xwtft == 0 and XwTf == 0,
      "delta-w/delta-f cross blocks at w=0: L_wf = (1/2)e^{-t} s f_u^2"
      "/f^2 (1-beta), L_wfu = e^{-t} s f_u/f (beta-1); all "
      "w-jet/f-jet crosses vanish at w=0")
check("22", sp.simplify(Xwf.subs(beta, 1)) == 0
      and sp.simplify(Xwfu.subs(beta, 1)) == 0,
      "BANDS ADJUDICATION (i): on the D_cell-ON branch (beta=1) the "
      "ENTIRE delta-w/delta-f cross block VANISHES IDENTICALLY at "
      "w = 0 (consequence of the tadpole cancellation being an "
      "identity in the f-jets): the per-u decoupling and hence the "
      "BANDS verdict are EXACT on [EXACT/D_cell-ON, q=0 class] — a "
      "rescue the agent never checked")
check("23", sp.simplify(Xwf.subs(beta, 0)) != 0
      and sp.simplify(Xwfu.subs(beta, 0)) != 0,
      "BANDS ADJUDICATION (ii): on the D_cell-OFF branch (beta=0) the "
      "cross block is NONZERO at w = 0: delta-w-only modes are NOT "
      "solutions of the coupled linearized system; the FROZEN spectra "
      "are diagonal-block readouts on an off-shell background "
      "(compounding the agent's own FROZEN label)")
# dressed background (w != 0): cross block on the ON branch too:
Xwf_dressed = sp.simplify(sp.diff(sp.diff(Lred, wv), fv)
                          .subs([(wt, 0), (wT, 0)]).subs(beta, 1))
check("24", sp.simplify(Xwf_dressed.subs(wv, 0)) == 0
      and sp.simplify(Xwf_dressed) != 0,
      "at dressed backgrounds (wbar != 0) the cross block REVIVES even "
      "on the D_cell-ON branch: the agent's A8 dressed spectra carry "
      "an unstated frozen-delta-f premise (AMENDMENT)")
# delta-q channel (free-q fork; unreduced variables):
Dc_full = Ra(1, 2) * sp.sin(th) * ((wp_ - 1) * fth_ ** 2 / f_
                                   + q_ * fr_ * fth_)
Lfull_q = sp.simplify(L_C1_banked.subs(fT_, 0)) + beta * Dc_full
X_qw = sp.simplify(sp.diff(sp.diff(Lfull_q, q_), wp_)
                   .subs([(q_, 0), (wp_, 1)]))
X_qq = sp.simplify(sp.diff(Lfull_q, q_, 2).subs([(q_, 0), (wp_, 1)]))
print(f"   L_qw|0 = {X_qw},  L_qq|0 = {X_qq}", flush=True)
check("25", sp.simplify(X_qw - sp.sin(th) * fr_ * fth_) == 0
      and sp.simplify(X_qq - Ra(1, 4) * sp.sin(th)
                      * (f_ * r ** 2 * fr_ ** 2 + fth_ ** 2)
                      / r ** 2) == 0
      and beta not in X_qw.free_symbols,
      "delta-q channel: L_qw|0 = sin f_r f_th != 0 on BOTH branches "
      "(D_cell is q-w-cross-free), L_qq|0 = (1/4) sin f (f r^2 f_r^2 "
      "+ f_th^2)/r^2 > 0 (q auxiliary): freeing q Schur-shifts the "
      "w-pencil POTENTIAL pointwise in u (no u-derivatives appear) — "
      "bands survive the free-q fork but the 3/(8 kappa) coefficient "
      "is q=0-class-scoped (AMENDMENT to F7/F8's scope)")

print(f"\nVERIFIER-1 SYMBOLIC: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
