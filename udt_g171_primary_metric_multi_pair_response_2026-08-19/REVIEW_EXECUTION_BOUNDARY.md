# G171 verification execution boundary

Date: 2026-08-19

G171 has two deliberately different gates.

## Repository outer gate

Run from the repository:

```text
python3 udt_g171_primary_metric_multi_pair_response_2026-08-19/verify_package.py
```

This gate verifies the frozen preregistration commit with `git show`, requires the repository intake
builder, reruns the three package programs, and invokes the repository-wide scientific-premise
verifier. `VERIFICATION_RESULT.json` records this **repository-only** gate. It is not expected to
run in a seal that intentionally contains no `.git` directory or full startup surface.

## Sealed intake gate

Run from the immutable intake:

```text
python3 /intake/udt_g171_primary_metric_multi_pair_response_2026-08-19/verify_sealed_intake.py
```

This gate validates every path, size, and SHA-256 in `REVIEW_SCOPE.json`; validates all 12 copied
sources; copies the immutable package and sources to isolated temporary scratch; reruns production,
independent, and catch scripts there; and checks 31, 108,000, and 14 passes respectively. It does
not edit the seal or require repository state.

The corrected intake includes `build_review_intake.py` for file-count transparency. The reviewer
must use the sealed gate for sealed reproducibility and treat the outer result only as recorded
evidence of the separately run repository gate.
