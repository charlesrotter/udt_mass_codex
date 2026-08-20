# G185 external-review adjudication

## Returned landing

`G185_REPAIR_REQUIRED`

## Scientific adjudication

The external reviewer independently recovered the bounded G185 result from the sealed source copies without fitting a shape parameter:

- Pantheon+: `chi2 = 1260.848088727467`, offset `22.34352850161705`;
- DES-SN5YR: `chi2 = 1444.186441962819`, offset `41.70895660296941`;
- frozen calibration: `n = 1.0559332414320268`;
- deletion, duplication, and wrong-transfer controls remain catastrophically worse.

The reviewer also confirmed the load-bearing type distinction: the radial pair-plane angular Gram vanishes because the supplied radial tangent has `Z=0`, while the distinct sky Jacobi screen retains `|det D_sky|=R^2`. The imported conditional transfer is used once and reduces to `d_L=Z^2 R`.

Therefore no scientific derivation, numerical result, dataset cut, calibration, or bounded landing is reopened by this review.

## Repair boundary

The return is not acceptance because the sealed artifact was not self-replayable in the review runtime:

1. its copied `SOURCE_MANIFEST.tsv` retained repository and absolute source paths instead of paths to the immutable sealed copies;
2. its Python entrypoints required NumPy, SciPy, and SymPy, which were absent from the declared sealed runtime;
3. consequently the sealed `verify_package.py` could not pass its own integrity and replay gates.

The permitted repair is packaging-only. It may change sealed path resolution and add a dependency-free sealed replay. It may not change the model, equations, cuts, calibration, expected values, tolerances, controls, or scientific landing.

## Evidence provenance

- reviewer session: `01a01d71-a802-73b2-9de7-7be6f040944b`
- raw last-message SHA-256: `0faf5eeff76f5d43c288b027b7f40c177b5fccd1006abb955ac98cdceacf18a2`
- full transcript SHA-256: `9d801288a6c82dea02160a44c40ad2baddd899bf1ec48bde33090761617540a6`
- reviewer scratch replay SHA-256: `0ae691b8390e377fdf03c8ee2ae98f427db74d50c6cca965bf456ab0d0160add`

The raw review is preserved verbatim in `EXTERNAL_ADVERSARIAL_REVIEW_RAW.md`. The transcript is preserved separately as a deterministic gzip artifact.
