# G239 commands

Run from this directory:

```bash
python3 derive_reference_operator.py
python3 verify_reference_operator_independent.py
python3 verify_sealed_premise_scope.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Inside a read-only sealed intake, copy the intake to a writable ephemeral directory and run the
bounded dependency audit without persistent output:

```bash
python3 verify_sealed_premise_scope.py --no-write
```

The full repository premise audit is separate repository-only evidence; its verifier is not part
of the sealed intake:

```bash
cd ..
python3 verify_current_scientific_premises.py
```

No command reads BOSS outcome artifacts.
