# G256 run record

Date: 2026-08-25  
Branch: `grok`  
Preregistration commit: `6a5cfb91`

No GPU, observational outcome, fit, ODE, or PDE was used.

Production command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 udt_g256_primary_state_value_closure_rank_2026-08-25/derive_value_closure.py --output udt_g256_primary_state_value_closure_rank_2026-08-25/DERIVATION_RESULT.json --rank-atlas udt_g256_primary_state_value_closure_rank_2026-08-25/VALUE_CLOSURE_RANK.tsv --hermite-atlas udt_g256_primary_state_value_closure_rank_2026-08-25/HERMITE_REALIZATION_ATLAS.tsv
```

Independent command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 udt_g256_primary_state_value_closure_rank_2026-08-25/verify_independent.py --output udt_g256_primary_state_value_closure_rank_2026-08-25/INDEPENDENT_VERIFICATION.json
```

Hostile-control command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 udt_g256_primary_state_value_closure_rank_2026-08-25/run_catch_proofs.py --output udt_g256_primary_state_value_closure_rank_2026-08-25/CATCH_PROOF_RESULT.json
```

Repository premise gate:

```bash
python3 verify_current_scientific_premises.py
```

All displayed commands exited zero in the repository before sealing.

## Original sealed-review finding

The original intake's `verify_package.py --no-write` failed because it attempted to rerun the
repository-wide premise verifier, which was not included in the sealed intake. The independent and
hostile-control registered commands passed, and the reviewer retained the scientific landing.

## R1 repair-only review

R1 removed the repository-external call, but the minimal external runtime exposed an undeclared
SymPy dependency. The independent standard-library replay exited zero; the package verifier and
hostile replay exited one before completion because `sympy` was unavailable. The reviewer retained
the scientific landing and returned `G256_R1_REPAIR_INCOMPLETE`.

## R2 repair replay

R2 preserves the original SymPy production script and frozen products but does not execute that
script inside the seal. The package verifier instead validates the frozen production fields and
atlases against the independent exact-Fraction replay. The hostile controls now duplicate only the
small validation predicates they attack and use the standard library exclusively. All three
registered commands must exit zero in a minimal runtime with no third-party Python packages.

## R2 external closure

Fresh gpt-5.4 repair-only review verified all 47 sealed payload rows and all 18 scientific source
hashes. The package verifier, independent replay, and hostile controls each exited zero in the
minimal runtime. It returned
`G256_R2_SELF_CONTAINED_REPLAY_ACCEPTED__SCIENTIFIC_LANDING_RETAINED` with no remaining defect in
scope.
