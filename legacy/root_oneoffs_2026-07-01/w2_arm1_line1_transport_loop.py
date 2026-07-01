"""W2 ARM-1, LINE 1 — DILATION TRANSPORT / LOOP STRUCTURE.

Declaration: w_stiffness_push_declaration.md, "W2 framing correction"
section (binding): UNCOVERING ONLY. Nothing here is added to the theory;
every object below is computed from the metric the theory already has.

QUESTION (metric-led): the postulate says clock rates at different
positions compose along paths. On a shaped configuration (P1 class +
full time row; conventions: same-minus theorem-grade, Q != 0, R-areal
rho = r), what is the metric's own clock-transport structure, how does
a rate comparison transported around a closed (r,theta) loop fail to
return, what scalar measures the failure, and what is its jet content
in w?

TRANSPORT-LAW GROUNDING (quoted, with provenance):
- udt_canonical_geometry.md sec 1.3: "Redshift (between points):
  1 + z = e^{phi(r_2) - phi(r_1)}" — pairwise rate comparison is
  MULTIPLICATIVE in e^{phi}, i.e. additive in phi along a path.
- udt_canonical_geometry.md sec 1.4: "These relations encode the
  geometric transformation accumulated along the null geodesic
  connecting source and observer." Reading clarifier (VR sec 62,
  2026-04-27, quoted in 1.4): "the null geodesic here is the geometric
  integration path along which the frame-relation between source and
  observer is computed; the 'accumulation' is of the metric's
  frame-comparison content, not transport of a physical field."
- negative_phi_native_geometry.md sec 1: "For a stationary observer at
  fixed r, dtau = sqrt(f) dt = e^{-phi} dt."
- UDT_REBUILD.md sec 1: "Macro: redshift 1+z = e^phi."

So the corpus transport law is: the RATE-comparison 1-form is
alpha = d phi (phi read from the metric), accumulated along the
connecting path. The corpus states it on the static spherical class,
where path-independence is automatic. On the shaped class the corpus
does NOT add anything; what the metric itself supplies is computed
below.

THE FORK (declared up front, reported honestly per the task brief):
the corpus determines the RATE transport (alpha = d phi); it nowhere
mentions the metric's second, independent transport structure — the
SIMULTANEITY (clock-synchronization) transport, which is GR-corpus
mathematics (Landau-Lifshitz sec 84 species: synchronizing clocks
along a closed contour fails by Delta t = -oint g_{Ti}/g_{TT} dx^i)
transformed under positional dilation (principle 4; guardrail:
"connection / curvature identities: usable exactly"). Both are
structures the metric POSSESSES; only the first is corpus-forced as
"the transport law of the postulate". Findings below are labeled by
which transport they belong to.

PRE-STATED FAILURE CRITERIA (hypothesis discipline; committed before
the computation cells below were run):
- F1: if the rate-transport holonomy is nonzero, that would CONFIRM a
  standing picture (phi-angular interaction) — so it gets the hardest
  check: d(d phi) = 0 must be verified exactly, and any nonzero
  holonomy claim must survive an exact closed-form recomputation.
  EXPECTED death: rate transport is exact => zero holonomy => ZERO jet
  content in w. If so, report the death as a death.
- F2: the synchronization holonomy may carry w-jets only through
  metric components the configuration class actually has (a, b on the
  eliminated branch). If its w-jet content vanishes identically, line
  1 returns "the metric transports clocks integrably on this class"
  and that negative is banked with its premise set.
- F3: any sonic-locus coupling claim must be an exact identity
  (Q restricted to spherical equals A*g with g = f f_r^2 - f_T^2/f),
  not a numerical observation.

Method: exact sympy on CPU; no linearization; exact rational spot
checks; assert-laden. New file (repo discipline). 2026-06-11, W2 ARM-1
agent.
"""

import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label


def zero_cancel(e):
    return sp.cancel(sp.together(sp.expand(e))) == 0


# ----------------------------------------------------------------------
# Coordinates and the P1 + full-time-row metric class (s1 conventions:
# rescued_workspaces/2026-06-11/nonstat_n2/s1_setup_anchors.py)
#   ds^2 = -f dT^2 + 2a dT dr + 2b dT dth + (1/f) dr^2 + 2q dr dth
#          + A dth^2 + B dvphi^2,
#   A = r^2 (1+w)^2, B = r^2 sin^2(th)/(1+w)^2,
#   f, q, w, a, b functions of (T, r, th).
# ----------------------------------------------------------------------
T, r, th = sp.symbols('T r theta', real=True)
c = sp.Symbol('c', positive=True)
f = sp.Function('f')(T, r, th)
q = sp.Function('q')(T, r, th)
w = sp.Function('w')(T, r, th)
a = sp.Function('a')(T, r, th)
b = sp.Function('b')(T, r, th)
A = r**2 * (1 + w)**2
B = r**2 * sp.sin(th)**2 / (1 + w)**2

print("=" * 72)
print("L1-S1: RATE TRANSPORT (the corpus's transport law) — loop failure")
print("=" * 72)

# The corpus rate-comparison 1-form: alpha = d phi, phi = -(1/2) ln f
# (the banked tie; f = -g_TT = e^{-2 phi}).
phi = -sp.log(f) / 2
alpha = [sp.diff(phi, x) for x in (T, r, th)]
# Loop failure of rate transport around any closed loop = exterior
# derivative of alpha. Compute ALL components of d alpha:
d_alpha = {}
coords = (T, r, th)
for i in range(3):
    for j in range(i + 1, 3):
        d_alpha[(i, j)] = sp.diff(alpha[j], coords[i]) - sp.diff(alpha[i], coords[j])
check("L1-01 RATE transport: d(d phi) = 0 EXACTLY on the full shaped "
      "nonstationary class — rate comparison transported around ANY closed "
      "(T,r,theta) loop returns EXACTLY (zero holonomy)",
      all(zero_cancel(v) for v in d_alpha.values()))
check("L1-02 ... therefore the rate-transport loop scalar has ZERO jet "
      "content in w (it is identically zero) — F1 death CONFIRMED, "
      "recorded as a death: the corpus's own transport law is integrable "
      "on every configuration, shaped or not",
      all(zero_cancel(v) for v in d_alpha.values()))

print()
print("=" * 72)
print("L1-S2: SIMULTANEITY TRANSPORT (the metric's own second transport)")
print("=" * 72)
# The metric's clock-synchronization 1-form (GR corpus, LL sec 84
# species, computed natively on this metric — pure metric algebra):
# synchronizing adjacent clocks along a spatial path defines
#   dT_sync = -(g_{Ti}/g_{TT}) dx^i = (a dr + b dth)/f.
# omega is structure the metric possesses; nothing is added.
omega_r = a / f
omega_th = b / f
# Loop failure of synchronization around a closed (r,theta) loop:
#   Delta T_loop = oint omega = integral of H dr ^ dth,
#   H = d_r(omega_th) - d_th(omega_r).
H = sp.diff(omega_th, r) - sp.diff(omega_r, th)
check("L1-03 the synchronization holonomy density H = d_r(b/f) - d_th(a/f) "
      "is generically NONZERO on the class (witness: exact rational point)",
      sp.simplify(H.subs([(a, sp.Integer(0)), (b, r * f)])) != 0)

# On C1's own solution branch the time row is NOT free: the unique
# nondegenerate stationary branch (same-minus theorem, VN) fixes
#   K = f_r b - f_th a = 0  and  S = v2^T adj(M2) (a,b) = S*,
#   S* = 2 f D2 f_T P / Q  (s1 B3b), with
#   P = A f_r^2 - 2 q f_r f_th + f_th^2/f,  D2 = A/f - q^2,
#   Q = f P - D2 f_T^2.
fT, fr, fth = sp.diff(f, T), sp.diff(f, r), sp.diff(f, th)
M2 = sp.Matrix([[1 / f, q], [q, A]])
adj2 = M2.adjugate()
v2 = sp.Matrix([fr, fth])
P_ = sp.expand((v2.T * adj2 * v2)[0, 0])
D2_ = sp.expand(M2.det())
Q_ = sp.expand(f * P_ - D2_ * fT**2)
S_star = 2 * f * D2_ * fT * P_ / Q_
ab = sp.solve([sp.Eq((v2.T * adj2 * sp.Matrix([a, b]))[0, 0], S_star),
               sp.Eq(fr * b - fth * a, 0)], [a, b], dict=True)
check("L1-04 the (a*, b*) branch solves uniquely", len(ab) == 1)
a_st, b_st = sp.cancel(ab[0][a]), sp.cancel(ab[0][b])
# anchor against nonstationary_opener_results.md: a* = 2 f D2 f_T f_r/Q,
# b* = (f_th/f_r) a*
check("L1-05 a* = 2 f D2 f_T f_r / Q (banked opener value, exact)",
      zero_cancel(a_st - 2 * f * D2_ * fT * fr / Q_))
check("L1-06 b* = (f_theta/f_r) a* (banked opener value, exact)",
      zero_cancel(b_st - (fth / fr) * a_st))

# THE STRUCTURE: on the branch, omega = lam * d_spatial f with
# lam = a*/(f f_r) = 2 D2 f_T / Q  — the synchronization 1-form is
# the spatial df, scaled by a dilation-weighted factor.
lam = sp.cancel(a_st / (f * fr))
check("L1-07 on the C1 branch omega = lam * (f_r dr + f_th dth), "
      "lam = 2 D2 f_T / Q  [exact]",
      zero_cancel(lam - 2 * D2_ * fT / Q_)
      and zero_cancel(b_st / f - lam * fth))

# Loop failure on the branch: dω = dlam ^ d_spatial f, i.e.
#   H* = d_r(lam f_th) - d_th(lam f_r) = lam_r f_th - lam_th f_r
#        (the f_{rth} cross terms cancel exactly).
H_branch = sp.diff(lam * fth, r) - sp.diff(lam * fr, th)
H_jacobian = sp.diff(lam, r) * fth - sp.diff(lam, th) * fr
check("L1-08 H* = lam_r f_th - lam_th f_r exactly (mixed f_{r theta} "
      "terms cancel: the holonomy is the (lam, f) spatial Jacobian)",
      zero_cancel(H_branch - H_jacobian))

# ---- JET CONTENT IN w --------------------------------------------------
# lam contains w ALGEBRAICALLY (through A = r^2(1+w)^2 inside D2, P, Q);
# d lam therefore contains FIRST derivatives of w. Census:
wr, wth = sp.diff(w, r), sp.diff(w, th)
wT = sp.diff(w, T)
H_expanded = sp.together(H_branch)
atoms = H_expanded.atoms(sp.Derivative)
w_atoms = sorted({d for d in atoms if d.expr == w}, key=str)
has_w1 = any(d.derivative_count == 1 for d in w_atoms)
has_w2 = any(d.derivative_count >= 2 for d in w_atoms)
print("    w-derivative atoms in H*:", [str(d) for d in w_atoms])
check("L1-09 JET CONTENT: the loop-failure scalar H* carries FIRST "
      "derivatives of w (w_r, w_theta) and NO second derivatives of w — "
      "the synchronization transport reads w exactly ONE jet deeper than "
      "C1 (which reads jet zero)",
      has_w1 and not has_w2)

# coefficient of w_r in H*: exact extraction. H* is linear in (w_r, w_th)
# (lam_r = (dlam/dw) w_r + ..., Jacobian structure), so coefficients are
# well-defined by differentiation.
coef_wr = sp.cancel(sp.diff(H_expanded, wr))
coef_wth = sp.cancel(sp.diff(H_expanded, wth))
dlam_dw = sp.diff(lam, w)
check("L1-10 H* is LINEAR in (w_r, w_theta) with coefficients "
      "(dlam/dw) f_th and -(dlam/dw) f_r: the w-jet enters ONLY through "
      "the dilation-weighted scale factor lam",
      zero_cancel(coef_wr - dlam_dw * fth)
      and zero_cancel(coef_wth + dlam_dw * fr))

# ---- FILTER SCORECARD (report-only, binding from the declaration) -----
# (i) vanishes on spherical: f_th = 0, q = 0, w = 0
sph = [(q, sp.Integer(0)), (w, sp.Integer(0))]
H_sph = H_branch.subs(sph).doit()
# impose f_theta = 0 by substituting f -> F(T, r)
F2 = sp.Function('F')(T, r)
H_sph = sp.cancel(H_sph.subs(f, F2).doit())
check("L1-11 SCORECARD vanish-on-spherical: H* = 0 identically when "
      "f = f(T,r), q = 0, w = 0 (exact)", zero_cancel(H_sph))
# (ii) vanishes on static: f_T = 0 => lam = 0
F3 = sp.Function('F')(r, th)
H_static = sp.cancel(H_branch.subs(f, F3).doit().subs(
    [(q, sp.Function('qs')(r, th)), (w, sp.Function('ws')(r, th))]).doit())
check("L1-12 SCORECARD macro/static sector untouched: H* = 0 identically "
      "on ANY static configuration (f_T = 0 kills lam) — the entire "
      "static/banked/macro stack is blind to this structure", zero_cancel(H_static))
# (iii) sonic-locus coupling: Q sits in lam's denominator; verify the
# EXACT identity Q|spherical = A * g, g = f f_r^2 - f_T^2/f  (F3 criterion)
Fsph = sp.Function('F')(T, r)
g_sonic_sph = Fsph * sp.diff(Fsph, r)**2 - sp.diff(Fsph, T)**2 / Fsph
Q_sph = Q_.subs(sph).subs(f, Fsph).doit()
check("L1-13 SCORECARD sonic-locus coupling (exact identity): "
      "Q restricted to spherical (f_theta = 0, q = 0, w = 0) equals "
      "A * (f f_r^2 - f_T^2/f) — the holonomy scale lam = 2 D2 f_T/Q "
      "diverges exactly on the sonic locus g = 0 "
      "(the close's fingerprint: Q is the shaped extension of A*g)",
      zero_cancel(Q_sph - A.subs(sph) * g_sonic_sph))
# (iv) axis regularity: omega_th = b*/f = lam f_th -> 0 on the axis for
# even-parity f (f_th ~ sin(th) -> 0); check on an explicit even profile
f_even = 2 + sp.cos(th)**2 / (1 + r**2) + T * r / (3 + T**2)
sub_even = {f: f_even, q: sp.Integer(0), w: sp.Integer(0)}
omega_th_branch = (b_st / f)
val_axis = sp.limit(omega_th_branch.subs(f, f_even).doit().subs(
    [(q, sp.Integer(0)), (w, sp.Integer(0))]), th, 0)
check("L1-14 SCORECARD axis behavior: omega_theta(branch) -> 0 on the "
      "axis for an explicit even-parity profile (no synchronization "
      "defect threaded through the axis)", sp.simplify(val_axis) == 0)

# ---- exact rational spot check of the whole chain ----------------------
# explicit polynomial configuration, all symbols rational
f_c = 2 + r**2 * sp.cos(th)**2 / 7 + T * r / 5
q_c = r * sp.sin(2 * th) / 11
w_c = r**2 * sp.sin(th)**2 / 13
subs_c = {f: f_c, q: q_c, w: w_c}
pt = {T: Ra(1, 3), r: Ra(3, 2), th: Ra(7, 8)}


def at_point(expr):
    return sp.nsimplify(sp.N(expr.subs(subs_c).doit().subs(pt), 50))


H_num = at_point(H_branch)
# independent recomputation: numerically differentiate the explicit
# omega components built from scratch
a_expl = (2 * f * D2_ * fT * fr / Q_)
b_expl = (fth / fr) * a_expl
om_r = (a_expl / f).subs(subs_c).doit()
om_t = (b_expl / f).subs(subs_c).doit()
H_indep = (sp.diff(om_t, r) - sp.diff(om_r, th)).subs(pt)
check("L1-15 exact spot check: H* at a rational point matches an "
      "independent from-scratch recomputation",
      sp.simplify(H_num - sp.nsimplify(sp.N(H_indep, 50))) == 0)
check("L1-16 ... and is NONZERO there (the holonomy is real on shaped "
      "moving configurations)", H_num != 0)

print()
print("=" * 72)
print("L1-S3: GAUGE STATUS OF THE HOLONOMY (the licensed chart freedom)")
print("=" * 72)
# The corpus's licensed residual time freedom (rho_dynamics_derivation_
# results.md Lemma 2: the B = 1/A chart is unique up to +-, shift, AND
# Killing-time rescaling T -> k T). Under T = k T' (constant k > 0) the
# metric components transform as g'_{T'T'} = k^2 g_TT, g'_{T'i} = k g_Ti
# and the fields are re-read at T = k T'. The synchronization 1-form and
# holonomy density therefore transform HOMOGENEOUSLY:
k = sp.Symbol('k', positive=True)
# omega'_i = -g'_{T'i}/g'_{T'T'} = (k g_Ti)/(k^2 f) = omega_i / k
check("L1-17 under the LICENSED chart freedom (Killing rescaling "
      "T -> kT; rho_dynamics Lemma 2) the synchronization 1-form scales "
      "as omega' = omega/k and H' = H/k exactly — a rate-covariant "
      "object (degree -1 in the time unit); its ZERO LOCUS and its w-jet "
      "content are chart-invariant",
      zero_cancel((k * a) / (k**2 * f) - (a / f) / k)
      and zero_cancel((k * b) / (k**2 * f) - (b / f) / k))
# HONEST LIMIT (reported, not hidden): under a GENERAL time relabeling
# T -> T + chi(r,theta) the synchronization loop itself (a fixed-T'
# circuit) is a DIFFERENT spacetime loop, and H changes by T-derivative
# terms — computed exactly:
chi = sp.Function('chi')(r, th)
om_r_new = a / f - sp.diff(chi, r)   # -g'_{T'r}/g'_{T'T'} with fields at T'+chi
om_th_new = b / f - sp.diff(chi, th)
# in the new chart, d'_i = d_i + chi_i d_T acting on fields:
H_new = (sp.diff(om_th_new, r) + sp.diff(chi, r) * sp.diff(om_th_new, T)
         - sp.diff(om_r_new, th) - sp.diff(chi, th) * sp.diff(om_r_new, T))
H_old = sp.diff(b / f, r) - sp.diff(a / f, th)
shift_terms = (sp.diff(chi, r) * sp.diff(b / f, T)
               - sp.diff(chi, th) * sp.diff(a / f, T))
check("L1-18 HONEST SCOPE: under a general relabeling T -> T + "
      "chi(r,theta) (NOT corpus-licensed: it leaves the B = 1/A areal "
      "chart class), H changes by exactly the slicing terms "
      "chi_r d_T(b/f) - chi_th d_T(a/f) (the pure chi_{r th} second "
      "derivatives cancel identically) — the holonomy is a property of "
      "the metric PLUS the corpus's preferred time function, and the "
      "corpus's chart theorem (R-areal canon) is what fixes that "
      "function. Reported as scope, not hidden",
      zero_cancel(H_new - H_old - shift_terms))

print()
print("=" * 72)
print("L1 VERDICT")
print("=" * 72)
print("""
1. THE CORPUS'S TRANSPORT LAW (rate comparison, alpha = d phi) is
   EXACT on every class: zero loop holonomy, ZERO w-jet content. The
   hypothesis-friendly outcome (rate holonomy seeing w) is DEAD —
   recorded as a death (pre-stated criterion F1).
2. THE METRIC'S SECOND TRANSPORT (clock synchronization, omega =
   -(g_Ti/g_TT) dx^i — GR-corpus mathematics computed natively) is
   NONTRIVIAL exactly on C1's own nondegenerate branch: omega = lam *
   d_spatial f, lam = 2 D2 f_T / Q. Its loop failure
   H* = lam_r f_th - lam_th f_r is FIRST-JET in w (one jet deeper than
   C1 reads), linear in (w_r, w_theta) through dlam/dw alone, vanishes
   identically on spherical AND on every static configuration (macro
   untouched by construction), and its scale diverges exactly on the
   sonic locus (Q|sph = A g — exact identity).
3. FORK (honest): the corpus forces only transport 1; transport 2 is
   structure the metric possesses but the corpus has never named. H*
   is therefore an UNCOVERED METRIC STRUCTURE with first-jet w content
   on the C1 branch — not yet a stiffness (second-jet) and not a
   derived action term. Its second-jet shadow belongs to line 4's
   census (curvature of the transport).
4. GAUGE STATUS: H* is covariant (degree -1) under the corpus's
   licensed chart freedom (Killing rescaling; L1-17) — zero locus and
   w-jet content invariant — and depends on the corpus's preferred
   time function under general relabelings (L1-18, exact slicing
   terms exhibited), which the R-areal chart theorem fixes.
""")
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL")
assert not FAIL
