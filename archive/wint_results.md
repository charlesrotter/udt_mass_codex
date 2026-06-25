# WINT — The Two-Way Interacting Whole: What Structures Form

Date: 2026-06-13. Driver: Claude (Opus 4.8), INTERACTING-WHOLE agent.
Frame: CRITICAL_UNIVERSE_FRAME.md (governing). Pre-registration:
wint_preregister.md (committed before any run). Declaration: METRIC-LED
("what structures does the two-way interacting metric+matter produce?").
HYPOTHESIS-GRADE. Blind adversarial verifier: agent ab889812658d33162
(independent machinery) — CONFIRMED-WITH-AMENDMENTS; both amendments
folded in and re-run clean before this record.

## Charles's order (verbatim register, not re-framed)

"Compute the solution space of the WHOLE metric and analyse what
structures form." "The geometry more likely forces the TYPES of lumps."
It is NOT the metric on a FIXED matter background — it is "how the metric
and matter INTERACT" (two-way, self-consistent). Solve and LOOK; impose
nothing. FORBIDDEN this push (the prior driver kept doing them):
determinacy/counting; imposing discreteness (integer tiling, mode
spectrum, eigenvalue ladder); freezing a background; adding terms
(W_wave/stiffness/D_cell/kappa); slaving the angular sector.

## (i) THE INTERACTING SYSTEM (exact; derived; nothing added)

The metric is primary and generates the dilation field (frame):
   ds^2 = -e^{-2phi}c^2 dt^2 + e^{+2phi}dr^2 + r^2 dOmega^2,  phi=phi(r,theta).
BOTH sectors live: phi is a genuine 2D field (angular NOT slaved). The
metric's OWN field equation is the C1 dilation-action EL (verified
exactly two ways in wint_symcheck.py, and independently re-derived from
scratch by the blind verifier):

   r^2 e^{-2phi}( phi_rr + (2/r) phi_r - 2 phi_r^2 )
     + ( phi_thth + cot(theta) phi_th - phi_th^2 )  =  S_matter.   (★)

  - RADIAL piece = EXACTLY the banked registry-#33 whole-profile operator.
  - ANGULAR piece = the metric's own e^{2phi}/r^2-DRESSED angular operator
    ( phi_thth + cot th phi_th - phi_th^2 ). The e^{2phi} dressing AND the
    angular nonlinearity -phi_th^2 are BOTH carried by the metric with
    NOTHING added — the phi-angular coupling (Charles's standing hunch's
    prime suspect) appears for free. (wint_symcheck.py: 3/3 PASS; verifier
    re-derived EL = (-4 e^{-2phi} sin th)·[(★)-bracket], exact.)

The matter is the metric's OWN derived ON restoring source (w_alg PART E /
w_whole_gm PART D — the two-exponential well that CLOSES a cell; the
OFF/vacuum monotone source provably cannot close, w_whole_gm PART C):
   S_matter:  in the radial flow chart  v_mm = Phi(e^{-2v} - e^{v}),
   first integral (1/2)v_m^2 + (Phi/2)e^{-2v} + Phi e^{v} = E,  well
   bottom U_min = 3Phi/2 at v=0 (the same-minus seal locus). TAKEN, not
   invented. (Phi->0 recovers the bare metric EOM, registry #33.)

THE TWO-WAY BACK-REACTION LOOP (neither frozen): the e^{-2phi}/e^{phi}
weights AND the angular dressing are evaluated on the CURRENT field at
every Newton step; the matter source reshapes the metric and the metric's
dressed operator reshapes the matter; iterate to mutual self-consistency.
The Misner-Sharp/dilation tie reads the matter off the SAME field:
   m(r) = (c^2 r/2G)(1 - e^{-2 <phi>_theta(r)}).
The genuine FREE DATUM is the partition energy E (audited PHYSICAL,
w_whole_gm step 3) and the source scale Phi; absolute size is scale-free
(Axis-1 theorem, registry #32), so structures are classified by
SCALE-FREE invariants (shape, angular class, compactness X, MS aspect).

## (ii) THE SOLUTION-SPACE EXPLORATION (what converged, on what scope)

Method: the cell is solved in the FLOW CHART (m, theta) where it actually
closes — NEUMANN-NEUMANN radial closure (the two turning points v_m=0 =
inner center regularity / mirror parity + outer CR-87 Neumann), axis
Neumann in theta (sphere regularity), the center depth = v_min(E) as the
sole energy anchor (NOT an imposed shape). Damped-Newton + Armijo line
search, scipy sparse (the explicit relaxation is unstable on the
Bratu/Liouville-type stiffness — standard). Scope: the interior/trust
window of the cell (the full domain to the seal f->0 collapses, known
fact, NOT a reason to freeze a background).

Converged: 20/20 2D interacting solves to maxres ~1e-12 (Newton 3-6
iters). Sweep: partition energy E/U_min in {1.1,1.3,1.6,2.0,3.0,4.0,6.0,
9.0}; seeds round AND Legendre-lobed l={1,2,3,4} with amplitudes up to
1.0; grid refinement 97x33 -> 193x73. Cross-engine: the converged radial
family reproduces the banked anchor L(E=3,Phi=1)=1.674279381 to 1e-11
(quadrature) and to ~7e-4 (independent RK4 IVP, verifier).

## (iii) THE STRUCTURES / TYPES THAT FORM — the deliverable

Pre-registered operational definition (wint_preregister.md): a STRUCTURE =
a converged self-consistent (two-way fixed point) cell, maxres < 1e-9,
that PERSISTS under grid refinement AND small perturbation. Outcomes
declared in advance: O1 one type / O2 a smooth family of one type / O3
several distinct types / O4 nothing stable.

VERDICT: **O2 — A SMOOTH FAMILY OF ONE TYPE.** The interacting
metric+matter forms exactly ONE kind of stable lump: a ROUND
(theta-independent) cell, a smooth one-parameter family in the partition
energy E. Two independent lines establish it:

1. PERSISTENCE (the seed sweep): EVERY angular seed — Legendre lobes
   l=1,2,3,4, amplitudes 0.2 to 1.0 — RELAXES BACK TO ROUND. Converged
   angular variation th_var ~ 1e-13 to 1e-16 (machine-zero), dominant
   angular harmonic dom_l = 0, at every E. Grid-refinement persistent
   (97->193: th_var stays ~1e-15; X stable to ~1e-5). The angular sector
   is fully live and carries the derived nonlinearity -phi_th^2, yet
   supports NO shaped attractor.

2. EXISTENCE (the decisive argument, from the blind verifier): the
   solver Jacobian about the round cell is NON-SINGULAR across the WHOLE
   E-family — min|eig| grows monotonically 0.0153 (E=1.1 U_min) ->
   0.145 (E=6 U_min), never approaching zero. NO bifurcation point, NO
   zero mode anywhere -> NO distinct shaped self-consistent type can be
   born. This rules out shaped types the seed sweep never reached; it is
   the proper existence proof of "one type."

CHARACTER OF THE ONE TYPE (scale-free invariants of the round-cell
family; the deliverable's quantitative content):

   E/U_min   L(width)   X=1-e^{-2 vmax}   vmax       MS-aspect
   1.10      1.79873    0.483871          0.33070    -0.04024
   1.30      1.76910    0.689573          0.58490    -0.12290
   1.60      1.72659    0.811957          0.83554    -0.24061
   2.00      1.67428    0.884499          1.07924    -0.38561
   3.00      1.56435    0.950076          1.49863    -0.69999
   4.00      1.47777    0.972101          1.78958    -0.96515
   6.00      1.34913    0.987642          2.19674    -1.40398
   9.00      1.21836    0.994514          2.60273    -1.92906

The compactness X and depth grow with E toward the horizon value X->1
(the seal); the cell width L shrinks. ONE smooth type, no internal
class distinction, parameterized by the conserved partition energy E.

WHY ROUND, physically (honest reading, not invented): the metric's own
angular operator carries NO bulk angular SOURCE — only the dressed
Laplacian + the -phi_th^2 self-term, both of which DAMP smooth angular
structure to the constant. The one native angular discreteness this
program has (q=1/3, eta=1/18, N=3) came from the H1 AREA FORM — a
TOPOLOGICAL/boundary structure at the seal, NOT a bulk dynamical mode. A
bulk two-way interior solve therefore correctly finds no shaped bulk
type; if angular TYPES exist they live in the boundary/topological sector
the interior trust-window solve does not reach. This is consistent with
(does not contradict) the area-form discreteness — they are different
sectors.

## (iv) RATIOS + DATA-BLIND WALL NOTE

The structures form a CONTINUUM (one type, smooth in E), NOT a discrete
set of distinct types. There are therefore NO distinct-type Misner-Sharp
mass RATIOS to report: a continuum has no preferred points, so no
data-blind ratio comparison is defined at this closure level. (This is
the same honest outcome as registry #33: the single-cell interacting
closure RELATES the invariants to E but does not pin a discrete catalog.)
The wall numbers (C_M1=0.977679087638, C_E1=1.93121474779,
ratio=1.97530536575) are noted here ONLY to record that NO comparison was
made and NO tuning occurred — there is no discrete structure to compare.

## (v) SCRIPTS + COUNTS + CONVERGENCE

- wint_preregister.md — pre-registration (committed before runs).
- wint_symcheck.py — sympy, exact: the field equation (★) IS the metric's
  own C1 dilation-action EL (radial = registry #33; angular dressed
  Laplacian + derived -phi_th^2). 3/3 PASS. (Replaces the slow/over-strict
  check 1a in the earlier-instance wint_system.py, left append-only.)
- wint_cell2d.py — the two-way interacting solve: radial cell family
  (PART A: L(E) anchor reproduced), live-angular 2D solve (PART B: 20/20
  converged, every lobe relaxes to round), grid-refinement persistence
  (REFINE PASS), the Jacobian-spectrum EXISTENCE test (PART C: EXIST
  PASS). 6/6 PASS total. Logs /tmp/wint_cell2d.log, /tmp/wint_symcheck —
  checkpoint /tmp/wint_cell2d.json.
- wint_solve2d.py — an earlier (r,theta)-direct torch attempt; superseded
  by wint_cell2d.py (the from-scratch 2D Dirichlet relaxation is unstable
  on the stiff e^{phi} reaction; the flow-chart Newton converges). Kept
  for provenance; its laplace_box is reused as the torch cross-check
  engine. NOT the result of record.

Convergence evidence: Newton maxres ~1e-12; grid refinement 97/129/193
(th_var stays machine-zero, X stable to ~1e-5); cross-method radial L(E)
quadrature vs RK4; independent verifier residual evaluator reproduced
maxres exactly; Jacobian min|eig| monotone and bounded away from 0.

## (vi) WHAT A BLIND VERIFIER SHOULD ATTACK FIRST (next pass)

1. The "round is the only type" conclusion is a BULK-INTERIOR statement.
   The load-bearing physical premise is "the metric carries no bulk
   angular source" — attack whether the area-form/topological angular
   structure (q,N) re-enters as a BOUNDARY condition at the seal that the
   interior trust-window solve cannot see, and whether closing to the
   seal (not just the trust window) changes the type count. This is the
   genuine open edge: bulk = one round type; the angular discreteness is
   topological/boundary, untested here.
2. The matter source is TAKEN as the ON two-exponential (w_alg PART E
   premise). Attack whether the metric's own field content SELECTS the ON
   (restoring) branch for the whole closed universe vs the OFF vacuum
   (the load-bearing step of registry #33).
3. The continuum (one type per E) is the same outcome as #33; attack
   whether any derived closure pins E to a discrete set (none found here;
   none added).

## Registry / discipline

- This push is METRIC-LED, HYPOTHESIS-GRADE, blind-verified
  (ab889812658d33162, CONFIRMED-WITH-AMENDMENTS, amendments folded in).
- Premise set: ON two-exponential source (w_alg PART E); flow-chart
  Neumann-Neumann closure; interior/trust-window scope (not to the seal);
  bulk dynamical angular sector (topological/boundary angular structure
  NOT included). Negative-scoped per the registry culture.
- Nothing canonical without Charles. Data-blind held (no wall comparison;
  no discrete structure to compare).
