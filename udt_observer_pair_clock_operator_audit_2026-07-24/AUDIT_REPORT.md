# UDT observer-pair clock-operator audit

Date: 2026-07-24

Preregistration: `1527cc4`

Pre-result type correction: `7ce44aa`

Compute: exact CPU algebra and independent stdlib/Fraction replay

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's central expectation is correct:

> The two founding postulates and registered composition already derive the
> abstract ordered observer-pair operator in the reciprocal clock/ruler
> sector.

It is

```text
S(delta)=diag(exp(-delta),exp(delta)),
```

with exact composition, inverse under observer-order reversal, determinant
one, and preservation of the founding dual pairing.

In the balanced basis the very same operator is exactly

```text
[[ cosh(delta),-sinh(delta)],
 [-sinh(delta), cosh(delta)]],
```

an `O(1,1)` boost. This is not an analogy imported from SR or GR; it is a
change of basis in the founded reciprocal operator.

The earlier claim that a shortest-path transport first had to create the
clock operator was therefore too strong. The operator was already present.

## The remaining distinction

Three objects must not be conflated:

1. the founded reciprocal comparison matrix;
2. metric parallel transport of coordinate components; and
3. comparison of physical orthonormal observer frames.

In the exact static diagonal UDT metric:

```text
coordinate covector transport = S(Delta phi);
coordinate vector transport   = S(-Delta phi);
orthonormal coframe transport  = identity
```

along a static spatial curve.

Thus the metric reproduces the founding matrix exactly for the correct
covector type, but this coordinate-component result is not by itself a
measured mutual clock slowdown.

## What the clock readouts say

The named time-per-length channel remains

```text
T(rho)=exp(-rho), rho>=0.
```

It is the derived multiplicative channel character.

The reversal-even half trace of the complete pair operator is

```text
Gamma(delta)=cosh(delta).
```

Its inverse `sech(delta)` is a possible mutual observer slow factor only if
the balanced dual pairing is adopted as the physical observer readout and
the endpoint observer frames are fixed. It is not a replacement for the
named exponential channel and does not itself obey the channel composition
law.

A stationary lapse ratio,

```text
N(q)/N(p)=exp(-(phi(q)-phi(p))),
```

is yet another object: it is ordered and depends on a common static slicing.
It is not symmetric mutual slowdown.

## What is now closed

- The abstract reciprocal pair operator is not missing.
- Its finite composition and reversal laws are exact.
- Its balanced Lorentz-type representation is exact.
- The clock/ruler channel assignment is not missing.
- A spatial coordinate-covector realization exists in the exact diagonal
  metric control.

## What remains open

- the physical map from a complete observer pair to additive depth;
- whether that depth is a local-field difference, a genuinely bilocal
  quantity, or an observer-based chart family;
- endpoint observer/event pairing for a mutual clock measurement;
- a complete reciprocal subbundle through angular and shift sectors;
- path/holonomy behavior and cut-locus degeneracy;
- a global physical `X_max`;
- mass, density, asymptotic boundary-layer, or CMB interpretation.

The existing ontology ledger was right to keep

```text
delta(p,q)=phi(q)-phi(p)
```

open. The identity is exact if supplied, but a single global signed scalar
need not represent every nonnegative pair separation in a centerless closed
geometry.

## Corrected role of connecting paths

The abstract operator does not need a path. A path becomes relevant only
when the complete metric must assign depth and carry angular/shift data
between actual observers. Multiple paths near a cut locus may then yield
different full transports. That possible angular modulation remains real,
but it is downstream of the already-derived reciprocal operator.

## Evidence

- preregistered before computation;
- type correction committed before result banking;
- 11 hash-pinned controlling sources;
- 62 exact SymPy production checks;
- 74 independent stdlib/Fraction checks;
- 12 exercised fail-closed mutations;
- exact coordinate-Christoffel and independent coframe/generator routes;
- no path, physical `K` readout, local-field join, action, source, mass,
  density, `X_max`, CMB, or GPU premise inserted.

No fresh external-model semantic review was authorized.

## Maximum conclusion

```text
THE FOUNDING POSTULATES ALREADY DERIVE THE ABSTRACT ORDERED RECIPROCAL
OBSERVER-PAIR OPERATOR, AND ITS BALANCED FORM IS AN EXACT O(1,1) BOOST.

THE COMPLETE PHYSICAL MUTUAL-CLOCK LAW STILL REQUIRES A METRIC-NATIVE
PAIR-DEPTH REALIZATION, PHYSICAL ENDPOINT FRAMES/EVENT PAIRING, AND THE
ANGULAR/HOLONOMY COMPLETION. THESE ARE NOW THE OPEN JOINS; THE OPERATOR
ITSELF IS NOT.
```
