# Cold external review dispatch — G81 nonradial screen covariance

You are a fresh adversarial reviewer. Inspect only the sealed intake. Do not edit files, continue
the research, infer broader UDT physics, or access repository material outside the intake.

## Question

On the exact fixed G79/G80 metric and the two preregistered controls, does the submitted calculation
correctly establish the conditional screen-covariance law

```text
D_reverse_AB = Z B transpose(D_forward) transpose(A)
```

together with unrotated Jacobi reciprocity, reciprocal frequency/redshift, and area reciprocity?
Does C1 genuinely activate nonradial angular/mixing geometry rather than disguise a radial or
diagonal test?

## Required audit

1. Verify all `REVIEW_MANIFEST.tsv` hashes and the exact nine frozen source rows.
2. Reconstruct the C1 direction/screen triad and both endpoint rotations exactly.
3. Derive the transformation rule, including the placement of `A`, `B`, `Z`, and the transpose.
4. Reconstruct the metric, stationary observer, source frequency, full tangent reversal, endpoint
   surfaces, and screen transport.
5. Verify C1 has live radial, polar, and azimuthal motion and a genuinely non-diagonal Jacobi map.
6. Independently replay load-bearing values without using the production Riemann/Jacobi equation
   where practical. Audit the submitted direct-Christoffel neighboring-ray method and state its
   remaining shared inputs.
7. Check refinement, endpoint return, frequency, phi, tangent, screen, null, conserved-momentum,
   Wronskian, matrix, determinant/area, and hostile-catch gates.
8. Hunt circularity, projection/source basis confusion, a missing inverse/transpose, silent
   diagonalization, sign/frequency errors, or a falsely nonradial control.
9. Classify generic Jacobi/Wronskian covariance honestly: it may be a valid conditional metric
   theorem without being a UDT-specific selector.
10. Confirm no future signal, physical profile, endpoint, scale, `Xmax`, source, SNe/CMB observable,
    `cmb_temp`, action, matter, or bootstrap theorem follows.

## Load-bearing values

```text
C0 production rotated residual       1.0086332137876813e-14
C1 production rotated residual       3.931585029333395e-15
C1 forward offdiagonal norm          1.1801666864663825e-3
C0 independent rotated residual      1.3498538204686179e-8
C1 independent rotated residual      1.1585881402639625e-8
```

## Required landing

Return exactly one primary status:

- `VERIFIED_AS_BOUNDED_SCREEN_COVARIANCE`;
- `VERIFIED_WITH_CAVEATS`;
- `CORRECTION_REQUIRED`; or
- `INVALID`.

State all binding caveats and corrections, the strongest justified maximum conclusion, and the
smallest next calculation. Do not continue the research. Supply runnable algebra or compact code
for every load-bearing challenge.
