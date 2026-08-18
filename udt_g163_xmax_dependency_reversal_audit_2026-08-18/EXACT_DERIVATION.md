# G163 exact derivation — scale-free reciprocal kernel

Date: 2026-08-18

## 1. Complete pair input

The full `B,Q,S,Y,Z` coframe/query data first form one supplied calibrated pair metric. On the
regular future-clock stratum it has the unique decomposition

```text
h = -T^2 (dy0 + beta dy1)^2 + L^2 dy1^2,
T > 0, L > 0.
```

The terminal reciprocal quantities are

```text
phi = 0.5 log(L/T),
q = T/L = exp(-2 phi).
```

No positional scale has entered.

## 2. Native projective readout

Define the projective common/contrast ratio

```text
chi = (L-T)/(L+T).
```

Exact substitution gives

```text
chi = (1-q)/(1+q) = tanh(phi),
q = (1-chi)/(1+chi).
```

Because T and L are positive, the exact gap

```text
(L+T)^2 - (L-T)^2 = 4LT > 0
```

proves `-1 < chi < 1`. The endpoints are projective boundary rays, not regular finite-pair
lengths.

For multiplicative reciprocal ratios `q12=q1*q2`, direct algebra gives

```text
chi12 = (chi1+chi2)/(1+chi1*chi2).
```

Observer reversal sends `q` to `1/q` and `chi` to `-chi`. The exact first differential is

```text
dchi = (1-chi^2) dphi.
```

This is the native replacement for differentiating `Xmax*chi` inside the local kernel.

## 3. Xmax identifiability rank

Assemble only the native terminal, inverse, composition, reversal, and differential residuals.
Introduce a new symbol `X` only after that system is complete. None of its entries contains `X`,
so its exact Jacobian with respect to `X` is the zero column and has rank zero.

Therefore current native kernel equations cannot identify a dimensionful `Xmax`. This is a type
statement, not a numerical failure.

## 4. Conformal and dimensional no-go

Under a positive common rescaling

```text
T -> aT,
L -> aL,
```

the quantities `q`, `phi`, and `chi` are unchanged, while pair volume density and half-density
scale. Hence the projective kernel cannot return a length that transforms with the metric scale.

The observed anchors also do not supply a length by themselves. Assigning exponents `alpha,beta`
to `c_E^alpha G_obs^beta`, zero mass power forces `beta=0`; zero time power then forces
`alpha=0`, contradicting the required length power one.

Reciprocal algebra alone also admits every positive finite dimensional display scale once such a
scale is supplied, and it admits an unbounded marking if the working finite-asymptote semantics is
not imposed. Thus the dimensionless boundary is derived while a finite physical length is not.

## 5. Noncircular global consequence theorem

A completed realization may derive `Xmax` only after independently supplying all of the following
without using `Xmax`:

1. a physical co-present relation space;
2. a dimensionful metric-natural nonnegative separation on that space;
3. overlap and observer-recentering invariance;
4. a global completion;
5. a finite positive all-frame supremum; and
6. proof that approaching that supremum is equivalent to divergent reciprocal depth on the
   relevant completed ends.

Only then may the supremum be named `Xmax`. Defining separation as `Xmax*chi`, inserting `Xmax`
into the Mobius law, or cutting the domain off at `Xmax` before taking its supremum is circular.

## 6. Ownership boundary

- Scale-free `chi`, its open bound, composition, reversal, and differential: `DERIVED` from a
  supplied complete calibrated pair metric, with physical normalized-position semantics retained
  as Charles's `CHOSE / WORKING` clarification.
- Dimensionful `x`, proper or areal separation, finite physical supremum, all-frame equality,
  numerical value, and global completion: `OPEN`.
- Existing fixed-`Xmax` calculations: lawful conditional probes, not native-kernel derivations.
