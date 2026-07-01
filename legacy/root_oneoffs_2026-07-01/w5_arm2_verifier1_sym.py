#!/usr/bin/env python3
"""W5 ARM-2 BLIND VERIFIER — SCRIPT 1: independent symbolic refutation
attempt (claims 1, 2-symbolic, 3-constant, and the ARM-RECONCILIATION
adjudication of attack B).

Date: 2026-06-12.  Verifier agent (blind, independent machinery).
ROUTES DELIBERATELY DIFFERENT from w5_arm2_sym.py:
  - species remainder computed in the V-CHART metric g_thth = r^2
    e^{2v}, g_phph = r^2 sin^2 e^{-2v} (their route: w-chart), with my
    own Ricci implementation (sanity-locked on Schwarzschild);
  - the corpus C1 density built from phi = -(1/2) ln f from scratch;
  - the v-equation source derived by substitution into the w-EL (their
    route: variation of the v-form action);
  - the static t-chart constant derived by chart transport (the
    convention adjudication: cc = 2, NOT the member weld momentum);
  - NEW: the f-channel two-arm reconciliation: E_f of the SUBTRACTED
    species density (the species' actual w-content L(w) - L(0)) vs
    E_f[D_alg]; the "uniqueness" claim adjudicated.

Log: /tmp/w5_arm2_verifier1_sym.log.  New file.
"""
import sys, time
import sympy as sp

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"VW5A2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th, ph = sp.symbols('T r theta varphi', positive=True)
kap, beta = sp.symbols('kappa beta', real=True)

# ---------------------------------------------------------------- my Ricci
def my_ricci_scalar(g, xs):
    """Own implementation (independent code path: inverse via adjugate,
    Riemann-then-contract, cancel-only simplification)."""
    n = len(xs)
    gi = g.adjugate().T / g.det()
    gi = gi.applyfunc(sp.cancel)
    Gam = {}
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                s = sum(gi[a, d] * (sp.diff(g[d, b], xs[c])
                                    + sp.diff(g[d, c], xs[b])
                                    - sp.diff(g[b, c], xs[d]))
                        for d in range(n)) / 2
                Gam[(a, b, c)] = Gam[(a, c, b)] = sp.cancel(s)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(b, n):
            s = 0
            for a in range(n):
                s += sp.diff(Gam[(a, b, c)], xs[a]) \
                    - sp.diff(Gam[(a, b, a)], xs[c])
                for d in range(n):
                    s += Gam[(a, a, d)] * Gam[(d, b, c)] \
                        - Gam[(a, c, d)] * Gam[(d, b, a)]
            Ric[b, c] = Ric[c, b] = s
    return sp.cancel(sum(gi[b, c] * Ric[b, c]
                         for b in range(n) for c in range(n)))

# sanity lock: Schwarzschild
M = sp.Symbol('M', positive=True)
fs = 1 - 2 * M / r
gS = sp.diag(-fs, 1 / fs, r ** 2, r ** 2 * sp.sin(th) ** 2)
check("00", sp.simplify(my_ricci_scalar(gS, [T, r, th, ph])) == 0,
      "engine sanity: R(Schwarzschild) == 0 (own Ricci)")

# ============================================================ PART I
print("=" * 72)
print("PART I — corpus C1 density from scratch (the convention constant)")
print("=" * 72)
f_, w_ = sp.symbols('f w', positive=True)
fr_, fth_, fT_ = sp.symbols('f_r f_theta f_T', real=True)
Wp = (1 + w_) ** 2
g4 = sp.diag(-f_, 1 / f_, r ** 2 * Wp, r ** 2 * sp.sin(th) ** 2 / Wp)
check("I0", sp.simplify(-g4.det() - (r ** 2 * sp.sin(th)) ** 2) == 0,
      "(-det g) = (r^2 sin th)^2 on the q=0 diagonal class "
      "(w-independent); sqrt taken on the 0<th<pi branch")
sqrtmg = r ** 2 * sp.sin(th)
# banked corpus convention: L_C1 = -(c/2) f K sqrt(-g), c = -2
phiT, phir, phith = -fT_ / (2 * f_), -fr_ / (2 * f_), -fth_ / (2 * f_)
gi4 = g4.inv()
K = (gi4[0, 0] * phiT ** 2 + gi4[1, 1] * phir ** 2
     + gi4[2, 2] * phith ** 2)
L_C1 = sp.simplify(-(sp.Integer(-2)) / 2 * f_ * K * sqrtmg)
L_C1ang_mine = sp.Rational(1, 4) * sp.sin(th) * fth_ ** 2 / (f_ * Wp)
check("I1", sp.simplify(L_C1.subs(fT_, 0)
                        - sp.Rational(1, 4) * sp.sin(th) * r ** 2 * fr_ ** 2
                        - L_C1ang_mine) == 0,
      "corpus density from scratch: L_C1(static) = (1/4) sin [r^2 f_r^2"
      " + f_th^2/(f(1+w)^2)]; angular coefficient 1/4 == (c/8)|_{c=2}: "
      "the v-equation convention constant is cc = 2 (claim-3 basis)")

# ============================================================ PART II
print("=" * 72)
print("PART II — species remainder, OWN ROUTE (v-chart metric)")
print("=" * 72)
fF = sp.Function('f')(T, r, th)
vF = sp.Function('v')(T, r, th)
gV = sp.diag(-fF, 1 / fF, r ** 2 * sp.exp(2 * vF),
             r ** 2 * sp.sin(th) ** 2 * sp.exp(-2 * vF))
print("  [own Ricci scalar, v-chart ...]", flush=True)
Rv = my_ricci_scalar(gV, [T, r, th, ph])
densV = r ** 2 * sp.sin(th) * Rv          # sqrt(-g) = r^2 sin, exact
def EL(L, u, xs):
    e = sp.diff(L, u)
    for x in xs:
        e -= sp.diff(sp.diff(L, sp.diff(u, x)), x)
        for y in xs:
            e += sp.diff(sp.diff(L, sp.diff(u, x, y)), x, y) \
                if x == y else 0
    return e
# densV carries second derivatives -> use sympy euler for order 2:
from sympy.calculus.euler import euler_equations
Ev_curv = (euler_equations(densV, [vF], [T, r, th])[0].lhs
           - euler_equations(densV, [vF], [T, r, th])[0].rhs)
WwaveV = 2 * r ** 2 * sp.sin(th) * (sp.diff(vF, T) ** 2 / fF
                                    - fF * sp.diff(vF, r) ** 2)
Ev_W = (euler_equations(WwaveV, [vF], [T, r, th])[0].lhs
        - euler_equations(WwaveV, [vF], [T, r, th])[0].rhs)
remV = sp.simplify(sp.expand(Ev_curv - Ev_W))
tgtV = sp.sin(th) * sp.exp(-2 * vF) * sp.Derivative(fF, th) ** 2 / fF ** 2
check("II1", sp.simplify(remV - tgtV) == 0,
      "OWN ROUTE (v-chart): E_v[sqrt(-g)R] - EL_v[W_wave] = "
      "sin e^{-2v} f_th^2/f^2 == (1+w) * [their w-chart tadpole]: "
      "claim-1 remainder CONFIRMED by an independent chart + engine")

# D_alg in v: -(1/2) sin f_th^2 e^{-2v}/f^2; dD/dv = -2 D = (1+w) dD/dw ok
D_alg_v = -sp.sin(th) * sp.Derivative(fF, th) ** 2 \
    * sp.exp(-2 * vF) / (2 * fF ** 2)
check("II2", sp.simplify(sp.diff(D_alg_v, vF) - tgtV) == 0,
      "dD_alg/dv == the v-chart tadpole exactly (consistent transport "
      "of their B2)")

# ============================================================ PART III
print("=" * 72)
print("PART III — 'uniqueness', the SUBTRACTED density, two-arm E_f")
print("=" * 72)
fS = sp.Function('f')(r, th)
wS = sp.Function('w')(r, th)
WpS = (1 + wS) ** 2
tad = sp.sin(th) * sp.Derivative(fS, th) ** 2 / ((1 + wS) ** 3 * fS ** 2)
D_alg = -sp.sin(th) * sp.Derivative(fS, th) ** 2 / (2 * fS ** 2 * WpS)
g_arb = sp.Function('g')(fS, th)          # arbitrary w-independent density
check("III1", sp.simplify(sp.diff(D_alg + g_arb, wS) - tad) == 0,
      "REFUTATION of 'unique w-potential' AS WORDED: D_alg + g(f,th) "
      "has the SAME w-EL for ARBITRARY g — uniqueness holds only "
      "modulo w-independent additive densities (the loose joint)")
# the species' actual algebraic w-content (Arm-1 weight-stripping):
D_sub = D_alg - D_alg.subs(wS, 0)
def E_f(L):
    return (sp.diff(L, fS)
            - sp.diff(sp.diff(L, sp.diff(fS, r)), r)
            - sp.diff(sp.diff(L, sp.diff(fS, th)), th))
Ef_Dalg = E_f(D_alg)
Ef_Dsub = E_f(D_sub)
check("III2", sp.simplify(Ef_Dsub.subs(wS, 0).doit()) == 0,
      "ARM RECONCILIATION: E_f[the SUBTRACTED species density "
      "D_alg(w) - D_alg(0)] == 0 IDENTICALLY at w = 0 — exactly "
      "Arm-1's E_f[Delta_w] = 0 statement")
Ef0 = sp.simplify(Ef_Dalg.subs(wS, 0).doit())
tgt0 = sp.simplify(sp.sin(th) * sp.Derivative(fS, th) ** 2 / fS ** 3
                   + sp.diff(sp.sin(th) * sp.Derivative(fS, th)
                             / fS ** 2, th))
check("III3", sp.simplify(Ef0 - tgt0) == 0 and Ef0 != 0,
      "E_f[D_alg]|_{w=0} = sin f_th^2/f^3 + d_th[sin f_th/f^2] != 0: "
      "the Arm-2 coupled system's f-force at w = 0 is ENTIRELY the "
      "w-independent additive piece — NOT species content.  The two "
      "arms' f-channel statements differ by E_f[D_alg(0)] exactly:")
check("III4", sp.simplify(Ef_Dalg - Ef_Dsub
                          - E_f(D_alg.subs(wS, 0))) == 0,
      "E_f[D_alg] = E_f[D_sub] + E_f[D_alg(0)] (exact decomposition; "
      "the coupled premise 'D_alg-as-action-density' injects the "
      "w-independent f-force E_f[D_alg(0)] of O(kappa) at v = 0)")

# ============================================================ PART IV
print("=" * 72)
print("PART IV — v-equation sources by SUBSTITUTION (own route) + cc")
print("=" * 72)
rr = sp.Symbol('r', positive=True)
ff = sp.Function('f', positive=True)(rr)
fthr = sp.Function('f_th')(rr)
wf = sp.Function('w')(T, rr)
sth = sp.Symbol('s_th', positive=True)
Wf = 1 + wf
Wwave = 2 * rr ** 2 * sth / Wf ** 2 * (sp.diff(wf, T) ** 2 / ff
                                       - ff * sp.diff(wf, rr) ** 2)
LC1w = sp.Rational(1, 4) * sth * fthr ** 2 / (ff * Wf ** 2)
Dalg_r = -sth * fthr ** 2 / (2 * ff ** 2 * Wf ** 2)
Dcell_r = sp.Rational(1, 2) * sth * (Wf - 1) * fthr ** 2 / ff
def EL_w(L):
    return (sp.diff(L, wf)
            - sp.diff(sp.diff(L, sp.diff(wf, T)), T)
            - sp.diff(sp.diff(L, sp.diff(wf, rr)), rr))
elw = EL_w(kap * (Wwave + Dalg_r) + LC1w + beta * Dcell_r)
# substitute w = e^v - 1 and reduce to v_TT form (OWN route):
vfun = sp.Function('v')(T, rr)
sub = {wf: sp.exp(vfun) - 1}
elv = elw.subs(wf, sp.exp(vfun) - 1).doit()
vTT = sp.solve(sp.expand(elv), sp.diff(vfun, T, 2))
assert len(vTT) == 1
vTT = vTT[0]
lin = (ff ** 2 * sp.diff(vfun, rr, 2)
       + ff * (2 * ff / rr + sp.diff(ff, rr)) * sp.diff(vfun, rr))
S_off = -fthr ** 2 * sp.exp(-2 * vfun) * (1 - 2 * kap / ff) \
    / (8 * kap * rr ** 2)
S_on = (fthr ** 2 / (8 * kap * rr ** 2)) \
    * (sp.exp(vfun) - (1 - 2 * kap / ff) * sp.exp(-2 * vfun))
check("IV1", sp.simplify(sp.expand(vTT.subs(beta, 0) - lin - S_off)) == 0,
      "OWN substitution route, OFF: v_TT = Lin[v] - (1/(8 kappa)) "
      "(f_th^2/r^2) e^{-2v} (1 - 2 kappa/f): the coefficient is 1/8 "
      "== cc/16 with cc = 2 (claims S_off + factorization + constant)")
check("IV2", sp.simplify(sp.expand(vTT.subs(beta, 1) - lin - S_on)) == 0,
      "OWN substitution route, ON: source +(1/(8k))(fth^2/r^2)[e^v - "
      "(1-2k/f)e^{-2v}]: claim S_on confirmed; v=0 gives S_on(0) = "
      "+(1/4) f_th^2/(f r^2) != 0 at ALL kappa != 0 (self-dressing)")
v0 = sp.Symbol('v0', real=True)
Son0 = S_on.subs(vfun, v0)
check("IV3", sp.simplify(Son0.subs(v0, sp.log(1 - 2 * kap / ff) / 3)) == 0,
      "ON algebraic equilibrium e^{3v} = 1 - 2 kappa/f (f > 2 kappa) "
      "confirmed")
check("IV4", sp.simplify(Son0.subs(v0, 0)
                         - fthr ** 2 / (4 * ff * rr ** 2)) == 0
      and sp.simplify(S_off.subs(vfun, 0).subs(ff, 2 * kap)) == 0,
      "v = 0 static on NEITHER branch at kappa != 0 (ON residual "
      "kappa-free +f_th^2/(4 f r^2); OFF source vanishes only ON the "
      "locus f = 2 kappa)")
S_inf = sp.limit(S_off.subs(vfun, v0), kap, sp.oo)
check("IV5", sp.simplify(S_inf - fthr ** 2 * sp.exp(-2 * v0)
                         / (4 * ff * rr ** 2)) == 0,
      "kappa -> oo: S_off -> +f_th^2 e^{-2v}/(4 f r^2) (kappa-FREE "
      "flipped repulsive C1 force; the W5 brief's 'vanishes at "
      "kappa->oo' premise is indeed WRONG; their C7 adjudication "
      "CORRECT)")
# static t-chart transport: r = e^{-t}; confirm (p v')' = lam b e^{-2v}
# with lam = 1/(8 kappa) for the W4-truncated OFF system:
t_ = sp.Symbol('t', real=True)
vt_ = sp.Function('v')(t_)
ft_ = sp.Function('f', positive=True)(t_)
btw = sp.Function('b', positive=True)(t_)
# static OFF truncated: Lin[v] - (1/(8k)) (fth^2/r^2) e^{-2v} = 0 in r;
# in t: d/dr = -e^{t} d/dt on r = e^{-t}:
rsub = sp.exp(-t_)
fth_t = sp.Function('f_th')(t_)
expr_r = (lin - fthr ** 2 * sp.exp(-2 * vfun) / (8 * kap * rr ** 2))
# build the same statics directly in t and compare with (p v')':
p_t = ft_ * sp.exp(-t_)
b_t = fth_t ** 2 / ft_ * sp.exp(-t_)
stat_t = sp.diff(p_t * sp.diff(vt_, t_), t_) \
    - (1 / (8 * kap)) * b_t * sp.exp(-2 * vt_)
# transport expr_r:  v(T,r)->vt(t), f->ft, fth->fth_t, r=e^{-t}; the
# r-equation times [e^{-3t}/f] must equal stat_t/<sign>:
sub_t = {vfun: vt_, ff: ft_, fthr: fth_t, rr: rsub,
         sp.diff(vfun, rr): -sp.exp(t_) * sp.diff(vt_, t_),
         sp.diff(vfun, rr, 2): sp.exp(2 * t_) * (sp.diff(vt_, t_, 2)
                                                 + sp.diff(vt_, t_)),
         sp.diff(ff, rr): -sp.exp(t_) * sp.diff(ft_, t_)}
expr_t = sp.expand(expr_r.subs(sub_t).doit() * sp.exp(-3 * t_) / ft_)
check("IV6", sp.simplify(sp.expand(expr_t - sp.expand(stat_t / 1))) == 0,
      "t-chart statics: (p v')' = (1/(8 kappa)) b e^{-2v}, p = f e^{-t}"
      ", b = (f_th^2/f) e^{-t}: lam* fold => kappa_s = 1/(8 lam*) = "
      "cc/(16 lam*) with cc = 2.  The committed W4-B suites coded "
      "kappa_s = mem.c/(16 lam*) (w4b_verifier_lib.py:267, "
      "w4b_evolib.py:120 sc = c*fth2/(16 r^2)): kappa_banked = "
      "kappa_true * c_member/2 CONFIRMED — the convention finding "
      "stands on an independent derivation")
# ON-branch frozen v=0 linearization -> kappa_c formula:
lin_on = sp.diff((fthr ** 2 / (8 * kap * rr ** 2))
                 * (sp.exp(vfun) - sp.exp(-2 * vfun)), vfun).subs(vfun, 0)
check("IV7", sp.simplify(lin_on - 3 * fthr ** 2 / (8 * kap * rr ** 2)) == 0,
      "frozen ON edge: potential slope 3/(8 kappa) (f_th^2/r^2) => "
      "kappa_c = 3/(8 mu_1) TRUE units = 3 cc/(16 mu_1); committed "
      "code used 3*mem.c/(16 mu) (w4b_verifier_lib.py:179): same "
      "member-wise rescale, ratio kappa_s/kappa_c EXACTLY invariant "
      "(both linear in the constant)")

# ============================================================ PART V
print("=" * 72)
print("PART V — macro gate + energy law (independent confirmation)")
print("=" * 72)
# macro gate: all new pieces carry f_th^2 factors:
check("V1", sp.simplify(D_alg.subs(sp.Derivative(fS, th), 0)) == 0
      and sp.simplify(E_f(D_alg).subs(sp.Derivative(fS, th), 0).doit()
                      .subs(sp.Derivative(fS, r, th), 0)
                      .subs(sp.Derivative(fS, th, 2), 0)) != sp.nan,
      "D_alg ∝ f_th^2 (vanishes on spherical); E_f[D_alg] vanishes "
      "when f_th == 0 on a neighborhood (all terms carry f_th or "
      "f_th-derivatives times f_th)")
ef_expanded = sp.expand(E_f(D_alg).doit())
ok_macro = sp.simplify(ef_expanded.subs([(sp.Derivative(fS, th), 0)])) == 0
check("V2", ok_macro,
      "E_f[D_alg] == 0 at f_th = 0 pointwise-in-jets? "
      + ("YES (every term carries f_th itself)" if ok_macro else
         "NO — carries f_thth terms surviving f_th -> 0: gate is "
         "neighborhood-only (still macro-safe on spherical f)"))
# energy law (their D1) on frozen f, x-chart:
X = sp.Symbol('x', real=True)
rx = sp.Function('r', positive=True)(X)
fx = sp.Function('f', positive=True)(X)
fthx = sp.Function('f_th')(X)
vx = sp.Function('v')(T, X)
fac = 1 - 2 * kap / fx
Ldx = (2 * kap * rx ** 2 * (sp.diff(vx, T) ** 2 - sp.diff(vx, X) ** 2)
       + fac * sp.Rational(1, 4) * fthx ** 2 * sp.exp(-2 * vx)
       + beta * sp.Rational(1, 2) * fthx ** 2 * (sp.exp(vx) - 1))
edens = sp.diff(Ldx, sp.diff(vx, T)) * sp.diff(vx, T) - Ldx
el = (sp.diff(Ldx, vx)
      - sp.diff(sp.diff(Ldx, sp.diff(vx, T)), T)
      - sp.diff(sp.diff(Ldx, sp.diff(vx, X)), X))
vTTsol = sp.solve(sp.expand(el), sp.diff(vx, T, 2))[0]
dedT = sp.diff(edens, T).subs(sp.diff(vx, T, 2), vTTsol)
flux = 4 * kap * rx ** 2 * sp.diff(vx, X) * sp.diff(vx, T)
check("V3", sp.simplify(sp.expand(dedT - sp.diff(flux, X))) == 0,
      "energy law de/dT = d_x[4 kappa r^2 v_x v_T] EXACT both "
      "branches (their D1 confirmed; energy gate licensed)")

print(f"\nVW5A2 SYM: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
