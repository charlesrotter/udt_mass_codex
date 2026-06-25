# P5c-step-3 STABILITY — BLIND ADVERSARIAL VERIFIER

Verifier: claude-opus-4-8[1m] (independent blind adversarial). Date: 2026-06-20.
Branch: `p5c-stability`. DATA-BLIND (units L=1; no wall numbers banked; M_MS/|S| are
dimensionless geometric readouts only). Bounded recompute on SAVED p5c_basins /
p5c_stability checkpoints (Nr=12). Anti-hang held: single clean sequential processes,
each < ~2 min, dense-LM only, no background poll, no concurrent solve.

Target: `p5c_stability_results.md`, `p5c_stability.py`, `p5c_stability_coupled.py`;
context `p5c_basins_results.md`, memory [[gravitating-soliton-stability-test]],
`winding_platonic_phase3b_results.md`.

---

## HEADLINE

(a) **"Melt to round" is a BIASED-BLEND ARTIFACT, not dynamical instability. BROKEN.**
    The melt re-solve does NOT flow basin->round; it floors the hand-imposed convex
    blend essentially IN PLACE. Landed distance ≈ seed distance to ~0.001-0.015 in
    every one of the 12 (basin × s) cells. The classifier's "ROUND / OWN basin" label
    is purely which endpoint the chosen s put the seed nearer to, thresholded at 0.05.
    The deformation toward round was imposed by hand; the solver added ~nothing. The
    melt establishes NOTHING about the off-round wells' dynamical stability.

(b) **All five ARE local minima (in the tested directions), and round IS calibrated.
    CONFIRMED — and STRENGTHENED.** Independently reproduced Theta-Hessian n_neg=0 for
    round/oblate/toroidal (min eig 0.19-0.26 >> tol 5e-4). Round: n_neg=0 + small
    unbiased coupled kick returns (saved). NEW unbiased check the report did not run:
    a small coupled kick (amp 0.01, ALL DOF) on OBLATE RETURNED to oblate (d=0.023).
    Unbiased-return is now 3/3 tested basins (round, toroidal, oblate). Zero off-round
    basins have been shown to decay to round under an unbiased perturbation.

(c) **"Shallow metastable" is OVER-READ. Barriers are UNMEASURED, and the one piece of
    unbiased barrier evidence points the OTHER way.** No barrier height / NEB was
    computed; "shallow" rests entirely on the discredited melt. NEW: a LARGER unbiased
    kick (amp 0.03) on TOROIDAL flowed to PROLATE (another off-round basin), NOT to
    round. So round is not a universal sink; off-round basins border each other, and a
    larger perturbation crosses to a neighbor, not preferentially to round.

(d) **HONEST FAMILY VERDICT: the family question is STILL OPEN, leaning MULTIPLE-STABLE
    — NOT "round = the one particle."** The melt that supplied the "others decay to
    round" half of the "mixed/hierarchical" verdict is an artifact and must be struck.
    What survives is: five distinct charge-1 coupled fixed points, each a Theta-sector
    local minimum, each returning to itself under a small unbiased kick (3/3 tested);
    round is the lowest-|S| and most-regular among them (a real, separate fact from
    step-2). That is the signature of MULTIPLE genuine same-charge local minima with
    UNMEASURED barriers — an energy ORDERING, not a demonstrated decay hierarchy.

---

## EVIDENCE

### 1. THE MELT CRUX — biased-blend artifact (decisive)

Convex blend seed u_seed=(1-s)·basin+s·round, BC-repinned, then coupled re-solve.
Measured seed distances (recomputed on saved fields) vs the LANDED distances from the
saved melt JSONs:

| basin | s | seed (d_round, d_basin) | landed (d_round, d_basin) | report label |
|---|---|---|---|---|
| oblate | 0.25 | (0.130, 0.043) | (0.130, 0.043) | OWN basin |
| oblate | 0.50 | (0.087, 0.087) | (0.086, 0.087) | "round" |
| oblate | 0.75 | (0.043, 0.130) | (0.043, 0.130) | ROUND |
| prolate | 0.25 | (0.129, 0.043) | (0.129, 0.043) | OWN basin |
| prolate | 0.50 | (0.086, 0.086) | (0.086, 0.086) | prolate |
| prolate | 0.75 | (0.043, 0.129) | (0.043, 0.129) | ROUND |
| pert_s | 0.25 | (0.215, 0.072) | (0.212, 0.087) | pert_s |
| pert_s | 0.50 | (0.143, 0.143) | (0.141, 0.147) | round |
| pert_s | 0.75 | (0.072, 0.215) | (0.070, 0.218) | round |
| toroidal | 0.25 | (0.187, 0.062) | (0.188, 0.062) | toroidal |
| toroidal | 0.50 | (0.125, 0.125) | (0.125, 0.125) | toroidal |
| toroidal | 0.75 | (0.062, 0.187) | (0.063, 0.187) | ROUND |

The re-solve moves the field by ≤ ~0.015 (worst: pert_s) and typically < 0.003. The
blend itself moved it 0.04-0.22. So the apparent "melt to round" is ≈100% the
hand-imposed blend and ≈0% solver flow. Every blend point also re-floors to Phi~1e-13
(it is a near-fixed point of where the blend left it). "Melts to round at s=0.75"
reduces to "a seed placed 75% of the way to round (d≈0.04-0.06 < 0.05 threshold) stays
there." This is exactly the biased-blend trap the brief flagged. The monotone-M_MS
"melt" in §3 of the target is the linear interpolation's M_MS, not a decay.

NB this also quietly contradicts the "decays to round" reading internally: at s=0.50
toroidal AND prolate land back on their OWN basin (d_basin < d_round), not round —
because at s=0.50 the seed is equidistant and the solver doesn't move it.

### 2. Hessian + calibration (confirmed, reproduced)

Independent recompute on saved fields (`p5c_stability.fixed_metric_hessian`):
round n_neg=0 (min eig 0.2325), oblate n_neg=0 (0.2614), toroidal n_neg=0 (0.1863);
all >> tol≈5e-4. Matches saved JSONs to machine precision. Refloor its=0 / dfield=0
for all five (saved) — genuine coupled fixed points, no drift. Round small kick
(amp 0.01) returns d_self=0.029 (saved). Calibration sound; sign-correct.
CAVEAT (the report's own ATTACK #1, unresolved): this is the FIXED-METRIC, Theta-ONLY
Hessian. It cannot see metric-direction (a,b,c,d) instabilities. "Local minimum" is
established only in the Theta sector + along the sampled kick directions, NOT proven
over the full coupled mode space. A few-mode coupled (constraint-projected) Hessian
remains the missing rigorous check.

### 3. NEW unbiased coupled kicks (the sound evidence)

- oblate, amp 0.01 (all DOF, random, BC-repinned, coupled re-solve, 10 its):
  RETURNED to oblate, d_self=0.023, M 0.405->0.405, Phi 7e-13. (NEW; report only
  kicked round + toroidal.) => off-round basin is a genuine local attractor.
- toroidal, amp 0.03 (all DOF): FLOWED to PROLATE (d=0.217), M 0.541->0.548, NOT to
  round. (NEW.) => larger unbiased perturbation crosses to a NEIGHBOR off-round basin,
  not to round. Round is not a universal sink. Consistent with the report's own
  round->oblate at amp 0.05 (round also goes to a neighbor under a large kick): the
  large-kick dynamics is basin-to-NEIGHBOR, symmetric, NOT "all roads to round."

---

## DISCIPLINE AUDIT

- Constraint-respecting genuinely applied? YES for the probes (each is a full
  newton_solve). But the load-bearing "melt" CONCLUSION is methodologically void
  (artifact), so constraint-respecting machinery was applied to a test that cannot
  answer the question. The raw Theta-Hessian was correctly NOT used as the verdict.
- Round calibrated? YES (n_neg=0, kick returns). Sign anchor holds.
- Data-blind / observe-not-target? YES. No M_MS banked; mixed verdict reported as
  mixed. (The "triply-selected round" framing leans on the artifact, however — see
  below.)
- Anti-hang held? YES. All my checks single-process, sequential, <~2 min each.

The report's §4/§5 "round = dominant, broadest attractor; others = shallow metastable
side-wells decaying to round; stability is a THIRD criterion agreeing on round" is
NOT supported: its decay/shallowness half is the melt artifact, and its
broadest-attractor half rests on one large kick on round (->oblate) plus the artifact.
The genuine large-kick data (toroidal->prolate; round->oblate) shows round is NOT the
broad sink. The honest "third criterion" content is only: round is lowest-|S| (step-2,
re-stated) and all basins are kick-stable local minima — which does NOT privilege round
dynamically.

---

## NET / NEXT MEASUREMENT

Charles's family question after this test: **OPEN, leaning toward a multiplicity of
genuine same-charge local minima** (5 coupled fixed points, all Theta-local-minima, all
unbiased-kick-stable where tested 3/3), ordered in energy with round lowest. The test
did NOT show the off-round objects decay to round; that claim was a biased-blend
artifact. Nothing here collapses the family to one particle, and the unbiased dynamics
(basin->neighbor under larger kicks) actively argues against a round-as-universal-sink
picture.

Decisive next measurements (in order):
1. **Barrier heights via NEB / string** between round and each off-round basin (and
   between off-round neighbors, e.g. toroidal-prolate). This is THE missing quantity:
   high barrier => genuinely distinct stable objects (a family); low barrier =>
   metastable. Until measured, "shallow" is unsupported.
2. **Few-mode coupled (constraint-projected) Hessian** over (a,b,c,d,Th) per basin, to
   confirm n_neg=0 in the FULL space, closing the Theta-only gap.
3. **Unbiased small kicks on the remaining basins** (prolate, pert_s) for 5/5 coverage,
   and a kick-amplitude sweep to map each basin's escape radius (the real "depth"
   proxy) — NOT a blend toward a chosen endpoint.

Strike the melt result from the inherited record; do not let "round triply-selected /
others decay to round" propagate to the selection-principle step. Round's selection,
if any, stands ONLY on lowest-|S| (an ordering, energy-minimization candidate), not on
demonstrated dynamical dominance.
