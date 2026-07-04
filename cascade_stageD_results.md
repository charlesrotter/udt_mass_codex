# STAGE-D PREDICTION TEST — PASSED (blind-verified; scoped)

**Date:** 2026-07-03. **Contract:** `cascade_stageD_prereg.md`, FROZEN at commit 34d1b6b
(Charles's pins: ±1.0% locations / exact consecutive integers / blind sweep; forecast held out
of the repo, SHA-256 committed in the contract before the sweep). **Data:** commit 6cb6e30.
**Blind adversarial verifier:** agent `ac8b3fe72dbae49b9`, this date — all 7 attacks HOLD,
false passes found: NONE (report below).

## The result

The derived quantization closure — d*(N) solves z_c_eff(γ(d)) = Θ(N)√x_c, Θ(N)=(N+1)π+θ₀(N)
(`ladder_theta0_accumulation_results.md`) — was evaluated BLIND-FORWARD into the never-refined
aliased window d ∈ (1.45e-3, 2.11e-3) (family A1 m=3, Z=8, ρ_c=1, below-stuck side; Stage B had
only "≈11 rungs extrapolated, unrefined"). The frozen forecast: **13 rungs, N = 23…35, with
per-rung locations.** The blind sweep (survey agent `a0e8a4002c4c669cd`, 1904 shots, every root
two-method confirmed + graduated-floor audited, zero unresolved spans) found:

- **COUNT: 13/13 exact** — window-proper found N-list = {23…35}, consecutive, none missing,
  none duplicated. Found integer LABELS match the forecast rung-for-rung (stronger than the
  contract required, which only demanded list membership).
- **LOCATIONS: 20/20 within the ±1.0% band** (13/13 window proper + 7/7 guard band N=20–22,
  36–39). Worst deviation −0.139% (N=21) — 7× inside the band. Assignment injective,
  denominator = predicted, per contract.
- **Secondaries (characterizing):** parity alternation 20/20; q within 0.2%; a_seal within ~1%.
- **N=40** correctly unmatched (frozen forecast excluded it: predicted below the swept floor).
- **Look-elsewhere (contract method):** joint uniform-null probability of the 13 window-proper
  location hits = 5.6e-3 (band fractions 0.57–0.87 — the ladder is dense, the band generous;
  this is the contract's deliberately null-friendly number). The count criterion is exempt
  (banked pre-arc). The observed deviations are ~10× tighter than the band; reported as
  characterization, NOT a retuned criterion (no-retuning clause honored).

**Domain extension (unplanned strengthener):** forecast rungs N≳31 sit at γ<0.4 — below the γ
range of every banked rung the law was built on (flagged honestly in the frozen forecast). They
hit anyway: the pass EXTENDS the law's tested domain, not just its interpolation.

## Verifier report (blind adversarial pass — agent `ac8b3fe72dbae49b9`)

1. **Freeze integrity HOLDS:** all three hashes match at 34d1b6b, at 6cb6e30 (its direct child),
   and at HEAD; sweep transcript starts 37 s AFTER the freeze commit; no alteration path.
2. **Blinding HOLDS:** transcript-level audit — the sweeper read only public Stage-B/C artifacts
   and solver code; zero forbidden reads; sweep scripts contain no hardcoded positions; the
   blind agent's Write payloads are byte-identical to the committed files.
3. **Comparison HOLDS:** independent Hungarian-assignment re-derivation reproduces 20/20,
   13/13, worst −0.1392% exactly; N=35 strictly inside the open window (+0.068% above the
   edge) on the verifier's own numerics too.
4. **Spot re-runs HOLD:** own pure-Python RK4 (not LSODA/DOP853), own event bisection, own
   graduated-floor counters — N=23/30/35 roots reproduced to 1.5–1.8e-7 relative; all counts,
   ρ_s, a_seal, q match.
5. **Forecast chain HOLDS:** fully independent re-evaluation (own bottom-γ-system integration,
   no spline; sympy-cross-checked family coefficients) — d*(25) and d*(33) to ~3e-7; the two
   frozen CHOSE premises are hash-covered and could not have flipped any verdict (RHS form
   moves d* ≤0.05%).
6. **Look-elsewhere HOLDS:** 5.648e-3 reproduced; no overselling anywhere in the record.
7. **Compliance HOLDS:** one forecast, one comparison, no retuning; PROVISIONAL labels
   everywhere pre-verdict.

**For the record (verifier, non-fails):** (a) all 20 deviations share one sign (found < predicted
by 0.067–0.139%) — a coherent small systematic offset of the 2nd-order law, consistent with its
stated error budget (open slivers: handover, parity boundary term); a candidate target for any
3rd-order sharpening. (b) The count-rule/edge-rule interaction (a predicted-in-window rung found
in the guard band) is ambiguous in the frozen wording — NOT exercised by the data; tighten in
future contracts.

## Scope (binding — what this pass is and is not)

- IS: a pre-registered, blind, hash-frozen prediction of 13 never-observed solutions of the
  metric's cell-closure problem by the DERIVED spectrum law, verified end-to-end — the law is
  the real law of the cascade in this family at ~0.1% accuracy, on rungs it was never fitted to,
  including a γ-regime it was never built on.
- IS NOT: an adjudication of the Z-fork (Z=8 only; stated per the banked rule); a statement
  beyond family A1 m=3 (Stage-C universality is its own banked result); anything beyond the
  round-static Branch-P reduction; a claim about the two open slivers (the one-signed ~0.1%
  systematic now bounds them empirically in this window).

## Provenance chain

Charles's four stability rulings (canon C-2026-07-03-1/-2, commit 5f99eec) → contract + Charles's
three contract pins, forecast hashes frozen (34d1b6b) → forecast agent `ac4fa347c6c5cc11d`
(closure algebra only, calibration reproduced banked deviations exactly; files held in scratchpad)
→ blind sweep agent `a0e8a4002c4c669cd` → forecast revealed + hash-verified + comparison
(`stageD_compare.py`, 6cb6e30, PROVISIONAL) → blind adversarial verifier `ac8b3fe72dbae49b9`
(scripts `stageD_bv_*.py`, committed with this doc) → THIS BANK.
