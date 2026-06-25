# Complete 4-D Solver — Stage 1: Pole-Stable GENERAL-Metric Einstein Engine (BANKED)

**Mode:** INFRASTRUCTURE, SOLVER-FIRST, DATA-BLIND. **Driver:** Claude Opus 4.8 (1M), agent for
udt_mass_codex. **Date:** 2026-06-21. **Status: BANKED — blind-verifier SUPPORTED-WITH-REVISIONS**
(verifier agent afe291bf819a17d0a; revisions folded in below).

**Context:** Stage 1 (the GATING stage) of THE COMPLETE 4-D SOLVER BUILD PROGRAM (COMPLETION_PROGRAM.md,
Charles-directed 2026-06-21: build ONE solver with every axis live — full spatial metric incl shear +
live time + multi-harmonic finite-amplitude time + independent phi + full-angular matter + free areal
chart; nothing frozen, only the grid bounded). The 3-parallel-agent infrastructure audit found the
primitives clean but every real residual silently routed through the DIAGONAL-ONLY `einstein_mixed_weyl`
(shear frozen), because the GENERAL engine `whole_metric_3d_core.einstein` is numerically N-DIVERGENT on
the steep soliton core. Stage 1 = remove that block. **It is the keystone: Stages 2-6 build on it.**

## THE PROBLEM + DIAGNOSIS (verified V1)
The general `CORE.einstein` builds Christoffels from a spectral `dg`, then spectrally differentiates them
again (`dGamma`) — **nested spectral differentiation**, each pass amplifying high modes O(N^2). On the
steep metric the Einstein-tensor error GROWS WITH RESOLUTION (the opposite of under-resolution):
on a SMOOTH analytic diagonal warp (exact ground truth), CORE body max|G| = 17.1 / 31.9 / 111.9 / 247.8
at Nr = 16/32/48/64, while the analytic references stay bounded (~12-17, the true curvature). An
exponential spectral filter between the passes does NOT cure it (tried, rejected). Structural, not tuning.

## THE FIX (verified V2-V5)
**Analytic general Christoffels/Einstein (codegen) — the general analog of `einstein_mixed_weyl`.** The
diagonal generator was extended to the GENERAL stationary metric (warps a,b,c,d + spatial shear
e_rt,e_rp,e_tp + time-row h_tt,h_tp), so curvature is closed-form and the grid differentiates only the
SMOOTH warp partials ONCE (no nested pass; poles 1/sinθ symbolic, evaluated only at interior GL nodes).
Convention matches `full3d_spectral.build_metric` exactly (off-diagonal scalings e_rt·r, e_rp·r·sinθ,
e_tp·r²·sinθ; time-row h_tt·r, h_tp·r·sinθ).

**Files (committed):** `gen_einstein_3d_general.py` (generator) -> `einstein_3d_general_gen.py` (65 KB,
CSE-factored closed form, flat-residual = 0, deterministic/byte-reproducible) -> `einstein_3d_general_eval.py`
(the engine: `einstein_mixed_general` + `ricci_scalar_general` = -trace G).

## ACCURACY (independently reproduced by the blind verifier)
- **Formula exactness (the critical claim, V2):** matches an INDEPENDENT FD general-Einstein (separate code
  path, full shear + time-row) converging as H^2 to the engine value — no O(1) formula bug; time-row carried
  (worst cell G^0_3=0.9369, 7-digit agreement).
- **Diagonal limit (V3):** vs `einstein_mixed_weyl` on the round soliton, ABSOLUTE agreement 5e-15 -> 1.5e-12
  across Nr 16->64, **N-STABLE** (warp partials bit-identical). [REVISION: state as absolute / relative-to-mean
  (~1e-11), NOT pointwise relative-max — the latter degrades to ~1e-7 only at genuine G-zero-crossing nodes,
  not engine error.]
- **Flat -> 3e-15..4e-13; Schwarzschild -> exponential** (2e-3 -> 4e-7 over Nr 16->48) (V4).
- **Shear:** machine-exact (1.1e-16) vs independent sympy. **Poles safe** (smallest sinθ=0.145, no nan/inf) (V5).
- **N-CONVERGENT, not N-divergent** — the CORE failure is gone.

## EDGE-BOUNDARY (folded into Stage 1, verified)
The old 3-row Chebyshev edge excision masked 38% of radial rows at Nr=16. With the analytic engine the
O(N^2) edge blowup is GONE: it agrees with the reference AT the edge rows (~1e-10 abs core/seal). =>
**drop the 3-row mask; enforce the physical BCs at the true boundary nodes** (a(seal)=0, b(core)=-p,
winding/phi BCs). No graded grid needed (Chebyshev already clusters 9-19x finer at the ends). [Item 4 of
Charles's 4 cleanups — done.]

## REVISIONS / CAVEATS ON THE RECORD (blind verifier)
1. **d_t = 0 (stationary) — BANKED LIMITATION.** The generator drops t-derivatives; the engine is correct
   ONLY for static/stationary metrics. Time-row off-diagonals are CARRIED, but genuinely time-DEPENDENT
   (breather/dynamical) metrics need REGENERATION with live ∂_t. **This is exactly Stage 5's task** — the
   generator must be re-run without the stationarity assumption when multi-harmonic time goes live.
2. **Relative-error wording:** use absolute / relative-to-mean tolerances downstream, not pointwise
   relative-max (misleading at G-zero-crossings).
3. **Angular accuracy** at low Nθ on steep genuinely-3-D angular structure was not stress-tested (tested
   warps had mild θ,ψ content); check when off-round shear fields go live (bump Nθ where shear has strong
   θ-structure). The pole structure itself is symbolically carried + verified.

## PREMISE LEDGER
| item | status |
|---|---|
| Analytic general Christoffel/Einstein generator (extends einstein_mixed_weyl to shear + time-row) | DERIVED/codegen; flat=0, FD-exact, sympy-exact |
| Metric convention = build_metric (off-diag scalings, time-row) | CHOSE (matches the existing solver); verified by independent FD using the same convention |
| Stationary d_t=0 in the generator | CHOSE (valid through Stage 4; Stage 5 regenerates with live ∂_t) |
| Poles via GL-interior-node exclusion (no symbolic cancel) | CHOSE; verified pole-safe |
| Drop the 3-row edge mask -> physical BCs at true nodes | DERIVED-consequence (engine clean at edges) |

## HONEST STATUS
**SOLVED + VERIFIED.** A clean, N-convergent, shear- and time-row-capable general-metric curvature engine
exists, machine-exact in formula, ~1e-12..1e-14 vs the diagonal-analytic reference in the diagonal limit.
The gating obstacle (why everything was secretly diagonal) is removed. Stages 2-6 (free matter, free chart,
assemble static, multi-harmonic time, run) can proceed on this engine. d_t=0 is the one banked limitation,
addressed at Stage 5.

## ATTACK HERE (future re-grade)
1. Re-confirm V2 with an independent symbolic (not FD) general Einstein at a shear+time-row point.
2. Stress-test angular accuracy at low Nθ on a steep genuinely-3-D shear field (the untested corner).
3. When Stage 5 regenerates with live ∂_t, re-verify the time-dependent generator the same way (flat=0,
   FD-exact, N-stable).
