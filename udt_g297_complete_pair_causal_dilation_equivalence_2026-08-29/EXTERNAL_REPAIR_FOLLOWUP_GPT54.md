# G297 external repair-only follow-up — gpt-5.4

Date: 2026-08-29

## Defects

None found.

## Repair verdicts

### R1 — implementation independence: PASS

`verify_causal_dilation_independent.py` imports only Python standard-library modules and does not
read production code or production output. The saved envelope reports 20,000 cases and 50,000
assertions. The exact derivation, evidence gates, audit report, and status ledger all use the
repaired count and independence boundary.

### R2 — general B-centered derivation: PASS

`EXACT_DERIVATION.md` explicitly derives the B-centered first germ from B-emission/B-return
future-null legs. It distinguishes that observer-reversed construction from algebraic inversion of
the A-centered legs and retains the supplied-observer/declared-route conditional scope. The status
ledger matches the written derivation.

### R3 — sealed replay contract: PASS

`COMMANDS.md` requires either a writable copy of the entire sealed intake or an explicit
`G297_SOURCE_ROOT`. `verify_package.py` and `run_catch_proofs.py` honor the inherited root.

From a writable copy under `/work`, the reviewer ran only the registered package verifier and
hostile-catch runner. They reproduced:

- 15 frozen source hashes;
- 125 production checks;
- 20,000 independent cases;
- 50,000 independent assertions;
- five hostile mutation catches.

## Scientific boundary

The unchanged bounded landing survives. No claim was found to exceed the repaired evidence.

```text
OWNER_CLARIFICATION_IS_SUBSTANTIVE_BUT_THE_TWO_LEG_COMPLETE_TRANSFER_REMAINS_UNDERDEFINED
__NO_UNIQUE_NONIDENTITY_FORM_YET
```

## Verdict token

```text
REPAIRS_VERIFIED__BOUNDED_LANDING_RETAINED
```
