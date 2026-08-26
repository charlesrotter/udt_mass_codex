# G268 repair-only external follow-up request

Date: 2026-08-26

The fresh external review accepted scientific/type/scope questions 1–8 and returned
`ACCEPT_WITH_REPAIRS` on evidence question 9. Review only the two frozen repairs in
`REPAIR_PREREGISTRATION.md`:

1. Does R1 remove the flagged hardcoded items from the symbolic-check count and replace the
   algebraic positivity claims with genuine mechanical checks?
2. Does R2 inject each of the eight mutations through the same real exact-rational validator used by
   the passing baseline, with a named targeted failure for every mutant?
3. Does `verify_package.py` enforce the repaired evidence contract without changing the bounded
   scientific landing?

Return one of `REPAIRS_ACCEPTED`, `REPAIRS_ACCEPTED_WITH_NOTES`, or `REPAIRS_REJECTED`, with exact
file and line references for any remaining defect. Do not continue the research or reconsider the
already accepted scientific questions except to detect an accidental change caused by the repairs.
