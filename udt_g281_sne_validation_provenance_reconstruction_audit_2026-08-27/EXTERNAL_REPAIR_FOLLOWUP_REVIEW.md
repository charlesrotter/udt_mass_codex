**Verdict**

Primary verdict: `ACCEPT`.

**Seal And Count Results**

- Outer seals match exactly: `REVIEW_SCOPE.json` `9a89c65d4078887006fa398d8978cce47a71f8abeb3bae5591c759f7346c9b72`, `REVIEW_MANIFEST.tsv` `6641d3f315fb399d9ee1b8c597d6c57b969ae6c0ff5d651cbd716f717d829b57`, `REVIEW_MANIFEST.sha256` `8113094bbf74682791ad7002ec942dd47ab0c77260f9e0392e695797b8de35fb`.
- Detached manifest seal passes: `REVIEW_MANIFEST.tsv: OK`.
- Manifest payload verification passes: `65/65` listed payloads matched recorded SHA-256 and byte size.
- Physical file count is `67`. Symlink count is `0`.

**R1-R4**

- `R1 PASS`: [SOURCE_SCOPE.tsv](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/SOURCE_SCOPE.tsv:1) and [SOURCE_MANIFEST.tsv](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/SOURCE_MANIFEST.tsv:1) contain the same exact `32` paths, in the same order; all `32` scoped files exist and hash-match. The repaired verifier enforces exact scope/manifest equality and source hash checks [verify_sne_provenance_audit.py](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_sne_provenance_audit.py:107). The mutable-file exemption is removed per [REPAIR_RESULT.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/REPAIR_RESULT.md:18) and [PREREGISTRATION_EXECUTION_NOTE.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/PREREGISTRATION_EXECUTION_NOTE.md:9).
- `R2 PASS`: [ROUTE_PROVENANCE_MATRIX.tsv](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/ROUTE_PROVENANCE_MATRIX.tsv:1) retains exactly six prediction gates; gate 1 is explicitly `history_metric_owned_or_physically_selected_and_fixed_before_SNe`. [ROUTE_PROVENANCE_MATRIX.tsv](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/ROUTE_PROVENANCE_MATRIX.tsv:7) gives `G79_same_geometry_control` = `NO` on gate 1 and `NATIVE_CONDITIONAL_EVALUATION`. Current tables remain `24` historical-tile rows and `15` route rows, with no `NATIVE_PREDICTION` route; the repair record states no route class changed and no route was promoted [REPAIR_RESULT.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/REPAIR_RESULT.md:29).
- `R3 PASS`: [COMMANDS.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/COMMANDS.md:5) lists exactly the four intake-resident runnable commands. [COMMANDS.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/COMMANDS.md:12) labels G279/G280 commands as repository-recorded historical evidence only. [EVIDENCE_GATES.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/EVIDENCE_GATES.md:21) states the saved-output script is a consistency replay, not a fresh derivation, and [AUDIT_REPORT.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/AUDIT_REPORT.md:186) preserves the same distinction.
- `R4 PASS`: active source/scope statements use `CURRENT_SCIENTIFIC_PREMISES.tsv` in [STALE_CLAIM_SCAN.tsv](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/STALE_CLAIM_SCAN.tsv:13) and [PREREGISTRATION_EXECUTION_NOTE.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/PREREGISTRATION_EXECUTION_NOTE.md:4). Exact `CURRENT_SCIENTIFIC_PREMISES.md` appears only in defect/repair quotation contexts: [EXTERNAL_REPAIR_PREREGISTRATION.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/EXTERNAL_REPAIR_PREREGISTRATION.md:29), [EXTERNAL_REVIEW.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/EXTERNAL_REVIEW.md:23), and [EXTERNAL_REVIEW_TRANSMISSION.md](/intake/udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/EXTERNAL_REVIEW_TRANSMISSION.md:50).

**Registered Command Outcomes**

- `python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_sne_provenance_audit.py`: exit `0`, `status: PASS`, landing `NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE`.
- `python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_sne_provenance_independent.py`: exit `0`, `status: PASS`, operational control `Z=2.75`, `R=17.0`, ratio `2.75`.
- `python3 udt_g281_sne_validation_provenance_reconstruction_audit_2026-08-27/verify_saved_lineage_outputs.py`: exit `0`, `status: PASS`, including `M3_P1_chi2=1260.8480887040496`, `G278_resolution_chi2=60.40538886961107`, `G278_resolution_ceiling=15.24744871391589`.
- `python3 verify_luminosity_distance_n2.py`: exit `0`; symbolic checks `(A)` through `(D)` passed and it printed `CONCLUSION: d_L = (1+z)^2 * D_A = r e^{2phi} = r * g_rr   (n = 2, FORCED)`.

Remaining scoped defect: none found.

The bounded G281 scientific landing did not change. No metric, kernel, history, transfer law, observational result, score, scale, `X_max`, or substantive scientific classification changed within the sealed repair scope.
