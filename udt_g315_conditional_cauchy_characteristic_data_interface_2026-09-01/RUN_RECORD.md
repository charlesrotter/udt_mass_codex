# G315 run record

Date: 2026-09-01
Preregistration ancestry: `6d26ca34`

## Registered commands

```text
python3 -S derive_data_interface.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

## Initial exact results

```text
G315 production PASS: 72 exact assertions; 15 interface rows
G315 independent PASS: 89 exact assertions
G315 hostile checks PASS: 17/17 caught
```

All calculations use Python standard-library exact rational arithmetic. No GPU, long process,
network access, observational data, protected local work, or external package was used.

## External replay

The fresh zero-context external reviewer authenticated all 35 manifest payloads and ran the exact
four registered commands in an isolated writable copy. It reproduced the five generated outputs
byte-for-byte, independently checked the scientific derivation, and returned:

```text
G315_ACCEPTED__CONDITIONAL_DATA_INTERFACE_UPHELD
```

Full response, transcript, isolation details, and hashes are banked in the three
`EXTERNAL_REVIEW_*` evidence files.
