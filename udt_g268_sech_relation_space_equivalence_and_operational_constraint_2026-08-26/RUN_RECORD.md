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

## Repair-only external follow-up

Sealed intake: `/tmp/udt_g268_repair_followup_y2nqoeyr`

Scope SHA-256: `03353578dd77252ef0d15fad06f378e780aa508e4ceb710fe3dcff68c14d1898`

Manifest SHA-256: `00970029cb1005d428b73db7d3fb11f5ab9ae85b0c00ada52bec582c62a35346`

External Codex `gpt-5.4` verified the seal, reran the registered no-write package replay, found no
remaining defect in R1 or R2, and confirmed that the bounded scientific landing was unchanged.
Disposition: `REPAIRS_ACCEPTED`.

No GPU, observation, fit, distance attachment, field equation, source, action, matter model,
`X_max`, or protected package was used.
