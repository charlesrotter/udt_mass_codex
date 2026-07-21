# Preregistered Real-Spectral-Projector Correction

Date: 2026-07-21

Status: frozen before changing the classifier or rerunning the atlas.

## Trigger

The first fresh adversarial review returned `FAIL`. It identified a real Lorentzian linear-algebra
omission: a real metric-self-adjoint endomorphism may have a complex-conjugate eigenvalue pair whose
combined real primary subspace has rank two. The current central-block routine rejects every complex
eigenvalue before constructing that real projector, then labels the row
`COMPLEX_JORDAN_OR_NUMERIC_OBSTRUCTION` while leaving its numeric status classified.

The review supplied a concrete counterexample in `R00_1_M1_B0_P0/F01_RICCI`. Its conjugate primary
plane and complement have rank two, with projector residuals between `7.6e-18` and `7.2e-15`.
Consequently the existing all-family zero-unique-split claim is invalid and must not be banked.

## Frozen failed layer

The review and raw transcript are retained as `FRESH_ADVERSARIAL_REVIEW.md` and
`FRESH_ADVERSARIAL_REVIEW_TRANSCRIPT.txt`. The immediately preceding result, transcript, family
census, and verification result are retained under `PRE_REAL_SPECTRAL_CORRECTION_*` names.

Load-bearing hashes before correction:

| object | SHA-256 |
|---|---|
| `ATLAS_RESULT.json` | `2d87656d1cb62e51e35ee5203d11189ce44773a7b31fa7114c97b036378c7cbc` |
| `ATLAS_TRANSCRIPT.txt` | `efb8d2c0642ce80d149d55187cf3525cee0ec78d31a36afaeebeeae7d44f8bfc` |
| `FAMILY_CLASS_CENSUS.tsv` | `845bfd3cd5c18175085fc33f43fafaec2ee9d8fa06417224d26f4da137f6d82b` |
| `FAMILY_SUBSPACE_ATLAS.tsv` | `6dc990996d16e2262e312006759979308d373de8a2b2af95e85c072d483c0043` |
| `VERIFICATION_RESULT.json` | `ba96cf770d96ce606f3ffbf678422d2c8097b5d2ecf4cfca9423ead13b82fb66` |
| `FRESH_ADVERSARIAL_REVIEW.md` | `c4a4b5734d5ae04cf53ba7461889d80daf74d295503fa587819e5d8a54f8ba61` |
| `FRESH_ADVERSARIAL_REVIEW_TRANSCRIPT.txt` | `f2a53ab5228a90b7c8cadaa574f40bb135f16bf741e29a9c1b265a5cbc8b4277` |

## Frozen correction contract

1. Keep the same 6,144 configurations, nine **named** preregistered families, nonlinear maps,
   tolerances, and maximum allowed conclusion. Do not broaden “complete” beyond those nine named
   families; unregistered joint subsets remain open.
2. For each real central element, cluster its distinct complex eigenvalues, pair conjugate clusters,
   and construct real primary projectors by polynomial spectral interpolation. A conjugate pair is
   one real primary block.
3. Accept a block only when the real projector passes rank, reality, idempotence,
   metric-self-adjointness, centrality, operator commutation, and complementary-sum gates.
4. Treat unpaired complex clusters, failed conjugacy/multiplicity, Jordan/projector residual failure,
   or trial instability as `NUMERIC_UNCERTAIN`; never count them as classified absence.
5. Recompute all central-block and nonlinear-chart classifications. Preserve every new unique,
   multiple, absent, and uncertain result without physical ranking.
6. Reimplement real primary projectors independently. Compute all preregistered anchor values before
   reading any saved builder classification.
7. Replace registry, nonsimple-bivector, filtered-row, and conclusion catches with mutations that
   are passed through the same fail-closed validators used for saved results. Retain the null-dyad,
   nonlinear-jet, dropped-operator, and hidden-uncertainty catches, strengthened similarly where
   needed.
8. Add a catch proving that deletion of conjugate-pair grouping fails on the adversarial
   `R00_1_M1_B0_P0/F01_RICCI` anchor.
9. Rerun the full atlas, independent anchors, repository gates, and a new fresh adversarial review.

No result count is preregistered. The full-joint irreducibility observation is provisional until the
corrected replay passes; no physical or global section conclusion is allowed.
