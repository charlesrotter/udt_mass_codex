# G192 external-review repair execution

Date: 2026-08-20

The two repairs preregistered after the first external review are implemented.

## Repair 1 — fresh/sealed identity

`verify_package.py` now parses each child replay's fresh JSON stdout and compares it field-for-field
with the corresponding saved artifact. The comparator is live:

1. before regenerating the structurally repaired catch artifact, the no-write replay failed with
   `catches fresh/sealed mismatch: fresh_only=['structural_evidence']`;
2. after regenerating that artifact, the replay passed;
3. a registered in-memory mutation of the sealed production artifact is rejected by the same
   comparator, reported as `stale_artifact_mutation_caught=true`.

A successful child exit plus stale on-disk evidence can therefore no longer pass the wrapper.

## Repair 2 — structural hostile catches

The catch script no longer searches production source text for the matrix, factorization, or
omitted-input labels. It now:

- launches a fresh no-write production derivation and parses its JSON;
- parses the returned Jacobi expressions with SymPy;
- verifies an exact symmetric `2 x 2` response, both modal projectors, determinant identity, and a
  generically nonzero cross term;
- reconstructs the positive-mode factorization and obtains zero formula and ODE residuals;
- extracts functional atoms from the returned scientific formulas and obtains exactly
  `I`, `J`, `a`, and `mu`;
- parses executable Python syntax and finds none of the registered P1, G116, G189, `X_max`, or
  radiative-transfer input names.

All 18 original catch names remain green. The existing numerical deletion, sign, scalarization,
turn, branch, and constant-control differences are unchanged.

## Identity and replay gates

- first-reviewed `PRODUCTION_RESULT.json` SHA-256:
  `ddfb7ec0b81ede4cc0d681c60835d8909a59f7830b7eec2cff8a9146962c9f23`
- repaired `PRODUCTION_RESULT.json` SHA-256: identical
- first-reviewed `INDEPENDENT_VERIFICATION.json` SHA-256:
  `993be1a673eb83549538fb93fe9fa62833760987cc254b2f8302b5324f4cb439`
- repaired `INDEPENDENT_VERIFICATION.json` SHA-256: identical
- repaired `CATCH_PROOF_RESULT.json` SHA-256:
  `12289d00fa5edb13dd51e1f81a5128ceff872706707360dec3d1098d92f216fc`
- repaired `PACKAGE_VERIFICATION_RESULT.json` SHA-256:
  `d0463a31cb20344f69f7002001be1fb71ef02fc0de857ea7b70f958d15cb58a0`
- repaired no-write replay: pass
- artifact hashes before and after that replay: byte-identical
- current 176-row premise verifier: pass
- repository tests: 130 passed, 1 expected xfail
- `git diff --check`: pass

No scientific formula, witness, tolerance, premise status, or bounded landing changed. Final external
acceptance remains pending a fresh authorized repair-only review.
