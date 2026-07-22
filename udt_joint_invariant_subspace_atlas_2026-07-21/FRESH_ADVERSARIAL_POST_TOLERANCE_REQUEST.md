Perform a fresh, read-only post-tolerance adversarial review of
`udt_joint_invariant_subspace_atlas_2026-07-21/`.

Do not edit files, switch branches, fetch, pull, push, use a GPU, or read the contents of the
original dirty checkout. Work only from the clean checkout and bounded CPU/read-only checks.

Read the preregistrations and every preserved correction/review layer, ending with
`FRESH_ADVERSARIAL_FINAL_REVIEW.md` and `BIVECTOR_TOLERANCE_CORRECTION.md`. Independently decide
whether the final package now satisfies all correction contracts.

Required checks:

1. Confirm the production bivector complementary-projector test now uses `RANK_TOL=1e-9`, and that
   no projector acceptance/realness/completeness/orthogonality/stability gate retains `1e-7`.
   Distinguish the allowed `1e-7` uncertainty-band ceiling from an acceptance threshold.
2. Reproduce the exact Lorentzian self-adjoint nilpotent Jordan counterexample in both the builder
   core and independent verifier; both must fail closed as `NUMERIC_UNCERTAIN`.
3. Independently reproduce 11,983 unique rows, 2,225 multiple rows, the four per-family counts,
   5,210 affected configurations, and zero escalation exceptions in both full registered families.
4. Independently reconstruct the `R00_1_M1_B0_P0/F01_RICCI` conjugate real rank-two primary plane
   by a third method if needed to verify the retained spectral correction.
5. Audit the ten catch paths and compute-before-read ordering; reject any vacuous validator.
6. Verify `REPOSITORY_GATES.json`, the 61-entry package manifest and its coverage, preserved failure
   hashes, six frozen manifests, 67 prior packages, navigation, documented test baseline, and the
   saved 54-path metadata-only dirty-checkout result. Do not query the original checkout yourself.
7. Confirm all conclusions remain confined to the nine named preregistered pointwise families and
   that transported/global/physical sections, action, source, carrier, boundary, scale, topology,
   and dynamics remain open.

Return exactly `PASS`, `PASS-WITH-CAVEATS`, or `FAIL`, followed by decisive evidence, any required
correction, and the maximum conclusion honestly supported.
