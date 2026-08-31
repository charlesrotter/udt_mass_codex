# G308 registered commands

## Package replays

```bash
python3 -S derive_global_chirality_coherence.py
python3 -S verify_global_chirality_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

The first three commands regenerate only their registered G308 outcome files. The package verifier
is no-write.

## Repository-only gates

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

These require the complete repository and are not promised as sealed-package replays.
