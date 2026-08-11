**Findings**
1. [replay_m3_unchanged.py](/tmp/udt_sne_native_query_review_u1ilD0/udt_sne_native_observer_query_replay_2026-08-11/replay_m3_unchanged.py:73) is numerically strict but not type-strict: float leaves are accepted after `float(replay)` coercion. A replay artifact with stringified numerics would still pass the recursive equality gate, so the comparison can hide a type mismatch even when the numeric values are identical.

**Verdict**
Primary verdict: `VERIFIED_WITH_CAVEATS`.

All `37/37` manifest entries matched their SHA-256. Direct execution of the five packaged reruns failed only at the final overwrite step because the intake is read-only; rerunning the same `run()` paths with file writes suppressed preserved the computation and produced these observed values:

- replay: `PASS`, `18` fits, `443` compared leaves, max abs diff `0.0`
- A:`zCMB`:P1: `1/n=0.9470295666076658`, `n=1.0559332414320268`, `chi2/dof=1260.8480887040496/1365`, `offset_B=22.343528501617104`
- B:`zCMB`:P1: `X_eff=2085.9586748597476 Mpc`, `R_w at best n=2202.6331050379085 Mpc`
- equivalence: `PASS`, `9/9` checks, `formula_change_from_retyping=false`
- independent P1: `1/n=0.9470305108426823`, `n=1.0559321886157444`, `chi2=1260.8480887249352`, `Delta chi2(n=1)=7.944900501660641`, `2.8186699880725024 sigma`, `X_eff=2085.9590069567967 Mpc`
- catches: `PASS`, `14/14` rejected
- package verifier: `PASS`, `38` checks

The maximum warranted claim remains `BASELINE_REPRODUCED__NATIVE_RETYPE_ALGEBRAICALLY_IDENTICAL` and `NO_OWNED_COMPLETE_SNE_QUERY_CORRECTION`. The sealed sources support that boundary: `phi_pair` and `c_eff^(pair)/c_E` are only conditional on a supplied calibrated pair and supplied pair cone [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/AUDIT_REPORT.md:25), [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md:16); `d_A=r` and `d_L=(1+z)^2r` remain conditional readout premises [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_pair_space_metric_transform_sne_readout_audit_2026-07-24/AUDIT_REPORT.md:33), [EXACT_DERIVATION.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_sne_native_observer_query_replay_2026-08-11/EXACT_DERIVATION.md:53); phi+orchestra modulation is structurally retained but no physical cocycle is selected [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md:12); the actual time-live path through that atlas is not owned [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_pair_instrument_mixing_solution_space_audit_2026-08-10/AUDIT_REPORT.md:17); the common-query package evaluates supplied realizations but does not select a physical query or branch [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_common_query_pair_immersion_reconstruction_2026-08-11/AUDIT_REPORT.md:21); and N03 keeps P1 in its observer-pair/SNe role while denying any role-correct complete global profile [AUDIT_REPORT.md](/tmp/udt_sne_native_query_review_u1ilD0/udt_cmb_N03_profile_role_regular_center_map_2026-08-09/AUDIT_REPORT.md:9). Bootstrap is inactive and no on-shell history law is owned in [CURRENT_SCIENTIFIC_PREMISES.tsv](/tmp/udt_sne_native_query_review_u1ilD0/CURRENT_SCIENTIFIC_PREMISES.tsv:13) and [CURRENT_SCIENTIFIC_PREMISES.tsv](/tmp/udt_sne_native_query_review_u1ilD0/CURRENT_SCIENTIFIC_PREMISES.tsv:61).

Smallest justified next step: tighten the replay comparator to reject stringified float leaves instead of accepting `float(...)` coercions. No further scientific step is justified from this sealed intake.
