# G334 run record

Date: 2026-09-03

```text
python3 -B -S derive_boosted_pair_first_jet.py --output DERIVATION_RESULT.json
{"checks_passed": 43026, "classifications": ["TRANSPORT_QUALIFIED_CONGRUENCE", "COMPLETE_MATRIX_STRONGER_ON_DECLARED_TRANSPORT"], "sample_count": 2520}

python3 -B -S verify_boosted_pair_first_jet_independent.py --output INDEPENDENT_VERIFICATION.json
{"checks_passed": 580, "verdict": "PASS"}

python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
{"mutations_caught": 12, "verdict": "PASS"}
```

The registered outputs are deterministic and are replayed by `verify_package.py` in an ephemeral
directory.

Post-review repair replay:

```text
python3 -B -S verify_sealed_replay_repair.py --output REPAIR_VERIFICATION_RESULT.json
{"checks_passed": 20, "verdict": "PASS"}

python3 -B -S verify_package.py
G334 package PASS: 103 aggregate gates
```

Fresh external review retained the scientific landing. Final repair-only external review accepted
R1--R3 with no remaining mechanical defect and no scientific change.

Repository integration:

```text
python3 verify_current_scientific_premises.py
PASS: 317-row premise registry and G242--G334 startup/premise guards

pytest -q
220 passed, 1 xfailed
```
