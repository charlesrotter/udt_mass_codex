# Fresh-context adversarial review prompt

You are an independent adversarial reviewer in the UDT repository. Perform a read-only review. Do
not edit files, run long computations, browse the web, or use conversational context outside the
repository.

Read `AGENTS.md`, then audit the uncommitted package
`asymptotic_boundary_lineage_audit_2026-07-19/`, especially `PREREGISTRATION.md`, `AUDIT_REPORT.md`,
all TSV ledgers, `DERIVATION_RESULT.json`, `VERIFICATION_RESULT.json`, and both Python scripts.
Independently inspect these load-bearing repository sources:

- `CANON.md` clauses C-2026-07-02-1, C-2026-07-04-1, and C-2026-07-09-1/1a;
- `universe_cell_fold_jc_sigma_results.md`;
- `archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md`;
- `archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md`;
- `UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md`; and
- `native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md`.

Attempt to falsify, in order:

1. the claim that the recorded CMB outer fold and WR-L wall are distinct;
2. the finite-proper/infinite-optical/finite-curvature/regular-horizon WR-L limit calculation;
3. the ruling that WR-L `X` remains supplied and is not yet global `X_max`;
4. the ruling that Misner-Sharp mass and raw lapse flux are not native total mass;
5. the dimensional-rank ruling that observed `c_E,G_obs` alone calibrate mass per length but do not
   select absolute `M_tot,X_max` without an independent native scale condition; and
6. compliance with the July-1 provenance firewall and the preregistered maximum conclusion.

Look specifically for swapped phi conventions, notation-only surface joins, nonuniform limits,
coordinate artifacts, hidden action/source assumptions, a missing independent equation, vacuous
catch-proofs, candidate-census omissions, and claims stronger than their premise stamps.

Return only:

- `VERDICT: PASS`, `PASS_WITH_REQUIRED_CORRECTIONS`, or `FAIL`;
- load-bearing findings with file/line references;
- any exact required correction;
- whether each of the six challenges survives; and
- the strongest conclusion the evidence supports.

