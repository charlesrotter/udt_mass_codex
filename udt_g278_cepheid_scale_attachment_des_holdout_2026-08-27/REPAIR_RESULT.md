# G278 external-review repair result

Date: 2026-08-27

Status: `R1_R2_R3_EXTERNALLY_ACCEPTED`

The three preregistered repairs were performed without changing the scientific question, inputs,
model, tolerances, observational masks, covariance routes, or accepted numerical artifacts.

## R1 — direct sealed replay

`build_review_intake.py` now copies all ten `SOURCE_MANIFEST.tsv` payloads into their existing
repository-shaped, intake-root-relative paths. The additional G275--G277 context is copied the same
way. From a freshly built intake root, without manual rearrangement:

- all `50/50` manifest payload rows matched exact byte counts and SHA-256 hashes;
- the production derivation passed;
- the implementation-distinct verifier passed;
- all eight hostile controls passed;
- the resolution diagnostic reproduced;
- the package verifier passed.

## R2 — detached manifest seal

The builder now writes `REVIEW_MANIFEST.sha256` after the payload manifest. Running
`sha256sum -c REVIEW_MANIFEST.sha256` in the fresh intake returned
`REVIEW_MANIFEST.tsv: OK`.

The detached seal is intentionally outside the payload manifest; its own hash and the manifest hash
are reported separately for external authorization.

## R3 — exact sealed command surface

`COMMANDS.md` now lists only commands runnable from the sealed intake root and points
`G236_DES_ROOT` to the sealed `external_data` directory. The repository-wide premise audit is
explicitly identified as a separate local banking gate and is not advertised as an intake replay.

## Unchanged scientific landing

Fresh intake-shaped replay retained exactly:

- primary `K=12` scale: `286.25733633510214 Mpc`;
- primary scale uncertainty: `5.142253493374308 Mpc`;
- calibration chi-square: `57.134728577478334` for `76` degrees of freedom;
- resolution chi-square: `60.40538886961107`, rank `3`, gate failed;
- maximum calibrator-subset excursion: `3.1114981409766966 sigma`, gate passed;
- DES chi-square: `1434.579290816418` for `1623` degrees of freedom, gate passed;
- landing: `SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE`;
- diagnostic: `PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS` and no regrade.

No preferred resolution, average, smoother, DES offset, `P1`, angular fit, `X_max`, LCDM distance,
metric change, kernel change, state retuning, or CMB model was introduced.

## External closure

A fresh sealed gpt-5.4 repair-only follow-up verified all `51/51` payload hashes, all three outer
seals, zero symlinks, direct intake replay, the five registered commands, post-replay integrity, and
the unchanged scientific landing. Verdict: `ACCEPT`. Remaining R1--R3 defects: none.
