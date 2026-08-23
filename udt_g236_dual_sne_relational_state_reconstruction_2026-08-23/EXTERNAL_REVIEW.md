# G236 fresh external adversarial review

Reviewer: external Codex `gpt-5.4`
Date: 2026-08-23
Intake: `/tmp/udt_g236_review_5ex3_c3_`
`REVIEW_SCOPE.json` SHA-256:
`87f46538fafa94b4e82e9d424dc17809b90c527f4b88c7ded9bc276a68cbc2cc`

## Finding

The sealed intake asserted preregistration and pre-outcome repair chronology, but did not contain
Git history or another immutable chronology artifact from which a fresh reviewer could verify that
claim. The reviewer therefore could not independently establish from the intake alone that commits
`184b1a78` and `318f35de` preceded every outcome artifact.

## Verdict

```text
G236_SCIENTIFIC_REPAIR_REQUIRED
```

The reviewer found **no scientific, statistical, type, or data-provenance error**. Read-only
recomputation reproduced:

- the sample counts `768` and `1623`;
- all `203` removed Pantheon+ survey-10 rows and `148` exact CID overlaps;
- the DES support bounds;
- all `K=8,12,16,24` reported chi-squares;
- the Pantheon covariance subsetting;
- the DES marginal covariance and independent omitted-block Schur complement; and
- the absence of P1, `X_max`, `tanh`, a Lambda-CDM distance curve, optimized knots, smoothing,
  monotonicity, and post-readout angular correction from the sealed production path.

The wrong DES principal-precision-submatrix shortcut was independently found to change the subset
covariance materially.

## Required repairs

1. Add auditable Git chronology evidence to the sealed intake.
2. Add evidence that the hostile preregistration repair did not change an observational result.

## Optional improvements

- stdout-only replay under a strict read-only reviewer;
- machine-readable overlap and resolution summaries.

No scientific landing is upgraded until a repair-only follow-up retains it.
