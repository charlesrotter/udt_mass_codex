# G240 fresh external adversarial review

Date: 2026-08-23

Reviewer: external Codex `gpt-5.4`, fresh ephemeral context, high reasoning, web disabled.

Primary landing:

```text
G240_REPAIR_REQUIRED__SCIENTIFIC_LANDING_RETAINED
```

## Finding R1 — sealed source-layout mismatch

The review builder copies the eleven manifest-bound source files under `intake/sources/`, while the
package verifier resolves those paths directly from the intake root. The delivered sealed replay
therefore fails before reaching the scientific checks. When the reviewer mirrored the same
hash-bound sources into the verifier's expected locations inside writable runtime space, the full
bounded replay passed.

This is a real reproducibility defect, not a failure of the derivation.

## Retained scientific result

The reviewer found the exact point-process result sound at its declared ceiling:

- `nu_2 = nu_1 tensor nu_1 + Sigma_sib` with ordered distinct image pairs;
- correct self-pair exclusion and `N^2 + S` normalization;
- exact reproduction of the G239 two-cell `+/-1/12` control;
- a genuinely separate 2,003-case exact enumerator;
- branch-relabel invariance and sky-permutation covariance;
- relevant hostile catches, including branch selection, arbitrary weights, sibling omission,
  self-pairs, wrong normalization, outcome opening, and forbidden inputs.

The theorem removes arbitrary numerical branch weights only inside the explicitly chosen query
`ALL_REGULAR_NULL_IMAGES_COUNTED_ONCE`. It does not prove that this query is Nature's detector or
transfer law.

Maximum retained conclusion:

```text
ALL_REGULAR_NULL_IMAGE_QUERY_REMOVES_ARBITRARY_BRANCH_WEIGHTS_CONDITIONALLY__METRIC_RELATION_INDUCES_IMAGE_INTENSITY_AND_SIBLING_PAIR_MEASURE_ON_A_SUPPLIED_HISTORY__PHYSICAL_HISTORY_SOURCE_MEASURE_TRANSFER_CRITICAL_STRATA_AND_OBSERVATIONAL_ANCHOR_OPEN
```

Required next action: repair the source-layout contract and prove that the no-write verifier passes
on a fresh sealed intake exactly as delivered. No observational outcomes or new physics may enter.

Raw runtime final-message SHA-256:
`5ddeeae908d5f00825152cc3f67ef154fb06e682095fe77df88bf7c6cf9886bb`.

The tracked transcription differs only by its terminating newline; its SHA-256 is
`015f2ccf300d21ce06bfea9051bf8423647aa08700987511cc9d311fae2cb070`.
