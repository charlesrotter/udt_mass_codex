# G313 repair-only preregistration

Date: 2026-09-01
Status: `PREREGISTERED_BEFORE_REPAIR_OUTCOMES`
Scientific question and landing: unchanged

External verdict:

```text
G313_REPAIRABLE_DEFECTS__SCIENTIFIC_LANDING_RETAINED
```

The repair scope is limited to the four reviewer findings below. No new universe selector,
history, scale, topology, population, source, action, matter model, mass law, observational result,
physical `X_max`, metric term, or reciprocal-kernel term may enter.

## R1 — replace the target-misaligned cosh check

Replace the production check that merely evaluates `cosh^2-sinh^2=1` with an exact evaluation of
the actual G309 residual

```text
Q[a] = a a'' - (a')^2 - 1
```

for `a(T)=X cosh((T-T0)/X)` over multiple exact rational `X` and hyperbolic parameter values. The
repair passes only if every registered residual is exactly zero and a mutation of the constant term
is caught.

## R2 — independently complete the positive product witness

Add an implementation-independent coordinate-tensor calculation for the explicit Lorentzian
`dS2 x S2` metric. Starting from the metric, inverse, and first/second coordinate derivatives, it
must reconstruct the Ricci tensor and verify `Ric_ab=Lambda g_ab` at multiple exact points and
positive `Lambda` values. Add a separate explicit global argument for periodic `chi`, compact
`S1 x S2` slices, temporal `tau`, and the Cauchy property. It must remain a witness, not a populated
history claim.

## R3 — strengthen the bootstrap/local-response type check

Replace the toy topology comparison with an exhaustive finite type model that distinguishes:

1. a whole-history acceptance predicate acting before local response;
2. a local response map that factors through the admitted finite metric jet; and
3. a forbidden hidden-history response assigning different responses to identical local jets.

The production and independent routes must separately show that a global selector can distinguish
histories with identical local jets without violating Local Metric Sufficiency, while the hidden
response fails the equal-jet factorization test.

## R4 — include direct G307 and G308 evidence

Add the exact G307 and G308 `AUDIT_REPORT.md` files to `SOURCE_SCOPE.tsv` and the sealed intake.
No claim from those reports may be strengthened; they are included only to make the existing
G305--G308 nonselection citation directly auditable.

## Certification contract

The repair may close only if:

- all four repairs are present and exact;
- production, independent, hostile, and aggregate no-write replays pass under `python3 -S`;
- a fresh manifest-authenticated sealed intake contains the direct G307/G308 sources;
- current premise and repository regression checks remain green;
- the landing remains exactly
  `ACTIVE_EQUATION_DEFINES_MULTIBRANCH_EINSTEIN_ARENA__GLOBAL_ADMISSIBILITY_REMAINS_OPEN`;
- a repair-only external reviewer verifies only R1--R4 and the unchanged landing.

Until that follow-up accepts, status remains
`REPAIRABLE_DEFECTS__SCIENTIFIC_LANDING_RETAINED__REPAIR_FOLLOWUP_PENDING`.
