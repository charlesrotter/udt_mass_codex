# G278 external repair-only follow-up review

Verdict: `ACCEPT`

## Seal verification

- `REVIEW_SCOPE.json` matched SHA-256 `886f5ccddc871faa5ebec03878dfd844253a106dc25247ce8816e9583f2cea63`.
- `REVIEW_MANIFEST.tsv` matched SHA-256 `3ac5ff91435eb4c8fcb8b87db45c1cc41c59475bacb1a25085c7b56620fce864`.
- `REVIEW_MANIFEST.sha256` matched SHA-256 `e924a6c1ec98be9542c88c0b5246d3a49aaffa3ec0e97a560ce0130e9f70bf0c`.
- The manifest contained exactly `51` payload rows; the intake contained exactly `53` physical
  files and `0` symlinks.
- All `51/51` payload rows matched their sealed byte counts and SHA-256 values.
- `sha256sum -c REVIEW_MANIFEST.sha256` returned `REVIEW_MANIFEST.tsv: OK`.

## R1--R3 replay verification

- R1 passed. The sealed intake was repository-shaped and directly replayable without internal
  rearrangement.
- All five registered intake-root commands passed in an unchanged writable copy:
  `derive_scale_and_holdout.py`, `verify_independent.py`, `run_catch_proofs.py`,
  `diagnose_resolution_sensitivity.py`, and `verify_package.py`.
- R2 passed. The detached outer checksum verified in both the sealed intake and replay copy.
- R3 passed. The sealed command surface contained only intake-root replays and excluded the
  repository-wide premise audit.
- Post-replay integrity held with `0` manifest mismatches.

## Scientific landing

The bounded landing remained `SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE`.

The load-bearing numbers remained unchanged:

- `ell_mpc=286.25733633510214`;
- `ell_sigma_mpc_delta=5.142253493374308`;
- `chi2_cal=57.134728577478334`, `dof_cal=76`;
- `resolution_chi2=60.40538886961107`, `resolution_rank=3`;
- DES `chi2=1434.579290816418`, DES `dof=1623`;
- DES `residual_mean_mag=0.1759203914730402`.

The diagnostic remained `PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS` with
`cannot_regrade_original=true`. Independent verification retained `10/10` checks and hostile
controls retained `8/8` checks.

Remaining R1--R3 defects: none.

Raw external response SHA-256:
`1a17543f1c74ea3818f8b1f91c23ee2fccca136721d0f027f34721e1e99d0d53`
