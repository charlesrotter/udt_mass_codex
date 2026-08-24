# G242 preregistration — exact quiet-subfamily SNe anchor

Date: 2026-08-24

Status: `PREREGISTERED_BEFORE_G242_EVALUATION__BOSS_OUTCOMES_CLOSED`

## Whole question and bounded regime

Does the exact G201 primary-metric family whose two local angular tidal modes vanish agree with the
byte-frozen G237 `K=12` relative SNe state on

```text
0.07077528204904217 <= phi <= 0.7627571949083936
```

under the unchanged G237 static-central query and imported-transfer caveats?

This is metric-led. It tests one exact native subfamily; it does not fit a physical profile or use
an observed BAO feature to choose a representation.

## Exact native null family

In the primary metric

```text
f(r)=exp(-2 phi(r)),
```

G201 derives simultaneous cancellation of both local angular modes for

```text
f(r)=1+C r^2.
```

On the observed positive-depth branch, `C<0` and therefore

```text
r(phi)^2 = [1-exp(-2 phi)]/(-C).
```

After anchoring at the first frozen depth, the unknown `C` and absolute ruler cancel. The exact
coefficient-free prediction for the G237 magnitude-like relative state is

```text
theta_quiet(phi)
  = (5/2) log10(
      [1-exp(-2 phi)]/[1-exp(-2 phi_0)]
    ).
```

No shape, angular, smoothing, or scale coefficient is fit.

## Frozen statistical test

Let `theta` and `C_theta` be the eleven non-anchor entries and full `11 x 11` covariance in
`FROZEN_PRIMARY_K12_STATE.json`. Compute

```text
r = theta - theta_quiet
chi2 = r^T C_theta^-1 r
dof = 11
ceiling = scipy.stats.chi2.ppf(0.999, 11).
```

Use Cholesky solves, never a covariance diagonalization. The classification is compatible only if
`chi2 <= ceiling`.

The same implementation must also verify on every frozen knot and a fixed 4097-point grid that:

1. the inferred radial history is strictly increasing;
2. the G241 inverse-derivative identity is finite;
3. the resulting dimensionless tidal contrast `J` is zero to `1e-10` absolute;
4. arbitrary positive rescaling of `r` leaves the state prediction and `J` unchanged.

## Independent verification

The production route may use NumPy/SciPy. A separate standard-library plus 80-digit `mpmath` route
must read only the frozen source files and independently recompute the predicted state, full-
covariance chi-square, ceiling, monotonicity, and zero-tide identity. It must not import production
code or read production output.

Hostile checks must catch at least: covariance diagonalization, a sign flip in `1-exp(-2 phi)`,
fitting `C`, inserting an angular coefficient, loosening the frozen threshold after the result,
opening a BOSS outcome, or importing P1, G116/G189, `X_max`, a Lambda-CDM distance, or protected
payload.

## Preregistered landings

- `EXACT_QUIET_SUBFAMILY_COMPATIBLE_WITH_FROZEN_SNE_STATE`
- `EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN`
- `IMPLEMENTATION_OR_COVARIANCE_FAILURE__NO_SCIENTIFIC_LANDING`
- `SCAFFOLDING_OR_OUTCOME_LEAKAGE__STOP`

## Scope and maximum conclusion

A compatible result would retain one exact metric-native zero-tide subfamily as an observationally
allowed SNe control. It would not select that history or predict BAO.

An incompatible result would reject only exact zero angular tide across this bounded conditional
SNe query. It would not reject a very quiet but nonzero response, later BAO onset, the native
radial-to-tidal identity, the reciprocal kernel, or UDT. No outcome authorizes adding a fitted
coefficient or opening BOSS before a new preregistered contract.
