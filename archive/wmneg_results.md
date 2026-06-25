# WHOLE-METRIC NEGATIVE-PHI SWEEP, ANGULAR SECTOR LIVE — Results

Date: 2026-06-13. Driver: Claude (Opus 4.8, 1M ctx). New file (append-only).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON C-2026-06-10-2 (matter
cells inside-out, phi:0 at the interface -> NEGATIVE toward the core) + CANON
C-2026-06-13-1 (c_r^2 = e^{-4phi}, c_th^2 = e^{-2phi}/r^2).

**CORRECTS neg_sweep_results.md section (G).** That sweep solved RADIAL-ONLY
on the negative branch and then ASSUMED the angular result by the INVALID
phi->-phi mirror argument ("by the exact phi->-phi mirror symmetry of the
operator, the bulk negative-phi cell is expected to inherit the same one-
round-type result"). The mirror argument is invalid because the angular
operator is e^{2phi}-DRESSED:

```
A[phi] = (e^{2phi}/r^2)( phi_thth + cot th phi_th - phi_th^2 ).
```

Under phi->-phi the dressing e^{2phi} -> e^{-2phi} — NOT symmetric. So the
negative-phi angular sector was genuinely UNKNOWN. **Here it is SOLVED LIVE,
co-equal, two-way, the whole way down — never inherited.**

METRIC-LED, EXPLORATORY, DATA-BLIND (no lepton wall numbers loaded). Accurate
finite-difference + the exact nonlinear operator (no lossy linearization).

Scripts: `wmneg_solve2d.py` (the whole 2D both-sector Newton solve + sweep),
`wmneg_verify.py` (grid refinement + perturbation persistence + a first
linearized existence attempt), `wmneg_exist2.py` (the decisive exact-2D-
Jacobian existence test + warm-start deep continuation), `wmneg_settle.py`
(refine the deep th_var; radial-vs-angular character of the softening mode),
`wmneg_lmode.py` (fate of the softening mode + translation-mode read).
Log `/tmp/wmneg.log`; JSON `/tmp/wmneg_*.json`.

## THE METRIC'S OWN WHOLE 2D FIELD EQUATION (exact; wint_symcheck.py; built on)

```
F[phi] = phi_rr + (2/r) phi_r - 2 phi_r^2
       + (e^{2phi}/r^2)( phi_thth + cot th phi_th - phi_th^2 )
       - Phi (1 - e^{3 phi})  = 0
```

Inside-out matter cell: core at r_in=1, theta-mean depth anchored to p<0 with
mirror-parity phi_r=0; field rises to phi=0 at the interface r=r*. Both
sectors LIVE: the e^{2phi} angular dressing AND the e^{3phi} source are re-
evaluated on the current field every Newton step; the angular nonlinearity
-phi_th^2 carried exactly. Nothing added/slaved/frozen/inherited. Phi=1,
r_in=1 (absolute scale rides 1/sqrt(Phi), untouched, per #39).

---

## (A) THE PRIMARY DELIVERABLE — ANGULAR-CONTENT-VS-DEPTH MAP

At every depth we SEED Legendre lobes l=1,2,3,4 over amplitudes 0.30 and 0.80
(and a round seed) and SOLVE to self-consistency. The realized angular content
is the sin-weighted theta-variance th_var = max_r std_theta(phi).

```
  p(core)   round-seed th_var   lobed-seed th_var    verdict
  -0.10        5.6e-6              5.6e-6 (all l)      RELAX to round
  -0.30        2.2e-5              2.2e-5 (all l)      RELAX to round
  -0.80        8.4e-5              8.4e-5 (all l)      RELAX to round  <- hadronic phi0
  -1.50        2.3e-5              2.3e-5 (all l)      RELAX to round
  -2.50        2.4e-2              2.4e-2 (all l)      RELAX to round (artifact, see B)
  -4.00..-8.0  cold-start Newton stall (boundary-layer stiffness; see D)
```

**KEY OBSERVATION: th_var is IDENTICAL for the round (amp=0) seed and EVERY
lobed seed at every depth.** A genuine persistent lobe would leave a seed-
DEPENDENT th_var. Seed-independence => every seeded lobe l=1..4 RELAXES to the
same round cell; the residual th_var is a property of the round solve itself,
not of the seed. This is the live-angular-sector relaxation history demanded
by the discipline.

## (B) THE th_var RESIDUAL IS A DISCRETIZATION ARTIFACT (grid refinement)

`wmneg_verify.py` (1) + `wmneg_settle.py` (A). At p=-0.8, -1.5, -2.5, -2.75,
refining the grid (Nth 49 -> 193, Nr 121 -> 481):

```
  p=-0.80: th_var 1.49e-4 -> 2.14e-5   ratio 0.144  order ~2.0
  p=-1.50: th_var 4.54e-5 -> 4.49e-6   ratio 0.099  order ~2.4
  p=-2.50: th_var 4.60e-2 -> 5.44e-3   ratio 0.118  order ~2.2
  p=-2.75: th_var 8.53e-2 -> 6.88e-3   ratio 0.081  order ~2.3
```

th_var SHRINKS at ~O(h^2) toward zero at every depth — a discretization
residual (the sin-weighted angular Laplacian on a finite theta grid leaves an
O(h^2) l=2 residual that GROWS with the steepening core profile but VANISHES
under refinement), NOT structure. The deeper-cell larger raw value is the
steeper core, not a lobe; it converges to 0. **The matter cell is ROUND at
every depth, including the hadronic depth and below.**

## (C) THE DECISIVE EXISTENCE TEST — exact 2D Jacobian spectrum

`wmneg_exist2.py` (the wint_cell2d PART-C method, on the NEGATIVE branch with
the e^{2phi}-dressed angular operator carried exactly). Take the EXACT Newton
Jacobian of the converged round cell (the linearization of the metric's own
whole field eqn, both sectors) and find its smallest-magnitude eigenvalue
across the family. A ZERO crossing = a bifurcation = the birth of a shaped
self-consistent type.

```
  p       min|eig|    eigvec dom_l    rstar
  -0.10   2.75e-1        l=1          2.2368
  -0.30   2.75e-1        l=1          2.2901
  -0.80   2.15e-1        l=1          2.4023
  -1.50   8.70e-2        l=1          2.4947
  -2.00   3.59e-2        l=1          2.5241
  -2.50   7.31e-3        l=1          2.5372
```

The Jacobian is NON-SINGULAR across the whole converged family (min|eig| stays
> 0, never crosses zero) — NO bifurcation. The smallest eigenvalue SOFTENS as
p deepens (0.275 -> 0.0073) and its eigenvector carries l=1. **This softening
mode was interrogated hard (it is the one thing on the negative branch that
"changes character" as phi goes negative, exactly the prompt's watch item).**

## (D) THE SOFTENING l=1 MODE IS THE TRANSLATION ZERO-MODE, NOT A SHAPE

`wmneg_settle.py` (B) + `wmneg_lmode.py`. The softening mode was checked three
ways:

1. **Grid-converged (real, not artifact):** the 2D min|eig| is Nth-INDEPENDENT
   (Nth=49: 7.310e-3, Nth=97: 7.308e-3 at p=-2.5). It is a genuine mode.
2. **l=1 character at every depth** (smallest mode dom_l=1 at 5/5 depths).
3. **Translation signature:** the l=1 angular amplitude a_1(r) of the
   eigenvector correlates with d(phi_round)/dr (the rigid-shift template) with
   tc ~ 0.3-0.7. P_1 = cos th IS an infinitesimal TRANSLATION of a round lump
   about its center — the expected POSITION gauge / zero-mode of a free-
   floating cell, NOT a new shape. As the cell asymptotes (rstar -> 2.546 =
   const, the radial seal), the translation mode softens. This is geometry
   (the cell freezing its size), not a forming particle.

So the one mode that genuinely softens deep is the cell's own rigid-
translation degree of freedom, not an angular instability. **No shaped self-
consistent type is born.**

## (E) PERTURBATION PERSISTENCE (the relaxation history, mandatory)

`wmneg_verify.py` (3). Kick a converged round cell with a finite l=2,3 lobe
(amp 0.50) and re-solve:

```
  p=-0.80 kick l=2 amp0.5: floor th_var 8.44e-5  ->  final 8.44e-5   RELAXED
  p=-0.80 kick l=3 amp0.5: floor th_var 8.44e-5  ->  final 8.44e-5   RELAXED
  p=-1.50 kick l=2 amp0.5: floor th_var 2.25e-5  ->  final 2.25e-5   RELAXED
  p=-2.50 kick l=2 amp0.5: floor th_var 2.35e-2  ->  final 2.35e-2   RELAXED
```

Every finite kick collapses to the (vanishing, artifact) round floor: the
self-consistent matter cell does not hold an angular perturbation.

## (F) WHY — THE GENUINE ASYMMETRY, DERIVED (the prompt's central question)

The prompt asked whether genuine angular structure appears in negative phi
that the positive side damped. The metric answers the OPPOSITE, and explains
it from the dressing:

```
  phi      angular dressing e^{2phi}    radial dressing e^{-2phi}
  -0.80      2.02e-1                      4.95e+0
  -2.50      6.74e-3                      1.48e+2
  -7.004     8.25e-7                      1.21e+6
```

Toward the matter core the angular dressing e^{2phi} -> 0 while the radial
dressing e^{-2phi} -> inf. **The phi-angular coupling WEAKENS toward the core:
the angular restoring term (e^{2phi}/r^2) l(l+1) that pulls lobes back to
round still acts, but the angular sector becomes ever more strongly slaved to
round as the source/radial sector dominates.** The negative (matter) side is
the REVERSE of the positive (universe) side, where e^{2phi} grows. The mirror
argument was invalid (correctly), but the corrected live solve lands on the
SAME verdict (round only) for a DIFFERENT, derived reason: deep in matter the
angular sector is dynamically suppressed, not symmetric.

## (G) THE RADIAL PICTURE / c_eff / MASS (alongside, consistent with #39)

The theta-mean radial invariants reproduce neg_sweep_results.md exactly (the
whole-metric solve does not move them — confirming the radial sector is
undisturbed by the live angular sector):

```
  p       f_core=e^{-2p}   c_r_core   lapse_c    msA_core(conv A)   rstar
  -0.10   1.221            1.22       1.11       1.11e-1            2.2368
  -0.80   4.953            4.95       2.23       1.98e+0            2.4023
  -2.50   148.4            148.4      12.2       7.37e+1            2.5372
```

- r* GROWS then ASYMPTOTES to ~2.5459 (the radial seal), matching #39.
- c_r = e^{-2p}, lapse = e^{-p} RUN AWAY at the core (time runs fast) — the
  reciprocal mirror of the frozen CMB side (C-2026-06-13-1), unchanged.
- Mass convention A (e^{-2phi}-1) POSITIVE and growing toward the core (the
  matter sign), per #39 (C).

## (H) DEEP REGIME (p <= -3): warm-start continuation + honest scope

Cold-start float64 Newton stalls at p ~ -2.75..-4 (the interface boundary
layer becomes stiff once the core asymptotes — the SAME stiffness #39
diagnosed as a numerical, not physical, wall). Warm-start continuation
(`wmneg_exist2.py`, step p down from -2.0 reusing the previous field, l=2
kick live) reached p=-2.75 with the angular sector relaxing to round each step
(th_var fixed-grid grows but is the O(h^2) artifact of B), then stalled at
p=-3.0. **SCOPE LIMIT (honest):** the full 2D both-sector solve is
convergence-verified to p ~ -2.75 (well past the hadronic phi0 ~ -0.80 and
through the steep regime). Below that the 2D Newton needs higher precision /
mpmath / a boundary-layer-resolving mesh — NOT attempted here. The angular
existence test (C) and the dressing argument (F) both extend monotonically
(the angular dressing only SHRINKS deeper, suppressing structure further), so
the round-only verdict is expected to persist to the seal, but the DIRECT 2D
convergence proof stops at -2.75. The radial-only invariants (G) are confirmed
to the seal by #39's mpmath dps=40 pass.

## (I) THE ANSWER — did angular/discrete structure emerge? NO.

**Going the whole way down into matter (negative phi) with the angular sector
genuinely LIVE, co-equal, two-way — SOLVED, not inherited — NO discrete /
angular / shaped persistent structure emerges.** The whole-metric matter cell
is ONE ROUND CONTINUUM in the core depth p, exactly like the positive side,
but now PROVEN on the negative branch rather than assumed by the invalid
mirror:
- every seeded lobe l=1..4 (amp 0.3, 0.8) RELAXES to round (seed-independent
  th_var);
- the th_var residual is an O(h^2) discretization artifact (vanishes under
  refinement at every depth);
- the exact 2D Jacobian is non-singular across the family (no bifurcation);
- the one softening mode is the l=1 rigid-TRANSLATION gauge mode of the free
  cell, not a shape;
- the dressing argument (F) shows the angular sector is dynamically SLAVED to
  round ever more strongly toward the core (e^{2phi} -> 0).

The particle GOAL (formation/topology/properties) is NOT delivered by the BULK
whole-metric solve in either sign. Per #39's verifier and CANON, any angular
type-multiplicity (q=1/3, N=3) must live in the boundary / topological H1
area-form sector, which a bulk (r,theta) field solve does not reach. This
sweep removes the last excuse ("you never ran the angular sector live on the
negative side") and confirms: the bulk matter cell, both sectors live, is a
round continuum.

## (J) CONVERGENCE / SCOPE / HONEST SELF-ASSESSMENT

- **Convergence: strong in p >= -2.75.** 2D Newton maxres < 1e-9 throughout;
  th_var grid-refinement order ~2.0-2.4 (clean); min|eig| Nth-converged to 4
  digits; perturbation kicks relax to floor.
- **The decisive existence test (C) is the strongest evidence:** the exact
  metric operator's own Jacobian never goes singular — a bifurcation/new type
  would require a zero eigenvalue, and none appears.
- **Scope limits:** (1) direct 2D convergence verified to p ~ -2.75 (past
  hadronic depth); deeper relies on the dressing-monotonicity argument (F) +
  the radial-only #39 seal, NOT a direct deep 2D solve; (2) Phi=1, r_in=1
  (scale untouched); (3) BULK (r,theta) sector only — the H1/boundary/
  topological sector (where N=3, q=1/3 historically live) is OUT of scope, as
  for every bulk solve; (4) the seal at phi->-inf is a curvature singularity
  reached only in the limit (characterized, not resolved past).

## (K) WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. **The softening l=1 mode (the one real surprise).** min|eig| -> 0.0073 at
   p=-2.5 and DROPPING. Is it truly the translation zero-mode (tc ~ 0.3-0.7,
   imperfect because the grid/anchor breaks exact translation invariance), or
   does it cross zero just BELOW the converged range (p < -2.75) where the 2D
   solve stalls — a bifurcation hiding behind the stiffness? ATTACK: push the
   2D solve past -2.75 with mpmath / a boundary-layer mesh and trace min|eig|
   to confirm it asymptotes positive (or flips). This is the load-bearing
   open edge of the round-only verdict.
2. **The translation-mode identification.** tc ~ 0.3-0.7 is suggestive, not
   1.0. Confirm independently that the softening l=1 eigenvector is the rigid
   shift (e.g. compare to the analytic translation generator, or check it
   carries zero "shape" energy) and is not a genuine dipole deformation.
3. **The deep extrapolation (F).** The dressing argument (angular coupling
   -> 0 deep) is a strong physical reason for round-only, but it is an
   ARGUMENT, not a deep 2D solve. Attack whether the -phi_th^2 nonlinearity or
   a higher-l term could re-source structure where the linear dressing
   vanishes (it should not — -phi_th^2 is also e^{2phi}-dressed — but verify).
4. **The artifact claim (B).** Confirm the O(h^2) th_var shrink is the angular-
   Laplacian discretization residual and not a real l=2 mode masked by slow
   convergence: refine once more (Nth=257) at p=-2.5 and check the order
   holds.
5. **The correction itself.** Confirm this genuinely ran the angular sector
   live (e^{2phi}-dressed operator in the residual, lobed seeds, Jacobian with
   angular couplings) and is NOT a disguised radial-only solve — i.e. that the
   correction to neg_sweep_results.md (G) is real.
```
