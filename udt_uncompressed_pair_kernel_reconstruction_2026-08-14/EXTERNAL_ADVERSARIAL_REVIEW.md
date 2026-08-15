# External adversarial review — raw return

Date: 2026-08-14

Reviewer: external Codex `gpt-5.4`, high reasoning, ephemeral, web disabled

Intake: `/tmp/udt_uncompressed_pair_review_lasyl_g1`

Scope SHA-256: `1e39c04f30e9df911839541a40d92e9a8dda844431a3fe3d10ac27b4c77a0782`

Raw-return SHA-256: `ee018eba1a889682d46cde482895f4d433e32f57eeeb175ac0443ee16edd4af2`

The text below is the verbatim last-message return from the sealed review. Its temporary absolute
links record the review environment and are not durable repository links.

---

VERIFIED_WITH_CAVEATS

No blocking defect found in the sealed scope.

Defects or caveats:
- The main result is only a conditional local evaluator for supplied `E` and supplied pair Jacobian `J`; it does not derive the physical pair realization or any live history, and the source mostly respects that boundary [EXACT_DERIVATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md:42) [EXACT_DERIVATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md:241) [PREREGISTRATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/PREREGISTRATION.md:218).
- The Gram compression `P=C^TqC` is exact only on the explicitly secondary invertible-`Y` A-calibrated quotient; it is not used in the primary formula, but it does erase `S` versus embedding, screen-frame representative data, and some live uncompressed motion [PREREGISTRATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/PREREGISTRATION.md:70) [EXACT_DERIVATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md:282).
- No source-owned bridge identifies July `mu_old` with modern `S`, `C`, `P`, or any unique scalar invariant; the sealed source supports keeping scalar `mu` open [EXACT_DERIVATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md:362) [AUDIT_REPORT.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md:7).
- The earlier quiet-middle kernel remains a fixed-`P` conditional diagnostic, not a derived physical regime law; the regrade is semantically correct on that point [PREREGISTRATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_uncompressed_pair_kernel_reconstruction_2026-08-14/PREREGISTRATION.md:18) [EXACT_DERIVATION.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/EXACT_DERIVATION.md:29).

Independently reproduced checks:
- Verified `REVIEW_SCOPE.json` SHA-256 and all 28 payload hashes and sizes exactly.
- Reconstructed `h=J^TE^Teta_4EJ=Y^TB^Teta_2BY+(SY+Z)^TQ^TQ(SY+Z)` independently; direct and factored forms matched on an exact rational witness.
- Tested the hidden `det(Y) != 0` risk with a regular singular-`Y` witness: `det(Y)=0`, `rank(J)=2`, `h00=-1799/648`, `det(h)=-98975/20736`, and the primary pullback plus terminal ratio-squared identity still held exactly. So the primary result is not secretly using `Y^-1`.
- Replayed the full first-variation census without production imports. Exact one-channel `E00` perturbations produced nonzero `dphi` in all five sectors `B,Q,S,Y,Z`, so no sector is frozen in the claimed live identity.
- Reconstructed the terminal readout algebra independently: `T_pair^2=-h00`, `L_pair^2=h11-h01^2/h00`, `-det(h)=T_pair^2L_pair^2`, `phi_pair=(1/4)log[(-det h)/h00^2]`, and `c_eff/c_E=(-h00)/sqrt(-det h)` is derived from that decomposition, not merely renamed.
- Reproduced the compression fibers: `S -> S+D`, `W -> W-D` preserves `C`; `Q -> OQ` preserves `q`; `C -> OC` preserves `P`; and there are equal-`P`, equal-`Pdot` paths with nonzero skew `dot C`, so `P` loses representative live motion even when it preserves the pair metric data.
- Searched the sealed source universe for a type-correct `mu_old` bridge and found none; the July audit itself says the registered cocycle/orientation machinery is `mu`-blind rather than selective [AUDIT_REPORT.md](/tmp/udt_uncompressed_pair_review_lasyl_g1/udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md:79).

Maximum justified conclusion:
For a supplied regular complete metric and supplied regular ordered pair realization, the sealed package does derive an exact uncompressed pair metric and terminal `phi_pair`/`c_eff` evaluator, with reciprocal/base, screen, four-component mixing, and pair-embedding channels retained up to the point of readout. The chain rule and live formulas are kinematic only. The compressed `P` quotient is sufficient for the zero-order A-calibrated pair metric on `det(Y) != 0`, but it loses source attribution and some uncompressed live information. No justified current scalar `mu` emerges, and no physical pair-selection or evolution law is derived.

Lay explanation:
The math checks out as a calculator for “given this metric and this chosen observer pair, what final clock-ratio comes out?” It does not yet show which observer pair nature picks, how that pair evolves, or that one special scalar `mu` has been discovered.
