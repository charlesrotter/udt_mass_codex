# G307 registered commands

Run from this package directory with no third-party package import:

```bash
python3 -S derive_directed_member_reconstruction.py
python3 -S verify_directed_member_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

Run the current premise audit from the repository root:

```bash
python3 verify_current_scientific_premises.py
```

The first three commands write only their registered JSON/TSV outcome files inside this package.
`verify_package.py` and the premise verifier are no-write checks.
