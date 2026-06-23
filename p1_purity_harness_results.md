# P1 PURITY HARNESS — RESULTS (SOLVER_INTEGRITY_UPGRADES_SPEC P1)

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-23. **MAP:** P1_PURITY_HARNESS_MAP.md (signed off).
**Status:** BUILT + blind-verified (VERIFIED). Files: `tests/test_solver_integrity.py`,
`tests/conftest.py`, `pytest.ini`. **Suite: 9 passed / 5 xfailed, <1s, no Newton/jacrev.**

## What it is
A pytest suite that fails LOUDLY when a past solver failure mode reappears, so integrity stops
depending on an agent remembering to check. Guards the CURRENT live production solver
(`p1_residual_general_einstein.py`) — Charles ruling 2026-06-23 "guard live solver now; RED
documents gaps".

**SPINE:** the harness REFERENCES derivations, it never RE-ASSERTS their results. No derived VALUE
(kap8=1, a=e^{φ}) is hard-coded; P1 checks the TAG is present, P2's action file sources the value.
This is what keeps the integrity layer from becoming a new import surface (Charles's embedding-risk
catch).

## The four checks (each anchored to a banked bug)
1. **Liveness** (`test_all_dofs_live`, `test_time_row_is_frozen_static`) — perturb each of the 8
   live DOFs (a,b,c,d,Θ,e_rt,e_rp,e_tp) on a GENERIC OFF-ROUND background; the residual must move.
   Verified to flow through the FIELD-EQUATION rows (1792–2395 Einstein rows + ~384 matter rows
   move; 0 BC rows) — not a boundary-row tautology. Time-row off-diagonals asserted frozen
   (STAGE-5 TODO, documented not silent).
2. **Provenance lint** (`test_no_smuggled_literal_in_operator` + 3 documented-gap xfails) — scans
   the operator-physics functions (`einstein_general_hybrid`, `residual_vector_p1`,
   `component_residuals_p1`) for un-allowlisted bare numeric literals. Allowlist is MINIMAL
   (`STRUCTURAL_INTS={0,1,2}`, `STRUCTURAL_FLOATS={0.0,1e-30}`) + line-anchored registered-gap
   sites (`stress_tensor(`). Catches a smuggled `kap8=0.05` AND a smuggled `1.0` on any non-stress
   line.
3. **Limit recovery** — `test_flat_limit_zero` (G=0 exactly), `test_schwarzschild_vacuum_N_convergent`
   (vacuum G→0, error non-increasing with Nr: 3.5e-3→2.0e-3→8.75e-4), `test_offdiag_zero_hybrid_equals_weyl`
   (pole-stable hybrid == analytic Weyl to <1e-12 when off-diagonals are zero), and
   **`test_de_sitter_operator_normalization`** — de Sitter (G^μ_ν=−Λ analytically) pins the operator
   NORMALIZATION, catching a constant rescale that the vacuum (G=0) tests cannot see.
4. **Native-object guard** — hard: `test_default_bc_is_not_skyrme_control`,
   `test_skyrme_mpi_ladder_is_control_only` (the m·π Skyrme ladder appears ONLY in the labeled
   negative-control branch). Documented-gap xfails characterize the live import: 4-component S³
   hedgehog, default `core_mode='deg1'` pinning Θ(0)=π.

## The 5 documented-gap xfails = the migration TODO (self-resolving tripwires)
These FAIL now (current = import) and will XPASS the day the production path is migrated to the
derived+native foundation — the XPASS is the signal to flip the guard to a hard assert. They are
NOT spurious failures; they are the live gap, made machine-visible:
- `test_kap8_callers_tagged` — kap8=1 (DERIVED) not propagated; callers pass untagged 0.05.
- `test_matter_couplings_tagged` — ξ=κ=1.0 hardcoded untagged at the stress call (FREE per F2).
- `test_derived_a_phi_in_operator` — live operator is the a=−1 GR baseline; a(φ)=e^{φ} not wired.
- `test_matter_winding_is_native_S2` — production matter is the 4-component S³ hedgehog, not n=x/r.
- `test_default_core_mode_is_native_free` — default `deg1` pins Θ(0)=π; native is the value-free node.

## Acceptance — CATCH-PROOF (the suite must BITE)
On throwaway scratch branches, each historical bug reintroduced → matching test RED, no masking:
- Dead off-diagonals (operator ignores e_rt,e_rp,e_tp) → ONLY `test_all_dofs_live` RED (e=0.0).
- Smuggled `kap8=0.05` in operator body → ONLY `test_no_smuggled_literal_in_operator` RED.
- Operator corruption (broken vacuum) → `test_flat_limit_zero`/Schwarzschild/offdiag RED.
- Skyrme control as default (`node_core=False`) → ONLY `test_default_bc_is_not_skyrme_control` RED.
Hardening holes (post-verifier) also proven to bite:
- Smuggled `1.0` on a non-stress line → `test_no_smuggled_literal_in_operator` RED (was a hole).
- Constant 2× rescale of the operator → `test_de_sitter_operator_normalization` RED (vacuum-invisible).
Repo restored byte-identical after every probe.

## Verifier trail (blind, fresh zero-context — P4 ruling)
- **Verifier 1** (agent a8d2dae18fdcecfc9, 2026-06-23): VERIFIED-WITH-CAVEATS. Confirmed 9/5… (8/5
  pre-hardening) split, catch-proof real, liveness flows through field equations, xfails honest
  (forced an XPASS), anti-hang clean. Raised 4 caveats: (1) lint blind to value-1.0 / small-int
  couplings; (2) vacuum tests scale-blind; (3) scans 3 of 7 functions; (4) stale @slow docstring.
- **Hardening** (this session): caveat 1 → line-anchored registered sites + STRUCTURAL_INTS={0,1,2};
  caveat 2 → de Sitter normalization anchor (analytic G=−Λ); caveat 4 → docstrings corrected;
  caveat 3 → accepted scope (the other 4 functions are solver-loop numerics, not couplings).
- **Verifier 2** (agent a1b23eea2004b7446, 2026-06-23): **VERIFIED.** Caveats 1, 2, 4 CLOSED —
  independently re-derived the de Sitter G=−Λ reference in sympy (R=4Λ, all mixed diagonals −Λ),
  confirmed the smuggled-1.0 catch and the 2×-rescale catch. No regressions.

## Honest residual notes (non-blocking, recorded)
- The de Sitter anchor is convergence-sensitive (not a flat identity): at the committed Nr=16 the
  error is 7.9e-13 vs 1e-9 tol (~10³ margin, healthy); Nr=8 would fail. Grid/tol are pinned in the
  test, so this is safe but not grid-decoupled.
- The registered-site excuse keys on the line substring, so a WRONG untagged coupling placed
  directly in the `stress_tensor(...)` arg list is still excused by the HARD test — but ξ/κ there
  are independently surfaced by the `test_matter_couplings_tagged` xfail.
- Caveat 3 stands by design: a physics constant placed in `newton_solve_p1`/`jacobian_p1` (solver
  loop) would be unscanned.

## Next (per spec ORDER P1→P2→P3)
P2 — operator-from-the-action codegen (single source-of-truth action; the values kap8/a(φ)/ξ/κ get
SOURCED here, which is what turns the 5 documented-gap xfails green). Then P3 disciplines-as-skills.
