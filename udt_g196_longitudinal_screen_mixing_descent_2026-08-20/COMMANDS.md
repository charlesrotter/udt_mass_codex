# G196 registered commands

Run from the repository root.

```bash
python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/derive_longitudinal_screen_mixing.py
python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_longitudinal_screen_mixing_independent.py
python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/run_catch_proofs.py
python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/build_source_manifest.py
python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_package.py
```

Strict replay without evidence writes:

```bash
G196_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_package.py --no-write
```
