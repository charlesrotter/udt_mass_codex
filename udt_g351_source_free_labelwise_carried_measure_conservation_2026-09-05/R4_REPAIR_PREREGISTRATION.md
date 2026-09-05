# G351 R4 saved-aggregate and evidence-state repair preregistration

Date: 2026-09-05
Trigger: fresh R1--R3 completion verifier
Status: `PREREGISTERED_REPAIR_PENDING_EXECUTION`

## Frozen defects

- Current registered aggregate replay is 38/38, but `VERIFICATION_RESULT.json` still records the
  prior 34/34 state and prior review-status token.
- `EVIDENCE_GATES.md`, `STATUS_LEDGER.tsv`, and `RUN_RECORD.md` stop before completed R2/R3 replay.
- The aggregate checks only the saved landing, not exact saved-check/state reproduction or the
  evidence-state surfaces.

## Authorized repair

Update only the saved aggregate and evidence-state records to the already observed R1--R3 results;
add aggregate guards for exact saved-check reproduction and the three state surfaces. Do not alter
the theorem, premise, scripts' mathematics, source set, landing, or physical ceiling.

## Acceptance contract

- Saved aggregate exactly matches the live registered aggregate check map, count, landing, failed
  list, and review-state token.
- Evidence gates, status ledger, and run record all state that R1--R3 replay completed and that only
  R4 follow-up / sealed external review remains.
- Production stays 60,325/60,325; independent stays 11,290/11,290; hostile stays 12/12.
- Replay changes no bytes and creates no bytecode.

Maximum conclusion: evidence-state completion only; no scientific change.
