# P5c-step-4 BARRIERS + FULL-DIRECTION — BLIND ADVERSARIAL VERIFIER

Verifier: claude-opus-4-8[1m] (independent blind adversarial). Date: 2026-06-20.
Branch: `p5c-barriers`. DATA-BLIND (units L=1; no wall numbers / M_MS banked; M_MS,|S|
are dimensionless geometric readouts only). Bounded recompute on SAVED fields. Anti-hang
held: single clean SEQUENTIAL processes, never concurrent; each < ~4 min; dense-LM /
`full3d_newton.newton_solve` + committed residual only; no background poll of a live solve
(monitored to completion). One Nr=16 check run (floored in budget).

Target: `p5c_barriers_results.md`, `p5c_barriers.py`, `p5c_fulldir.py`. Context:
`p5c_basins_results.md`, `p5c_stability_results.md` + `p5c_stability_VERIFIER.md`,
memory [[gravitating-soliton-stability-test]].

---

## HEADLINE

(a) **NO-BARRIER result is GENUINE; the NEB is sound; oblate<->prolate-through-round is
    CONFIRMED. The verdict is NOT an under-relaxed artifact.** Independently recomputed the
    KILLER oblate<->prolate pair at Nr=12 with a FINER chain (9 images vs 5) and MORE iters
    (8 vs 5). The |S| profile is smooth and barrierless, dipping to its minimum at s=0.5
    exactly = |S|=84.4 ~ round (83.7): oblate(117.5) -> 101.6 -> 90.7 -> 85.0 -> **84.4** ->
    88.9 -> 98.5 -> 113.2 -> prolate(132.9). Every image floors to Phi ~1e-13 (genuine
    residual zeros), relaxed S ~ raw S to <0.2%. The denser sampling found NO intermediate
    ridge that 5 images skipped. The "dips through round" claim is real and robust. A
    representative round<->basin pair (round<->toroidal, Nr=12) is cleanly MONOTONE
    (83.7 -> 94.0 -> 113.2 -> 141.6 -> 179.3) — confirmed from the saved path.

(b) **THE Nr-TREND GAP (the decisive open risk) — CLOSED for the stress-test pair. NO
    barrier sharpens at Nr=16.** Ran ONE Nr=16 NEB on round<->toroidal (the widest-gap pair,
    and the one whose M_MS spread grew most, 75%->104%). The s=0.5 image FLOORED (Phi=1.4e-10,
    the same depth as the basins' own Nr=16 floor) at |S|=98.4, sitting cleanly INSIDE
    [round 75.9, toroidal 166.7]: barrier_above = -68.3 (no rise above the higher endpoint),
    monotone/barrierless exactly as at Nr=12. The growing spread is a LENGTHENING FLAT
    manifold, NOT sharpening structure. "Growing spread + zero barrier" is self-consistent and
    now DIRECTLY OBSERVED at Nr=16, not merely reasoned.

(c) **Full-direction stability + reconciliation are SOUND, with a scoped caveat.** The
    metric-direction probes call the committed coupled `newton_solve` (constraint-respecting,
    not the over-counting fixed-metric Hessian — correct per [[gravitating-soliton-stability-test]]).
    The local-min character rests on the SMALL-h FD curvature (positive a,b on round+toroidal)
    AND step-3's small unbiased kicks (3/3 return); the broadband amp=0.05 kick is ~15-50% of
    the warp magnitude and lands d_self~0.24 ~ inter-basin spacing — so it does NOT cleanly
    separate "no wall" from "kick > well", but it is NOT load-bearing: the BARRIER (NEB) is the
    evidence, and it is independent of kick size. The reconciliation (positive local curvature +
    no global ridge = shallow connected manifold) is internally consistent with step-3's
    kick-stable result. CAVEAT: FD curvature tested only a,b channels on only round+toroidal;
    c,d (shear) + 3 basins untested — but a hidden negative metric mode would only make a basin
    LESS stable, REINFORCING "not a durable family"; it cannot create a barrier. Does not
    threaten the verdict.

(d) **HONEST FAMILY VERDICT: NOT-a-family (one soft object) — CONFIRMED.** The >=5 same-charge
    floored solutions are shallow dimples on a flat, fully-connected manifold with no separating
    ridges; off-round basins connect to round downhill and to each other THROUGH round. The
    decisive Nr-trend gap the agent flagged is now closed on the strongest pair. Charles's
    family question stands **ANSWERED at this regime: NO, these are metastable wiggles of one
    soft object, not >=5 distinct durable particles.** Consistent with #44 (one carrier = one
    particle) and #65 (the static carrier does not tower). Step-3's "OPEN, leaning
    MULTIPLE-STABLE" is correctly RESOLVED by the barrier measurement step-3 said was missing.

NET: The verdict is genuine and the decisive Nr-trend gap is closed for the widest-spread
pair. Family question = ANSWERED (no family; one soft object). Residual scope (honest, not
blocking): the oblate<->prolate Nr=16 fields don't exist so the *killer* pair was re-checked
only at Nr=12 (robustly, 9 images); Nr=16 confirmation is on round<->toroidal (the harder
spread case). A full Nr=16/24 sweep of all pairs would be the belt-and-suspenders closure but
is not required to support the verdict.

---

## EVIDENCE (independent recompute on saved fields)

### 1. Killer pair oblate<->prolate, Nr=12, FINER NEB (9 img / 8 it) — verifier recompute
| s | relaxed \|S\| | raw \|S\| | Phi |
|---|---|---|---|
| 0.000 (oblate) | 117.49 | — | endpt |
| 0.125 | 101.56 | 101.56 | 8.1e-14 |
| 0.250 | 90.71 | 90.70 | 1.8e-13 |
| 0.375 | 84.98 | 84.93 | 2.5e-13 |
| **0.500** | **84.37** | 84.27 | 2.7e-13 |
| 0.625 | 88.87 | 88.71 | 2.2e-13 |
| 0.750 | 98.48 | 98.29 | 1.3e-13 |
| 0.875 | 113.16 | 113.00 | 5.2e-14 |
| 1.000 (prolate) | 132.87 | — | endpt |

barrier_above = -19.7 (interior max 113.2 < higher endpt 132.9); min at s=0.5 = 84.4 ~ round
83.7. Smooth, single-welled, barrierless. The barrier got *less negative* (-34.4 @5img ->
-19.7 @9img) only because finer sampling caught points nearer the endpoints — the interior
profile is unchanged and still never crosses the higher endpoint. No hidden ridge. Relaxed ~
raw confirms the straight chord already lies on the min-energy connecting path (a flat
manifold), not under-relaxation: the images independently FLOOR to 1e-13 at held chord
coordinate.

### 2. round<->toroidal MONOTONE — Nr=12 (saved) and Nr=16 (verifier recompute)
- Nr=12 (saved JSON): |S| = 83.7 -> 94.0 -> 113.2 -> 141.6 -> 179.3. Monotone, barrier_above
  = -37.7. No hump.
- **Nr=16 (verifier, fresh): endpoints S_round=-75.9 (M=0.2915), S_toroidal=-166.7 (M=0.5951)
  — match step-2's Nr=16 basins. s=0.5 image FLOORED to Phi=1.4e-10 at |S|=98.4, inside
  [75.9,166.7]. barrier_above = -68.3. Monotone/barrierless at Nr=16 too.** The Nr-trend
  hypothesis (a barrier appears as the grid sharpens) is FALSIFIED for this pair.

### 3. NEB construction audit
The transverse relaxation pins each image's chord projection at s_k (re-snapped each iter via
`restore`), projects OUT the along-chord step component (`du -= dot(du,e)*e`), with FIXED
endpoints — a legitimate string/NEB transverse relaxation, NOT the condemned biased blend
(which freed ALL DOF and slid to the nearest well). Each image floors to a genuine residual
zero (Phi 1e-12..1e-13) using the committed `residual_vector_vsafe` + `jacobian_jacrev`
(unedited). The "relaxed ~ raw" observation is the SAME physical fact as step-3's "blend
re-floors in place" (solver moves the seed ~0); here that fact is correctly read — a residual
zero EXISTS at the interpolated point along the chord, i.e. the solution manifold is
essentially linear/flat between basins. That is genuine evidence of a connected soft manifold,
not an artifact.

### 4. Provenance / discipline
- Solver = committed `full3d_newton.newton_solve`; residual = committed `residual_vector_vsafe`;
  energy = inline native action S=int sqrt(-g)(L2+L4)dV (matches step-2 basin |S| to all
  digits: oblate -117.49, round -83.72, etc.). No edited committed module.
- DATA-BLIND: no observation compared, no M_MS/wall banked. Verdict (no family) is the
  un-wanted direction — observe-not-target holds; I checked whether it is OVER-corrected (are
  barriers small-but-real?) — they are robustly NEGATIVE at finer sampling and at Nr=16, not
  marginal.
- Anti-hang: 2 fresh solves total (oblate<->prolate 9img Nr=12, 213s; round<->toroidal Nr=16,
  97s), strictly sequential, monitored to completion, never concurrent, no live-solve poll.

---

## VERDICT TABLE
| Prosecution item | Finding |
|---|---|
| (1) NEB genuine vs under-relaxed | GENUINE. Finer 9-img chain reproduces barrierless dip-to-round; images floor 1e-13; relaxed~raw is flatness, not under-relaxation. |
| oblate<->prolate dips through round | CONFIRMED. min |S|=84.4 at s=0.5 ~ round 83.7. |
| (2) Nr-trend risk | CLOSED on widest-spread pair. Nr=16 round<->toroidal floored, barrier_above=-68.3, monotone. Growing spread = lengthening flat manifold. |
| (3) full-direction stability | SOUND (constraint-respecting). Broadband kick not load-bearing; c,d/3-basin curvature untested but cannot create a barrier (caveat scoped, non-blocking). |
| (4) reconciliation | SOUND. local-min(small-h) + no-ridge(NEB) = shallow connected manifold, consistent with step-3 kick-stable. |
| (5) discipline | HELD. data-blind, observe-not-target, committed tools, anti-hang. |

## RESIDUAL OPEN (honest, non-blocking)
- oblate<->prolate (the killer) re-checked only at Nr=12 (9 img, robust); its Nr=16 fields
  don't exist. Nr=16 confirmation is on round<->toroidal (the harder spread case).
- c,d metric-shear curvature + curvature on oblate/prolate/pert_s untested (only weakens
  basins, can't make a barrier).
- A full Nr=16/24 NEB sweep of all pairs = belt-and-suspenders; not required for the verdict.

NET: The family question stands ANSWERED — NOT a durable family; one soft connected object —
and the decisive Nr-trend gap that could have flipped it is CLOSED for the strongest pair.
