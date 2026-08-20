# G184 external-review packaging repair preregistration

Date: 2026-08-19

## Frozen external finding

The first fresh external gpt-5.4 review returned `G184_REPAIR_REQUIRED`. It independently accepted
the substantive witnesses but found that `verify_default_read_only_entrypoint.py` writes
`DEFAULT_ENTRYPOINT_VERIFICATION.json` on its default invocation inside a read-only intake. It also
found that `verify_package.py` trusts the stored helper artifact instead of live-replaying it.

## Exact permitted repair

Only these changes are allowed:

1. make the helper write its stored JSON artifact only under an explicit local-generation
   environment variable;
2. make the default `verify_package.py` replay the helper live and read-only;
3. prevent recursion by omitting the helper only from the nested verifier run carrying
   `G184_SKIP_DEFAULT_CHECK=1`;
4. regenerate the stored helper and package results locally through explicit write flags;
5. update evidence and review records to report the repair state.

## Frozen scientific content

The arena, equivalence relations, witnesses, counts, derivation, landing, physical-choice ledger,
falsifiers, and conclusion ceiling must not change. The repaired intake must still report:

```text
TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT
```

## Repair falsifiers

The repair fails if:

- either default verifier entrypoint writes in a read-only replay;
- the live helper replay recurses or is skipped by the ordinary package verifier;
- any source hash, scientific result count, witness, or landing changes;
- the first repair-required review is hidden or overwritten.

A fresh repair-only external review is required before banking.
