**Landing**

`VERIFIED_WITH_CAVEATS`

**Findings**

- Medium: the package’s own `PACKAGE_VERIFICATION` is not sealed-intake-pure. It invokes repo-wide premise tests, repo-wide pytest, external frozen manifests, and the current artifact registry outside the 20-row source manifest, so that verifier cannot be counted as sealed evidence for this dispatch. See [verify_package.py](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/verify_package.py:86) and [verify_package.py](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/verify_package.py:102).

- Medium: the claimed “independent verification” is independent for the census/algebra, but not for the ownership join itself. It hardcodes the seven expected route statuses and re-reads the produced landing JSON instead of re-deriving route ownership from the frozen sources. That weakens the independence claim, but it does not expose a contradictory route owner. See [verify_owner_join_independent.py](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/verify_owner_join_independent.py:76) and [verify_owner_join_independent.py](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/verify_owner_join_independent.py:93).

- Low: the sealed source universe is exactly 20 rows, and it omits some current parent packages such as G66 and G74. I checked the current registry lines for those omitted parents; both still leave the physical realization/source/endpoint/scale open, so I did not find a missing current source that already closes a G78 route. This remains a bounded 20-source landing, not a stronger current-universe theorem. See [SOURCE_MANIFEST.tsv](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/SOURCE_MANIFEST.tsv:2) and [CURRENT_SCIENTIFIC_PREMISES.tsv](/tmp/udt_g78_review_I5y4y7/CURRENT_SCIENTIFIC_PREMISES.tsv:67).

**Reproduced values**

- Source scope: `20` sealed rows at base `9a78af889321d84914ae5eb2c066da56bc957719`. See [SOURCE_MANIFEST.tsv](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/SOURCE_MANIFEST.tsv:2).

- Family census: `591 = 49*4*3 + 3 = 588 + 3`; I recomputed `588` nonzero controls and `3` zero controls. See [G75 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/EXACT_DERIVATION.md:32).

- G77 census: `590 STRONG_DIRECT_AGREEMENT`, `1 REGISTERED_DIRECT_AGREEMENT`, `0 unresolved`; every row had `crossed_vertices=2562`, `missing_vertices=0`, `negative_faces=0`, `negative_projected_face_maps=0`, `near_area_1e2=0`; reproduced `max |degree-1| = 2.220446049250313081e-16`. See [G77 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11/EXACT_DERIVATION.md:27).

- Scale factorization: under `tau=c_E t/R`, I reproduced
  `tau_tau=-A`, `x_x=1/A`, `theta_theta=1`, `psi_psi_unit_x2=1`, `tau_psi=2 h sin^2(theta)`,
  hence `ds^2=R^2 dSigma^2`. I found no scoped re-entry of `R` or `c_E` that defeats the dimensionless angular-relation claim; affine rescaling only changes common response scale, not the angular path relation. See [G78 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/EXACT_DERIVATION.md:31) and [G72 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G72_metric_screen_response_join_2026-08-11/EXACT_DERIVATION.md:23).

- Endpoint/SNe typing: G76/G77 use the first outward crossing of `|X|=1`; `X_max` is still only an observer-pair asymptotic separation requirement; P1 remains `r(phi_pair)=R_w[1-exp(-2 phi_pair/n)]` with no frozen map to `(R,a,q,x_endpoint)`. See [G76 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11/EXACT_DERIVATION.md:73), [Xmax STATUS_AND_WORKFLOW.md](/tmp/udt_g78_review_I5y4y7/udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md:8), and [SNe EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_sne_native_observer_query_replay_2026-08-11/EXACT_DERIVATION.md:38).

- Source congruence: exact `D C_src(D) D^T = C_obs`; my 256-case replay reproduced `max_relative = 2.188160128020986795e-14` and `min_source_eigenvalue = 1.297799791027531846e-02`. The scoped claim remains valid only on the invertible-response stratum and is not promoted to a continuum theorem. See [G69 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11/EXACT_DERIVATION.md:67), [G70 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G70_query_owned_restriction_atlas_2026-08-11/EXACT_DERIVATION.md:44), and [G73 TOPOLOGY_SCOPE_CORRECTION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G73_global_sky_source_sensitivity_atlas_2026-08-11/TOPOLOGY_SCOPE_CORRECTION.md:18).

- Route ledger reproduced as written: `4 OPEN_NO_OWNER`, `1 COMPATIBILITY_ANCHOR_ONLY`, `1 NECESSARY_REQUIREMENT_ONLY`, `1 CONDITIONAL_IDENTIFIABILITY_ONLY`, `0 OWNED_NATIVE`. See [G78 EXACT_DERIVATION.md](/tmp/udt_g78_review_I5y4y7/udt_cmb_G78_profile_endpoint_source_owner_join_2026-08-11/EXACT_DERIVATION.md:127).

**Caveats**

The surviving landing is bounded to the frozen 20-source universe plus the stationary-axial finite-mesh G75-G77 family. It is not a continuum injectivity theorem, not a generic UDT no-go, and not a proof that no future same-geometry cross-query can own endpoint/scale or source selection.

**Smallest next calculation**

Derive one same-geometry dimensional SNe query on the already-fixed G75/G77 control/query, returning `phi_pair` and `d_A` or `d_L` for a single realization, before any P1 comparison or family fit. That is smaller than a full cross-query atlas and is the first calculation that could directly pressure the open endpoint/scale route.