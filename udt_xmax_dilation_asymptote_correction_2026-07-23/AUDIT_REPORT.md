# Xmax dilation-asymptote correction

Date: 2026-07-23

Preregistration commit:
`94c6ee3eae92cc67a8e3f370c98e93d75da4d4f8`

Frozen parent:
`udt_invariant_xmax_asymptotic_boundary_audit_2026-07-23`

Parent manifest SHA-256:
`8798461fbd59891c1eff90c36311e38a29a3753dd4066d75360a813a859955c0`

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's correction is adopted as the controlling working meaning:

> `Xmax` is the invariant positional scale at which UDT time dilation becomes
> asymptotic, analogous in limiting role—but not units—to Einsteinian `c`.

The parent audit's question “which distance readout defines `Xmax`?” was
therefore backwards. Coordinate reach, proper length, optical depth, and a
projective display are different ways of describing a metric near its
limit. None owns the definition of `Xmax`.

There is also a stronger existing result than the parent audit credited.
The post-July WR-L chain derives, on its recorded static reciprocal branch,

```text
A = exp(-2 phi) = 1-r/X,
r/X = 1-exp(-2 phi),
phi = -log(1-r/X)/2.
```

As `r` approaches `X`, `phi` diverges, `A` tends to zero, and the static
clock factor `exp(-phi)` tends to zero. This is exactly a metric realization
of the owner-defined dilation asymptote.

The status is precise:

```text
DERIVED_CONDITIONAL_WRL
```

It is a direct geometric derivation from the reciprocal metric, residual
composition/re-centering, and the Charles-accepted WR-L wall package. It is
not a derivation from the bare line element alone, and not the supernova
fit.

## The SNe connection

The full-covariance Pantheon comparison independently observed:

| supplied profile | chi-squared/dof | RMS mag | status |
|---|---:|---:|---|
| WR-L linear ceiling | 0.909857 | 0.158164 | near the data |
| hyperbolic `tanh` plus J1 | 2.166502 | 0.307403 | shape failure |

For WR-L, the metric redshift and the `n=2` comparison/readout give

```text
1+z = exp(phi),
r/X = 1-(1+z)^-2,
dL = (1+z)^2 r,
dL/X = z(z+2).
```

Thus the profile selected by WR-L is the same profile that the SNe work
called the “linear ceiling.” The logical direction is:

```text
metric + WR-L geometry -> profile -> SNe comparison
```

not:

```text
SNe fit -> profile -> UDT theory.
```

The SNe result is therefore genuine independent observational support for
the scoped profile, but it is not a premise in the derivation and does not
select the absolute value of `Xmax`.

## What happened to the hyperbolic law

The earlier

```text
r/X = tanh(phi)
```

chain requires a first-degree fractional-linear positional readout and a
join identifying that readout with physical position. The script
`derive_xmax_boost.py` hardcodes the fractional-linear composition law and
then verifies its algebra; it does not prove that invariant endpoints alone
force that law.

The exact projective theorem remains valid:

```text
tanh(phi) is the unique anchored first-degree projective readout.
```

Its physical-position status remains conditional. At `phi=log(2)`, the
distinction is visible:

```text
WR-L coordinate fraction = 3/4,
WR-L proper fraction      = 1/2,
projective tanh display   = 3/5.
```

All reach the same asymptotic end. They are not the same interior marking.
The strongest existing metric-selected profile is WR-L, not `tanh`.

The historical `sne_test_derived_law.py` also does not derive WR-L. It
hardcodes `phi=-log(1-kr)`, which gives a squared lapse, and uses the later
corrected `n=1` luminosity readout. Its filename is not authority.

## Exact WR-L premise audit

Residual composition and affine areal re-centering first give

```text
A=(1-r/X)^alpha.
```

Near the asymptote:

- infinite optical depth requires `alpha>=1`;
- finite proper reach requires `alpha<2`;
- finite wall angular-curvature/second-derivative behavior leaves
  `alpha=1` inside that band.

That is why the angular sector already contributed to the positional law.
It selected the exponent. It did not select the remaining angular
normalization, topology, twist, section, or full time-live completion.

The scope appendices in `CANON.md` remain binding: WR-L is a wall/exterior
profile; exact extension to the seat has a center singularity/fork, and the
wall is a regular null horizon rather than a hard terminal edge. The
complete global universe still has to select this branch before its `X` can
be identified physically with the universe's realized `Xmax`.

## Correction to the parent questions

1. **Position–dilation profile:** no longer generically open. The strongest
   recorded answer is `r/X=1-exp(-2phi)`,
   `DERIVED_CONDITIONAL_WRL`. The projective `tanh` display remains
   conditional and is not the selected WR-L profile.
2. **Observer preservation:** not a request to invent another position law.
   Common `Xmax` is part of the owner frame postulate. The remaining task is
   only to verify that any complete moving/accelerating frame realization
   preserves the same limiting surface and law.
3. **Angular regularity:** partly paid. Its finite-wall condition helped
   select the WR-L exponent. It does not complete the angular geometry or
   force `lambda=1`.
4. **Numerical `Xmax`:** still open. Known `c_E` and `G_obs` calibrate units,
   but a native total mass and a scale-breaking global bootstrap equation
   are still required to select a number.

## Native mass precision

The metric directly derives the clock/lapse asymptote. It does not yet
derive a native mass increase because the complete UDT matter functional
and normalized mass/charge are open. Historical

```text
M = c_E^2 X/(2G_obs)
```

is a GR/Misner-Sharp comparison readout, not independent UDT mass closure.
The owner expectation of asymptotic mass increase remains `WORKING_OPEN`.

## Four evidence gates

1. **Preregistered:** yes, commit `94c6ee3` before the correction audit.
2. **Full or bounded space:** bounded and explicit—the post-July
   static/spherical SNe–WR-L lineage, not all complete metric solutions.
3. **Independent verification:** exact algebra and source hashes were
   recomputed in a separate standard-library implementation; no fresh
   semantic agent was launched, so the grade remains
   `VERIFIED-WITH-CAVEATS`.
4. **Premises audited:** yes for the bounded chain. Static spherical/areal
   slice, residual re-centering, wall regularity, comparison optics, global
   selection, mass, angular completion, and bootstrap are all explicit.

## Maximum conclusion

> `Xmax` is owner-defined as UDT's invariant positional dilation asymptote.
> The recorded WR-L branch conditionally derives
> `r/X=1-exp(-2phi)` from metric/geometric premises, and the Pantheon
> comparison independently favors the resulting linear-ceiling shape over
> the conditional hyperbolic-J1 display. Selection of the complete global
> branch, the numerical value of `Xmax`, and native mass dilation remain
> open.

No canonization, action, source, carrier, numerical refit, GPU work, or
navigation update is made here.
