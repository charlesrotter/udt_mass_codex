# Branch-P solver floor + X-continuation — solver INTEGRITY arc + the X premise + no static localization

**Driver:** Claude (Opus 4.8, 1M). **Dates:** 2026-06-23/24. **Mode:** OBSERVE, DATA-BLIND.
**Status:** SOLVER-INTEGRITY result (continuation fix) + a PREMISE catch (X=−2e5 chosen) + a SCOPED
physics negative (no interior localization on static Branch P, even with φ unthrottled). NOT a
final physics verdict — Nr=10 coarse; static only.

**New scripts (committed with this doc; reuse the immutable `branchGP_native_s2_coupled_OBSERVE.py`
+ `jfnk_branch_solver.py` verbatim):** `jfnk_floor_driver.py`, `jfnk_P_dilation_diagnostic.py`,
`equilibrated_lm_floor.py`, `probe_phi_terms.py`, `x_continuation.py`, `sharpen_localization.py`.
Logs: /tmp/jfnk_{G,P}.log, /tmp/jfnk_P_diag.log, /tmp/equil_P.log, /tmp/jfnk_equil_P.log,
/tmp/probe_phi.log, /tmp/xcont.log, /tmp/sharpen.log. Fields: /tmp/uP_X*.pt.

## Frontier on entry
The LIVE next-action: FLOOR the JFNK matrix-free coupled solver — switch from `pc='none'` (stalled
near Φ≈4 on Branch G) to `pc='jacobi'`, then floor the stiff Branch P (does native matter localize /
select a scale on the untried φ-angular branch, or stay the 1/r² defect?).

## What ran, in order (each a bounded single GPU process; no solve delegated to an agent)

1. **JFNK pc='jacobi' broke the stall.** Branch G: Φ 1.7e5 → **2.75** in 7 Newton iters (wall-capped
   mid-descent, NOT stalled) — well below the old `pc='none'` Φ≈4 floor and below dense-LM's 37.
   Branch P first floored to **8.67** (jfnk_floor_driver.py / jfnk_P.log). **That "P stalls at 8.67" was
   a STOCHASTIC-PC artifact** — the Jacobi PC uses unseeded Hutchinson probes (jacobi_pc, torch.randn);
   a second draw (the floor inside jfnk_P_dilation_diagnostic.py / jfnk_P_diag.log) reached **3.49**,
   still descending. P is NOT meaningfully stuck vs G.

2. **Stall/dilation diagnostic (jfnk_P_dilation_diagnostic.py).** At the P floor: gradient JᵀF small
   but not zero (still descending, not a clean critical point); **cond(J)~1e10** (σ 1.5e-4..2.5e6),
   with the irreducible residual on the **interior Einstein E_TT (0.50), E_RR (0.31)** rows, 0 on BC
   rows. The "stall = scale modulus" hypothesis was **REFUTED**: the dilation generator d=−r∂_r u is
   NOT the flat mode (overlap with smallest right-singular vectors ~0.09; Φ(u+εd) a sharp well). So
   the wall is conditioning on the diagonal Einstein equations, not a physical modulus.

3. **Ruiz equilibration (equilibrated_lm_floor.py).** 2-sided row+col scaling cut σmax 2.5e6 → 13.5.
   **KEY:** once equilibrated, the interior-Einstein residual → **0** and the residual moved entirely to
   **EL_φ (0.98–1.00)**. => the Einstein "obstruction" was a **SCALING artifact**, NOT under-resolution
   and NOT a missing term. The Einstein sector is sound. (The dense-LM globalization then STALLED at
   Φ=569 on the now-dominant φ-equation; JFNK's inexact-Newton reached 3.49 — the dense LM was the weak
   link, not the conditioning.)

4. **φ-term decomposition (probe_phi_terms.py, no solve).** EL_φ on Branch P is a delicate balance
   **2X·div(φ) ≈ 2U'(φ)**, U'(φ)=2e^{2φ}, with the curvature/matter piece `alg` small (O(1–7)). With
   **X=−2e5**, φ's required curvature is div≈U'/X≈1.4e-4 — TINY — so φ is forced ~flat (~1e-5), and
   EL_φ ≈ X·(φ-curvature discretization error): a **singularly-stiff** equation. At the best floor
   (probe_phi.log, field uP_stall): |alg|=7.5, |2X·div|=54.9, |2U'|=55.4 cancel to |EL_φ|=0.0225 —
   catastrophic cancellation of two O(55) terms. (Blind Ruiz col-scaling lifts the tiny-φ columns to a
   column scale ~206 vs ~9e-4 elsewhere → over-aggressive φ steps → it floored WORSE, Φ=8421:
   jfnk_equil_floor.py.)

5. **Infrastructure audit (provenance of X).** **X=−2e5 is CHOSEN, not derived.** The UDT weight
   derivation (R1–R3) pins only the e^{2φ} exponent and that X is large-negative (no-ghost + the
   *imported* Cassini PPN bound |X−8|>1.74e5); within the half-line **nothing internal fixes the value**
   — −2e5 is "the smallest round number clearing Cassini," tagged `FREE`/`CHOSE` (branch_operator.py:85,
   branch_G_characterization §3, native_dilation_weight §9). φ's response (and the derived hair charge)
   scale as **1/|X|**; a prior X-scan (branch_P_characterization_results.md:94) shows φ develops
   structure at modest |X| and is throttled flat at −2e5. => the "scale-free" verdict was
   **X-conditioned**, and the same huge X (7-decade spread vs ξ,κ~2e-2) IS the solver stiffness. One
   root cause. (Honest caveat from the audit: Cassini legitimately forces large |X| in the *weak-field
   LOCAL* regime; whether the deep inside-matter regime, exp(−2φ₀)~5, shares that X is OPEN.)

6. **Continuation in X (x_continuation.py) — the fix that doubles as the probe.** Warm-started up a
   geometric ladder X=−3 → −2e5. **Floors every rung in ~2 iters, including −2e5** (where the cold seed
   is stuck at Φ=2720). φ unthrottles as |X| drops (depth 0.05 at −2e5 → 0.89 at −3; the cold-seed −2e5
   field is shallower still, ~0.002), confirming 1/|X|
   throttling live. Warm-started continuation reaches a MORE-structured branch the cold seed misses.

7. **Sharpen + interior/edge + multi-branch (sharpen_localization.py).** Tight floors (X=−1e3 → Φ=0.068;
   X=−2e5 → Φ=0.18) + FULL radial profiles. **The continuation's "extra structure" is BC-driven
   BOUNDARY LAYERS, not an interior body:** at −2e5, φ = −0.40 at the core (r=0.10) and ≈+0.44 just
   inside the seal (r=7.86)→0 at the pinned seal, but only ~0.01–0.04 across the physical body (r=2.1–6.1);
   proper-energy is U-shaped/edge-spiked over the body, NOT an interior max declining both sides. These
   are the boundary layers of a singularly-perturbed BVP (large X × highest derivative). M_MS=750/AB=8.3
   are dominated by the (under-resolved) boundary layers in the core/seal buffer zones.

## Verdict
- **SOLVER FIXED:** continuation-in-X navigates the φ-stiffness that beat every cold-started solver
  (cold −2e5: Φ=2720; continuation −2e5: Φ=0.18). Reusable.
- **PREMISE CAUGHT + ARTIFACT-WORRY CLOSED:** X=−2e5 is a chosen placeholder that throttles φ ∝1/|X|;
  but **unthrottling φ (continuation) does NOT reveal a hidden localized body** — φ's response goes into
  BC boundary-layers; the **physical body stays a featureless ~1/r² defect**. So "static Branch P =
  scale-free defect, no interior localization" SURVIVES, now understood (boundary-layer response, not a
  self-bound core) rather than asserted.
- **EVIDENCE SCOPE (honest):** the flat-Derrick scale-invariance test (M_MS≈1.358–1.362 across a 3× s
  range, jfnk_P_diag.log) was run on the DEFECT field (Φ=3.49), not on the continuation/boundary-layer
  field. The "continuation body stays a flat defect" conclusion rests on the edge-pinned SHAPE of its
  (4-node, under-resolved) body profile, not on a Derrick test of that field — two evidence streams,
  two different fields.

## Premises (scope of the negative)
Nr=10/Nth=6/Nps=8, cell=8, rc=0.1 (COARSE — boundary layers ~1 node wide, UNDER-RESOLVED; magnitudes
AB/M_MS grid-dependent, the qualitative shape-read is robust). STATIC only (the φ-angular hunch's home
is TIME-LIVE — untested). X=−2e5 chosen (re-graded across the healthy half-line via continuation; the
deep-regime X is OPEN). DATA-BLIND. Native S² L2+L4 matter, derived Branch-P operator, gtw free at both
ends. Multi-branch "distinct" = continuation reaches a floorable boundary-layer state the cold seed
cannot (Φ=0.18 vs 2720), not two clean physical branches.

## CONDITIONS-CHANGED reopeners
A grid refinement (Nr=16/24, resolved boundary layers) that turns the flat body into a peaked interior
core; OR a deep-regime derivation fixing X≠−2e5 that un-throttles φ into a self-bound body; OR the
TIME-LIVE native S² producing a localized object the statics cannot.

## Forward
Static instruments on BOTH branches now say scale-free defect (no interior localization), with the
solver trustworthy and the X-premise retired. Per LIVE.md the φ-angular discreteness hunch's one
untested instrument is the TIME-LIVE / non-stationary native S². (Optional firming: Nr=16/24 grid
refinement to close the coarse-grid caveat on the boundary-layer reading.)

## Verifier
Blind adversarial pass (agent a7456ae7e3f520d1e, zero-context, 2026-06-24): **PASS-WITH-FIXES**.
Re-derived the numbers against the logs: floors (G→2.75, P→3.49), cond~1e10, E_TT 0.50/E_RR 0.31,
σmax 2.5e6→13.5, residual→EL_φ, X_PROD=−2e5 FREE (branch_operator.py:85), sharpen profiles
(M_MS=750, AB=8.3, φ core=−0.40/seal=+0.44), the unseeded jacobi_pc, all CONFIRMED. Independent
support: the Derrick curve is flat on the defect field. **Overclaim check: PASS** — the negative is
explicitly scoped (Nr=10 coarse, static-only, X-conditioned, under-resolved layers, "multi-branch ≠
two clean branches"). Fixes APPLIED before commit: (1) φ-depth at −2e5 corrected 0.005→0.05 (was the
cold-seed value); (2) probe_phi magnitudes captured to /tmp/probe_phi.log (re-run, verifiable); (3)
the 3.49 floor re-cited to jfnk_P_dilation_diagnostic.py (jfnk_floor_driver.py gave 8.67); (4) added
the Derrick-on-defect-field evidence-scope note; (5) "206×" reworded to "column scale ~206". No
overclaim found; verdict STANDS post-fix.
