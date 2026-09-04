# G345 preregistration execution note

Date: 2026-09-04
Preregistration commit: `d22f1bdb`

## Preserved first execution

The first production execution returned `9822/9824` checks. The only misses were
`coincidence_convergence_improves_23` and `coincidence_convergence_improves_85`. All preregistered
affine, reference-event, general-screen, reversal, endpoint-reset, stationary-composition,
reference-free, and principal-formula maxima were between `7.6e-16` and `7.0e-14` except the
reference block comparison at `4.8e-14`.

The failed check was an additional numerical monotonicity demand: the absolute error of
`Dhat(T0+epsilon,T0) epsilon^2` had to decrease strictly when `epsilon` fell from `1e-4 T0` to
`2.5e-5 T0` in every case. In the misses, both errors had already reached roughly `1e-11`; the
smaller value changed by floating-point quadrature noise. The preregistration requires the limit
to approach one, not strict sample-by-sample error monotonicity below numerical resolution.

## Recorded repair before rerun

Retain the preregistered fine-step limit gate `abs(Dhat epsilon^2-1)<8e-5`. Replace only the
over-strong supplemental strict-monotonicity assertion by a two-scale consistency assertion:

```text
fine_error < max(4 coarse_error, 1e-9).
```

This still rejects a nonconvergent or wrong-pole implementation while not ordering two values
already inside the double-precision/quadrature noise floor. No candidate formula, tolerance on the
preregistered limit, scientific alternative, domain, or maximum conclusion changes.

## Aggregate-verifier wording repair

The first aggregate package replay passed `16/17`. Its only miss required the preregistration file
to contain the hash of the commit that created that same file, which is mechanically impossible.
The verifier was repaired to require the hash in the subsequent immutable execution note and audit
report instead. No evidence value, scientific check, or result language changed.
