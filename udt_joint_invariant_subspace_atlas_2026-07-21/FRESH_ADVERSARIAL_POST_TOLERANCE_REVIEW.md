PASS

Decisive evidence:

- Production complementary-projector pairing now uses `RANK_TOL = 1e-9`. All projector realness, residual, completeness, orthogonality, and stability acceptance gates use `1e-9`. The remaining `1e-7` values exclusively define the preregistered uncertainty-band ceiling; they are not acceptance thresholds.
- For the exact Lorentzian \(g\)-self-adjoint nilpotent \(J\), independent execution confirmed \(J^2=0\), \(J\neq0\), and both builder and verifier return `NUMERIC_UNCERTAIN_CENTRAL_BLOCKS / NUMERIC_UNCERTAIN`.
- Independent census reproduced:

  - Unique: 11,983 — F01 4,298; F02 3,003; F04 2,533; F05 2,149.
  - Multiple: 2,225 — F01 1,078; F02 69; F04 539; F05 539.
  - Affected configurations: 5,210.
  - Escalation exceptions in either F08 or F09: zero.

- An independent 4,096-point Riesz-contour reconstruction of `R00_1_M1_B0_P0/F01_RICCI` recovered the conjugate spectrum and rank-two real primary plane plus rank-two complement. Projector idempotence, self-adjointness, commutation, completeness, and orthogonality residuals were \(7.8\times10^{-17}\)–\(4.7\times10^{-15}\).
- All ten catches exercise their applicable production/saved-record validators. K03 invokes the production dyad path; K05 includes an actual non-simple bivector classification; K09 and K10 invoke the real-primary and Jordan classifier paths. The verifier computes all 480 original and 960 transformed anchors before reading saved builder classifications.
- All 61 package-manifest entries hash-replay and exactly cover the package. Preserved failure layers pass their registered hashes. Six frozen manifests replay with 127 entries/133 tracked paths; 67 prior packages replay with 1,731 entries. Navigation verifies 1,114 current paths, 306 frontier rows/101 targets, and eight package links.
- The documented baseline remains 69 passed, one known hygiene failure, and one xfailed, with a matching result signature. The saved dirty-checkout record reports 54 metadata-only paths, `contents_read=false`; the original checkout was not queried.
- Claims remain explicitly limited to the nine named preregistered pointwise families. Transported/global/physical sections, action, source, carrier, boundary, scale, topology, and dynamics remain `OPEN`.

Required correction: none.

Maximum conclusion honestly supported: `BOUNDED_POINTWISE_JOINT_INVARIANT_SUBSPACE_ATLAS_CHARACTERIZED`.