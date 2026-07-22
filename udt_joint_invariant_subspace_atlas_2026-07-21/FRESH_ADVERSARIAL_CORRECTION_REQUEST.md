# Fresh Adversarial Correction Review Request

Review the corrected package `udt_joint_invariant_subspace_atlas_2026-07-21/` read-only against:

1. committed `PREREGISTRATION.md` and `PREREGISTRATION_CORRECTION.md`;
2. committed `REAL_SPECTRAL_PROJECTOR_CORRECTION.md`;
3. the first failed `FRESH_ADVERSARIAL_REVIEW.md` and its required corrections.

Do not edit files, switch branches, fetch, pull, push, or use a GPU.

Independently audit:

- real primary projectors for complex-conjugate central spectra, including the exact
  `R00_1_M1_B0_P0/F01_RICCI` counterexample;
- the corrected 11,983 unique and 2,225 multiple central-split rows by family;
- the claim that every smaller-family unique-split configuration becomes full-matrix-algebra
  irreducible in both complete curvature-plus-phi families;
- whether unresolved primary/Jordan cases are fail-closed as uncertain;
- whether the independent Vandermonde/CRT verifier is genuinely distinct and computes all anchors
  before reading saved classifications;
- whether all nine catch-proofs are exercised end-to-end enough to detect the registered mutations;
- whether “complete” is now confined to the nine named families and other subsets remain open;
- whether the reports accurately distinguish a smaller-family local split from a full-joint,
  transported, global, or physical section.

Replay focused CPU checks if useful, but do not mutate the package.

Return exactly `PASS`, `PASS-WITH-CAVEATS`, or `FAIL`, followed by decisive evidence, any required
correction, and the maximum conclusion honestly supported.
