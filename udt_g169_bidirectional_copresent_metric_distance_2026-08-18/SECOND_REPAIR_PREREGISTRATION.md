# G169 second repair preregistration — germ/carry ledger alignment

Date: 2026-08-19

Trigger: repair-only external return `FOLLOWUP_REPAIR_REQUIRED__LANDING_SURVIVES`.

## Frozen repair

1. Change the `STATUS_LEDGER.tsv` object label from `physical two-ended germ ownership` to
   `physical two-ended germ and carry ownership`.
2. Change the `OUTCOME_PREMISE_LEDGER.tsv` statement from `physical co-present relation owns both
   endpoint germs` to `physical co-present relation owns both endpoint germs and inverse carry`.
3. Retain `OPEN_NOT_DERIVED` and state that the quotient cannot supply or replace either input.
4. Strengthen catch proofs and package verification to require the full germ-and-carry wording.
5. Change no algebra, landing component, or other premise status.
6. Rerun the complete internal package, premise, and repository gates before requesting a final
   repair-only follow-up.

## Falsifier

The repair fails if any live outcome ledger narrows the open ownership joint to endpoint germs alone
or promotes either the germs or carry to derived status.

## Maximum conclusion

The repair may only align ledger wording with the already retained landing. It cannot strengthen the
conditional reversal theorem or adopt a physical UDT distance definition.
