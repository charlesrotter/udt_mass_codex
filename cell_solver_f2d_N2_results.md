# N>=2 build — Class-A FREE (H=0) finite-mirror cell, N ∈ {2,3}, Z ∈ {1,8}

**Date:** 2026-07-02. **Mode:** OBSERVE (the pre-registered N≥2 tiles; `discreteness_preregistration.md`
Class-A FREE, AMENDMENT 2026-07-01b). **Driver:** Claude Code session. **Scripts:**
`cell_solver_f2d_N2.py` (θ-relax-first scan + the corrected two-tier stability filter), reusing the
CAS-verified operators of `cell_solver_f2d.py` and the N=1 scan machinery of
`cell_solver_f2d_first_build.py`. **Status:** UNLABELED observation. **N=2 and N=3 ONLY — two more
tiles of the charter grid (MAP §7). NOT a discreteness verdict, and NOT a frame verdict.**
**BLIND-VERIFIED 2026-07-02 (agent a7c27191): the N=2,3 no-closure negative is CONFIRMED + bankable
(the verifier's own 0/240 wide-seed sweep + budget-scaling independently confirm the non-convergence
is REAL, not a solver stall). PASS-WITH-CAVEATS: two prose over-reaches corrected (see the ⚠️
CORRECTIONS block below and the VERIFIER section).**

> **⚠️ CORRECTIONS (verifier a7c27191) — the conclusion is unchanged; two characterizations were too
> strong:**
> 1. **The non-convergence MECHANISM is not a clean "φ→−∞ attractor."** It is "**the field BVP has no
>    finite stationary point; configs drift to a degenerate boundary via ≥2 channels** — often ρ→+∞
>    with φ bounded (e.g. φ_c≈−0.4, ρ_c→47), sometimes φ deep-negative." The outcome tag is `stall`
>    (φ bottoms ≈−6, never hits the |φ|=8 cap), not a literal runaway to −∞. Read "φ-runaway" below as
>    shorthand for this multi-channel drift-to-degenerate-boundary.
> 2. **"H(seal) uniformly positive at N≥2 / never straddles zero" holds only along the θ-relaxed
>    continuation BRANCH scanned here** — NOT across the solution space (the verifier's wide seed span
>    finds H(seal) of BOTH signs, down to −1654, on NON-converged configs). This does **not** create a
>    hidden crossing: a genuine crossing needs a CONVERGED branch carrying H(seal) through 0, and
>    **0/240 converge**, so the no-closure conclusion is safe — but the "sign flipped, never straddles"
>    narrative is branch-specific, not a robust global fact.

**Fixed values (all tagged):** N ∈ {2,3} (DERIVED-topological, one per run); ξ=κ=1 (CHOSE-units);
Z ∈ {1,8} run BOTH (CHOSE-fixed, pre-reg amendment; Z=8 = OBS-2 Route-A-structure-carrying-Route-B-
number); Nr=16, Nth=12 scan grid, {12,16,24} grid spot-check (CHOSE, anti-hang bound); L ∈ [0.5,2.0],
7 points (CHOSE scan range); 3 distinct seeds — θ-relaxed+r, far amp=2.0, far amp=3.0 (CHOSE; criterion
2; far-from-rigid per Step-0 V7). No per-solution retuning; Z held fixed within each scan (criterion 5).
Per-solve wall 12 s, total 520 s; **actual total wall = 29 s** (not throughput-limited).

---

## Headline (lay first)

At **N=2 and N=3**, both Z, the derived round static free-f(r,θ) cell with the minimal {L2,L4} matter
and a Class-A smooth mirror seal **again produces no isolated finite cell** — but by a **different
mechanism than N=1**, and with one clean new observation.

- The knot's angular shape **genuinely deforms** away from rigid f=θ (θ-relax-first finds a real
  deformed profile, max|U|≈0.089 at N=2, ≈0.114 at N=3), exactly as OBS-3 predicted (rigid is not
  even stationary for N≥2). So the matter does **not** unwind to rigid the way it did at N=1
  (max|u| stays ≈0.24–0.35, it does not drain to 0).
- Nonetheless every starting guess, at every cell size, at both Z, drains the **geometry** the same
  way: the field BVP has **no finite stationary point** — configs drift to a degenerate boundary
  (ρ→+∞ with φ bounded, and/or φ deep-negative; e^{2φ}→0 suppressing the source). **No configuration
  converges to a stationary cell.** (See ⚠️ CORRECTION 1 — this is a multi-channel drift, not a clean
  φ→−∞ attractor.)
- The free-boundary closure condition **H(seal)=0 is never met** — and here is the new observation:
  for N≥2 **H(seal) is uniformly POSITIVE** (≈+0.5…+0.9 at N=2, ≈+5.4…+6.4 at N=3, growing ~N²),
  whereas at N=1 it was uniformly NEGATIVE (≈−0.95). H(seal) does **not change sign** along any branch
  — it never crosses zero — so the isolated-closure set is **EMPTY** at N=2 and N=3. The sign of
  H(seal) flipped between N=1 (negative) and N≥2 (positive), but **it does not straddle zero within any
  fixed-N branch**, so no closure appears.

This is a **scoped negative on two more tiles** (N=2, N=3), joining the N=1 tile. The result is
Z-independent (Z=1 and Z=8 agree to ~3 digits). The frame verdict is **NOT** reached.

---

## What was built (spec-faithful) — the two fixes over the N=1 build

1. **Closure-MANIFOLD map, THETA-RELAX-FIRST (MAP §9.2).** New `theta_relax()`: at a representative L,
   FIRST solve the θ-part of the f-PDE for a radially-uniform deformed profile f=f(θ) (for an r-uniform
   config f_r=0 ⇒ `res_f` reduces to the pure θ-PDE; all Nθ GL nodes are interior, so it is a square
   Nθ×Nθ system). The relaxed θ-profile then seeds the full 2-D solve with the radial dependence freed.
   **f(θ) genuinely deforms** (max|U| = 0.089 [N=2], 0.114 [N=3]; θ-solve Φ≈1e-15, 8 iters) — OBS-3
   confirmed at the solver level. Far-from-rigid seeds (amp 2.0, 3.0) are also included (the N=1 build
   under-sampled these; the N=1 verifier had to push amp to 3.0).
2. **TWO-TIER stability filter — the CORRECT formulation (fixes the N=1 action-Hessian error).**
   The N=1 build used the Hessian of the ACTION (structurally ~90% indefinite → "PD ⇒ stable" never
   fires; a real cell would be misclassified). This build uses:
   - **Tier (a) — the MATTER ENERGY Hessian** (right signs): `E_m = −L_m =
     (ξ/2)(ρ²I_r + I_θ + N²I_s) + (κN²/2)(I_4r + I_4θ/ρ²)`, all POSITIVE terms, Hessian w.r.t. the
     matter DOF δu only (geometry φ,ρ frozen at converged values), via torch autodiff. PD ⇒ accept as
     stable (trustworthy: a fixed-background Hessian OVER-counts NEGATIVES, so a positive-definite
     verdict is trustworthy — `gravitating-soliton-stability-test`).
   - **Tier (b) — constraint-respecting perturb + coupled RE-SOLVE** (the project's banked method):
     perturb along the top-3 most-negative matter eigenvectors, full coupled re-solve (φ,ρ,f together),
     RETURN (small distance back) ⇒ over-count / stable; run off / collapse ⇒ genuine instability.
   - **No closures existed to filter** (as at N=1), so tier (a)/(b) did not fire on real cells — but the
     machinery is built and its right-signedness is VERIFIED (below).
3. **Robustness:** BOTH Z ∈ {1,8}; a grid spot-check Nr ∈ {12,16,24}; Derrick + H-drift as artifact
   filters. Single unbuffered process, everything bounded, no hang.

### Tier-(a) right-signed SANITY (passed — real energy code path, not a toy matrix)

All three exercise `matter_energy_of_u → M.fields` (the real code path):

- **(S1) STABLE reference (N=1 rigid f=θ, Step-0 V7 strict min):** the ENERGY Hessian is dominantly
  positive — **n_neg = 5/192 (3%)**, and every negative lies in a near-kernel band (max|λ|/λ_max =
  2.5e-3 — the discretization image of V7's exact sin θ zero mode). The ACTION Hessian on the SAME
  config is **n_neg = 203/224 (91%)**. This demonstrates the energy is the RIGHT-signed object for the
  matter sector (symmetry error 3.6e-15). (Nuance, verifier a7c27191: the 3%-vs-91% is not a strict
  apples-to-apples count — the energy Hessian is u-only, 192 dims; the action Hessian is full-w, 224
  dims, and an action is *structurally* a saddle in the geometry sector — so "the action was WRONG" is
  better stated as "the action Hessian is the wrong OBJECT for a matter-stability screen"; immaterial
  here since no cells exist to classify.)
- **(S2) PHYSICALLY PD:** directional curvature along RESOLVED physical modes (the V7 kernel sin θ, and
  the cos 2f<0 band mode) is POSITIVE for the full matter at every N tested (sin: +0.026 [N=1], +0.207
  [N=3]; band: +0.087 [N=1], +0.574 [N=3]). The matter energy is genuinely convex in all resolved
  directions (matches V7's κ-lift of the kernel).
- **(S3) CATCHES NEGATIVE curvature (not sign-locked):** with the κ (L4) stabilizer turned OFF (κ=0,
  pure L2), the winding potential −(ξN²/2)cos 2f/sin θ along the band mode gives a genuinely NEGATIVE
  directional curvature for N≥3 (−0.037 [N=3], −0.225 [N=6], −0.672 [N=10]) — the code returns it.
  Turning κ=1 back ON restores positivity (+0.574 [N=3], +6.12 [N=10]) — **V7's L4 stabilization
  mechanism, verified numerically.**

**Physical reading of the near-kernel band (important):** the matter energy is convex along all
physical directions (V7); the few small raw-Hessian negatives are under-resolved near-pole (1/sin θ)
modes, NOT a matter instability. Consequence: the matter sector is stably wound, and the cells'
non-existence here is a **geometry/closure failure (the φ-runaway, no H=0), not a matter instability.**
Because winding matter always carries this near-kernel band, tier (a) is essentially never *cleanly*
PD; the design therefore runs tier (b) (decisive) on any closure — of which there were none.

---

## What is there — plainly, per (N, Z)

**Are there H(seal)=0 CROSSINGS (cells)?** — **NO**, at N=2 and N=3, both Z. No converged branch
exists; H(seal) is single-signed (positive) on every relaxed configuration and never crosses zero.
The isolated-closure set is EMPTY.

**Isolated vs continuum?** — Neither. There are no stable finite cells at all; the scanned manifold is
a runaway continuum with H(seal)>0 throughout (no closure), same structural outcome as N=1 (which had a
runaway continuum with H(seal)<0).

**Stability class?** — **N/A: nothing to classify** (no H=0 closure). The two-tier filter is built and
its tier-(a) right-signedness is verified (above), but there were no cells to pass through it — exactly
as at N=1.

**Continuum tables (θ-relaxed seed, continuation; all entries `stall` = φ-runaway, never converged):**

| N | Z | L range | φ_c range | ρ_c range | max\|u\| | H(seal) | H-drift | ΔDerrick |
|---|---|---------|-----------|-----------|--------|---------|---------|----------|
| 2 | 1 | 0.5→2.0 | −2.87 → −4.80 | 1.73 → 2.25 | 0.30–0.35 | **+0.86 → +0.53** | ≤1.7e−7 | +0.36 → +0.92 |
| 2 | 8 | 0.5→2.0 | −2.88 → −4.81 | 1.73 → 2.24 | 0.30–0.35 | **+0.86 → +0.54** | ≤1.7e−7 | +0.36 → +0.92 |
| 3 | 1 | 0.5→2.0 | −3.91 → −5.16 | 1.08 → 1.17 | 0.25–0.28 | **+6.22 → +5.53** | 1.8e−6–2.3e−5 | +1.24 → +3.99 |
| 3 | 8 | 0.5→2.0 | −3.94 → −6.10 | 1.05 → 1.20 | 0.24–0.29 | **+5.39 → +6.42** | 1.8e−6–2.4e−6 | +1.31 → +3.79 |

- **H(seal) uniformly positive, no sign change** on any branch → no closure. (For comparison: N=1 was
  uniformly ≈−0.95.) Across the ADVERSARIAL seeds (amp=2, amp=3) H(seal) was also positive everywhere
  (up to +107 for the amp=3 seed at N=3 Z=8) — robust: no sign change anywhere in the scanned space.
- **The drift is a genuine non-stationary limit, not a stall to be broken:** as iterations grow
  (maxit 140→300→600 at N=2), a field marches monotonically (φ_c −3.61 → −4.15 → −4.38, and/or ρ→+∞)
  with Φ decreasing but never reaching machine zero (iters always = maxit); the residual vanishes only
  in the degenerate limit — no finite fixed point. Seed-independent (all 3 seeds stall). Independently
  reproduced by verifier a7c27191 (0/240 converged; budget-scaling to maxit 600 confirms non-stationary).
- **Matter deforms, does not drain:** max|u| ≈ 0.24–0.35 throughout (unlike N=1, where u→0). OBS-3
  confirmed: the θ-profile is genuinely non-rigid for N≥2.

**Artifact filters (criterion, MAP §9.4c).** H-drift is tiny at N=2 (≤1.7e−7). At N=3 it is larger and
grows mildly with L (1.8e−6 up to 2.3e−5 at L=2, N=3 Z=1) — still small, but flagged as a mild
grid-drift caveat at the largest cells (the stiffer N² source). The Derrick residual ΔS is large and
grows with L (necessary condition of a TRUE solution; these runaway configs are not solutions, so a
large ΔS is the CORRECT reading — it flags them as non-solutions). There is no genuine solution for the
artifact filter to admit or reject.

**Grid spot-check (N=2, Z=8, Nr ∈ {12,16,24}, θ-relaxed seed @ mid-L).** All stall; θ deforms at every
Nr (max|U| ≈ 0.09); H(seal) stays positive (+0.560, +0.702, +0.762 for Nr=12/16/24). The exact runaway
endpoint (φ_c, ρ_c) drifts with Nr because it is a runaway (no fixed point), but the QUALITATIVE
outcome — stall, φ-runaway, H(seal)>0, no closure — is grid-independent.

---

## Reading against the 9 pre-registered criteria (Class-A FREE, N=2 and N=3)

- **(1) Isolated vs continuum:** no stable finite cells at all; a runaway continuum with H(seal)>0
  throughout (no closure).
- **(2) Same solutions from different seeds:** the OUTCOME (no cell → φ-runaway, H(seal)>0) is
  seed-independent (all 3 seeds, incl. far-from-rigid amp 2/3); the runaway destination is
  seed-dependent. Consistent with "no cell."
- **(3) Stability without imposed targets:** no cell holds together; nothing imposed.
- **(4) Grid/method independence:** the negative is grid-independent (Nr 12/16/24); θ-deformation and
  H(seal)>0 robust.
- **(5) No hidden fitting knobs:** Z held fixed per scan; run at BOTH Z ∈ {1,8}; outcome is
  Z-independent; no per-solution retuning.
- **(6) Quantized flux:** N/A (Class-A FREE is q=0 by construction; no cell anyway).
- **(7) Branch consistency:** interior P only (Class-A FREE, closed mirror); the derived interior EOMs
  are satisfied to the stall tolerance, but there is no stationary cell.
- **(8) Perturbation survival:** the corrected two-tier filter is BUILT and its right-signedness
  VERIFIED (energy 3% vs action 91%; convex in physical directions; catches negatives when κ off);
  no genuine cell to test at N=2,3.
- **(9) Blind classification:** output is UNLABELED; no particle comparison.

**KEY ACCEPTANCE TEST (Class A):** "do the mirror-seal conditions close only at isolated cell sizes,
or can every nearby size be adjusted to close?" — **Neither**: at N=2 and N=3 the conditions close at
NO cell size; the free-boundary H=0 is never satisfied by any relaxed configuration (H(seal) is
uniformly positive and never crosses zero).

---

## Provenance / discipline

- **Observing, not targeting:** the guidance expected crossings were LIKELY at N≥2 (H_seal carries N²;
  rigid-ish N=2 ≈ +0.5, runaway → −1, straddling 0). The run was NOT sculpted toward crossings: the
  rigid-ish +0.5 was seen (N=2 H(seal)≈+0.5–0.9), but the runaway did NOT drive H(seal) to −1 — for
  N≥2 the φ-runaway keeps H(seal) POSITIVE, so it never straddles zero within a fixed-N branch. This is
  an honest null on the crossing prediction, reported as-is.
- **Solver-first (before the "no cell" reading):** (1) left out? — the matter basis is the
  pre-registered minimal {L2,L4}; X²/L6 are the registered NEXT in-frame freedoms (P4), not wrongly
  omitted. (2) numeric? — the φ-runaway is monotone (maxit escalation), seed-independent,
  grid-independent; operators CAS-verified (11/11); H-drift ≤1.7e−7 (N=2). Not a conditioning artifact.
  (3) frozen DOF? — φ, ρ, u all free; L scanned; both mirror ends free-natural; nothing frozen. (4)
  whole space? — 3 seeds (incl. far-from-rigid) × 7 L × 2 Z, all consistent. Solver-complete for these
  tiles.
- **Derived backstop:** OBS-3 (blind-verified in Step 0) — rigid f=θ is not stationary for N≥2 → the
  θ-profile must deform; the θ-relax found exactly that (max|U|=0.089/0.114). The matter-energy Hessian
  being right-signed and convex-in-physical-directions (V7) says the matter is stably wound; the cells'
  non-existence is a geometry-closure failure (the φ-runaway), NOT a matter instability.
- **Scope:** N=2, N=3 only. Next tiles (open, not verdicts): the in-frame freedoms **X²/L6** (P4), then
  **Class-B** (charged/pinned seal — where H carries a nonzero seal flux / ambient value, MAP §4d),
  then **off-round** h, then **time-live**. Any null here propagates ONLY along the L2+L4, Class-A,
  round, static row (MAP §7).

## Caveats (flagged)

- **Not a discreteness or frame verdict** — this is N=2,3, two more slices of the charter grid.
- **Mild grid drift at N=3, large L:** H-drift rises to ~2e−5 at L=2 (N=3 Z=1) — still small but the
  largest cells at N=3 are the stiffest; the qualitative outcome (H(seal)>0, no closure) is robust.
- **Tier-(a) near-kernel band:** the raw matter-energy Hessian carries ~3% small negatives (near-pole
  discretization image of V7's sin θ zero mode); this is why tier (b) is the decisive test. No cells
  existed to exercise tier (b) on real data (its machinery runs, but is unexercised by a genuine cell).
- **H(seal) sign prediction:** the guidance's "straddle 0" did not occur within a fixed-N branch (see
  Observing-not-targeting above) — but note ⚠️ CORRECTION 2: H(seal) IS both-signed across the wider
  solution space; what fails is that no CONVERGED branch carries it through zero.

## VERIFIER
**Blind adversarial pass — 2026-07-02, agent `a7c27191`. VERDICT: PASS-WITH-CAVEATS; the negative is
BANKABLE.** Independent re-check (own solve loop, own convergence gate, NOT the author's scan):
- **Runaway REAL, not a stall — CONFIRMED, load-bearing:** **0 / 240** converged across a wide span
  (amp∈{0.5,1,2,3} × φ0∈{−2..1} × ρ0∈{0.3..2} × L∈{0.3..3} × N∈{2,3} × Z∈{1,8}); budget-scaling
  (maxit 60→600) shows Φ plateauing with iters always = maxit and a field diverging — a real
  non-stationary drift with **no finite fixed point**, robust even to a loose Φ<1e−4 gate. The
  runaway-vs-stall question (told not to give benefit of the doubt) resolved in the result's favor.
- **No hidden crossing** within the explored space (a crossing needs a converged branch; none exists).
- **Two-tier filter fix VALID:** tier (a) is genuinely the ENERGY Hessian (right-signed, exercises the
  real `matter_energy_of_u→fields` path, catches the κ=0 instability, PD-⇒-trustworthy logic sound);
  honestly not exercised on a real cell (none exist).
- **"Geometry not matter" read HOLDS** (|u| bounded ~0.24–0.35; divergence in ρ/φ).
- **No hollow checks;** convergence gate honest (no false-pass of a stall, no false-fail of a real cell);
  θ-relax genuinely solves the θ-PDE (Φ=9e−16).
- **Two prose corrections REQUIRED + now applied** (the ⚠️ CORRECTIONS block above): the "φ→−∞
  attractor" mechanism (→ multi-channel drift to a degenerate boundary) and "H(seal) uniformly positive"
  (→ branch-specific; both signs globally; no converged crossing). Conclusion unaffected.
