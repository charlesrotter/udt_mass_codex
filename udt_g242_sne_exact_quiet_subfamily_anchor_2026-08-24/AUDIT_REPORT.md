# G242 audit — exact quiet-subfamily SNe anchor

Date: 2026-08-24

Status: `EXTERNALLY_VERIFIED_WITH_CAVEATS`

## Landing

```text
EXACT_QUIET_SUBFAMILY_INCOMPATIBLE
__SMALL_NONZERO_RESPONSE_REMAINS_OPEN
__BOSS_OUTCOMES_CLOSED
```

## What was learned

The primary metric's exact coefficient-free family with both local angular tidal modes identically
zero does not reproduce the frozen G237 SNe radial state. The full-covariance mismatch is
`chi2=8519.009211032242` for eleven state coordinates, versus the preregistered 0.999 ceiling
`31.264133620239985`.

The negative is not caused by a turning point or a numerical failure. The tested quiet family is
strictly monotone on the full interval; its G241 tidal invariant vanishes to `3.3e-15` in the
production replay and to `3.4e-80` in the independent replay.

This is a secondary compatibility statement about one radial subfamily. In the active SNe query,
redshift itself remains the direct reciprocal endpoint readout `1+z=exp(phi_s-phi_o)` and does not
require an angular response.

## What was not learned

The test used exact silence as a metric-native radial null control. It did not test the origin of
SNe redshift, define angular loudness, or determine how small a nonzero response may be. Therefore
it does not contradict the working expectation that angular effects remain weak through SNe and
only begin to become noticeable in the BAO regime.

It does not reject the radial-to-tidal identity, the reciprocal kernel, or UDT. It does not select
a continuous history, derive transfer, open BOSS outcomes, determine `X_max`, or authorize a fitted
angular coefficient.

## Evidence gates

- preregistered and pushed at `b04e18c7` before evaluation;
- full G237 `11 x 11` covariance retained;
- no fitted coefficient or absolute scale;
- production NumPy/SciPy and independent 80-digit direct Cholesky routes agree;
- the exact `J=0` and `C` cancellation identities replay independently;
- eight hostile checks pass;
- no BOSS outcome or protected package path is opened.

Fresh external Codex `gpt-5.4` review returned
`G242_BOUNDED_NEGATIVE_ACCEPTED__SMALL_NONZERO_RESPONSE_OPEN` with no requested repairs. The
reviewer reproduced the full-covariance statistic independently, verified all scoped hashes and
registered replays, and accepted both the interpretation correction and the append-only registry
lineage repair. Repository ancestry independently closes its source-only provenance caveat.

## Next scientific question

G243 has already performed the next covariance-aware, explicitly observational radial
representation census while keeping reciprocal redshift separate; its certification gate returned
`NO_FREEZE` but retained one strongly reproduced local turning candidate. The next scientific
question is therefore a separately typed, outcome-blind angular-query construction on the metric's
native screen/Jacobi operators. Exact silence is rejected as a universal SNe-interval replacement,
but no fitted small-response coefficient is authorized. BOSS outcomes remain closed until that
query and its physical inputs are preregistered.
