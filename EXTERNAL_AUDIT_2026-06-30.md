# External audit (2026-06-30) — solution-space instrument + the basin reframe

Charles's outside auditor. **Static, source-level (read-only); not an execution audit.** Driver (Claude) reviewed
and AGREES with the substance — especially the reframe (the driver had drifted into MERIT/expectation language, a
real violation of `solution-space-not-imposition` / the anti-imposition gate). Captured here as the next-session
to-do (deferred this session for context limits). LIVE.md "CURRENT STATE" carries the actionable summary.

## A. Instrument self-consistency (false-pass / stale-guard risks)
Theme: docs/tests still partly describe a GR-baseline / MIGRATION-DEFERRED instrument while the LIVE solver already
uses the migrated derived operator + e^{2φ}-weighted matter. That mismatch can make the solver look cleaner than it is.
1. **Action provenance layer STALE.** `solver_action.py` calls itself the single source-of-truth action but states its
   scope is the old a=−1 GR-baseline and marks the derived dilaton-kinetic + matter-weight terms MIGRATION-DEFERRED /
   not wired. But the live path uses `branch_operator.E_mixed_branch/EL_phi_branch` (derived scalar-tensor, f=e^{2φ},
   matter −kap8 f T) and `_el_matter_s2_weighted` weights matter by e^{2φ}. → test layer may certify the OLD relation.
2. **"No silent defaults" cleanup INCOMPLETE.** `branch_operator` now requires explicit X/xi/kap (good), but
   `residual_vector_p1` AND `newton_solve_p1` still default `X=-1.0, xi=1.0, kap=1.0, branch="G"` → the requirement is
   bypassable at the higher entrypoint; a run can silently inherit provenance.
3. **Premise-ledger checks only TOKEN PRESENCE** (`test_premise_ledger_tagged_and_synced`): catches stale deletion,
   not whether the premise is used in the intended call path / default changed / appears only in a comment / all call
   sites ledger the choice.
4. **Live tests exercise the OLD/default path more than the determined path:** the liveness test calls
   `residual_vector_p1(...)` WITHOUT `determined=True` and with `kap8=0.05` — but the frontier is determined=True + kap8=1.
5. **`test_operator_from_action.py` tests GR-baseline only** (locks φ=0 where the derived operator degenerates to the
   baseline; warns not to wire the e^{2φ} theory "to pass a test"). Valuable as a regression LOCK, but NOT a live proof
   that the migrated UDT operator equals the intended action.
6. **Conditional runtime imports vs the gate's graph walker:** `galerkin_basis` is registered in
   `PROJECT_MODULE_REGISTRY` but imported conditionally inside `newton_solve_p1` (step=='galerkin'), not top-level; the
   gate scans top-level imports then asserts no dead registry entries. Either the test is fragile or the graph model
   doesn't cover conditional solver modes (galerkin/svd_ls). Graph model incomplete. (pytest currently 32/1xfail = passes,
   so it's a latent completeness gap, not a current failure.)
7. **Hooks are reminders, NOT guards** (non-blocking, silent-exit on parse error / unmatched tool). Matches the
   "never judge merit" design — but must NOT be counted as enforcement.

## B. The reframe — numeric problems vs EXPECTATIONS (the important part)
Earlier = real numerical/discretization problems (now mostly resolved: the seal-BC spectral-vs-warp mismatch that
catapulted Phi 2e-3→7e7 is FIXED; determined branch now imposes warp-Robin c'(ri)=-1/ri, d'(ri)=-1/ri,
e_tp'(ri)+(2/ri)e_tp=0). Now = **basin/branch-selection + expectation language.** The galerkin solve CAN move (6-order
descent). The "spurious branch / RIGHT branch / physical compact object" language is an **expectation headwind** that
violates the gate (check provenance/honesty, NEVER merit; don't discard a solution for being un-smooth/un-lumpy/
unexpected). NEUTRAL framing:
- **Branch A** = LM/crawl basin: alive dilaton, modest warp, residual ~2e-3, NOT floored.
- **Branch B** = cold-galerkin basin: low residual ~1.5e-5, dead dilaton/extreme warp, STILL physical-band (under-converged).
- Neither may be called "the physical object" until both are tested under identical diagnostics + a PRE-REGISTERED criterion.

## C. Best next test — BASIN AUDIT (classify, don't select)
Do NOT force "LM-to-close then galerkin-polish" as the only path (may preserve the expected object by construction).
Instead: (1) from the old LM/crawl field, apply small galerkin-polish steps; (2) from the cold-galerkin field, continue
with damped/line-searched physical-band reduction; (3) track BOTH with identical diagnostics; (4) if both floor, both
are UDT solutions unless a PRE-REGISTERED geometric criterion rejects one; (5) if only one floors, it's the stronger
candidate. **Frame:** "Do not find the compact object. Chart the UDT solution manifold and let compactness, dilation
survival, and mass localization EMERGE as diagnostics, not acceptance criteria."

## D. Fix order (auditor; driver concurs)
**Before the basin audit (only what could CONTAMINATE it):**
1. Remove "right/spurious branch" language → neutral Branch A/B (DONE in LIVE.md + memory 2026-06-30).
2. Basin-audit DRIVER passes ALL provenance explicitly (X, xi, kap, kap8, branch, p, wbc, determined, step, grid) —
   hard-code NO hidden choices; the entrypoint defaults (#A2) make this mandatory.
3. Emit a per-run MANIFEST: run_id, seed_type, start_field, X, xi, kap, kap8, branch, p, wbc, determined, step, grid,
   Phi, physical_residual_fraction, gauge_residual_fraction, Q, phi_max, warp_max, rho_max, lapse_min, accepted_steps.
**DEFER to before any PHYSICS claim (NOT blocking the basin audit):** A1 action-registry cleanup; A3 ledger upgrade
(token → call-path); A4 add determined=True tests; A5 split GR-baseline regression from live-UDT-action consistency;
A6 first-class conditional solver modes in the gate graph; A7 hooks-are-not-enforcement.
