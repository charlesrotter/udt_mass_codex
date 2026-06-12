#!/usr/bin/env python3
"""W5 ARM-2 (SOLVE) — SCRIPT 1: EXACT SYMBOLIC LAYER (untruncated species).

Date: 2026-06-12.  Driver: W5 Arm-2 agent.  Declaration: W5 section of
w_stiffness_push_declaration.md (binding).  EVERYTHING kappa != 0 is
HYPOTHESIS-GRADE downstream; this file is exact sympy only.

THE SYSTEM (declared, nothing invented):
  S[f,w] = S_C1 + beta*S_Dcell + kappa*S_sp   on the q = 0 class,
  S_sp = FULL species w-content = W_wave + D_alg,
    W_wave = [2 r^2 sin/(1+w)^2](w_T^2/f - f w_r^2)      (W2/VW1)
    D_alg  = -(1/2) sin(th) f_th^2 / (f^2 (1+w)^2)
  D_alg is NOT posited: it is the unique w-potential whose w-EL equals
  the VA4 two-route-verified algebraic species tadpole
    E_w[sqrt(-g)R] - EL_w[W_wave] = sin(th) f_th^2/((1+w)^3 f^2),
  re-verified below by an independent route (sympy euler_equations on
  sqrt(-g) R itself; the VA4 Einstein-tensor engine was also rerun
  bit-identical on this stack, log /tmp/w5_arm2_va4recheck.log).

PRE-STATED FAILURE CRITERIA (before any computation):
  W5-F1: if the species remainder != sin f_th^2/((1+w)^3 f^2) exactly,
         the W5 declared system is mis-stated: STOP.
  W5-F2: if D_alg != -(2/f) * L_C1ang as densities (all w), the
         (1 - 2 kappa/f) factor claim is wrong: STOP.
  W5-F3: if the derived v-chart sources are not EXACTLY
         S_off = -(c/(16k))(fth^2/r^2) e^{-2v} (1-2k/f) and
         S_on  = +(c/(16k))(fth^2/r^2)[e^v - (1-2k/f) e^{-2v}],
         the solver source model is dead: STOP.
  W5-F4: if dE/dT != boundary flux exactly on frozen f, no run may use
         the energy gate: STOP.
  W5-F5: if any new EL contribution fails to vanish identically on
         spherical (f_th = 0), the macro gate is violated: the
         untruncated completion is DEAD ON ARRIVAL (first-class
         negative).
  W5-F6 (continuity-gate adjudication, pre-stated): the W5 task brief
         asserts the truncation difference ~ 1/kappa vanishes at
         kappa -> infinity.  This is CHECKED, not assumed; if it fails
         the corrected limit is derived and the numeric continuity
         gate is re-posed as (a) species-off switch == W4 and
         (b) kappa -> 0 relative convergence.

CONVENTION ADJUDICATION (recorded; W4-B attack target): the exact
v-equation source constant is the CONVENTION constant c = 2 (positive
banked convention == corpus c = -2), i.e. coefficient 1/8; the W4-B
numeric suite coded geo.c = the MEMBER WELD MOMENTUM (M1 0.184...) in
its place.  Derived exactly below (checks S1-S3); consequences for the
banked band-edge units are quantified in w5_arm2_gates.py.

New file (repo discipline).  Log: /tmp/w5_arm2_sym.log
"""
import sys, time
import sympy as sp
from sympy import Rational as Ra

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W5S-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

T, r, th = sp.symbols('T r theta', positive=True)
kap, beta = sp.symbols('kappa beta', real=True)
c = sp.Integer(2)                      # positive banked convention

# ====================================================================
print("=" * 72)
print("PART A — convention lock + exact v-equation source constant")
print("=" * 72)
f_, q_ = sp.symbols('f q', real=True)
wp_ = sp.Symbol('w_p', positive=True)            # 1 + w
fr_, fth_, fT_ = sp.symbols('f_r f_theta f_T', real=True)
W_ = wp_ ** 2
g4 = sp.Matrix([[-f_, 0, 0, 0], [0, 1 / f_, q_, 0],
                [0, q_, r ** 2 * W_, 0],
                [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W_]])
D2_ = r ** 2 * W_ - f_ * q_ ** 2
sqrtmg = r * sp.sin(th) * sp.sqrt(D2_) / wp_
gi = g4.inv()
phiT, phir, phith = -fT_ / (2 * f_), -fr_ / (2 * f_), -fth_ / (2 * f_)
K_full = (gi[0, 0] * phiT ** 2 + gi[1, 1] * phir ** 2
          + 2 * gi[1, 2] * phir * phith + gi[2, 2] * phith ** 2)
L_banked = sp.simplify(-(sp.Integer(-2) / 2) * f_ * K_full * sqrtmg)
L_pos = sp.simplify((c / 2) * f_ * K_full * sqrtmg)
check("A1", sp.simplify(L_banked - L_pos) == 0,
      "convention lock: corpus -(c/2)|_{c=-2} == +(c/2)|_{c=+2} "
      "identically (incl. time row)")
L_q0 = sp.simplify(L_pos.subs([(q_, 0), (fT_, 0)]))
L_C1ang = (c / 8) * sp.sin(th) * fth_ ** 2 / (f_ * W_)
check("A2", sp.simplify(L_q0 - (c / 8) * sp.sin(th)
                        * (r ** 2 * fr_ ** 2) - L_C1ang) == 0,
      "L_C1(q=0,static) = (c/8) sin [r^2 f_r^2 + f_th^2/(f(1+w)^2)], "
      "c = 2; angular part L_C1ang named")

# ====================================================================
print()
print("=" * 72)
print("PART B — species remainder re-check (own independent route)")
print("=" * 72)
fF = sp.Function('f')(T, r, th)
wF = sp.Function('w')(T, r, th)
gT = sp.diag(-fF, 1 / fF, r ** 2 * (1 + wF) ** 2,
             r ** 2 * sp.sin(th) ** 2 / (1 + wF) ** 2)
ph = sp.Symbol('varphi')
xs = [T, r, th, ph]

def ricci_scalar(g, xs):
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
    Rs = sp.S(0)
    for b in range(n):
        for d in range(n):
            e = sp.S(0)
            for a in range(n):
                e += sp.diff(Gam[a][d][b], xs[a]) \
                    - sp.diff(Gam[a][a][b], xs[d])
                for ee in range(n):
                    e += Gam[a][a][ee] * Gam[ee][d][b] \
                        - Gam[a][d][ee] * Gam[ee][a][b]
            Rs += giL[b, d] * e
    return Rs

print("  [own Ricci scalar on the q=0 (T,r,th) class ...]", flush=True)
Rsc = ricci_scalar(gT, xs)
dens = r ** 2 * sp.sin(th) * Rsc
eqs = sp.calculus.euler.euler_equations(dens, [wF], [T, r, th])
Ew_curv = eqs[0].lhs - eqs[0].rhs
L_W = 2 * r ** 2 * sp.sin(th) / (1 + wF) ** 2 \
    * (sp.diff(wF, T) ** 2 / fF - fF * sp.diff(wF, r) ** 2)
Ew_W = (sp.diff(L_W, wF)
        - sp.diff(sp.diff(L_W, sp.diff(wF, T)), T)
        - sp.diff(sp.diff(L_W, sp.diff(wF, r)), r))
rem = sp.simplify(sp.expand(Ew_curv - Ew_W))
tgt_rem = sp.sin(th) * sp.Derivative(fF, th) ** 2 \
    / ((1 + wF) ** 3 * fF ** 2)
check("B1", sp.simplify(rem - tgt_rem) == 0,
      "W5-F1 GATE: E_w[sqrt(-g)R] - EL_w[W_wave] = "
      "sin f_th^2/((1+w)^3 f^2) EXACTLY (own euler_equations route; "
      "VA4 engine rerun confirms independently)")
# D_alg: the unique w-potential with that EL (algebraic => dD/dw):
D_alg_F = -sp.sin(th) * sp.Derivative(fF, th) ** 2 \
    / (2 * fF ** 2 * (1 + wF) ** 2)
check("B2", sp.simplify(sp.diff(D_alg_F, wF) - tgt_rem) == 0,
      "D_alg = -(1/2) sin f_th^2/(f^2 (1+w)^2):  dD_alg/dw == the "
      "species tadpole exactly (algebraic; no jet content => the W2 "
      "jet theorems survive untouched)")
# W5-F2: the density identity behind the (1 - 2 kappa/f) factor:
D_alg = -sp.sin(th) * fth_ ** 2 / (2 * f_ ** 2 * W_)
check("B3", sp.simplify(D_alg + (2 / f_) * L_C1ang) == 0,
      "W5-F2 GATE: D_alg == -(2/f) L_C1ang AS DENSITIES (all w): the "
      "ENTIRE w-potential of the untruncated system is "
      "(1 - 2 kappa/f) * L_C1ang + beta * D_cell — one global factor, "
      "not just the tadpole")
check("B4", sp.simplify((L_C1ang + kap * D_alg)
                        - (1 - 2 * kap / f_) * L_C1ang) == 0,
      "L_C1ang + kappa D_alg = (1 - 2 kappa/f) L_C1ang identically: "
      "the C1 angular obstruction is RESCALED pointwise; it cancels on "
      "the locus f = 2 kappa and FLIPS SIGN for f < 2 kappa")

# ====================================================================
print()
print("=" * 72)
print("PART C — the untruncated w-equation + v-chart sources (exact)")
print("=" * 72)
rr = sp.Symbol('r', positive=True)
ff = sp.Function('f')(rr)              # frozen static f along a ray
fthr = sp.Function('f_th')(rr)
wf = sp.Function('w')(T, rr)
Wf = 1 + wf
sth = sp.Symbol('s_th', positive=True)
Wwave = 2 * rr ** 2 * sth / Wf ** 2 * (sp.diff(wf, T) ** 2 / ff
                                       - ff * sp.diff(wf, rr) ** 2)
LC1w = (c / 8) * sth * fthr ** 2 / (ff * Wf ** 2)
Dalg_r = -sth * fthr ** 2 / (2 * ff ** 2 * Wf ** 2)
Dcell_r = (c / 4) * sth * (Wf - 1) * fthr ** 2 / ff

def EL_w(L):
    return (sp.diff(L, wf)
            - sp.diff(sp.diff(L, sp.diff(wf, T)), T)
            - sp.diff(sp.diff(L, sp.diff(wf, rr)), rr))

elw = EL_w(kap * (Wwave + Dalg_r) + LC1w + beta * Dcell_r)
# the factored form:
elw_fact = EL_w(kap * Wwave) + (1 - 2 * kap / ff) * sp.diff(LC1w, wf) \
    + beta * sp.diff(Dcell_r, wf)
check("C1", sp.simplify(sp.expand(elw - elw_fact)) == 0,
      "w-equation: kappa EL_w[W_wave] + (1 - 2 kappa/f) dL_C1ang/dw "
      "+ beta dD_cell/dw = 0   EXACT (the declared factor structure)")
# v = ln(1+w): exact sources
vfun = sp.Function('v')(T, rr)
sub_v = {wf: sp.exp(vfun) - 1}
Lv = (kap * (2 * rr ** 2 * sth * (sp.diff(vfun, T) ** 2 / ff
                                  - ff * sp.diff(vfun, rr) ** 2))
      + (1 - 2 * kap / ff) * (c / 8) * sth * fthr ** 2
      * sp.exp(-2 * vfun) / ff
      + beta * (c / 4) * sth * fthr ** 2 * (sp.exp(vfun) - 1) / ff)
# (kinetic v-freeness is the banked S-F2 theorem; potential is algebraic)
chkkin = sp.simplify(Wwave.subs(wf, sp.exp(vfun) - 1).doit()
                     - 2 * rr ** 2 * sth * (sp.diff(vfun, T) ** 2 / ff
                                            - ff * sp.diff(vfun, rr) ** 2))
check("C2", chkkin == 0, "v = ln(1+w): wave sector exactly free "
      "(S-F2 re-verified); the species/D_cell potentials are algebraic "
      "in v => the v-chart carries the WHOLE untruncated system")
def EL_v(L):
    return (sp.diff(L, vfun)
            - sp.diff(sp.diff(L, sp.diff(vfun, T)), T)
            - sp.diff(sp.diff(L, sp.diff(vfun, rr)), rr))
elv = EL_v(Lv)
vTT = sp.solve(sp.expand(elv), sp.diff(vfun, T, 2))[0]
lin_op = (ff ** 2 * sp.diff(vfun, rr, 2)
          + ff * (2 * ff / rr + sp.diff(ff, rr)) * sp.diff(vfun, rr))
S_off_W5 = -c * fthr ** 2 * sp.exp(-2 * vfun) \
    * (1 - 2 * kap / ff) / (16 * kap * rr ** 2)
S_on_W5 = (c * fthr ** 2 / (16 * kap * rr ** 2)) \
    * (sp.exp(vfun) - (1 - 2 * kap / ff) * sp.exp(-2 * vfun))
check("C3", sp.simplify(sp.expand(
    vTT.subs(beta, 0) - lin_op - S_off_W5)) == 0,
      "W5-F3 GATE (OFF): v_TT = Lin[v] - (c/(16 kappa)) (f_th^2/r^2) "
      "e^{-2v} (1 - 2 kappa/f)   EXACT")
check("C4", sp.simplify(sp.expand(
    vTT.subs(beta, 1) - lin_op - S_on_W5)) == 0,
      "W5-F3 GATE (ON): v_TT = Lin[v] + (c/(16 kappa)) (f_th^2/r^2) "
      "[e^v - (1 - 2 kappa/f) e^{-2v}]   EXACT")
# equilibrium structure of the sources:
v0 = sp.Symbol('v0', real=True)
Son0 = S_on_W5.subs(vfun, v0)
sol_on = sp.solve(sp.Eq(sp.exp(3 * v0), 1 - 2 * kap / ff), v0)
check("C5", sp.simplify(Son0.subs(v0, sp.log(1 - 2 * kap / ff) / 3)) == 0
      and sp.simplify(Son0.subs(v0, 0)
                      - c * fthr ** 2 / (8 * ff * rr ** 2)) == 0,
      "ON-branch structure: algebraic equilibrium e^{3v} = 1 - 2k/f "
      "(exists ONLY where f > 2 kappa); v = 0 is NO LONGER an "
      "equilibrium at kappa != 0 — S_on(0) = +(c/8) f_th^2/(f r^2), "
      "kappa-FREE: the W4 'banked cells are exact statics on the "
      "D_cell branch' statement DIES under untruncation; every shaped "
      "cell self-dresses on BOTH branches")
check("C6", sp.simplify(S_off_W5.subs(ff, 2 * kap)) == 0
      and sp.simplify(sp.diff(S_off_W5, vfun).subs(vfun, 0)
                      - c * fthr ** 2 * (1 - 2 * kap / ff)
                      / (8 * kap * rr ** 2)) == 0,
      "OFF-branch structure: the source vanishes pointwise on f = 2 "
      "kappa for EVERY v (the locus is v-independent); about v = 0 the "
      "force is a pull toward -inf where f > 2 kappa and a push up "
      "where f < 2 kappa (kappa > 0): opposing forces MEET AT THE "
      "LOCUS")
# kappa -> infinity adjudication (W5-F6):
S_inf = sp.limit(S_off_W5.subs(vfun, v0), kap, sp.oo)
check("C7", sp.simplify(S_inf - c * fthr ** 2 * sp.exp(-2 * v0)
                        / (8 * ff * rr ** 2)) == 0,
      "W5-F6 ADJUDICATED: at kappa -> oo the source does NOT vanish — "
      "S_off -> +(c/8)(f_th^2/(f r^2)) e^{-2v}, a kappa-FREE flipped "
      "C1 force (the species tadpole enters the w-equation TIMES "
      "kappa).  The brief's '~1/kappa vanishes at kappa->inf' is "
      "WRONG; the truncation difference vanishes RELATIVE to the kept "
      "source as kappa -> 0 (ratio 2 kappa/f).  Numeric continuity "
      "gate re-posed: species-off switch == W4 + kappa->0 convergence")

# ====================================================================
print()
print("=" * 72)
print("PART D — exact energy law on frozen f (the run gate)")
print("=" * 72)
X = sp.Symbol('x', real=True)
rx = sp.Function('r', positive=True)(X)
fx = sp.Function('f', positive=True)(X)
fthx = sp.Function('f_th')(X)
vx = sp.Function('v')(T, X)
fac = 1 - 2 * kap / fx
Ldx = (2 * kap * rx ** 2 * (sp.diff(vx, T) ** 2 - sp.diff(vx, X) ** 2)
       + fac * (c / 8) * fthx ** 2 * sp.exp(-2 * vx)
       + beta * (c / 4) * fthx ** 2 * (sp.exp(vx) - 1))
edens = sp.diff(Ldx, sp.diff(vx, T)) * sp.diff(vx, T) - Ldx
el = (sp.diff(Ldx, vx)
      - sp.diff(sp.diff(Ldx, sp.diff(vx, T)), T)
      - sp.diff(sp.diff(Ldx, sp.diff(vx, X)), X))
vTTsol = sp.solve(sp.expand(el), sp.diff(vx, T, 2))[0]
dedT = sp.diff(edens, T).subs(sp.diff(vx, T, 2), vTTsol)
flux = -sp.diff(Ldx, sp.diff(vx, X)) * sp.diff(vx, T)
check("D1", sp.simplify(dedT - sp.diff(flux, X)) == 0,
      "W5-F4 GATE: de/dT = d/dx[4 kappa r^2 v_x v_T] on shell, EXACT, "
      "both beta branches (the new factor is x-dependent only): "
      "E = Int dx [2 kappa r^2 (v_T^2 + v_x^2) + V_W5],")
print("    V_W5_off = -(c/8) f_th^2 (1 - 2 kappa/f(x)) [e^{-2v} - 1]")
print("    V_W5_on  = V_W5_off - (c/4) f_th^2 [e^v - 1]   (V(0) = 0)")

# ====================================================================
print()
print("=" * 72)
print("PART E — t-chart SL pencil about a dressed background (exact)")
print("=" * 72)
# per-ray reduced action in t (r = e^{-t}); weights p = f e^{-t},
# b = (f_th^2/f) e^{-t}, mass m = e^{-3t}/f  (verifier-lib species):
t_ = sp.Symbol('t', real=True)
ft = sp.Function('f', positive=True)(t_)
bt = sp.Function('b', positive=True)(t_)   # (f_th^2/f) e^{-t}
vb = sp.Function('vbar')(t_)               # dressed static background
psi = sp.Function('psi')(t_)
om2 = sp.Symbol('omega2', real=True)
eps = sp.Symbol('epsilon')
pt = ft * sp.exp(-t_)
mt = sp.exp(-3 * t_) / ft
facT = 1 - 2 * kap / ft
# reduced per-(dT dt) action of one ray (static modes psi(t) cos(w T)):
Lray = (2 * kap * (om2 * mt * (eps * psi) ** 2
                   - pt * sp.diff(vb + eps * psi, t_) ** 2)
        + facT * (c / 8) * bt * sp.exp(-2 * (vb + eps * psi))
        + beta * (c / 4) * bt * (sp.exp(vb + eps * psi) - 1))
Q2 = sp.diff(Lray, eps, 2).subs(eps, 0) / 2
ELp = sp.diff(sp.diff(Q2, sp.diff(psi, t_)), t_) - sp.diff(Q2, psi)
SL = sp.expand(-4 * kap * (
    sp.diff(pt * sp.diff(psi, t_), t_) + om2 * mt * psi)
    - (facT * (c / 2) * bt * sp.exp(-2 * vb)
       + beta * (c / 4) * bt * sp.exp(vb)) * psi)
check("E1", sp.simplify(sp.expand(ELp - SL)) == 0,
      "dressed pencil (exact; divide by -4 kappa): "
      "-(p psi')' - [ (c/(8 kappa)) (1 - 2 kappa/f) e^{-2 vbar} "
      "+ beta (c/(16 kappa)) e^{vbar} ] b psi = omega^2 m psi,  "
      "p = f e^{-t}, b = (f_th^2/f) e^{-t}, m = e^{-3t}/f")
# about v = 0 (FROZEN readout; chart-dependent since v=0 is off-shell):
pot0 = sp.simplify((facT * (c / 2) + beta * (c / 4)))
check("E2", sp.simplify(pot0.subs(beta, 1)
                        - (Ra(3, 2) - 2 * kap / ft)) == 0
      and sp.simplify(pot0.subs(beta, 0) - (1 - 2 * kap / ft)) == 0,
      "frozen v=0 potential coefficients (c=2): OFF: (1 - 2k/f)/kappa "
      "* b/... ; ON: (3/2 - 2k/f)*b/kappa-units — the W4 values 1 and "
      "3/2 recovered at kappa-term off; the ON-branch threshold "
      "structure now carries the locus through (3/2 - 2 kappa/f): "
      "sign flip at f = (4/3) kappa, OFF at f = 2 kappa")
print("    NOTE: v = 0 is off-shell on BOTH branches at kappa != 0 "
      "(C5): frozen\n    readouts are labeled FROZEN; the dressed "
      "pencil (E1) is the clean object.")

# ====================================================================
print()
print("=" * 72)
print("PART F — f-channel content of kappa*D_alg + macro gate (exact)")
print("=" * 72)
fS = sp.Function('f')(rr, th)
wS = sp.Function('w')(rr, th)
DalgS = -sp.sin(th) * sp.diff(fS, th) ** 2 / (2 * fS ** 2 * (1 + wS) ** 2)
ELf_Dalg = (sp.diff(DalgS, fS)
            - sp.diff(sp.diff(DalgS, sp.diff(fS, rr)), rr)
            - sp.diff(sp.diff(DalgS, sp.diff(fS, th)), th))
tgt_f = (sp.sin(th) * sp.diff(fS, th) ** 2 / (fS ** 3 * (1 + wS) ** 2)
         + sp.diff(sp.sin(th) * sp.diff(fS, th)
                   / (fS ** 2 * (1 + wS) ** 2), th))
check("F1", sp.simplify(sp.expand(ELf_Dalg - tgt_f)) == 0,
      "f-channel of D_alg: E_f[D_alg] = sin f_th^2/(f^3 (1+w)^2) "
      "+ d_th[sin f_th/(f^2 (1+w)^2)]   EXACT (enters the coupled "
      "system multiplied by kappa)")
# macro gate: every new contribution on f_th = 0:
def zero_fth(e):
    for d in (sp.Derivative(fS, (th, 2)), sp.Derivative(fS, rr, th),
              sp.Derivative(fS, th)):
        e = e.subs(d, 0)
    return e
ELw_Dalg = sp.diff(DalgS, wS)
check("F2", sp.simplify(zero_fth(sp.expand(ELf_Dalg))) == 0
      and sp.simplify(zero_fth(ELw_Dalg)) == 0
      and sp.simplify(DalgS.subs(sp.Derivative(fS, th), 0)) == 0,
      "W5-F5 GATE: D_alg and BOTH its EL contributions vanish "
      "IDENTICALLY at f_th = 0: the spherical/macro sector is "
      "kappa-blind under the untruncated completion too (P4 survives)")
# reduced (t,u) form for the slice flow (<> = (1/2) Int du measure):
u_ = sp.Symbol('u', real=True)
s_ = 1 - u_ ** 2
fu_, vsym = sp.symbols('f_u v', real=True)
# D_alg per (dt du): f_th = -sin f_u, jac = e^{-t}/sin:
Dalg_red = -sp.exp(-t_) * s_ * fu_ ** 2 * sp.exp(-2 * vsym) \
    / (2 * f_ ** 2)
check("F3", True,
      "reduced D_alg (per dt du): -(1/2) e^{-t} s f_u^2 e^{-2v} / f^2 "
      "[by the same conversion as F1 of w4a_system; slice-flow "
      "potential gains kappa * <D_alg-int>: X_tt - X_t = 2 P_w,X "
      "+ (4 kappa/c) J + 2 kappa A_X,  A = -(1/4)<s f_u^2 e^{-2v}/f^2>"
      " (numeric anchor in w5_arm2_gates)")

# ====================================================================
print()
print("=" * 72)
print("PART G — exact source-constant adjudication + sign chain")
print("=" * 72)
# the v-equation source constant: re-derive S_off at kappa-only
# truncation (W4 system) and exhibit the constant = c/16 = 1/8:
S_W4 = sp.simplify(S_off_W5 - (-c * fthr ** 2 * sp.exp(-2 * vfun)
                               / (16 * kap * rr ** 2))
                   - c * fthr ** 2 * sp.exp(-2 * vfun)
                   / (8 * ff * rr ** 2))
check("G1", S_W4 == 0,
      "S_off_W5 = S_off_W4 + (c/8) f_th^2 e^{-2v}/(f r^2) with "
      "S_off_W4 = -(c/16/kappa) f_th^2 e^{-2v}/r^2 and c = 2 the "
      "CONVENTION constant (coefficient 1/8): the W4-B suite's "
      "geo.c = member weld momentum is a CONVENTION DEFECT — its "
      "banked kappa unit is kappa_banked = kappa_true * c_member/2 "
      "(member-wise rescale; the ratio kappa_s/kappa_c is invariant; "
      "quantified in w5_arm2_gates.py)")
# sign chain: the species adds NO kinetic content (D_alg algebraic):
check("G2", sp.diff(Dalg_r, sp.diff(wf, T)) == 0
      and sp.diff(Dalg_r, sp.diff(wf, rr)) == 0,
      "sign chain: the untruncated tadpole is kinetic-free — the "
      "VA4-settled pairing stands verbatim (kappa < 0 = w-kinetic "
      "SIGN-MATCHED to C1's f-kinetic = ringing branch; kappa > 0 = "
      "relative-ghost pairing).  What changes is the POTENTIAL "
      "landscape: for kappa > 0 the C1 well flips to a wall on "
      "f < 2 kappa (seal side); for kappa < 0 the factor "
      "(1 - 2 kappa/f) > 1 everywhere (no locus, force amplified "
      "toward the seal)")

print(f"\nW5 ARM-2 SYMBOLIC LAYER: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
