# Native global coframe-definition audit package

Read in this order:

1. `PREREGISTRATION.md`
2. `AUDIT_REPORT.md`
3. `LAY_REPORT.md`
4. `EXACT_DERIVATION.md`
5. `STATUS_LEDGER.tsv`
6. `MINIMAL_SELECTOR_SET.tsv`
7. `COUNTERFAMILY_ATLAS.tsv`
8. `P03_CORRECTION_LAYER.md`
9. `VERIFICATION_RESULT.json`

`SOURCE_MANIFEST.tsv` freezes 99 input artifacts. `derive_global_definition.py` generates the
machine-readable audit tables and exact algebra. `verify_global_definition.py` independently
rebuilds the load-bearing algebra and exercises all 27 preregistered catch-proofs without importing
the production implementation.

The package does not modify or supersede frozen evidence bytes. Its P03 correction is append-only
and narrows the interpretation of the frozen P03 return.
