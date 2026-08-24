# G243 preregistration — SNe-only radial spline representation

Date: 2026-08-24

Status: `PREREGISTERED_BEFORE_G243_EVALUATION__ANGULAR_AND_BOSS_OUTCOMES_CLOSED`

## Whole question and regime

Using only the exact G236 de-overlapped processed Pantheon+ and DES release vectors and their full
covariances, construct a smooth observational representation of

```text
theta(phi) = 5 log10[R(phi)/R(phi_min)]
```

on the common interval

```text
0.07077528204904217 <= phi=log(1+z) <= 0.7627571949083936.
```

Redshift is a direct reciprocal-depth readout. No angular response enters this reconstruction.

## Frozen data and query

Reuse the exact G236 cuts:

- 768 Pantheon+ rows after calibrator, low-redshift, survey-10, and common-support cuts;
- 1,623 DES survey-10 rows;
- transformed release observable `y=m-10log10(1+z)`;
- one free additive offset per release;
- Pantheon retained covariance and DES retained marginal covariance;
- zero unknown cross-release covariance after exact-CID de-overlap remains `CHOSE`.

All hashes are frozen in `SOURCE_MANIFEST.tsv`. No BOSS/BAO/CMB outcome may be read.

## Numerical representation census

For cubic B-spline basis count

```text
K in (16,24,32,48,64),
```

use uniformly spaced interior knots in founded depth `phi`, clamped endpoint knots, and anchor the
shape exactly by replacing each basis column with `B_j(phi)-B_j(phi_min)` and removing the one
partition-of-unity redundancy. The two release offsets remain unpenalized.

Let `X` be the block release design after full-covariance whitening and let `P` be the Gauss-
Legendre evaluation of

```text
integral [theta''(phi)]^2 dphi
```

on the spline basis. This is an observational roughness regularizer, not a UDT action.

Define the dimensionless regularization multiplier by

```text
lambda = alpha * trace(X_shape^T X_shape)/trace(P_shape)
```

and evaluate the fixed grid

```text
log10(alpha) = -12,-11.75,...,+11.75,+12.
```

For every `(K,alpha)`, solve the penalized full-covariance normal equations and compute

```text
edf = trace[(X^T X + lambda P)^-1 X^T X]
GCV = N * chi2_raw/(N-edf)^2.
```

The selected observational representation is the pair with smallest GCV over the complete fixed
census. If the minimum lies at either alpha boundary, return an unresolved regularization range;
do not extend it after seeing the outcome.

## Characterization, not filtering

On a fixed 4097-point grid report:

- `theta`, `theta'`, and `theta''`;
- the corresponding `s=(ln10/5)theta` first two derivatives;
- every connected interval on which `s'>0`;
- raw full-covariance chi-square, effective degrees of freedom, GCV, penalty, and condition number;
- the selected result's sensitivity to the adjacent registered basis counts.

Monotonicity is not imposed. A turning representation remains an observed statistical output but
cannot be globally inverted for a later G241 tidal carry.

## Certification

The production route may use NumPy/SciPy whitened least squares. An independent route must assemble
the block normal equations from Pantheon covariance solves and the DES marginal-precision Schur
route, without importing production code or reading its output. For every candidate, require
agreement within `1e-7` for raw chi-square and GCV and within `1e-8` for the selected coefficients.

Hostile checks must catch covariance diagonalization, deletion of a release offset, angular-term
insertion, monotonicity enforcement, alpha-grid extension after outcome, a Lambda-CDM distance,
P1/G116/G189/`X_max`, protected payload, or BOSS outcome access.

## Preregistered landings

- `SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__GLOBALLY_INVERTIBLE`
- `SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__TURNING_INTERVALS_RETAINED`
- `REGULARIZATION_MINIMUM_ON_REGISTERED_BOUNDARY__NO_FREEZE`
- `CROSS_ROUTE_OR_FULL_COVARIANCE_FAILURE__NO_FREEZE`
- `OUTCOME_LEAKAGE_OR_SCAFFOLDING__STOP`

## Maximum conclusion

At most G243 can freeze one SNe-only, processed, conditional, covariance-aware **observational
representation** of relative `R(phi)` and its derivatives. It cannot promote that representation
to the physical history, derive transfer, infer an angular response, predict BAO/CMB, determine
`X_max`, or validate UDT.
