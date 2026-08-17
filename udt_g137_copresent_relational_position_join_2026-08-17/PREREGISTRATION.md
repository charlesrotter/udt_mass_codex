# G137 preregistration — co-present relational position join

Date: 2026-08-17

## Owner decision being carried

Charles approved the following as a working foundational clarification:

> Physical normalized position for a regular co-present observer pair is a continuous strictly
> increasing coordinate of the completed reciprocal relation, carries that relation's native
> Mobius composition law, and uses the local unit convention `F'(0)=1`.

This is `CHOSE / WORKING_FOUNDATIONAL_CLARIFICATION`. It is not a claim that G136 derived the
physical interpretation, and it is not a `CANON.md` canonization.

## Whole bounded question

Given that clarification and a supplied regular calibrated complete pair metric, derive and
type-check:

1. signed normalized observer position and dimensional signed position;
2. nonnegative pair separation and its symmetry under observer reversal;
3. the exact join to `phi_pair`, `T/L`, conditional pair `c_eff/c_E`, and `X_max`;
4. coincidence, boundedness, asymptotic behavior, inverse maps, and composition;
5. which operations do not descend after orientation is discarded.

## Frame and ownership

- Method: metric-led downstream constitution, not template-led fitting.
- Arena: regular calibrated complete pair metrics with `T>0`, `L>0` and matched calibration for
  composition.
- `DERIVED`: terminal `phi_pair`, `q=T/L=exp(-2 phi_pair)`, G136 same-law classification.
- `CHOSE`: the physical-position clarification and unit slope.
- `WORKING_FOUNDATIONAL_FRAME`: positive dimensional `X_max` as the frame-shared observer-pair
  positional-dilation asymptote.
- `CONDITIONAL`: `q=c_eff^(pair)/c_E` as an inter-observer frame readout.
- `OPEN`: numerical or dimensional owner of `X_max`, its profile and global realization, proper
  length, areal radius, signal distance, singular/null strata, pair realization, and history.

No angular, screen, or mixing channel is added after the readout: those data must already have
entered the complete pair pullback that owns `T` and `L`.

## Preregistered candidate equations

Let `phi=phi_pair` and `q=T/L`. Test exactly:

```text
xi_AB = tanh(phi) = (L-T)/(L+T) = (1-q)/(1+q)
x_AB = X_max xi_AB
sigma_AB = |xi_AB|
s_AB = X_max sigma_AB
phi = atanh(xi_AB)
q = (1-xi_AB)/(1+xi_AB)
```

On the conditional pair-`c_eff` branch:

```text
xi_AB = (c_E-c_eff^(pair))/(c_E+c_eff^(pair)).
```

For matched composable oriented pairs:

```text
xi_AC = (xi_AB+xi_BC)/(1+xi_AB xi_BC),
x_AC = (x_AB+x_BC)/(1+x_AB x_BC/X_max^2).
```

## Certification and falsification contract

The production check must verify symbolically:

- all displayed joins and inverse maps;
- `xi_BA=-xi_AB`, `x_BA=-x_AB`, `sigma_BA=sigma_AB`, and `s_BA=s_AB`;
- coincidence at `phi=0`;
- `|xi|<1` and `0<=sigma<1` for finite real depth;
- approach to `+/- X_max` only as `phi` approaches `+/- infinity`;
- exact signed Mobius composition on matched depths;
- failure of a universal composition law on `sigma` alone, witnessed by two oriented input pairs
  with the same magnitudes but different signs and different output magnitudes.

An independent implementation must recompute finite witnesses without importing the production
implementation. Source hashes must be checked in their frozen through-G136 scope.

## Maximum conclusion

At most:

```text
OWNER_ADOPTED_WORKING_POSITION_CONSTITUTION__
SIGNED_AND_NONNEGATIVE_XMAX_JOIN_DERIVED_ON_SUPPLIED_REGULAR_COMPLETE_PAIRS__
ORIENTATION_REQUIRED_FOR_COMPOSITION__
XMAX_VALUE_PROPER_LENGTH_PAIR_REALIZATION_HISTORY_AND_GLOBAL_COMPLETION_OPEN
```

No observational fit, action, source law, signalling law, proper-distance theorem, universe size,
or numerical `X_max` may be inferred.
