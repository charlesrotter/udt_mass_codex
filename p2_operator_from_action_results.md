# P2 — OPERATOR FROM THE ACTION (SOLVER_INTEGRITY_UPGRADES_SPEC P2)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **Status:** BUILT + blind-verified
(VERIFIED-WITH-CAVEATS, caveats CLOSED). Files: `solver_action.py`,
`tests/test_operator_from_action.py`. **Suite (P1+P2): 16 passed / 5 xfailed, <1.1s, no Newton/jacrev.**

## Scope (Charles decision 2026-06-23)
The spec's action `S=∫√−g[e^{2φ}R + X e^{2φ}(∂φ)² + e^{2φ}L_m]` was traced to the derivation docs
(P2 MAP) and found NOT safe to canonize: the `e^{2φ}R` weight is derived only on the GRADIENT
curvature (angular sector refuses it — Branch G/P fork UNRESOLVED = the phi-angular tension); the
`e^{2φ}` matter weight is UNTRACED (corpus matter action has none); X is FREE; and the LIVE operator
runs the **a=−1 GR baseline**, not the derived theory. So P2 builds the codegen+equality MACHINERY
against the action the live operator ACTUALLY realizes (GR-baseline), and the derived-theory version
is **deferred to MIGRATION** (which must resolve the fork + matter weight). The P1 xfails + this P2
baseline = the migration's acceptance tests.

## The single source-of-truth: `solver_action.py`
The GR-baseline action `S = ∫√−g[(1/2κ8)R + L2 + L4]`, with `ACTION_TERMS` — every term carrying a
provenance TAG (DERIVED/FREE/IMPORTED/MIGRATION-DEFERRED) + evidence + the live operator that realizes
it. The derived-theory terms (dilaton kinetic, the UNTRACED matter weight `e^{2φ}L_m`) are recorded as
MIGRATION-DEFERRED with `operator=None` so they cannot be silently smuggled in to pass a test. SPINE
(shared with P1): this file REFERENCES derivations, it never RE-ASSERTS their values.

## What P2 PROVES vs CHECKS (stated honestly — verifier-driven)
- **Matter STRESS == exact Hilbert variation of the action** — `stress_tensor` == autograd
  `−2 ∂L_m/∂g^{μν} + g L_m`. **PROVEN to ~1e-15.** Independent routes (hand-calculus vs autodiff of
  the same L_m); exercises L4/off-diagonals.
- **Gravity G^μ_ν == EL of √−g R** — two INDEPENDENTLY-generated analytic engines (`einstein_mixed_general`
  general-sheared vs `einstein_mixed_weyl` diagonal) agree to **1.7e-13** on a smooth metric → **no
  hand-coding drift.** Correctness-vs-truth anchored by P1 (de Sitter G=−Λ to 1e-13, Schwarzschild/flat
  G=0). (Honest: engine-agreement proves no-drift, not EL-correctness; P1 supplies the truth anchor.)
- **Matter FIELD-EOM consistent with the action** — `matter_el_3d` (strong-form sympy codegen) ==
  `−matter_el_autograd` (weak-form autograd of the same action). Two independent routes; CONVERGE with
  resolution (pole-θ-excluded bulk rel 0.9%→0.38%→0.29% over Nr 16→24→32). **CONSISTENCY ~0.4%, NOT
  machine-precise** (strong vs weak discretizations differ at 1/sin²θ pole nodes). Catches the
  codegen-bug class (an 8% Lagrangian drift → bulk rel 4.4%, well past the 2% gate). This closes the
  verifier's coverage gap (the matter Θ-EOM was previously untested) — the failure class is exactly the
  historical "L4 codegen bug" `matter_el_3d`'s docstring warns of.
- **Residual assembles G − κ8 T** — the field-eq rows of `residual_vector_p1` == `(W·(G−κ8 T))[body]`
  recomputed with the same engine. **REGRESSION LOCK** (tautological as an EL proof; locks the assembly
  recipe — W weighting, κ8 sign/order, component list — and would catch a changed coupling).
- **Provenance** — every `ACTION_TERMS` entry tagged; MIGRATION-DEFERRED terms not wired; the untraced
  matter weight flagged (`operator=None`); every LIVE term traced (DERIVED/FREE).

## Acceptance — CATCH-PROOF (the suite must BITE)
On scratch branches/backups (repo restored each time):
- matter stress drifted (`Tab*=1.0001`) → ONLY `test_matter_stress_is_action_variation` RED.
- residual mis-assembles (`G − 2κ8 T`) → ONLY `test_residual_assembles_einstein_eq` RED.
- untraced matter weight wired (`operator="SNUCK IN"`) → 3 provenance tests RED.
- matter Lagrangian drifted (`L2 ×1.08`) → `test_matter_field_eom_consistent_with_action` RED (bulk rel 4.4%).

## Verifier trail (blind, fresh zero-context — P4 ruling)
- **Verifier** (agent acc513a4bfdeef941, 2026-06-23): VERIFIED-WITH-CAVEATS. Confirmed 15/5 (pre-fix)
  counts, the stress proof non-circular, the two gravity engines genuinely independent (distinct
  generators/md5), the catch-proof reproduces, no DERIVED tag overclaims. CAVEATS: (1) the matter
  FIELD-EOM was untested (only the stress); (2) `test_residual_assembles_einstein_eq` is a
  regression-lock mislabeled "proof"; (3) the provenance tests are a registry self-consistency lint,
  not a live-code scan.
- **Closure (this session):** (1) added `test_matter_field_eom_consistent_with_action` (converging,
  catch-proven); (2) relabeled the residual test a regression-lock + fixed the `solver_action.py`
  header to distinguish PROVEN/CONSISTENCY/LOCK; (3) accepted as scope — the registry lint pairs with
  P1's `test_no_smuggled_literal_in_operator` (live-code literal scan); a smuggled weight that ALSO
  bypasses the registry is a residual gap noted for migration.

## Honest residual notes
- The field-EOM check is a CONSISTENCY test (~0.4%, converging), not a machine-precision proof; pole-θ
  and coordinate-edge nodes are excluded (strong-vs-weak discretizations diverge there, resolution-
  independent ~3%).
- A truly independent machine-precision matter Θ-EOM proof (fresh sympy EL of L_m) was NOT built —
  high bug-risk for the L4 Skyrme term; the convergence + stress-consistency + the banked
  VERIF_divT_committed cover it instead.

## Next (per spec ORDER P1→P2→P3)
P3 — factor the binding disciplines (solver-first, verifier-before-record, no-shortcuts,
completeness-map) into auto-loading `.claude/skills/` SKILL.md files; CLAUDE.md points to them but
keeps the short tripwires inline (always-in-context). Then P4 (cross-model verify) / P5 (LIVE.md shrink).
