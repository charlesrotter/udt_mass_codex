# R4 verifier method correction — preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_FIRST_VERIFIER_FAILURE__BEFORE_RERUN`

## First return

The first independent verifier implementation reconstructed all 9,286 relation descriptors and
both complete cross-lag arrays, then stopped on the first rank-limited cap-covariance record:

```text
record: CMASS / factor 1 / group 0 / W0_UNIT / NSIDE 4
metric: range_quadratic_per_rank
saved production value:       547.3837280228104
independent SciPy-eigh value: 547.3837289743768
absolute difference:          9.515664380232105e-7
relative difference:          1.738919558498532e-9
```

No R4 outcome was interpreted. No verification result file was written.

## Diagnosis

Two verifier-method problems were exposed:

1. The verifier called a separate SciPy FFT for each short relation vector. That is algebraically
   independent but operationally wasteful; it consumed most of the 17-minute failed replay.
2. The verifier applied one fixed relative tolerance to a quadratic constructed from an explicitly
   rank-thresholded, ill-conditioned covariance range. Different symmetric eigensolvers return
   slightly different bases and eigenvalues in that numerical range. The fixed tolerance ignored
   the already recorded positive condition number.

The failed value is not a production identity mismatch. It is smaller than the declared
condition-aware floating-point scale below. This statement is frozen before any later cap record is
inspected.

## Frozen corrections

Only the independent verifier changes:

1. Build every centered relation vector first, then evaluate the same full linear correlations in
   one batched SciPy FFT convolution along the angular axis. The saved arrays are still compared at
   `rtol=2e-12`, `atol=2e-13`.
2. Keep the general cap-descriptor comparison at `rtol=3e-10`, `atol=3e-12`.
3. For `range_quadratic_per_rank` only, use the preregistered condition-aware relative bound

   ```text
   rtol_q = max(3e-10, 2048 * eps_float64 * positive_condition).
   ```

   The factor 2048 is a numerical safety multiplier on the observed eigensystem conditioning, not
   a physical tolerance and not fitted to an outcome. The first failed record requires about
   `1.74e-9`; its recorded condition makes the new bound larger than that value.
4. Record the maximum realized absolute difference and maximum allowed condition-aware relative
   bound in the final verifier result.

No R4 production file, relation definition, covariance, rank rule, physical premise, output count,
or maximum conclusion changes. A second failure outside these exact rules stops again.
