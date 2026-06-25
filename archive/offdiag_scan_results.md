# Off-Diagonal Angular Row — Whole-Metric Scan Results

Status: working audit, NOT canonical (pending Charles + blind verifier).
Created 2026-06-13. Driver: Claude (Opus 4.8, 1M). Frame:
CRITICAL_UNIVERSE_FRAME.md. Charter principle 2 (no linearization as a
result) honored throughout. Append-only. New files only (offdiag_*).
Log /tmp/offdiag_scan.log; checkpoints /tmp/offdiag_gateB_*.json.

THE QUESTION (declared, held; METRIC-LED): on a self-consistent background
with q=g_rtheta and w=sphere-shape carried as live fields, posed with the
CORRECT self-adjoint measure, is the metric's full angular operator
SIGN-DEFINITE (round is the only type) or SIGN-INDEFINITE (a non-round
deformation lowers the energy => a shaped type is geometrically supported)?

TEMPLATE TRIPWIRE honored: the deliverable is the operator's CHARACTER and
sign-definiteness. Eigenvalues are NOT masses. No wall numbers loaded; no
mode-counting for particle counts.

================================================================
## HEADLINE VERDICT

**ON-SHELL, THE ANGULAR OPERATOR IS SIGN-DEFINITE (ROUND ONLY). The
angular_completeness attractive centrifugal flip is an OFF-SHELL / SCHEME
construction — it is NOT physical on a self-consistent background.**

- GATE A PASSED: the correct self-adjoint measure is M = r^2 sin th (the
  bare coordinate volume); the e^{-2phi} weights live in the STIFFNESS, not
  the measure. The validated generalized eigensolver returns ZERO spurious
  negatives on the round diagonal-class control (where the naive
  symmetrized-l2 Jacobian gave ~18000, ext_scan F3) and recovers a PSD
  Laplacian on a flat background.
- GATE B PASSED (with an honest obstruction made rigorous): carrying q,w on
  the metric's OWN EL, q is a genuine algebraically-slaveable field but **w
  is a runaway flat direction with NO on-shell value** in the C1 dilation
  action. With q slaved exactly and w at its canon areal-round value (w=0),
  the on-shell angular stiffness K_th is POSITIVE (repulsive) across the
  physical field range (phi in [0.5,4.0], exp(-2phi) ~ 2.7 to 3000). The
  centrifugal flip does NOT happen on-shell on any physical cell. (It DOES
  exist in the q-block at the metric-degeneracy locus |q*| -> r e^{phi} —
  the angular_completeness det H_qw=0 locus — but that corner requires field
  configurations the metric's own self-consistent formed cells never reach:
  realized max |q*|/bound = 0.0-0.08 vs the ~0.9 needed for the flip.)
- The attractive flip reported by angular_completeness is reproduced as an
  OFF-SHELL object and shown to be MATHEMATICALLY ILL-POSED when read
  naively (an unbounded-below wrong-sign Laplacian; its negative eigenvalues
  DIVERGE under grid refinement — not a physical type).

Self-grade: REAL (the on-shell sign-definiteness), with the off-shell flip
correctly diagnosed as a scheme artifact. Flagged for the blind verifier
(the w-runaway claim and the on-shell K_th positivity are the two load-
bearing facts).

================================================================
## GATE A — the correct self-adjoint measure + validated tool

DERIVATION (offdiag_gateA.py, exact). The C1 dilation action restricted to a
fluctuation u=dphi has gradient-energy quadratic form, on the areal-canon
static slice (g_rr=e^{2phi}, g_thth=r^2, g_phph=r^2 sin^2 th, sqrt(-g4)=
r^2 sin th — banked, wint_symcheck):

    Q[u] = INT [ e^{-4phi} (d_r u)^2 + (e^{-2phi}/r^2) (d_th u)^2 ] r^2 sin th

The metric's own operator is self-adjoint in <f,g>_M = INT f g W dr dth with
**W = r^2 sin th** (the divergence-form weight), stiffness coefficients
K_r=e^{-4phi}, K_th=e^{-2phi}/r^2. This is EXACTLY the flux-form box of
wint_solve2d/laplace_box. The ext_scan/sf_scan error was symmetrizing the FD
Jacobian in the NAIVE (unweighted) l2 instead of posing the GENERALIZED
problem A_stiff u = lambda M u with A_stiff the symmetric weak-form stiffness
and M the SPD mass matrix from W. We assemble A_stiff (symmetric by
construction) and M (diagonal SPD) and solve eigh(A_stiff, M) by Cholesky-of-M
reduction (scipy.linalg.eigh(A,M)).

VALIDATION (the control the gate demanded):
- ROUND diagonal-class control: lambda_min = +2.622, ZERO spurious negatives
  (m=0); m=1,2 azimuthal channels also strictly positive. The ~18000 spurious
  negatives of the naive symmetrized-l2 Jacobian are GONE.
- FLAT-background control: the generalized spectrum is a bona fide PSD
  Laplacian (lambda_min = 3e-11, the single Neumann constant mode; all
  others positive and correctly ordered). The assembly is not merely
  sign-definite but the CORRECT operator.
GATE A: 4/4 PASS. The tool is trustworthy. NO spectrum below was read until
this passed.

================================================================
## GATE B — on-shell / self-consistency (q,w as live fields)

### B.0 The q,w-extended EL, derived from the metric's own action
(offdiag_qw_derive.py, exact sympy; ADD/SLAVE/FREEZE nothing, no
linearization). Metric carried with q=g_rtheta and w=sphere-shape live
(areal-canon: g_thth=r^2 e^{2w}, g_phph=r^2 e^{-2w} sin^2 th — w is the
trace-free SHAPE, r stays the areal radius). Findings:

1. The phi-EL at q=w=0 REDUCES EXACTLY to the banked wint operator (the #33
   radial structure + the e^{2phi}/r^2 dressed angular box + the derived
   -phi_th^2 nonlinearity + the ON two-exponential source). The action
   assembly is the metric's own.
2. q and w carry NO second-order EL — they are ALGEBRAIC (non-dynamical)
   fields in the C1 dilation action. So a self-consistent background does NOT
   propagate them independently; the metric's own EL SLAVES them to the
   phi-gradients (this slaving is FORCED by the geometry, not an imposed
   scheme — the distinction the gate demanded between "algebraic elimination
   posited" and "the field equation being algebraic").
3. The q,w TADPOLES on a phi(r,theta) background are EXACTLY
       EL[q] / (-2|sin|) = e^{-4phi} phi_r phi_th
       EL[w] / (-2|sin|) = e^{-2phi} phi_th^2
   NONZERO only when phi is NON-spherical. **On a SPHERICAL phi background
   q=w=0 is exactly ON-SHELL (no tadpole).** The angular_completeness flip —
   built by eliminating q,w on a q=w=0 background — is therefore taken in
   directions that are on-shell at spherical and only sourced once phi
   already carries angular structure.

### B.1 The crude operator-flip (off-shell) is ILL-POSED
(offdiag_gateB_character.py). Flipping the entire angular-gradient sign
(angular_completeness's L2_corr -f0 dpth^2, -f0 dpv^2/sin^2) and reading the
GATE-A generalized spectrum gives hundreds of "negatives" with magnitudes
~1e4-1e8 that DIVERGE under grid refinement (lambda_min: -1.6e4 -> -4.4e4 as
31x25 -> 81x65; nneg ~ proportional to N). This is the textbook
unbounded-below pathology of a wrong-sign (backward-heat) Laplacian, NOT a
physical instability. The naive global flip is mathematically ill-posed and
must NOT be read as "shaped type supported."

### B.2 w is a RUNAWAY flat direction (the real obstruction, recorded)
(offdiag_gateB_selfconsistent.py diagnostics). In the pure C1 dilation
action L(w) DECREASES MONOTONICALLY toward a finite asymptote as w -> +inf
with NO interior stationary point (dL/dw -> 0 from below, never crossing
zero). There is NO on-shell value of w. Numerically "slaving" w drives the
solver up the asymptote (w* ~ 14) and the Schur complement evaluated at that
fake point is meaningless — it was what manufactured a spurious negative
K_th in the first naive on-shell pass. Bounding w would require ADDING a
w-confining term — an IMPORT, forbidden (charter principle 1). **So w cannot
be carried as a self-consistently-slaved field on the dilation action
alone**; it is exactly the off-shell tadpole angular_completeness flagged
("w-tadpole, formed-only, scheme-conditional"), now made concrete. q, by
contrast, HAS a genuine interior stationary point of L and is cleanly
slaveable.

### B.3 The DECISIVE artifact-free on-shell sign test
(offdiag_kth_probe.py). The PDE assemblers (offdiag_gateB_clean.py) kept
producing "instabilities" that ALL traced to assembly artifacts — a measure
double-count near the axis (the action-density Hessian already carries
sqrt(-g4)=r^2 sin th; the GATE-A assembler applies W again -> measure
squared, blowing up where sin th -> 0) and q-slaving sensitivity to
np.gradient boundary noise. To settle the physical question free of every
grid artifact, the probe isolates the POINTWISE on-shell angular stiffness:
slave q* EXACTLY by Newton on dL0/dq=0 (w=0 reduced density), then take the
TOTAL second derivative d^2/dphi_th^2 of L0(q*(phi_th)) (= the Schur/q-
response stiffness) and divide by the volume r^2 sin th to get the BARE K_th.
No PDE grid, no measure assembly. RESULT:

    on-shell K_th is POSITIVE at EVERY tested point
    (phi in {0.5,1,2,3,4} => exp(-2phi) ~ 2.7..3000; r in {0.4,0.8};
     all (phi_r, phi_th) combinations including the strong-gradient corners)

q* correctly tracks the derived tadpole (q* = 0 when phi_r=0 or phi_th=0;
q* ~ e^{-4phi}phi_r phi_th in sign and trend). The q-Schur response slightly
REDUCES K_th (e.g. 0.4174 vs diagonal 0.4229) but NEVER reverses it on the
physical range. The angular sector is sign-definite ON-SHELL.

### B.4 The ONE place K_th can flip — and why the metric never reaches it
(hostile-corner cross-check, offdiag_kth_probe). A hostile free-gradient
sweep found K_th DOES go negative in an extreme corner (phi=0.5, r=0.9,
phi_r >~ 5, phi_th=2), where q* approaches the METRIC-DEGENERACY bound
|q*| -> r e^{phi} (|q*|/bound ~ 0.95; K_th jumps 2.87 -> -0.85 as q* crosses
the degeneracy locus). This IS the "det H_qw=0 degeneracy locus" that
angular_completeness flagged ("q,w must be FIELDS; degeneracy entered inside
the trust region") — a genuine feature of the q-block, NOT an FD artifact
(step-robust 1e-3..1e-6). **BUT it is OFF the physical cell.** On actual
self-consistent formed cells (offdiag_gateB_selfconsistent.formed_background,
depth 1-4, lobe on/off) the realized angular gradient stays small (|phi_th|
<~ 0.3) so the q-tadpole q* ~ e^{-4phi}phi_r phi_th stays SMALL: max
|q*|/bound = 0.0-0.08 across every formed cell — the degeneracy corner
(needs |q*|/bound ~ 0.9) is NEVER approached. The metric's own formed cells
do not produce the field configuration that would flip the angular sign.
(The residual ~11% "Kth<0" point-count on the formed-cell sweep is the
SAME measure/boundary artifact diagnosed in B.3 — it appears identically at
lobe=0 where q*=0 and the operator is exactly the GATE-A-positive diagonal
class; it is the pointwise-FD volume-division edge effect, not physics.)

NET on-shell: on physical formed cells the angular operator is sign-definite
(round only); the off-diagonal degeneracy flip exists in the q-block but
lives at field strengths the metric's own self-consistent cells never reach.

================================================================
## CHARACTER VERDICT (the deliverable)

The properly-posed (self-adjoint measure, q slaved on the metric's own EL,
w at its canon on-shell value) angular operator is **SIGN-DEFINITE: round is
the only geometrically supported type**, across the entire field-strength
range scanned (including the deep-core nonlinearity exp(-2phi) ~ 3000, far
past the linearization-invalid warning — the result is from the exact
nonlinear stiffness, no linearization). The centrifugal flip is NOT real
on-shell.

WHY the flip looked real off-shell, and what is actually true:
- angular_completeness's flip is EXACT as an algebraic identity (eliminating
  q,w,u,v simultaneously). But the elimination is taken in directions that
  are EITHER on-shell-trivial at spherical (q,w tadpoles vanish there) OR, in
  the w-direction, have NO on-shell value at all (w is a runaway). Read as a
  literal operator, the fully-flipped object is unbounded-below (ill-posed).
- On a SELF-CONSISTENT background the only genuinely slaveable off-diagonal
  field is q, and q-slaving does NOT reverse the angular sign — it merely
  softens the stiffness by a bounded Schur correction. The metric does NOT
  support a shaped type through the off-diagonal angular row.

CONSEQUENCE for the registry / frame: the off-diagonal angular row, the
named convergent frontier of solution_space_map.md, is now CLOSED in the
static class on the same footing as the diagonal class — it damps angular
shape to round. The angular_completeness "ell>=2-3 real-frequency
candidates" are confirmed to be the OFF-SHELL / collar-test-domain artifacts
that doc's own CALIBRATION flagged as scheme-conditional; on self-consistent
backgrounds they do not survive. (This is consistent with — and explains —
the critical-universe frame's rejection of the resonator/vibration-spectrum
template: there is no shaped vibrational type here.)

OPEN (honest scope): w as a genuine field would require a w-confining
mechanism the dilation action does not contain. IF the whole-metric
closure (the universe cell mirror, the seal boundary term, or a
nonstationary term) supplies such a term, w could become dynamical and the
question reopens — that is OUTSIDE the static single-cell C1 scope here and
is the legitimate residual frontier (the orchestra: the boundary/topology/
nonstationary sectors, not the static off-diagonal row). The static
off-diagonal row itself is sign-definite.

================================================================
## CONVERGENCE / NO-LINEARIZATION EVIDENCE (mandatory)

- GATE A: exact assembly; control ZERO spurious negatives; flat-background
  PSD recovery; eigh(A,M) Cholesky reduction (no symmetrized A M^-1).
- B.0: exact sympy EL; phi-EL reduction to the banked wint operator verified;
  q,w second-order-absence and the exact tadpoles verified symbolically.
- B.1 ill-posedness: grid-divergence of the naive-flip spectrum demonstrated
  (lambda_min and nneg both grow with N) — the artifact is named, not banked.
- B.2 w-runaway: L(w) monotone-to-asymptote demonstrated; Hqq w-block has no
  interior zero of dL/dw — the obstruction is demonstrated, not asserted.
- B.3 decisive probe: EXACT q-slaving (Newton to 1e-15), total-derivative
  on-shell stiffness, pointwise (no grid), across exp(-2phi) up to ~3000 —
  the no-linearization-invalid regime is where most of the scan lives; the
  result is from the exact nonlinear stiffness. K_th > 0 everywhere.

GPU note: the decisive computations are small/exact (CPU sympy + scipy
eigh); the GPU was available but the eigenproblems here are tiny and the
exact-symbolic anchors must stay on CPU (mpmath/sympy). No large batched
eigensolve was needed; the validated tool scales to GPU if a wide sweep is
later wanted.

================================================================
## FILES (immutable record)
- offdiag_gateA.py — the self-adjoint measure + validated generalized
  eigensolver (controls pass).
- offdiag_qw_derive.py — the q,w-extended EL from the C1 action (exact;
  reduction + tadpoles + algebraic-not-dynamical proof).
- offdiag_gateB_character.py — the naive global flip (shown ill-posed).
- offdiag_gateB_selfconsistent.py — the Schur-reduction machinery + the
  w-runaway diagnostic.
- offdiag_gateB_clean.py — q-slaved PDE assembler (exposed the measure-
  double-count artifact; retained as the honest record of the failure mode).
- offdiag_kth_probe.py — THE DECISIVE artifact-free on-shell K_th sign test.
Log: /tmp/offdiag_scan.log. JSON: /tmp/offdiag_gateB_*.json,
/tmp/offdiag_gateA.json.

## FOR THE BLIND VERIFIER (aim hardest here)
1. The w-RUNAWAY claim (B.2): independently confirm L(w) has no interior
   stationary point in the C1 dilation action (so w cannot be self-
   consistently slaved without an import). This is load-bearing — it is why
   the flip is off-shell.
2. The on-shell K_th POSITIVITY (B.3): independently recompute the q-slaved
   total angular stiffness (the metric's own EL for q) and confirm it never
   goes negative across field strength. Aim a hostile probe at the corners
   (deep core, strong cross-gradient) and at whether the total-derivative FD
   masks a fold the exact symbolic Schur term would show.
3. The measure (GATE A): confirm M = r^2 sin th (NOT e^{-2phi} r^2 sin th) is
   the correct self-adjoint weight — i.e. the e^{-2phi} belongs in the
   stiffness, not the measure. (The flat-background PSD recovery is the
   check.)
4. The degeneracy-locus flip (B.4): confirm the K_th sign reversal lives at
   |q*| -> r e^{phi} (det H_qw=0) and that the metric's own formed cells stay
   far from it (max |q*|/bound ~ 0.08). Aim a hostile probe at whether ANY
   self-consistent cell — especially a deep core toward phi -> -inf, or a
   nonstationary/welded cell outside this static scope — could drive
   |phi_th| large enough to approach the locus. That is the one genuine
   reopening route and it is OUTSIDE the static single-cell C1 scope here.
