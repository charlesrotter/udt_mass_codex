# G330 R3-completion-only external mathematical referee report

Date: 2026-09-02
Role: zero-context R3-completion-only external referee
Intake inspected: `/intake`
Writable replay copy: `/work/g330_intake_r3_b3Ngue`

## Scope

I reviewed only the sealed intake and only the frozen completion described in
`/intake/package/R3_COMPLETION_FOLLOWUP_REQUEST.md` and
`/intake/package/R3_COMPLETION_PREREGISTRATION.md`. I did not continue the research, change the
scientific question, introduce a different repair, access another repository, or edit intake
evidence files.

## 1. Intake authentication and registered-command replay

Using the intake verifier at `/intake/package/verify_review_intake.py`, whose checks cover the
detached seal, manifest, payload byte counts, payload SHA-256 values, safe relative paths, and
sealed-tree completeness ([verify_review_intake.py](/intake/package/verify_review_intake.py:21)),
I authenticated:

- `/intake`: `G330 sealed intake authentication PASS: 48 payloads; 50 files`
- `/work/g330_intake_r3_b3Ngue`: `G330 sealed intake authentication PASS: 48 payloads; 50 files`

I then ran the four registered commands listed in
[COMMANDS.md](/intake/package/COMMANDS.md:1) from one writable copy only, namely
`/work/g330_intake_r3_b3Ngue/package`:

1. `python3 -S derive_berger_hopf.py --output DERIVATION_RESULT.json`
   Result: `G330 production PASS: 39 exact checks`
2. `python3 -S verify_berger_hopf_independent.py --output INDEPENDENT_VERIFICATION.json`
   Result: `G330 independent PASS: 40 exact checks`
3. `python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json`
   Result: `G330 hostile PASS: 8/8 caught`
4. `python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json`
   Result: `G330 package PASS: 178 aggregate gates`

The generated aggregate verifier output confirms `all_passed: true`, `check_count: 178`, the same
bounded landing string, five explicit `r3_explicit_*` gates, all 15 sealed source rows, and
byte-exact command replay checks
([PACKAGE_VERIFICATION_RESULT.json](/work/g330_intake_r3_b3Ngue/package/PACKAGE_VERIFICATION_RESULT.json:1)).

## 2. R3 completion check

The exact phrase `isometry-extension consequence` now appears in all five required R3 records:

- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:164)
- [LAY_REPORT.md](/intake/package/LAY_REPORT.md:16)
- [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:10)
- [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:8)
- [EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:28)

Each occurrence also preserves the required dependency and scoping:

- `EXACT_DERIVATION.md` states the local persistence step is conditional on the general imported
  smooth marked Einstein-Cauchy existence/uniqueness theorem and its standard isometry-extension
  consequence, and says G321 is a registered scoped application/interface, not a proof of the
  general theorem for Berger data
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:164)).
- `LAY_REPORT.md` states the same dependency in lay language and says G321 recorded an earlier
  scoped use but did not prove the theorem
  ([LAY_REPORT.md](/intake/package/LAY_REPORT.md:14)).
- `PREMISE_LEDGER.tsv` classifies the theorem as `IMPORTED_MATHEMATICAL_METHOD` and says G321 is a
  scoped application/interface, not a proof or UDT law
  ([PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:10)).
- `STATUS_LEDGER.tsv` keeps `local_time_persistence` conditional on the general imported
  Einstein-Cauchy uniqueness statement, with the theorem’s standard isometry-extension consequence,
  and again limits G321 to application/interface status
  ([STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:8)).
- `EVIDENCE_GATES.md` now states the local persistence dependence explicitly and limits G321 to its
  registered scoped application/interface role
  ([EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:28)).

This matches the frozen preregistered repair and the strengthened verifier requirement in
[verify_package.py](/intake/package/verify_package.py:137).

## 3. Non-regression and bounded scientific landing

I found no evidence that the R3 completion changed the scientific question or broadened the claim.

- The bounded landing remains exactly
  `NONROUND_BERGER_S3_METRIC_DEFINES_INTRINSIC_HOPF_EIGENLINE__NORMALIZED_ABSOLUTE_HELICITY_ONE__LOCAL_SMOOTH_EINSTEIN_DEVELOPMENT_PRESERVES_WHILE_GAP_OPEN__ROUND_AND_OTHER_TOPOLOGY_CONTROLS_BLOCK_UNIVERSAL_SELECTOR`
  in [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:210),
  [AUDIT_REPORT.md](/intake/package/AUDIT_REPORT.md:6), and the replayed package verifier output
  ([PACKAGE_VERIFICATION_RESULT.json](/work/g330_intake_r3_b3Ngue/package/PACKAGE_VERIFICATION_RESULT.json:186)).
- The Hopf normalization remains intrinsic and metric-measured, not external-scale based, in
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:9) and
  [EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:27).
- The persistence scope remains local and bounded: a nonzero interval while the eigengap stays open,
  not global persistence
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:176),
  [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:8)).
- The nonselector and open-boundary controls remain in place: no global persistence, no occupancy
  selection, no transferred historical stability, no matter/mass/source law, and no scale or
  `X_max` upgrade
  ([EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:181),
  [LAY_REPORT.md](/intake/package/LAY_REPORT.md:22),
  [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:9),
  [PREMISE_LEDGER.tsv](/intake/package/PREMISE_LEDGER.tsv:11),
  [EVIDENCE_GATES.md](/intake/package/EVIDENCE_GATES.md:24),
  [AUDIT_REPORT.md](/intake/package/AUDIT_REPORT.md:82)).
- The replayed verifier also enforces the unchanged bounded structure through `status_token_*`,
  `premise_token_*`, `exact_landing`, `production_no_*`, `independent_nonselector`, and forbidden
  token absence checks, all of which passed
  ([verify_package.py](/intake/package/verify_package.py:92),
  [PACKAGE_VERIFICATION_RESULT.json](/work/g330_intake_r3_b3Ngue/package/PACKAGE_VERIFICATION_RESULT.json:35)).

## Conclusion

The sealed intake authenticated cleanly. All four registered commands replayed successfully from one
writable copy. The preregistered R3 completion is implemented exactly where requested, with the
explicit `isometry-extension consequence` wording now present in all five required records, and each
record preserves the imported-theorem dependence while confining G321 to a scoped
application/interface role. I found no regression in metric content, equations, Berger data, Ricci
results, Hopf normalization, persistence scope, or the bounded scientific landing, and no new
global stability, conservation, occupancy, matter/mass, scale, `X_max`, or canon claim.

R3_COMPLETION_ACCEPTED__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED
