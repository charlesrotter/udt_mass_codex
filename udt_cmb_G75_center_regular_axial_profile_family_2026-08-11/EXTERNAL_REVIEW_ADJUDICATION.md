# G75 external-review adjudication

Date: 2026-08-11

External landing: `VERIFIED_WITH_CAVEATS`

Accepted project status:
`EXTERNALLY_VERIFIED_BOUNDED_FAMILY__INTERNAL_INDEPENDENCE_AND_CATCH_COMPLETENESS_CAVEATS_CLOSED_LOCALLY`.

`AUDIT_REPORT.md` and the 23-file `PACKAGE_SHA256SUMS.txt` payload remain byte-identical historical
records of the pre-review landing. This additions-only adjudication is the current status layer.

## What survived

The sealed reviewer verified all `34/34` authorized payload hashes before scientific inspection and
reconstructed the finite family without using the production generator:

- `49` primitive coefficient rays;
- `591` profiles (`49 x 4 x 3 + 3`);
- zero shape-row mismatches;
- zero profile-row mismatches;
- behavior census `28/9/6/5/1` for persistent sign, interior sign change, center-off, endpoint
  taper, and zero at both boundaries;
- eight exact root/boundary strata;
- center orders `41/7/1`, endpoint orders `43/5/1`, and odd-interior-root counts `40/9`;
- Cartesian `C-infinity` center regularity for every profile;
- Lorentz signature throughout the closed symbolic cell for every registered lapse control.

The reviewer also sharpened the reflection statement: `psi -> -psi` is an isometry taking `g[q]`
to `g[-q]` inside the declared stationary axial envelope. Orientation remains physically
unselected; the equivalence does not select a measured branch.

## Caveats and corrections

No algebraic field, classification row, or scientific conclusion required correction. The two
caveats concern the strength of the original local evidence:

1. `verify_profile_family_independent.py` was only partially independent. It independently
   enumerated the lattice and checked normalization, root multiplicity, and boundary orders, but
   did not separately reconstruct every exact root, extremum, behavior label, and stratum label.
2. `run_catch_proofs.py` caught aggregate/status mutations but did not attack algebraic fields while
   preserving aggregate counts.

The preregistered correction layer now expands the local replay from `10/10` to `16/16` checks and
the hostile layer from `10/10` to `16/16` mutations. The fresh sealed review—not the local script—is
the independent load-bearing reconstruction. The historical 49-row and 591-row atlases remain
byte-identical.

## Evidence gates

1. Preregistered: **yes**, original G75 commit `e88d7511`; external review commit `43de3554`;
   correction preregistration commit `e79fe73f` before local repair.
2. Full space: **yes only for the frozen 49-ray quadratic definition**.
3. Independently verified: **yes for the bounded finite-family claim**, by the fresh sealed external
   reconstruction with zero row mismatches.
4. Premises audited: **yes for the bounded stationary axial envelope**.

## Maximum justified conclusion

G75 exactly constructs and classifies the complete frozen `49`-ray / `591`-profile
center-regular stationary axial quadratic family. Multiple exact smooth shape strata survive.

It does **not** exhaust all smooth center-regular profiles, represent the generic ten-function
metric, select a physical CMB profile/source/endpoint/scale, determine `R` or `X_max`, populate a
sky, fit peaks, or derive bootstrap, action, matter, or dynamics.

## Exact preserved review artifacts

- `EXTERNAL_REVIEW_RAW.md` SHA-256:
  `d4b0a0a8529b08930d180eee010edd9060bd43e0d72460cf82d29b482d14dde8`
- `EXTERNAL_REVIEW_TRANSCRIPT.txt` SHA-256:
  `506245bd94ecdd5e23f11bfc9600413167203eb0381011e9d8a3dbdb8c4a9e21`
- reviewer response body hash (excluding its self-referential hash bullets):
  `5b7701a9927ec651aca9b21e1d45a5ad9ceebec89f9dcba61f91d49e44f70a06`
- reviewer inline verifier hash:
  `8b22b0c63f9c3b90e64975d88c28a6da9d8200e3301c8a8a45f984e14f564cc1`

## Next bounded gate

Preregister a whole-sky angular response map whose inputs are fixed before response inspection by
the exact G75 strata. Cover the complete family if computationally reasonable; otherwise use a
representative set chosen solely from the preregistered stratum labels. Do not fit peaks, rank
profiles by desired appearance, or treat the control envelope as the physical universe.
