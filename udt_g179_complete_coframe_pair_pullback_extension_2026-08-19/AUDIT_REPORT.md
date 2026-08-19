# G179 audit report — complete-coframe completed-pair extension

Date: 2026-08-19

## Primary result

G179 reaches the preregistered landing:

```text
GENERAL_COMPLETE_COFRAME_PULLBACK_EXTENDS_COMPLETED_PAIR_KERNEL_WITHOUT_EXTRA_SCALAR
```

For any supplied invertible Lorentz coframe (E) and supplied rank-two germ (J), form the entire
pair metric first:

\[
h=J^TE^T\eta_4EJ.
\]

On (h_{00}<0), (det h<0), the adopted completed-pair application of Dual Reciprocity uniquely
gives

\[
m=\sqrt{-\det h},
\qquad
\Phi=-\frac12\log(-h_{00}),
\qquad
\det h_s=-1.
\]

No additional scalar, coefficient, path, score, or regime function occurs.

## What was actually extended

The result is no longer tied to the static-spherical chart. It survives:

- arbitrary invertible coframe presentation;
- a non-block coframe obtained by a general ambient basis change;
- nonspherical screen (Q);
- all four complete mixing components (S);
- nonzero pair-screen tangent (Z);
- nonzero terminal shift;
- a regular pair with singular base projection (Y);
- exact query-live variation of (E) and (J).

Every orchestra channel enters through (h) before reciprocity fixes the physical ruler. A generic
exact witness gives nonzero (d\Phi) and (d(m^2)) from each of (B,Q,S,Y,Z).

## Evidence

- preregistration commit: `c8070adb`;
- ten frozen source hashes: exact;
- symbolic direct-versus-block residuals: exactly zero;
- exact full-sector witness: (h=[[-118,102],[102,822]]), (det h=-107400);
- regular singular-(Y) witness: (det h=-45324);
- independent standard-library exact-rational replay: 20,000/20,000 pass;
- semantic/algebraic mutations: 30/30 caught;
- Lorentz gauge, ambient coordinate, ruler reparameterization, orientation, and live product-rule
  controls: pass.

## Scientific grade

`DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS_PENDING_FRESH_ADVERSARIAL_REVIEW`

This is a general local scalar-kernel theorem on supplied regular completed pair germs, conditional
on the `WORKING_FOUNDATIONAL_CLARIFICATION`. It is not canon and does not select observer events or
germs, determine a global history, close singular strata, or derive non-scalar transport,
`X_max`, observations, radiative transfer, dynamics, source, matter, or signalling.
