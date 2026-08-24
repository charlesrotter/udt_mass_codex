# G250 external-review repair preregistration

Date: 2026-08-24

The fresh external reviewer retained the bounded scientific landing and required exactly three
certification repairs. No scientific formula, candidate class, anchor value, history, or outcome may
change during this repair cycle.

## R1 — sealed source-path contract

Repair `verify_package.py` so every exact manifest source is resolved either at the repository root
or, in a sealed intake, below the explicit `sources/` relocation root. Require exactly one valid
candidate and retain SHA-256 verification. Add a hostile check proving that a missing, ambiguous, or
hash-mismatched relocated source fails.

## R2 — command-scope contract

Split `COMMANDS.md` into commands runnable inside the sealed intake and the repository-only current-
premise verifier. The sealed command list must contain no absent executable. The premise-registry
gate remains mandatory in the repository before banking and must not be represented as an intake
replay.

## R3 — source-backed provenance certification

Replace assertion-like G236/G237, G99, and attachment-law checks with checks that:

1. resolve the exact source through `SOURCE_MANIFEST.tsv`;
2. verify its frozen SHA-256;
3. parse the relevant structured ledger rows for the SNe zero-point deletion and G99's external
   `M_B`, P1, and imported-transfer dependencies;
4. inspect the exact-hashed G132/G202 attachment statements before retaining the dimensional-
   candidate classification;
5. make hostile mutations of those source-backed facts fail.

The independent verifier must implement these checks without importing production code or output.

## Certification contract

After R1--R3:

- production, independent, hostile, and package replays must pass in the repository;
- the package verifier must also pass from the corrected sealed intake;
- every declared sealed command must exist and run there;
- the current scientific-premise verifier and full repository suite must pass separately;
- a corrected sealed intake must receive repair-only external follow-up before banking.

## Maximum conclusion

The scientific G250 conclusion remains exactly the externally retained bounded landing. This repair
may improve certification only; it cannot strengthen ownership, supply an anchor, select a scale or
history, or read an observational outcome.
