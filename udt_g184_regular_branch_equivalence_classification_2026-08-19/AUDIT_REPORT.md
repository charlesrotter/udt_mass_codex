# G184 audit report — regular branch equivalence

Date: 2026-08-19

## Primary result

G184 reaches the corrected preregistered landing:

```text
TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT
```

Two supplied regular branches are the same realization in different coordinates exactly when a
query-preserving pair-domain diffeomorphism makes their immersion diagram commute. If the fully
typed query explicitly admits ambient isometries, the quotient can be enlarged by those symmetries.
The two quotients must not be silently conflated.

The metric-native completed kernel descends through either lawful quotient. The converse fails:
equal endpoints, depth, tape, pair metric, or image do not generally establish realization
equivalence.

## Decisive counterexamples

- A nonlinear marked reparameterization gives the expected exact pullback and completed-density
  covariance.
- A unit-speed semicircle and unit-speed helix join the same observer lines and induce the identical
  metric `-dt^2+ds^2`, but their squared second-fundamental-form norms differ. No domain or ambient
  isometry identifies them.
- Circle immersions of degree one and two have the same image but cannot be related by a domain
  diffeomorphism because absolute degree is invariant.
- The G183 reflected polynomial and opposite-lift winding branches are strict-distinct but become
  symmetry-equivalent only when the relevant reflection is explicitly admitted. A typed
  transverse/circle orientation excludes it.

## Evidence

- preregistration commit: `32d53ab9`;
- terminology clarification commit: `2302e924`;
- 12,000 production exact-rational families and 121,544 assertions;
- 20,000 independently generated exact-rational families and 145,709 assertions;
- 10,158 orientation-preserving and 9,842 orientation-reversing independent Jacobians;
- exact witness derivations plus 2,001-point independent helix/semicircle derivative replay;
- 30 executable mutation catches and 12 semantic guards;
- eight immutable load-bearing source hashes;
- fresh external gpt-5.4 independently reproduced the substantive witnesses and returned
  `G184_REPAIR_REQUIRED` for one default-helper write defect only;
- the exact preregistered packaging repair now makes both default verifier entrypoints no-write and
  makes `verify_package.py` live-replay the helper;
- fresh external repair-only follow-up returned `G184_REPAIR_ACCEPTED` after both entrypoints passed
  without changing the sealed intake tree.

## Scientific grade and ceiling

`VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REPAIR_FOLLOWUP_ACCEPTED`

This is one bounded quotient tile on the G183 regular branch arena. It does not define the physical
query symmetry group, select a branch or observer population, infer holonomy, extend through a
degenerate stratum, or derive any global completion, `X_max`, observation, dynamics, action, source,
matter, bootstrap, radiative-transfer, or signalling result.
