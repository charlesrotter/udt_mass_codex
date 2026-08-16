# G117 evidence gates

1. **Preregistered — PASS.** Commit `a7890d9f` froze the types, formulas, data reductions,
   tolerances, non-identifiability witness, and maximum conclusion before confirmatory replay.
2. **Full or bounded — PASS in scope.** Every retained row of the two declared reductions was
   evaluated. Physical-history and global-regime completeness are explicitly excluded.
3. **Independently verified — PASS with caveats.** Production and the precision-domain verifier are
   closely inherited from G112 and therefore supply regression evidence. A fresh blind context
   separately parsed the raw data, rebuilt the P1 equivalence, covariance/Schur likelihoods, and
   exact rational witness, and returned `VERIFIED_WITH_CAVEATS`.
4. **Premises audited — PASS locally.** `TYPE_AND_PREMISE_LEDGER.tsv` separates observation,
   derived conditional geometry, chosen screen/transfer interfaces, and open history.

Repository premise/startup gates pass with the exact 104-row registry and line caps. The full suite
passes `90 passed, 1 xfailed`; the xfail is the unchanged known matter-sector habit-pin guard.
