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
2. **The matter solution's CHARACTER is UNMEASURED — could be trivial.** The guard returned ONLY
   (Phi, metric warp); it never inspected the solved matter (winding survival, |n|=1, T^μ_ν), and the
   solved field was NOT saved. The matter core is FREE, so the winding can UNWIND to vacuum (an unwound
   constant n gives elN=0, |n|=1 exactly — a valid competing floored solution). The metric BCs alone
   (b(core)=−1, a(seal)=0) already source an O(1) warp. **So the recorded warp could be a BC artifact
   with NO matter** — the result does NOT yet establish a non-trivial S² matter solution.
3. **The "cure" comparison is CONFOUNDED.** Vs the old divergent run, TWO things changed at once:
   off-diagonals were completed AND the matter was swapped S³→native-S². So these solves do **NOT
   isolate** "the frozen off-diagonal DOF" as the cause; attributing the milder trend specifically to
   off-diagonals is unsupported here.
4. **The strong-field HORIZON hypothesis REMAINS OPEN.** The standing hypothesis (kap8=1 divergence =
   a real forming horizon / supermassive global monopole, to be resolved by GR-corpus analysis) is NOT
   retired by this run. Declaring "cured by completeness" on confounded 2-grid data would be the
   "impose the expected answer / demand smoothness" drift the solution-space gate exists to stop.

## Follow-ups to upgrade (none run yet)
- **3rd grid Nr=12** (both branches) — plateau vs creep. (Costly: Branch-P Nr=10 was ~20 h; Nr=12 is days.)
- **Save + inspect the solved fields** — winding degree, |n|, matter T^μ_ν max — to establish the
  solution is a non-trivial S² object, not unwound vacuum. (Re-solve Nr=8 ~2 h, saving u.)
- **Off-diagonals-OFF control on native-S² matter** — to actually isolate the off-diagonal effect from
  the S³→S² matter swap (resolves caveat 3).

## Verifier (blind, adversarial — verifier-before-record)
Agent `a7cd2e2e403170dfb`, 2026-06-27. Verdict: **NOT-CLEAN as first framed** — A (solver correctness)
PASS (pytest 32 passed/1 xfail; residual=EL verified; off-diagonals live + regression-locked; native-S²
grid-exact); **B CONCERN** (2-grid insufficient for "converged"); **C FAIL** (matter character unmeasured;
possibly-trivial/unwound solution); **D FAIL** (confounded baseline; horizon hypothesis pre-empted). The
narrow statement above is the verifier's licensed wording. The strong "divergence cured / it was the
frozen off-diagonal DOF, not a horizon" headline is REJECTED and NOT banked.
