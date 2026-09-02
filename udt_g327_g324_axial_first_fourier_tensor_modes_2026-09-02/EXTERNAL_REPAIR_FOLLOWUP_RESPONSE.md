# G327 Repair-Only External Review

No repair-blocking findings were identified within the allowed scope.

## Scope and method

- I inspected only `/intake` and used `/work/g327_review_writable_00f1db00` for writable ephemeral replay.
- I did not browse, download, install packages, access any repository, or modify sealed evidence under `/intake`.
- I authenticated `REVIEW_SCOPE.json`, `REVIEW_MANIFEST.tsv`, `REVIEW_MANIFEST.sha256`, and every manifest payload before replay.

## Intake authentication

- `REVIEW_SCOPE.json` fixes the scope to repairs `R1` through `R3`, forbids research continuation, repository access, installs/downloads, and scientific-landing changes, and declares `manifest_payload_count: 49`.
- Independent recomputation of the detached seal matched `REVIEW_MANIFEST.tsv` SHA-256 `97d4345cd1cdaa8015a476629ed2f86a2a24ec92dc60f8cfead333c352c6bebd`.
- All 49 registered payloads existed, matched their recorded byte counts and SHA-256 values, were read-only, and exactly matched the actual sealed payload set.
- `python3 -S /intake/verify_review_intake.py` also passed with `payload_count: 49`.

## R1

- The vendored runtime archive authenticated as SHA-256 `caa6a0b9aae296979d86b54ae5ce8a1df50081c0701aaae4c2e370867a233d9d`, matching `VENDORED_RUNTIME_MANIFEST.json`.
- Independent zip inspection found 1,633 non-directory entries, including `sympy/__init__.py` and `mpmath/__init__.py`, with no `__pycache__`, `.pyc`, or `.pyo` entries.
- The runtime bootstrap in `sealed_runtime.py` prepends only `VENDORED_SYMPY_RUNTIME.zip` to `sys.path`.
- The three symbolic scripts each activate that bootstrap before importing SymPy.
- In the writable copy, with `PYTHONNOUSERSITE=1`, an independent probe reported:
  - `sympy 1.13.1` from `/work/g327_review_writable_00f1db00/VENDORED_SYMPY_RUNTIME.zip/sympy/__init__.py`
  - `mpmath 1.3.0` from `/work/g327_review_writable_00f1db00/VENDORED_SYMPY_RUNTIME.zip/mpmath/__init__.py`
- I then ran the four registered commands literally from one writable copy, with `PYTHONNOUSERSITE=1` exported in the shell:

```text
python3 derive_axial_tensor_modes.py --output .review_runtime/DERIVATION_RESULT.json
python3 verify_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json
python3 run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json
```

- All four commands exited successfully without any install, download, repository, or network activity.

## R2

- I independently recomputed the raw Git commit object identifier from `PREREGISTRATION_COMMIT_OBJECT.txt` using standard Git object encoding and obtained exactly `9bec301bc265bf67afa5f8398f7557ccdabb855b`.
- The raw commit payload records tree `1a7fedca384e509831597d19ff16d032526e4731` and parent `2077ec6bef8dab2102a7b64dc8c5146c5670716c`.
- `PREREGISTRATION_CHANGESET.tsv` records exactly five added paths, all status `A`:
  - `COMPLETENESS_MAP.md`
  - `MAP.md`
  - `PREMISE_LEDGER.tsv`
  - `PREREGISTRATION.md`
  - `SOURCE_SCOPE.tsv`
- `PREREGISTRATION_TREE.tsv` records exactly those five blob objects and modes/types `100644 blob`.
- Independent blob-ID recomputation from the sealed local payloads matched all five registered SHA-1 blob identifiers exactly.
- `python3 -S /intake/verify_preregistration_proof.py` passed with 12 assertions.
- The trusted-timestamp ceiling is explicit and correctly bounded: the proof authenticates content plus the Git ancestry marker only; it does not claim an external trusted timestamp.

## R3

- `REPLAY_COMMANDS.txt` contains exactly four registered lines, and the fourth line is literally `python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json`.
- In `verify_package.py`, the nested sentinel is only `UDT_G327_NESTED_AGGREGATE=1`.
- The sentinel branch is entered only after the verifier has already executed the scientific landing/status checks, source-integrity checks, evidence-integrity checks, vendored-runtime checks, preregistration-proof checks, independence checks, and scope-boundary checks.
- The outer aggregate run succeeded with:
  - `registered_replay_count: 4`
  - `literal_fourth_command_replayed: true`
  - `assertion_count: 73`
- The outer verifier also rejects canned artifact republishing by mutating each of the first three scripts in scratch copies and requiring a source-integrity failure.
- I independently ran a direct nested invocation in the writable copy with `UDT_G327_NESTED_AGGREGATE=1` and `PYTHONNOUSERSITE=1`. It passed with 56 checks, including:
  - `production_landing`
  - `production_status`
  - `source_integrity:derive_axial_tensor_modes.py`
  - `source_manifest_exact`
  - `evidence_integrity:PREREGISTRATION_COMMIT_OBJECT.txt`
  - `preregistration_proof_pass`
  - `audit_scope_boundary`
  - `lay_stability_boundary`
  - `nested_replay_guard_active`
- On inspection, the sentinel suppresses only recursive replay/canned-substitution loops. I found no bypass of scientific, source-integrity, provenance, status, or scope gates.

## Scientific noninterference

- The three regenerated scientific JSON artifacts were byte-identical to the sealed originals:
  - `DERIVATION_RESULT.json` SHA-256 `5690b46eb0404425c6c7ab56da1db25b7d5b5fea44d647919b87c89640c5c491`
  - `INDEPENDENT_VERIFICATION.json` SHA-256 `2cf480694c7799511a874e907d75c3579871fd30afdfe17c419c74e64cc2ec48`
  - `CATCH_PROOF_RESULT.json` SHA-256 `ea1d7f441d2c318ebf2cf712d31a9729516e54f551a1190c77ef851fea05ebfe`
- The bounded scientific landing token is unchanged across the sealed derivation, independent verification, aggregate verifier, exact derivation, audit report, and lay report.
- The sealed boundary language also remains unchanged: it is still not the complete nonzero Fourier problem and not proof of whole-spacetime stability.

## Conclusion

Within the permitted zero-context repair-only scope, I found the preregistered repairs `R1` through `R3` implemented and authenticated, the fourth command literally replayed from one fresh writable copy, the nested guard non-bypassing for the required gates, and the bounded scientific landing unchanged with byte-identical scientific artifacts.

ACCEPT__G327_R1_R2_R3_REPAIRS__SCIENTIFIC_LANDING_UNCHANGED
