# Complete-pair observed-pattern shape test — audit report

Date: 2026-08-12
Primary landing:

```text
COMPLETE_PAIR_SHAPE_OPERATOR_DERIVED__BOTH_FROZEN_SCALAR_CONTROLS_INCOMPATIBLE
```

Evidence maturity:

```text
VERIFIED_WITH_CAVEATS__FRESH_EXTERNAL_REVIEW_SUSTAINED
```

## Result

The complete observer-pair geometry defines the normalization-free shape operator

```text
F_pair = d_A (dz/dlambda)/L_pair
       = exp(phi_pair) d_A (dphi_pair/dlambda)/L_pair.
```

It is invariant under every orientation-preserving reparameterization of the pair history. It is
only evaluated on the regular monotone stratum. The derivation uses the complete pair outputs:
angular and mixing effects can already be present in `d_A`, `L_pair`, and `phi_pair`.

The two preregistered scalar controls give:

| control | frozen definition | chi-square / 6 | preregistered class |
|---|---|---:|---|
| C0 | exact reciprocal-L, `n=1` | 114.721148358071 | `INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY` |
| C1 | fixed SNe-P1, `n=1.0559332414320268` | 31.274892627885 | `INCOMPATIBLE_ON_SIX_BIN_SHAPE_QUERY` |

C1 improves the frozen residual by `83.446255730186` chi-square units relative to C0, without a
fit. This is not model selection over a menu and does not make C1 a complete history. Both controls
cross the preregistered `22.458` incompatibility threshold.

## Residual structure

C1 is individually mild in four bins and concentrated in two:

```text
z=0.510: chi2=0.0292
z=0.706: chi2=2.3012
z=0.934: chi2=20.3109
z=1.321: chi2=7.2650
z=1.484: chi2=0.1306
z=2.330: chi2=1.2380
```

This is an `OBSERVED` residual map. It is not authority to add a localized feature, fit a bump,
choose a branch, or retune `n`. A future complete history must predict its own `F_pair(z)` before it
is compared to these directions.

## What the negative does and does not say

The result rejects the use of either frozen scalar control as the full six-bin pattern-shape
prediction. It does not reject equation (1), because neither control supplies the complete angular,
mixing, embedding, and time-live history that equation (1) evaluates.

The result is therefore a useful boundary:

```text
scalar reciprocal law alone       -> insufficient
SNe-frozen scalar P1 improvement  -> real but insufficient
complete pair orchestra           -> still untested until a history is owned
```

No conventional feature-origin story, standard ruler, yardstick, acoustic scale, or Lambda-CDM
dynamics is imported. The public release labels and symbols remain data-packaging names only.

## Verification

- preregistration was banked first at commit `efdecd35`;
- official mean and covariance hashes match the banked data-suitability audit;
- SymPy proves the operator reparameterization and scalar reductions exactly;
- the analytic profile agrees with direct Brent minimization to `5.7e-14` in chi-square;
- an independent 70-digit standard-library Decimal replay agrees to below `1.9e-13` per bin;
- all 9 preregistered hostile mutations were caught;
- no UDT parameter, `n`, row, covariance, or history coefficient was optimized.
- a fresh sealed gpt-5.4 review independently reconstructed the operator and controls, directly
  replayed the raw six-bin likelihood, verified exact zero cross-bin covariance, and returned
  `SUSTAINED_VERIFIED_WITH_CAVEATS`.

The reviewer's sole repair was documentary. `SOURCE_OWNERSHIP_CORRECTION.md` now makes explicit that
the provisional regime-flow source is not load-bearing; the banked pair-first and G79 sources plus
this package's self-contained derivation suffice.

## Maximum justified conclusion

On a supplied regular monotone complete pair history, UDT has an exact normalization-free
transverse/radial shape operator. Neither preregistered scalar control describes all six released
shape directions. The residual atlas now supplies a bounded future test for a metric-owned complete
history; it does not supply or select that history.

## Next bounded action

The next scientific calculation is not a fit of an arbitrary correction. It is to take a
pre-existing, independently specified complete pair history and evaluate its native `d_A`,
`L_pair`, and `phi_pair` in equation (1). If no such history is currently owned, the honest landing
remains `OPEN` rather than constructing one from the residuals.
