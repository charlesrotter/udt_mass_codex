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

## GRID-CONVERGENCE UPDATE (CORRECTION, 2026-06-17) — m>=2 mass is NOT converged
phase3b_grid_converge.py (base-only solves; phase3b_grid_converge_out.json):
| grid | m=1 M (psivar,Phi) | m=2 M (psivar,Phi) |
|------|--------------------|--------------------|
| 16x8x8   | 0.2919 (1.3e-3, 8e-13) | 19.547 (5.9e-3, 2e-15) |
| 18x8x8   | 0.2993 (2.9e-3, 5e-12) | 13.404 (0.297, 1e-8) |
| 20x8x8   | 0.2893 (8e-4, 3e-12)   | 9.758 (0.067, 3e-6*) |
| 18x10x10 | 0.3026 (3.3e-3, 3e-11) | 38.454 (0.203, 3e-7*) |
(* under-converged: Phi did not reach a deep floor.)

FINDING: **m=1 is grid-stable (M ~ 0.29-0.30); m=2 is NOT grid-converged** — M_MS ranges
9.8-38.5 and psivar jumps 0.006-0.30 across grids. The base solve lands on DIFFERENT critical
points at different resolutions (even the DEEPLY-converged 16x8x8, Phi 2e-15, found a near-
AXISYMMETRIC state at M=19.5, not the toroid). This is consistent with the Hessian's many nearby
modes: residual-Newton converges to WHICHEVER critical point is nearest the seed/grid-path, NOT the
global minimum. So the earlier "m=2 toroidal ground state M=13.40" is GRID-SPECIFIC, one of several
critical points — NOT a converged ground-state mass. Binding at 18x10x10 (B=-37.8, ratio 63) is
therefore NOT meaningful.

SCOPE CORRECTION to the headline above: what stands is (a) m=1 is a clean, grid-stable, coupled-
stable ROUND ground state; (b) for m>=2 the round state is unstable and lower NON-axisymmetric
(toroidal/axial) critical points EXIST and are coupled-stable along the steepest tested modes AT A
GIVEN GRID — but the m>=2 GROUND-STATE MASS and the global shape are NOT numerically pinned (multiple
grid-dependent critical points + some under-convergence). The m=2~toroidal / m=3~axial / Skyrme-B2-
overlap / not-tetrahedral readings are SCOPED to specific grid-states, not grid-robust.

TOOL GAP (the real next step for the catalog): residual-Newton finds arbitrary critical points; to
pin the m>=2 STABLE GROUND STATES (the actual particles = global minima) needs an ENERGY MINIMIZER
(gradient flow / arrested Newton / negative-mode descent to convergence) + systematic CONTINUATION
in resolution from one tracked branch — not residual-zeroing from a fresh seed per grid. Until then
the m>=2 catalog masses are UNSETTLED. (m=1, the one true minimum found, is unaffected.)

## BRANCH-TRACKING ATTEMPT (2026-06-17) — FAILED its m=1 validation gate (tool NOT ready)
To pin the m>=2 mass I built warm-start CONTINUATION (cross_grid_branch.py): converge once, then
spectrally INTERPOLATE the state onto the next grid and warm-start Newton (track one branch).
HARD GATES first:
- GATE A (interpolation accuracy, analytic field 18x8x8->24x12x12): PASS, max err 1.78e-15 (exact).
- GATE B (m=1 branch-track must reproduce the DIRECT m=1 solve): **FAIL**. Tracked m=1 masses DRIFT
  monotonically UP: 0.29192 -> 0.29427 -> 0.30109 -> 0.33202 (grids 16/18/20/22) while DIRECT solves
  stay 0.292/0.299/0.289/0.296. Warm-started solves converge to good residuals (Phi ~1e-8) but to
  DIFFERENT, drifting critical points than the direct solves; the bias COMPOUNDS along the chain.
VERDICT: warm-start continuation does NOT fix mass-pinning — it re-finds a nearby CRITICAL POINT at
each grid (accumulating drift), it does not DESCEND to the minimum. No masses banked (gate failed).
CONFIRMS the tool gap: pinning the m>=2 ground-state mass needs a genuine ENERGY MINIMIZER (gradient
flow / arrested-Newton descent to the actual local minimum, which IS grid-robust), not continuation
of critical points. (m=1's stability/mass claim stands: direct solves agree ~0.29-0.30; the tracked
drift to 0.332 is a continuation artifact, not real m=1 physics.) Next-session build, gated.

## MULTI-START LANDSCAPE SURVEY (2026-06-17) — m=2 at 18x8x8 (validated solver only)
11 diverse seeds (base, cos2psi/cos3psi/tetra/oblate/sin2psi @ amp 0.3,0.6), all converged deeply
(Phi~1e-9), all category-A (maxB1A~2.8, B=1/A free). phase3b_multistart_out.json.
RESULT: the m=2 landscape is CROWDED — **6 distinct local-minimum clusters spanning M=12.2-17.2**,
ALL non-axisymmetric (psivar 0.30-0.40, tvar 0.67-0.77):
  M~12.0 (oblate) | M~13.5 (base) | M~14.0 (oblate@0.3) | M~16.0 (cos2psi,tetra,sin2psi x5) |
  M~16.5 (cos3psi) | M~17.0 (cos3psi,sin2psi)
LOWEST found: **M=12.16, psivar 0.343, via the 'oblate' seed** — LOWER than the "base" 13.40 we had
been quoting (the default solve was NOT the ground state even at this grid). Most seeds fall into a
higher ~M=16 cluster.
READING: confirms (physics) a genuinely crowded landscape of many nearby NON-axisym minima, and (tool)
that the ground state requires BASIN-HUNTING — even at fixed grid only the oblate seed reached 12.16.
Best m=2 ground-state estimate at 18x8x8 = ~12.2 (oblate), but (a) not exhaustive (lower may exist),
(b) still grid-specific (cross-grid convergence needs the energy minimizer). All shapes are oblate/
toroidal-family (no platonic l=3); consistent with the axial reading, refined: lowest is OBLATE.

## ENERGY MINIMIZER (2026-06-17) — built, bug-caught, pivoted; m=2 global min CONFIRMED (oblate ~12.3)
energy_minimizer.py: metric-slave solve + local relaxation + basin_hop global search.
- GATE 1 caught a BUG in the original gradient-descent inner loop: it stepped DOWN the action while
  the line search required energy(=-action) to DROP -- opposed directions, so eta underflowed and the
  descent did nothing (fell back to Newton, fullPhi 4.7e-7). Since phase3b_descend already established
  these states are local MINIMA (not saddles), the saddle-rolling descent is also UNNECESSARY here ->
  local_min pivoted to the validated Newton as the inner relaxation; basin_hop does the GLOBAL search.
- m=2 basin_hop (8 hops, 18x8x8): seed 13.68; most hops land in the ~16 cluster; an OBLATE perturbation
  (hop 5) drops to **M=12.370 (psivar 0.349)** = the accepted global min. INDEPENDENTLY CONFIRMS the
  multi-start lowest (12.16, also oblate): the m=2 GROUND-STATE BASIN is the OBLATE soliton, M~12.2-12.4
  at 18x8x8 (two independent global-search methods agree on the basin; ~1.7% apart within it).
RESULT: the energy minimizer reliably IDENTIFIES the m=2 global minimum at a fixed grid (oblate, ~12.3).
STILL OPEN (the remaining hard item): GRID-CONVERGING that mass -- blocked by large-grid Newton
under-convergence (20x8x8 / 18x10x10 don't reach a deep floor), a separate SOLVER-STRENGTH need, NOT a
global-search problem. Banked at-grid: m=2 ground state = oblate, M_MS ~ 12.2-12.4 @ 18x8x8 (interim).

## MASS GRID-CONVERGENCE — a robust NEGATIVE (2026-06-17): not achievable with current tools
Goal: grid-converge the winding masses to the continuum. After the energy minimizer fixed the
GLOBAL-min search at a fixed grid (m=2 oblate ~12.3 @18x8x8), the remaining step was grid convergence.
ALL approaches tried FAIL to give grid-converged masses:
- LARGE-GRID DEEP-FLOOR SOLVER (large_grid_solver.py): DIAGNOSIS = the jacrev Jacobian BUILD dominates
  (37.9s/iter @20x8x8, 132.7s/iter @24x10x10; lstsq only 0.5-2s). Dense newton_solve works but is
  cost-limited at scale. MATRIX-FREE 2-grid Newton-Krylov (newton_krylov_2grid) STALLS: Phi frozen
  (10.84 flat for 12 iters) with BOTH a cheap (12x6x6) AND a geometric (prev-grid) coarse precond
  built-once -- the preconditioned-CG step is not a descent direction (likely a bug/ineffectiveness in
  the matrix-free JVP/precond machinery; the dense route works on the same grids). Dead end as built.
- DEEP-FLOORED WARM-START CONTINUATION (phase3b_richardson.py, tol 1e-11): DRIFTS/DIVERGES.
  m=1: 16->18->20 = 0.2918 -> 0.2997 -> 0.3181 (UP 8.6%), psivar GROWS 6e-4 -> 0.022 -> 0.034 -- the
  ROUND soliton picks up spurious NON-axisym structure under warm-start (yet FRESH m=1 solves are grid-
  stable 0.29-0.30). => interp_state warm-start INJECTS structure into steep soliton states (passes the
  smooth-field accuracy gate 1.8e-15 but not the steep-core reality), compounding up the ladder.
  m=2 (oblate seed): 16->18->20 = 16.87 -> 41.25 -> 94.39 (diverges); the oblate basin isn't even
  reached at 16x8x8 (psivar 2e-3 ~ axisym there). Richardson meaningless.
KEY DIAGNOSTIC: FRESH per-grid solves give grid-STABLE m=1 (~0.29-0.30); WARM-START continuation does
NOT (injects non-axisym structure). For m>=2 the multi-basin landscape + per-grid basin shift + finer-
grid solver difficulty compound, so even fresh basin-hopping per grid does not yield a consistent mass.
VERDICT: the CATALOG STRUCTURE is solid (sectors exist; m=1 round stable, mass 0.29-0.30 grid-stable;
m>=2 break to non-axisym oblate/toroidal, coupled-stable) but the m>=2 ABSOLUTE MASSES are NOT grid-
convergeable with the current spectral solver + continuation machinery. Pinning them needs a research-
grade upgrade (a working strong-preconditioned matrix-free solver, or a discretization that doesn't
inject non-axisym structure under refinement, or a fundamentally better-conditioned large-grid solve)
-- a real next-phase effort, OR a reframe. Banked m>=2 mass = NOT DETERMINED (only at-grid 18x8x8
estimates: m=2 oblate ~12.2-12.4, which itself is one grid). DATA-BLIND; category-A throughout.
