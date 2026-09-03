# External Repair Follow-up: G332

Date: 2026-09-03

Scope discipline was preserved. I inspected only `/intake`, used one writable ephemeral replay copy at `/work/g332_followup_8wdrvb1u`, did not edit evidence files, and did not access any repository, protected package, or network resource.

## Authentication

- [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:1) authenticated at `sha256=3ff86d10726e30952353547490a4ad1cfe1885f5ab8eb0d9b228374e39505c5d`, matching [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:2).
- The detached seal in `/intake/REVIEW_MANIFEST.sha256` authenticated the manifest exactly: `sha256sum -c /intake/REVIEW_MANIFEST.sha256` returned `REVIEW_MANIFEST.tsv: OK`, and the manifest digest is `57630f165e728e4eca8e6dd0d5b42c6b4c9b896f6f535a9732d4038529360169`.
- The manifest contains 44 payload rows. I verified every payload's existence, byte count, and SHA-256 against [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1); all 44 matched.
- The sealed source registry contains 12 rows in [SOURCE_MANIFEST.tsv](/intake/package/SOURCE_MANIFEST.tsv:1). All 12 source payloads authenticated with their registered byte counts and SHA-256 digests.

## R1: Sealed Source Resolution

R1 was preregistered in [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:13). The repaired verifier now resolves paths from the intake-local source subtree when present:

- [verify_package.py](/intake/package/verify_package.py:15) defines `ROOT`, `REPO`, and `SEALED_SOURCE_ROOT = REPO / "sources"`.
- [verify_package.py](/intake/package/verify_package.py:125) selects `source_root = SEALED_SOURCE_ROOT if SEALED_SOURCE_ROOT.is_dir() else REPO`.
- [verify_package.py](/intake/package/verify_package.py:128) rejects absolute paths and `..` segments.
- [verify_package.py](/intake/package/verify_package.py:132) enforces containment under the resolved source root before accepting a path.
- [verify_package.py](/intake/package/verify_package.py:134) through [verify_package.py](/intake/package/verify_package.py:136) verify existence, byte count, and SHA-256 for every source row.

In the actual replay copy, all 12 `SOURCE_MANIFEST.tsv` rows resolved inside `/work/g332_followup_8wdrvb1u/sources/...`; every row was `safe=True`, `contained=True`, `exists=True`, `size_ok=True`, and `sha_ok=True`.

I also checked the verifier's dependency surface. [verify_package.py](/intake/package/verify_package.py:6) imports only Python standard-library modules, and its internal replays invoke the three subordinate scripts with `python3 -S` at [verify_package.py](/intake/package/verify_package.py:29). No repository path outside the writable copy is referenced anywhere in the source-resolution logic.

## Literal Replay In One Writable Copy

I ran the four registered commands from [REPLAY_COMMANDS.txt](/intake/package/REPLAY_COMMANDS.txt:1) literally, in order, in `/work/g332_followup_8wdrvb1u/package`:

1. `python3 derive_weighted_constraint_embedding.py --output DERIVATION_RESULT.json`
2. `python3 verify_weighted_constraint_embedding_independent.py --output INDEPENDENT_VERIFICATION.json`
3. `python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json`
4. `python3 verify_package.py`

All four passed:

- production replay: `checks_passed=642`, `sample_count=80`
- independent replay: `checks_passed=65`, `verdict=PASS`
- catch proofs: `mutations_caught=9`, `verdict=PASS`
- aggregate verifier: `G332 package PASS: 91 aggregate gates`

The three registered generated JSON artifacts reproduced byte-for-byte against the sealed intake:

- `DERIVATION_RESULT.json`: `40106` bytes, `sha256=ab2fbcd4c65cbb4ab2b58f0bffb939be32b08fa4768f018f656726a0c5f97f5a`
- `INDEPENDENT_VERIFICATION.json`: `13395` bytes, `sha256=88248cff9763d880ef229ffce4a53d93979b57aaa8cddc584c6175bb0e73d6b3`
- `CATCH_PROOF_RESULT.json`: `475` bytes, `sha256=9fb51091cf158a131e728307b21c2afa23233105daf3b4b7776e91966670d4b1`

For completeness, `PACKAGE_VERIFICATION_RESULT.json` also reproduced byte-for-byte: `3195` bytes, `sha256=000ae200fc8ce4584ab34ac6a5a76c25afb8d40cefb447fc402440fbfa79a50b`.

## R2: Tensor Index Convention

R2 was preregistered at [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:30). The repaired derivation now makes the index convention explicit and type-consistent:

- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:45) states that the momentum calculation uses the contravariant tensor `P^ij = K^ij - tau gamma^ij`.
- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:50) keeps the contravariant product `xi^i xi^j` in that momentum expression.
- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:86) gives the later unindexed covariant form `K = ((C-b)/2) gamma + b xi_flat tensor xi_flat`.
- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:90) explicitly states that this `K` is obtained by lowering both indices, and that `xi^i xi^j` becomes `xi_flat tensor xi_flat`.

I found no coefficient, sign, trace inversion, eigenvalue, residual, branch, or conclusion change in the repaired derivation. The same formulas remain in force:

- constraints at [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:35)
- trace inversion at [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:86)
- Hamiltonian quadratic at [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:110)
- two algebraic branches at [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:122)
- unchanged weighted metric and Killing field at [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:159)

## Unchanged Bounded Scientific Landing

The bounded landing remained unchanged across the repaired package:

- [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:10) through [EXACT_DERIVATION.md](/intake/package/EXACT_DERIVATION.md:12)
- [AUDIT_REPORT.md](/intake/package/AUDIT_REPORT.md:9) through [AUDIT_REPORT.md](/intake/package/AUDIT_REPORT.md:11)
- [derive_weighted_constraint_embedding.py](/intake/package/derive_weighted_constraint_embedding.py:359)
- [DERIVATION_RESULT.json](/intake/package/DERIVATION_RESULT.json:655)
- [PACKAGE_VERIFICATION_RESULT.json](/intake/package/PACKAGE_VERIFICATION_RESULT.json:98)

The bounded scope boundary also remained unchanged:

- [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:7) through [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:11) freeze the metric family, witness, equations, branches, finite connected `Lambda`, and bounded landing.
- [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:44) through [REPAIR_PREREGISTRATION.md](/intake/package/REPAIR_PREREGISTRATION.md:47) retain the maximum conclusion as externally accepted bounded `DERIVED_CONDITIONAL` existence only.
- [STATUS_LEDGER.tsv](/intake/package/STATUS_LEDGER.tsv:14) records `metric_kernel_angular_equation	UNCHANGED	G332 adds constraint data only`.

## Conclusion

Both preregistered repairs pass exactly as requested. R1 is fixed in the sealed replay path and verifies all 12 sealed sources inside the intake-local `sources/` subtree without repository dependence. R2 is fixed in the written derivation by explicitly separating contravariant momentum notation from the lowered covariant `K`, while preserving the same equations, coefficients, branches, metric, provenance boundaries, and bounded scientific landing. The literal four-command replay succeeded in one writable copy, and the sealed generated artifacts reproduced byte-for-byte.

REPAIRS_ACCEPTED__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED
