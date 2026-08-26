# G262 run record

Date: 2026-08-25
Device: CPU
GPU: not used
Long solve: none

## Commands

```bash
python3 -m py_compile \
  udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/derive_hierarchy.py \
  udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/verify_independent.py \
  udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/run_catch_proofs.py

python3 udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/derive_hierarchy.py \
  --output udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/DERIVATION_RESULT.json

python3 udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/verify_independent.py \
  --output udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/INDEPENDENT_VERIFICATION.json

python3 udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/run_catch_proofs.py \
  --output udt_g262_reciprocal_clock_acceleration_mass_aspect_xmax_bridge_2026-08-25/CATCH_PROOF_RESULT.json
```

## Execution note

The first symbolic run failed closed because a two-symbol endpoint swap used sequential SymPy
substitution. The code was repaired to request simultaneous substitution explicitly. No result had
been produced and no scientific formula, candidate landing, or tolerance changed.

## Results

- production arbitrary-function symbolic checks: 19/19 pass;
- independent exact-Fraction cases: 1,000;
- independent assertions: 10,003;
- applied mutation catches after preregistered external repair: 12/12;
- GPU, fit, observational outcome, protected input: zero.

## Repository gates

- `python3 verify_current_scientific_premises.py`: PASS over the 244-row registry;
- `python3 -m pytest tests/`: 166 passed, 1 expected xfail in 64.64 seconds;
- the xfail is the pre-existing documented matter-sector HABIT-pin migration item, not a G262
  regression.

## External review and bounded repair

Fresh isolated `gpt-5.4` review returned `ACCEPT_WITH_REPAIRS`. It accepted the acceleration,
mass-aspect, angular, endpoint-arrow, character, asymptotic, and nonselection results. It required
the package to surface the pre-existing sealed raw WR-L wall lapse flux `-2*pi*X` without promoting
it to mass. The repair was preregistered and pushed at `91448643` before implementation.

The reviewer reran `verify_independent.py`, `run_catch_proofs.py`, and `verify_package.py` in its
ephemeral runtime. SymPy was absent there, so it did not rerun `derive_hierarchy.py`; the local
saved SymPy derivation and dependency-free replay remain separately typed.
