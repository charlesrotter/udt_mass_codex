# G126 correction record

Date: 2026-08-16

No scientific landing, candidate set, or observational outcome was changed after review.

## Registered repairs

1. Replaced the production screen surrogate with the exact rational rotation
   `[[3/5,-4/5],[4/5,3/5]]`; the script now tests `O^T O=I`, exact area `R^2`, scaled inner
   products, the isotropic generator, expansion, and zero shear.
2. Replaced the uniform reference witness with the normalized nonuniform footprint
   `(1,2,3,4)/10`; both implementations verify that any positive radial multiplier cancels after
   normalization against that registered footprint.
3. Replaced the relative-only affine witness by
   `u_1=Z^(2/n+1)/(2X)` and `u_2=[1+alpha(Z-1)]u_1`. Both satisfy
   `u_i(1)=1/(2X)` and `K_i(1)=1`; away from the vertex they retain identical `R(Z)` and distinct
   `K`. The independent rational witness now gives `K_1=1`, `K_2=6/5` at `Z=3/2`.
4. Added the frozen R2 preregistration to `SOURCE_MANIFEST.tsv`. It explicitly owns the
   Landy--Szalay estimator, official-random construction, observer-angle bins, and observed-redshift
   windows inherited by R5.
5. Corrected the evidence and status files to record completed production, independent, package,
   and initial blind-review stages.

## Reverification

- production: 15/15 exact symbolic checks pass;
- independent: 12/12 standard-library Fraction checks pass;
- source manifest: 10/10 hashes pass;
- isolated replays: both exit zero and reproduce saved JSON byte for byte.

Fresh blind follow-up is required before final banking.
