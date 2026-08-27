# G275 second repair preregistration

Date: 2026-08-26

Trigger: external repair-only verdict `REPAIRS_NOT_ACCEPTED`. The reviewer retained the scientific
landing and accepted R1--R3 except for one sealed-replay self-containment defect.

## R4 — sealed repair replay self-containment

Repair the review builder and repair verifier so that:

1. `build_review_intake.py`, when invoked from a sealed intake, resolves frozen sources first and
   exclusively from the existing package-local `sources/` tree;
2. it never reaches Git or any path outside that sealed intake;
3. `verify_review_repairs.py --no-write` recognizes an existing sealed root and uses it as the
   immutable source for writable ephemeral test copies rather than depending on a repository root;
4. repository-mode building retains the exact preregistered-source fallback needed after live
   startup documents change;
5. a registered test launches the repair verifier from a fresh sealed intake and proves it passes;
6. a fake-Git tripwire remains untouched throughout sealed builder and verifier replay.

No scientific file, equation, landing, observational input, anchor, history, population, or
`X_max` statement may change.

Maximum conclusion before a fresh external second follow-up:
`SCIENTIFIC_LANDING_UNCHANGED__R4_IMPLEMENTED__PENDING_SECOND_REPAIR_FOLLOWUP`.
