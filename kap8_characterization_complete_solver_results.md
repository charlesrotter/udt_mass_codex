> **⚠ QUARANTINE / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — DO NOT CITE AS A NATIVE-MICRO RESULT.**
> This doc's banked "native identification" (a core-concentrated degree-1 S² winding defect in a gentle dilation
> well; not a horizon, not a localized particle, not a clean monopole) was computed by RUNNING the PRE-NATIVE
> SCALAR-TENSOR operator (φ-outside-g, f=e^{2φ}, e^{2φ}-weighted matter, X=−2e5) via
> migration_convergence_guard.py → p1_residual → branch_operator.py. That frame was SUPERSEDED 2026-07-01 by the
> native constrained-two-player operator (∂_r(√h Z_φ φ')=−2√h·e^{−2φ}·𝒦̂; EH-empty, φ-BLIND matter, geometric 𝒦
> source). The object identification does NOT transport to the native operator and must be RE-RUN there before use.
> The convergence/horizon caveats and blind-verifier passes validated the run UNDER THE WRONG OPERATOR. Registry:
> NEGATIVES_REGISTRY #77. Saved-field follow-ups (check_winding_survival, caveat3_offdiag_off_control,
> ponder_horizon_signatures, native_object_characterization) INHERIT this quarantine.

# kap8=1 characterization on the COMPLETE static solver — results

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-27. **Mode:** OBSERVE / characterize. DATA-BLIND.
**Status:** PARTIAL — recorded with caveats per the blind verifier (NOT-CLEAN as first framed; the
over-claimed "divergence cured" headline is REJECTED; the narrow honest statement is banked instead).

## What was run
The completed static solver — derived scalar-tensor operator, **off-diagonal metric DOF live**
(e_rt/e_rp/e_tp), **native-S² 3-component matter** (free core, no Θ pin; grid-exact dθ via
`spectral_sph_exact`) — at the DERIVED strong coupling **kap8=1**, via the reframed
`migration_convergence_guard.py` (CHARACTERIZER, not a pass/fail filter). Seed = `seed_round_native`
(round metric + canon degree-1 winding n=x/r). Continuation in X to the production −2e5. Grids Nr=8,10
(Nθ=6, Nps=8). Both branches G and P, run SEQUENTIALLY (one process). Total wall ~40.9 h.

## Raw numbers (the data — these are solid)
```
                     Nr=8 warp   Nr=10 warp   trend    residual Phi (8 -> 10)
OLD (incomplete:                                        (for comparison; CONFOUNDED — see caveat 3)
  diagonal-only +                3.98     ->   8.42     x2.12   floored ~1e-12
  imported S^3 matter)
NEW Branch G:        1.022    ->  1.181            x1.16   9.1e-22 -> 7.2e-10
NEW Branch P:        2.530    ->  2.866            x1.13   4.7e-12 -> 3.3e-12
```
warp = max|a,b,c,d| (the diagonal metric warp). Both NEW branches FLOORED their residual to ≤1e-9 at
both grids (numerically converged solves). Branch-G Nr=10 took ~13.7 h; Branch-P Nr=10 ~20 h.

## What this DOES establish (narrow, honest — the banked claim)
With the completed operator (off-diagonals live) and native-S² matter, the kap8=1 solve **floors its
residual at both Nr=8 and Nr=10 on both branches**, with a metric warp that grows only **mildly
(×1.13–1.16)** across the two grids — **much less than the ×2.12** of the earlier S³/diagonal-only run.
The complete solver is numerically healthy at the derived strong coupling on both branches. Branch P
(scale-breaker potential, drives φ deep) settles at a larger warp (~2.5–2.9) than Branch G (~1.0–1.2);
both are resolution-mild, not runaway.

## What this does NOT establish (the caveats — BLOCKING the strong claim)
1. **NOT proven converged.** A 2-grid (Nr=8,10) trend has no second difference / Richardson estimate /
   plateau. ×1.13–1.16 is *milder* than ×2.12 but is NOT a "converged" verdict — it could be slow creep
   or residual under-resolution. **A 3rd grid (Nr=12) is required** to tell plateau from creep
   (Branch-P warp is still *rising*, 2.53→2.87).
2. ~~**The matter solution's CHARACTER is UNMEASURED — could be trivial.**~~ **RESOLVED 2026-06-27
   (follow-up #2, `check_winding_survival.py`) — the winding SURVIVED.** Re-solved Nr=8 / Branch G /
   X=−2e5 saving the field; the topological DEGREE per shell (computed with the grid-EXACT dn;
   diagnostic validated: canon winding reads Q=1, unwound vacuum reads Q=0) is **Q ≈ 1 on every shell**
   (per-shell [0.996,0.986,0.957,1.0,0.974,0.976,0.989,1.0]; the ~2–4% wobble is coarse-grid (Nθ=6)
   integration error, nowhere near the Q≈0 of vacuum), with **|n| in [0.987,1.010]** and **nonzero,
   slightly-increased matter density rho 0.102→0.183**. So the converged solution is a GENUINE
   non-trivial degree-1 S² matter object — NOT unwound vacuum. PRECISE framing (per blind verifier,
   below — corrects an earlier overstatement): **there is REAL matter** (ρ_max(body)=0.182, degree≈1)
   and **ρ vanishes EXACTLY when n̂→const**, so the matter is real and winding-sourced; *part* of the
   metric warp is BC/gauge-driven (b(core)=−1 depth dial, a(seal)=0 gauge) — the claim is "real
   winding matter present," NOT "the entire warp is matter." SCOPE: shown for Nr=8 / Branch G (the
   representative case); Branch-P (deep φ) and finer grids not yet checked for degree leakage.
   **BLIND-VERIFIED CONFIRMED (agent `a63753fff5ff008b5`, 2026-06-28, zero-context adversarial,
   saved-field-only, no re-solve):** independently re-derived the degree integral AND built a SECOND
   method (geometric solid-angle, no derivatives) — both read ≈1 on the solved field (A interior mean
   0.977, B 0.943), calibrate cleanly (seed→1.0/0.939, vacuum→0/0), and the diagnostic is NOT rigged
   (a forced solved→const unwinding collapses Q smoothly to exactly 0). Re-evaluated residual on the
   loaded `u`: Φ=9.13e-22 (genuinely converged). VERDICT: could not break it — winding survived.
3. ~~**The "cure" comparison is CONFOUNDED.**~~ **RESOLVED 2026-06-29 (follow-up #3, off-diagonals-OFF
   control, `caveat3_offdiag_off_control.py`; BLIND-VERIFIED PARTIALLY-CONFIRMED, agent `ae5a16bb5c0247cdd`)
   — the off-diagonal completion is EXCLUDED as the warp-tamer.** Control = the SAME native-S²/Branch-G/kap8=1
   system with e_rt=e_rp=e_tp FROZEN to zero (masked Newton). LOAD-BEARING result (same-grid Nr=8, both
   fields saved + reverified; off-ON is fully floored Φ=9e-22): freezing the off-diagonals moves the
   diagonal warp only **1.0220→1.0293 (+0.7%)**. So completing the off-diagonals does NOT change the warp
   magnitude → it is NOT the cause of the milder-than-×2.12 trend. Three independent Nr=8 warps agree
   (off-ON 1.022, warm-frozen 1.021, cold-frozen 1.029). PRECISE (verifier's correction): off-diagonals
   don't change the warp MAGNITUDE, but they ARE required for CONSISTENCY (e_rt=0.11 floors the rth
   Einstein row; freezing leaves rth at 3.5e-3 / 0.39) — "irrelevant to the warp," NOT blanket-irrelevant.
   SOFT leg (not load-bearing): the cold off-OFF TREND ×1.19 (Nr8 1.029→Nr10 1.221) vs off-ON ×1.16, BUT
   the off-OFF Nr=10 point is under-floored (Φ=4.54, diagonal rows O(0.5), winding degraded Q_min=0.84) and
   the off-ON Nr=10=1.181 anchor is un-reverifiable (no saved field). ATTRIBUTION NARROWED: off-diagonals
   excluded; the milder trend is the **S³→native-S² matter swap and/or the SH-exact grid fix**, which remain
   MUTUALLY CONFOUNDED (no S³ control re-run). So caveat #3's specific question is answered; one residual
   confound (matter-vs-grid) is noted but was not part of #3's ask.
4. **The strong-field HORIZON hypothesis REMAINS OPEN.** The standing hypothesis (kap8=1 divergence =
   a real forming horizon / supermassive global monopole, to be resolved by GR-corpus analysis) is NOT
   retired by this run. Declaring "cured by completeness" on confounded 2-grid data would be the
   "impose the expected answer / demand smoothness" drift the solution-space gate exists to stop.

## Follow-ups to upgrade
- ✅ **DONE (2026-06-28) — Save + inspect the solved fields** (caveat #2): winding SURVIVED, blind-verified.
- ✅ **DONE (2026-06-29) — Off-diagonals-OFF control** (caveat #3): off-diagonals EXCLUDED as the warp-tamer,
  blind-verified PARTIALLY-CONFIRMED. Scripts: `caveat3_offdiag_off_control.py`; saved fields
  `control_offdiagOFF_cold_nr{8,10}_G_kap8_1.pt`; trace `control_offdiagOFF_cold.log`.
- ⏳ **OPEN — 3rd grid Nr=12** (caveat #1): plateau vs creep for the native-S² warp-trend. (Costly: Branch-P
  Nr=10 was ~20 h; Nr=12 is days.) This is now THE live question: with off-diagonals excluded, is the
  native-S² ×1.16 trend a converged plateau or a slow approach to a horizon? The HORIZON hypothesis is alive.
- (optional firming) the off-OFF Nr=10 control point is under-floored (soft); the conclusion does not need it.

## Verifier (blind, adversarial — verifier-before-record)
Agent `a7cd2e2e403170dfb`, 2026-06-27. Verdict: **NOT-CLEAN as first framed** — A (solver correctness)
PASS (pytest 32 passed/1 xfail; residual=EL verified; off-diagonals live + regression-locked; native-S²
grid-exact); **B CONCERN** (2-grid insufficient for "converged"); **C FAIL** (matter character unmeasured;
possibly-trivial/unwound solution); **D FAIL** (confounded baseline; horizon hypothesis pre-empted). The
narrow statement above is the verifier's licensed wording. The strong "divergence cured / it was the
frozen off-diagonal DOF, not a horizon" headline is REJECTED and NOT banked.

### Follow-up verifiers (2026-06-28/29)
- **Caveat #2** (winding survival): agent `a63753fff5ff008b5` — CONFIRMED (see caveat-2 block above).
- **Caveat #3** (off-diagonals-OFF control): agent `ae5a16bb5c0247cdd`, 2026-06-29, zero-context adversarial,
  saved-field + log only, no re-solve. Verdict **PARTIALLY-CONFIRMED**: all three warps reproduce to 4 sig
  figs (off-ON 1.0220 / off-OFF Nr8 1.0293 / off-OFF Nr10 1.2214); freeze exact (e_*=0.000); same winding
  class in all three; the fully-floored off-ON-vs-frozen Nr=8 same-grid pair (+0.7%) is the solid leg. Limits
  it imposed (now reflected above): "irrelevant" → "irrelevant to the warp MAGNITUDE" (off-diagonals required
  for rth consistency); the Nr=10 trend leg is soft (under-floored off-OFF point + un-reverifiable off-ON
  anchor). Net: off-diagonal completion EXCLUDED as the warp-tamer; matter-vs-grid attribution left open.

## STATUS after caveats #2 + #3 (the kap8 picture now)
The original "divergence CURED — it was the frozen off-diagonal DOF, not a horizon" headline is DEAD on two
counts: (#2) the native-S² matter is real and survived (the warp is matter-sourced, not an empty-cell artifact);
(#3) the off-diagonal completion is NOT what tamed the trend. What stands: the native-S² run shows a MILD warp-
trend (×1.16 at Nr=8→10) vs the old S³/diagonal ×2.12, and that milder behavior comes from the matter-swap
and/or the grid-fix, NOT the off-diagonals. The REMAINING question is caveat #1 (Nr=12): is the native-S² ×1.16
a converged plateau or slow creep toward a horizon? The strong-field HORIZON hypothesis is ALIVE and is now the
live question. No "cured" conclusion is banked.

## NATIVE REFRAME (2026-06-29): "what is this dense object?" in UDT variables, NOT the GR horizon lens
Charles's directive: drop the GR "horizon/black-hole" question; read the object in UDT's own variables
(dilation φ, the winding defect, areal law ρ=r, public charge). Diagnostics (`ponder_horizon_signatures.py`,
`native_object_characterization.py`) run on the SAVED fields, no solve. Primary = off-ON Nr=8 (floored).
**What the existing fields show (Nr=8, Branch G, kap8=1 — SCOPED):**
- **NOT a forming horizon.** Lapse e^a min ≈ 0.37 (no collapse); GR compactness 2m/R peaks ~0.89 but does
  NOT climb to 1; it sign-flips/degenerates in the outer interior (the GR "near-horizon, above-Buchdahl"
  reading was a misapplied ruler, not a physical horizon). One real feature: a curvature (Ricci) spike at
  the r→0 core (~−6e5) — a genuine core feature, not a horizon.
- **NOT a localized lump.** The clean cumulative energy-charge E(<r) keeps rising to the seal (does not
  saturate). [Clean diagnostic: dE/dr = ∫ρ√(det g_spatial) dθdφ — replaces the spectral-ringing-contaminated
  Misner-Sharp m(r) the first cut used.]
- **NOT a clean scale-free monopole either.** E(<r)/r FALLS ~5–6× across the interior (≈147→26), where a
  scale-free defect (E∝r) would hold E/r constant. So the energy is **CORE-CONCENTRATED** (winding-gradient
  density ρ ~ r^−2.4, huge at the core), with an extended power-law tail — degree-1 winding present on EVERY
  shell (caveat #2) but energetically core-weighted.
- **Gentle in φ** (~4% redshift, |φ|≲0.04 at Nr=8) and **ρ=r holds to ~10%** (exp(c)∈[0.90,1.09]).
**THE NATIVE IDENTIFICATION (banked, conservative):** the kap8 object is a **core-concentrated degree-1 S²
winding defect sitting in a gentle dilation well** — neither a black hole (horizon), nor a localized particle,
nor a clean scale-free monopole. This RESOLVES the horizon scare natively and is consistent with the canon
(native matter = S² winding defect, not a localized particle).
**OPEN / NOT banked:** (a) the *quantitative* defect law is not pinned at Nr=8 (~6 interior shells), and the
core-dominated CHARGE profile is genuinely soft (rc-entangled — see spectral check below); (b) ~~the shallow-φ is
grid-fragile (frozen Nr=10 hints |φ| deepens ~6×)~~ **RETRACTED 2026-06-29 — see spectral check: φ is RESOLVED
at Nr=8; the 6× came from the under-floored frozen Nr=10, not real physics.**

### Spectral-resolution check (2026-06-29) — blind-verified PARTIALLY-CONFIRMED, agent `a73caf9cf0e6ca7fd`
A Chebyshev-spectrum / truncation-error check on the Nr=8 off-ON field, run because the native numbers above must
not ride an under-resolved field. **Result: the SMOOTH sector is RESOLVED at Nr=8.** φ truncation error decays
cleanly (~3% at the top mode); lapse a is dominated by modes 0–1. So the load-bearing native reading (gentle φ
~4%, not-a-horizon) is on a **resolved** field — SOLID. The apparent "fat tails" are NOT generic under-resolution:
(i) the radial-metric b's flat Chebyshev spectrum is the *mathematically exact* fingerprint of the imposed
`b(core)=−1` depth-dial BC step (a single endpoint cardinal function on N=8 Lobatto nodes is exactly flat —
demonstrated synthetically by the verifier; excluding the core node, b's tail collapses 0.66→0.15 and decays) —
benign and exactly captured, NOT a smooth feature the solver missed; (ii) ρ is fully unresolved but that is the
*inherent* singular winding-defect core (ρ~1/r², dynamic range ~3.4e5) regulated by **rc=0.1, not Nr**. Verifier
REFUTED my original suspicion (the flat-b was an artifact/noise) — the numbers were sound — but corrected my
mechanistic framing (I'd called it "generic under-resolution / grid-fragile φ"; it is a BC step + an inherent
core singularity, with φ/interior actually resolved). **Consequence for the Nr=12 question:** LOW value — the
smooth sector is resolved (finer Nr won't change "gentle well / not a horizon"), and the only soft quantity (the
core charge) is rc-regulated, not Nr-fixable. Recommendation: carry to the time-live build rather than spend a
finer-grid solve.
**Blind verifier (zero-context adversarial, saved-field only, agent `a9efe4b52689b19a7`, 2026-06-29): PARTIALLY-
CONFIRMED.** It UPHELD the exclusions (not-horizon: lapse 0.37, 2m/R not→1; not-localized) and the gentle-φ /
ρ=r / core-concentration, and it REJECTED the original over-claim ("clean scale-free monopole / m∝r / constant-
2m/R deficit": R²=0.013 over the full interior, MS-mass contaminated by spectral ringing). It also caught two
errors since corrected here (a real core Ricci spike — NOT "no singularity"; and the grid-fragility of φ). The
conservative identification above is the verifier-licensed wording; the strong "global monopole" headline is
NOT banked.
