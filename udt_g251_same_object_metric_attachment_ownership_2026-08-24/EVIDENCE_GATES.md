# G251 evidence gates

Date: 2026-08-24

1. **Preregistered:** PASS at `d76dfec4`, pushed before derivation.
2. **Whole or bounded scope:** PASS WITH BOUNDS. All 18 G250 candidates are classified on the one
   positive G249 homothety orbit after history and branch are supplied.
3. **Independent verification:** PASS. The standard-library implementation imports neither
   production code nor production output and independently rebuilds the cited ledger digest.
4. **Premise audit:** PASS internally against the exact 12-source manifest and current 233-row
   registry. The sealed registry-only replay is self-contained; the broader repository startup and
   premise verifier also passes separately.
5. **Fresh external review:** `ACCEPT_WITH_REPAIRS`; the scientific landing was retained.
6. **R1/R2 repair:** PASS internally under preregistration committed at `bd8f0a2b`; repair-only
   follow-up remains pending.

Additional gates:

- production: 4,096 cases / 20,480 assertions;
- independent: 12,000 cases / 60,014 assertions;
- hostile mutations: 26/26 caught;
- explicit cited ownership cells: 72/72;
- sealed premise registry: 233/233 rows, exact hash;
- candidate census: 18/18;
- observational values: zero;
- fitted coefficients: zero;
- protected work and BOSS/CMB outcomes: unopened.

Current maximum grade: `EXTERNAL_REVIEW_ACCEPT_WITH_REPAIRS__REPAIRS_INTERNALLY_VERIFIED__FOLLOWUP_PENDING`.
