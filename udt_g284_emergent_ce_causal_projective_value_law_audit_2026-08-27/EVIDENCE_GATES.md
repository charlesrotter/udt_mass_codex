# G284 evidence gates

Date: 2026-08-27

1. **Preregistered:** PASS — commit `c61ed4f4` predates outcome execution.
2. **Full bounded space:** PASS — generic smooth symmetric `T(u)` remains symbolic; local regular
   causally convex tube and finite path-labelled network only.
3. **Independent verification:** PASS internally — 512 exact cases, 7,168 assertions, and 64
   varying-tide network cases use no production output or implementation.
4. **Premises audited:** PASS internally — all excluded physics and stronger causal premises remain
   explicit.
5. **Fresh external adversarial review:** `ACCEPT-WITH-REPAIRS` — no scientific defect; the bounded
   landing survived unchanged. One dependency/replay packaging defect and one executable-evidence
   defect were preregistered as R1/R2 and repaired.
6. **Repair replay:** PASS internally — all four recomputations now run with `python3 -S` in an
   ephemeral exact-source copy, and an artifact-level broken-replay mutation is rejected.
7. **External repair-only follow-up:** PENDING.

Until gate 7 closes, the result remains repair-follow-up pending and must not enter
`CURRENT_SCIENTIFIC_PREMISES.tsv` or the startup surface.
