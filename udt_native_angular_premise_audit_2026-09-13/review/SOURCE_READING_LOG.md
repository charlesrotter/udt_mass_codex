# Review source-reading command log

All paths below were read in /home/udt-admin/udt_mass_codex. Source-first reads ran between receipt of dispatch and the recorded 18:48:52 UTC freeze. Exact stdout/stderr was returned in the tool transcript; source byte correspondence is in SOURCE_FIRST_FREEZE.json. This log preserves executed read commands, not an independent transcript archive. Source files were not modified. The sole failed read was the absent .md source-pin filename, preserved below.

```sh
cat udt_native_angular_premise_audit_2026-09-13/review/SOURCE_FIRST_REQUEST.md
cat udt_native_angular_premise_audit_2026-09-13/WORK_ORDER.md
cat AGENTS.md
rg -n '^#|How we work|DRIVER TRIGGERS|repo discipline' CLAUDE.md
cat udt_native_angular_premise_audit_2026-09-13/SOURCE_PINS.md
# exit1: No such file or directory
sed -n '9,83p;121,134p' CLAUDE.md
rg --files udt_native_angular_premise_audit_2026-09-13 -g '*SOURCE_PIN*'
git branch --show-current
git rev-parse HEAD
cat .claude/skills/no-shortcuts/SKILL.md .claude/skills/completeness-map/SKILL.md .claude/skills/verifier-before-record/SKILL.md
cat udt_native_angular_premise_audit_2026-09-13/SOURCE_PINS.json
git status --short --branch
cat udt_local_kernel_symmetry_release_2026-09-13/REVIEWED_RESULT.md
cat udt_local_kernel_symmetry_release_2026-09-13/LEADING_JET_CLASSIFICATION.md
cat udt_g166_primary_metric_ordered_pair_kernel_descent_2026-08-18/AUDIT_REPORT.md
cat udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md
cat udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/AUDIT_REPORT.md
cat udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/AUDIT_REPORT.md
cat udt_g311_universal_reciprocity_full_covariant_response_2026-09-01/AUDIT_REPORT.md
cat udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md
rg -n 'W5|W6|Reciproc|sufficien|pair|metric|clock|ruler' founding.md
cat udt_local_kernel_symmetry_release_2026-09-13/SCOPE_CLARIFICATION.md
sed -n '61,140p;197,262p;539,592p;640,660p' founding.md
cat udt_local_kernel_symmetry_release_2026-09-13/INITIAL_CANDIDATE.md
cat udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/AUDIT_REPORT.md
cat udt_g214_completed_tuple_overlap_and_three_observer_carry_2026-08-22/AUDIT_REPORT.md
```

Three small metadata-only Python csv reads queried exact registry rows G166/G176/G179/G310/G311/G312, then compact term/active-use/source pointers matching shared_clock/incidence/carry/response_class/first_curvature, then exact G214/G215/G301 rows. They used csv.DictReader(delimiter='\t') and printed only selected rows/columns; no scientific computation.

After source-first freeze, still before NEW candidate exposure:

```sh
cat udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/AUDIT_REPORT.md
rg --files udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30 -g '*DERIVATION*' -g '*THEOREM*' -g '*SCOPE*' -g '*WORK_ORDER*'
cat CROSS_MODEL_VERIFY.md
cat udt_g301_scale_free_quiet_regular_causal_principal_classification_2026-08-30/EXACT_DERIVATION.md
```

No prior package executable or raw-array campaign was opened or rerun. No protected payload was read. Original source text includes historical scope/status wording; current exact registry and G312 authority controlled interpretation.

Further source-first reads for the independent checker, before NEW candidate exposure:

```sh
rg -n 'tangent|U|N|u\^|n\^|delta|dot|shape' udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md
sed -n '19,153p' udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md
```

Direct review after18:53:54.699071--18:54:01UTC exposure bracket:

```sh
cat udt_native_angular_premise_audit_2026-09-13/CANDIDATE_FREEZE.json
cat udt_native_angular_premise_audit_2026-09-13/INITIAL_CANDIDATE.md
cat udt_native_angular_premise_audit_2026-09-13/ADDITIONAL_SOURCE_PINS.json
cat udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/AUDIT_REPORT.md
cat udt_g235_rank_complete_matched_network_nonselection_2026-08-23/AUDIT_REPORT.md
cat udt_g182_completed_pair_two_sided_carry_classification_2026-08-19/AUDIT_REPORT.md
cat udt_g311_universal_reciprocity_full_covariant_response_2026-09-01/EXACT_DERIVATION.md
cat startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md
```

Metadata-only pin validation created DIRECT_EXPOSURE.json: every initial/additional source pin and candidate freeze pin matched. A read of own saved independent stdout printed all eight actual Ricci/TF/DDR case records. No new scientific computation was started for either action.

Post-verdict execution-evidence checks at18:56--18:57UTC:

```sh
rg --files /tmp -g 'udt_native_angular_premise_audit_2026-09-13_startup*'
# exit2: exact four target paths found; unrelated systemd-private/snap-private directory permission errors reported. No privileged data read or escalation attempted.
git diff --stat
# empty: no tracked diff at this check.
cat /tmp/udt_native_angular_premise_audit_2026-09-13_startup.json /tmp/udt_native_angular_premise_audit_2026-09-13_startup.capture_provenance.json
tail -n 4 /tmp/udt_native_angular_premise_audit_2026-09-13_startup.stdout
wc -c /tmp/udt_native_angular_premise_audit_2026-09-13_startup.stderr
```

Actual current saved startup evidence: verifier command python3 verify_current_scientific_premises.py, started18:41:45.245436UTC, duration405.2891067840392s, returncode0, timeoutfalse, maxRSS120192KiB, final406-row PASS, stderr0bytes. Reviewer independently inspected those saved records; this is not an independent rerun of full406. Exact scientific-check command, stdout, stderr, timing, code/result hashes and limits are separately preserved in INDEPENDENT_CHECK_EXECUTION.json and independent_center_check.stdout/.stderr.
