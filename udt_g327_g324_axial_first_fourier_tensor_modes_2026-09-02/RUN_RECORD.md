# G327 run record

Date: 2026-09-02

## Registered commands

Run from this package directory:

```text
python3 derive_axial_tensor_modes.py --output .review_runtime/DERIVATION_RESULT.json
python3 verify_independent.py --output .review_runtime/INDEPENDENT_VERIFICATION.json
python3 run_catch_proofs.py --output .review_runtime/CATCH_PROOF_RESULT.json
python3 -S verify_package.py --output .review_runtime/PACKAGE_VERIFICATION_RESULT.json
```

Production and independent routes use Python 3.10.12, intake-local SymPy 1.13.1, and intake-local
mpmath 1.3.0. `sealed_runtime.py` inserts the manifest-authenticated
`VENDORED_SYMPY_RUNTIME.zip` before importing SymPy, so the commands need no network, installation,
repository package, protected package, or host user site. Both routes are exact symbolic
calculations; no GPU, grid, tolerance, fitted value, numerical boundary, or long-running process is
used. Generated JSON artifacts record the exact assertion lists.

The registered commands never overwrite banked evidence. The outer package verifier repeats all
four registered commands literally inside one temporary copy. It demands byte identity for the
three scientific artifacts and verifies the fourth command's nested result. The environment token
`UDT_G327_NESTED_AGGREGATE=1` prevents only unbounded self-recursion in that nested fourth command;
all scientific, source-integrity, provenance, status, and scope gates still run.

The repaired outer aggregate has 73 assertions. The raw preregistration proof has 12 assertions.
All three scientific JSON artifacts are byte-identical before and after the evidence repair.

## External repair-only replay

The external reviewer authenticated all 49 sealed payloads and ran all four registered commands
from one writable ephemeral copy with host user packages disabled. It independently verified the
vendored runtime, raw preregistration commit and five blobs, literal nested fourth command, and
byte identity of all three regenerated scientific artifacts. Final token:

`ACCEPT__G327_R1_R2_R3_REPAIRS__SCIENTIFIC_LANDING_UNCHANGED`.
