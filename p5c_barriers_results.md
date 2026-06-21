# P5c-step-4 — BARRIER HEIGHTS + FULL-DIRECTION STABILITY between same-charge basins

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE (not target).
**DATA-BLIND** (units L=1; NO M_MS banked; no wall numbers). Driver: claude-opus-4-8[1m].
Date: 2026-06-20. Branch: `p5c-barriers`. NEW FILES ONLY (`p5c_barriers.py`,
`p5c_fulldir.py`; committed `full3d_*`/`p5c_*` reused as imports — never edited).

Parents: `p5c_basins_results.md` (>=5 distinct same-charge floored basins @Nr12),
`p5c_stability_results.md` + `p5c_stability_VERIFIER.md` (all 5 are charge-1 LOCAL
minima in the Theta-only fixed-metric Hessian; round/toroidal/oblate kick-stable;
round NOT a universal sink; the "melt to round" was a biased-blend artifact).

THE QUESTION (Charles, OBSERVE not target): are the >=5 distinct same-charge floored
solutions a GENUINE DURABLE FAMILY (HIGH barriers between basins => distinct objects
that cannot slump into each other) or METASTABLE WIGGLES of one object (LOW barriers
=> not a family)? Plus: are they stable in ALL directions (metric + matter), not just
the matter Theta field?

**INTERPRETATION CRITERIA (stated UP FRONT, observe-not-target):**
- barrier >> round<->basin energy gap AND >> numerical noise => GENUINE distinct
  durable objects (family plausible).
- barrier ~ 0 / comparable to noise / NEGATIVE (no ridge) => metastable wiggles / not
  distinct (NOT a family).
We report the NUMBERS and which criterion they meet. No verdict-hunting.

Energy proxy = native matter action S = int sqrt(-g)(L2+L4) dV, recomputed inline
(committed `matter_action` has a cosmetic RETURN bug, not in the value). The basin
ladder is |S| ascending: round(84) < oblate(117) ~ pert_s(118) < prolate(133) <
toroidal(179) @Nr12.

---

## 1. BARRIER TABLE (NEB / string method, Nr=12)

Method: endpoints = two SAVED floored basins (fixed); 5 images (3 interior); each
interior image relaxed PERPENDICULAR to the round<->basin chord while its chord
projection is HELD at s_k (transverse-only NEB relaxation; the image cannot collapse
to an endpoint). Images floor to Phi shown. Barrier = max interior |S| - higher
endpoint |S| (a separating ridge would be POSITIVE). DIP = lower endpoint |S| - min
interior |S| (POSITIVE => the path passes BELOW the lower basin, i.e. through a
lower-energy / rounder region — the opposite of a wall).

| pair | barrier (\|S\| above higher endpt) | dip below lower endpt | gap_AB | barrier/gap | nimg | max image Phi | nebit |
|---|---|---|---|---|---|---|---|
| round <-> oblate    | **-16.16** | -0.74 | 33.78 | -0.478 | 5 | 2.0e-12 | 4 |
| round <-> prolate   | **-19.88** | -4.68 | 49.16 | -0.404 | 5 | 1.4e-12 | 4 |
| round <-> pert_s    | **-13.35** | -3.90 | 34.10 | -0.392 | 5 | 2.5e-09 | 4 |
| round <-> toroidal  | **-37.71** | -10.25 | 95.54 | -0.395 | 5 | 2.1e-11 | 4 |
| oblate <-> prolate  | **-34.39** | **+33.13** | 15.38 | -2.236 | 5 | 2.7e-13 | 5 |
| toroidal <-> prolate| **-17.08** | -6.19 | 46.39 | -0.368 | 5 | 5.1e-13 | 5 |

Relaxed S ~ raw-interpolation S to <0.5% in EVERY image (e.g. round<->oblate s=0.5:
raw -90.306 vs relaxed -90.323). The transverse NEB relaxation barely moves the path:
the straight chord between any two floored basins ALREADY lies on (essentially) the
minimum-energy connecting path. Image floors: machine-floor (1e-12..1e-13) on every
axisymmetric pair; round<->pert_s images at 1e-9 (the non-axisym basin + long chord
5.6) — still below the <1e-9 real-image bar, FLAGGED.

---

## 2. FAMILY VERDICT FROM THE BARRIERS

**METASTABLE WIGGLES OF ONE OBJECT — NOT a durable family.** (Meets the
barrier~0/NEGATIVE criterion stated up front, decisively, on all 6 pairs.)

- **NO pair has a separating barrier.** barrier_above is NEGATIVE for every pair
  (-13 to -38 in |S|): the relaxed connecting path never rises above the higher
  endpoint. There is NO energy ridge between any two basins. barrier/gap < 0 always.
- **The round<->basin paths are MONOTONE** (|S| climbs straight from round up to each
  off-round basin, no hump): each off-round basin connects to round downhill with no
  wall — it can slump to round (or round can be pushed up to it) freely.
- **The killer: oblate <-> prolate DIPS to round.** The relaxed path between the two
  off-round basins drops to |S| ~ 84 in the middle (dip_below = +33 above the LOWER
  endpoint) — i.e. essentially down to the ROUND value. The two off-round basins are
  connected THROUGH the round region with no intervening barrier. They are not walled
  off from each other; they share the same floor via round.

So the >=5 floored same-charge solutions are shallow local dimples on a nearly-flat,
fully-connected manifold with NO barriers between them. By the up-front criterion this
is metastable wiggles, NOT a genuine durable family.

---

## 3. FULL-DIRECTION (metric + matter) STABILITY — closing the Theta-only gap

Two probes (both constraint-respecting; the fixed-metric Hessian over-counts, per
memory [[gravitating-soliton-stability-test]]):

### (a) FD curvature of the CONSTRAINED action along METRIC channels a,b
For each channel: add +/-h*(smooth body bump) to that warp ONLY, COUPLED re-solve
(Theta + other DOF relax to the constraint surface), read |S|; central 2nd difference
= curvature. POSITIVE => local min along that metric direction.

| basin | ch a curv | ch b curv | verdict |
|---|---|---|---|
| round (calibration) | +6.94 | +23.2 | metric-stable (local min, all +) |
| toroidal            | +99.0 | +15.4 | metric-stable (local min, all +) |

Round calibration PASSES (positive curvature both metric channels => round is a
genuine local min in the metric directions, not a metric-saddle). toroidal likewise.
=> Along a single coherent smooth metric mode, each saved basin IS a local minimum —
no metric-direction negative mode the Theta-only Hessian missed. (Channels c,d not
swept — budget; a,b are the dominant warps. Throughput-limited on c,d.)

### (b) METRIC-ONLY random kick + COUPLED re-solve (broadband metric perturbation)
Kick ONLY a,b,c,d by +/-0.05 random (Theta untouched), re-pin BCs, full coupled
re-solve. Does it return to its own saved basin?

| basin | M0->Mr | \|S\|0->\|S\|r | d_self | nearest basin | verdict |
|---|---|---|---|---|---|
| round    | 0.309->0.306 | 83.7->89.8 | 0.247 | pert_s (0.214) | FLOWED off (not back to round) |
| oblate   | 0.405->0.412 | 117.5->133.9 | 0.241 | pert_s (0.198) | FLOWED off |
| toroidal | 0.541->0.595 | 179.3->232.9 | 0.238 | toroidal (0.238) | wandered, |S|+30% |

NONE returns tightly to its own saved point: d_self ~ 0.24 in ALL three — comparable
to the inter-basin field spacing itself (0.17-0.29 from p5c_basins). A broadband metric
kick lands on a DIFFERENT floored point on the same connected manifold (round & oblate
both drift toward pert_s; toroidal into a deeper nearby config). The metric directions
are NOT stiff confining walls.

### Reconciliation (the two probes agree on "shallow, connected"):
The single-coherent-mode FD curvature is POSITIVE (each point is a weak local dimple),
yet a broadband random kick WANDERS to neighbors and the inter-basin barriers are
ABSENT. Both are the same picture: a nearly-flat manifold of shallow local minima with
NO separating barriers. Locally each is a min; globally there are no walls between them.

### (c) Unbiased coupled kicks — 5/5 complete
- round, toroidal, oblate: kick-stable in the loose neighborhood sense (prior step +
  metric-kick here; stay in broad neighborhood).
- **prolate (new):** unbiased coupled kick (amp 0.03) FLOWED to round (d=0.222), did
  NOT return to prolate. M 0.440->0.459 then toward round.
- **pert_s (new):** unbiased coupled kick stayed nearest pert_s (d=0.091) but SLID
  DOWNHILL — |S| 117.8->107.8, M 0.375->0.323 toward round (lower energy).
=> 5/5: none is a tight attractor; prolate and pert_s drift toward round / lower |S|.

---

## 4. AUDIT

- **NEB genuine (not a blend-toward-endpoint)?** YES. The condemned 'melt' test blended
  toward round with ALL DOF free (it slid to the nearest well — biased dynamics). This
  NEB instead PINS each image's chord projection at s_k (re-snapped every iter) and
  projects OUT the along-chord step component (P_perp du) — pure transverse relaxation
  with FIXED endpoints. No image can reach an endpoint; the relaxed string is the
  minimum-energy connecting ridge. The finding (relaxed S ~ raw S) is itself evidence
  the manifold is flat, not an artifact of insufficient relaxation (images floored to
  1e-12..1e-13).
- **Constraint-respecting metric-direction test genuine?** YES. Both the FD curvature
  and the metric-kick call the committed `full3d_newton.newton_solve` (re-imposes
  Einstein + matter EL every step), so displaced metric warps relax onto the constraint
  surface — the over-counting fixed-metric Hessian is NOT used for the metric directions.
- **Round calibrated?** YES. FD metric curvature POSITIVE both channels (round = local
  min, sign-correct). (Note: under a BROADBAND metric kick even round wanders off — this
  is a real property of the flat manifold, consistent with p5c_stability's "round is NOT
  a universal sink", not a calibration failure: the coherent-mode test is the curvature
  calibration and it passes.)
- **DATA-BLIND, no M_MS banked, observe-not-target?** YES. Units L=1; M_MS/|S| are
  dimensionless geometric readouts used only to compare basins; no observation compared;
  no M_MS canonized. Criteria stated UP FRONT before reading the numbers; the verdict
  (no family) is the opposite of a "wanted" family — observed, not targeted.
- **Anti-hang held?** YES. Single clean process per solve, strictly SEQUENTIAL, never
  concurrent (each background job ran ONE python at a time inside a sequential loop; GPU
  never contended). Nr=12 only (saved basin set; NEB recomputes on saved endpoints — no
  full re-solve from scratch). Each invocation 73-122 s, well under the ~6-min cap.
  4 NEB images / bounded NEB iters / bounded Newton maxit throughout. No background poll
  of a solve. Throughput-limited items declared: metric channels c,d not swept; FD
  curvature only on round+toroidal; Nr=16 not attempted (the saved basins are Nr=12).

---

## 5. SCOPED STATUS / HONEST STANDING OF THE FAMILY QUESTION

**After this test, the family question is answered (at Nr=12, this regime, these 5
basins): the same-charge multiplicity is NOT a durable family of distinct objects.**
The >=5 floored charge-1 solutions are shallow local dimples on a flat, fully-connected
manifold with NO barriers between them — they slump into one another (and into round)
without crossing any wall; the oblate<->prolate path even dips through round. Each is a
weak local min along coherent metric/matter modes, but there are no separating ridges,
so they are metastable wiggles of essentially one object, not >=5 distinct particles.

This is consistent with the standing frontier: the single static carrier does NOT tower
into a discrete spectrum (#65 box-controlled tachyon; #44 one carrier = one particle).
The seed-dependent "basins" of p5c-step-2 are the numerical shadow of that flat
direction, not a particle catalog. It strengthens the post-postulate program: the
classical static solve gives ONE soft object; DISCRETENESS / distinct objects must come
from elsewhere (the postulate-A quantization, or DISTINCT SECTORS — charge/winding +
free non-stationary/off-diagonal/ensemble DOF — NOT one carrier's static spectrum).

**Decisive remaining gaps (the ATTACK list):**
1. Nr-trend: barriers measured at Nr=12 only (the saved basin set). A barrier could in
   principle GROW with resolution. ATTACK: re-floor 2 basins at Nr=16 and re-run one NEB
   pair; if the manifold sharpens (a real barrier appears), the verdict flips. (Step-2
   found the SPREAD grows with Nr but said nothing about barriers — untested.)
2. c,d metric channels + full FD curvature on all 5 basins (only a,b on round+toroidal
   here) — a negative metric mode could hide in the shear channels. ATTACK: `curv ... abcd`
   on each basin (budget permitting).
3. The NEB used the STRAIGHT chord + transverse relaxation with FIXED endpoints; a
   genuinely curved minimum-energy path could (in principle) have a barrier the chord
   misses. The flat result (relaxed ~ raw) argues against this, but a full climbing-image
   NEB with more images would be the rigorous closure.
4. Non-axisymmetric directions: pert_s (the psivar branch) was an endpoint here, not
   probed as a transverse mode along the round<->round neighborhood.

---

## PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual / coupled solve = committed `full3d_solver` + `full3d_newton.newton_solve` | DERIVED (reused) | unchanged; constraint-respecting |
| Energy proxy = native matter action S=int sqrt(-g)(L2+L4)dV | DERIVED (reused) | recomputed inline (cosmetic return bug in committed matter_action) |
| Endpoints = SAVED Nr=12 floored basins | DERIVED (reused) | no re-solve from scratch |
| NEB = transverse relaxation, chord projection held at s_k, P_perp step, fixed endpoints | CHOSE (method) | the standard string/TS construction; NOT a blend |
| 5 images / 4-5 NEB iters per image | CHOSE (anti-hang) | images floored 1e-12..1e-9; more images = throughput |
| metric FD bump = sin(pi*radial-frac) smooth body mode; h=0.05 | CHOSE (probe) | vanishes at both ends; single coherent metric mode |
| metric-kick amp 0.05 (a,b,c,d only, Theta fixed); kick RNG seed 7777 | CHOSE (probe) | broadband metric perturbation; reproducible |
| channels swept = a,b (not c,d); curvature only round+toroidal | CHOSE (anti-hang) | dominant warps; c,d + full set = throughput-limited (flagged) |
| barrier criterion: positive ridge >> gap & noise = family; ~0/neg = wiggles | CHOSE (criterion) | stated UP FRONT before reading numbers |
| Nr=12 only | CHOSE (control) | saved basin set; Nr-trend = open attack |
| "metastable wiggles, not a family" | OBSERVED (not chosen) | EMERGED from 6/6 negative barriers + flat metric directions; opposite of a wanted family |

---

## ATTACK HERE (for a blind verifier)
1. **Re-floor 2 basins at Nr=16 and re-run one NEB pair** (e.g. round<->toroidal). Does
   any barrier APPEAR as the grid sharpens? The whole verdict rests on barriers staying
   ~0 / negative with resolution. (Step-2's spread-grows result does NOT imply barriers.)
2. **Full FD curvature `abcd` on all 5 basins.** A negative metric-shear (c,d) mode would
   change "each is a local min" — only a,b on 2 basins tested here.
3. **Climbing-image NEB with more images** on round<->oblate: confirm the straight-chord
   transverse relaxation didn't miss a curved-path barrier. (relaxed~raw argues no, but
   it's the cheap version.)
4. **Is the metric-kick wander a real flat direction or under-relaxed?** round kick
   landed d_self=0.247 at Phi=1e-12 (floored) — so it's a genuine neighboring solution,
   not a stall. Re-run with a different RNG seed: if it lands on yet ANOTHER floored
   point at similar distance, the flat-manifold reading is confirmed.
5. **Sign/convention check on barrier_above.** S is negative; we report on |S| with the
   basin ladder = |S| ascending. Verify a TRUE transition state between two energy minima
   is a |S| MAX (it is, in this convention) and that dip_below>0 (oblate<->prolate) really
   means "passes through a lower-energy/rounder region" (it does: midpoint |S|~84=round).
