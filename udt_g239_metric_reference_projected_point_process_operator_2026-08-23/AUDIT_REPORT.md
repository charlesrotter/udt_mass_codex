# G239 audit — metric/reference-projected point-process operator

Date: 2026-08-23

Status: `INTERNALLY_VERIFIED__EXTERNAL_REVIEW_OPEN`

## Landing

```text
REFERENCE_PROJECTED_METRIC_INTENSITY_OPERATOR_DERIVED_CONDITIONALLY
__MATCHED_REFERENCE_AND_ANGULARLY_CONSTANT_RESPONSE_CANCEL_EXACTLY
__NONCONSTANT_METRIC_PUSHFORWARD_CAN_SURVIVE_FIXED_SURVEY_REFERENCE
__CONNECTED_PAIR_TERM_SEPARATES_EXACTLY
__PHYSICAL_HISTORY_SOURCE_AND_BRANCH_POPULATION_OPEN
```

## What was learned

G238's missing reference-projected forward map now has an exact conditional form. For normalized
metric-pushed intensity `P`, normalized survey reference `Q`, bin kernel `K`, and connected observed
pair remainder `Gamma`, the population Landy--Szalay expectation is

\[
w_K=
\frac{\langle K,(P-Q)\otimes(P-Q)\rangle}{\langle K,Q\otimes Q\rangle}
+\frac{\langle K,\Gamma\rangle}{\langle K,Q\otimes Q\rangle}.
\]

A homogeneous Poisson source with factorized branch population gives `Gamma=0`; it remains
factorized under the metric observation map. Nevertheless its metric-pushed one-point intensity can
produce a nonzero reference-projected angular pattern when `P` differs from the separately supplied
survey reference `Q`.

Two cancellations are exact:

- a reference matched to the metric-pushed intensity gives zero;
- a purely angularly constant radial multiplier gives zero after normalization.

Therefore the simple spherical radial state still cannot generate the BOSS angular curve. A
nonspherical/direction-dependent complete-metric response can survive the fixed survey reference.
G127 supplies an exact local metric liveness witness: the tilted Jacobi area differs from the radial
control at coefficient `-2/25 lambda^4`. The arbitrary four-cell response used for the exact
Landy--Szalay witness is only operator certification and is not promoted to a metric history.

## Evidence

- preregistered and pushed at `c7257695` before witness evaluation;
- 12 frozen source hashes;
- exact rational finite witness with `DD=8/25`, `DR=11/25`, `RR=12/25`, and `w=-1/6`;
- exact zero matched-reference and common-response controls;
- exact connected decomposition with term `-1/240`;
- exact factorized branch/product pushforward proof;
- independent standard-library `Fraction` replay over 1,997 valid randomized cases;
- 11/11 hostile semantic mutations caught;
- BOSS outcomes remain closed.

## What remains

G239 narrows the gap but does not supply the physical values of `P` or `Gamma`. Those still require:

1. one continuous complete physical metric history;
2. observer/source incidence;
3. populated null branches and their weights;
4. a physical source one-/two-point hypothesis or law;
5. any native transfer required to relate source events to the catalogued population.

The next lawful step is to determine whether the already derived completed observer-pair family can
own a nonconstant whole-sky `P` without inserting a profile, or whether one explicit observational
history anchor must be frozen before BOSS outcomes are opened.

## Certification ceiling

This is a conditional operator theorem and exact existence/cancellation classification. It is not a
BOSS prediction, UDT validation, BAO-origin result, source law, history selector, feature scale, or
`X_max` result. Fresh external adversarial review remains required before startup integration.
