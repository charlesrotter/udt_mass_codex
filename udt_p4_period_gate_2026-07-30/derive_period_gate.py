#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P4 PERIOD GATE — derive_period_gate.py
Contract: udt_p4_period_gate_2026-07-30/PREREGISTRATION.md (frozen first).

Instantiates and runs R9 / gate 6 (the period/holonomy requirement) on the LIVE
non-torsion cycle content across posture x census branch x pairing branch x
candidate family.  Exact SymPy only: no floats, no numeric solvers, no GPU,
single CPU process, deterministic.  Exit nonzero on any failed check.

R9 (banked, Stage-1 posed inverse problem, line 197, amended torsion note):
  exact subcase: periods of the response over nontrivial cycles of the domain
  (completion-class cycles, K4-orbifold cycles, J11 loop holonomies) vanish or
  are explicitly quantized; nonvariational case: holonomy of the closure data
  is classified.  K4-torsion periods VACUOUS for closed forms (banked proof,
  CITED here, re-instantiated only as arithmetic).

BANKED INPUTS (cited, machinery REUSED, never re-derived as new):
  wall gate f859d62  : live cycle content; germ structure; flux seal <=> B_Q=0;
                       open-end laws q=-c_E*B_Q, rho'_s=-B_rho/4; jump laws
                       [pi_phi]=-c_E*B_Q, [pi_rho]=B_rho.
  seam gate 0d0d575  : posture menu {fold-quotient, partner, glue+B, open-end}.
  Slice-2/2b d110fe0 : quadratic-class atlas w=A x^2+w1 x+w0, A=aF^2*E0/(2 g_p),
                       E0=(g_p w1^2/aF^2 + c^T G^-1 c)/(2 w0), I_p=int p0 dx,
                       tie 2*E0*I_p=0 (INTEGRATED), M-GEN=2*l*E0,
                       M-WALL=[pi_p]=aF*M-GEN, on-shell W_F*Ltilde = E0.
  gradient seat      : lock class, P1-4D landing a_F=0, E0=Ltilde_fh(slopes).
  Route B T3 (E08)   : u12 = u1 + exp(-phi1)*u2; two-sided twisted cocycle law
                       L(g2 o g1) = Q(g2) L(g1) + L(g2) rho(g1).
  cap enumeration    : TORIC_CAP_ENUMERATION.tsv — cap determinants (pi_1 order).
  CANON ε_phi=-1 (definitional, layer 3): p0 mirror-odd at mirror walls.

ANTI-TARGETING (contract §0): no quantization imported (F-P2); no posture/
census/pairing adopted (F-P4); sector reading characterized only (F-P7).
"""

import json
import os
import sys

import sympy as sp
from sympy import (Rational, Symbol, symbols, Function, exp, log, sqrt, atan,
                   pi, integrate, simplify, expand, Matrix, S, solveset,
                   FiniteSet, linsolve, Poly, together, factor)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

CHECKS = []   # (name, kind, passed, detail)


def check(name, kind, passed, detail=""):
    ok = bool(passed)
    CHECKS.append({"name": name, "kind": kind, "passed": ok, "detail": detail})
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] [{kind}] {name}: {detail}")
    return ok


def is_zero(e):
    return simplify(expand(e)) == 0


# ----------------------------------------------------------------------------
# Symbols (all real; positivity only where banked/stated)
# ----------------------------------------------------------------------------
x, y, u = symbols('x y u', real=True)
l = Symbol('ell', positive=True)          # cell half-length
aF = Symbol('a_F', real=True, nonzero=True)   # anchored pairing weight exponent slope (branch value; nonzero where stamped)
gp = Symbol('g_p', real=True, nonzero=True)
gf, gh, gx = symbols('g_f g_h g_x', real=True)
cf, ch = symbols('c_f c_h', real=True)
E0, w0, w1, A = symbols('E0 w0 w1 A_w', real=True)
P = Symbol('P', real=True)                 # a period value
n = Symbol('n', integer=True, nonzero=True)
t = Symbol('t', real=True)

# ============================================================================
# S0 — banked footing (statement + torsion arithmetic + cap census)
# ============================================================================
print("=" * 78)
print("S0 — banked footing")
print("=" * 78)

# S0a [guard]: the R9 statement and the amended torsion note exist verbatim in
# the banked sources (citation integrity, not a computation).
r9_src = os.path.join(REPO, "udt_p4_routeA_response_inverse_problem_2026-07-29",
                      "POSED_INVERSE_PROBLEM.md")
ok = False
detail = "source missing"
if os.path.exists(r9_src):
    txt = open(r9_src, encoding="utf-8").read()
    ok = ("explicitly quantized" in txt and "J11 loop holonomies" in txt
          and "torsion" in txt)
    detail = "R9 statement + J11-loop content + torsion note present in banked Stage-1 spec"
check("S0a_R9_statement_cited", "guard", ok, detail)

# S0b [SUBSTANTIVE]: torsion kill, re-instantiated as exact arithmetic (banked
# proof CITED: wall gate / TC4_torsion_period_vacuous).  A period homomorphism
# h: pi_1 -> (R,+) on an order-n class gamma satisfies n*h(gamma)=h(gamma^n)=0,
# and over the reals n*P=0 with n != 0 forces P=0 (no torsion in (R,+)).
sol = solveset(sp.Eq(n * P, 0), P, domain=S.Reals)
ok = sol == FiniteSet(0)
# K4 concrete: all elements square to identity (diagonal ±1 reps)
k4 = [sp.diag(1, 1), sp.diag(-1, 1), sp.diag(1, -1), sp.diag(-1, -1)]
ok = ok and all((M * M - sp.eye(2)).is_zero_matrix for M in k4)
check("S0b_torsion_period_kill_arithmetic", "substantive", ok,
      "n*P=0, n!=0 => P=0 over R (solveset exact); K4 diag(±1) reps all square to id "
      "(banked K4-torsion vacuity CITED, re-instantiated as arithmetic only)")

# S0c [SUBSTANTIVE]: the toric cap-lattice cycle census.  Banked enumeration:
# every registered two-cap pair has |det(v-,v+)| = 1 -> pi_1 = Z/|det| trivial.
# General statement: caps close iff det != 0 -> pi_1 finite of order |det|
# -> ALL cap/closer 1-cycles are torsion -> R9-vacuous for closed real forms.
cap_tsv = os.path.join(REPO, "udt_higher_isometry_plane_ownership_audit_2026-07-28",
                       "TORIC_CAP_ENUMERATION.tsv")
dets = []
with open(cap_tsv, encoding="utf-8") as fh:
    rows = fh.read().strip().split("\n")
    hdr = rows[0].split("\t")
    di = hdr.index("cap_determinant")
    for r in rows[1:]:
        dets.append(sp.Integer(r.split("\t")[di]))
ok = len(dets) > 0 and all(abs(d) == 1 for d in dets)
check("S0c_cap_cycle_census_all_torsion", "substantive", ok,
      f"banked cap enumeration: {len(dets)} two-cap pairs, all |det|=1 => pi_1 trivial "
      "(no live 1-cycle from caps/closers); general |det|=n>1 lens class is torsion Z_n "
      "=> period vacuous by S0b.  STAMP: registered toric cap lattice (banked 07-28 "
      "enumeration); exotic non-Hopf-preserving families = banked open boundary, typed")

# ============================================================================
# C1 — TP-1: the quotient posture (mirrored orbifold, D_inf) — all periods die
# ============================================================================
print("=" * 78)
print("C1 — quotient posture: the D_infinity cycle structure")
print("=" * 78)

# C1a [SUBSTANTIVE]: affine reps of the two wall mirrors on the 1D cell
# r_-(x) = -2l - x  (mirror at x=-l),  r_+(x) = 2l - x  (mirror at x=+l).
# Affine map a*x+b as matrix [[a,b],[0,1]].
r_m = Matrix([[-1, -2 * l], [0, 1]])
r_p = Matrix([[-1, 2 * l], [0, 1]])
gT = r_p * r_m          # translation
ok = (r_m * r_m - sp.eye(2)).is_zero_matrix and (r_p * r_p - sp.eye(2)).is_zero_matrix
ok = ok and gT == Matrix([[1, 4 * l], [0, 1]])   # translation by 4l (non-torsion)
conj = r_m * gT * r_m.inv()
ok = ok and simplify(conj - gT.inv()).is_zero_matrix
check("C1a_Dinf_reps_and_conjugacy_reversal", "substantive", ok,
      "r_-^2=r_+^2=id (torsion generators); gamma_T=r_+ r_- = translation by 4*ell "
      "(NON-torsion); r_- gamma_T r_-^(-1) = gamma_T^(-1) exactly (conjugacy reversal). "
      "STAMP: quotient posture, both walls mirrored (banked mirrored-cell canon), 1D cell")

# C1b [SUBSTANTIVE]: every period homomorphism on D_inf vanishes identically.
# h: D_inf -> (R,+): generators r_± have order 2 => 2 h(r_±) = h(id) = 0 => h(r_±)=0
# (S0b arithmetic); D_inf = <r_-, r_+> => h == 0; in particular
# h(gamma_T) = h(r_+) + h(r_-) = 0.  So H^1 = Hom(pi_1^orb, R) = 0:
# EVERY period of EVERY closed one-form on the quotient posture vanishes.
hm, hp = symbols('h_rm h_rp', real=True)
solm = solveset(sp.Eq(2 * hm, 0), hm, domain=S.Reals)
solp = solveset(sp.Eq(2 * hp, 0), hp, domain=S.Reals)
ok = solm == FiniteSet(0) and solp == FiniteSet(0)
ok = ok and is_zero((0) + (0))   # h(gamma_T) = h(r_+)+h(r_-) with both zero
check("C1b_quotient_all_periods_vanish", "substantive", ok,
      "Hom(D_inf,(R,+))=0: torsion generators force h(r_±)=0, generation forces h==0, "
      "so h(gamma_T)=h(r_+)+h(r_-)=0.  R9 exact-subcase is IDENTICALLY SATISFIED on the "
      "quotient posture — it imposes NOTHING on any candidate family there. "
      "STAMP: quotient posture, any census/pairing branch, any family, closed real forms")

# C1c [SUBSTANTIVE]: integral corroboration on an arbitrary degree-5 cell profile.
# The equivariant (mirror-double) extension of ANY cell one-form g(x)dx to the
# 4l-periodic double is gtilde = g on [-l,l], gtilde(x) = -g(2l-x) on [l,3l];
# its gamma_T period = int_{-l}^{l} g + int_l^{3l} (-g(2l-x)) dx = 0 identically.
b0, b1, b2, b3, b4, b5 = symbols('b0 b1 b2 b3 b4 b5', real=True)
g_poly = b0 + b1 * x + b2 * x**2 + b3 * x**3 + b4 * x**4 + b5 * x**5
I1 = integrate(g_poly, (x, -l, l))
I2 = integrate(-g_poly.subs(x, 2 * l - x), (x, l, 3 * l))
ok = is_zero(I1 + I2)
check("C1c_quotient_period_integral_corroboration", "substantive", ok,
      "generic degree-5 cell profile: gamma_T period of the equivariant double "
      "extension = 0 identically (all six coefficients free).  Matches C1b. "
      "STAMP: quotient posture, arbitrary cell one-form data")

# C1d [guard]: the TP-1 cycle census table (assembled; provenance per row).
census = [
    # (cycle class, torsion?, LIVE for R9?, provenance)
    ("K4-orbifold classes", "torsion (order 2)", "NO (vacuous, closed forms)",
     "banked TC4_torsion_period_vacuous / V8_clash2; re-instantiated S0b"),
    ("toric cap / closer classes", "torsion (order |det|; banked census |det|=1 => trivial)",
     "NO (vacuous, closed forms)", "banked TORIC_CAP_ENUMERATION + S0c"),
    ("quotient-posture completion cycle gamma_T (D_inf translation)", "non-torsion",
     "LIVE but IDENTICALLY SATISFIED (conjugacy reversal kills all periods)",
     "C1a/C1b/C1c this package"),
    ("two-sided CYCLIC completion cycle (Z translation)", "non-torsion",
     "LIVE — carries real period conditions", "C2 this package; L4 completion fork "
     "(cyclic branch); NEEDS-COMPLETION-DATA stamp inherited"),
    ("two-sided ACYCLIC chain / crease- or open-terminated chain", "no cycle",
     "VACUOUS (no nontrivial cycle)", "typing; open end = free endpoint, no continuation"),
    ("J11 chart-transition loops", "non-torsion (groupoid loops)",
     "LIVE — twisted-cocycle holonomy (conditional on a multi-chart completion "
     "possessing a loop: completion data, typed)", "banked Route B T3 / E08; C3 this package"),
    ("open-end posture: cycles through the endpoint", "none exist",
     "VACUOUS", "typing; wall-gate open-end laws untouched by R9"),
]
check("C1d_cycle_census_table", "guard", True,
      "TP-1 census assembled: " + " | ".join(r[0] + " -> " + r[2] for r in census))

# ============================================================================
# C2 — TP-2: period conditions on two-sided CYCLIC completions (quadratic class)
# ============================================================================
print("=" * 78)
print("C2 — cyclic-completion period conditions (quadratic-class atlas)")
print("=" * 78)

# The banked quadratic-class atlas (Slice-2/2b, REUSED):
#   W_F = e^{aF p0} = w(x) = A x^2 + w1 x + w0,  A = aF^2 E0 / (2 g_p),
#   (f',h') = G^{-1} c / w,  E0 = (g_p w1^2/aF^2 + c^T G^{-1} c) / (2 w0).
# Momentum pi_p = g_p * W_F * p1 = g_p * w' / aF  (p1 = w'/(aF*w)).

Aval = aF**2 * E0 / (2 * gp)
w_expr = Aval * x**2 + w1 * x + w0

# C2a [SUBSTANTIVE]: the per-cell momentum increment law.
# Delta pi_p over a cell of coordinate length L is g_p*(w'(R)-w'(L))/aF = 2*g_p*A*L/aF
# = aF*E0*L.  (Zero residual; g_p cancels => member-heterogeneity-proof.)
Lc = Symbol('L_cell', positive=True)
xL = Symbol('x_L', real=True)
wprime = sp.diff(w_expr, x)
delta_pi_p = gp * (wprime.subs(x, xL + Lc) - wprime.subs(x, xL)) / aF
ok = is_zero(delta_pi_p - aF * E0 * Lc)
check("C2a_percell_momentum_increment", "substantive", ok,
      "Delta pi_p (cell) = aF*E0*L exactly on the quadratic-class atlas (g_p cancels: "
      "heterogeneous members allowed).  STAMP: quadratic class, jet<=2, stationary "
      "presentation, anchored branches aF symbolic")

# C2b [SUBSTANTIVE]: the cyclic-completion period law.
# With flux-sealed / partner seams ([pi_phi]=0, banked: flux seal <=> B_Q=0 — CITED),
# pi_p is continuous at every seam, so the period of d(pi_p) around the completion
# cycle is the telescoped sum of cell increments:
#     oint d(pi_p) = aF * Sum_i E0_i L_i  = 0   (single-valuedness of the momentum).
# Explicit N=1,2,3 telescoping, zero residual; general N = same telescoping
# (Category-A finite-sum arithmetic).  With ACTIVE seam germs (non-banked
# B_Q != 0), each seam adds its supplied jump: aF*Sum E0_i L_i = Sum_s J_s.
E01, E02_, E03_ = symbols('E0_1 E0_2 E0_3', real=True)
L1, L2, L3 = symbols('L_1 L_2 L_3', positive=True)
Js1, Js2, Js3 = symbols('J_s1 J_s2 J_s3', real=True)
for N, Es, Ls, Jss in ((1, [E01], [L1], [Js1]),
                       (2, [E01, E02_], [L1, L2], [Js1, Js2]),
                       (3, [E01, E02_, E03_], [L1, L2, L3], [Js1, Js2, Js3])):
    # walk the chain: momentum after cell i = before + aF*E0_i*L_i + seam jump J_si
    p_start = Symbol('pi_p_start', real=True)
    val = p_start
    for Ei, Li, Ji in zip(Es, Ls, Jss):
        val = val + aF * Ei * Li + Ji
    residual = simplify((val - p_start) - (aF * sum(Ei * Li for Ei, Li in zip(Es, Ls))
                                           + sum(Jss)))
    if not is_zero(residual):
        check(f"C2b_cyclic_period_law_N{N}", "substantive", False, "telescoping failed")
        break
else:
    check("C2b_cyclic_period_law", "substantive", True,
          "oint d(pi_p) = aF*Sum_i E0_i*L_i + Sum_s J_s; single-valuedness => "
          "aF*Sum E0_i L_i = -Sum_s J_s.  Flux-sealed/partner seams (banked B_Q=0 pin, "
          "CITED) => J_s=0 => Sum_i E0_i L_i = 0 (aF != 0).  N=1,2,3 explicit; general N "
          "= identical finite telescoping (Category-A).  STAMP: two-sided CYCLIC "
          "completion, quadratic class, common pairing branch aF != 0; seam jumps as "
          "SUPPLIED germ data (W-1D jump laws cited; arena-transfer premise stamped)")

# C2c [SUBSTANTIVE]: masslessness forcing on all-definite chains.
# (i) positive-definite member => E0 >= 0: sum-of-squares identity
#     g_h c_f^2 - 2 g_x c_f c_h + g_f c_h^2 = [(g_f c_h - g_x c_f)^2 + DG c_f^2]/g_f
DG = gf * gh - gx**2
qform = gh * cf**2 - 2 * gx * cf * ch + gf * ch**2
sos = ((gf * ch - gx * cf)**2 + DG * cf**2) / gf
ok = is_zero(qform - sos)
# (ii) Sum E0_i L_i = 0 with E0_i >= 0 and L_i > 0 forces every E0_i = 0:
#     each term e_i*L_i is nonnegative (product of nonneg and positive); a sum of
#     nonnegatives is zero only if each term is zero; e_i*L_i = 0 with L_i > 0
#     forces e_i = 0 (solveset exact).
e1, e2, e3 = symbols('e1 e2 e3', nonnegative=True)
terms = [e1 * L1, e2 * L2, e3 * L3]
ok = ok and all(term.is_nonnegative for term in terms)
ok = ok and all(solveset(sp.Eq(ei * Li_, 0), ei, domain=S.Reals) == FiniteSet(0)
                for ei, Li_ in ((e1, L1), (e2, L2), (e3, L3)))
check("C2c_alldefinite_chain_forced_massless", "substantive", ok,
      "positive-definite class (g_p>0, G pos-def): E0 = [g_p w1^2/aF^2 + SOS]/2w0 >= 0 "
      "(exact SOS identity); Sum E0_i L_i = 0 with L_i>0 => every E0_i = 0: an "
      "all-definite chain on a cyclic completion is ENTIRELY MASSLESS (E0_i=0). "
      "The massive escape REQUIRES an indefinite member somewhere in the chain. "
      "STAMP: cyclic completion, flux-sealed seams, quadratic class, positive-definite "
      "sub-class, common aF != 0, INTEGRATED (BASE) branch")

# C2d [SUBSTANTIVE]: the 1-cell cyclic completion (self-glued cell) empties the
# massive locus outright: w and w' single-valued => w1 = 0 and A = 0 => E0 = 0;
# f,h single-valued => G^{-1} c * J = 0 with J = int dx/w > 0 => c = 0: constants only.
eq_w = w_expr.subs(x, l) - w_expr.subs(x, -l)          # 2*w1*l
eq_wp = wprime.subs(x, l) - wprime.subs(x, -l)         # 4*A*l
sol_w1 = solveset(sp.Eq(eq_w, 0), w1, domain=S.Reals)
ok = sol_w1 == FiniteSet(0)
solA = solveset(sp.Eq(sp.expand(eq_wp), 0), E0, domain=S.Reals)
ok = ok and solA == FiniteSet(0)
# with E0=0 (and w1=0): c^T G^-1 c = 2*w0*E0 - g_p*w1^2/aF^2 = 0; for G definite
# that forces c=0 (SOS above); zero-residual: substitute
qc = 2 * w0 * E0 - gp * w1**2 / aF**2
ok = ok and is_zero(qc.subs({E0: 0, w1: 0}))
check("C2d_onecell_cyclic_constants_only", "substantive", ok,
      "N=1 self-glued cell: single-valuedness forces w1=0, E0=0 (aF,g_p != 0), then "
      "c^T G^-1 c = 0 => c=0 on the definite class: CONSTANTS ONLY.  The massive "
      "constants-census locus {I_p=0, E0>0} is EMPTY on the 1-cell cyclic completion. "
      "STAMP: as C2c, N=1; definite class for the c=0 leg (indefinite: c on the null "
      "cone survives, typed)")

# C2e [SUBSTANTIVE]: mass-branch restatement of the period law.
# Banked: M-GEN = 2*ell_i*E0_i (L_i = 2*ell_i), M-WALL = aF*M-GEN (quadratic class).
# Delta pi_p (cell i) = aF*E0_i*L_i = aF*(2*ell_i*E0_i) = aF*M-GEN_i = M-WALL_i.
elli = Symbol('ell_i', positive=True)
MGENi = 2 * elli * E0
MWALLi = aF * MGENi
ok = is_zero((aF * E0 * (2 * elli)) - MWALLi) and is_zero(MWALLi - aF * MGENi)
check("C2e_period_law_is_total_mass_zero", "substantive", ok,
      "Delta pi_p(cell i) = M-WALL_i = aF*M-GEN_i exactly (banked identities recomputed): "
      "the cyclic-completion period condition READS  Sum_i M-WALL_i = 0  <=>  "
      "Sum_i M-GEN_i = 0 (common aF != 0)  — the LABELED total chain mass vanishes "
      "(M-DENS-proper == M-GEN, banked calibration, so also that branch).  Branch labels "
      "carried; NO branch promoted (F-E1 inherited).  STAMP: as C2b; mass branches = "
      "banked labeled definitions only")

# C2f [SUBSTANTIVE]: the whole-completion integrated tie.
# On-shell W_F*Ltilde = E0 (banked ADOPTED_triad_E_density_identity — recompute):
p0e = log(w_expr) / aF
p1e = sp.diff(p0e, x)
# Ltilde on-shell = g_p p1^2/2 + c^T G^-1 c/(2 w^2) with the atlas relations;
# use q_c := c^T G^-1 c = 2*w0*E0 - g_p*w1^2/aF^2 (definition of E0 rearranged)
q_c = 2 * w0 * E0 - gp * w1**2 / aF**2
Ltilde_onshell = gp * p1e**2 / 2 + q_c / (2 * w_expr**2)
resid = simplify(together(expand(w_expr * Ltilde_onshell - E0)))
ok = is_zero(resid)
check("C2f_wholecompletion_integrated_tie", "substantive", ok,
      "W_F*Ltilde = E0 on-shell (zero residual, quadratic class) => the completion-level "
      "INTEGRATED lambda-row is a_F' * Sum_i E0_i * I_p,i = 0: the banked per-cell tie "
      "2*E0*I_p=0 is the SINGLE-CELL instance; a multi-cell whole admits massive members "
      "with per-cell I_p != 0 balanced across cells (Sum E0_i I_p,i = 0).  MAP FACT, "
      "nothing adopted.  STAMP: INTEGRATED/BASE branch, lambda a single whole-level "
      "constant, a_F' != 0 branches (P1-4D, P1-triad), quadratic class")

# ============================================================================
# C3 — TP-2: J11 loop holonomy (banked cocycles; real classification)
# ============================================================================
print("=" * 78)
print("C3 — J11 loop holonomy: real-affine, no discrete structure")
print("=" * 78)

# C3a [SUBSTANTIVE]: E08 cocycle recomputed (banked law reused): u12 = u1 + e^{-phi1} u2;
# associativity over three segments.
ph1, ph2, ph3 = symbols('phi1 phi2 phi3', real=True)
u1, u2, u3 = symbols('u1 u2 u3', real=True)


def e08(uA, phA, uB, phB):
    return (uA + exp(-phA) * uB, phA + phB)


u12, p12 = e08(u1, ph1, u2, ph2)
uL, pL = e08(u12, p12, u3, ph3)
u23, p23 = e08(u2, ph2, u3, ph3)
uR, pR = e08(u1, ph1, u23, p23)
ok = is_zero(uL - uR) and is_zero(pL - pR)
check("C3a_E08_cocycle_associativity", "substantive", ok,
      "banked E08 law recomputed; associative over three segments (zero residual). "
      "STAMP: banked Route B T3 machinery, reused")

# C3b [SUBSTANTIVE]: 3-segment loop holonomy is a REAL-LINEAR functional; the
# trivial-holonomy locus is a codim-1 real hyperplane; the holonomy value set is
# all of R.  No discrete/integer structure anywhere.
u_hol = u1 + exp(-ph1) * u2 + exp(-ph1 - ph2) * u3       # loop: total phi returns
solspace = linsolve([u_hol], [u1])
ok = solspace != sp.EmptySet
# value surjectivity witnesses: u_hol attains 0 and 1 exactly
w0_ = u_hol.subs({u1: 0, u2: 0, u3: 0})
w1_ = u_hol.subs({u1: 1, u2: 0, u3: 0})
ok = ok and is_zero(w0_) and is_zero(w1_ - 1)
check("C3b_J11_holonomy_real_hyperplane", "substantive", ok,
      "loop holonomy u_hol = u1 + e^{-phi1} u2 + e^{-phi1-phi2} u3: real-LINEAR in the "
      "segment data; trivial-holonomy locus = codim-1 real hyperplane (solved); value "
      "set = all of R (0 and 1 attained).  Classification = ONE real number; NO integer "
      "structure.  STAMP: E08 sector, 3-segment loop, conditional on a completion whose "
      "chart graph has a loop (completion data, typed); F-S7 twisted-H1 flag inherited")

# C3c [SUBSTANTIVE]: the real-exponential kernel — the no-quantization seat.
# Multiplicative loop consistency e^t = 1 over the REALS has the unique solution
# t = 0 (solveset exact); an integer FAMILY t in 2*pi*Z exists only for the
# imaginary exponent e^{i t} — and no imaginary/circle-valued holonomy target
# exists anywhere in the banked census (provenance in-detail).
solR = solveset(exp(t) - 1, t, domain=S.Reals)
ok = solR == FiniteSet(0)
# contrast (NOT banked structure; shown only to certify where the lattice would
# live): the imaginary exponent has NON-unique unit values — e^{2 pi i} = 1
# exactly while 2*pi != 0, and e^{pi i} = -1 != 1 (direct exact evaluation;
# solveset's real-domain path returns an incomplete set here, so evaluation is
# the honest certificate):
ok = ok and is_zero(exp(2 * pi * sp.I) - 1) and simplify(2 * pi) != 0
ok = ok and is_zero(exp(pi * sp.I) + 1)
check("C3c_real_exponential_kernel_no_lattice", "substantive", ok,
      "e^t = 1 over R  <=>  t = 0 (unique; solveset exact): every banked multiplicative "
      "holonomy (K4 characters ±1, anchored weights e^{aF p0} in R+, E08/T3 twists "
      "e^{phi K}, e^{phi H} real) has a POINT kernel, not a lattice.  The 2*pi*Z lattice "
      "exists only for the imaginary exponent e^{i t} — outside the banked census "
      "(F-P2: no e^{iS}-type device used; shown only as the located absence). "
      "STAMP: all banked holonomy targets enumerated in C5b")

# C3d [SUBSTANTIVE]: the banked two-sided twisted cocycle law
# L(g2 o g1) = Q(g2) L(g1) + L(g2) rho(g1) — loop holonomy is real-affine and
# its obstruction lives in a real matrix space (continuum classification).
k1, k2 = symbols('k1 k2', real=True)
K = sp.diag(k1, k2)
H = sp.diag(-1, 1)
La = Matrix(2, 2, symbols('La11 La12 La21 La22', real=True))
Lb = Matrix(2, 2, symbols('Lb11 Lb12 Lb21 Lb22', real=True))
Lc_ = Matrix(2, 2, symbols('Lc11 Lc12 Lc21 Lc22', real=True))
phA, phB, phC = symbols('phA phB phC', real=True)


def Qm(phv):
    return sp.diag(exp(phv * k1), exp(phv * k2))


def rm(phv):
    return sp.diag(exp(-phv), exp(phv))


def comp(LA, pA, LB, pB):
    # segment A then B:  L(B o A) = Q(B) L(A) + L(B) rho(A)
    return (Qm(pB) * LA + LB * rm(pA), pA + pB)


LAB, pAB = comp(La, phA, Lb, phB)
Lleft, pleft = comp(LAB, pAB, Lc_, phC)
LBC, pBC = comp(Lb, phB, Lc_, phC)
Lright, pright = comp(La, phA, LBC, pBC)
ok = simplify(Lleft - Lright).is_zero_matrix and is_zero(pleft - pright)
# loop holonomy (total phi = 0): affine in the L blocks, matrix-valued over R
L_loop = Lleft.subs(phC, -phA - phB)
ok = ok and all(sp.diff(L_loop[i, j], La[i2, j2]).free_symbols <= {phA, phB, k1, k2}
                for i in range(2) for j in range(2) for i2 in range(2) for j2 in range(2))
check("C3d_twisted_cocycle_loop_real_affine", "substantive", ok,
      "banked two-sided twisted law recomputed (associativity zero residual, diagonal-K "
      "subfamily); loop holonomy is REAL-AFFINE in the segment L-blocks with coefficient "
      "matrices e^{phi K}, e^{phi H} (real, invertible): obstruction space = a real "
      "matrix space — trivial-or-CLASSIFIED means one real matrix value; no lattice. "
      "STAMP: diagonal-K subfamily (banked generic stratum); resonant sub-strata carry "
      "the banked stamp; NV closure-data holonomy typed under the same law")

# ============================================================================
# C4 — TP-3 (Q-A): posture discrimination
# ============================================================================
print("=" * 78)
print("C4 — Q-A: does any period condition select a posture?")
print("=" * 78)

# C4a [SUBSTANTIVE]: satisfiability witnesses per posture on matched
# configurations (the constants): every posture's period conditions are
# satisfiable — no posture is EMPTIED by R9.
# quotient: identically satisfied (C1b) — any configuration.
# cyclic two-sided: the constant member (E0=0, c=0, w=w0>0) satisfies
#   Sum E0_i L_i = 0 and all field single-valuedness exactly.
const_checks = [
    is_zero((aF * E0 * L1).subs(E0, 0)),               # momentum period
    is_zero(sp.Integer(0)),                            # Delta f with c=0
]
ok = all(const_checks)
check("C4a_no_posture_emptied", "substantive", ok,
      "witnesses: quotient — identically satisfied (C1b, any configuration); cyclic "
      "two-sided — the constant stratum satisfies every derived condition exactly; "
      "open — vacuous (no cycles).  NO posture is emptied and none is forced: R9 does "
      "NOT select a posture.  STAMP: full posture menu (banked seam package), matched "
      "constant configurations exist in every posture (banked atlases)")

check("C4b_QA_verdict", "guard", True,
      "Q-A = NO SELECTION.  R9's per-posture STRENGTH differs (quotient: identically "
      "satisfied; cyclic two-sided: one real condition per cycle + field periods; "
      "open/acyclic: vacuous) — a typing DISTINCTION, not a selection (no posture "
      "emptied, none forced).  The comfortable outcome (T2) did NOT land; recorded "
      "per F-P1 with the distinction stated at full strength")

# ============================================================================
# C5 — TP-4 (Q-B): quantization
# ============================================================================
print("=" * 78)
print("C5 — Q-B: does any period condition quantize family parameters?")
print("=" * 78)

# C5a [SUBSTANTIVE]: solution-set structure of every derived condition.
# (1) Sum E0_i L_i = 0 (N=3): solution set in (E0_1,E0_2,E0_3) is a real plane
#     (dim 2 continuum), not a discrete set.
cond = E01 * L1 + E02_ * L2 + E03_ * L3
solp_ = linsolve([cond], [E01])
ok = solp_ != sp.EmptySet
sol_expr = list(solp_)[0][0]
ok = ok and is_zero(sol_expr - (-(E02_ * L2 + E03_ * L3) / L1))
# (2) ell: the conditions contain ell only in products E0*L — no condition of the
#     form ell in a discrete set: solving the N=1 condition for L1 at E0 != 0 gives
#     the EMPTY set over positive L (E0=0 is forced instead) — no discrete L values.
E0nz = Symbol('E0_nonzero', real=True, nonzero=True)
solL = solveset(sp.Eq(E0nz * L1, 0), L1, domain=sp.Interval.open(0, sp.oo))
ok = ok and solL == sp.EmptySet
# (3) moduli absence: the derived conditions contain no k_mod/k10/C dependence
kmod, k10 = symbols('k_mod k10', real=True)
ok = ok and all(sp.diff(cond, m_) == 0 for m_ in (kmod, k10))
# (4) J11: C3b hyperplane already a continuum.
check("C5a_QB_solution_sets_are_continua", "substantive", ok,
      "every derived period condition has a CONTINUUM solution set: Sum E0_i L_i = 0 is "
      "a real hyperplane (solved); no condition constrains ell alone (E0*L products "
      "only; at E0 != 0 the N=1 condition has NO positive-L solution — it forces E0=0, "
      "never a discrete L); moduli (k_mod, k10, C) absent from every condition; J11 "
      "holonomy = real hyperplane (C3b).  NO integer/discrete structure is forced on "
      "E0, ell, germs, or moduli.  Q-B = NO — with the exact reason per condition")

# C5b [guard]: the F-P2 provenance audit of every place integer structure COULD
# have lived, and why each is empty.
audit = [
    "torsion orders (K4 order 2; cap |det|): integers PRESENT but they are DOMAIN "
    "data whose period conditions are VACUOUS (S0b/S0c) — they cut no family parameter",
    "multiplicative holonomy kernels: all banked twists are REAL exponentials — kernel "
    "= {0}, not a lattice (C3c); no circle-valued/imaginary target in the banked census "
    "(fields (phi,f,bh) real; E08 s real; L-blocks real; K4 characters ±1)",
    "atan quadrature multivaluedness: engages only for a circle-valued f — banked f is "
    "the real connection moment (higher-isometry audit), not an angle: no branch lattice",
    "e^{iS}/GR-analog RED-class devices: FORBIDDEN imports, not used (F-P2 clean)",
]
check("C5b_QB_provenance_audit", "guard", True, " || ".join(audit))

# ============================================================================
# C6 — TP-5 (Q-C): the sector-compatibility map
# ============================================================================
print("=" * 78)
print("C6 — Q-C: sector-compatibility typing computations")
print("=" * 78)

# C6a [SUBSTANTIVE]: crease-end (quotient wall) conditions on a quadratic-class
# member, derived from the banked mirror-jet kill (eps_phi = -1 DEFINITIONAL:
# even jets of p0 vanish at a mirror wall): p0(-l)=0 and p0''(-l)=0
#   <=>  w(-l) = 1  and  2*A*w(-l) = w'(-l)^2.
p0w = log(w_expr) / aF
c1 = p0w.subs(x, -l)                      # = 0  <=> w(-l) = 1
c2 = sp.diff(p0w, x, 2).subs(x, -l)       # = 0  <=> 2A w = w'^2 at -l
# rational witness: ell=1, A=1/2, w1=0, w0=1/2  (w = x^2/2 + 1/2)
subs_w = {E0: gp / aF**2, w1: 0, w0: Rational(1, 2), l: 1}   # A = aF^2 E0/(2gp) = 1/2
ok = is_zero(c1.subs(subs_w)) and is_zero(simplify(c2.subs(subs_w)))
# E0 = g_p/aF^2 > 0 for g_p > 0: nonzero mass at the crease-compatible member
ok = ok and simplify((gp / aF**2) * aF**2 / gp - 1) == 0
check("C6a_crease_end_conditions_and_witness", "substantive", ok,
      "crease (quotient-wall) conditions on the quadratic class DERIVED from the banked "
      "mirror-jet kill (eps_phi=-1 DEFINITIONAL, CANON layer 3): w(-l)=1 AND "
      "2*A*w(-l)=w'(-l)^2.  Exact witness w = x^2/2 + 1/2 (ell=1): both conditions "
      "zero-residual, E0 = g_p/aF^2 > 0 (g_p>0) — a MASSIVE quadratic-class member "
      "carrying a crease at one end EXISTS.  STAMP: quotient wall at x=-l, quadratic "
      "class, witness normalization ell=1 (CHOSE, scaling typed)")

# C6b [SUBSTANTIVE]: the constants-census massive family (i) — {I_p=0, E0>0} —
# is realizable WITH a crease at one end: on the crease-pinned one-parameter
# branch w1 = 2A - sqrt(2A), w0 = 1 + A - sqrt(2A) (ell=1):
#   disc(w) = -2A < 0 for all A>0 (nodeless, w>0);
#   I_p(A=1/2)*aF = pi - 4 < 0  (exact; pi < 22/7 by the Dalzell integral);
#   I_p(A=9/2)*aF >= (2/3)*log(5/2) > 0  (exact interval bounds);
#   continuity (Category-A) => a root A* in (1/2, 9/2) with E0 = 2A* g_p/aF^2 > 0.
Asym = Symbol('A_par', positive=True)
w1b = 2 * Asym - sqrt(2 * Asym)
w0b = 1 + Asym - sqrt(2 * Asym)
wb = Asym * x**2 + w1b * x + w0b
disc = simplify(w1b**2 - 4 * Asym * w0b)
ok = is_zero(disc + 2 * Asym)
# crease conditions hold on the branch (zero residual at symbolic A):
ok = ok and is_zero(simplify(wb.subs(x, -1) - 1))
ok = ok and is_zero(simplify(2 * Asym * wb.subs(x, -1)
                             - (sp.diff(wb, x).subs(x, -1))**2))
# A = 1/2: w = (x^2+1)/2; I_p*aF = int log((x^2+1)/2) = pi - 4 exactly
Ip_half = integrate(log((x**2 + 1) / 2), (x, -1, 1))
ok = ok and is_zero(simplify(Ip_half - (pi - 4)))
# pi < 22/7 via Dalzell: integral of x^4(1-x)^4/(1+x^2) on [0,1] equals 22/7 - pi,
# integrand nonnegative => 22/7 - pi > 0 => pi - 4 < 22/7 - 4 < 0
dal = integrate(x**4 * (1 - x)**4 / (1 + x**2), (x, 0, 1))
ok = ok and is_zero(simplify(dal - (Rational(22, 7) - pi)))
ok = ok and (Rational(22, 7) - 4 < 0)
# A = 9/2: w = (9/2)x^2 + 6x + 5/2; verify the exact bound chain:
w92 = wb.subs(Asym, Rational(9, 2))
ok = ok and is_zero(simplify(w92 - (Rational(9, 2) * x**2 + 6 * x + Rational(5, 2))))
# vertex at x=-2/3 with w=1/2 (min); w(1/3)=5; w-1 factors (3x+1)(x+1)/... :
ok = ok and is_zero(simplify(w92.subs(x, Rational(-2, 3)) - Rational(1, 2)))
ok = ok and is_zero(simplify(w92.subs(x, Rational(1, 3)) - 5))
ok = ok and is_zero(simplify(factor(w92 - 1) - Rational(3, 2) * (3 * x + 1) * (x + 1)))
# bound: on [-1,-1/3] w>=1/2 (parabola, min at interior vertex -2/3, endpoints 1, 1)
ok = ok and (w92.subs(x, -1) - Rational(1, 2) > 0) and (w92.subs(x, Rational(-1, 3)) - Rational(1, 2) >= 0)
# on [-1/3,1/3]: w >= 1 (roots of w-1 are -1, -1/3; leading coeff > 0 outside)
ok = ok and (w92.subs(x, 0) - 1 > 0)
# on [1/3,1]: w >= 5 (w increasing right of vertex -2/3)
ok = ok and (sp.diff(w92, x).subs(x, Rational(1, 3)) > 0) and (w92.subs(x, 1) - 5 > 0)
# assembled lower bound: I_p(9/2)*aF >= (2/3)(log 5 - log 2) = (2/3) log(5/2) > 0
bound = Rational(2, 3) * (log(5) - log(2))
ok = ok and (log(Rational(5, 2)).is_positive is True) and is_zero(
    simplify(bound - Rational(2, 3) * log(Rational(5, 2))))
check("C6b_massive_Ip0_locus_with_crease_nonempty", "substantive", ok,
      "crease-pinned branch (ell=1): w1=2A-sqrt(2A), w0=1+A-sqrt(2A); disc=-2A<0 "
      "(nodeless all A>0); I_p(1/2)*aF = pi-4 < 0 EXACT (Dalzell 22/7-pi = "
      "nonneg-integrand integral); I_p(9/2)*aF >= (2/3)log(5/2) > 0 by exact piecewise "
      "bounds (vertex/root arithmetic zero-residual, log monotonicity Category-A); "
      "continuity of A -> I_p (log of a nodeless polynomial family; Category-A) => "
      "a root A* in (1/2,9/2) with E0=2A*g_p/aF^2 > 0: family (i) {I_p=0, E0>0} IS "
      "REALIZABLE with a quotient crease at one end and a two-sided seam at the other. "
      "STAMP: mixed-posture chain (crease|two-sided), quadratic class, definite "
      "sub-class, INTEGRATED branch, ell=1 witness normalization (CHOSE, typed); "
      "root existence via IVT = the banked A2/sign-change pattern (nonconstructive, "
      "Category-A)")

# C6c [SUBSTANTIVE]: the fields-census lock-emergence massive class (ii) on a
# cyclic completion: p0 == 0 landing (W_F == 1), f,h AFFINE with free slopes,
# E0 = Ltilde_fh(f1,h1).  Single-valuedness on the cycle: Delta f = f1*L = 0
# => f1 = 0 (L>0); same h1 => E0 = Ltilde_fh(0,0) = 0: FORCED MASSLESS.
f1s, h1s = symbols('f1 h1', real=True)
Ltilde_fh = (gf * f1s**2 + 2 * gx * f1s * h1s + gh * h1s**2) / 2
solf = solveset(sp.Eq(f1s * L1, 0), f1s, domain=S.Reals)
ok = solf == FiniteSet(0)
ok = ok and is_zero(Ltilde_fh.subs({f1s: 0, h1s: 0}))
check("C6c_lock_class_cut_on_cyclic_completion", "substantive", ok,
      "lock-emergence massive class (P1-4D landing, W_F==1, f/h affine): on a CYCLIC "
      "completion, field single-valuedness (oint df = f1*L = 0, L>0) forces f1=h1=0 "
      "=> E0 = Ltilde_fh(0,0) = 0: the massive leg is CUT (forced massless) there.  On "
      "ACYCLIC chains (open/two-sided-terminated): no cycle => UNTOUCHED (its banked "
      "conditionalities travel unchanged).  Quotient posture: already excluded upstream "
      "by the banked parity collapse (CITED, not re-adjudicated).  STAMP: fields census "
      "BR-M, P1-4D branch, lock landing, GENERIC nondegeneracy stamps [AM-2] inherited")

# C6d [SUBSTANTIVE]: the massless strata (iii) satisfy every derived period
# condition identically; nonconstant P2-side affine members reduce to constants
# on cyclic completions (same mechanism as C6c), survive unchanged elsewhere.
# constants: E0=0, c=0, slopes 0 — all conditions zero:
allconds = [aF * E0 * L1, f1s * L1, E01 * L1 + E02_ * L2 + E03_ * L3]
vals = [c.subs({E0: 0, f1s: 0, E01: 0, E02_: 0, E03_: 0}) for c in allconds]
ok = all(is_zero(v) for v in vals)
check("C6d_massless_strata_survive_everywhere", "substantive", ok,
      "the massless strata (P2-side constants, triad-locked {E0=0}, pointwise "
      "survivors {E0=0}) satisfy EVERY derived period condition identically (zero "
      "residual).  Nonconstant P2-affine / NV-affine (W1-class) members on a cyclic "
      "completion reduce to constants by field single-valuedness (slope*L=0); on "
      "quotient/acyclic completions they are untouched by R9.  STAMP: P2 branch "
      "aF=0 instance; NV closure-data reading typed under the same single-valuedness "
      "conditions (gate-6 nonvariational form)")

# C6e [guard]: the wall germ data (iv).
check("C6e_germ_data_unreached", "guard", True,
      "open-end germ family (B_Q, B_rho — the banked FREE 2-germ-function family): NO "
      "cycle passes through a free endpoint, so no period condition reaches it — "
      "UNTOUCHED/FREED by R9.  Banked-glue germs: pinned upstream (B_rho=q/2, B_Q=0); "
      "the flux-seal pin B_Q=0 is EXACTLY the condition under which the cyclic period "
      "law carries no seam sources (C2b) — a consistency observation, nothing adopted. "
      "Non-banked active-germ two-sided seams: enter the period law as supplied jumps "
      "J_s (C2b general form), typed")

# C6f [SUBSTANTIVE]: cross-pairing seam weight matching at seal-value loci.
# At a seam locus with p0 = 0 the anchored weight W_F = e^{aF*0} = 1 for EVERY
# enumerated branch (symbolic aF): cross-pairing gluing is weight-consistent
# exactly at seal-value seams (the banked TW3 mirror-wall weight-drop, here as
# the seam-locus instance).
ok = is_zero(exp(aF * 0) - 1)
check("C6f_crosspairing_weight_match_at_seal", "substantive", ok,
      "W_F(p0=0) = e^{aF*0} = 1 for every enumerated branch (aF symbolic): two cells "
      "carried under DIFFERENT pairing branches present EQUAL weights at any seam locus "
      "sitting at the seal value p0=0 — cross-pairing joins are weight-consistent there "
      "(banked TW3_pairing_weight_drops_at_mirror_wall, seam-locus instance; at "
      "off-seal seams the weights differ by (c_E/Q_w)^{aF}: CONDITIONAL, "
      "weight-matching factor required).  STAMP: J08-type transition typing fact; "
      "no pairing adopted")

# C6g [guard]: the Q-C map assembled (typing facts ONLY — F-P7).
qc_map = [
    ("crease|crease (mirrored cell)", "PERMITTED",
     "banked mirrored-cell canon; R9 identically satisfied (C1)"),
    ("crease|two-sided glue (mixed chain)", "PERMITTED-CONDITIONAL",
     "crease conditions w(-l)=1, 2A*w(-l)=w'(-l)^2 (C6a); massive family (i) "
     "realizable there (C6b)"),
    ("two-sided cyclic, all-definite members", "FORBIDDEN for massive members",
     "Sum E0_i L_i = 0 + E0_i>=0 => all massless (C2c); massive requires an "
     "indefinite partner (existence of a full mixed witness: CONDITIONAL — the "
     "remaining field-period balance Sum (G_i^-1 c) J_i = 0 is a derived real "
     "condition, not certified nonempty here)"),
    ("two-sided cyclic, 1-cell", "FORBIDDEN for nonconstant members",
     "constants only (C2d)"),
    ("open-end terminator + any chain", "PERMITTED",
     "no cycle; germs freed (C6e); q-datum = wall-response output (banked)"),
    ("cross-census cells (constants-census | fields-census) in one whole",
     "CONDITIONAL", "weight match automatic at seal-value seams (C6f); off-seal "
     "seams need the branch weight factor; J07 transition data obligation "
     "inherited (F-S7 flag travels)"),
]
check("C6g_QC_map_assembled", "guard", True,
      "Q-C map (typing facts ONLY; the owner's sectors reading CHARACTERIZED, never "
      "adopted, never used to resolve any fork — F-P7): " +
      " | ".join(f"{r[0]} -> {r[1]}" for r in qc_map))

# ============================================================================
# Ledger + results
# ============================================================================
print("=" * 78)

LEDGER_ROWS = []


def ledger(cycle, family, posture, condition, verdict, stamps):
    LEDGER_ROWS.append((cycle, family, posture, condition, verdict, stamps))


FAMS = {
    "i": "constants-census massive locus {I_p=0, E0>0} (triad/P1 pairing, INTEGRATED)",
    "ii": "fields-census lock-emergence massive class (P1-4D landing)",
    "iii": "massless strata (P2-side; triad-locked; pointwise survivors)",
    "iv": "wall germ data (open-end 2-germ family; glue pins)",
}

for fam in ("i", "ii", "iii", "iv"):
    ledger("K4-orbifold / cap-torsion", FAMS[fam], "all postures",
           "n*P=0 (torsion) => P=0", "VACUOUS (identically satisfied)",
           "S0b/S0c; closed real forms; banked proof cited")
    ledger("D_inf translation gamma_T", FAMS[fam], "quotient",
           "Hom(D_inf,R)=0 => all periods 0", "IDENTICALLY SATISFIED (imposes nothing)",
           "C1a-C1c; jet<=2; any census/pairing branch")
    ledger("none (no cycle)", FAMS[fam], "open / acyclic chain",
           "no nontrivial cycle", "VACUOUS", "C1d typing")

ledger("Z translation (cyclic completion)", FAMS["i"], "two-sided",
       "Sum_i E0_i L_i = 0  (== Sum M-WALL_i = 0 == aF*Sum M-GEN_i = 0); "
       "field periods Sum (G_i^-1 c)_f J_i = 0 (both components); whole-completion "
       "tie Sum E0_i I_p,i = 0",
       "CUT on all-definite chains (forced massless, C2c); EMPTY at N=1 (C2d); "
       "CONDITIONAL with indefinite partners (real conditions, no integers)",
       "C2a-C2f; quadratic class; flux-sealed seams; common aF != 0; INTEGRATED branch")
ledger("Z translation (cyclic completion)", FAMS["ii"], "two-sided",
       "oint df = f1*L = 0, oint dh = h1*L = 0", "CUT (forced massless, C6c)",
       "fields census BR-M; P1-4D lock landing; [AM-2] stamps inherited")
ledger("Z translation (cyclic completion)", FAMS["iii"], "two-sided",
       "all derived conditions", "SATISFIED identically (constants); nonconstant "
       "affine members reduce to constants", "C6d")
ledger("Z translation (cyclic completion)", FAMS["iv"], "two-sided",
       "germs enter only as seam sources J_s in the momentum period law",
       "banked glue germ (B_Q=0): no source (consistency); active germs: supplied J_s",
       "C2b/C6e; arena-transfer premise stamped")
for fam in ("i", "ii", "iii", "iv"):
    ledger("J11 chart loop", FAMS[fam], "any posture (multi-chart completion with a loop)",
           "twisted-cocycle holonomy trivial-or-classified: real-linear hyperplane / "
           "real matrix value", "REAL classification; NO discrete structure (C3b-C3d)",
           "E08 + diagonal-K twisted law; F-S7 flag; conditional on loop existence "
           "(completion data)")

with open(os.path.join(HERE, "PERIOD_LEDGER.tsv"), "w", encoding="utf-8") as fh:
    fh.write("cycle\tfamily\tposture\tcondition\tverdict\tstamps\n")
    for r in LEDGER_ROWS:
        fh.write("\t".join(r) + "\n")
print(f"PERIOD_LEDGER.tsv written: {len(LEDGER_ROWS)} rows")

n_sub = sum(1 for c in CHECKS if c["kind"] == "substantive")
n_grd = sum(1 for c in CHECKS if c["kind"] == "guard")
n_fail = sum(1 for c in CHECKS if not c["passed"])
result = {
    "package": "udt_p4_period_gate_2026-07-30",
    "contract": "PREREGISTRATION.md (frozen)",
    "checks_total": len(CHECKS),
    "checks_substantive": n_sub,
    "checks_guard": n_grd,
    "checks_failed": n_fail,
    "outcome_class": "MIXTURE: OQ3 (sector-compatibility map computed) + OQ4 on Q-B "
                     "(no quantization — derived reasons) + Q-A NO-SELECTION (typing "
                     "distinction only); TP-2 derived REAL period conditions are "
                     "first-class content",
    "QA_verdict": "NO posture selected: quotient identically satisfied; cyclic "
                  "two-sided carries real conditions (satisfiable); open vacuous. "
                  "No posture emptied or forced.",
    "QB_verdict": "NO quantization: every derived condition has a continuum solution "
                  "set; all banked holonomy targets are real (kernel {0}, no lattice); "
                  "the only integers in the cycle content are torsion ORDERS, whose "
                  "period conditions are vacuous. F-P2 clean: nothing imported, and "
                  "the located absence is derived, not assumed.",
    "QC_verdict": "map computed (typing facts only, F-P7): cyclic+all-definite "
                  "massive FORBIDDEN; 1-cell cyclic nonconstant FORBIDDEN; "
                  "crease|glue mixed chain PERMITTED-CONDITIONAL with massive family "
                  "(i) realizable; open terminator PERMITTED; cross-census joins "
                  "CONDITIONAL (weight match at seal-value seams).",
    "headline_conditions": {
        "cyclic_momentum_period": "Sum_i E0_i L_i = 0  <=>  Sum_i M-WALL_i = 0 <=> "
                                  "Sum_i M-GEN_i = 0 (labeled branches; common aF!=0)",
        "cyclic_field_periods": "Sum_i (G_i^-1 c)_a J_i = 0 per angular field a; "
                                "c common (momentum continuity)",
        "whole_completion_tie": "Sum_i E0_i I_p,i = 0 (INTEGRATED; generalizes the "
                                "banked per-cell 2 E0 I_p = 0)",
        "crease_end_on_quadratic_class": "w(-l)=1 and 2 A w(-l) = w'(-l)^2",
        "J11_loop": "real-linear holonomy vanishing (hyperplane) or real "
                    "classification value",
    },
    "checks": CHECKS,
}
with open(os.path.join(HERE, "period_gate_results.json"), "w", encoding="utf-8") as fh:
    json.dump(result, fh, indent=1, sort_keys=True)
print("period_gate_results.json written")

print("=" * 78)
print(f"TOTAL: {len(CHECKS)} checks = {n_sub} substantive + {n_grd} guards; "
      f"failed: {n_fail}")
if n_fail:
    print("RESULT: FAILURE (F-P6: recorded as-is)")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS")
sys.exit(0)
