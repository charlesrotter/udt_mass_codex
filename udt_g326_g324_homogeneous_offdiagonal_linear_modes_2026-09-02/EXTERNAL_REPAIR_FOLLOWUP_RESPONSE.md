# External Repair Follow-Up Response

Date: 2026-09-02
Reviewer mode: fresh zero-context, repair-only, adversarial
Evidence root inspected: `/intake` only
Writable workspace used for replay checks: `/work`

## Scope and compliance

I followed `/intake/REPLAY_PRECONDITION.md` and restricted all writable execution to `/work`. I did
not edit any file under `/intake`, did not access any repository, did not access any protected
package, and did not use browsing, downloads, package installation, `curl`, `wget`, or
network-capable Python.

`/intake/REVIEW_SCOPE.json` states:

- `evidence_read_only: true`
- `ephemeral_copy_checks_allowed: true`
- `repository_access_allowed: false`
- `protected_package_access_allowed: false`
- `research_continuation_allowed: false`

These settings are consistent with a repair-only review of R1 and R2 and inconsistent with any
research continuation.

## Intake authentication

I authenticated the sealed intake in two ways.

1. Detached manifest seal:
   `sha256(/intake/REVIEW_MANIFEST.tsv) =
   d9d99483dba8d74cc25eacbeec3ef72ae43213c0ea5ab78c78530df2bfca437e`,
   which exactly matches `/intake/REVIEW_MANIFEST.sha256`.
2. Full manifest walk:
   all 38 manifest payload rows in `/intake/REVIEW_MANIFEST.tsv` existed, matched the declared byte
   counts, and matched the declared SHA-256 digests.

I also ran `/intake/verify_review_intake.py`, which returned `PASS` with:

- `manifest_payload_count = 38`
- `total_file_count = 40`
- `manifest_sha256 = d9d99483dba8d74cc25eacbeec3ef72ae43213c0ea5ab78c78530df2bfca437e`
- `scope_sha256 = c8ae629f7028fb1e6bb3ef59d2672bb2dd42f3a6e833839133607d3cd3d3b7f8`

The two unlisted files are the manifest itself and its detached seal, which is consistent with
`manifest_payload_count: 38` in the scope file.

Filesystem state also matches the sealed-intake claim: `/intake` is `555` and its files are `444`,
and `test -w /intake` returned nonzero.

## R1 review: exact computational-source integrity

### R1.1 Exact SHA-256 pins are present

`/intake/verify_package.py` hard-pins exact SHA-256 digests for the three required computational
sources:

- `derive_offdiagonal_modes.py`
- `verify_offdiagonal_independent.py`
- `run_catch_proofs.py`

The pins appear in `SOURCE_SHA256`, and the verifier enforces them by recomputing each digest and
asserting `source_integrity:<name>` for each file.

### R1.2 The aggregate verifier contains executable canned-substitution rejection logic

`/intake/verify_package.py` defines a real `canned_emitter()` that reads a banked JSON artifact and
writes it to the requested output path. It then:

1. copies the package to a temporary writable directory,
2. replaces exactly one of the three scripts with that emitter,
3. runs `verify_package.py` in the mutated copy, and
4. requires nonzero exit plus the matching `source_integrity:<script>` failure marker on stderr.

This is executable mutation logic, not a string-only declaration.

### R1.3 Independent live proof that the three source-integrity gates reject canned substitution

I did not rely only on reading `verify_package.py`. In fresh writable copies under `/work`, I
manually replaced each source one at a time with a canned emitter, then ran the corresponding
literal command so the substituted script emitted the expected banked artifact, and finally ran
`python3 -S verify_package.py`.

Observed results:

- Mutated `derive_offdiagonal_modes.py`:
  the emitter reproduced `DERIVATION_RESULT.json` exactly, then aggregate verification failed with
  `AssertionError: source_integrity:derive_offdiagonal_modes.py`.
- Mutated `verify_offdiagonal_independent.py`:
  the emitter reproduced `INDEPENDENT_VERIFICATION.json` exactly, then aggregate verification failed
  with `AssertionError: source_integrity:verify_offdiagonal_independent.py`.
- Mutated `run_catch_proofs.py`:
  the emitter reproduced `CATCH_PROOF_RESULT.json` exactly, then aggregate verification failed with
  `AssertionError: source_integrity:run_catch_proofs.py`.

That is the required live rejection proof. The verifier does not merely inspect strings; it rejects
executable source substitution even when the substituted script still reproduces the banked JSON.

### R1.4 Literal replay in writable copy

I followed `/intake/REPLAY_PRECONDITION.md` literally:

```bash
mkdir -p /work/g326_review_writable
cp -r /intake/. /work/g326_review_writable/
chmod -R u+w /work/g326_review_writable
cd /work/g326_review_writable
```

I then ran the four registered commands literally from `/intake/REPLAY_COMMANDS.txt`:

```bash
python3 -S derive_offdiagonal_modes.py --output .review_runtime/DERIVATION_RESULT.json
python3 -S verify_offdiagonal_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json
```

Results:

- all four commands exited `0`;
- the writable copy became writable as intended (`/work/g326_review_writable` and the copied
  sources were mode `u+w`);
- all four generated JSON files in `.review_runtime/` matched the banked intake files byte-for-byte
  by both `cmp -s` and SHA-256;
- aggregate verification returned
  `PASS_EXTERNAL_SCIENCE__R1_R2_IMPLEMENTED_PENDING_FOLLOWUP` with `assertion_count = 56`.

Exact replay confirmations:

- `DERIVATION_RESULT.json` exact:
  `6babb0ea591c57ab7a554d51dad73b6dbeafad26d1b66094c489df235eb17f12`
- `INDEPENDENT_VERIFICATION.json` exact:
  `0f96adaab2f55d56975bb9e33cb3c6e18dd9a9e4fd951ec3ba6cac936cf97ec6`
- `CATCH_PROOF_RESULT.json` exact:
  `3f31d3ede44933831a3a946c0e8610a3089865d0630f438f06c43605f92e80fa`
- `PACKAGE_VERIFICATION_RESULT.json` exact:
  `044a517d2cc0c72535213c5701f5d0bc3c11efcfefe0ed34389b87fb07a0511d`

Conclusion on R1: implemented and verified.

## R2 review: writable ephemeral-copy replay

`/intake/REPLAY_PRECONDITION.md` explicitly states that the sealed intake is read-only, requires a
writable copy under `/work/g326_review_writable`, and states that generated files go only under
`.review_runtime/` in the writable copy. It further states that this is an execution precondition,
not permission to edit evidence.

This satisfies the three requested R2 checks:

1. The sealed intake is explicitly preserved as read-only.
2. The registered `cp -r` plus `chmod -R u+w` commands create a writable replay copy without
   changing intake evidence.
3. The scope permits checks only in that ephemeral copy and does not permit evidence edits or
   research continuation.

My observed filesystem state matched the instruction:

- `/intake` remained nonwritable during the review.
- `/work/g326_review_writable` was writable after the registered permission step.
- all replay outputs landed in `/work/g326_review_writable/.review_runtime/`.

Conclusion on R2: implemented and verified.

## Scientific boundary check

I did not reopen the scientific question. I verified only whether the bounded accepted landing was
unchanged.

The bounded landing remains the same:

- off-diagonal mode dimensions remain `5` fixed quotient lattice moduli plus `1` local transverse
  Kasner shear;
- the combined homogeneous count remains `12`;
- the accepted landing token remains
  `HOMOGENEOUS_OFFDIAGONAL_MODES_CLOSE_AS_FIVE_QUOTIENT_LATTICE_MODULI__ONE_LOCAL_TRANSVERSE_KASNER_SHEAR__NO_NEW_GAUGE_OR_SCALAR_MODE__NO_FULL_STABILITY_CLAIM`;
- `metric_changed`, `kernel_changed`, and `angular_sector_changed` remain `false`;
- the bounded closure remains limited to homogeneous synchronous first variation;
- nonzero Fourier modes, full linear stability, nonlinear stability, physical occupancy, physical
  scale, and `X_max` remain open or unselected.

This matches the scientific boundary stated in the request and the current accepted-grade ledgers.

## Verdict

Both registered repairs are complete on the evidence supplied. R1 now has exact source-digest pins
plus three live executable canned-substitution rejection proofs. R2 now has an explicit read-only
intake to writable-ephemeral-copy replay procedure, and the literal replay works exactly as
registered without changing sealed evidence. The already accepted bounded G326 landing is unchanged
and remains supported within its stated boundary.

accept R1 and R2 and the unchanged bounded landing;
