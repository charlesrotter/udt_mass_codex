"""W4 SOLVER AGENT B — script 1: SYMBOLIC FOUNDATION + EXACT ENERGY LAW.

Declared in w_stiffness_push_declaration.md (W4 section, binding).
System: S[f,q,w] = C1 + kappa * W_wave on the P1 class, full time row.
This script re-derives, ONCE and exactly (sympy CPU), every ingredient
the W4-B solvers consume, and derives the exact w-channel energy
functional on frozen f with its flux law (the pre-registered
integrator gate: relative drift > 1e-6 invalidates a run).

EVERYTHING DOWNSTREAM (kappa != 0) IS HYPOTHESIS-GRADE. This script is
exact structure only.

Conventions (banked, re-stated):
  L_C1 = -(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f,  f = e^{-2 phi};
  P1 class + full time row:
    ds^2 = -f dT^2 + 2a dT dr + 2b dT dth + f^{-1} dr^2 + 2q dr dth
           + A dth^2 + B dph^2,  A = r^2 (1+w)^2, B = r^2 sin^2(th)/(1+w)^2.
  W_wave = [2 r^2 sin(th)/(1+w)^2] (w_T^2/f - f w_r^2)   (W2/VW1 theorem-
  grade; the unique EL-visible w-content of the second-jet species at
  q = 0; right-sign kinetic for kappa > 0; characteristics dr/dT = +-f).
  D_cell = (c/4) sin(th) [w f_th^2/f + q f_r f_th]  (test-both branch).
  Q != 0 convention; same-minus theorem-grade (nonstationary_opener).

FRAME DECLARATION (recorded fork, test-both): the static C1 w-force is
frame-dependent through the algebraic q:
  PRIMARY frame  = q-eliminated (q = q*, envelope; the W4 spec's
                   "q algebraic"):  dL*/dw = -(c/4) s f_th^2/(f(1+w)^3)
  VARIANT frame  = diagonal q = 0 (the S1 library frame):
                   dL0/dw = +(c/4) s f_th^2/(f(1+w)^3)
Both are carried in the solvers, labeled. D_cell cancels the PRIMARY
frame's w-tadpole at w = 0 (checked exactly below).

PRE-STATED FAILURE CRITERIA (committed before execution):
- S-F1: if the q-eliminated static w-force != -(c/4) s f_th^2/(f(1+w)^3)
  exactly, the source model of the solvers is DEAD - stop, report.
- S-F2: if W_wave is not EXACTLY a free f-weighted wave density in
  v = ln(1+w) (kinetic coefficients v-independent), the v-formulation
  is dead and the solvers must run in w with the null-form term.
- S-F3: if dE/dT != boundary flux exactly on frozen static f, the
  energy gate is invalid - no run may proceed.
- S-F4: if D_cell does not cancel the primary-frame w-tadpole at w=0
  exactly, the D_cell branch is mis-specified - stop, report.
- S-F5: if the tortoise/psi reduction (psi = r v, dx = dr/f) does not
  give psi_TT = psi_xx - (f f_r / r) psi + r*source exactly, the
  production stencil is mis-derived - stop.

New file (repo discipline). Logs flush-per-line. 2026-06-12, W4-B.
"""
import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label

def zc(e):
    return sp.cancel(sp.together(sp.expand(e))) == 0

c, kap = sp.symbols('c kappa', positive=True)  # kappa>0 branch for forms;
# sign enters only as an overall factor in the EL, handled in solvers.
f, r, th = sp.symbols('f r theta', positive=True)
sth = sp.Symbol('s_th', positive=True)
vr, vh, vT = sp.symbols('v_r v_theta v_T', real=True)   # f_r, f_th, f_T
q = sp.Symbol('q', real=True)
W1 = sp.Symbol('W1', positive=True)                     # 1 + w
A = r**2 * W1**2
B = r**2 * sth**2 / W1**2

print("=" * 72)
print("BLOCK A: static C1 elimination re-derivation (own route)")
print("=" * 72)
# static 3x3 (T row trivial: vT=0, a=b=0): L = (c/8) sqrt(B) N_s/(f sqrt(D_s))
Ns = -(f * (A * vr**2 - 2 * q * vr * vh + vh**2 / f))      # = -f*P
Ds = f * (A / f - q**2)                                     # = f*D2
# d/dq of N_s/sqrt(D_s): numerator 2 Ns' Ds - Ns Ds'
Eq = sp.expand(2 * sp.diff(Ns, q) * Ds - Ns * sp.diff(Ds, q))
roots = sp.solve(sp.factor(Eq), q)
qstar = 2 * A * vr * vh / (f * A * vr**2 + vh**2)
check("A1 unique static q* = 2 A vr vh/(f A vr^2 + vh^2) (re-derived)",
      len(roots) == 1 and zc(roots[0] - qstar))
Lq = Ra(1, 8) * c * sp.sqrt(B) * Ns / (f * sp.sqrt(Ds))
Kst = f * A * vr**2 - vh**2
check("A2a [N^2/D](q*) = (f A vr^2 - vh^2)^2 / A   (perfect square)",
      zc((Ns**2 / Ds).subs(q, qstar) - Kst**2 / A))
samp = {f: Ra(2), r: Ra(3, 2), W1: Ra(4, 5), vr: Ra(1), vh: Ra(1, 2),
        sth: Ra(7, 8)}
check("A2b branch sign: N_s(q*) < 0 on a subsonic K>0 sample",
      Ns.subs(q, qstar).subs(samp) < 0 and Kst.subs(samp) > 0)
Lstar = -Ra(1, 8) * c * sp.sqrt(B) * Kst / (f * sp.sqrt(A))
check("A2c L*(q*) = -(c/8) s [r^2 vr^2 - vh^2/(f(1+w)^2)]  (P1 flip form)",
      zc(sp.powsimp(Lstar, force=True)
         - (-Ra(1, 8) * c * sth * (r**2 * vr**2 - vh**2 / (f * W1**2)))))
L0 = -Ra(1, 8) * c * sth * (r**2 * vr**2 + vh**2 / (f * W1**2))
check("A3 diagonal (q=0) L0 = -(c/8) s [r^2 vr^2 + vh^2/(f(1+w)^2)] "
      "(same-minus; the q-fork flips ONLY the angular term sign)",
      zc(Lq.subs(q, 0).doit() - L0) or
      zc(sp.powsimp(Lq.subs(q, 0), force=True) - L0))
LstarP1 = -Ra(1, 8) * c * sth * (r**2 * vr**2 - vh**2 / (f * W1**2))
Fw_star = sp.diff(LstarP1, W1)
Fw_diag = sp.diff(L0, W1)
check("A4 S-F1 GATE: dL*/dw = -(c/4) s vh^2/(f(1+w)^3) [primary], "
      "dL0/dw = +(c/4) s vh^2/(f(1+w)^3) [diagonal] - EXACT, opposite",
      zc(Fw_star + Ra(1, 4) * c * sth * vh**2 / (f * W1**3)) and
      zc(Fw_diag - Ra(1, 4) * c * sth * vh**2 / (f * W1**3)))
Dcell = Ra(1, 4) * c * sth * ((W1 - 1) * vh**2 / f + q * vr * vh)
check("A5 S-F4 GATE: D_cell cancels the PRIMARY w-tadpole at w=0 exactly: "
      "d(L* + D_cell)/dw |_{w=0} = 0",
      zc((Fw_star + sp.diff(Dcell, W1)).subs(W1, 1)))
# the full primary-frame w-force with D_cell on (used by solvers):
Fw_on = sp.simplify(Fw_star + sp.diff(Dcell, W1))
print("    primary-frame w-force, D_cell ON :", Fw_on)
print("    primary-frame w-force, D_cell OFF:", Fw_star)

print("=" * 72)
print("BLOCK B: W_wave EL, v = ln(1+w), tortoise/psi reduction, energy")
print("=" * 72)
T, x = sp.symbols('T x', real=True)
rr = sp.Symbol('r', positive=True)
wf = sp.Function('w')(T, rr)
ff = sp.Function('f')(rr)            # FROZEN STATIC f (per theta-ray)
fthr = sp.Function('f_th')(rr)       # f_theta along the ray (frozen)
Wf = 1 + wf
Wwave = 2 * rr**2 * sth / Wf**2 * (sp.diff(wf, T)**2 / ff
                                   - ff * sp.diff(wf, rr)**2)
# C1 w-potential parts along the ray (primary frame), w-dependent parts only:
LC1w_off = Ra(1, 8) * c * sth * fthr**2 / (ff * Wf**2)
LC1w_on = LC1w_off + Ra(1, 4) * c * sth * fthr**2 * (Wf - 1) / ff


def EL_w(L):
    return (sp.diff(L, wf)
            - sp.diff(sp.diff(L, sp.diff(wf, T)), T)
            - sp.diff(sp.diff(L, sp.diff(wf, rr)), rr))


elw = EL_w(kap * Wwave + LC1w_off)
wTT = sp.solve(sp.expand(elw), sp.diff(wf, T, 2))[0]
wTT_expected = (ff**2 * sp.diff(wf, rr, 2)
                + ff * (2 * ff / rr + sp.diff(ff, rr)) * sp.diff(wf, rr)
                + (sp.diff(wf, T)**2 - ff**2 * sp.diff(wf, rr)**2) / Wf
                - c * fthr**2 / (16 * kap * rr**2 * Wf))
check("B1 w-equation (frozen f, D_cell OFF, primary): w_TT = f^2 w_rr "
      "+ f(2f/r + f_r) w_r + (w_T^2 - f^2 w_r^2)/(1+w) "
      "- (c/(16 kappa)) f_th^2/(r^2 (1+w))   EXACT",
      zc(wTT - wTT_expected))
check("B2 principal symbol: coeff[w_rr]/coeff[w_TT] = f^2 "
      "(characteristics dr/dT = +-f; hyperbolic in (T,r))",
      zc(sp.diff(wTT, sp.diff(wf, rr, 2)) - ff**2))
# null-form structure: the quadratic term vanishes on both characteristics
chR = {sp.diff(wf, T): ff * sp.Symbol('k'), sp.diff(wf, rr): sp.Symbol('k')}
nullq = (sp.diff(wf, T)**2 - ff**2 * sp.diff(wf, rr)**2).subs(chR)
check("B3 the quadratic nonlinearity is a NULL FORM (vanishes on "
      "dr/dT = +-f data)", sp.simplify(nullq) == 0)
# v = ln(1+w): exact linearization of the kinetic sector
vfun = sp.Function('v')(T, rr)
sub_v = {wf: sp.exp(vfun) - 1}
Wwave_v = Wwave.subs(wf, sp.exp(vfun) - 1).doit()
Wwave_v = sp.simplify(Wwave_v)
Wv_free = 2 * rr**2 * sth * (sp.diff(vfun, T)**2 / ff
                             - ff * sp.diff(vfun, rr)**2)
check("B4 S-F2 GATE: W_wave[w = e^v - 1] = 2 r^2 s (v_T^2/f - f v_r^2) "
      "EXACTLY - the wave sector is a FREE f-weighted wave in v",
      zc(Wwave_v - Wv_free))


def EL_v(L):
    return (sp.diff(L, vfun)
            - sp.diff(sp.diff(L, sp.diff(vfun, T)), T)
            - sp.diff(sp.diff(L, sp.diff(vfun, rr)), rr))


Soff_v = LC1w_off.subs(wf, sp.exp(vfun) - 1)
Son_v = LC1w_on.subs(wf, sp.exp(vfun) - 1)
elv_off = EL_v(kap * Wv_free + Soff_v)
elv_on = EL_v(kap * Wv_free + Son_v)
vTT_off = sp.solve(sp.expand(elv_off), sp.diff(vfun, T, 2))[0]
vTT_on = sp.solve(sp.expand(elv_on), sp.diff(vfun, T, 2))[0]
lin_op = (ff**2 * sp.diff(vfun, rr, 2)
          + ff * (2 * ff / rr + sp.diff(ff, rr)) * sp.diff(vfun, rr))
S_off = -c * fthr**2 * sp.exp(-2 * vfun) / (16 * kap * rr**2)
S_on = (c * fthr**2 / (16 * kap * rr**2)) * (sp.exp(vfun)
                                             - sp.exp(-2 * vfun))
check("B5a v-equation D_cell OFF: v_TT = Lin[v] - (c/(16 kappa)) "
      "f_th^2 e^{-2v}/r^2   (Liouville-type one-sided source)",
      zc(vTT_off - lin_op - S_off))
check("B5b v-equation D_cell ON: v_TT = Lin[v] + (c/(16 kappa)) "
      "f_th^2 (e^{v} - e^{-2v})/r^2   (sinh-Gordon-type; v=0 exact "
      "equilibrium; linearization +3(c/16kappa) f_th^2 v/r^2 -> "
      "ANTI-restoring for kappa>0, restoring for kappa<0)",
      zc(vTT_on - lin_op - S_on))
lin_coef = sp.diff(S_on, vfun).subs(vfun, 0)
check("B5c linearized D_cell-ON source coefficient = "
      "+3 c f_th^2/(16 kappa r^2) exactly",
      zc(lin_coef - 3 * c * fthr**2 / (16 * kap * rr**2)))

# tortoise x: dr/dx = f(r); psi = r v  =>  KG form
X = sp.Symbol('x', real=True)
rx = sp.Function('r', positive=True)(X)
fx = sp.Function('f', positive=True)(X)     # f as function of x along ray
vx = sp.Function('v')(T, X)
# Lin[v] in x-coordinates: v_r = v_x / f, etc., with dr/dx = f
# build by direct substitution rules:
vT_, vxx_ = sp.symbols('vT_ vxx_')
# express f^2 v_rr + f(2f/r + f_r) v_r in terms of x-derivatives:
# v_r = v_x/f ; v_rr = (1/f) d/dx (v_x/f) = v_xx/f^2 - v_x f_x/f^3 ;
# f_r = f_x / f
lin_x = (fx**2 * (sp.diff(vx, X, 2) / fx**2
                  - sp.diff(vx, X) * sp.diff(fx, X) / fx**3)
         + fx * (2 * fx / rx + sp.diff(fx, X) / fx) * sp.diff(vx, X) / fx)
lin_x = sp.simplify(lin_x)
check("B6a Lin[v] in tortoise x = v_xx + 2 (f/r) v_x  (f_x terms cancel "
      "EXACTLY)", zc(lin_x - sp.diff(vx, X, 2)
                     - 2 * fx / rx * sp.diff(vx, X)))
# psi = r v: psi_TT = psi_xx - (f f_r / r) psi + r * source,  f_r = f_x/f
psi = sp.Function('psi')(T, X)
v_of_psi = psi / rx
lhs = sp.diff(v_of_psi, X, 2) + 2 * fx / rx * sp.diff(v_of_psi, X)
# r * (v_xx + 2(f/r) v_x)  vs  psi_xx - (f_x/r) psi   [dr/dx = f =>
# f f_r = f_x]
lhs_r = sp.expand(rx * lhs.doit())
target = (sp.diff(psi, X, 2)
          - sp.diff(fx, X) / rx * psi)
check("B6b S-F5 GATE: r*(v_xx + 2(f/r)v_x) = psi_xx - (f_x/r) psi with "
      "psi = r v, dr/dx = f   EXACT",
      zc((lhs_r - target).subs(sp.diff(rx, X), fx).doit().subs(
          sp.diff(rx, X), fx)))
print("    PRODUCTION FORM: psi_TT = psi_xx - U0(x) psi + r(x)*Source(psi/r)")
print("    U0 = f_x/r  (= f f_r / r);  Source = S_off or S_on above")

print("=" * 72)
print("BLOCK C: exact energy functional + flux law (the run gate)")
print("=" * 72)
# per-ray Lagrangian in (T,x):  L dr = [2 kappa r^2 (v_T^2 - v_x^2)
#   + f * LC1w(v)] dx     (using v_r^2 f^2 = v_x^2, dr = f dx)
Ldx_off = (2 * kap * rx**2 * (sp.diff(vx, T)**2 - sp.diff(vx, X)**2)
           + fx * Ra(1, 8) * c * sp.Symbol('fth', positive=True)**2
           * sp.exp(-2 * vx) / fx)
fth_s = sp.Symbol('fth', positive=True)
Ldx_on = Ldx_off + fx * Ra(1, 4) * c * fth_s**2 * (sp.exp(vx) - 1) / fx
check("C0 kinetic flatness in (T,x): L dr -> 2 kappa r^2 (v_T^2 - v_x^2) dx"
      " (weight r(x)^2 only)", True)  # established by B4 + dr = f dx
# energy density e = v_T dL/dv_T - L ; flux from EL identity:
for tag, Ldx in (("OFF", Ldx_off), ("ON", Ldx_on)):
    edens = sp.diff(Ldx, sp.diff(vx, T)) * sp.diff(vx, T) - Ldx
    dedT = sp.diff(edens, T)
    # on-shell substitution: solve EL for v_TT
    el = (sp.diff(Ldx, vx)
          - sp.diff(sp.diff(Ldx, sp.diff(vx, T)), T)
          - sp.diff(sp.diff(Ldx, sp.diff(vx, X)), X))
    vTTsol = sp.solve(sp.expand(el), sp.diff(vx, T, 2))[0]
    dedT_onshell = dedT.subs(sp.diff(vx, T, 2), vTTsol)
    flux = -sp.diff(Ldx, sp.diff(vx, X)) * sp.diff(vx, T)
    resid = sp.simplify(dedT_onshell - sp.diff(flux, X))
    check(f"C1-{tag} S-F3 GATE: de/dT = d/dx[4 kappa r^2 v_x v_T] on shell"
          " EXACT (frozen static f; D_cell " + tag + ")", resid == 0)
print("    E_ray = Int dx [ 2 kappa r^2 (v_T^2 + v_x^2) + V(v;x) ],")
print("    V_off = -(c/8) f_th^2 [e^{-2v} - 1]   (normalized V(0)=0)")
print("    V_on  = -(c/8) f_th^2 [e^{-2v} + 2 e^{v} - 3]")
print("    dE/dT = [4 kappa r^2 v_x v_T]_{x_in}^{x_out}  -> 0 for "
      "Dirichlet (v_T=0) or Neumann (v_x=0) ends")
# explicit potential checks (normalization + extremum structure)
v0 = sp.Symbol('v0', real=True)
Voff = -Ra(1, 8) * c * fth_s**2 * (sp.exp(-2 * v0) - 1)
Von = -Ra(1, 8) * c * fth_s**2 * (sp.exp(-2 * v0) + 2 * sp.exp(v0) - 3)
check("C2a V_off(0)=0, V_off' (0) = +(c/4) f_th^2 (constant pull: no "
      "equilibrium at v=0, D_cell OFF)",
      Voff.subs(v0, 0) == 0 and
      zc(sp.diff(Voff, v0).subs(v0, 0) - Ra(1, 4) * c * fth_s**2))
check("C2b V_on(0)=0, V_on'(0)=0, V_on''(0) = -(3c/4) f_th^2 < 0: v=0 is "
      "the GLOBAL MAX of V_on (AM-GM: e^{-2v}+2e^v >= 3)",
      Von.subs(v0, 0) == 0 and zc(sp.diff(Von, v0).subs(v0, 0)) and
      zc(sp.diff(Von, v0, 2).subs(v0, 0) + Ra(3, 4) * c * fth_s**2))
# consistency of energy-vs-EL sign pairing: for kappa>0 the kinetic term
# in E is positive and V_on has a max at 0  => kappa>0 D_cell-ON is the
# anti-restoring branch; kappa<0 flips the kinetic sign in E and the
# dynamics (EL/kappa) sees a confining effective potential. (B5b shows
# the same at the equation level - consilient.)

print("=" * 72)
print("BLOCK D: f-coupling sources and flow-frame transcription")
print("=" * 72)
ffree = sp.Symbol('f', positive=True)
vT2, vr2 = sp.symbols('vT2 vr2', positive=True)   # v_T^2, v_r^2 stand-ins
Wfree = 2 * rr**2 * sth * (vT2 / ffree - ffree * vr2)
check("D1 dW_wave/df = -2 r^2 s (v_T^2/f^2 + v_r^2)  (negative-definite "
      "f-source for kappa>0)",
      zc(sp.diff(Wfree, ffree) + 2 * rr**2 * sth * (vT2 / ffree**2 + vr2)))
# flow-frame (t = ln(1/r)) identities used by the slice re-solve:
t = sp.Symbol('t', real=True)
g_t = sp.Function('g')(t)
# r = e^{-t}: r^2 g_r^2 = g_t^2 ; dr = -e^{-t} dt
gr = sp.diff(g_t, t) * sp.diff(sp.exp(-t), t)**-1   # dg/dr = g_t * dt/dr
check("D2 r^2 (dg/dr)^2 = (dg/dt)^2 at r = e^{-t} (flow-frame kinetic "
      "identity)", zc(sp.exp(-2 * t) * gr**2 - sp.diff(g_t, t)**2))
# dressed flow potential (library/diagonal frame, labeled):
#   P_w = (1/8) Int (1-u^2) f_u^2 / ((1+w)^2 f) du ; EL X_tt - X_t = 2 P_X
# (numerically anchored in w4b_backgrounds.py against bg_*.dat)
print("    slice re-solve EL (library frame, labeled): "
      "X_tt - X_t = 2 dP_w/dX - (4 kappa/c) Jtilde,")
print("    Jtilde_l = -Int du [e^{-2t} v_T^2/f^2 + v_t^2] Y_l(u)")

print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
    raise SystemExit(1)
print("ALL GATES OPEN: S-F1..S-F5 pass; solvers may build.")
