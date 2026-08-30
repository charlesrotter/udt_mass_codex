# G301 preregistration

Date: 2026-08-30
Question class: `METRIC_LED_BOUNDED_CLASSIFICATION`

## Frozen question

Within the exact bounded lane in `MAP.md`, classify the residual solution classes before choosing
coefficients. Determine whether smooth scale freedom plus quiet causal regularity leaves one or
more inequivalent complete-metric principal classes.

## Frozen mathematical hypotheses

Let `K` be the finite-dimensional vector space of algebraic curvature tensors at a Lorentzian
point and `S2` the symmetric covariant two-tensors. A candidate residual map `F: K -> S2` is tested
under:

1. `F(0)=0` and `F` is differentiable at `0`;
2. `F(lambda K)=lambda F(K)` for every positive `lambda` in the star-shaped quiet domain;
3. `F` is natural under the unoriented Lorentz frame group;
4. no independent dimensionful scale or auxiliary field enters;
5. the residual is nonidentity;
6. quiet curved GR comparison members are not discarded merely because their native angular
   channels are individually nonzero;
7. a viable principal class must constrain all local metric polarizations modulo diffeomorphism
   gauge, rather than only a scalar trace.

Items 1--4 and 7 are `FREE_AND_EXPLORED` candidate law-class premises. They are not promoted to
F1--F4/W1/W3/W4/W5/W6 consequences.

## Frozen candidate classification

The production derivation must test, not assume, the following candidate reduction:

```text
F_ab = a Ric_ab + b R g_ab.
```

It must classify at least these mutually exclusive coefficient strata in four dimensions:

- `a = 0, b != 0`;
- `a != 0, a + 4 b != 0`;
- `a != 0, a + 4 b = 0`;
- `a = b = 0`.

It must not discard the exceptional `a + 4 b = 0` stratum merely because it is not the familiar
divergence-free representative.

## Residual-equivalence rule

Two residual formulas count as the same bounded law class only if they are related by an
invertible natural pointwise map on residual space. Such a map preserves the zero set and the
principal equation after multiplication by an invertible algebraic operator. Mere resemblance,
shared quiet solutions, or an observationally preferred interpretation is insufficient.

## Required witnesses

1. An exact inverse for the generic trace adjustment when `a != 0` and `a + 4 b != 0`.
2. A nonzero pure-trace Ricci witness admitted by the trace-free class and rejected by the generic
   class.
3. A nonzero traceless Ricci witness admitted by the scalar-only class and rejected by both
   complete classes.
4. The contracted-Bianchi consequence of the trace-free equation: scalar curvature is constant
   on each connected solution region.
5. A nonzero-frequency quiet-principal check showing whether the trace-free class has the same
   local causal propagation content as the Ricci-flat class, modulo one constant integration
   datum.
6. A proof boundary showing exactly where smoothness or scale freedom is used to exclude nonlinear
   curvature-ratio competitors.

## Preregistered landings

1. `ONE_EQUIVALENCE_CLASS_IN_BOUNDED_LANE`
   - all nonidentity, complete, quiet-causal residuals are invertibly equivalent.
2. `TWO_OR_MORE_INEQUIVALENT_CLASSES_SURVIVE`
   - an exact counterclass passes the frozen gates without an imported scale.
3. `HYPOTHESES_DO_NOT_SUPPORT_THE_CLAIMED_LINEAR_REDUCTION`
   - the homogeneity/naturality reduction fails or an unregistered competitor survives.
4. `INTERNAL_CERTIFICATION_FAILURE`
   - algebraic, provenance, replay, or hostile-catch gates fail.

## Falsification contract

Landing 1 is falsified by one smooth, scale-free, natural, metric-two-jet symmetric rank-two
residual that:

- is not related to the generic class by an invertible residual map;
- contains the quiet Ricci-flat comparison family;
- has nondegenerate metric-causal quiet principal behavior;
- uses no additional scale, field, source, action, or observation.

Landing 2 is falsified if every apparent exceptional class either loses complete principal rank,
is singular at the quiet origin, imports a scale, or is invertibly equivalent to the generic
class.

## Certification gates

- production derivation uses exact rational/standard-library arithmetic where executable;
- independent implementation imports no production function;
- coefficient strata are swept, not sampled only at a favored representative;
- hostile mutations catch the determinant/trace factor, exceptional-class deletion, scalar-lane
  promotion, premise promotion, and full-metric/angular deletion;
- source hashes and commands are recorded;
- result wording names the bounded lane and every remaining open architecture;
- fresh zero-context adversarial review is required before any banked verdict.

## Prohibited outcome-driven changes

No coefficient retuning, observed value, fitted profile, `X_max`, source, action, matter model,
distance law, cosmology, GR field equation import, protected package, or post-readout orchestra may
enter after outcomes are seen.
