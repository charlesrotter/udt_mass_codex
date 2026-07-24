# Clock/angular solder regularity audit

Date: 2026-07-24

Preregistration commit: `388d015`

Compute: CPU-only exact algebra and independent coordinate-curvature replay

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The founding reciprocal clock factor and the conditional reciprocal
angular/Hopf depth cannot be carried by the same scalar across two regular
primitive caps in the complete static diagonal fixed-pairing class.

This result covers every finite positive relative clock/angular depth unit
`kappa`, not only `kappa=1`.

The obstruction is geometric. It is not an equation-of-motion failure:
inserting the same scalar into the clock leg makes the four-dimensional
scalar curvature diverge at both round caps. Enforcing a complete reciprocal
clock/depth pair can regularize one cap at `kappa=1`, but the opposite cap
still diverges for every finite positive `kappa`.

## What this means for `X_max`

It does not make `X_max` optional and does not refute its emergence from the
complete metric.

It does rule out one tempting shortcut: `X_max` cannot be obtained, in this
bounded class, by treating one globally smooth spacetime scalar as both the
clock-dilation coordinate and the angular coordinate all the way across a
closed two-cap cell.

The surviving alternatives are exactly the ones appropriate to the
observer-frame definition:

- an open/asymptotic endpoint;
- patchwise depth with a cut locus;
- a time-live, shifted, or nonintegrable realization;
- distinct clock and angular depth objects; or
- a relational scalar on observer-pair/configuration space.

The last option is especially aligned with “maximum distance between two
observers”: a global diameter is a two-point property of a complete metric,
not normally a one-point scalar value.

## Directional variation

The angular sector can matter twice:

1. it determines whether a local depth actually closes into a complete
   finite-cell geometry; and
2. in a nonround completion it can make limiting pair distance depend weakly
   on direction.

The clean notation is a directional endpoint `X(p,n)` and an absolute

```text
X_max = sup d_h(p,q).
```

The present round control has no directional variance. The repository has no
complete nonround clock-soldered branch from which such a variance can yet be
calculated. A possible CMB relation remains an observational comparison, not
an input or a derived result.

## Exact family rulings

| Family | Ruling |
|---|---|
| isolated clock on round space | curvature-singular at both caps |
| fixed-pairing double reciprocal round solder | at least one singular cap for every finite positive `kappa` |
| smooth positive physical common factor | cannot cancel the cap pole while retaining the same regular completion |
| arbitrary open profile | infinite open family; endpoint and diameter not selected |
| constant-clock round control | regular, but clock and angular roles remain separate |
| shifted/time-live/patchwise/pair-space families | open outside the bounded class |

No cross-family splice is counted as a solution.

## Why the result is useful

The earlier branch audit found three disconnected pieces: clock depth,
angular reciprocal geometry, and a conditional round diameter. This audit
tests the simplest exact join and shows why it fails globally. The failure is
not “more math is missing”; it identifies the wrong ontology for that join.

The next metric-led question should therefore be two-point and angular:
derive the directional cut/endpoint and global diameter functional of each
complete observer-rest branch, without assuming roundness or using CMB data
to select an answer.

## Evidence

- preregistered before evaluation at `388d015`;
- six frozen solder families;
- all finite positive `kappa` treated analytically;
- 37 exact production checks;
- independent standard-library five-point coordinate derivatives;
- 59 independent checks and 11 exercised semantic corruptions;
- eight hash-pinned source identities;
- no action, source, carrier, mass, density, fit, or GPU work.

No fresh external-model review was authorized, so the grade is
`VERIFIED-WITH-CAVEATS`.

## Maximum conclusion

```text
NO REGULAR TWO-PRIMITIVE-CAP SAME-SCALAR CLOCK/ANGULAR SOLDER EXISTS
IN THE BOUNDED STATIC DIAGONAL FIXED-PAIRING RECIPROCAL-TORIC CLASS.

OPEN, PATCHWISE, SHIFTED, TIME-LIVE, NONINTEGRABLE, AND OBSERVER-PAIR
REALIZATIONS REMAIN OPEN. GLOBAL X_MAX REMAINS OPEN_NOT_EVALUABLE.
```
