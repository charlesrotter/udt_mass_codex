# Preregistration — twisted `S3` intrinsic clock/ruler witness

Date: 2026-07-27

Base: `cacfaa178d2199ecb13d5196545ff36797c82177`

Question type: **METRIC-LED, OBSERVING A BOUNDED CONFIGURATION FAMILY**.

## Whole question

Does one explicit, globally complete member of the already registered twisted reciprocal-coframe
family allow the complete metric—not its coordinate presentation—to identify both:

1. the stationary clock line through an intrinsic scalar-invariant certificate; and
2. the reciprocal ruler line through the nonzero twist of that same clock line?

The test characterizes eight frozen configurations. It does not ask for a particle, action,
preferred topology, preferred `lambda`, empirical fit, or desired cosmology.

## Premise stamps carried forward

These four distinctions are mandatory in every result:

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

Co-presence means that the events belong to one complete candidate solution. It does not supply the
solution law, erase metric intervals, force endpoint-only comparison, or derive signalling. The
algebra below must remain valid if the co-presence interpretation is later abandoned.

## Frozen configuration family

Let `q=(q0,q1,q2,q3)` be the unit-quaternion coordinates on `S3`, and let `sigma_i` be the global
left Maurer-Cartan coframe. In unit conventions `c_E=R=1`, test

```text
tau     = dt + a sigma_3
theta_0 = exp(-phi) tau
theta_1 = exp(+phi) sigma_3
theta_2 = exp(lambda phi) sigma_1
theta_3 = exp(lambda phi) sigma_2
g       = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2.
```

The units remove no dimensionless degree of freedom and do not select physical `R`, `c_E`, `a`, or
`lambda`. Dimensions can be restored after the invariant certificate.

For C01–C07 use `phi=epsilon f`, with

```text
f = q1 + 2 q2 + 3 q3
  + q1 q2 + 2 q2 q3 + 3 q3 q1
  + 2 q1^2 - 3 q2^2 + 5 q3^2
  + q1 q2 q3 + 2 q1^3 - q2^3 + 3 q3^3.
```

This is a deterministic free profile, not a field-equation solution. Its coefficient bound is
`|f| <= 29`. With `epsilon=1/50` and `|a|=1/64`, the strict slice gate follows from
`|phi|<=29/50` and `1/64 < exp(-58/50)`; the verifier must certify a rationally bounded version of
that inequality rather than rely on floating-point sampling.

The exact candidates are frozen in `CANDIDATE_UNIVERSE.tsv`. No profile or parameter may be added,
removed, or retuned after invariant ranks are inspected.

## Intrinsic certificate

Use three scalar invariants of the complete four-metric:

```text
I1 = scalar curvature,
I2 = Ricci_ab Ricci^ab,
I3 = Riemann_abcd Riemann^abcd.
```

At the frozen north-chart event `q=(1,0,0,0)`, compute their spatial gradients with exact arithmetic.
If the `3 x 3` gradient determinant is nonzero, every Killing field must have value proportional to
`K=partial_t` at that event. Subtracting that multiple of `K`, preservation of the three invariant
covectors forces the residual Killing one-jet to vanish. A Killing field is determined by its
one-jet through Killing transport/Jacobi continuation. Therefore the local and hence global Killing
algebra is exactly the line spanned by `K`.

The verifier must independently audit every implication in this paragraph. Merely finding three
different numerical invariant values, or a nonzero floating determinant, is insufficient.

## Computation contract

- CPU only; no GPU.
- Exact rational multivariate jets through the order required for first derivatives of all three
  curvature invariants.
- A separate high-precision or independently implemented exact replay may diagnose the calculation,
  but may not replace the exact determinant certificate.
- All eight candidates are reported, including rank-deficient and control outcomes.
- The twist-off and depth-off controls must fail their corresponding all-gate requirements.
- No action, equation of motion, stability, endpoint/path ontology, signal law, carrier, source,
  density, bootstrap, mass, or `X_max` inference is allowed.

## Falsification and maximum conclusion

If at least one of C01–C06 has an exact nonzero gradient determinant and passes all regularity,
slice, timelike-clock, nonzero-twist, reciprocal-weight, and provenance gates, the maximum result is:

```text
ONE_COMPLETE_TWISTED_S3_CONFIGURATION_HAS_A_METRIC_INTRINSIC_CLOCK_LINE_AND_TWIST_SELECTED_RECIPROCAL_RULER_LINE;
ALL_GATE_CONFIGURATION_EXISTENCE_DERIVED_IN_THE_FROZEN_FAMILY;
NO_ON_SHELL_SELECTION_OR_PHYSICAL_LAW_DERIVED.
```

If none passes, the maximum negative is only:

```text
THREE_SCALAR_INVARIANT_RANK_ROUTE_NOT_CERTIFIED_IN_THE_EIGHT_FROZEN_CONFIGURATIONS.
```

It is not a no-go for the full smooth family. A computation or proof gap remains `OPEN`, not a
negative result.

## Completeness map

This audit covers one stationary analytic `R x S3` configuration family, all four metric coframe
legs inside that ansatz, global regularity, local invariant rank, stationary-line uniqueness, and
clock twist. It drops field equations, action terms, variation, boundary selection, time-live
branches, alternative completions, bifurcations, stability, carrier, matter, scale selection, and
physical regime. Every dropped sector could still select or reject the configuration. This audit is
one configuration-space tile, not closure of the metric's solution space.
