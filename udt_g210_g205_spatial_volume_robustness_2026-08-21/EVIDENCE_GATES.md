# G210 evidence gates

Date: 2026-08-21

1. **Preregistered — PASS.** Commit `d1458d37` was pushed before outcomes.
2. **Full space or bounded scope — PASS WITH CAVEATS.** The unique local determinant scalar is
   complete; global results cover only declared G205 subclasses.
3. **Independent verification — PASS WITH CAVEATS.** The separate Fraction implementation checks
   10,000 distinct exact cases and 250,001 assertions without importing production code. The
   analytic global theorems remain separately argued.
4. **Boundary controls — PASS.** Four registered profiles passed at 120 digits.
5. **Premise audit — PASS.** The 193-row verifier passed before the solve.
6. **Hostile catches — PASS.** Twenty-five mutations cover determinant factors, cone center/width,
   affine/global typing, pair strata, evidence ceiling, history selection, and `X_max`.
7. **Fresh external review — PASS WITH CAVEATS.** External `gpt-5.4` verified the 35 scoped
   payload hashes, passed the registered no-write replay, found no mathematical refutation, and
   requested no repairs. The global G205 survivor/failure results remain analytic rather than
   independently mechanized end to end.

Current package grade: `EXTERNALLY_VERIFIED_WITH_CAVEATS__NO_REPAIRS_REQUIRED`.
