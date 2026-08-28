# G286 registered commands

Run from the package directory after the preregistration commit is banked:

```bash
python3 derive_propagation_discriminator.py --output DERIVATION_RESULT.json
python3 verify_independent.py --production DERIVATION_RESULT.json --output INDEPENDENT_VERIFICATION.json
python3 verify_package.py --output VERIFICATION_RESULT.json
python3 run_repair_catch.py --output REPAIR_RESULT.json
python3 derive_propagation_discriminator.py
python3 verify_independent.py --production DERIVATION_RESULT.json
python3 verify_package.py
```

Both commands are dependency-free CPU checks. They evaluate a supplied smooth metric witness and do
not solve or propose a physical field equation.
