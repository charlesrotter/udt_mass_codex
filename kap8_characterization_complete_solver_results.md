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
