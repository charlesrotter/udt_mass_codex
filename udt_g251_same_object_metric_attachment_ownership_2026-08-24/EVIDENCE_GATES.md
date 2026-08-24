# G251 evidence gates

Date: 2026-08-24

1. **Preregistered:** PASS at `d76dfec4`, pushed before derivation.
2. **Whole or bounded scope:** PASS WITH BOUNDS. All 18 G250 candidates are classified on the one
   positive G249 homothety orbit after history and branch are supplied.
3. **Independent verification:** PASS. The standard-library implementation imports neither
   production code nor production output.
4. **Premise audit:** PASS internally against the exact 12-source manifest and current 233-row
   registry; external review remains pending.

Additional gates:

- production: 4,096 cases / 20,480 assertions;
- independent: 12,000 cases / 60,013 assertions;
- hostile mutations: 22/22 caught;
- candidate census: 18/18;
- observational values: zero;
- fitted coefficients: zero;
- protected work and BOSS/CMB outcomes: unopened.

Maximum pre-review grade: `INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.
