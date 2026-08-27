# G279 registered commands

Run from the package directory unless stated otherwise.

```bash
python3 freeze_source_manifest.py
python3 derive_native_provenance.py
python3 verify_native_chain_independent.py
python3 run_dependency_subtractions.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Repository gates, run from the repository root:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
git diff --check
```
