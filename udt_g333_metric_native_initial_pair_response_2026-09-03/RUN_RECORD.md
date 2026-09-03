# G333 run record

Date: 2026-09-03

## Before execution

- actual synchronized base: `116fab2f` on `grok`;
- preregistration commit: `c56714b3`, pushed before outcome execution;
- unrelated protected untracked paths were not inspected, modified, cited, staged, or deleted;
- no GPU or long process was launched.

## Outcome commands

```text
python3 -S derive_initial_pair_response.py --output DERIVATION_RESULT.json
python3 -S verify_initial_pair_response_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Observed stdout:

```text
{"checks_passed": 6882, "classifications": ["METRIC_2_PLUS_1", "COMPLETE_PULLBACK_STRONGER"], "sample_count": 360}
{"checks_passed": 146, "verdict": "PASS"}
{"mutations_caught": 9, "verdict": "PASS"}
```

The exact production result and the independent representative rotated-matrix checks agree. At
this stage in the chronology external review remained pending.

## Fresh external review

The authenticated 38-file intake returned
`ACCEPT_WITH_REPAIRS__G333_BOUNDED_FIRST_RESPONSE_RETAINED`. The reviewer independently retained
the algebra and bounded landing, and requested four non-scientific repairs. Those repairs were
preregistered at commit `019e869e` before implementation.

## Repair-only external follow-up

The authorized corrected 43-file intake authenticated 41 manifest payloads. The zero-context
repair-only reviewer replayed the production, independent, hostile, and aggregate checks in a
writable ephemeral copy; all regenerated JSON outputs were byte-identical to the intake. It
accepted R1--R4 and retained the scientific landing:

```text
REPAIRS_ACCEPTED__G333_BOUNDED_FIRST_RESPONSE_RETAINED
```
