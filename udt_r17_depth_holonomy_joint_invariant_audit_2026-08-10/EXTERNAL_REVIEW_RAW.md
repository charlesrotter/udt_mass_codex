**Verdict**

`VERIFIED_WITH_CORRECTIONS`

**Reconstructed Mathematics**

- The manifest-backed stationary R17 joint datum is a typed arrow
  `(\Delta_K(p,q), U_\gamma)` with `\Delta_K(p,q)=\phi(q)-\phi(p)` from the intrinsic pair-leaf metric and `U_\gamma:H_p->H_q` the metric-projected normal parallel transport on the oriented normal plane `H`. This is a product of groupoids, not a single fixed matrix group. Local `R x SO(2)` coordinates appear only after choosing oriented endpoint frames in `H_p,H_q`. See [intrinsic pair foliation](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:30), [path-labelled connection](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/EXACT_DERIVATION.md:157).
- Composition is
  `(\Delta_2,U_2)∘(\Delta_1,U_1)=(\Delta_2+\Delta_1,U_2U_1)`,
  inversion is `(-\Delta,U^{-1})`, and for every real `w`,
  `C_w(\gamma)=exp(w\Delta_K(\gamma))U_\gamma`
  obeys the same composition law. This follows from additivity of `\Delta_K` and functoriality of `U_\gamma`. See [path-labelled connection](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/EXACT_DERIVATION.md:157), [R17 conditional assembly](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_branch_nonisometric_calibration_transition_audit_2026-08-10/EXACT_DERIVATION.md:40).
- The complete coframe fixes the screen metric class, not a full observer arrow. Since `q_H=exp(2\lambda\phi)(\sigma_1^2+\sigma_2^2)`, the geometric screen lift is `exp(\delta X_\lambda)` with screen weight `+\lambda` on orthonormal screen vectors; relative to inherited reference-vector coefficients `(X,Y)` that is weight `-\lambda`, while in the variance-dual reference-coframe representation `(σ_1,σ_2)` it is `+\lambda`. The sign flip is the usual vector vs covector / inverse-transpose convention. See [magnitude-to-grading](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_magnitude_to_grading_selection_audit_2026-08-10/EXACT_DERIVATION.md:86).
- Open-path holonomy is only endpoint-gauge covariant: under independent endpoint screen-frame changes,
  `U_\gamma -> h_q U_\gamma h_p^{-1}`.
  For open paths this action is transitive on the unframed `SO(2)` representative, so no nonconstant order-zero real scalar can depend on `U_\gamma` alone. Loops and two-path relative holonomy `U_\beta^{-1}U_\gamma` survive because they transform only by basepoint conjugation; in `SO(2)` that leaves the angle, while an optional `O(2)` quotient identifies `\theta~-\theta`. See [scalar descent](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/EXACT_DERIVATION.md:51), [path-labelled connection](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_path_labelled_connection_decomposition_audit_2026-08-10/EXACT_DERIVATION.md:171).
- For continuous real characters factoring through the local order-zero model `R x SO(2)`, the `SO(2)` part must vanish because any continuous homomorphism from compact `SO(2)` to additive `R` is zero. So every such character is `c\Delta`; reciprocal normalization fixes `c=1`, leaving only `\Delta_K`. This is strictly weaker than classifying arbitrary cocycles on flag/path groupoids. Compare the broader flag-source caveat at [reciprocal flag foundation](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/EXACT_DERIVATION.md:197).
- Every continuous action `R->Aut(SO(2))` is trivial: `Aut(SO(2))≅{±1}` is discrete, so continuity forces the identity action. If orientation reversal is retained, the enlargement is `R x O(2) ≅ (R x SO(2)) ⋊ Z_2`, with `Z_2` acting by inversion on the `SO(2)` factor and trivially on `R`.
- The C08 control gives `\Delta(loop)=0`, `B_0(1)=4097/4096`, and `F23=-2B_0(1)=-4097/2048`, so zero reciprocal depth coexists with nontrivial angular holonomy. That suffices to show reciprocal depth does not determine angular holonomy in this stationary arena. See [stationary sublocus](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/EXACT_DERIVATION.md:111), [stationary sublocus](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_stationary_connection_sublocus_ownership_audit_2026-08-10/EXACT_DERIVATION.md:252).
- On higher jets, the only generic fact I can defend from the sealed intake is that a supplied one-form has additive line integral under concatenation. The intake does not contain a manifest-backed `alpha = I dphi` or rectangle derivation to ratify, and it explicitly keeps higher-jet nonmetric families unselected. So no endpoint-frame-invariant non-exact scalar one-form independent of `dphi` is derived for stationary cohomogeneity-one R17. See [reciprocal flag foundation](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/EXACT_DERIVATION.md:293), [premise ledger](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/CURRENT_SCIENTIFIC_PREMISES.tsv:36).

**Corrections**

- Replace any silent fixed-group reading by the correct product-groupoid typing: endpoint fibers are different until frames are chosen.
- Treat `C_w=exp(w\Delta_K)U_\gamma` as a screen representation family only. The full physical observer arrow remains conditional, not derived. See [magnitude-to-grading](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_r17_magnitude_to_grading_selection_audit_2026-08-10/EXACT_DERIVATION.md:193).
- Do not call the open-path `SO(2)` matrix gauge invariant; only loop classes and same-endpoint relative holonomy survive endpoint gauge.
- Do not inflate the character theorem into a classification of arbitrary path cocycles, endpoint coboundaries, or derivative-dependent line integrals.
- No manifest-backed equation here selects a path, a physical non-isometric observer arrow, a branch, a universal `lambda`, a higher-jet one-form, or a universal mixed-geometry `c_eff`. The semidirect R17 formula is exact on matched carried states but not branch-owned. See [branch transition](/tmp/udt_r17_depth_holonomy_joint_review_preflight_uZBW6W/sources/udt_branch_nonisometric_calibration_transition_audit_2026-08-10/EXACT_DERIVATION.md:40).

**Maximum Defensible Claim**

On the sealed regular stationary R17 intake, the defensible joint order-zero structure is the path-labelled product-groupoid arrow `(\Delta_K,U_\gamma)`, with exact composition and inversion, and with the complete coframe fixing only the projector-preserving vertical screen metric class `exp(\delta X_\lambda)` modulo endpoint `SO(2)`. After quotienting by endpoint gauge, open-path angular data carry no nonconstant order-zero real scalar, while loop and relative-path holonomy survive; continuous real characters of the local connected model reduce to `\Delta_K` alone.

**Open Seams**

- Physical path/query selection and the physical non-isometric observer arrow.
- Identification of carried and rebuilt endpoint gradings beyond the derived `SO(2)` alignment bitorsor.
- Integration of the conditional linear arrow into a global calibrated pair surface/comparison Jacobian.
- Any stationary R17-owned endpoint-frame-invariant non-exact scalar one-form independent of `dphi`.
- Any universal mixed-geometry `c_eff`, and any extension beyond regular stationary R17 to time-live, null, rank-changing, or other branches.
