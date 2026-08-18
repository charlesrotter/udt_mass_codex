# G157 evidence gates

1. **Preregistered:** PASS — commit `c633b7d0` predates G157 outcome artifacts.
2. **Full bounded space:** PASS — the symbolic factorization and composition proof covers arbitrary
   regular `B+(2)` transitions; all 20 frozen sources have one ledger row.
3. **Independent verification:** PASS — no production import; 500 exact-rational semidirect trials
   plus 300 independent numerical subgroup trials, including 100 on the zero-reciprocal-generator
   branch.
4. **Premise audit:** PASS — the 144-row G157-extended registry and startup guards verify.

Fresh adversarial review: PASS — initial `PASS_WITH_REPAIRS`, then `FOLLOWUP_PASS` after all
mathematical, scope, ledger, and evidence-state repairs.

Repository regression: PASS — 117 passed, 1 expected xfail.

Package verification: PASS — 19 required files, 20 sources, 20 ledger rows, 10 exact checks, 500
exact semidirect trials, 300 subgroup trials, and 6 catches.

Maximum grade: `VERIFIED_WITH_CAVEATS`.
