FAIL

Decisive evidence:

- The production bivector complementary-projector gate still accepts completeness/orthogonality residuals at `1e-7`, violating the preregistered controlling `1e-9` tolerance: [invariant_subspace_core.py](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_joint_invariant_subspace_atlas_2026-07-21/invariant_subspace_core.py:625). The independent verifier correctly uses `1e-9`. Zero saved candidate eigenplanes make this defect outcome-silent, but the frozen certification contract requires the production gate itself to be correct.

Everything else reviewed passed:

- The exact Lorentzian \(g\)-self-adjoint nilpotent Jordan example has \(J^2=0\ne J\) and spectrum \(\{0,0,0,0\}\). Both actual classifiers return `NUMERIC_UNCERTAIN_CENTRAL_BLOCKS / NUMERIC_UNCERTAIN`. Their implementations are separate modules with independent centralizer/projector paths.
- Independent counts reproduce 11,983 unique rows—F01 4,298; F02 3,003; F04 2,533; F05 2,149—and 2,225 multiple rows—1,078; 69; 539; 539—across 5,210 configurations. Escalation to both F08 and F09 yields zero exceptions.
- An independent Riesz-contour reconstruction of `R00_1_M1_B0_P0/F01_RICCI` gives spectrum
  \(-0.014654793138\pm0.010524327286i,-0.000112976085,0.040414989992\), with rank-two conjugate and complementary projectors. Idempotence, Lorentzian self-adjointness, commutation, completeness, and orthogonality residuals are \(7.3\times10^{-17}\)–\(3.3\times10^{-15}\).
- The read-only verifier recomputed all 480 original and 960 transformed anchors before loading builder classifications: 12,960 classifications agreed, with four retained uncertain comparisons. All ten catches passed; K01–K08 use the saved-record validators, K03 uses the production dyad function, and K09/K10 exercise the actual spectral/classifier paths.
- The 57-entry manifest replays exactly; preserved failure-layer hashes, six frozen manifests, 67 prior-package manifests, 1,114 current paths, 306 frontier rows, and seven historical `path:line` links pass. Tests reproduce the registered baseline: 69 passed, one known hygiene failure, one xfailed.
- Dirty-checkout metadata records 54 paths, all `NOT_READ`, with the expected metadata hash. The original checkout was not accessed.
- Wording is confined to the nine named pointwise families; transported/global/physical sections, action, source, carrier, boundary, scale, and dynamics remain open.

Required correction: replace the `1e-7` bivector complementary-projector threshold with the controlling `1e-9` constant, then rerun builder, independent verifier, manifest, repository gates, and fresh review.

Maximum conclusion honestly supported: `BOUNDED_FULL_JOINT_FAMILY_IRREDUCIBILITY_OBSERVED`; the 11,983/2,225 census is also `OBSERVED`, but final atlas certification remains open.