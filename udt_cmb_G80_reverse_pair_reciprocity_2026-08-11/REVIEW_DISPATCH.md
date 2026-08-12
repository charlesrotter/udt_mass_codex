# Cold external review dispatch — G80 reverse ordered-pair reciprocity

You are a fresh adversarial reviewer. Inspect only the sealed intake. Do not edit files, continue
the research, infer broader UDT physics, or access any repository material outside the intake.

## Question

On one frozen stationary complete-metric control and one ordered endpoint pair, does the submitted
calculation correctly prove the conditional identities

```text
Z_reverse = 1/Z_forward,
phi_reverse = -phi_forward,
D_reverse = Z_forward transpose(D_forward),
d_A_reverse = Z_forward d_A_forward?
```

The branch called “reverse” must be typed exactly: it is the past-directed affine reversal of the
same spacetime curve, with the full tangent negated and divided by the former source frequency. It
is not a future-directed signal.

## Required audit

1. Verify every `REVIEW_MANIFEST.tsv` hash and the exact 10-row source subset.
2. Reconstruct the metric, profile, endpoint observers, frequency convention, forward normalization,
   and reverse initial state from scratch.
3. Prove or refute the factor and transpose in the Jacobi relation. Explicitly distinguish:
   - unscaled affine reversal;
   - source-unit-frequency renormalization;
   - screen-basis transport and possible orientation reflections;
   - determinant/area scaling.
4. Check whether the production result is merely imposed by its initial conditions or is a genuine
   consequence of the self-adjoint Jacobi/Wronskian structure.
5. Independently replay the load-bearing values by a method that does not use the submitted
   production Riemann/Jacobi implementation where practical.
6. Audit the direct-Christoffel neighboring-ray check. State precisely what is independent and what
   metric/query/endpoint/screen/integrator inputs are shared.
7. Test all endpoint, null, Killing-energy, screen, refinement, redshift, transpose, and area gates.
8. Determine whether the result is a generic conditional theorem of metric null congruences rather
   than a UDT-specific physical selector. Do not treat genericity as invalidation, but prevent an
   originality or selection overclaim.
9. Confirm that no future signalling law, luminosity distance, physical profile, `R`, `X_max`, SNe
   fit, `cmb_temp`, CMB field/spectrum, source, action, matter law, or bootstrap rule follows.
10. Hunt for circularity, a sign error, a frequency-normalization error, an unreported screen gauge,
    a hidden zero-mixing simplification, or a mismatch between the stored path and the recomputation.

## Load-bearing controls

```text
profile                         G75_AM_S01_E05
A(x)                            1-x^2/4
h(x)                            x^6/20
Z_forward                       sqrt(21)/4
D reciprocity residual          6.885259158085081e-15
area-ratio residual             6.661338147750939e-15
independent reciprocity residual 1.4204869936356233e-08
```

## Required landing

Return exactly one primary status:

- `VERIFIED_AS_BOUNDED_GEOMETRIC_RECIPROCITY`;
- `VERIFIED_WITH_CAVEATS`;
- `CORRECTION_REQUIRED`; or
- `INVALID`.

State every binding caveat and correction. Give the strongest justified maximum conclusion and the
smallest next calculation, but do not continue the research. Supply runnable algebra or compact
code for every load-bearing challenge.
