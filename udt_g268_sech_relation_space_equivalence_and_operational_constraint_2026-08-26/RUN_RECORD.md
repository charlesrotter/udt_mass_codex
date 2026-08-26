# G268 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `fc9b13ca`

## Production

```bash
python3 udt_g268_sech_relation_space_equivalence_and_operational_constraint_2026-08-26/derive_relation_equivalence.py
```

Initial result: `PASS`, 43 reported exact symbolic checks.

The first invocation stopped before writing a result because of three SymPy branch-simplification
limitations. `PREREGISTRATION_EXECUTION_NOTE.md` records the proof-method-only repair.

## Independent replay

```bash
python3 udt_g268_sech_relation_space_equivalence_and_operational_constraint_2026-08-26/verify_independent.py
```

Result: `PASS`, 95,617 exact-rational assertions across 1,100 ratios, 6,000 compositions, 2,000
associativity cases, and 1,200 varied networks containing 34,742 checked edges. It imports no
production module and reads no production result.

## Catch proofs

```bash
python3 udt_g268_sech_relation_space_equivalence_and_operational_constraint_2026-08-26/run_catch_proofs.py
```

Result: `PASS`, 8/8 preregistered mutations caught.

## External review and evidence repair

Fresh external review returned `ACCEPT_WITH_REPAIRS`: the bounded scientific landing survived, but
some reported exact checks were hardcoded and the original mutation script did not inject changed
logic through a real verification path. Repairs were frozen at commit `89670c8a` before execution.

R1 replaced the flagged positivity booleans with exact factorizations and mechanical SymPy queries,
and moved analytic zero-rejection and protocol-ownership conclusions outside the symbolic-check
count. Production now passes 41 mechanically evaluated exact checks.

R2 replaced the standalone bad-statement tests with one exact-rational `validate(candidate)` path.
The baseline produces no failures; eight separately mutated candidates each produce their
preregistered named failure class.

The production, independent, mutation, package, and repository-suite commands were rerun after the
repairs. Their final counts are recorded in `REPAIR_RESULT.md`.

No GPU, observation, fit, distance attachment, field equation, source, action, matter model,
`X_max`, or protected package was used.
