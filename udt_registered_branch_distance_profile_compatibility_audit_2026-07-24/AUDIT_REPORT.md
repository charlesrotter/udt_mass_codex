# Registered-branch distance-profile compatibility audit

Date: 2026-07-24

Grade: `VERIFIED-WITH-CAVEATS`

Compute: CPU-only exact algebra and fixed-registry replay

## Result first

The existing UDT evidence contains three exactly distinct bounded profile
structures:

1. projective reciprocal display: `tanh(phi)`;
2. WR-L local clock-depth proper distance: `1-exp(-phi)`; and
3. conditional round `B19` angular depth:
   `(2/pi)atan[sinh(2phi)]`.

The third profile is the new structural observation from this overlay. At
unit relative depth it approaches its cap with the same
`exp(-2phi)` rate as `tanh`, but it is not `tanh`. An origin-shape invariant
distinguishes them for every finite positive constant rescaling of `phi`.

Therefore neither “it is exponential near the limit” nor the endpoint
exponent selects the physical law.

## Exact discriminator

For endpoint-normalized `P(phi)`, the rescaling-invariant origin data are

| profile | `P''/P'^2` | `P'''/P'^3` |
|---|---:|---:|
| projective `tanh` | `0` | `-2` |
| WR-L exponential | `-1` | `1` |
| round `B19`, all positive `kappa` | `0` | `-pi^2/4` |

All three are pairwise distinct. This conclusion does not depend on their
positive length scales or on a constant clock/angular depth-unit choice.

## Registry accounting

The already verified source universe was replayed, not re-adjudicated:

- 12/12 finite-cell rows accounted for;
- 28/28 equation/evidence families accounted for;
- 3/3 calculated transnormal controls accounted for;
- zero complete clock/angular/event-pair/global-diameter witnesses.

The reciprocal-toric `FC12` control can reproduce any of the profiles by
choosing its free function `A(phi)`. Since no registered equation selects
`A`, that is `CHOICE_COMPATIBILITY_NOT_SELECTION`.

## Honest profile rulings

- projective `tanh`:
  `AVAILABLE_PROJECTIVE_PHYSICAL_SOLDER_OPEN`;
- WR-L simple exponential:
  `DERIVED_CONDITIONAL_LOCAL_CLOCK_DEPTH`;
- round `B19`:
  `DERIVED_CONDITIONAL_THIRD_BOUNDED_PROFILE`, with angular rather than
  clock `phi`;
- pairwise exact identity:
  `REFUTED` under positive constant scale/depth-unit changes;
- a shared endpoint exponent as selector: `REFUTED`;
- first-order Taylor data as selector: `REFUTED`;
- free `FC12` profile as selector: `REFUTED_CHOICE_NOT_DERIVATION`;
- registered complete physical distance selector: `ZERO`;
- global physical `X_max`: `OPEN_NOT_EVALUABLE`.

## Meaning

The reciprocal exponential is unquestionably present, but the metric can
turn it into more than one bounded geometric profile depending on which
metric sector carries `phi`. Clock depth, projective display, and angular
depth are mathematically related but not interchangeable.

That clarifies the missing join. UDT does not need another guessed distance
formula. It needs a coherent complete metric realization telling us which
`phi` role belongs to observer-pair clock dilation and how that role joins
the global angular geometry.

## Evidence

- preregistered at `f17dd4a`;
- 69 exact production checks;
- 72 independent stdlib/Fraction/series checks;
- 14 exercised semantic catch-proofs;
- 14 hash-pinned source identities;
- complete replay of the 12-row, 28-family, and three-control registries.

The independent implementation does not import SymPy or the production
script. No fresh external-model verifier was authorized, so the grade
remains `VERIFIED-WITH-CAVEATS`.

## Maximum conclusion

```text
THREE DISTINCT BOUNDED PROFILE STRUCTURES ARE PRESENT.
NO REGISTERED COMPLETE BRANCH SELECTS ONE AS THE PHYSICAL
OBSERVER-DISTANCE LAW OR MAKES GLOBAL X_MAX EVALUABLE.
```

No action, source, carrier, density, boundary, physics verdict, GPU task, or
repository organization is changed.
