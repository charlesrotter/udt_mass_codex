# G330 R3 completion preregistration

Date: 2026-09-02
Trigger: repair follow-up verdict
`REPAIR_INCOMPLETE__G330_BOUNDED_SCIENTIFIC_LANDING_RETAINED`

The repair-only reviewer accepted R1 and R2 and retained the bounded scientific landing. It found
one exact mechanical omission in R3: `EXACT_DERIVATION.md` and `PREMISE_LEDGER.tsv` explicitly name
the standard isometry-extension consequence of the imported Einstein-Cauchy theorem, but
`LAY_REPORT.md`, `STATUS_LEDGER.tsv`, and `EVIDENCE_GATES.md` do not contain that explicit term.

Before implementation, the completion is frozen as follows:

1. Add `standard isometry-extension consequence` to the lay report's imported-theorem sentence.
2. Add the same explicit dependency to the `local_time_persistence` status row.
3. Add the same explicit dependency to the evidence-ledger item.
4. Strengthen `verify_package.py` to require `isometry-extension` in all five registered R3 records:
   exact, lay, premise, status, and evidence.
5. Update only the evidence status and follow-up record needed to report R1/R2 acceptance and R3
   completion pending final review.

No metric, equation, Berger data, Ricci formula, Hopf normalization, persistence interval,
topological conclusion, or scientific landing may change. The completion must not add global
persistence, arbitrary nonsymmetric perturbation stability, energetic stability, conservation,
matter/mass, occupancy, scale, `X_max`, or canon claims.

Maximum conclusion before final R3-completion review:

`DERIVED_CONDITIONAL__R1_R2_EXTERNALLY_ACCEPTED__R3_COMPLETED__FINAL_FOLLOWUP_PENDING`
