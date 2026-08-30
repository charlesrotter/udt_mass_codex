# G304 commands

## Sealed-intake replay commands

Run these from a writable ephemeral copy of the intake:

```bash
python3 udt_g304_global_cell_constant_sector_discriminator_2026-08-30/derive_global_cell_discriminator.py
python3 udt_g304_global_cell_constant_sector_discriminator_2026-08-30/verify_global_cell_discriminator_independent.py
python3 udt_g304_global_cell_constant_sector_discriminator_2026-08-30/run_catch_proofs.py
python3 udt_g304_global_cell_constant_sector_discriminator_2026-08-30/verify_package.py
```

The production derivation requires SymPy. When SymPy is not sealed into a review intake, reviewers
must not install it; they may inspect that script and run the dependency-free independent, catch,
and package checks.

## Repository-only banking gates

These commands require repository files intentionally absent from a source-bounded review intake:

```bash
python3 verify_current_scientific_premises.py
git diff --check
```

All computations are CPU symbolic or bounded scalar checks. No GPU, observation, network access, or
long-running process is used.
