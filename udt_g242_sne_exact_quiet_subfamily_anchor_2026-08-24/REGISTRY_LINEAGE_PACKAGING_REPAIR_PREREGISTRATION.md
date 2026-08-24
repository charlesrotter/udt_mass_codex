# G242 registry-lineage packaging repair preregistration

Date: 2026-08-24

## Observed mechanical failure

G242 preregistered against the exact 224-row `CURRENT_SCIENTIFIC_PREMISES.tsv` recorded in
`SOURCE_MANIFEST.tsv`. Afterward, the externally reviewed G243 result was banked by appending one
`G243` row to that registry. The current G242 production replay therefore stops at its source hash
gate before recomputing the already saved scientific result.

This is an append-only authority-lineage problem. It is not evidence for changing the G242 model,
data, covariance, threshold, classification, or epistemic ceiling.

## Preregistered repair

The production manifest check and sealed-intake builder may treat the present registry specially:

1. read its bytes without editing the registry;
2. require exactly one line whose first field is `G243`;
3. remove exactly that line in memory;
4. require the SHA-256 of the reconstructed bytes to equal the preregistered G242 manifest hash;
5. leave every other source under its ordinary full-file SHA-256 check.

The current registry, including its banked G243 row, may be copied into the sealed intake. The same
in-memory reconstruction must then pass inside the intake without repository access.

## Forbidden repair drift

The repair must not:

- change `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, or `CATCH_PROOF_RESULT.json`;
- change the exact quiet-subfamily equation, frozen G237 state, full covariance, chi-square ceiling,
  or classification;
- remove, ignore, normalize, or rewrite any line other than the single `G243` row;
- open BOSS/BAO/CMB outcomes or access protected packages;
- treat the historical 224-row registry as current authority.

## Acceptance gates

The repair is accepted only if:

- the reconstructed registry digest is exactly
  `2ccd420adb34d0b9effe7b92a1bbf0b1fc3916f446dcf3e64fb2916345dd9290`;
- all three registered no-write replays and `verify_package.py --no-write` reproduce the saved
  artifacts exactly;
- a direct repository-relative sealed replay passes;
- the retained scientific landing remains
  `EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN`.

Maximum conclusion: packaging and append-only premise lineage are repaired; the G242 scientific
landing is unchanged and still requires fresh external adversarial review.
