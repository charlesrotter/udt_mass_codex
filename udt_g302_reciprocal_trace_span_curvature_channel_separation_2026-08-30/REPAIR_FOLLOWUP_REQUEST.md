# G302 repair-only external follow-up request

Date: 2026-08-30

Verify only the preregistered G302 domain-certification repair and the unchanged scientific landing.
Do not reopen, alter, or continue the research.

## R1 — exhaustive independent domain census

1. Confirm `verify_domain_census_independent.py` imports no production function and runs under
   dependency-free `python3 -S`.
2. Verify the nondimensionalized positive- and negative-curvature cubics and discriminants.
3. Verify that `x=1,beta=-2/3` is the only positive repeated-root boundary for `R0>0`, and that it
   maps to `b=-4/(3 sqrt(R0))`.
4. Verify `beta=0` is separately treated as the excluded `r=0` crossing.
5. Check the exact Sturm implementation and every registered connected parameter cell, including
   the positive discriminant boundary at `beta=+2/3`.
6. Verify interval orientation follows from root count, `P(0)=b`, leading sign, monotonicity/maximum,
   and exact double-root factorization.
7. Confirm all eight `DOMAIN_CLASSIFICATION.tsv` rows are compared field by field and pass.
8. Run the dependency-free verifier and six hostile domain mutations in a writable ephemeral copy.

## R2 — wording and unchanged landing

9. Confirm the original review and its caveat remain preserved rather than overwritten.
10. Confirm the updated audit/evidence/status wording says internal exhaustive repair is complete but
    repair-only external follow-up remains open.
11. Confirm no formula, metric, kernel, field equation, history, mass, observation, physical-query,
    nonspherical, or time-live claim changed.
12. Confirm the retained landing remains exactly:

```text
RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN
__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION
```

Return `ACCEPT_REPAIRS` or `REJECT_REPAIRS`, identify any exact remaining defect, and state whether
the scientific landing changed.

