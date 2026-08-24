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

Fresh external gpt-5.4 review returned `ACCEPT_WITH_REPAIRS`. Repair preregistration was committed
and pushed at `bd8f0a2b` before implementation. R1 adds explicit cited `E/I/C/W` fields to all 18
candidate rows and four hostile citation catches. R2 adds the self-contained sealed 233-row premise
registry replay while retaining the separate repository-wide startup/premise gate. During R1 the
first repaired production replay failed closed on two line-wrapped G250 citation locators; only
their literal locators were corrected. The landing, formulas, source universe, and classifications
were unchanged.
