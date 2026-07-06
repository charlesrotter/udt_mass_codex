# Provenance audit + X solution-space exploration (2026-06-29/30)

Triggered by Charles catching that `X_PROD=-2e5` (branch_operator.py:85), tagged `# FREE`, has its MAGNITUDE
pinned by a Cassini (solar-system PPN) fit, not derived — and had silently shaped every downstream result.
Two independent audits (one direct ledger `a7cc21df8`, one BLIND adversarial prosecutor `a910a6016`) + an
X-window solution-space sweep. OBSERVE/audit mode.

## 1. The verdict on asserted numbers: X=-2e5 is the LONE observation-fit kluge on the live path
Both audits independently agree. After verifying every `DERIVED` tag against its cited derivation:
- **X = -2e5 — OBSERVATION-FIT, mis-tagged FREE.** R1-R3 fix only that both action terms wear e^{2φ} and (no-ghost)
  the SIGN (X<0); the MAGNITUDE is purely the Cassini PPN bound: |γ-1|=4/|X-8|, Cassini |γ-1|<2.3e-5 → |X|>1.74e5;
  -2e5 = that edge rounded up (`native_dilation_weight_derivation_results.md:256-259`). NOTHING in the metric
  selects it; the derivation doc lists "what fixes X" as OPEN. It is ALSO the solver's rate-limiter (smax~|X|,
  the D1 conditioning wall). Every live quantitative static result is conditioned on this solar-system fit.
- **kap8 = 1 — DERIVED, holds** (independent sympy: matter term = -1× Hilbert stress of e^{2φ}L_m; verifier-
  confirmed; it even corrected a previously-smuggled 0.05). The legacy kap8=0.05 scripts are off the live graph.
- **xi = kap = 1 — units** (L=√(kap/xi)=1). The `XI_PROD=KAP_PROD=2e-2` branch_operator defaults are DEAD CODE
  (the live solver always overrides to 1.0) — inert, but latent traps; reconcile/remove.
- **p, m, branch G — FREE and surfaced** (p,m explored; branch G is the open G/P fork = the `test_no_habit_pins`
  xfail). **rc, cell, wbc=30, grid, clamps, body-mask — CHOSE/category-A** (numerics, legitimately fixable).
- **No other observation-fit number on the live path.** 7.004/z_CMB is canon narrative only, never in the solver;
  the lepton data-blind contract is intact (no wall numbers loaded anywhere).

## 2. Two DERIVED-headlines that are SOFTER than they read (surfaced, not smuggled — but unresolved)
The blind prosecutor flagged two load-bearing choices whose "DERIVED" headlines paper over real tension:
- **The e^{2φ} matter weight (LIVE, load-bearing).** `solver_action.py:110-125` tags it MIGRATION-DEFERRED,
  "flagged CHOSE for field matter — NOT derived." a(φ)=e^{+φ} is derived only for a STATIC POINT-PARTICLE rest
  mass; extending to the full field Lagrangian is "the natural reading," not forced. It shifts the matter EOM by
  an **O(5) factor at hadronic depth** (e^{2φ}~5 — exactly the Principle-2 legacy warning territory). The
  scale-symmetry-correct angular field-matter weight may be e^0. **Deserves Charles's eye — could materially
  change the matter sector.**
- **φ(seal)=0.** Two source docs CONTRADICT on its parity: `seal_junction_condition_results.md:69` says φ
  EVEN→Neumann (time-index count); `D1_FIX_DESIGN.md:88` says φ odd→Dirichlet=0 (spatial mirror). The DERIVED
  tag rides one branch of that fork (correctly flagged "canon-confirm pending"). Needs adjudication.
- (Minor: CANON C-2026-06-18-1 "metric form derived from relativity" is an over-read — only the exponential
  time-law and B=1/A are forced; sphericity/diagonality/staticity/areal-r are CHOICES. Don't read it as the
  whole line element being derived.)

## 3. X solution-space sweep (`x_solution_space_explore.py`) — the object is X-STABLE (not a Cassini artifact)
Determined posing, branch G, kap8=1, Nr=8, warm-started X-ladder from natural X=-1 toward throttled. PROVISIONAL:
none of these floored (Phi 2e-3 at X=-1 growing with |X|; 40-iter budget), so observables are AT-FIXED-BUDGET,
not converged — strong signal, not floor-certified.

| X | Phi | phi_absmax | winding Q | lapse_min | warp | rho_max |
|---|---|---|---|---|---|---|
| -1 | 2.1e-3 | 0.90 | 1.000 | 0.55 | 2.57 | 0.0097 |
| -10 | 5.0e-2 | 0.86 | 1.000 | 0.56 | 2.56 | 0.0094 |
| -100 | 2.1e-1 | 0.82 | 1.000 | 0.55 | 2.56 | 0.0098 |
| -1000 | 1.1e0 | 0.75 | 1.000 | 0.50 | 2.80 | 0.0107 |

- **The object barely changes across 1000× in X:** dilaton ALIVE (φ≈0.8, only gently throttled), winding EXACTLY
  degree-1 throughout, NO horizon at any X, warps/density flat. => the kap8=1 "winding-defect, not-a-horizon"
  result **survives un-pinning X** — a robust metric feature, NOT a creature of the Cassini-pinned X=-2e5.

## 4. [SUPERSEDED later 2026-06-30 — RESOLVED; see LIVE.md CURRENT STATE] The non-flooring puzzle at X=-1
**RESOLVED after this was written:** `d1_lsfloor_test.py` proved F is 99.9% REDUCIBLE (a near-exact solution EXISTS;
posing CONSISTENT) → the non-flooring was solver GLOBALIZATION, not a posing flaw. The galerkin BC-basis + seal-BC
reconciliation then made the determined solve DESCEND 6 orders. The live open item is NOT this puzzle but the BASIN
AUDIT (Branch A vs B; see LIVE.md). Original (now-stale) note kept below for the record:
At X=-1, smax~2.4e4 (good conditioning), yet 40 iters from the seed → Phi=2e-3, not floored. So there is a
convergence obstruction BEYOND the X-stiffness we'd blamed. This is now the top solver-trust item — it undercuts
trusting any quantitative result until resolved. NEXT: localize where the Phi=2e-3 residual concentrates (cheap
row/sector breakdown at the saved X=-1 field) before expensive re-solves.

## Cleanups owed (deferred): kill the dead XI/KAP/X _PROD=2e-2/-2e5 defaults in branch_operator.py; retire
legacy kap8=0.05 scripts from any cited results.
