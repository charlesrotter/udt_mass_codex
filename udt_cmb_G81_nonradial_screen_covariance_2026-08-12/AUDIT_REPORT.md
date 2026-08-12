# G81 audit report — nonradial and endpoint-screen covariance

## Landing

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

Both preregistered controls reached the fixed `x=1` endpoint regularly and passed every production
and independent gate. C1 was genuinely nonradial: its endpoint changed in both angular coordinates,
its forward Jacobi map had off-diagonal norm `1.1801666864663825e-3`, and no diagonalization was used.

The finest production residuals for

```text
D_reverse_AB = Z B transpose(D_forward) transpose(A)
```

were `1.0086332137876813e-14` for C0 and `3.931585029333395e-15` for C1. The independent
direct-Christoffel neighboring-ray residuals were `1.3498538204686179e-8` and
`1.1585881402639625e-8`, inside the preregistered `2e-4` gate. Endpoint return, frequency
reciprocity, full tangent reversal, screen carry, area reciprocity, nullness, conserved momenta,
screen orthonormality, and Wronskian controls all passed.

## Interpretation

The G80 reverse relation survives both a live angular ray and independent source/receiver screen
basis changes. This is the expected covariance of generic Jacobi/Wronskian reciprocity on the
supplied complete metric segment. It is stronger than a radial-coordinate check and weaker than a
physical-selection theorem.

The independent replay is materially different at the load-bearing differential-equation layer: it
rebuilds the Christoffels and estimates the maps from finite differences of neighboring geodesics.
It still shares the same supplied metric, observer query, endpoint, and SciPy integrator family, so
its independence is bounded rather than absolute.

## Four gates before external review

1. **Preregistered:** yes, exact two-control universe committed at `b8b2eef1` before outcomes.
2. **Full space or bounded scope:** bounded scope justified; exactly one radial and one nonradial
   direction, one metric profile, one endpoint, and fixed rotations.
3. **Independently verified:** yes, by direct Christoffels plus centered neighboring rays.
4. **Every premise audited:** yes in `PREMISE_LEDGER.tsv`; physical selection remains open.

Fresh external adversarial review remains the final evidence gate before this result may be banked
as verified rather than an internally verified conditional result.

## Authority boundary

G81 does not select the stationary profile, endpoint, angular direction, screen, source, scale,
`Xmax`, action, matter, bootstrap closure, CMB spectrum, `cmb_temp`, or any future signalling law.
