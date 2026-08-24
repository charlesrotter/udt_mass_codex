# G247 commands

Run from the repository root with bytecode disabled for no-persistent-output replay:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 udt_g247_global_null_branch_network_descent_2026-08-24/derive_global_null_branch_network.py --cases 2048
PYTHONDONTWRITEBYTECODE=1 python3 udt_g247_global_null_branch_network_descent_2026-08-24/verify_global_null_branch_network_independent.py --cases 5000
PYTHONDONTWRITEBYTECODE=1 python3 udt_g247_global_null_branch_network_descent_2026-08-24/run_catch_proofs.py
PYTHONDONTWRITEBYTECODE=1 python3 udt_g247_global_null_branch_network_descent_2026-08-24/verify_package.py
```

The saved JSON evidence was generated with the same case counts and the scripts' `--output`
options. No observation file or protected package is read.

