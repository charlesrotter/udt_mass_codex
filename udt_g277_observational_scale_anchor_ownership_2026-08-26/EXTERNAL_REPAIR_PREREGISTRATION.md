# G277 external-review repair preregistration

Date: 2026-08-26

External verdict: `ACCEPT_WITH_REPAIRS`

Raw response SHA-256:
`21e2882cdcf14ce62441cb7c211925c8ad5a4d7c16822a2eca4906abc36d8ff3`

The reviewer independently reproduced the 1,657-row mask, 77 calibrators, raw covariance defect,
and all three weighted-rank-two symmetric routes. It retained the complete bounded scientific
landing and requested two evidence-only repairs.

## R1 — separate repository evidence from sealed-review evidence

Retain the repository-wide `181 passed, 1 xfailed` result as local repository evidence, but mark it
explicitly `OUTSIDE_SEALED_REVIEW_SCOPE__NOT_EXTERNALLY_REPLAYED`. The sealed external evidence
claim may include only the 49-file containment, 48 manifest entries, 18 source hashes, three
registered no-write replays, and the reviewer's direct covariance replay.

Do not rerun or import repository tests into the repair-only intake.

## R2 — distinguish same-object identity from transfer/distance ownership

The independent verifier must derive two separate facts:

1. `same_object`: whether a supplied physical record is identified with the exact modeled object or
   segment, using the frozen G250/G251/G276 ownership sources;
2. `bridge_owned`: whether the operational-distance and radiative-transfer comparison is already
   owned, using the frozen G258/G275 sources.

For the SNe and DES routes, both facts remain false, but for different source-backed reasons. The
G276 exact-segment clock control remains true on both. Derive every production candidate row through
the explicit predicate so the independent evidence does not silently cover a smaller candidate
census than the production ledger.

## No-change contract

These repairs may not:

- inspect an observational fit or compute a numerical scale;
- change any candidate, primary class, rank, covariance route, or scientific landing;
- alter the metric, kernel, W5, transfer status, history, operational-distance status, or `X_max`;
- access or touch protected work.

## Acceptance

R1 and R2 pass only if:

1. sealed versus repository-only evidence is explicit in every affected report;
2. the independent verifier emits distinct source-derived `same_object` and `bridge_owned` facts for
   all eight production candidates;
3. all eight independent classes exactly equal the frozen production classes;
4. all 18 source hashes, three no-write replays, eleven hostile controls, and the bounded landing
   remain unchanged;
5. a sealed repair-only follow-up accepts the repairs.
