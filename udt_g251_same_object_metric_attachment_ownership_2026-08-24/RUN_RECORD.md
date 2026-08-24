# G251 run record

Date: 2026-08-24

All runs used `PYTHONDONTWRITEBYTECODE=1` from repository root.

```text
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/derive_attachment_ownership.py --cases 4096 --output .../DERIVATION_RESULT.json --ledger-output .../ATTACHMENT_OWNERSHIP.tsv
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/verify_attachment_ownership_independent.py --cases 12000 --output .../INDEPENDENT_VERIFICATION.json
python3 udt_g251_same_object_metric_attachment_ownership_2026-08-24/run_catch_proofs.py --output .../CATCH_PROOF_RESULT.json
```

The first production attempt stopped because one line-wrapped G250 source phrase was matched too
literally. The first hostile run likewise exposed one overly literal G244 source phrase. Only those
source-token checks were repaired; the preregistered question, candidate census, formulas, and
landing were unchanged. Final production, independent, and hostile routes all pass.
