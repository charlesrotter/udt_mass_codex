# G236 external-review repair preregistration

Date: 2026-08-23
Status: evidence-only repair; scientific result frozen

## Trigger

The fresh external reviewer reproduced the scientific and numerical result but returned
`G236_SCIENTIFIC_REPAIR_REQUIRED` because the sealed intake did not contain independently auditable
Git chronology.

## Frozen scientific content

The following may not change during this repair:

- observational data or cuts;
- transformed observable;
- covariance construction;
- fitted state coefficients or uncertainties;
- all four raw and shape chi-squares;
- hostile definitions, values, or pass thresholds;
- result landing and scientific scope.

## Registered repair

Add only:

1. exact raw Git commit objects and recursive tree listings for `184b1a78` and `318f35de`;
2. the exact patch and changed-path record for the repair commit;
3. a machine-readable chronology and hostile-noninterference proof;
4. a repair-only review request and fresh sealed intake containing those artifacts.

The chronology proof must establish cryptographically checkable commit hashes and the parent order

```text
184b1a78 -> 318f35de
```

and show that the second commit changed only `PREREGISTRATION.md` and added
`PREREGISTRATION_REPAIR.md`. It must also show that neither committed tree contains production
code, reconstructed state, or outcome artifacts.

The hostile-noninterference proof must show structurally that the production reconstruction and
landing are computed from the release data before the hostile-control object is constructed, and
that hostile values are certification gates and reported metadata rather than inputs to the state
coefficients or concordance statistic.

## Honest proof ceiling

Git can prove commit identity, parent order, and committed-tree contents. It cannot retroactively
prove the absence of an untracked private computation. The repair must state that limitation rather
than presenting Git chronology as proof of an impossible negative. The intended evidence grade is
`PASS_REPOSITORY_CHRONOLOGY_WITH_RETROACTIVE_UNTRACKED_ABSENCE_LIMIT`.

## Follow-up return

The repair-only reviewer must return whether these exact evidence repairs close the original
contract issue while leaving the scientific landing unchanged. Any scientific or numerical change
invalidates this repair path and requires a new preregistration.
