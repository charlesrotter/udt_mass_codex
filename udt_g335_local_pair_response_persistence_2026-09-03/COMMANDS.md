# G335 commands

Run from this directory with bytecode disabled:

```text
python3 -B -S derive_local_pair_persistence.py --output DERIVATION_RESULT.json
python3 -B -S verify_local_pair_persistence_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -B -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json
```

Review-intake and external-review commands are added only after the aggregate package passes.

```text
python3 -B -S build_review_intake.py
python3 -B -S verify_review_intake.py /tmp/<sealed-intake>
```
