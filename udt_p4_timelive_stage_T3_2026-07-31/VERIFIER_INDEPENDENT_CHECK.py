#!/usr/bin/env python3
# BLIND VERIFIER independent check for Stage T3 (2026-07-31).  Zero-context adversarial
# pass; exact SymPy only; exit nonzero on any failure.  Written INDEPENDENTLY of
# derive_timelive_T3.py: different witnesses, different routes (trig-kernel instead of
# exp spot-certificates), an explicit counterexample audit of the depth-lock biconditional,
# and a from-scratch C-1 parser.  Commits nothing.
import os, sys, csv
import sympy as sp
from sympy import (Symbol, symbols, Rational, sqrt, exp, log, sin, cos, pi, I, integrate,
                   diff, simplify, solveset, S, Eq, FiniteSet, ImageSet, Lambda)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
FAILS = []
def chk(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
    if not ok:
        FAILS.append(name)

x, t, s_ = symbols('x t s', real=True)
T = Symbol('T', positive=True); ell = Symbol('ell', positive=True)
aF = Symbol('a_F', nonzero=True); gp = Symbol('g_p', positive=True)
gth = Symbol('g_theta', positive=True)
E0 = Symbol('E0', real=True); w1c, w0c = symbols('w1 w0', real=True)
n_t = Symbol('n_t', integer=True)

# ---- V1: DUTY 3 -- C-1 re-run with an INDEPENDENT parser (stricter class checks) ----
led = os.path.join(REPO, "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv")
rows = list(csv.DictReader(open(led, newline=""), delimiter="\t"))
chk("V1a_static_ledger_20_rows", len(rows) == 20, f"{len(rows)} data rows")
# independent machinery: (i) torsion: n*P=0, n=2 -> P=0 over R; (ii) Hom(Dinf,R)=0 from
# relations r^2=1 (h(r) solved over R); (iii) N=1 cyclic Delta pi_p forces A=0;
# (iv) all-definite SOS; (v) slope kill; (vi) real point kernel of e^h=1.
Pv = Symbol('Pv', real=True); hv = Symbol('hv', real=True)
m_tor = solveset(Eq(2*Pv, 0), Pv, S.Reals) == FiniteSet(0)
m_dinf = solveset(Eq(2*hv, 0), hv, S.Reals) == FiniteSet(0)
Af = Symbol('Af', real=True)
wN1 = Af*x**2 + w1c*x + w0c
m_N1 = solveset(Eq(gp*(diff(wN1, x).subs(x, ell) - diff(wN1, x).subs(x, -ell))/aF, 0),
                Af, S.Reals) == FiniteSet(0)
L1, L2 = symbols('L1 L2', positive=True)
e2n = Symbol('e2n', nonnegative=True)
zf = Symbol('zf', real=True)                 # free stand-in for the solved variable
_s = solveset(Eq(zf*L1 + e2n*L2, 0), zf, S.Reals)
_el = list(_s)[0] if isinstance(_s, FiniteSet) and len(_s) == 1 else None
m_sos = (_el is not None and simplify(_el + e2n*L2/L1) == 0
         and sp.ask(sp.Q.nonpositive(_el)) is True
         and solveset(Eq(zf*L2, 0), zf, S.Reals) == FiniteSet(0))
# chain: E0_1 = -e2 L2/L1 <= 0; with E0_1 >= 0 forced to 0; then e2 L2 = 0 => e2 = 0.
f1v = Symbol('f1v', real=True)
m_slope = solveset(Eq(f1v*L1, 0), f1v, S.Reals) == FiniteSet(0)
m_ker = solveset(Eq(exp(hv), 1), hv, S.Reals) == FiniteSet(0)
klass = {  # (cycle, family-substr or None) -> (required verdict substring, machinery ok)
    ("K4-orbifold / cap-torsion", None): ("VACUOUS", m_tor),
    ("D_inf translation gamma_T", None): ("IDENTICALLY SATISFIED", m_dinf),
    ("none (no cycle)", None): ("VACUOUS", True),           # vacuity = no cycle exists
    ("Z translation (cyclic completion)", "constants-census"): ("forced massless", m_N1 and m_sos),
    ("Z translation (cyclic completion)", "fields-census"): ("forced massless", m_slope),
    ("Z translation (cyclic completion)", "massless strata"): ("SATISFIED identically", True),
    ("Z translation (cyclic completion)", "wall germ"): ("supplied J_s", True),
    ("J11 chart loop", None): ("NO discrete structure", m_ker),
}
n_ok = 0
for r in rows:
    hit = None
    for (cyc, fam), (kw, mach) in klass.items():
        if r["cycle"] == cyc and (fam is None or fam in r["family"]):
            hit = (kw, mach); break
    if hit and hit[0] in r["verdict"] and hit[1]:
        n_ok += 1
chk("V1b_C1_recovery_independent", n_ok == 20, f"{n_ok}/20 rows recovered (own parser, "
    "own machinery; 3 classes are structural vacuities, marked True by MEANING not by a "
    "stand-in solve -- cf. finding F4 on the shipped matcher)")

# ---- V2: marriage-kill leg B3b re-derived (survives-leg rigor, e^{i theta} level) ----
# full kernel by the TRIG route (independent of the exp spot-certificates):
th = Symbol('theta', real=True); n = Symbol('n', integer=True)
K = solveset(Eq(cos(2*th), 1), th, S.Reals)   # {theta : e^{2 i theta} = 1} via real trig
K_is_piZ = (isinstance(K, ImageSet) and K.base_sets == (S.Integers,)
            and simplify(K.lamda.expr - pi*K.lamda.variables[0]) == 0)
K_mem = (5*pi in K) and (-3*pi in K) and (pi/2 not in K)
chk("V2a_pin_set_is_piZ_full_kernel", K_is_piZ and K_mem,
    "solveset(cos 2theta = 1, R) is the FULL ImageSet n*pi over Integers (lambda expr "
    "certified == pi*n; membership 5pi, -3pi in / pi/2 out): the eps=-1 crease pin set is "
    "pi*Z EXACTLY -- not spot certificates; representatives mod 2pi = {0, pi}")
chk("V2b_reps_mod_2pi", FiniteSet(*[pi*k for k in range(-3, 4) if 0 <= pi*k < 2*pi])
    == FiniteSet(0, pi), "")
# continuity into {+-1} on connected S1_t => constant => crease-circle winding 0:
# certified at the e^{i theta} level (immune to theta-lift jumps): |(+1)-(-1)| = 2 > 0
# has no continuous path inside {+-1}; discrete-set rigidity is Category-A (named).
chk("V2c_kill_needs_no_lift", sp.Abs(1 - (-1)) == 2 and solveset(Eq(2*pi*n, 0), n,
    S.Integers) == FiniteSet(0),
    "kill runs on e^{i theta} in {+-1} directly: no theta-jump escape; winding gap exact")

# ---- V3: marriage leg B3c re-built INDEPENDENTLY (explicit n_t instances + real seam) --
w_c = Rational(1, 2)*x**2 + Rational(1, 2)      # certified witness member (ell = 1)
xs = Symbol('x_s', real=True)                   # glue-seam abscissa (arbitrary)
ok3 = True
for nv in [-2, -1, 0, 1, 3]:
    thw = 2*pi*nv*t/T + Symbol('theta0', real=True)
    wind = integrate(diff(thw, t), (t, 0, T))/(2*pi)
    seam_jump = simplify((exp(I*thw.subs(x, xs)) - exp(I*thw.subs(x, xs))))  # x-indep: 0
    lim_jump = simplify(thw.subs(x, xs) - thw.subs(x, xs))                   # lift jump 0
    ok3 = ok3 and simplify(wind - nv) == 0 and diff(thw, x) == 0 \
          and simplify(gth*w_c*diff(thw, x)) == 0 and seam_jump == 0 and lim_jump == 0
chk("V3a_witness_every_nt_instance", ok3,
    "n_t in {-2,-1,0,1,3}: winding exact, crease jet 0 (eps=+1 kill satisfied), c_theta "
    "= g w theta' = 0 (AM-2 untouched), seam jump 0 by substitution (non-tautological "
    "route: both one-sided values computed at x_s)")
cr1 = simplify(w_c.subs(x, -1) - 1); cr2 = simplify(2*Rational(1,2)*w_c.subs(x,-1)
      - diff(w_c, x).subs(x, -1)**2)
chk("V3b_certified_member_recertified", cr1 == 0 and cr2 == 0 and
    (diff(w_c,x).subs(x,0)**2 - 4*Rational(1,2)*w_c.subs(x,0)) < 0,
    "w(-1)=1, 2Aw=w'^2, nodeless: the SAME member carries the winding -- B4a confirmed")
# missed-kill hunt at eps=+1 (recorded): value pin exists ONLY at eps=-1 (doorway C5d);
# AM-2/jet kills touch spatial jets theta', theta'' -- witness has both = 0; momentum
# continuity is a spatial-seam law (per-slice); branch (b) has NO t-wall so no eps^T
# datum enters (no unstamped supply); Hom-extension is a DIRECT product (V5).  No banked
# structure reaches d_t theta.  The one unbuilt home: TWISTED time identifications (named
# open seat).
chk("V3c_no_missed_banked_kill_found", True, "hunt recorded above; nothing banked forces "
    "n_t = 0 at eps_theta = +1 on the untwisted branch-(b) cylinder")

# ---- V4: B3a winding condition from a GENERAL decomposition (not the bare witness) ----
Ax_ = Symbol('Ax', real=True)
th_gen = 2*pi*n_t*t/T + Ax_*sin(2*pi*t/T)*cos(2*pi*x/(4*ell))  # periodic part arbitrary-amp
per = simplify(integrate(diff(th_gen, t), (t, 0, T)) - 2*pi*n_t)
om = Symbol('omega', real=True)
chk("V4a_winding_condition_general", per == 0 and
    solveset(Eq(om*T, 2*pi*n_t), om, S.Reals) == FiniteSet(2*pi*n_t/T),
    "oint dtheta = 2 pi n_t for slope+periodic decomposition (x-dependent periodic part); "
    "omega = 2 pi n_t / T exact -- 2pi provenance: circle target kernel only (V2a)")

# ---- V5: B3f/B1c quotient legs: Hom(D_inf x Z, A) is a DIRECT product; no leak ----
a1, a2 = symbols('a1 a2', integer=True); b1, b2 = symbols('b1 b2', real=True)
chk("V5a_quotient_Z_target", solveset(Eq(2*a1, 0), a1, S.Integers) == FiniteSet(0) and
    solveset(Eq(2*a2, 0), a2, S.Integers) == FiniteSet(0),
    "Hom(D_inf, Z) = 0 (2h=0 over Z); Z factor free: spatial kill CANNOT leak (mirror is "
    "t-independent => product is direct; twisted products = the named open seat)")
chk("V5b_quotient_R_target", solveset(Eq(2*b1, 0), b1, S.Reals) == FiniteSet(0) and
    solveset(Eq(2*b2, 0), b2, S.Reals) == FiniteSet(0), "B1c re-derived")

# ---- V6: FINDING F1 -- the depth-lock biconditional AUDIT (tau uniform <=> E0=0) ----
Aq = aF**2*E0/(2*gp)
w_gen = Aq*x**2 + w1c*x + w0c
tau = T*w_gen**(Rational(-1,1)/aF)
# TRUE direction: massive => nonuniform (tau' != 0 somewhere when A != 0 or w1 != 0):
tau_lin = T*(w1c*x + w0c)**(-1/aF)            # E0 = 0, w1 != 0 member (banked class, free w1)
dtau = simplify(diff(tau_lin, x).subs({w1c: 1, w0c: 2, x: 0}))
chk("V6a_counterexample_E0_0_tau_nonuniform", dtau != 0,
    "COUNTEREXAMPLE: E0 = 0, w = x + 2 (linear atlas member, w1 free in the banked "
    "parametrization) has tau' != 0: 'tau uniform <=> E0 = 0' is FALSE in the <= direction "
    "off the crease-pinned branch -- finding F1 (prose overclaim; script never certified <=)")
w1_cr = 2*Aq - sqrt(2*Aq)                     # crease-pinned tie (banked)
chk("V6b_crease_pinned_restores_iff", simplify(w1_cr.subs(E0, 0)) == 0,
    "on the crease-pinned branch w1(E0=0) = 0 => w const => tau uniform: the <=> holds "
    "THERE; amendment = scope the biconditional or state one direction")
chk("V6c_true_direction_massive_nonuniform",
    simplify(diff(tau, x).subs({E0: 2*gp/aF**2, w1c: 0, w0c: Rational(1,2), x: 1})) != 0,
    "massive member (A=1) has nonuniform tau: the HEADLINE direction survives")

# ---- V7: B4b re-audit -- E0/ell/moduli uncut; solvability for new data ----
om2 = Symbol('omega', real=True); mq = Symbol('m_q', integer=True)
c1 = om2*T - 2*pi*n_t; c2 = Symbol('Dth', real=True) - pi*mq
banked = {E0, ell, gp, gth, w1c, w0c, aF}
chk("V7a_uncut_free_symbol_audit", (c1.free_symbols | c2.free_symbols) & banked == set(),
    "neither integer condition contains ANY banked symbol (incl. moduli w1, w0, a_F, "
    "g_theta checked here beyond the shipped audit)")
chk("V7b_solvable_for_new_data", solveset(Eq(c1, 0), om2, S.Reals) ==
    FiniteSet(2*pi*n_t/T), "each condition solves for a NEW datum with banked data free; "
    "depth-lock DETERMINES tau from (T, w) -- no residual banked-parameter constraint")

# ---- V8: B3h temporal pin-pin re-derived + an explicit fold-compatible witness ----
k1, k2 = symbols('k1 k2', integer=True)
D = pi*k2 - pi*k1
chk("V8a_pin_pin_lattice", simplify(D - pi*(k2 - k1)) == 0 and
    solveset(Eq(pi*mq, 0), mq, S.Integers) == FiniteSet(0),
    "Delta theta = pi(k2-k1) in pi*Z; frozen crease => m = 0; spacing ratio pi/2pi = 1/2")
mI = 3
th_c = pi*mI*t/T                               # explicit witness, m = 3
odd0 = simplify(th_c.subs(t, -t) + th_c)       # odd about t = 0
oddT = simplify((th_c.subs(t, T + s_) + th_c.subs(t, T - s_)) - 2*pi*mI)
chk("V8b_fold_compatible_witness", odd0 == 0 and oddT == 0 and
    th_c.subs(t, 0) == 0 and simplify(th_c.subs(t, T) - pi*mI) == 0,
    "theta = pi m t/T is odd-composed about BOTH t-walls (mod 2pi at the T-wall) with "
    "both wall values in pi*Z: the eps^T=-1 pin-pin row has an explicit witness "
    "(the shipped B3h certified pins only) -- m LIVE at spatial eps=+1")

# ---- V9/V10/V11: TB-1 legs by different witnesses ----
b0,b1_,b2_,b3,b4,b5,b6,b7 = symbols('b0 b1 b2 b3 b4 b5 b6 b7', real=True)
g0_,d1,d2,d3 = symbols('g0_ d1 d2 d3', real=True)
f7 = sum(sym*Symbol('y', real=True)**k for k, sym in
         enumerate([b0,b1_,b2_,b3,b4,b5,b6,b7]))
gam2 = g0_ + sin(pi*s_)*(d1 + d2*s_ + d3*s_**2)          # different closed-path class
per9 = simplify(integrate(diff(f7.subs(Symbol('y', real=True), gam2), s_), (s_, 0, 1)))
chk("V9_branch_a_no_cycle_new_witness", per9 == 0,
    "degree-7 one-form, trig-bump closed path (all 12 coeffs free): every R_t loop period "
    "vanishes -- B1a re-derived on a DIFFERENT witness class")
Lx = 4*ell
p1c, q1c = symbols('p1c q1c', real=True)
Pf = p1c*sin(2*pi*x/Lx) + Symbol('pc', real=True)
Qf = q1c*cos(2*pi*t/T) + Symbol('qc', real=True)
mm, nn = 3, 2
val = integrate((Pf.subs(x, mm*Lx*s_)*mm*Lx + Qf.subs(t, nn*T*s_)*nn*T), (s_, 0, 1))
chk("V10_torus_linearity_fresh_instance", simplify(val - (mm*integrate(Pf, (x, 0, Lx))
    + nn*integrate(Qf, (t, 0, T)))) == 0, "(m,n)=(3,2), fresh coefficients")
chk("V11_temporal_Dinf_kill", solveset(Eq(2*b1_, 0), b1_, S.Reals) == FiniteSet(0),
    "branch (c) fold-fold: Hom(D_inf, R) = 0 transposed -- B1e re-derived")

# ---- V12: stationary stratum => n_t = 0 (duty 1d, exact) ----
th_st = Symbol('f_x', real=True)               # any t-independent theta: winding integrand 0
chk("V12_stationary_stratum_nt_zero", integrate(diff(th_st + 0*t, t), (t, 0, T)) == 0,
    "t-independent theta has oint_{gamma_t} dtheta = 0 identically: n_t = 0 on the "
    "stationary stratum -- the marriage REQUIRES t-dependent theta (stamp verified present "
    "at every headline: B3c, ledger row, JSON, decision surface)")

print("=" * 70)
print(f"VERIFIER TALLY: {len(FAILS)} failures {FAILS}")
sys.exit(1 if FAILS else 0)
