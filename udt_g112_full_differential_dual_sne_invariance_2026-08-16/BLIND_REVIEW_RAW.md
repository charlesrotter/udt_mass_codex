# Fresh zero-context blind review — raw return

Landing: `VERIFIED_WITH_CAVEATS`

The reviewer stayed inside G112 and its 19 manifest-listed sources. The temporary-copy package
verifier passed with byte-identical replays and all hashes matching.

## Verified evidence

- The pointwise algebra is exact on the retained positive-redshift rows. Maximum floating-point
  magnitude differences are `4.44e-15` for Pantheon+ and `1.78e-15` for DES.
- Frozen `n=1.0559332414320268` is bit-identical to G99 and no optimizer runs.
- Pantheon+ retains 1,367 rows and freshly gives `chi2=1260.848088727492`,
  `B=22.343528501617104`.
- DES retains 1,623 rows and freshly gives `chi2=1444.1864417504923`,
  `B=41.70895660296954`.
- Production uses the full 1,820-object precision matrix before marginalizing DES; the second route
  uses the Schur complement. Direct precision subblocking shifts chi-square by `6.86889202096`.
- DES retains the mandatory low-chi-square warning (`lower-tail p=0.0006144042`).
- The additive offsets are survey calibration nuisances, not metric freedom.

## Caveats

1. Pantheon's `dof=1366` belongs to the fixed-`n`, one-offset replay. G99 fitted `n` on the same
   data and therefore recorded `ndof=1365`. Pantheon+ is the calibration set, not an independent
   holdout.
2. The second route is implementation-distinct but not independent end-to-end software or
   provenance. It shares NumPy/SciPy and the inputs and reads production JSON as comparison target.
3. Some catch and semantic checks are hard-coded or string guards. They must be described as
   regression guards, not strong mutation proof.
4. DES packed precision values are stored as float32 and promoted to float64. The accurate phrase
   is “full 1,820-object precision-matrix inversion,” not “full-precision inversion.”

## Maximum justified claim

G112 verifies only that one supplied isotropic `CONDITIONAL_REPRESENTATIVE` for `D_sky`, combined
with the inherited `CONDITIONAL_OBSERVATIONAL_TRANSFER`, is algebraically identical to and
numerically non-regressive against the frozen P1 curve on these Pantheon+ and DES reductions. It
does not derive or constrain the new kernel, isotropy, flux, or a complete metric history.
