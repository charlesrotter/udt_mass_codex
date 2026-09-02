# G326 run record

Date: 2026-09-02

## Preregistration

- `32fa2f98`: bounded question, candidate landing, falsifiers, completeness map, premise ledger,
  sources, and replay commands frozen.
- `04c7fb8f`: pre-production clarification that curvature of cover-coordinate modes is evaluated
  modulo Lie transport, while the log mode uses transverse tidal splitting.

## Production

```text
python3 -S derive_offdiagonal_modes.py --output DERIVATION_RESULT.json
```

Result: 33 exact assertions passed; preregistered positive landing obtained.

## Independent direct tensor verification

```text
python3 -S verify_offdiagonal_independent.py --output INDEPENDENT_VERIFICATION.json
```

Result: 137 exact component assertions passed. The verifier imports no production code and reads no
production result.

## Hostile controls

```text
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Result: 5 of 5 registered mutation classes caught.

## Aggregate replay and repository gates

```text
python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

Results: 46 aggregate package checks passed with byte-exact regeneration of all three generated
artifacts; the 308-row premise registry passed; the full repository suite passed `218` tests with
one registered expected failure.

## Current boundary

Internal exact result only. Fresh sealed adversarial review is required before acceptance. No long
solve or GPU process was used.
