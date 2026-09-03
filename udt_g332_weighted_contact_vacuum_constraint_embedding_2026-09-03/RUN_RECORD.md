# G332 run record

Date: 2026-09-03

## Preregistration

Committed and pushed before outcome execution:

```text
352837d9 Preregister G332 weighted constraint embedding
```

## Registered executions

```text
python3 derive_weighted_constraint_embedding.py --output DERIVATION_RESULT.json
python3 verify_weighted_constraint_embedding_independent.py --output INDEPENDENT_VERIFICATION.json
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Observed summaries:

```text
production: 642 checks, 80 cases, PASS
independent: 65 checks, 64 cases, PASS
hostile: 9 mutations caught, PASS
```

All calculations use exact standard-library rational and quadratic-extension arithmetic. No GPU,
long solve, network data, observational outcome, fitted coefficient, or protected local work is
used.

## External review

The authenticated 40-payload fresh intake returned
`ACCEPT_WITH_REPAIRS__G332_SCIENTIFIC_LANDING_RETAINED`. The reviewer independently retained the
constraint theorem and identified only sealed source-root resolution and tensor-index wording.

Repairs R1 and R2 were preregistered and committed at `f5417715` before implementation. The
authenticated corrected 44-payload intake then returned
`REPAIRS_ACCEPTED__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED`. Its literal four-command replay
returned 642 production checks, 65 independent checks, nine caught mutations, and 91 aggregate
gates, with all generated artifacts byte-identical.
