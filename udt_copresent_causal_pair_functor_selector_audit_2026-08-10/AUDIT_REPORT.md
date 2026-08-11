# Audit report — co-present causal pair-functor selector

Date: 2026-08-10
Preregistration commit: `86380447`
External verdict: `VERIFIED_WITH_CORRECTIONS`
Final grade: `VERIFIED-WITH-CAVEATS`

## Result

On every supplied regular calibrated pair metric

```text
h=-T^2(dy^0+beta dy^1)^2+L^2(dy^1)^2,
```

the complete shifted cone gives exactly

```text
r_±=-beta±L/T,
center=-beta,
centered half-width=L/T=exp(2phi_pair),
c_eff^(pair)/c_E=T/L=exp(-2phi_pair).
```

This is the exact causal meaning of the conditional terminal reciprocal readout. `beta` is retained
as cone tilt; it is not set to zero. Time, angular, screen, shift, and mixing dependence enters the
induced pair metric and its differential before the readout.

For the declared smooth local time-oriented **bidirectional causal-isomorphism** class, null
coordinates give exactly

```text
u'=f(u), v'=g(v), f'>0, g'>0,
```

plus the null-branch-exchange component. Composition, inversion, one-point `c_E` calibration, and
both reciprocal asymptotes leave infinite local transition/calibration freedom.

## Adversarial correction

Those local witnesses may include gauge-equivalent descriptions of one supplied pair surface.
They do **not** prove that several ambiently distinct physical pair immersions exist, and therefore
do not prove that current UDT premises fail to select a unique physical ambient family. That
construction/selection question remains `OPEN`.

Co-presence remains whole-solution co-membership semantics. It contributes no additional local
selector in this audit and does not imply material signalling. Pullback causal preservation is
automatic after an immersion is supplied; ambient-order reflection and global causal faithfulness
are stronger open conditions.

## Verification

- exact symbolic identities: `33/33`;
- sampled independent standard-library smoke checks: `58/58`;
- numeric/semantic scope guards: `22/22`;
- exact source replay: 14/14 in both repository and sealed `sources/` layouts;
- cold gpt-5.4 review: `VERIFIED_WITH_CORRECTIONS`, all four corrections accepted.

The external reviewer independently accepted the universal cone theorem and local causal-
isomorphism classification. It did not rerun write-producing scripts inside the read-only intake.

## Four banking gates

1. **Preregistered:** yes, commit `86380447` before result generation.
2. **Full or bounded scope justified:** yes, complete declared local smooth regular 1+1
   bidirectional causal-isomorphism class on a supplied calibrated pair family; singular, one-way,
   global, and ambient-family construction scopes remain explicit.
3. **Independently verified on the load-bearing premise:** yes with caveat—cold semantic review
   independently rederived the theorem; the Fraction program is only a sampled smoke test.
4. **Every premise audited:** yes within the exact 14-source intake; the review transport initially
   could not replay repository-relative hashes, and the repaired sealed-layout verifier now closes
   that mechanical gap.

## Maximum conclusion

`PAIR_CONE_JOIN_VERIFIED__LOCAL_CAUSAL_TRANSITION_AND_CALIBRATION_NONSELECTION_ON_A_SUPPLIED_FAMILY__AMBIENT_PHYSICAL_PAIR_FAMILY_SELECTOR_OPEN`

No action, source, matter, mass, bootstrap fixed point, material signal law, numerical `X_max`, CMB
spectrum, or physical regime assignment is derived.
