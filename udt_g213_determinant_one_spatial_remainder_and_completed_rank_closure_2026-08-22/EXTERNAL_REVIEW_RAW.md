**Landing**

`G213_REQUIRES_REPAIR_BUT_BOUNDED_LANDING_SURVIVES`.

The authorized scope hash matches the registered value (`bab22cbfe6bf1c789ba3629b1a9478e7931a83ad7a392080fc01043418932751`), all 34 review-manifest payload hashes match, and all 12 frozen-source hashes match: [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:1), [SOURCE_MANIFEST.tsv](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/SOURCE_MANIFEST.tsv:1), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:1).

**Scientific defects**

No bounded scientific defect was established.

Within the stated ceiling, the five-mode landing survives. The determinant-one spatial remainder is correctly typed as a tracefree self-adjoint `3x3` spatial log with a unique `1+2+2` split into one grading, two radial-screen mixing, and two screen-shape coordinates [EXACT_DERIVATION.md](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EXACT_DERIVATION.md:19). A no-dependency rank check on the explicit coefficient map gives full rank `5`, while the G207+G208 columns give rank `4`, matching the stated missing coordinate. G207 really is the two screen-shape directions [EXACT_DERIVATION.md](/intake/udt_g207_g205_tracefree_screen_timelive_robustness_2026-08-21/EXACT_DERIVATION.md:28), and G208 really is the two radial-screen mixing directions [EXACT_DERIVATION.md](/intake/udt_g208_g205_radial_screen_mixing_robustness_2026-08-21/EXACT_DERIVATION.md:29); no combined commuting history is warranted [EXACT_DERIVATION.md](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EXACT_DERIVATION.md:168).

The completed-pair claim also survives, conditionally on the explicit G176 working clarification that `m` belongs to the typed relation state [EXACT_DERIVATION.md](/intake/udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md:12). The identities `h_s=J^{-T}h_sigma J^{-1}` and `h_sigma=J^T h_s J` are lawful with `J=diag(1,m)` [EXACT_DERIVATION.md](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EXACT_DERIVATION.md:188), so the G129 six-plane rank-ten witness transfers locally and exactly, but only for supplied known germs; it does not prove physical germ population or stronger global selection [EXACT_DERIVATION.md](/intake/udt_g129_copresent_relational_network_faithfulness_2026-08-16/EXACT_DERIVATION.md:74), [EXACT_DERIVATION.md](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EXACT_DERIVATION.md:227). The density-deletion counterfamily is real: dropping `m` makes the normalized completed metrics blind to the spatial rescaling family while the ambient metrics remain distinct.

**Packaging defects**

The preregistered no-write replay does not currently run as packaged in this sealed environment. Executing the registered command from [REPLAY_COMMAND.txt](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/REPLAY_COMMAND.txt:1) fails because [verify_package.py](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/verify_package.py:37) invokes [derive_spatial_remainder_and_rank.py](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/derive_spatial_remainder_and_rank.py:6) and [run_catch_proofs.py](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/run_catch_proofs.py:9), both of which require unavailable `sympy`. That is a packaging/runtime defect, not a refutation of the bounded science.

There is also a certification overstatement in [EVIDENCE_GATES.md](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/EVIDENCE_GATES.md:7). The claimed “separate exact-Fraction census and row reduction” is not what the actual no-dependency independent script does: [verify_completed_rank_independent.py](/intake/udt_g213_determinant_one_spatial_remainder_and_completed_rank_closure_2026-08-22/verify_completed_rank_independent.py:72) independently verifies the completed-tuple roundtrip, density-blind counterfamily, and G129 rank-ten reconstruction, but it does not independently replay the `1+2+2` mode census or G207/G208 four-of-five provenance.

**Required repairs**

- Make the registered replay actually self-contained in the sealed environment: vendor `sympy`, declare/enforce it, or replace the symbolic pieces with dependency-free exact linear algebra.
- Either add a true independent no-dependency verifier for the five-mode census and G207/G208 four-of-five coverage, or narrow the evidence-gate wording to rank-bridge-only independence.
- Keep the bounded claim wording conditional on the supplied split, reference metrics, known germs, and G176 working clarification.

The preregistered G213 scientific landing survives in bounded form: five determinant-one spatial coordinates, G207+G208 cover four, `m` is essential, and the completed tuple preserves the G129 local rank-ten witness. The preregistered replay/certification package does not fully survive until those repairs are made.
