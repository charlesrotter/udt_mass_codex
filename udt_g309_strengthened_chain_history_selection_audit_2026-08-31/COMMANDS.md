# G309 registered commands

From this package directory:

```bash
python3 -S derive_strengthened_history_audit.py
python3 -S verify_strengthened_history_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

These invocations use only the Python standard library, print their results, and do not write files.
The package verifier executes the live production builder and requires exact equality with the saved
production JSON.

Repository-only gates:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

These are provenance gates run in the repository. They are intentionally not promised as replayable
inside a sealed intake that restricts the reviewer to the copied package and frozen sources.
