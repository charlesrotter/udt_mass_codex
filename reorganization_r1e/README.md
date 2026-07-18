# R1E batch-migration planning records

R1E is a planning-only phase based on `b59005dba9acaf6c575185876655bd6a5c792094`.
It moves, renames, copies, deletes, and edits no research artifact. The exact 119-candidate
universe was frozen in preregistration commit `2755abb` before candidate content was inspected.

The controlling records are:

- [preregistration](R1E_PREREGISTRATION.md) and the
  [frozen candidate universe](PREREGISTERED_CANDIDATE_UNIVERSE.tsv);
- [complete candidate ledger](COMPLETE_CANDIDATE_LEDGER.tsv);
- [atomic family graph](ATOMIC_FAMILY_GRAPH.json) and
  [dependency evidence](DEPENDENCY_EVIDENCE.tsv);
- [batch ranking](BATCH_RANKING.tsv), [exact file plan](PROPOSED_BATCH_FILE_PLAN.tsv), and
  [rollback/verification contracts](R1E_BATCH_PROPOSALS.md);
- [proposed append-only migration-ledger schema](PROPOSED_MIGRATION_LEDGER_SCHEMA.tsv);
- [audit report](R1E_AUDIT_REPORT.md) and [machine verification result](VERIFY_RESULT.json).

The three ranked batches are proposals only. No R1F migration is authorized by these records.
