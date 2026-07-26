# Replay commands

Install the pinned dependency into an isolated temporary target:

```bash
python3 -m pip install --target /tmp/udt_observable_census_pydeps sympy==1.14.0
```

Run the deterministic package replay with ambient site packages disabled:

```bash
UDT_PINNED_SITE=/tmp/udt_observable_census_pydeps \
python3 udt_native_global_observable_closure_census_2026-07-26/run_isolated_replay.py
```

Run the standard-library independent verifier directly:

```bash
PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= \
python3 udt_native_global_observable_closure_census_2026-07-26/verify_independent.py
```

Run repository preservation gates after building the package manifest:

```bash
python3 udt_native_global_observable_closure_census_2026-07-26/build_manifest.py
python3 udt_native_global_observable_closure_census_2026-07-26/verify_repository_gates.py
```
