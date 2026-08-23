# G233 run log

Date: 2026-08-23

## Production

Command:

```bash
python3 derive_primary_profile_cartan_closure.py
```

Result: exit 0; all 11 registered checks passed. Full stdout content is preserved structurally in
`exact_results.json`.

Key exact outputs:

```text
metric jet nonzero counts orders 0..5 = 0,0,0,0,0,2
n^0 Rscalar = 0
n^1 Rscalar = 12/r0^3
n^2 Rscalar = 24(2c-1)/r0^4
n^3 Rscalar = 12(20b-24c+1)/r0^5
b1-b0 next difference = 240/r0^5
```

Arbitrary-order coefficients for `N=0..6` matched
`2(N+3)!/r0^(N+3)` exactly.

## Independent first run

Command:

```bash
python3 verify_independent_series.py
```

Result: exit 1. The load-bearing invariant difference passed exactly (`560/81`), while the
geodesic-series guard failed because it inspected coefficients at the truncated series boundary.
The exact failed result is preserved in `INITIAL_INDEPENDENT_FAILURE.json` and the repair was frozen
in `REPAIR_PREREGISTRATION.md` before editing.

## Independent repaired run

Same command. Result: exit 0; all seven checks passed. Full stdout content is preserved
structurally in `independent_results.json`.

Exact independent values with `c=2`, `r0=3`, `b=-2,5`:

```text
shared state through nabla^2 scalar contractions = [0, 4/9, 8/9]
next values = -116/27 and 212/81
difference = 560/81
expected = 560/81
```

The exact test values are algebraic replay choices, not physical calibrations.

## Package, catch proofs, and root gates

```text
python3 verify_package.py --replay
PASS: six package/source/no-write replay checks

python3 hostile_mutation_tests.py
PASS: seven of seven substantive evidence mutations caught

python3 verify_current_scientific_premises.py
PASS: 215-row registry and G232 startup guards

python3 -m pytest tests/
PASS: 137; XFAIL: 1 known matter-lane premise debt
```

The root suite initially exposed stale G232 startup catch-proof and readability debt. Every failure
and repair scope is preserved in the four `STARTUP_REPAIR_*` preregistration records. No scientific
equation or G233 result changed during those repairs.

## Fresh external review

The sealed 32-file intake had `REVIEW_SCOPE.json` SHA-256
`337c310f7dd69ba03cd5b2f07314a3c29e3984c334e7c6e3dd6e18a7a1961521`.

The external gpt-5.4 reviewer returned `VERIFIED_WITH_CAVEATS`, reran the six registered no-write
checks and seven hostile checks, and independently checked all 31 payload hashes. No scientific
repair was required. Its sole packaging caveat was one form-feed character replacing `\frac` in
`EXACT_DERIVATION.md`; the repair was preregistered and changed no mathematical content.

Post-repair gates:

```text
python3 verify_package.py --replay --no-write
PASS: six checks

python3 verify_current_scientific_premises.py
PASS: 216-row registry and G233 startup/premise guards

python3 -m pytest tests/test_startup_surface.py -q
PASS: 64

python3 -m pytest tests/ -q
PASS: 138; XFAIL: 1 known matter-lane premise debt

python3 verify_final_evidence_manifest.py
PASS: 30 final evidence hashes and exact membership
```
