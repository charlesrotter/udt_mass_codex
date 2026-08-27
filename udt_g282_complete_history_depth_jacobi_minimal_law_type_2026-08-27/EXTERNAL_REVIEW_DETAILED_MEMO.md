# External Review: G282

Verdict: `ACCEPT-WITH-REPAIRS`

Strongest source-bounded landing:

```text
NO_OWNED_JOINT_HISTORY_LAW__NEIGHBOR_RELATION_CURVATURE_CONSTRAINT_REQUIRED
__COMPLETE_CENTRAL_METRIC_AND_FIRST_JET_DO_NOT_FIX_REGULAR_JACOBI_AREA
__EQUAL_PRIMARY_DEPTH_DOES_NOT_FIX_ONE_AREAL_POSITION
__ALLOWED_MISSING_LAW_HOME_NOT_UNIQUELY_SECOND_ORDER_METRIC_PDE
```

Scope compliance:

- I inspected only `/intake`, used `/work` for a writable replay copy, and wrote this memo in `/return`.
- I did not inspect any authentication file, any protected package, or any path outside `/intake`, `/work`, and `/return`.

Intake integrity findings:

1. `REVIEW_SCOPE.json` matches the requested hostile read-only bounded mode and forbids adopting a replacement law, importing field equations, outcomes, fits, scales, or `X_max`: `/intake/REVIEW_SCOPE.json`.
2. The detached seal file `/intake/REVIEW_MANIFEST.sha256` matches the SHA-256 of `/intake/REVIEW_MANIFEST.tsv`.
3. Every manifest payload hash and byte count in `/intake/REVIEW_MANIFEST.tsv` matched on disk at review time: `42/42` entries verified.
4. No symlinks were present anywhere under `/intake`.

Registered replay findings:

1. I copied `/intake` to `/work/intake_copy_g282_audit` and ran only the five registered no-write commands listed in `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/COMMANDS.md:1-35`.
2. All five commands exited zero and reproduced `PASS` outputs consistent with `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/DERIVATION_RESULT.json:1-50`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/INDEPENDENT_VERIFICATION.json:1-14`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/CATCH_PROOF_RESULT.json:1-16`, and `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/VERIFICATION_RESULT.json:1-41`.

Direct answers to the seven review questions:

1. Yes. The Brinkmann witness does preserve the full central metric matrix, all first derivatives, and the central Christoffels on the ray `x=y=0`, while separating transverse curvature and regular pre-caustic Jacobi area. The exact witness and equations are stated in `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/EXACT_DERIVATION.md:16-66`, and the replay script checks the same points in `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/derive_minimal_law_type.py:58-139`.
2. Yes. The primary witness really shows that equal reciprocal depth does not pick one areal position: at depth `2`, `phi_A(s)=s^2` gives `s_A=sqrt(2)` while `phi_B(s)=s^2+s^4` gives `s_B=1`. See `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/EXACT_DERIVATION.md:71-93`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/PREREGISTRATION.md:71-82`, and `/intake/udt_g280_projective_position_optical_area_bridge_audit_2026-08-27/AUDIT_REPORT.md:24-30`.
3. No frozen source I audited already owns a nonidentity law jointly generating depth values and neighboring-ray curvature/Jacobi evolution. The founding file itself says the open object is what fixes or propagates the valued score, explicitly allows non-PDE or global-relation possibilities, and rules out automatic closure by Einstein, Cartan/Bianchi identities, or Jacobi propagation alone: `/intake/founding.md:23-38`, `/intake/founding.md:742-766`, `/intake/founding.md:821-909`. The retrospective frozen-universe audit also reports zero owned nonidentity local metric conditions and zero owned nonidentity global relation laws: `/intake/udt_g255_g165_g254_lost_closure_recovery_audit_2026-08-24/AUDIT_REPORT.md:48-95`. G256 reaches the same bounded ownership result on the primary state: `/intake/udt_g256_primary_state_value_closure_rank_2026-08-25/AUDIT_REPORT.md:13-30`.
4. No. W3, W4, G262, G271, and the complete coframe were not unfairly demoted. W3 is only a quiet-regime reduction requirement and imported GR comparator, not a derived field law: `/intake/founding.md:141-154`, `/intake/udt_g260_gr_quiet_angular_nondiscard_audit_2026-08-25/AUDIT_REPORT.md:40-46`. W4 states one metric controls clocks, free fall, and null propagation, but does not select a field equation or source/history law: `/intake/founding.md:199-210`, `/intake/udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/AUDIT_REPORT.md:14-17`. G262 is an exact static hierarchy that still holds for arbitrary positive profiles and therefore does not propagate profile values: `/intake/udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/AUDIT_REPORT.md:81-91`, `/intake/udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/AUDIT_REPORT.md:107-110`. G271 is a local first-jet interlock that still requires a supplied profile and supplied null branch: `/intake/udt_g271_primary_metric_null_screen_first_jet_interlock_2026-08-26/AUDIT_REPORT.md:68-73`. The coframe/connection route is correctly typed as a realization architecture that integrates compatible supplied data but does not choose curvature values or a physical history unless a classifying law is added: `/intake/udt_g231_cartan_regional_realization_bridge_2026-08-23/AUDIT_REPORT.md:33-50`, `/intake/udt_g231_cartan_regional_realization_bridge_2026-08-23/AUDIT_REPORT.md:76-85`, `/intake/udt_g231_cartan_regional_realization_bridge_2026-08-23/AUDIT_REPORT.md:97-103`.
5. Yes. The minimum missing information is typed correctly as one of three allowed homes: a nonidentity complete-metric two-jet/curvature law, an equivalent first-order coframe/connection/curvature system, or a genuinely value-bearing global neighboring-relation law. This is preregistered and repeated consistently in `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/PREREGISTRATION.md:42-55`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/EXACT_DERIVATION.md:106-117`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/STATUS_LEDGER.tsv:8-10`, and `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/DERIVATION_RESULT.json:29-40`.
6. Yes. The package does avoid falsely privileging a second-order metric PDE and avoids importing Einstein equations, action, source, observations, fits, scale, or `X_max`. The preregistration forbids that overreach: `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/PREREGISTRATION.md:52-55`, `/intake/founding.md:897-909`. The derivation explicitly says the second-order metric PDE is not uniquely implied and no such imports are used: `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/EXACT_DERIVATION.md:108-117`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/DERIVATION_RESULT.json:35-41`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/VERIFICATION_RESULT.json:19-40`.
7. Mostly yes on the science, but not cleanly yes on every certification layer. The exact derivation and the separate RK4 replay are genuinely noncircular with respect to the main mathematics: `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/derive_minimal_law_type.py:58-197`, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/verify_independent.py:1-102`. However, the hostile-catch layer is only a schematic claim-logic guard, not an artifact-level mutation replay: `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/run_catch_proofs.py:9-62`. And the package verifier is intentionally a fail-closed consistency checker that reads saved JSON/report artifacts rather than independently recomputing them: `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/verify_package.py:29-158`.

Required repairs:

1. Repair the certification wording around hostile catches. As written, `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/AUDIT_REPORT.md:98-100` can be read as stronger than what `/intake/udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/run_catch_proofs.py:9-62` actually certifies. The script tests a boolean claim schema, not mutated evidence files, mutated derivation code, or mutated source-census artifacts. The report should either say exactly that, or the catch layer should be upgraded to actual artifact mutations and bounded replay checks.

Bottom line:

The hostile mathematical and provenance audit supports the package’s bounded scientific landing. The two witnesses are valid, the frozen 18-source universe does not already own the missing joint history law, the coframe/connection alternative is retained correctly, and the package does not smuggle in Einstein, action, source, fit, scale, observation, or `X_max`. I do not support `ACCEPT` because the hostile-catch certification is overstated relative to the script that implements it. With that repair, the bounded landing is acceptable.
