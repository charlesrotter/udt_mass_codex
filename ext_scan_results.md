# Exterior / Medium Whole-Metric Scan — Results

Status: working audit, NOT canonical. Created 2026-06-13. Driver: Claude
(Opus 4.8, 1M). Frame: CRITICAL_UNIVERSE_FRAME.md. Append-only.
Task: HANDOFF item 1 step (b), the EXTERIOR / MEDIUM axis of the
open-ended whole-metric solution-space scan. Yardstick:
solution_space_baseline.md (B1-B6). New files only (ext_scan_*).

Scripts (immutable record):
- ext_scan_whole.py — the broad exterior map + (attempted) angular-gap
  sweep + threshold sweep + artifact-control verifier (PARTS A-D).
- ext_scan_verify.py — lean independent existence test (Newton / PTC /
  Phi-continuation) + sparse angular-gap (Q1, Q2).
- ext_scan_fold.py — the clean, fast existence-fold mapper (the decisive
  robust result): critical source strength Phi_c by Phi-continuation +
  interior control + grid convergence.
Logs: /tmp/ext_scan.log, /tmp/ext_scan_verify.log, /tmp/ext_scan_fold.log.
JSON: /tmp/ext_scan_A.json, /tmp/ext_scan_fold.json.

All operators are the metric's OWN, TAKEN verbatim from wint_solve2d.py /
wint_cell2d.py: the dilation-weighted box
Box_g phi = (1/r^2) d_r(r^2 e^{-2phi} phi_r)
          + (1/(r^2 sin th)) d_th(sin th e^{-2phi} phi_th)
and the derived ON restoring source S(phi) = Phi(e^{-2phi} - e^{phi}).
Convention f = e^{-2phi}: INTERIOR f<1 (phi>0); EXTERIOR/medium f>1
(phi<0). Both sectors live (phi(r,theta), angular seeded then free).
ADDED NOTHING, SLAVED NOTHING, FROZE NOTHING. No lepton-wall comparison
(this is exploration, not mass-matching). No interior retreat (the
exterior IS the scan target; the interior appears only as a CONTROL).

---

## Headline

ONE robust, grid-stable, undocumented-in-detail structure was found, and
on honest scoping it turned out to be a GENERIC (both-sided) phenomenon,
NOT an exterior-specific anomaly. The decisive comparison killed the
"exterior is special" reading. Honest verdict: BASELINE LARGELY HOLDS on
the exterior; the one new structure is a properly-scoped REFINEMENT of an
already-banked fact, not a new region.

- **F1 (the find, REAL — graded GENERIC/DOCUMENTED-CLASS).** The
  whole-metric static elliptic system with the ON source has a
  **Gelfand-Bratu-type EXISTENCE FOLD**: a smooth static solution exists
  only below a critical source strength Phi_c; above it NO smooth static
  whole-metric solution exists. On the EXTERIOR (f>1) Phi_c ≈ 0.19-0.20,
  essentially independent of medium depth (Dout from -0.5 to -2.0:
  Phi_c = 0.1994, 0.1980, 0.1911; off-zero inner Din: 0.1982, 0.1905).
  Grid-stable: Phi_c(101x51)=0.2000, (161x81)=0.1980, (241x121)=0.1958
  (drift 0.004 — REAL, not discretization).
- **F1-SCOPE (what kills the anomaly).** The INTERIOR (f<1) CONTROL ALSO
  FOLDS — and EARLIER: Phi_c = 0.011-0.025 (both Dirichlet-Dirichlet and
  the native inner-Neumann closure). So the fold is NOT exterior-specific;
  it is a general property of the ON-source whole-metric elliptic system,
  and the exterior is actually MORE robust to source strength than the
  interior, not less. This is the documented-class fact (B3/exterior_
  cavity already banked "formed depth DIVERGES at a threshold c*" — a
  fold). The exterior medium does NOT change character relative to the
  interior here; both share the same fold structure.
- **F2 (the sourceless exterior — BASELINE HOLDS).** The SOURCELESS
  (Phi=0, vacuum/mirror) exterior closes cleanly to a smooth MONOTONE
  medium at every driving (36/36 solves converged, turns=0, theta-flat
  to ~1e-16 from lobed seeds). This is the medium's one smooth static
  whole-metric solution and it is B6/CANON-consistent (the mirror
  exterior). No angular structure is born in the smooth medium at the
  SEED level (lobed seeds relax to round), matching B2.
- **F3 (angular-gap on the gradient exterior — INCONCLUSIVE, method
  failed).** The intended decisive test (does the #36 "pure damping about
  ROUND" angular gap stay positive on a gradient-CARRYING exterior
  background?) was NOT cleanly answered. The full-Jacobian symmetrized-
  eigenvalue reading is an ARTIFACT (the e^{-2phi}-weighted box is not
  self-adjoint in the naive grid inner product; the symmetrized FD
  Jacobian gives ~18000 spurious negative eigenvalues even on the round
  INTERIOR control that B2 proves is positive). No bankable gap-sign
  result. This question remains OPEN and needs the correct
  measure-weighted self-adjoint form. See "Honest negatives / method
  failures" below.

NET: no genuinely undocumented exterior region was found within the
scanned scope. The one real new structure (the Bratu fold) is both-sided
and documented-class. The medium's smooth static whole-metric solution is
the sourceless monotone mirror; the ON source does not form an additional
smooth static medium above a (boundary-dependent) critical strength.

---

## Method and what was solved

PART A (ext_scan_whole.py, 144 solves). The exterior whole-metric solution
map: solve Box_g phi = S(phi) with both sectors live on the f>1 domain,
driven by inner depth Din (cell-interface side) and outer depth Dout
(universe side); the MEDIUM GRADIENT ~ (Dout-Din)/span is the medium's
intrinsic content (the monopole dilation gradient gamma). Sweep
Din in {0,-0.2,-0.5}, Dout in {-0.2..-2.0}, Phi in {0,0.3,1.0,3.0},
angular seeds l in {0,1,2} amp 0.15. Diagnostics: convergence, radial
turn count, theta-variation, dominant Legendre l, f>1 fraction,
compactness reach, MS aspect.

RESULT (the clean split, /tmp/ext_scan_A.json):
- Phi=0 (sourceless): 36/36 converged, turns=0, theta-flat ~1e-16. The
  smooth monotone mirror medium. Lobed seeds relax to round.
- Phi>0 (ON source): 0/108 converged; multi-turn (2-6) profiles, residual
  O(1)-O(100). FLAGGED as a candidate character change (the ON source
  closes the f<1 interior cell but does NOT close a smooth f>1 medium).

PART (existence, ext_scan_verify.py Q1 + ext_scan_fold.py). Newton failure
is not a no-existence proof, so existence was tested by the robust
homotopy (Phi-continuation: ramp Phi from 0, warm-start each Newton from
the previous converged field) and pseudo-transient continuation. Result:
a weak ON source (Phi=0.1) DOES admit a smooth static exterior medium
(Newton AND Phi-continuation converge to 1e-13); Phi=0.3 does NOT (the
Phi-continuation branch ENDS — not a bad guess). ext_scan_fold.py then
located the fold Phi_c by continuation+bisection across five exterior
media, controlled with the interior (both closures), and checked grid
convergence. (See F1, F1-SCOPE above for numbers.)

PART (angular gap — method failed, F3). Attempted the gradient-background
angular-stiffness sign via the symmetrized Jacobian spectrum (PART B of
ext_scan_whole; sparse interior-block version in ext_scan_verify Q2). The
control failed (positive-by-theorem round interior read ~18000 negative
eigenvalues), exposing the symmetrization as invalid. No result banked.

---

## The map (exterior solution space, scanned scope)

| Region (f>1 medium) | What the whole metric does | Baseline status |
|---|---|---|
| Sourceless (Phi=0), any drive | Smooth MONOTONE medium; turns=0; theta-flat; lobed seeds relax to round | B2/B6 HOLD; the medium's one smooth static solution = the mirror |
| ON source, Phi < Phi_c(~0.19-0.20) | Smooth static medium exists (multi-turn absent at weak Phi) | new detail; within Bratu-fold class |
| ON source, Phi > Phi_c | NO smooth static whole-metric solution (existence fold) | documented-class (B3 "depth diverges at threshold"); REAL, grid-stable, but BOTH-SIDED (interior folds earlier) |
| Angular sector on gradient background | gap sign UNDETERMINED (method artifact) | OPEN — F3 |

---

## Flagged candidate anomalies — each self-graded

**FLAG F1 — exterior ON-source existence fold Phi_c ≈ 0.19-0.20.**
What changed character: above Phi_c the smooth static whole-metric medium
ceases to EXIST (PART A's universal Phi>0 non-convergence is this fold).
Evidence: Phi-continuation branch ends; bisected Phi_c = 0.1905-0.1994
across 5 media; grid-stable (drift 0.004). Self-grade: **REAL but
DOCUMENTED-CLASS / NOT-EXTERIOR-SPECIFIC.** The interior control folds too
(Phi_c 0.011-0.025), so this is a generic Gelfand-Bratu fold of the
ON-source whole-metric elliptic system, already foreshadowed by the banked
"formed depth diverges at threshold" (B3). The exterior is more robust
than the interior, not anomalous. Specific Phi_c is boundary-setup-
dependent (Dirichlet-Dirichlet here; wint_solve2d's inner-Neumann +
outer-Dirichlet trust window converged the interior to Phi=3). NOT a new
region.

**FLAG F3 — angular gap on the gradient exterior: UNRESOLVED.**
What it would have changed: if the angular gap went negative on a
gradient-carrying exterior background, a shaped type the interior damps
away (#34/#36) would be born in the medium — a genuine new region and a
hit on the GOAL (particle types from the boundary/medium). Evidence:
none bankable — the symmetrized FD-Jacobian eigen-reading is an artifact
(control fails). Self-grade: **METHOD FAILURE, OPEN.** This is the single
most worthwhile follow-up and is NOT closed by this push.

---

## Honest negatives / method failures (first-class)

1. The full/symmetrized FD-Jacobian angular-gap reading (ext_scan_whole
   PART B/C/D; ext_scan_verify Q2) is INVALID: the e^{-2phi}-weighted box
   is not self-adjoint in the naive l2 grid inner product; symmetrizing
   and reading eigenvalues yields thousands of spurious negatives even on
   the B2-positive round interior control (n_neg≈18000). PARTS B/C/D of
   ext_scan_whole.py therefore produce NO bankable gap/sign/threshold-
   phase result. The correct object is the second variation in the
   metric's own measure (sqrt|g| sin th e^{-2phi} weighting) cast as a
   genuine self-adjoint generalized eigenproblem — deferred.
2. ext_scan_whole.py PARTS C/D additionally risk OOM (dense eig on up to
   ~42000^2). Superseded by the sparse/continuation approach; not re-run.
3. Pseudo-transient continuation (ext_scan_verify PTC) was numerically
   unstable on this stiff exponential source (blew to 1e+149); the
   informative existence evidence came from Phi-continuation, not PTC.

## Scope / premise set

f>1 exterior, both sectors live, STATIC, single mirrored domain, ON source
S=Phi(e^{-2phi}-e^{phi}) and Phi=0 sourceless; Dirichlet-Dirichlet medium
drive (and inner-Neumann control); axisymmetric even sector; classical
(no hbar); q=1/3, N=3 held; rho=r. The fold Phi_c is boundary-data-
dependent. The angular-gap question is OUT (method failed). NONSTATIONARY,
multi-cell/ensemble, and the corrected self-adjoint angular spectrum are
all UNTOUCHED here and remain the live exterior frontier.

## Verifier note

Built-in artifact control (ext_scan_whole PART D) plus an independent lean
re-derivation (ext_scan_fold.py: different code path, continuation+
bisection, interior control, grid sweep) cross-confirm F1 and expose F3's
method failure. A fully independent blind verifier pass is NOT yet done;
per Self-Hardening this doc is working-audit grade until that pass.
Recommended verifier aim: (a) reproduce Phi_c by an independent arclength
continuation and confirm the both-sided fold; (b) attempt the correct
measure-weighted self-adjoint angular generalized eigenproblem to settle
F3.
