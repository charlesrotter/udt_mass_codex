# P5c-step-3 — STABILITY TEST on ALL BASINS (the family question)

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE (constraint-respecting
stability of the five physical basins; the explicit question — FAMILY of stable distinct
objects, or round = the one particle + unstable saddles). **DATA-BLIND** (units L=1; no
wall numbers; NO M_MS banked). Driver: claude-opus-4-8[1m]. Date: 2026-06-20.
Branch: `p5c-stability`. NEW FILES ONLY (`p5c_stability.py`, `p5c_stability_coupled.py`;
committed `full3d_*`/`p5c_basins` reused as imports / saved fields only — not edited).

Parent: `p5c_basins_results.md` (+ `p5c_basins_VERIFIER.md`, SOUND). At Nr=12, m=1,
charge-1, p=0.4, kap8=0.05: FIVE distinct physical basins — round (M_MS 0.309, |S|84,
lowest-energy + most-regular), oblate (0.405), pert_s (0.375, non-axisym), prolate
(0.440), toroidal (0.541) — plus pert_L (spurious, excluded). The basins' FLOORED fields
were SAVED by p5c_basins.py at `/tmp/p5c_basin_12_{name}.pt` and are REUSED here (no
re-solve from scratch).

THE QUESTION (Charles, OBSERVE not target): are the multiple same-charge floored
solutions a FAMILY of genuinely STABLE distinct objects, or is the round one the single
particle with the others UNSTABLE saddles that decay to it? **OBSERVE — no family wanted.**

---

## METHOD (constraint-respecting throughout — NOT raw fixed-metric Hessian alone)

Memory [[gravitating-soliton-stability-test]] / phase3b precedent: the FIXED-METRIC
matter Hessian OVER-COUNTS instabilities for a gravitating soliton (off-constraint
negative modes). So the test is two-layered, and the *coupled* layer is decisive.

**(1) Fixed-metric body-Theta Hessian** (`p5c_stability.py hess`). Energy Hessian
H_E = −H_S of the native matter action S = ∫√(−g) L dV (the SAME action that orders the
basins) over the FREE body-Theta DOF (interior radial shells [1:−1]; the residual pins
Th[0]=mπ, Th[−1]=0 via BC rows, so those are not free). Diagnostic of Theta-sector
saddle structure ONLY — recompute on the saved field, no re-solve.

**(2) Coupled, constraint-respecting probes** (`p5c_stability_coupled.py`). Every probe
re-solves the FULL coupled residual (`full3d_newton.newton_solve` — re-imposes Einstein +
matter EL each step), so the perturbed state is dragged back onto the constraint surface.
Three probes:
  - **REFLOOR (A):** re-solve from the saved field in place. A genuine coupled fixed
    point stays put (its=0). Confirms each basin is a real coupled solution, not a stall.
  - **KICK (B):** perturb the WHOLE field (a,b,c,d,Th) by a random body kick, re-pin BCs,
    re-solve. Small kick → does it return to its OWN basin (locally stable) or flow away?
  - **MELT (C):** seed from the convex blend u = (1−s)·basin + s·round (BCs re-pinned),
    re-solve at s=0.25/0.50/0.75. Tracks whether the basin is separated from round by a
    BARRIER (returns to itself) or slides into round (same well / shallow barrier).

m=1 ROUND = SIGN CALIBRATION: under refloor it must stay (its=0), and under a small kick
it must return to round. Confirmed (see §1, §3).

---

## 1. ROUND SIGN-CALIBRATION — PASSED

- **Fixed-metric Theta-Hessian:** round n_neg=0 (lowest8 = [0.232, 0.232, 0.948, …], all
  POSITIVE). RAW n_neg=0 already — the cleanest calibration (no off-constraint negatives
  even to clear).
- **Coupled REFLOOR:** its=0, dM=0, d_field=0 — round is a perfect coupled fixed point.
- **Coupled small KICK (amp=0.01):** RETURNED to round (d_self=0.029, M 0.309→0.311).
  Round is locally STABLE (n_neg=0 constraint-respecting). **Calibration holds — method
  is sign-correct; no fix needed.**

---

## 2. PER-BASIN STABILITY TABLE (Nr=12)

Fixed-metric Theta-Hessian (RAW) and coupled (constraint-respecting, CR) classification:

| basin | M_MS | \|S\| | RAW Theta-Hess n_neg | coupled refloor | small-kick (amp 0.01) | CR local class |
|---|---|---|---|---|---|---|
| round    | 0.309 | 84  | **0** | its=0 (fixed pt) | RETURNS (d 0.029) | **STABLE (local min)** |
| oblate   | 0.405 | 117 | **0** | its=0 (fixed pt) | (melt, see §3) | LOCAL min, SHALLOW well |
| pert_s   | 0.375 | 118 | **0** | its=0 (fixed pt) | (melt, see §3) | LOCAL min, SHALLOW well |
| prolate  | 0.440 | 133 | **0** | its=0 (fixed pt) | (melt, see §3) | LOCAL min, SHALLOW well |
| toroidal | 0.541 | 179 | **0** | its=0 (fixed pt) | RETURNS (d 0.025) | LOCAL min, SHALLOW well |

**KEY OBSERVATION (surprising): ALL FIVE basins have RAW fixed-metric Theta-Hessian
n_neg = 0.** None is a Theta-sector saddle; every floored solution is a local *minimum*
of the matter action in the Theta direction (lowest eig ≈ 0.19–0.26 for all). So the
multiplicity is NOT "round = minimum, others = Theta-saddles." The phase3b m≥2 picture
(raw n_neg=19, 44 → off-constraint) does NOT recur at m=1: there are no negative
Theta-modes to be off-constraint in the first place.

The basins differ in their METRIC warps + coupled structure, which the Theta-only
Hessian cannot see — so the family question must be settled in the COUPLED space (§3).

---

## 3. THE COUPLED MELT TEST — WHERE THE NEGATIVE FLOW HEADS

Blend each off-round basin toward round (s = fraction of round), re-solve. M_MS of the
re-floored result (round ref M_MS = 0.309), and where it lands by field distance:

| basin | s=0.25 (mostly basin) | s=0.50 | s=0.75 (mostly round) |
|---|---|---|---|
| oblate   | M 0.359 → own side | M 0.328 → ROUND (d 0.086) | M 0.311 → **ROUND** |
| prolate  | M 0.386 → own side | M 0.346 → near round (d 0.086) | M 0.320 → **ROUND** |
| pert_s   | M 0.338 → own side | M 0.310 → ROUND (d 0.141) | M 0.303 → **ROUND** |
| toroidal | M 0.449 → own side | M 0.379 → own side (d 0.125) | M 0.332 → **ROUND** |

**Pattern (uniform across all four off-round basins):** the re-floored M_MS DECREASES
MONOTONICALLY toward round's 0.309 as the round-fraction grows, and EVERY basin MELTS TO
ROUND at s=0.75 (and most already at s=0.50). At s=0.25 each returns toward its own
region (a barrier exists), but the barrier is SHALLOW — a finite (~half-way) push toward
round is enough to cross it. Round is the dominant attractor; the off-round basins sit in
shallow side-wells.

Corroborating KICK evidence: a LARGE random kick (amp=0.05, d_self=0.33) on ROUND did NOT
return — it flowed to OBLATE (M 0.309→0.428, floored Phi 5e-13). So oblate is a real
attractor that catches a sufficiently-kicked round; but a SMALL kick (amp=0.01) on round
returns to round, and a small kick on toroidal returns to toroidal. The wells are real
but shallow and closely spaced.

---

## 4. THE FAMILY VERDICT (observed, not targeted)

**MIXED — and specifically: the off-round basins are LOCALLY stable but GLOBALLY
metastable shallow wells; round is the dominant (lowest-energy, locally stable, widest)
attractor.** Neither extreme of the question is clean:

- It is NOT "round = the one stable particle, others = unstable saddles that decay to it"
  in the strict Hessian sense: the others are NOT saddles (RAW Theta-Hess n_neg=0 each,
  small kicks return, in-place fixed points). They are genuine LOCAL minima.
- It is NOT a clean "family of co-equal stable distinct objects" either: every off-round
  basin MELTS to round under a finite coupled push (melt s≥0.5–0.75), the barriers are
  shallow, and round is strictly lower energy (|S|=84 vs 117–179) and the broadest
  attractor (catches a kicked round at amp=0.05).

**The honest reading:** ONE dominant, lowest-energy, locally-and-broadly stable object
(round), surrounded by several SHALLOW metastable side-wells (oblate/prolate/pert_s/
toroidal) that are locally stable but decay to round under a finite perturbation and lie
strictly above it in energy. The multiplicity is real but ENERGETICALLY and
DYNAMICALLY HIERARCHICAL, not flat. This is consistent with — and SHARPENS —
p5c-step-2's "energy-min and regularity both select round": stability now adds a THIRD
agreeing criterion (round is the broadest attractor + the others are shallow metastable),
all three pointing at the same branch.

**Caveat (scope):** "shallow / metastable" is read from finite-amplitude melt + kick
behavior at Nr=12, not from a barrier-height computation. The melt seeds at s=0.25 do not
return EXACTLY to the deep basin (they land partway), so the side-well depths are not
precisely pinned here. The qualitative hierarchy (round dominant; others shallow,
higher-energy, decay-to-round under finite push) is robust across all four; the
quantitative barrier heights are not measured.

---

## 5. AUDIT

- **Constraint-respecting genuinely applied (not raw Hessian)?** YES. The verdict rests
  on the COUPLED probes (refloor/kick/melt), each a full `newton_solve` re-imposing
  Einstein + matter EL. The raw fixed-metric Theta-Hessian is reported as a *diagnostic*
  (and it found n_neg=0 everywhere, so there was nothing to "demote" — the coupled layer
  carries the result). The Theta-only Hessian was explicitly NOT trusted as the verdict.
- **Round calibrated?** YES. Theta-Hess n_neg=0; coupled refloor its=0; small kick
  returns (d 0.029). Method is sign-correct; no fix was needed.
- **Data-blind?** YES. Units L=1; M_MS/|S| are dimensionless geometric readouts; no
  comparison to any observation; NO M_MS banked.
- **Observe-not-target (no family wanted)?** YES. The result is MIXED and is reported as
  mixed — neither a clean family nor a clean single-particle. The round-dominant reading
  was not sought; it EMERGED and happens to agree with step-2's energy/regularity finding
  (flagged as corroboration, not as a target hit).
- **Anti-hang held?** YES. SINGLE clean process per solve, strictly sequential, never
  concurrent. Nr=12 only (Nr=16 deferred — see throughput note). Newton maxit capped
  (15–25); each invocation < ~5 min (longest: pert_s melt 281s for 3 blends; per-solve
  ≤140s). Hessian/refloor recomputed on saved fields (no re-solve). One probe was
  auto-backgrounded by the harness but ran as a single process to completion; no
  concurrent solve, GPU never contended.

---

## 6. SCOPED STATUS / WHAT THE SELECTION-PRINCIPLE STEP INHERITS

- **At Nr=12, m=1:** all five physical basins are coupled fixed points + Theta-sector
  local minima + locally kick-stable; under a finite coupled melt toward round they ALL
  collapse to round, monotonically in M_MS. Round is the lowest-energy, broadest,
  dominant attractor; the other four are SHALLOW metastable side-wells above it.
- **The selection-principle step inherits:** stability is now a THIRD criterion (after
  energy-min and regularity, step-2) that AGREES on round — round is not just the energy
  minimum and most-regular branch but the DOMINANT, broadest stable attractor; the
  off-round basins are higher-energy shallow metastable wells that decay to it under a
  finite push. An energy-min / continuation-from-known-limit selection of round is now
  triply corroborated.
- **NOT settled here:** (i) the quantitative barrier heights / well depths (only finite-
  amplitude behavior probed); (ii) Nr=16 confirmation of the melt hierarchy (throughput —
  the Nr=16 free-solve tail is slow per p5c-step-2; deferred, FLAGGED); (iii) whether at
  HIGHER winding (m≥2, charge≥2) the picture changes (the phase3b m≥2 sector DID have
  genuine Theta-saddles — out of scope here). NO M_MS bankable; selection-principle DERIVE
  remains GATED on Charles.

---

## PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual / coupled solve = `full3d_newton.newton_solve` | DERIVED (reused) | committed; re-imposes Einstein+matter EL (constraint-respecting) |
| Matter action S = ∫√(−g) L dV (Hessian + energy) | DERIVED (reused) | native action; recomputed inline (committed matter_action has stray-`n` bug) |
| Saved floored fields `/tmp/p5c_basin_12_{name}.pt` | DERIVED (reused) | p5c_basins.py output; refloor confirms each is a true coupled fixed point |
| Free-Theta DOF for Hessian = interior radial [1:−1] | CHOSE (numerics) | BC rows Th[0],Th[−1] pinned by residual, not free |
| Hessian neg-mode tol = 1e-6·scale | CHOSE (numerics) | phase3b convention; n_neg=0 for all basins regardless |
| Melt blends s=0.25/0.50/0.75 toward round | CHOSE (probe) | spans basin-dominant→round-dominant; BC rows re-pinned |
| Kick amp 0.01 (small, local) / 0.05 (large) | CHOSE (probe) | 0.01 stays in-basin (local test); 0.05 leaves round's well |
| "shallow metastable" reading | OBSERVED (not chosen) | from monotone melt-to-round + small-kick-returns; barrier heights NOT measured |
| Nr=12, p=0.4, kap8=0.05, m=1 | CHOSE (control) | the step-2 anchor regime; Nr=16 deferred (throughput) |

---

## ATTACK HERE (for a blind verifier)

1. **Are the off-round basins REALLY local minima, or did the Theta-only Hessian miss
   metric-direction negatives?** The RAW n_neg=0 is for the Theta sector at fixed metric.
   A genuine coupled-Hessian (over a,b,c,d,Th jointly, constraint-projected) could reveal
   a metric-direction instability the Theta-Hessian hides. Attack: build the full coupled
   Hessian (or a Lanczos few-mode probe of dF/du’s symmetric part) and confirm n_neg=0
   per basin — the small-kick-returns result argues for stability, but a single random
   kick samples one direction, not the full mode space.
2. **Is the melt "collapse to round" a real basin merge, or a seed artifact of the convex
   blend?** The blend (1−s)·basin + s·round may pass THROUGH round’s basin geometrically
   regardless of barriers. Attack: melt along a NON-round target (basin→toroidal, etc.) and
   along a curved path; check whether the collapse is specifically toward round or just
   toward whichever endpoint the straight blend favors.
3. **Barrier heights are not measured.** "Shallow metastable" is qualitative. Attack: a
   string/NEB (nudged elastic band) between round and each basin to get the actual barrier;
   if a barrier is high, that basin is a genuinely distinct stable object, not metastable.
4. **Nr-dependence.** Everything here is Nr=12. p5c-step-2 found the basin SPREAD GROWS
   with Nr. Attack: re-run the melt hierarchy at Nr=16 (throughput-limited — the free tail
   is slow); does the round-dominance survive, or do the side-wells deepen at finer grid?
5. **The large-kick-round→oblate result.** A 0.05 kick on round floored at oblate. Verify
   this is round LEAVING its basin (expected for a kick > barrier) and not a solver
   artifact; map the kick amplitude at which round stops returning (the basin radius).
6. **Charge/winding scope.** Only m=1 tested. phase3b found genuine saddles at m≥2. The
   "round dominant + shallow side-wells" picture may be m=1-specific. Attack: repeat at
   m=2 once that sector’s basins are mapped.
