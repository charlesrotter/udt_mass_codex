# G333 commands

Run from this directory:

```text
python3 -S derive_initial_pair_response.py --output DERIVATION_RESULT.json
python3 -S verify_initial_pair_response_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -S verify_package.py
```

The first three commands regenerate registered evidence. `verify_package.py` reruns them in a
temporary directory and compares the JSON byte-for-byte without changing the package.
