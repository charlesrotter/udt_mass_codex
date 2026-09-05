# G351 R2 notation and evidence-state repair preregistration

Date: 2026-09-05
Trigger: fresh post-R1 blind verification
Status: `PREREGISTERED_REPAIR_PENDING_EXECUTION`

## Frozen defects

1. After decomposing `mu=mu_ac+mu_s`, the density display still wrote
   `n_i=dmu/dArea_i`; it must say `n_i=dmu_ac/dArea_i`.
2. The conservation quotient in equation (5) reverted to dimensionful `omega_i^w` notation; it
   must retain `(omega_i/omega_*)^w` even though the common reference cancels.
3. `EVIDENCE_GATES.md`, `STATUS_LEDGER.tsv`, and the final sentence of `RUN_RECORD.md` still marked
   the R1 aggregate replay pending after it had passed 34/34.
4. The aggregate verifier did not guard the exact `dmu_ac` notation or the dimensionless form in
   equation (5).

## Authorized repair

Change only those two proof notations, reconcile the three evidence-state statements to the
already observed 34/34 R1 replay, and add exact aggregate guards. Do not change the theorem,
premise, source set, numerical results, landing, or physical ceiling.

## Acceptance contract

- `n_i=dmu_ac/dArea_i=s/J_i` appears exactly.
- Both the component definition and the equation-(5) conservation quotient contain the common
  dimensionless reference `omega_*`.
- Aggregate replay passes all old gates plus the two new notation gates without changing bytes.
- Production remains 60,325/60,325, independent remains 11,290/11,290, and hostile catches remain
  12/12.

Maximum conclusion: notation and evidence-state repair only; no scientific change.
