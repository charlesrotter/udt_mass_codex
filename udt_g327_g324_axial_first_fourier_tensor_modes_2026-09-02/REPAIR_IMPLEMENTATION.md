# G327 repairs R1--R3 implementation record

Date: 2026-09-02
Repair contract: commit `46f3aaaa`
Scientific landing: unchanged

## R1 — completed

`build_vendored_runtime.py` produced deterministic archive
`VENDORED_SYMPY_RUNTIME.zip` with SHA-256
`caa6a0b9aae296979d86b54ae5ce8a1df50081c0701aaae4c2e370867a233d9d`.
It contains 1,633 non-cache source/data files from SymPy 1.13.1 and mpmath 1.3.0.
`sealed_runtime.py` activates that archive before any of the three symbolic programs imports
SymPy. With `PYTHONNOUSERSITE=1`, all three programs run and reproduce their banked JSON artifacts
byte for byte.

## R2 — completed

The intake-local proof contains the raw preregistration commit payload, exact five-file changeset,
and the five blob IDs at commit `9bec301bc265bf67afa5f8398f7557ccdabb855b`.
`verify_preregistration_proof.py` independently recomputes Git object IDs with the standard-library
SHA-1 object encoding and passes 12 assertions. Its precise ceiling is visible: it authenticates
content and the Git ancestry marker, not an external trusted timestamp.

## R3 — completed

The aggregate verifier now executes all four registered lines literally in one fresh copy. The
fourth invocation receives only `UDT_G327_NESTED_AGGREGATE=1`; it reruns every scientific,
source-integrity, provenance, status, and scope gate but does not recursively launch a fifth copy.
The outer result records `registered_replay_count: 4`,
`literal_fourth_command_replayed: true`, and 73 assertions.

## Noninterference

The only changes to the three scientific scripts are the standard-library lines that activate the
sealed runtime before importing the same SymPy version. Their generated scientific artifacts are
byte-identical to the prerepair artifacts. No equation, sign, coefficient, field, boundary,
solution branch, norm, physical premise, metric, kernel, angular sector, source, action, matter,
observation, scale, history, or `X_max` statement changed.

Status:
`R1_R2_R3_EXTERNALLY_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`.
