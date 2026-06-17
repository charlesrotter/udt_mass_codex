# Phase 3b — Platonic winding ground states: shapes + stability — 2026-06-17

**Push:** Phase 3b (characterize the classical winding catalog before looking for its
"spectrum"). Charles steer: finish the classical catalog first. OBSERVE, DATA-BLIND
(units L=sqrt(kappa/xi)=1; no wall numbers). Category-A only. Driver: Claude (Opus 4.8, 1M).
**Scripts (committed):** phase3b_platonic_solve.py (Step 1 checkpoints), phase3b_symmetry.py
(Step 4, SH power spectrum + self-test), phase3b_hessian.py (Step 5a fixed-metric Hessian),
phase3b_descend.py (Step 5b decisive coupled stability test), phase3b_grid_converge.py (Step 2/3).
**Builds on:** off_round_solver_results.md (the Newton solver), winding_catalog_verified_results.md
(the catalog exists; m>=2 round is unstable).

## HEADLINE (regime-stamped; masses INTERIM at 18x8x8)
The UDT winding ground states are: m=1 ROUND (stable), m=2 TOROIDAL/axial (stable), m=3 AXIAL
(stable). The round->axial symmetry breaking for m>=2 MATCHES the Skyrme/large-N-QCD B=2 torus;
but m=3 is AXIAL, NOT the tetrahedral Skyrme B=3 — UDT OVERLAPS Skyrme at B=2 and DIVERGES at
B=3, plausibly because the strong gravitational self-binding (super-linear mass, absent in flat
Skyrme) reshapes the energetics toward axial shapes. All three are coupled-stable along the
steepest tested modes. Masses (18x8x8): m=1 ~0.299, m=2 ~13.40, m=3 ~143.0.

## EVIDENCE
### Checkpoints (Step 1; SH-exact grid 18x8x8, p=0.4, kap8=0.05)
| m | M_MS | psivar | winning seed | maxB1A (B=1/A free) | indep residual (max) |
|---|------|--------|--------------|---------------------|----------------------|
| 1 | 0.29926 | 2.9e-3 | base (round) | 0.192 | 2.5e-7 |
| 2 | 13.4045 | 0.297  | base         | 2.795 | 4.9e-5 |
| 3 | 142.989 | 0.358  | cos3psi@0.3  | 5.408 | 2.5e-5 |
All category-A (B=1/A free, large maxB1A); residual at the grid floor (~1e-5 at 18x8x8);
independent component_residuals path agrees.

### Symmetry (Step 4; SH power spectrum P(l)=sum_m|c_lm|^2, rotation-invariant; self-test PASSED)
SELF-TEST: synthetic pure-l fields peak at the correct l; cos(3psi) -> A(|m|=3). Machinery trusted.
| m | P(l)/P(0), l=0..4 | leading l | verdict |
|---|-------------------|-----------|---------|
| 1 | [1, 0, 5e-4, 0, 4e-4] | none | SPHERICAL (control PASS) |
| 2 | [1, 0, 0.274, 0, 0.208] | l=2 (even ladder, no l=3) | AXIAL / TOROIDAL |
| 3 | [1, 3e-4, 0.760, 2.5e-3, 0.330] | l=2 (even, l=3≈0) | AXIAL (NOT tetrahedral) |
m=2 = torus (Skyrme B=2 analog). m=3 = axial; the tetrahedral l=3 signature (within resolution,
Lmax=4) is ABSENT (0.0025) => m=3 is NOT tetrahedral at this grid/seed.

### Stability — the key methodological catch (Step 5a + 5b)
Step 5a (FULL-BODY matter Hessian at FIXED metric): m=1 n_neg=0 (calibration PASS — the round
hedgehog is a genuine minimum, sign convention valid); m=2 n_neg=19; m=3 n_neg=44.
*** But the fixed-metric matter Hessian is NOT the physical stability operator for a GRAVITATING
soliton: perturbing Theta at fixed metric moves OFF the Einstein constraint surface, so its
"negative modes" can be unphysical off-constraint directions. ***
Step 5b (DECISIVE, constraint-respecting): perturb along the steepest fixed-metric negative
eigenvectors, then FULL COUPLED re-solve (re-imposes Einstein + matter EL):
| m | base M | top neg evals | coupled re-solve result |
|---|--------|---------------|--------------------------|
| 2 | 13.4045 | -302, -183 | ALL go UPHILL (M -> 14.5, 16.9, 16.3) |
| 3 | 142.989 | -908, -884 | ALL go UPHILL (M -> 148.2) |
=> the fixed-metric negatives were OFF-CONSTRAINT; both states are COUPLED-STABLE along the
steepest tested modes. The round->axial states are genuine ground states, not saddles.

## MASS / BINDING (interim)
Progression 0.299 -> 13.40 -> 143.0: strongly SUPER-LINEAR but DECELERATING (x44.8 then x10.7).
M(m) >> m*M(1) (2*0.299=0.60 << 13.40; 3*0.299=0.90 << 143) => the winding solitons are
gravitationally ANTI-BOUND (self-energy dominated) — OPPOSITE to nuclear binding. This is a
kap8-dependent (back-reaction) statement; kap8=0.05 here. [Grid-convergence of M_MS(2) + binding
running at submission; numbers to be appended.]

## METHODOLOGICAL LESSON (carry forward)
For a GRAVITATING (constrained) soliton, the fixed-metric matter Hessian OVER-COUNTS instabilities
(off-constraint directions). The physical stability test is the CONSTRAINT-RESPECTING one: perturb
+ FULL COUPLED re-solve (or the reduced/Schur Hessian on the constraint surface). Here it flipped
the reading from "saddle (n_neg=19,44)" to "coupled-stable." Banked as a reusable discipline.

## COMPLETENESS-MAP IMPACT
- crit-6 (topological sectors m=1,2,3): distinct, converged. crit-8 (catalog): EXISTS; within each
  m>=2 a round->axial bifurcation; the ground states are axial (m=2 toroidal, m=3 axial).
- crit-9 (stability): m=1 stable minimum (matter Hessian n_neg=0); m=2,3 coupled-stable along the
  steepest modes (off-constraint negatives ruled out by coupled re-solve). NOT a full stability
  proof (only top-2 of 19/44 modes tested; reduced coupled Hessian not computed).
- DROPPED / caveats: masses interim (one grid; grid-conv pending); resolution Lmax=4, m<=4 (m=3
  not-tetrahedral is within resolution but a dedicated finer tetrahedral search would strengthen
  it); only steepest stability modes tested; matter-sector (not full coupled) Hessian.

## STANDING-QUESTION ANSWERS
1. COVERS: shapes (symmetry) + coupled stability of the m=1,2,3 winding ground states. DROPS:
   grid-converged masses, full stability spectrum, finer-resolution platonic search, off-diagonal
   metric / full S^3 matter.
2. Dropped hosting structure? The m=3 tetrahedral question is resolution/seed-limited — a finer
   dedicated search could still find a lower tetrahedral state (flagged, not closed).
3. REGIME: p=0.4, kap8=0.05, grid 18x8x8 (Lmax=4); masses interim.
4. Category-A? YES (B=1/A free maxB1A 0.19-5.4; SH-exact grid; no tie/inject/tune; data-blind).
5. Tooling next: finer-grid platonic search (Nps>=12) for the m=3 tetrahedral question + a proper
   minimizer/reduced-coupled-Hessian for full stability; grid convergence (running).
6. ONE tile: shapes+coupled-stability of m<=3 winding ground states. Blank: grid-converged masses,
   full spectrum, higher m, the eigenvalue/standing-wave "spectrum" layer (the agreed next thrust).

## PROVENANCE
Step1 phase3b_step1_out.json; symmetry phase3b_symmetry_out.json (self-test PASS);
hessian phase3b_hessian_out.json; descent phase3b_descend_m2/m3_out.json. Checkpoints
u_plat_m{1,2,3}_18x8x8.pt. All this session (2026-06-16/17), driver-run, foreground solves.
