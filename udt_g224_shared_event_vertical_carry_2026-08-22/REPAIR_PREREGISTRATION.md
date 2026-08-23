# G224 repair preregistration

Date: 2026-08-22

External verdict: `ACCEPT_WITH_REPAIRS`.

## Frozen repair R1 — distinct-event wording

Replace the stale final sentence of `OBSERVATION.md` with wording that distinguishes:

- the abstract isomorphism `mu_2^-1 mu_1`, which exists between two observer-calibrated
  future-null lines even at distinct events; and
- physical vertex composition, which requires the two supplied relations to share the same marked
  observer event.

No equation, result JSON, source, or scientific landing may change under R1.

## Frozen repair R2 — review-grade alignment

After R1 passes, update:

- `AUDIT_REPORT.md`;
- `EVIDENCE_GATES.md`;
- `STATUS_LEDGER.tsv`;
- `VERIFICATION_RESULT.json`;
- `verify_package.py`; and
- `run_catch_proofs.py`

to record `ACCEPT_WITH_REPAIRS`, the final externally reviewed grade, and the presence of the fresh
review and repair record.

## Repair acceptance gates

1. `OBSERVATION.md` no longer claims that abstract distinct-event normalization needs transport.
2. It still denies physical vertex composition without shared incidence.
3. The accepted landing is byte-identical.
4. All 24 symbolic checks, 20,000 independent cases, 220,003 assertions, source hashes, and
   no-write replay remain unchanged.
5. Catch proofs reject deletion or reversal of the repaired scope distinction and any false review
   grade.
6. No protected or unrelated local work is touched.
