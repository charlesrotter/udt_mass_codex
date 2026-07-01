"""W2 ARM-1, LINE 2 — THE TIE'S HONEST DEPTH.

Declaration: w_stiffness_push_declaration.md "W2 framing correction"
(binding): UNCOVERING ONLY. We do not pick a reading because it helps;
we compute the dilation field as read by each observer family the
corpus licenses and report which readings make angular structure enter
the tied slot, ranked by derivation strength.

POSTULATE GROUNDING (quotes, provenance):
- udt_canonical_geometry.md sec 1.0 (S58-009 chain, step 2):
  "Positional-dilation postulate -> g_tt = -e^{-2 phi(r)} c^2, i.e.
  A(r) = e^{-2 phi(r)} as primitive structural ingredient of spacetime
  geometry". THE TIE IS STATED AT THE METRIC-COMPONENT LEVEL (g_tt),
  not at the observer level.
- negative_phi_native_geometry.md sec 1: "For a stationary observer at
  fixed r, dtau = sqrt(f) dt = e^{-phi} dt." THE ONLY OBSERVER FAMILY
  THE CORPUS EVER NAMES is the stationary (constant-spatial-coordinate)
  family; for it, rate = sqrt(-g_tt) and the two statements coincide.
- udt_canonical_geometry.md sec 1.3: "Lapse function: N(r) = e^{-phi(r)};
  Proper time: dtau = e^{-phi} dt." NOTE: on the diagonal static class
  the corpus's "lapse" and sqrt(-g_tt) are THE SAME OBJECT; the corpus
  has never had to distinguish them. On the shaped + time-row class
  they SPLIT (computed below) — this is the honest fork.
- Corpus-wide searches (2026-06-11, this agent): "weld frame",
  "weld-frame", "Eulerian", "normal observer", "preferred observer"
  appear NOWHERE in the repo's .md corpus. The medium/exterior-field
  picture is Charles's standing hunch (memory file), explicitly
  direction-not-evidence under hypothesis discipline. THEREFORE: the
  corpus licenses exactly TWO candidate readings on the shaped class,
  both inherited from the same static-class object that splits:
    (R-stat)  phi from the stationary family's rate sqrt(-g_TT)
              [= the banked tie phi = -(1/2) ln f]
    (R-norm)  phi from the slice-normal (lapse) rate N = 1/sqrt(-g^TT)
              [the other factorization of the SAME corpus formula]
  No third family has any corpus text.

PRE-STATED FAILURE CRITERIA (hypothesis discipline — this line would
CONFIRM the standing picture "shape modes entering the tied slot
acquire derivatives" (W1-VA proviso), so the bar is highest here;
committed before the computation cells ran):
- F1 (forcing): the confirming outcome requires the corpus to FORCE a
  reading under which angular structure enters the tied slot. Given
  the grounding above (tie stated at g_tt level; only the stationary
  family named), the expected verdict is NOT FORCED: R-stat outranks
  R-norm. If so, that death of the confirming outcome is recorded as
  a death, and R-norm is banked as an unforced fork only.
- F2 (degeneracy): if N = sqrt(f) identically on all STATIC shaped
  configurations, then no static/banked/macro result can distinguish
  the readings — the fork is invisible to the entire validated stack.
  This must be verified exactly, both ways (it protects the macro
  sector under either reading, AND it removes any data-side ground for
  preferring R-norm).
- F3 (structure): any claimed w-content of the R-norm dilation field
  must vanish on spherical (else it would be macro-touching) and any
  sonic-locus statement must be an exact identity.
- F4 (jet honesty, added after a first-draft self-catch and BEFORE this
  version ran): phi_norm is zeroth-jet in w and first-jet in f, so the
  C1 DENSITY under R-norm is FIRST-jet in w and SECOND-jet in f; the
  claim is "w becomes dynamical (second-order EL)", NOT "second jets in
  the density". Any check finding second w-jets in the density itself
  would be flagging spurious (uncancelled) atoms and must not be
  trusted.

Method: exact sympy on CPU (adjugate/cofactor identities, no full 4x4
inversion of branch metrics); no linearization; rational spot checks;
assert-laden. New file. 2026-06-11, W2 ARM-1 agent.
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


T, r, th = sp.symbols('T r theta', real=True)
c = sp.Symbol('c', positive=True)
f = sp.Function('f')(T, r, th)
q = sp.Function('q')(T, r, th)
w = sp.Function('w')(T, r, th)
a = sp.Function('a')(T, r, th)
b = sp.Function('b')(T, r, th)
A = r**2 * (1 + w)**2
B = r**2 * sp.sin(th)**2 / (1 + w)**2

# the (T, r, theta) block (B decouples; s1 conventions)
M3 = sp.Matrix([[-f, a, b], [a, 1 / f, q], [b, q, A]])
M2 = sp.Matrix([[1 / f, q], [q, A]])
adj2 = M2.adjugate()
D2_ = sp.expand(M2.det())
wv = sp.Matrix([a, b])
W2_ = sp.expand((wv.T * adj2 * wv)[0, 0])
Delta_ = sp.expand(-M3.det())

print("=" * 72)
print("L2-S1: THE TWO RATES, COMPUTED FROM THE METRIC")
print("=" * 72)

check("L2-01 stationary-family rate = sqrt(-g_TT) = sqrt(f) on the full "
      "shaped + time-row class (w, q, a, b do NOT enter): the banked tie "
      "phi = -(1/2) ln f is EXACTLY this family's reading",
      zero_cancel(M3[0, 0] + f))

# slice-normal rate: N^2 = -1/g^TT; cofactor identity g^TT =
# cof_TT(M3)/det(M3) = det(M2)/det(M3) = D2/(-Delta), so N^2 = Delta/D2.
N2_expr = Delta_ / D2_
check("L2-02 slice-normal (lapse) rate: N^2 = -1/g^TT = Delta/D2 "
      "= f + W2/D2 exactly (cofactor identity; Delta = f D2 + W2, "
      "W2 = (a,b) adj(M2) (a,b)^T) — the time row and the angular block "
      "BOTH enter this family's rate",
      zero_cancel(N2_expr - (f + W2_ / D2_)))
check("L2-03 THE SPLIT IS TIME-ROW-ONLY: a = b = 0 forces N = sqrt(f) "
      "IDENTICALLY (all q, w, f) — on every diagonal-time configuration "
      "the two corpus formulas ('lapse' and 'sqrt(-g_tt)') are one "
      "object, which is why the corpus never had to choose [F2 part 1]",
      zero_cancel(sp.cancel(N2_expr.subs([(a, sp.Integer(0)),
                                          (b, sp.Integer(0))])) - f))

print()
print("=" * 72)
print("L2-S2: THE RATES ON C1'S OWN BRANCH (a*, b*) — where the fork is real")
print("=" * 72)
fT, fr, fth = sp.diff(f, T), sp.diff(f, r), sp.diff(f, th)
v2 = sp.Matrix([fr, fth])
P_ = sp.expand((v2.T * adj2 * v2)[0, 0])
Q_ = sp.expand(f * P_ - D2_ * fT**2)
R_ = sp.expand(f * P_ + D2_ * fT**2)
a_st = 2 * f * D2_ * fT * fr / Q_
b_st = (fth / fr) * a_st
# W2 on the branch: K = f_r b* - f_th a* = 0 and S = S* = 2 f D2 fT P/Q,
# so W2* = S*^2/P (Gram identity with K = 0).
W2_branch = sp.cancel(W2_.subs([(a, a_st), (b, b_st)]))
S_star = 2 * f * D2_ * fT * P_ / Q_
check("L2-04a branch values: W2(a*, b*) = S*^2/P exactly (K = 0 Gram "
      "identity)", zero_cancel(W2_branch - S_star**2 / P_))
N2_branch = sp.cancel(f + W2_branch / D2_)
check("L2-04 ON THE BRANCH: N^2 = f R^2/Q^2 EXACTLY, R = fP + D2 f_T^2, "
      "Q = fP - D2 f_T^2 — the time-row PERFECT SQUARE of the opener IS "
      "the slice-normal rate's factorization (N |Q| = sqrt(f) R): "
      "Q^2 + 4 f D2 P f_T^2 = R^2 <=> N^2 Q^2 = f R^2",
      zero_cancel(N2_branch - f * R_**2 / Q_**2)
      and zero_cancel(Q_**2 + 4 * f * D2_ * P_ * fT**2 - R_**2))

# the dilation field under each reading:
phi_stat = -sp.log(f) / 2
phi_norm = -sp.log(f * R_**2 / Q_**2) / 2
phi_corr = phi_norm - phi_stat          # = -(1/2) ln(R^2/Q^2)
check("L2-05 the reading split phi_norm - phi_stat = -(1/2) ln(R^2/Q^2) "
      "VANISHES IDENTICALLY on every static configuration (f_T = 0 => "
      "R = Q = fP) [F2 part 2 — no banked static/macro result can "
      "distinguish the readings]",
      zero_cancel(sp.cancel((R_ - Q_).subs(f, sp.Function('F')(r, th))
                            .doit())))

Fs = sp.Function('F')(T, r)
ratio_sph = sp.cancel((R_ / Q_).subs(q, sp.Integer(0)).subs(f, Fs).doit())
check("L2-06 on SPHERICAL (f_theta = 0, q = 0): R/Q = "
      "(f^2 f_r^2 + f_T^2)/(f^2 f_r^2 - f_T^2), w-INDEPENDENT (A "
      "cancels) — the split's w-content vanishes on spherical [F3 pt 1]",
      zero_cancel(ratio_sph
                  - (Fs**2 * sp.diff(Fs, r)**2 + sp.diff(Fs, T)**2)
                  / (Fs**2 * sp.diff(Fs, r)**2 - sp.diff(Fs, T)**2)))
subs_c = {f: 2 + r * T / 5 + r**2 * sp.cos(th)**2 / 7,
          q: r * sp.sin(2 * th) / 11,
          w: r**2 * sp.sin(th)**2 / 13}
pt = {T: Ra(1, 3), r: Ra(3, 2), th: Ra(7, 8)}
check("L2-07 ... but on SHAPED configurations the split DOES carry w: "
      "d(phi_norm - phi_stat)/dw != 0 (exact rational witness)",
      sp.cancel(sp.diff(phi_corr, w).subs(subs_c).doit().subs(pt)) != 0)
g_sonic = Fs * sp.diff(Fs, r)**2 - sp.diff(Fs, T)**2 / Fs
Q_sph_check = sp.cancel(Q_.subs(q, sp.Integer(0)).subs(f, Fs).doit()
                        .subs(w, sp.Integer(0)).doit())
check("L2-08 SCORECARD sonic coupling (exact identity): Q|spherical = "
      "A g (g = f f_r^2 - f_T^2/f), so the slice-normal rate "
      "N = sqrt(f) R/|Q| DIVERGES exactly on the sonic locus [F3 pt 2]",
      zero_cancel(Q_sph_check - r**2 * g_sonic))

print()
print("=" * 72)
print("L2-S3: THE C1 DENSITY UNDER EACH READING (computed, not chosen)")
print("=" * 72)
# R-stat: the banked density. Spatial-gradient quadratic via the 3x3
# adjugate (cofactor identity, no inversion):
grad_stat = sp.Matrix([sp.diff(phi_stat, x) for x in (T, r, th)])
K_stat_num = sp.expand((grad_stat.T * M3.adjugate() * grad_stat)[0, 0])
# K_stat = K_stat_num/det(M3); w-jet census needs only the numerator and
# det — both polynomial in the fields and their FIRST f-jets:
w_atoms_stat = ({d for d in K_stat_num.atoms(sp.Derivative) if d.expr == w}
                | {d for d in Delta_.atoms(sp.Derivative) if d.expr == w})
check("L2-09 reading R-stat: the C1 density carries NO derivative of w "
      "on this class (W1 Route A theorem, reconfirmed via cofactor "
      "census)", len(w_atoms_stat) == 0)

# R-norm on the branch: phi_norm contains w ALGEBRAICALLY and f's first
# jets; its gradient therefore contains w's FIRST jets (F4: that is the
# honest claim — the density is first-jet in w, second-jet in f; the EL
# for w is then SECOND order: w is dynamical).
dphin_dth = sp.diff(phi_norm, th)
# coefficient of w_theta in d_theta(phi_norm): chain rule = d(phi_norm)/dw
# evaluated... extract by substituting jets with symbols:
wth_atom = sp.Derivative(w, th)
coef_wth = sp.diff(dphin_dth, wth_atom)
coef_val = sp.cancel(coef_wth.subs(subs_c).doit().subs(pt))
check("L2-10 reading R-norm [F4-corrected claim]: the C1 density's tied "
      "slot phi_norm = -(1/2) ln(f R^2/Q^2) carries w ALGEBRAICALLY, so "
      "grad(phi_norm) carries w_r, w_theta, w_T (exact rational witness: "
      "coeff[w_theta] in d_theta phi_norm != 0) — ANGULAR STRUCTURE "
      "ENTERS THE TIED SLOT and w ACQUIRES DERIVATIVES in the C1 density "
      "(first-jet density => second-order w-EL: w is DYNAMICAL under "
      "this reading), with zero new postulates. Exactly the W1-VA "
      "proviso mechanism, realized by a metric-defined object",
      coef_val != 0)
# and f acquires SECOND jets in the density under R-norm (honest extra):
f_second = {d for d in dphin_dth.atoms(sp.Derivative)
            if d.expr == f and d.derivative_count == 2}
check("L2-11 honest extra: under R-norm the tied slot also carries f's "
      "FIRST jets, so the density carries f's SECOND jets — R-norm "
      "would change the f-sector's differential order too (the readings "
      "are not a w-only fork; reported as computed)",
      len(f_second) > 0)
check("L2-12 R-norm reduces to the banked tie on every static "
      "configuration (phi_norm = phi_stat when f_T = 0): both readings "
      "reproduce the banked spherical vacuum, the macro sector, and all "
      "static results IDENTICALLY [F2 closed]",
      zero_cancel(sp.cancel((R_ - Q_).subs(f, sp.Function('F')(r, th))
                            .doit())))

print()
print("=" * 72)
print("L2-S4: RANKING BY DERIVATION STRENGTH (the F1 adjudication)")
print("=" * 72)
ranking = """
RANK 1 — R-stat (the banked tie). Derivation strength: EXPLICIT CORPUS
  DEFINITION. The S58-009 chain states the postulate AT THE METRIC
  COMPONENT: "g_tt = -e^{-2 phi} c^2 ... as primitive structural
  ingredient". Every observer statement the corpus makes (the
  stationary family) is consistent with and downstream of it. On this
  reading the W1 theorem stands: C1 is first-jet in g_TT only; no
  w-dynamics; the forced object remains missing.
RANK 2 — R-norm (slice-normal / lapse). Derivation strength: UNFORCED
  FORK. Its only corpus anchor: the corpus's word "lapse" (sec 1.3)
  denotes the same object as sqrt(-g_tt) on every class the corpus
  ever computed on; the two formulas split only on the time-row-on
  class, which no corpus text addresses. No corpus text defines phi
  operationally in a way that selects N over sqrt(-g_tt) there. The
  medium/weld-frame picture that would motivate R-norm is a hunch
  (memory), not corpus.
VERDICT (F1): THE CORPUS DOES NOT FORCE THE READING THAT PUTS ANGULAR
  STRUCTURE IN THE TIED SLOT. The confirming outcome dies as a forced
  result — recorded as a death. What survives, uncovered not chosen:
  (i) the readings split EXACTLY and ONLY where the forced object
      lives (shaped + moving configurations) and nowhere the data or
      the banked stack has ever looked (L2-03, L2-05, L2-12);
  (ii) the split factor IS the opener's perfect square: N |Q| =
      sqrt(f) R (L2-04) — the square is the lapse factorization of
      the metric's own normal-observer rate;
  (iii) under R-norm, w enters the tied slot and becomes dynamical
      with zero new postulates (L2-10), at the price of raising the
      f-sector's order (L2-11);
  (iv) the split diverges exactly on the sonic locus (L2-08) and its
      w-content vanishes on spherical (L2-06).
"""
print(ranking)
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL")
assert not FAIL
