# G253 repair-only follow-up request

Review only the preregistered G253 sealed-source replay repairs and the unchanged bounded scientific
landing.

## Required checks

1. Verify `REVIEW_SCOPE.json` and every payload SHA-256 before opening evidence.
2. Read `EXTERNAL_REVIEW_GPT54.md`, `REPAIR_PREREGISTRATION.md`, and
   `REPAIR_IMPLEMENTATION.md`.
3. Run the four commands registered in `REVIEW_SCOPE.json` from the sealed intake.
4. Confirm that repository and sealed source layouts are accepted only when every existing source
   candidate matches its frozen manifest hash.
5. Confirm that missing, mismatched, and conflicting dual-layout cases fail closed.
6. Confirm that production and independent scientific results are unchanged and that no new source,
   premise, formula, node, edge, observational value, fitted coefficient, or protected input entered.

Do not continue the research or reconsider unrelated scientific questions. Return
`REPAIRS_ACCEPTED`, `REPAIRS_INCOMPLETE`, or `SCIENTIFIC_LANDING_CHANGED`, with exact reasons.
