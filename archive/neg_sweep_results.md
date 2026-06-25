# NEGATIVE-PHI MATTER-CELL BOUNDARY SWEEP — Results

Date: 2026-06-13. Driver: Claude (Opus 4.8, 1M ctx). New file (append-only).
Frame: CRITICAL_UNIVERSE_FRAME.md (governing) + CANON C-2026-06-10-2 (matter
cells inside-out, phi: 0 at the interface -> NEGATIVE toward the core, the
whole structure the MIRROR across phi->-phi of the universe cell whose
boundary is the CMB at +7.004 = ln(1101)) + CANON C-2026-06-13-1 (the metric
propagates; c_r^2 = e^{-4phi}, c_th^2 = e^{-2phi}/r^2).

**CORRECTS a regime error:** the prior whole-metric sweep (sweep_results.md /
sweep_branch_map.py / registry #39) ran the core depth in POSITIVE phi (p>0).
By canon MATTER LIVES AT NEGATIVE PHI. This sweep flips the inside-out core
into negative phi and asks Charles's binding question: is there a FINITE
NEGATIVE-phi physical boundary (the mirror of the CMB at +7.004) that you
cannot integrate past — and is THAT what "no math worked at large negative
phi" was?

METRIC-LED, EXPLORATORY, DATA-BLIND (boundary read independently, THEN
compared to -7.004). Accurate Taylor/regular-series allowed per Charles's
method ruling; no lossy linearization; both mass-sign conventions reported.

Scripts: `neg_sweep_branch.py` (float64 map + bisection), `neg_sweep_mpmath.py`
(high-precision adaptive boundary test), `neg_sweep_verify.py` (final
cross-integrator pass-through proof + mirror test). Log `/tmp/neg_sweep.log`;
JSON `/tmp/neg_sweep_branch.json`, `/tmp/neg_sweep_verify.json`.

The metric's OWN radial field equation (exact; `wint_symcheck.py`; built on,
NOT re-derived):

```
(1/r^2) d_r(r^2 e^{-2phi} phi_r) = Phi(e^{-2phi} - e^{phi})
 <=>  phi'' + (2/r)phi' - 2 phi'^2 = Phi(1 - e^{3 phi})      [x e^{2phi}]
```

Inside-out matter cell: phi(r_in=1) = p < 0 (NEGATIVE core), phi'(r_in) = 0
(the metric's mirror-parity regularity phi'=0 at the core — the SAME regular
series the historical CMB-blowup fix used: {const + quadratic + cubic, NO
linear term}; here the const is p<0). Integrate OUTWARD; the field RISES from
p<0 to 0; r* = first radius where phi returns to 0 = the outer interface.
Phi=1, r_in=1 throughout (the absolute scale rides 1/sqrt(Phi) per #39 §4,
unchanged here).

---

## (A) THE NEGATIVE BRANCH — the matter solution space toward the core

`neg_sweep_branch.py` [A], float64 Radau (rtol 1e-12), instrumented at every
depth. msA = (c^2 r/2G)(e^{-2phi}-1) [convention A]; comp from the extremal
(core) phi. Reading down the table = going DEEPER toward the core:

```
 p(core)     r*        comp        f_core=e^{-2phi}_core  c_r_core   lapse_c     msA_core      Kmax    Kloc
 -0.010    2.2120    -0.0202        1.020                 1.020       1.010       1.01e-2     5.3e-3   0.00
 -0.100    2.2368    -0.2214        1.221                 1.221       1.105       1.11e-1     6.0e-1   0.00
 -0.300    2.2901    -0.8221        1.822                 1.822       1.350       4.11e-1     7.4e+0   0.00
 -0.800    2.4023    -3.9530        4.953                 4.953       2.226       1.98e+0     1.4e+2   0.00   <- hadronic phi0
 -1.000    2.4363    -6.3891        7.389                 7.389       2.718       3.20e+0     3.6e+2   0.00
 -2.000    2.5241   -53.598        54.60                 54.60        7.389       2.68e+1     2.3e+4   0.00
 -3.000    2.5425  -402.43        403.4                 403.4         20.09       2.01e+2     6.9e+8   1.00
 -5.000    2.5459 -2.2e4          2.20e4                2.20e4        148.4       1.10e+4     4.7e16   1.00
 -7.004    2.5459 -1.2e6          1.21e6                1.21e6        1101        6.06e+5     4.6e23   1.00
-10.000    2.5459 -4.9e8          4.85e8                4.85e8        2.43e4      2.43e+8     1.2e34   1.00
-12.000    2.5459 -2.6e10         2.65e10               2.65e10       1.63e5      1.32e+10    1.1e41   1.00
```

What the matter (negative-phi) solution space looks like toward the core:

- **ONE round cell, a smooth one-parameter family in the core depth p<0** —
  the exact mirror partner of the positive-phi family (#39). No bifurcation,
  no second type, no discrete preferred p along the family.
- **r* GROWS then ASYMPTOTES** (2.21 -> **2.5459305436**), the negative-phi
  mirror of the positive side's SHRINK-to-1.6859. The interface sits a fixed
  absolute distance outside the core; the cell is geometrically bounded.
- **comp = 1 - e^{-2p} EXACTLY** (here p<0, so comp goes NEGATIVE and runs to
  -inf): the dilation tie X = 1 - f with f = e^{-2phi} > 1 at the core. The
  "compactness" is the same machine-exact law as #39, continued through the
  fixed point phi=0 into the negative branch.
- **Curvature (Kretschmann) DIVERGES toward the core and LOCALIZES there**
  (Kloc: 0 -> 1 by p~-3): the curvature-singular seal is the deep core, just
  as on the positive side.

## (B) c_eff AND TIME-RATE — do they diverge? YES, reciprocally

By canon C-2026-06-13-1, at the matter core (phi=p<0):
- radial wave speed **c_r = e^{-2phi} = e^{-2p} -> +inf** (RUNS AWAY LARGE),
- angular **c_th = e^{-phi}/r = e^{-p}/r -> +inf**,
- lapse / time-rate **sqrt(-g_tt) = e^{-phi} = e^{-p} -> +inf** (time runs
  INFINITELY FAST at the core).

This is the EXACT RECIPROCAL of the universe/CMB side, confirmed numerically
(`neg_sweep_verify.py` [3]): c_r(matter, phi=-X) * c_r(universe, phi=+X) = 1
to machine precision for X = 0.8 and X = 7.004. At +7.004 the universe is
FROZEN (c_r ~ e^{-14} ~ 8.25e-7, lapse 1/1101); at the matter core the same
depth gives c_r ~ 1.21e6, lapse 1101 — "time stopping" mirrored into "time
running away." **Charles's reciprocal-c_eff prediction is CONFIRMED as a
pointwise phi->-phi symmetry of the metric.**

## (C) MASS-SIGN VERDICT — convention A (e^{-2phi}-1) is the physical one

Both conventions of the Misner-Sharp dilation tie m = (c^2 r/2G)(±(...)):
- **Convention A: (e^{-2phi} - 1).** At phi<0, e^{-2phi}>1 -> msA POSITIVE,
  and it GROWS monotonically toward the core (1.0e-2 at p=-0.01 -> 1.3e10 at
  p=-12). **POSITIVE energy GROWING toward the core = "smaller cell = higher
  energy."** This is the physical convention for the matter cell.
- **Convention B: (1 - e^{-2phi}).** At phi<0 this is NEGATIVE everywhere in
  the cell — unphysical for a matter cell (it is the convention natural to
  the POSITIVE-phi universe side, where 0<f<1).

**VERDICT: the matter cell takes mass convention A; the universe cell takes
convention B. The sign convention FLIPS across the phi=0 mirror fixed point**
— consistent with phi=0 being the matter<->non-matter dissolution surface
(horizon_cmb_correspondence.md §3). Smaller/deeper = higher energy holds in
the matter sector under A.

## (D) THE BOUNDARY VERDICT *** SMOOTH SEAL — NO FINITE-PHI PHYSICAL WALL ***

This is the decisive deliverable. Charles's central hypothesis was that "no
math worked at large negative phi" might be a PHYSICAL boundary at finite
negative phi (the mirror of not passing the CMB). It is NOT. The blowups are
NUMERICAL; the field continues smoothly through every one of them.

**Discrimination chain (fold-you-pass-through vs finite-phi wall):**

1. **float64 Radau** quits at p ~ **-13.2034** (`neg_sweep_branch.py` [B],
   bisected to 1e-9). This LOOKS like a clean finite boundary.

2. **It is a SOLVER ARTIFACT — pass-through proven** (`neg_sweep_verify.py`
   [1]). At p = -13.20, -13.21, -13.5, -14.0, Radau returns `None` (stiff
   stall in the razor-thin interface boundary layer) while **scipy DOP853
   sails straight through** and returns r* = 2.54593060955... A genuine
   physical wall is integrator-INVARIANT; this "edge" is not. The Radau stall
   is the interface boundary layer becoming stiff once the core has already
   asymptoted, NOT the field ceasing to exist.

3. **High-precision mpmath, DATA-BLIND, 33x deeper** (`neg_sweep_mpmath.py`,
   `neg_sweep_verify.py` [2]; adaptive RK4, dps=40, step-doubling error
   control, source-overshoot guard so a transient never overflows e^{3phi}).
   The cell **ALWAYS CLOSES** and r*(p) CONVERGES to a finite asymptote:

   ```
       p        r*(p)                 r*(p) - r*(-20)
     -10      2.5459305405...         -3.0e-9
     -13.2    2.5459305436...         -5.0e-12   (past the float64 "edge")
     -20      2.54593054355641        0          (anchor)
     -50      2.54593054355641        -2.3e-15
     -100     2.54593054355640        -9.4e-15
     -354     2.54593054355638        -2.9e-14   (past e^{-2p} float overflow)
     -500     2.54593054355637        -4.2e-14
   ```

   From p=-15 to p=-500 — a factor 33 deeper than the float64 "edge", and
   PAST the float64 overflow of e^{-2p} at p~-354 — r* is CONSTANT to ~4e-13.
   The residual drift (1e-13 ... 4e-13) GROWS with integration length =
   accumulated step error, NOT an approach to a wall (a wall would diverge,
   not converge). **r*(p -> -inf) = 2.5459305435564 (smooth finite asymptote).**

**VERDICT: the negative-phi matter cell has NO finite-phi physical wall in
the radial sector. The boundary is the SMOOTH SEAL at the core endpoint
phi -> -inf (f_core = e^{-2p} -> +inf, curvature-singular), the exact mirror
of the positive-phi seal (#39 §3: f_core -> 0 there). The cell closes for ALL
p<0.** Data-blind boundary phi value = **-infinity (the seal), NOT a finite
-7.004.** Three independent integrators agree (scipy Radau, scipy DOP853,
mpmath adaptive RK4).

## (E) THE MIRROR TEST — symmetry YES, wall-map NO

Reciprocal c_eff: **CONFIRMED** (§B; product = 1 exactly). The phi->-phi
involution IS an exact pointwise symmetry of the metric and its wave speeds.

BUT the mirror does NOT map the matter boundary onto the CMB boundary, and
the data-blind value does NOT come out at -7.004:

- The CMB boundary at +7.004 is set by an OBSERVATION (1+z_CMB = e^{phi*});
  the radial field does NOT stop closing at +7.004 — on the positive side it
  runs smoothly to the seal at +inf (#39 §3). It is a finite OBSERVED depth
  on an open existence interval, not an integration wall.
- Its mirror image is therefore NOT a wall at -7.004 either: nothing in the
  radial sector stops the matter cell at -7.004. -7.004 is simply the depth
  at which the matter cell's reciprocal c_eff equals the CMB's frozen value's
  reciprocal — a distinguished OBSERVED depth on the negative branch, the
  mirror of the CMB depth, but NOT a boundary the field cannot pass.

**So Charles's "fascinating if a similar scale" reading survives only in the
WEAK sense: -7.004 is a distinguished mirror depth (reciprocal-c image of the
CMB), but it is NOT a physical wall. The matter cell integrates straight
through -7.004 (table (A): p=-7.004 is a fully regular OK cell) and onward to
the seal at -inf.** The strong reading (a finite-phi wall near -7.004) is
REFUTED by the high-precision pass-through.

## (F) DID THIS EXPLAIN "NO MATH WORKED AT LARGE NEGATIVE PHI"? — YES, as ARTIFACT

Charles's prior-failure question is answered, and the answer is the OPPOSITE
of the hypothesis's strong form:

- The prior large-negative-phi blowups (Bratu fold, e^{3phi} overflow, the
  unbounded operators, the flow-chart retreats) were **NUMERICAL artifacts,
  not a physical boundary.** This sweep reproduces every one of them and
  shows the field passes through:
  - the "Bratu fold" / Radau stall at p~-13.2 -> DOP853 + mpmath pass through;
  - **e^{3phi} overflow:** in the negative-phi core, phi<0 makes e^{3phi}
    TINY (the source -> Phi), so the overflow is NOT in the source at the
    core — it is the e^{-2phi} = e^{-2p} term in the DIAGNOSTICS/operator
    that overflows float64 at p~-354. mpmath/log-domain passes it (§D row
    -500). This is exactly the "do NOT mistake float overflow for the
    physical boundary" trap, caught.
  - the "unbounded operators / flow-chart retreats": the field equation is
    perfectly well-behaved; the operator quantities (f, c_eff, lapse) run to
    +inf at the core BECAUSE the seal is a genuine curvature singularity at
    phi->-inf — a real endpoint, but reached only in the limit, never a
    finite-p wall.

**CONCLUSION: "no math worked at large negative phi" was float64 stiffness +
overflow at the deep seal, NOT a finite physical boundary. The math works
fine in high precision; the cell closes for all p<0.** This CORRECTS the
implicit premise of the prior retreats.

## (G) EMERGENT STRUCTURE NEAR THE EDGE

Not tested with live 2D angular lobes in THIS negative-phi run (scope: the
radial-sector boundary verdict was the decisive deliverable and is now
settled). The positive-phi whole-metric solve (#39 §5) found every seeded
lobe l=1..4 relaxes to ROUND at machine zero in the full 2D both-sector
solve; by the exact phi->-phi mirror symmetry of the operator, the bulk
negative-phi cell is expected to inherit the same "one round type, no bulk
angular source" result. **This sweep finds NO emergent discrete/angular
structure in the radial sector toward the core — the family is a smooth
continuum in p, no preferred depth, no lobes.** Per #39's verifier and
CANON, any angular type-multiplicity (q=1/3, N=3) lives in the
boundary/topological H1 area-form sector, which a bulk radial solve does not
reach. OPEN (carried forward): seed live 2D lobes on the negative branch to
confirm the mirror inheritance, and reach the H1/boundary sector.

## (H) CONVERGENCE / SCOPE / HONEST SELF-ASSESSMENT

- **Convergence: strong.** Three independent integrators (scipy Radau, scipy
  DOP853, mpmath dps=40 adaptive RK4) agree on r*(p); the asymptote
  2.5459305435564 is stable to ~13 digits across p=-15..-500. The pass-
  through of the float64 -13.2 edge is reproduced in two independent ways.
- **The boundary verdict is robust and high-precision** (the core requirement
  for physical-vs-artifact discrimination is met: mpmath went 33x past the
  float64 edge and past float overflow; the cell still closes).
- **Scope limits:** (1) radial sector only — the FULL 2D both-sector
  negative-phi solve and the H1/boundary sector are NOT done here; (2) Phi=1,
  r_in=1 (absolute scale rides 1/sqrt(Phi) per #39, untouched); (3) the seal
  at phi->-inf is a genuine curvature singularity reached only in the limit —
  characterized, not "resolved" past it (there is nothing past it); (4) the
  exact asymptote value 2.5459305436 differs from the positive side's 1.6859
  — the cell is NOT symmetric in r* under phi->-phi (the equation is not
  phi->-phi symmetric: Phi(1-e^{3phi}) is not odd), only the wave-speed
  RECIPROCITY is exact. This asymmetry is itself a finding (the mirror is a
  symmetry of c_eff, not of cell geometry).

## (I) WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. **The pass-through claim.** Re-run p in [-13.0, -14.0] with a THIRD-party
   integrator basin (e.g. a from-scratch high-order Taylor/series integrator,
   or LSODA, or boost odeint) and confirm Radau's stall is solver-specific
   and the field continues. If ANY robust integrator also terminates at a
   FINITE p, the "no wall" verdict is wrong.
2. **The mpmath asymptote.** Independently integrate at p=-100 and p=-1000 in
   a fresh high-precision implementation; confirm r* converges (not diverges)
   and matches 2.5459305436. Watch the overshoot-guard (arg>5 cap): prove it
   never fires inside the cell (phi<0 there) and is not masking a real
   blowup. Re-run WITHOUT the guard at moderate p to confirm identical r*.
3. **The mass-sign verdict.** Check that convention A (e^{-2phi}-1) is the
   one that makes msA positive AND that this is the Misner-Sharp m, not a
   sign chosen to look physical. Confirm the flip at phi=0 is forced by the
   tie m=(c^2 r/2G)(1-f), f=e^{-2phi}, not hand-picked.
4. **The mirror reading.** Hardest target: is -7.004 truly only a
   distinguished OBSERVED depth and not a wall? Confirm the cell at exactly
   p=-7.004 is fully regular (table A says OK) and that integration continues
   smoothly through it. Attack any residual temptation to read -7.004 as a
   boundary (data-blind discipline).
5. **The regime-correction itself.** Confirm the prior #39 sweep really was
   positive-phi and that flipping to negative phi is the canon-correct matter
   regime (CANON C-2026-06-10-2), so this isn't double-counting the same
   physics.
```
