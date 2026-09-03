# G337 R1 external repair follow-up

Scope honored: I inspected the sealed intake only, copied it to `/work`, and ran the decisive checks only against the writable copy at `/work/g337_r1_followup_clean`, with temporary outputs confined to `/work/g337_r1_runtime/tmp`. I did not modify `/intake`, access any repository, browse, download, or install packages.

## Authentication

1. [REVIEW_SCOPE.json](/work/g337_r1_followup_clean/REVIEW_SCOPE.json), [REVIEW_MANIFEST.tsv](/work/g337_r1_followup_clean/REVIEW_MANIFEST.tsv), and [REVIEW_MANIFEST.sha256](/work/g337_r1_followup_clean/REVIEW_MANIFEST.sha256) authenticated exactly. The detached seal matched `sha256(REVIEW_MANIFEST.tsv) = 248232c3534f1dc2fe06d329e352af8e7eee61cb3f2b4089eeb29232bbe44238`.
2. The manifest registered 39 payload rows. The copied intake contained exactly 41 files: those 39 payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. There were no extras and no missing files.
3. Every manifest payload matched its registered byte count and SHA-256.
4. The six frozen-source rows in [SOURCE_MANIFEST.tsv](/work/g337_r1_followup_clean/package/SOURCE_MANIFEST.tsv:1) all resolved and authenticated directly from the sealed `sources/` tree in the copied intake.

## Repair R1 verification

1. The repair preregistration states the defect and acceptance contract at [PREREGISTRATION_EXTERNAL_REPAIR.md](/work/g337_r1_followup_clean/package/PREREGISTRATION_EXTERNAL_REPAIR.md:9) and [PREREGISTRATION_EXTERNAL_REPAIR.md](/work/g337_r1_followup_clean/package/PREREGISTRATION_EXTERNAL_REPAIR.md:32).
2. [verify_package.py](/work/g337_r1_followup_clean/package/verify_package.py:37) now tries both `ROOT / relative` and `ROOT / "sources" / relative` with path-containment, size, and SHA-256 checks before the historical `git show` fallback at [verify_package.py](/work/g337_r1_followup_clean/package/verify_package.py:46).
3. I reran both the intake replay and the aggregate package verifier with `PATH` containing `python3` but no `git`. Both still passed. That proves the sealed replay succeeded from the authenticated `sources/` layout without Git history and without manual restaging.
4. The direct sealed replay path in [verify_review_intake.py](/work/g337_r1_followup_clean/package/verify_review_intake.py:25) authenticated the manifest, every payload, and the exact file set, then ran the aggregate verifier at [verify_review_intake.py](/work/g337_r1_followup_clean/package/verify_review_intake.py:46). Command result from the clean copy:

```text
G337 intake PASS: 39 payloads
G337 sealed package replay PASS: 69 aggregate gates
```

5. A separate direct run of [verify_package.py](/work/g337_r1_followup_clean/package/verify_package.py:55) from the clean copy also passed and reproduced [PACKAGE_VERIFICATION_RESULT.json](/work/g337_r1_followup_clean/package/PACKAGE_VERIFICATION_RESULT.json) byte-for-byte:

```text
G337 package PASS: 69 aggregate gates
```

## Output identity and unchanged bounded claims

1. Fresh reruns of the three registered generators reproduced the registered outputs byte-for-byte:
   - [DERIVATION_RESULT.json](/work/g337_r1_followup_clean/package/DERIVATION_RESULT.json) matched exactly; `checks_passed = 149`.
   - [INDEPENDENT_VERIFICATION.json](/work/g337_r1_followup_clean/package/INDEPENDENT_VERIFICATION.json) matched exactly; `check_count = 26`.
   - [CATCH_PROOF_RESULT.json](/work/g337_r1_followup_clean/package/CATCH_PROOF_RESULT.json) matched exactly; `mutations_caught = 17`.
2. The bounded landing constant in [verify_package.py](/work/g337_r1_followup_clean/package/verify_package.py:18) was reproduced exactly by the production replay. No landing drift was observed.
3. The aggregate verifier also rechecked the unchanged bounded scientific and premise anchors:
   - preregistered identity at [PREREGISTRATION.md](/work/g337_r1_followup_clean/package/PREREGISTRATION.md:51)
   - hand-structure disclosure at [PREREGISTRATION.md](/work/g337_r1_followup_clean/package/PREREGISTRATION.md:94)
   - unchanged derivation statements at [EXACT_DERIVATION.md](/work/g337_r1_followup_clean/package/EXACT_DERIVATION.md:63), [EXACT_DERIVATION.md](/work/g337_r1_followup_clean/package/EXACT_DERIVATION.md:71), and [EXACT_DERIVATION.md](/work/g337_r1_followup_clean/package/EXACT_DERIVATION.md:120)
   - unchanged lay bounds at [LAY_REPORT.md](/work/g337_r1_followup_clean/package/LAY_REPORT.md:14) and [LAY_REPORT.md](/work/g337_r1_followup_clean/package/LAY_REPORT.md:20)
   - unchanged premise stamps at [PREMISE_LEDGER.tsv](/work/g337_r1_followup_clean/package/PREMISE_LEDGER.tsv:2) and [PREMISE_LEDGER.tsv](/work/g337_r1_followup_clean/package/PREMISE_LEDGER.tsv:15)
4. [REPAIR_IMPLEMENTATION.md](/work/g337_r1_followup_clean/package/REPAIR_IMPLEMENTATION.md:7) and [REPAIR_IMPLEMENTATION.md](/work/g337_r1_followup_clean/package/REPAIR_IMPLEMENTATION.md:19) are consistent with the executed evidence: the repair changed the replay packaging path, not the registered mathematical outputs.

## Assessment

The preregistered R1 defect was real: the external preregistration records that the earlier sealed layout forced a fallback to unavailable Git history unless a reviewer manually reconstructed the root layout. The corrected intake now satisfies the requested repair. In a clean writable copy, the intake authenticated exactly, the direct `verify_review_intake.py --replay-package` command passed all 69 aggregate gates, the aggregate JSON was reproduced byte-for-byte, the three registered outputs remained byte-identical, and the bounded landing and premise anchors remained unchanged. The retained `git` fallback in [verify_package.py](/work/g337_r1_followup_clean/package/verify_package.py:46) is not a blocker because the same replay succeeded when `git` was unavailable.

REPAIRS_ACCEPTED__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED
