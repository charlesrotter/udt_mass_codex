# G276 registered commands

Run from this package directory:

```bash
python3 derive_proper_clock_scale.py --no-write
python3 verify_proper_clock_scale_independent.py --no-write
python3 run_catch_proofs.py --no-write
python3 verify_package.py --no-write
```

All commands are CPU-only, write nothing in `--no-write` mode, use no observational outcomes, and
do not access protected packages.
