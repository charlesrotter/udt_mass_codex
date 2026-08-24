# G241 preregistration — SNe-anchored native tidal bridge

Date: 2026-08-23

Status: `PREREGISTERED_BEFORE_G241_CARRIER_EVALUATION__BOSS_OUTCOMES_CLOSED`

## Whole question and exact bounded regime

Can the byte-frozen G237 `K=12` relative state calibrate a smooth, invertible relative radial
history on

```text
0.07077528204904217 <= phi <= 0.7627571949083936
```

using no more than four observational coefficients, such that the already derived G127 local
tilted-screen curvature is then fixed with no angular coefficient?

This is metric-led after an explicit observational calibration. It is not a derivation of the
history from the founding postulates, a BOSS fit, or a search for a preferred feature.

## Frozen input

The only numerical observational input is the exact file and hash in `SOURCE_MANIFEST.tsv`:

- twelve fixed `phi` knots;
- eleven non-anchor relative-state coordinates `theta`;
- the full `11 x 11` frozen covariance;
- the G237 query and processing caveats unchanged.

No raw BOSS catalogue outcome, angular curve, covariance, feature, shell value, or descriptor may
be read during G241 evaluation. BOSS type metadata are not numerical inputs to this calculation.

## Registered carrier family

Let `phi_0` and `phi_1` denote the first and last frozen depth knots and define

```text
t(phi) = 2 (phi-phi_0)/(phi_1-phi_0) - 1.
```

For degree `d` in the fixed ordered candidate list `(2,3,4)`, define

```text
theta_d(phi) = sum_{k=1}^d c_k [T_k(t(phi)) - T_k(-1)],
```

where `T_k` is the Chebyshev polynomial. The subtraction makes the frozen first knot the exact
relative anchor. Chebyshev polynomials are a numerical representation choice in the founded depth
coordinate, not physical modes.

For each degree, the coefficients are fixed once by full-covariance generalized least squares:

```text
c = (B^T C^-1 B)^-1 B^T C^-1 theta.
```

No smoothing parameter, coefficient prior, monotonicity penalty, refit, or post-fit correction is
allowed.

## Adequacy and selection gates

For each candidate in ascending degree:

1. the frozen covariance and normal matrix must be positive definite;
2. the raw state residual must satisfy
   `chi2 <= scipy.stats.chi2.ppf(0.999, 11-d)`;
3. `s(phi)=(ln(10)/5) theta_d(phi)` must have strictly positive derivative throughout the closed
   interval;
4. the derived tidal invariant below must remain finite throughout the interval.

The derivative minimum is evaluated from the exact degree-at-most-three derivative polynomial at
the interval endpoints and all real stationary points. The numerical strictness tolerance is
`1e-10`; it is a solver guard, not a physics coefficient.

The selected carrier is the **smallest degree** passing all gates. If none passes, evaluation stops.
No candidate may be added after the result is known.

## Native tidal bridge

The relative areal history is

```text
R(phi)/R(phi_0) = exp(s(phi)).
```

On a regular monotone branch, write

```text
p = R dphi/dR = 1/s',
q = R^2 d^2phi/dR^2 = -(s'' + s'^2)/s'^3.
```

The G127 dimensionless curvature contrast is then

```text
J(phi) = R^2 Xi
       = exp(-2 phi) [2 p^2 - q + 2 p] - [1-exp(-2 phi)].
```

This formula contains no absolute radius and no angular amplitude. The local tilted contrast is
`sin(alpha)^2 J/R^2`; finite-path propagation remains a later conditional calculation.

## Source/query contract frozen for the later carry

The smallest future null-source control is preregistered now but not evaluated here:

- parent sources form an angularly unpatterned Poisson process with the registered survey
  depth/footprint selection;
- the observer query counts every regular image once, exactly in the G240 scope;
- the G239 survey reference remains the separately supplied registered random reference;
- no intrinsic connected parent-source pattern, numerical branch weight, acoustic ruler, or
  Lambda-CDM distance is admitted.

This is `CHOSE_NULL_SOURCE_CONTROL`, not UDT source physics. Critical, caustic, coherent, and
infinite-image strata remain outside the G240 theorem and must not be silently regularized.

## Independent verification

The production implementation will use NumPy/SciPy Chebyshev and Cholesky routines. An independent
implementation must use high-precision `mpmath`, a direct Chebyshev recurrence, and separately
implemented linear solves. It must not read the production result.

Both routes must reproduce:

- each candidate's coefficients, raw chi-square, degrees of freedom, and pass/fail gates;
- the selected degree or the exact no-selection landing;
- derivative minima and their locations;
- `p`, `q`, and `J` on all frozen knots and a fixed dense certification grid;
- invariance of `J` under multiplying `R` by an arbitrary positive constant.

Hostile checks must catch at least: diagonalizing the covariance, changing the degree order,
removing the anchor subtraction, accepting a nonpositive derivative, flipping the `q` sign,
inserting an angular coefficient, reading a BOSS outcome path, or inserting P1, G116/G189,
`X_max`, a Lambda-CDM distance, or protected payload.

## Preregistered landings

- `D2_SNE_ANCHOR_ADEQUATE__NATIVE_TIDAL_BRIDGE_FROZEN`
- `D3_SNE_ANCHOR_ADEQUATE__NATIVE_TIDAL_BRIDGE_FROZEN`
- `D4_SNE_ANCHOR_ADEQUATE__NATIVE_TIDAL_BRIDGE_FROZEN`
- `NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS`
- `NONINVERTIBLE_OR_NONFINITE_HISTORY__STOP_BEFORE_BOSS`
- `SCAFFOLDING_OR_OUTCOME_LEAKAGE__STOP`

## Maximum conclusion

A positive result would freeze one **observationally calibrated, bounded, conditional** relative
radial history and its metric-derived local tidal response on the SNe/BOSS overlap interval. It
would not derive a physical history from the founding postulates, prove a BOSS/BAO pattern, select
an absolute scale, derive transfer or source physics, determine `X_max`, or validate UDT.
