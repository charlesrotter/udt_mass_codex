VERDICT

PASS-WITH-REQUIRED-REPAIRS

INDEPENDENT CHECKS

`verify_preregistration.py` passed exactly as claimed: 24 source files exist and both the SHA-256 and git-blob hashes match [verify_preregistration.py](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/verify_preregistration.py:1) and [PREREGISTRATION_VERIFICATION.json](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/PREREGISTRATION_VERIFICATION.json:1).

The non-importing verifier also passed in this environment and does reject the intended mutations [independent_verify.py](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/independent_verify.py:1) and [INDEPENDENT_VERIFICATION.json](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/INDEPENDENT_VERIFICATION.json:1).

I also checked the algebra from scratch without importing target code. For `n=e3` and `D_in=((1,2,0),(3,5,0),(7,11,0))`, I got `L2=209=tr S` and `L4=28=sum_ij(a_i b_j-b_i a_j)^2`. For a rank-one family `D_i n=q_i(2,-3,0)`, I got `L2=273>0` and `L4=0`. That independently confirms one projector identity and one rank-one countermodel.

The primary SymPy derivation did not replay here because the environment has `sympy 1.13.1`, while [requirements.txt](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/requirements.txt:1) pins `1.14.0`; [derive_reciprocal_closure.py](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/derive_reciprocal_closure.py:26) intentionally fails closed on version mismatch.

CLAIM-BY-CLAIM RULINGS

1. Claim 1: sustained. The scalar reciprocal channel is one-generator and Maurer-Cartan flat for smooth `phi`; the derivation in [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:3) is correct.

2. Claim 2: sustained. Ordinary Levi-Civita curvature is too generic to be a matter discriminator; this is consistent with the curved control in [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:22) and the full-holonomy obstruction in [udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md:64).

3. Claim 3: sustained. Current premises do not select a rank-one projector `P`; zero pointwise selector rank and holonomy obstruction are explicit in [udt_complete_coframe_native_selector_audit_2026-07-26/AUDIT_REPORT.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_complete_coframe_native_selector_audit_2026-07-26/AUDIT_REPORT.md:9) and [udt_metric_natural_joint_selector_nogo_2026-07-28/AUDIT_REPORT.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_metric_natural_joint_selector_nogo_2026-07-28/AUDIT_REPORT.md:123).

4. Claim 4: sustained. For supplied rank-one orthogonal `P`, the `L2` and commutator/area `L4` identities are correct. I confirmed them independently, and they match [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:37).

5. Claim 5: sustained with scope discipline. The ambient-versus-relative curvature distinction is stated correctly, and the report does keep open any selection of the relative term or subtraction convention [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:102).

6. Claim 6: sustained. The quartic uniqueness claim is properly bounded to the declared first-derivative, parity-even, rotation-invariant rank-one-blind class; outside that class the report explicitly lists counterfamilies [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:123).

7. Claim 7: sustained. Rank-one blindness and the need for both path and loop response are extra premises, not derived consequences; this is consistently recorded in [STATUS_LEDGER.tsv](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/STATUS_LEDGER.tsv:8) and [FALSIFICATION_OUTCOMES.tsv](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/FALSIFICATION_OUTCOMES.tsv:10).

8. Claim 8: sustained. Coefficient and scale nonselection are correctly stated; finite size does not fix `c4/c2` without an independent scale law [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:171) and this matches prior coefficient audits.

9. Claim 9: sustained. The `RP2` target, `S2` lift on simply connected compactified 3-domain, and Hopf statement are accurately scoped as conditional and non-selective [EXACT_DERIVATION.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/EXACT_DERIVATION.md:183), consistent with [native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md](/tmp/udt_reciprocal_closure_review.N4tNzC/native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md:107).

10. Claim 10: sustained. The package does not promote native carrier, action, matter, mass, boundary, dynamics, or bootstrap closure; the upstream source registry still marks these as `POSIT`, `WORKING`, or `OPEN` [CURRENT_SCIENTIFIC_PREMISES.tsv](/tmp/udt_reciprocal_closure_review.N4tNzC/CURRENT_SCIENTIFIC_PREMISES.tsv:5) and [CURRENT_SCIENTIFIC_PREMISES.md](/tmp/udt_reciprocal_closure_review.N4tNzC/CURRENT_SCIENTIFIC_PREMISES.md:24).

REQUIRED REPAIRS

[AUDIT_REPORT.md](/tmp/udt_reciprocal_closure_review.N4tNzC/udt_reciprocal_closure_joint_selector_audit_2026-08-01/AUDIT_REPORT.md:111): change the evidence bullet `24/24 exact SymPy 1.14.0 checks;` to `frozen RESULT.json records 24/24 exact SymPy 1.14.0 checks; replay requires the pinned SymPy 1.14.0 environment, while this payload also includes a passing non-importing independent replay via independent_verify.py;`. As written, the line reads as a present replay fact from the payload alone, but the primary script is not replayable in this environment without installing the pinned dependency.

MAXIMUM HONEST CONCLUSION

The payload supports a real conditional theorem: if a branch supplies a rank-one orthogonal projector reduction, then `L2` is exactly the projector path-strain norm and `L4` is exactly the relative loop-curvature/area norm, with quartic uniqueness only inside the declared rank-one-blind first-derivative class. It does not support stronger claims that UDT currently selects `P`, requires both terms, fixes their coefficient, or closes carrier/action/boundary/dynamics/bootstrap physics. I could not write this review to an output file because the sandbox is read-only and the payload does not specify a writable output path.