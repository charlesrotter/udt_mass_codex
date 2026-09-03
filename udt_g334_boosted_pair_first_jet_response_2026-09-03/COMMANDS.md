# G334 commands

Run from this package directory:

```text
python3 -B -S derive_boosted_pair_first_jet.py --output DERIVATION_RESULT.json
python3 -B -S verify_boosted_pair_first_jet_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
python3 -B -S build_source_manifest.py
python3 -B -S verify_package.py
```

The first four commands write registered evidence. The aggregate verifier writes nothing unless an
explicit `--output` path is supplied.
