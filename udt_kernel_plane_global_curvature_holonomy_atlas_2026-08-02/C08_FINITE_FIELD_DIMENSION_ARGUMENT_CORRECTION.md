# C08 finite-field dimension argument — post-return correction

Date: 2026-08-04
Status: `OPEN_MISSING_HOMOGENEOUS_OR_FLATNESS_CERTIFICATE`

## Preserved exact observations

The preregistered prime-`32003` calculation returned an exact nine-element standard basis `H` and
full `6 x 9` transformation matrix over `Fp[z,y]`. Production and the separately implemented sparse
verifier both found:

- all nine transformation residuals identically zero;
- all 36 finite-field Buchberger reductions zero;
- all six input reductions zero;
- leading monomials
  `(13,0),(8,6),(10,4),(12,2),(7,8),(0,16),(2,14),(4,12),(6,10)`;
- finite-field quotient dimension 124; and
- all ten registered mutations caught.

The independently parsed `H` is also coefficient-for-coefficient equal to the prior rational
candidate `G` after reduction modulo 32003. These are exact finite-field and consistency results.

## Load-bearing correction

The preregistration and first independent result then used the statement

```text
dim_Q QQ[z,y]/I <= dim_Fp Fp[z,y]/I_p
```

without supplying the necessary homogeneous/flatness or good-prime certificate. That implication is
false for an arbitrary inhomogeneous integral presentation. For example,

```text
I_Z=(p*x-1) in Z[x]
```

has a one-dimensional rational quotient, while reduction modulo `p` makes the generator `-1` and
the special-fiber quotient zero. Degree loss can therefore make one special fiber artificially
smaller than the rational fiber.

The finite-field transformation proves `H subset I_p`; it does not lift `H` into `I_Q`. Equality
`H=G mod p`, even exact, is a modular consistency check rather than a rational membership proof.
The first independent JSON is preserved unchanged as false-pass evidence, but its
`PASS_IDEAL_EQUALITY_PENDING_COLD_REVIEW` status is superseded by this correction.

## What would repair the bridge

A valid upper bound can come from a graded integral model. Homogenize the six unchanged integer
generators with a new variable `t` to their individual total degrees and consider the homogeneous
ideal they generate in `Z[z,y,t]`. For every degree `D`, its degree-`D` coefficient map is a finite
integer matrix, so reduction modulo `p` cannot increase rank. If an exact finite-field
transformation/Gröbner certificate proves that this *unsaturated generated homogeneous ideal* has
eventual Hilbert function 124, then the characteristic-zero homogeneous quotient has eventual
Hilbert function at most 124. Dehomogenization gives the required rational affine upper bound.

This is stronger than the affine special-fiber result and may fail because of components at
infinity. Such a failure is informative and returns OPEN; it may not be repaired by silently
saturating, choosing another prime, or dropping the infinity component.

Alternatively, an exact rational Macaulay membership certificate for the required border relations
would close the bridge directly. Merely sampling more primes would remain probabilistic and does not
repair the proof.

## Current maximum conclusion

The prime-32003 fiber exactly reproduces the candidate basis and dimension, strongly localizing the
remaining issue to characteristic-zero lifting/flatness. Rational reverse containment and ideal
equality remain OPEN. Nothing about real roots, complete C08, physics, carrier, action, source,
bootstrap, matter, mass, or dynamics follows.
