# WCC — The Whole Closed Cell: Interior + Seal Mirror-Fold Closure Solved Together

Date: 2026-06-13. Driver: Claude (Opus 4.8), WHOLE-CLOSED-CELL agent.
Frame: CRITICAL_UNIVERSE_FRAME.md (governing). Scope: purely STRUCTURAL —
no mass-number matching, no clean-integer/generation hunting (registry #35
{3,5,7} rejected; not repeated), no invented sectors. New scripts wcc_*.
Reuses (does NOT edit) the verified wint residual/Jacobian and the
w6/w7a-derived mirror-fold parity closure. Independent blind adversarial
verifier (agent a035deeb280d8bbf9, fully independent machinery): the
central spectral claim CONFIRMED. HYPOTHESIS-GRADE on the topological-
locus reading (D3); the spectral verdict (B) is solid.

## The question (the genuine open edge, never solved before)

The bulk INTERIOR solve (wint, registry #34) proved both sectors live and
two-way, and found the angular sector is PURE DAMPING — every shape
smooths to round, the solver Jacobian non-singular (no bifurcation). But
it closed the OUTER end at a TRUST-WINDOW Neumann turning point; it never
imposed the SEAL mirror-fold parity closure on the live differential
angular field, and never closed TO the seal. W7 imposed the crease BC but
with the angular sector entering ALGEBRAICALLY only (its own scope note).
**Nobody had put the live differential angular field phi(r,theta) TOGETHER
with the mirror-fold parity closure at the seal** — exactly Charles's
prime suspect (phi-angular coupling) meeting the only place structure can
live (the closure). wint_results section (vi) #1 named this the genuine
open edge. WCC solves it.

## (i) THE CLOSED-CELL BVP AS POSED (both sectors live; seal = closure)

Field: v(m,theta), the dressed dilation phi in the flow chart (m,theta).
Interior = the metric's OWN field equation (wint (★), verified two ways in
wint_symcheck; nothing added):

    v_mm + e^{2v}( v_thth + cot(theta) v_th - v_th^2 ) = Phi( e^{-2v} - e^{v} )

with the radial piece = the registry-#33 whole-profile operator, the
angular piece = the metric's own e^{2v}-dressed angular operator carrying
the derived nonlinearity -v_th^2 (the phi-angular coupling, for free), and
the ON two-exponential restoring source (the member that CLOSES a cell,
w_alg PART E). Closures, all DERIVED:

  - inner (center / mirror parity): turning point v_m=0, depth anchor
    v=v_min(E) (the partition energy E is the genuine free datum).
  - axis (sphere regularity): v_th=0 at theta=0,pi.
  - OUTER SEAL = the same-minus MIRROR-FOLD parity closure (w6 + w7a,
    theorem-grade): the seal is the D=0 crease, fixed surface of the
    same-minus involution sigma:(a,b)->(-a,-b); crease normal
    rho = b - f q a is sigma-ODD; the mirror quotient glues cell onto
    mirror across rho=0; PARITY DICHOTOMY:
        sigma-EVEN sector (static shape)       -> NEUMANN  d_m v=0 at seal
        sigma-ODD  sector (f_T-driven amplitude) -> DIRICHLET v=v_seal.
    The seal is handled as a CLOSURE (boundary/parity/matching condition),
    NOT a dynamical march through the singular D=0 crease — the way the
    mirror-fold theorem and the area form already do.

Control branch: bulkN = the wint trust-window Neumann (the bulk closure),
included so the seal closures are compared against the proven baseline.

Area-form / topological closure of the angular sector (the H1 object) is
included as PART D (the cohomological datum, distinct from the dynamical
spectrum — see below).

## (ii) THE SOLUTION SPACE FOUND

The round (theta-independent) cell is a self-consistent fixed point under
ALL THREE outer closures — bulk-Neumann, mirror-fold EVEN (Neumann),
mirror-fold ODD (Dirichlet) — converging to maxres ~1e-11 with machine-
zero angular variation (th_var ~1e-15) at every partition energy E.
(wcc_closed_cell PART A, 3/3 PASS.) The free datum is E; the cell is the
same smooth one-parameter round family as wint, now closed at the seal.

## (iii) THE STRUCTURES THE CLOSED OBJECT SUPPORTS — the deliverable

### THE SHARP QUESTION ANSWERED: the seal closure supports NO angular
### structure that the bulk damps. The closed cell is STILL one round type.

The decisive test (wcc_seal_spectrum, the trustworthy self-adjoint
diagnostic; the first-pass raw-Jacobian sign reading in wcc_closed_cell
PART B is SUPERSEDED and labeled so): linearize the full 2D field equation
about the converged round cell, take the SYMMETRIC part of the solver
Jacobian Js=(J+J^T)/2 (real spectrum), and restrict to ANGULAR
(theta-varying) eigenvectors. The smallest |eigenvalue| among angular
modes — the angular bifurcation gap — is:

    branch   min angular gap over E    any angular eig negative?
    bulkN    0.648                     NO
    even     0.648                     NO
    odd      0.648                     NO

POSITIVE and BOUNDED AWAY FROM ZERO in every closure, across
E/Umin in {1.3,2,3,4,6,9}, grid-refinement-stable (gap ~0.85 at E=2
stable 61->111 in m), and stable to the horizon: at deep compactness
X->0.99 (E/Umin=9) the gap stays ~0.52 (the blind verifier pushed to
X=0.99999 and found the gap GROWS, not collapses). NO angular eigenvalue
goes negative under ANY seal closure, including the adversarially-targeted
odd-Dirichlet seal. The odd seal shifts the gap by <0.001 (it slightly
STIFFENS) — it does NOT soften any angular mode.

The nonlinear confirmation (wcc_seal_spectrum PART C): every lobed seed
(Legendre l=1,2,3, gentle amplitude ramp 0.05->0.20) under every seal
either relaxes to round or fails to converge; ZERO genuinely persistent
shaped closed cells survive convergence + grid refinement. The 6 odd-
branch "stuck shapes" are pure Newton non-convergences (the Dirichlet seal
fighting a large lobe), NOT persistent structure — settled by the
persistence test.

### THE ALGEBRAIC ROOT (exact, wcc_topology_at_crease D1)

The metric's angular nonlinearity -v_th^2 linearizes to EXACTLY ZERO about
the theta-flat round background (its variation = -2 v0_th u_th = 0 since
v0_th=0). So the closed cell's dynamical angular operator is the PURE
DRESSED LAPLACIAN e^{2v0}(u_thth + cot th u_th), eigenvalue -l(l+1) times
a STRICTLY POSITIVE radial weight — pure damping at every harmonic l, by
construction. This is WHY the seal-closed spectrum is round-only: the
closure cannot soften a sector whose linear operator is sign-definite
damping. (Blind verifier confirmed independently and analytically.)

### THE TOPOLOGY THE CLOSURE DOES HOLD (distinct object; D2/D3)

The one native discreteness the program HAS (q=1/3, N=3 from the H1 AREA
FORM) is NOT a dynamical mode and was never expected in this spectrum. It
is a COHOMOLOGICAL / boundary-transgression object, and WCC PART D pins
down WHERE it lives in the closed-cell structure (exact sympy, 6/6 PASS):

  - D2: omega_H1 = sin th dth dph is the S2 area form; INT omega_H1 = 4pi
    is a TOPOLOGICAL invariant (the fundamental class), not a dynamical
    amplitude. The area-form datum d ln f ^ omega_H1 = d[(ln f) omega_H1]
    is EXACT — a total derivative, a pure BOUNDARY/closure term. The bulk
    EL is blind to a total derivative, so this datum is delivered at the
    SEAL/closure, not in the bulk dynamics.
  - D3: the transgression (ln f) omega_H1 is RADIAL x ANGULAR; omega_H1 is
    sigma-invariant (sigma touches only the time row), the radial factor
    reverses orientation across the mirror crease, so the transgression is
    sigma-ODD -> carried by the DIRICHLET (odd) branch — the SAME parity
    branch the dynamical test found inert.

So the two findings are CONSISTENT and complementary: the closed cell
supports exactly ONE round DYNAMICAL type AND a topological 2-form datum
(the area-form q/N), in DIFFERENT objects (spectrum vs cohomology). The
closure that holds no dynamical angular mode HOLDS the topological 2-form,
in its odd parity sector. The structure of the closed object is: a
round dynamical body, sealed by a mirror fold whose odd-parity closure
carries a topological (not dynamical) 2-form datum.

## (iv) SOLID vs HYPOTHESIS-GRADE

SOLID (computed here + blind-verified independently):
  - the closed-cell BVP poses and the round cell closes under all three
    outer closures (PART A);
  - NO soft/negative angular dynamical mode under any seal closure;
    closed cell = one round type; grid- and horizon-robust (PART B,
    blind-verified with independent Legendre-harmonic + from-scratch 2D
    machinery);
  - the -v_th^2 linearizes to 0 about the round background (D1, exact);
  - the area form is a closed/exact boundary transgression with INT=4pi
    (D2, exact).
HYPOTHESIS-GRADE (needs Charles + a dedicated topology verifier):
  - the parity assignment of the transgression to the odd/Dirichlet sector
    (D3) — the orientation-reversal argument is a geometric reading, not a
    full junction-condition computation.
NOT re-derived / NOT promoted: the two-form lock C(N^2,2)=4N^2 -> N=3,
q=1/3 is re-STATED only to locate where it lives; the {3,5,7} generation
reading stays rejected (#35).

## (v) WHAT A BLIND VERIFIER SHOULD ATTACK FIRST (next pass)

1. The D3 parity-locus claim (the topological 2-form sits in the
   odd/Dirichlet crease sector) — replace the orientation-reversal reading
   with the actual same-minus junction/matching condition across D=0; does
   the area-form transgression genuinely glue antisymmetrically?
2. The dynamical-spectrum scope: WCC tests LINEAR stability of the round
   cell. A nonlinear bifurcation that is not visible as a zero linear mode
   (a fold/transcritical born at finite amplitude) is not excluded by the
   gap test — though PART C's seed continuation found none. Attack with an
   arc-length continuation in a deliberate symmetry-breaking parameter.
3. The premise that the matter source is the ON two-exponential (w_alg
   PART E) — the standing load-bearing premise of the whole closed cell.

## (vi) SCRIPTS / COUNTS

- wcc_closed_cell.py — the closed-cell BVP + residual/Newton with the
  seal-branch parity closure (PART A 3/3 PASS; PART B/C measurements,
  PART B sign-reading SUPERSEDED, labeled). Log /tmp/wcc_closed_cell.log,
  checkpoint /tmp/wcc_closed_cell.json.
- wcc_seal_spectrum.py — the TRUSTWORTHY self-adjoint angular bifurcation
  gap per seal branch + nonlinear persistence test (2/2 PASS; the verdict
  of record). Log /tmp/wcc_seal_spectrum.log, checkpoint
  /tmp/wcc_seal_spectrum.json.
- wcc_topology_at_crease.py — exact sympy: D1 (-v_th^2 linearizes to 0),
  D2 (area form is a closed/exact boundary transgression, INT=4pi), D3
  (topological 2-form in the odd/Dirichlet sector). 6/6 PASS. Log
  /tmp/wcc_topology_at_crease.log.
- Blind verifier agent a035deeb280d8bbf9 (independent machinery):
  CONFIRMED the spectral claim; flagged the WCC PART B "angular gap" as
  conservatively BC-block-contaminated (the genuine interior dynamical gap
  is LARGER, ~7-23) — the verdict (no soft/negative mode) holds either way.

## Registry note (proposed)

A new negative, premise-scoped: THE SEAL MIRROR-FOLD CLOSURE DOES NOT
SUPPORT A DYNAMICAL ANGULAR MODE THE BULK DAMPS — the whole closed cell
(interior + seal parity closure, both sectors live and two-way) supports
ONE round dynamical type; the angular operator is sign-definite damping at
linear order under all three closures (Neumann/even/Dirichlet/odd),
grid- and horizon-robust, blind-verified. PREMISES: ON two-exponential
source (w_alg PART E); flow-chart Neumann center / parity seal closure;
linear stability about the round cell (nonlinear continuation found no
shaped fixed point but is not a theorem). This CLOSES the wint sec-(vi)-#1
open edge in the NEGATIVE for the dynamical sector. It does NOT touch the
topological/cohomological angular discreteness (q=1/3, N=3 from the H1
area form), which lives in a different object (an exact boundary
transgression at the closure, D2/D3) — that discreteness is unaffected and
remains the program's one native discreteness.
