# G332 commands

Run from this directory:

```text
python3 derive_weighted_constraint_embedding.py --output DERIVATION_RESULT.json
python3 verify_weighted_constraint_embedding_independent.py --output INDEPENDENT_VERIFICATION.json
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 verify_package.py
```

The first three commands regenerate tracked evidence. `verify_package.py` reruns them in a temporary
directory and compares the regenerated JSON byte-for-byte without modifying the package.
