# Environment and commands

- CPU only; no GPU process launched
- Python `3.10.12`
- SymPy `1.13.1`
- Linux `6.8.0-124-generic x86_64`

Commands:

```bash
python3 freeze_sources.py
python3 freeze_refined_sources.py
python3 derive_transition_ownership.py
python3 verify_transition_ownership_independent.py
python3 run_catch_proofs.py
python3 verify_source_manifests.py
python3 verify_repository_gates.py
python3 build_package_manifest.py
sha256sum -c PACKAGE_MANIFEST.sha256
```

All derivation and verification processes were bounded CPU runs. No relaxation, ODE solve,
eigensolve, fitting, or numerical tolerance entered a scientific ruling.
