# Strong-Field / Off-Diagonal Whole-Metric Scan — Results

Queue-head step (b)/(c), HANDOFF item 1, the STRONG-FIELD / OFF-DIAGONAL
axis (solution_space_baseline.md axis table, last row). Driver: Claude
(Opus 4.8). Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md. Append-only
research record (working audit, NOT canonical). HYPOTHESIS-GRADE; flagged
for blind verifier. New files only: sf_scan_strongfield.py,
sf_scan_probe1b.py, sf_scan_probe1c.py, sf_scan_probe2.py, sf_scan_anggap.py.
Log: /tmp/sf_scan.log; checkpoints /tmp/sf_probe1.json, sf_probe1c.json,
sf_probe2.json, sf_anggap.json.

## The axis and the baseline being tested

The documented interior baseline (B1, registry #34/#36): with both sectors
live and two-way, the bulk damps every angular shape to round; the angular
operator is PURE DAMPING; the round-cell bifurcation gap is bounded away
from zero (banked ~0.65 over the trust E-family); ONE round type, a smooth
E-continuum. PREMISE SET (where it was proven): a TRUST WINDOW — modest
depth (E/Um up to ~4–6, nonlinearity exp(-2v) up to ~16) and the angular
drive effectively OFF (only the metric's dressed SCALAR operator; no live
off-diagonal/shear field). The named open frontier (baseline table): "the
fully two-way, unfrozen, strong-field off-diagonal (large shear, deep core
toward phi->-inf) solution is not mapped; whether documented invariants
persist there is open."

This scan steps OUTSIDE that premise set on two fronts, with the metric's
OWN derived operators, nothing frozen/slaved/added, no linearization as a
result.

## Method (what was solved)

PROBE 1 (scalar, strong field). The EXACT wint two-way residual + existence
test (the metric's own e^{2v}-dressed angular operator A = e^{2v}(v_thth +
cot th v_th - v_th^2) + ON two-exponential source Phi(e^{-2v}-e^{v}),
v(m,theta) live both sectors; wint_symcheck-verified as the metric's own C1
EL), driven FAR past the trust window: partition energy E/Um from 1.1 to
1000, so the deep-core depth |v_min| and the nonlinearity exp(-2 v_min) run
to ~3000 (well past the exp(-2phi)~5 hadronic-depth warning and the trust
window's ~16). Full nonlinear Newton solve at each E (maxres ~1e-10);
linearization-validity exp(-2v_min) reported at every point — we rely on NO
linearization, the Jacobian is the exact FD Jacobian of the full nonlinear
residual.

PROBE 2 (off-diagonal / shear live). The metric's OWN ell=1 off-diagonal /
sheared class f = F(y)(1 + kappa cos theta) carrying the off-diagonal shape
amplitude a = F*kappa as a co-equal field (the angular drive ON). The
source-free shape-channel potential (fork_tests trivial-cell lemma,
series-verified) P_a = a/F + (6/5)a^3/F^3 + (81/35)a^5/F^5, plus the DERIVED
phi-angular cross-block (sourced_second_jet finding 6, V2-verified to
1e-12): V_a0gamma0 = -sqrt(15)kappa/3F, V_a1gamma1 = -sqrt(5)kappa/2F. The
full {amplitude, shape} reduced Hessian eigenstructure scanned across kappa
in (0.05, 0.999) — the whole approach to the documented kappa->1 metric
degeneration, well past the ~0.97 trust edge. EXACT sympy/mpmath; the
Hessian IS the exact second jet of the derived reduced potential (no
linearization as a result).

Discriminators for any flagged signal (probes 1b/1c/anggap): grid
refinement; unit-chart rescale (operator on a fixed domain); 1D-radial-vs-2D
match; and — decisive — the BLIND-VERIFIED (ab035deeb...) symmetric,
angular-restricted bifurcation gap (Js=(J+J^T)/2, eigh, smallest |eig| with
a theta-varying eigenvector), the SAME diagnostic that established the
banked ~0.65 trust-window gap.

## The map (what the strong-field/off-diagonal whole metric does)

PROBE 1 — scalar deep core (existence-test raw min|eig|): non-monotone. It
RISES across the trust window (0.0153 -> 0.145 at E/Um=6, reproducing B1's
banked monotone-rise exactly), then TURNS OVER at the trust edge and DECAYS
steadily toward zero at strong field (0.145 -> 0.0019 at E/Um=1000,
nonlin~3000). Read naively this looks like an approaching bifurcation —
exactly the kind of "character change past the trust window" the scan hunts.
IT WAS PROSECUTED HARD and found to be an ARTIFACT (see below).

PROBE 2 — off-diagonal/shear Hessian: CLEAN NEGATIVE. The shape stiffness
P_aa at amplitude a=F*kappa is (405 kappa^4 + 126 kappa^2 + 35)/(35 F); the
derived phi-angular cross-block |V_a0gamma0| = sqrt(15)kappa/3F. As field
strength rises toward the kappa->1 degeneration, the cross-block GROWS but
the shape stiffness grows FASTER (the 405 kappa^4 term dominates), so the
overturn-threshold s_crit = (cross/P_aa)^2 DECREASES monotonically (0.075 at
kappa=0.3 down to 0.0064 at kappa=0.999). The {amplitude, shape} block stays
strictly positive-definite all the way to kappa=0.999, far past the 0.97
trust edge. The derived phi-angular coupling becomes RELATIVELY WEAKER, not
stronger, deep in the field. NO off-diagonal shaped type is born. This
robustly EXTENDS fork_tests #3 strict-positivity into the strong-field /
large-shear regime.

DECISIVE angular-gap test (sf_scan_anggap.py, blind-verified diagnostic):
the trust-window cross-check reproduces the banked gap (0.94 -> 0.65 over
E/Um 1.3->4). At STRONG field the symmetric angular bifurcation gap does NOT
go to zero: it decreases from 0.85 and ASYMPTOTES CLEANLY to exactly 0.5 as
E/Um -> 1000 (nonlin -> 3000), positive, sign-definite, grid-converged
(0.50000 at three radial AND three angular resolutions). The angular sector
STAYS pure damping into the deep core.

## Flagged candidate anomalies — and their adjudication

FLAG-1 (raised, then REFUTED as artifact). "Strong-field bifurcation: the
existence-test Jacobian min|eig| decays toward zero past the trust window."
ADJUDICATION (blind discriminators, self-prosecuted):
 - (1b) the raw FD min|eig| SHRINKS ~25-30% per grid refinement at FIXED E,
   and its near-null eigenvector is FULLY ANGULAR (ang content = 1.00) — a
   grid-limited mode, not a converged physical eigenvalue.
 - (1c) the 1D radial stiffness RISES (0.23 -> 1.0) while the 2D min|eig|
   FALLS — the soft mode is NOT radial; and in the unit-width chart the
   decay persists, so it is not pure cell-shrinking either. (My first hand-
   deflated "symmetric angular gap" gave huge negatives EVEN IN THE TRUST
   WINDOW — a self-evident artifact from symmetrizing the BC-contaminated
   raw Jacobian; discarded.)
 - decisive: the BLIND-VERIFIED symmetric angular-restricted gap (the
   trustworthy object) is POSITIVE and asymptotes to 0.5 — NOT zero. The raw
   min|eig| decay is the superposition of (i) the documented RADIAL
   E-continuum slide (B2b/#33: a continuum of cells in E, whose own near-
   zero family-mode is expected) and (ii) BC-row contamination, NOT an
   angular bifurcation.
 SELF-GRADE: ARTIFACT. Documented behavior (B1 pure damping) HOLDS into
 strong field. This is a textbook instance of the verifier-before-record
 rule earning its keep — a naive scan would have banked a false bifurcation.

FLAG-2 (raised as "gap -> 1/2 floor", then DEMOTED to a BC-flavored number;
the ROBUST content is the SIGN, not the value). The symmetric angular gap
asymptotes to a clean grid-independent 0.5 at strong field (0.500008 ->
0.500000 under Nm and Nth refinement). BUT on prosecuting it (verifier
concern (a), self-checked): the gap EIGENVECTOR is structureless — its
Legendre content is ~0 in every l (coef[1:4] all ~0) and it concentrates on
the theta-BOUNDARY columns (boundary-column fraction ~1.0-1.4) — at strong
field AND in the trust window alike. So the symmetric angular-gap VALUE
(including the banked ~0.65 it was validated against) is dominated by the
axis-Neumann BC-closure rows, NOT a clean physical bulk l=1 shape mode. The
exact 0.5 (and 0.65) are therefore BC-flavored numbers and are NOT banked as
physical metric constants. SELF-GRADE: the VALUE is a BC artifact; demoted.
What IS robust and physical: the gap is POSITIVE, sign-definite, bounded
away from zero, and never softens to zero or flips across the entire
strong-field family — i.e. NO bulk angular mode goes unstable. That
qualitative statement (the B1 character) survives; the quantitative 1/2
floor does not bank.

## CRITICAL SCOPE LIMIT — the off-diagonal-ON attractive-ladder region (NOT reached)

Both probes use the DIAGONAL-class angular operator: PROBE 1 the wint
e^{2v}-dressed scalar operator (g_rtheta = q OFF), PROBE 2 the source-free
ell=1 reduced potential (also diagonal-class). The banked, blind-verified
angular_completeness_results.md (VAA 2026-06-11) establishes — EXACTLY,
gauge-protected — that carrying the FULL OFF-DIAGONAL ROW LIVE (time row
a,b,p; g_rtheta=q; shape w; axial u,v) FLIPS THE ANGULAR-GRADIENT
(centrifugal) TERM TO ATTRACTIVE SIGN, which "the diagonal class
structurally cannot produce," and at ell>=2-3 yields REAL-FREQUENCY
OSCILLATION CANDIDATES — a discrete real-frequency ladder (1 -> 6 candidates
as ell -> 6) — on collar TEST domains. The decisive computation (that
corrected, off-diagonal-ON spectrum on SELF-CONSISTENT, q,w-on, strong-field
FORMED backgrounds) was left explicitly UNDONE, "owned by the full-PDE run."

THEREFORE: my "baseline holds" verdict is SCOPED TO THE DIAGONAL-CLASS
angular operator. It does NOT test the attractive-sign off-diagonal regime —
which is exactly the named undocumented region of this axis and the most
likely place a shaped/oscillatory type is born. My probes confirm the
DIAGONAL-class damping persists into strong field (a real, if scoped,
extension of B1); they do NOT close the off-diagonal-on question. This is the
honest boundary of the scan.

(Note: an untracked file sf_scan_symcheck.py is present in the working tree,
created at 16:07 by an sf_scan_* / Opus 4.8 / 2026-06-13 author, aimed
precisely at re-deriving the off-diagonal g_rtheta angular-gradient sign flip
from the C1 action and scanning the corrected-class strong-field Jacobian for
a zero. It was NOT authored, run, or verified in THIS session and is NOT
incorporated into any result here — flagged for the next session / Charles.
It correctly identifies the gap my two probes leave open.)

## Honest verdict (the distilled map)

BASELINE HOLDS on the DIAGONAL-class strong-field axis, with its reach now
EXTENDED far past the trust window — but the OFF-DIAGONAL-ON corrected-class
region (the attractive ell>=2-3 ladder, banked as CANDIDATES on test
domains) is the genuine open frontier this scan did NOT reach (see scope
limit above):
 - SCALAR deep core to nonlin~3000 (E/Um=1000): the angular sector stays
   pure damping; the bifurcation gap stays POSITIVE and sign-definite,
   never softening to zero or flipping (the gap VALUE is BC-flavored and not
   banked, but its positivity is robust). NO shaped scalar type is born deep
   in the core. (B1 character confirmed and extended; FLAG-1 refuted as
   artifact; FLAG-2 value demoted, sign-content kept.)
 - OFF-DIAGONAL / SHEAR (ell=1 amplitude live, the angular drive on) to
   kappa=0.999: the {amplitude, shape} Hessian stays strictly positive; the
   derived phi-angular cross-block becomes relatively weaker, not stronger,
   approaching degeneration. NO off-diagonal shaped type is born.
   (fork_tests #3 strict-positivity confirmed and extended into strong
   field.)

SCOPE REACHED: single open-interior cell; static; ON two-exponential
source; the metric's own e^{2v}-dressed scalar angular operator (PROBE 1)
and the derived ell=1 off-diagonal reduced potential + phi-angular
cross-block (PROBE 2); E/Um up to 1000 (nonlin exp(-2v) up to ~3000); kappa
up to 0.999. NOT reached (left to other axes / future pushes): the
NONSTATIONARY off-diagonal sector (the f_T-driven fold, where #36/W6 and the
baseline both point the discreteness reopening — PROBE 1/2 are static); the
fully live differential off-diagonal field SOLVED two-way through a 2D BVP
at the SEAL closure (PROBE 2 used the derived reduced potential, not a live
2D (F,a) seal solve); the genuine kappa->1 metric degeneration itself
(approached to 0.999, the curvature-singular seal f^2 K -> 12 a^2/y^4 is the
documented endpoint, not crossed). On the regimes actually mapped, the
metric does nothing undocumented in CHARACTER — it damps angular shape and
keeps the off-diagonal channel stiff — and the one new quantitative fact (the
1/2 gap floor) is baseline-consistent.

## Convergence / no-linearization evidence (mandatory, recorded)

- PROBE 1: all 11 strong-field solves converged, maxres 3e-13..5e-10; the
  full NONLINEAR residual is solved at every E; exp(-2 v_min) reported
  (1.8 .. 3000) — the linearization-invalid regime (>5) is where most of the
  scan lives, and the result is from the nonlinear solve, not a linearization.
- angular gap: trust-window cross-check reproduces the banked ~0.65 (and
  the strong-field gap is grid-converged 0.50000 across Nm in {61,81,121,161}
  and Nth in {21,31,41,61}); CAVEAT recorded — the gap EIGENVECTOR is
  structureless/BC-concentrated even in the trust window, so the diagnostic's
  trustworthy content is the SIGN (positive, never zero/negative), not the
  exact value. The negative findings (no scalar/off-diagonal type born) do
  not depend on the value.
- PROBE 2: exact symbolic Hessian (sympy) + mpmath 40-digit eigenvalues; no
  numerical solve, no linearization — the Hessian is the exact second jet.

## For the blind verifier

Aim hardest at: (a) whether the angular-gap diagnostic (gaps()) is truly
sign-reliable at strong field or whether the 0.5 floor is itself a
symmetrization artifact of the BC rows (cross-check by an independent
self-adjoint angular operator, not the symmetrized FD Jacobian); (b) whether
PROBE 2's reduced-potential Hessian is the right object for "a shaped
off-diagonal type born" or whether the LIVE 2D (F,a) seal BVP could find a
fold the reduced potential misses (PROBE 2 is the homogeneity/Hessian
statement, not a live 2D solve — its scope); (c) the FLAG-1 artifact call —
confirm the raw min|eig| decay is fully accounted for by the radial
E-continuum + BC contamination and carries no residual angular signal.
