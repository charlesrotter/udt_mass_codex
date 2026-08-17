# G143 audit report — single-pair domain carry ownership

Date: 2026-08-17

Current grade: `VERIFIED_WITH_CAVEATS__FRESH_ADVERSARIAL_PASS`

## Result first

One supplied regular calibrated pair chart already owns a same-query identity-carry presentation.
Under a flag-preserving reparameterization, that identity becomes

\[
M_{BA}'=J_BJ_A^{-1},
\]

while `R_i'=R_iJ_i^-1`, so the total G142 comparison remains exactly invariant:

\[
C_{BA}'=R_B'M_{BA}'(R_A')^{-1}=R_BR_A^{-1}.
\]

This means no new carry mechanism is missing inside one fully specified calibrated query. G141 is
its same-chart presentation; G142 is its chart-covariant form.

## Boundary

The result is conditional on one supplied pair realization and a calibrated chart or atlas. The
pair metric owns Levi-Civita transport along a supplied path but not a universal path-independent
coordinate identity. Distinct queries, branches, or realizations remain unglued without overlap or
transport. No physical restriction to
`B^+(2)`, query family, metric history, proper length, or `X_max` is derived.

## Evidence

- preregistered and pushed at `3364b364` before execution;
- exact production algebra: 24/24;
- independent stdlib/Fraction replay: 28/28;
- frozen source hashes: 6/6;
- fresh adversarial review: `PASS`; production 24/24, independent 28/28, package 13/13,
  sources 6/6.

## Bounded landing

```text
ONE_SUPPLIED_CALIBRATED_PAIR_CHART_OWNS_A_SAME_QUERY_IDENTITY_CARRY_PRESENTATION__
FLAG_PRESERVING_REPARAMETERIZATION_MOVES_THAT_CARRY_TO_ENDPOINT_JACOBIAN_RATIO__
TOTAL_G142_COMPARISON_REMAINS_INVARIANT__
PAIR_METRIC_ALONE_DOES_NOT_SUPPLY_UNIVERSAL_PATH_INDEPENDENT_IDENTITY_BETWEEN_SEPARATED_TANGENT_FIBERS__
CROSS_QUERY_BRANCH_NETWORK_CARRY_AND_PHYSICAL_HISTORY_REMAIN_OPEN
```
