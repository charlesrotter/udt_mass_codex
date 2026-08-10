**Findings**
- [verify_integrability_independent.py](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/verify_integrability_independent.py:21) overstates its independence: it hard-codes the bracket and leaf-metric coefficients at lines 35-41 instead of deriving them from the coframe and Maurer-Cartan data. That weakens the package’s local evidence-gate wording, but not the landing itself.
- Terminology should be tightened. In 4D, `H` is load-bearingly a nonintegrable rank-two normal bundle; “contact” is accurate only in the weaker “contact-type on each `S^3` slice” sense, not as a literal 4D contact structure. The real point is the unavoidable `e1` term in `[e2,e3]` in [package derivation](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:107).

**Landing**
Accept, but only at the bounded conditional strength already intended by [AUDIT_REPORT.md](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/AUDIT_REPORT.md:19) and G46 in [CURRENT_SCIENTIFIC_PREMISES.tsv](/tmp/udt-r17-foliation-review-20260810-AiqqlV/CURRENT_SCIENTIFIC_PREMISES.tsv:47):

`GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN`

I do not find a manifested-source refutation of the foliation claim. I do reject any stronger reading that would promote it to branch selection, a universal pair map, a common connecting pair surface across leaves, path-independent normal carry, or carried-to-intrinsic reset closure; those remain open in the package and upstream gates [package derivation](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:179), [magnitude selection report](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_magnitude_to_grading_selection_audit_2026-08-10/AUDIT_REPORT.md:23), [pair-map atlas](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_calibrated_pair_map_owner_atlas_2026-08-09/EXACT_DERIVATION.md:259), [finite-cell reduction](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27/EXACT_DERIVATION.md:150).

**Independent Algebra**
1. From the manifested coframe `theta0=u^-1(dt+a sigma3)`, `theta1=u sigma3`, `theta2=v sigma1`, `theta3=v sigma2`, the dual frame is
   `e0=uT`, `e1=u^-1(Z-aT)`, `e2=v^-1X`, `e3=v^-1Y`, so `E=span(T,Z)` and `H=span(X,Y)` [package derivation](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:45), [twisted-S3 witness](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/EXACT_DERIVATION.md:34).

2. Using `[fA,gB]=fg[A,B]+fA(g)B-gB(f)A`, stationarity `T(phi)=0`, and Maurer-Cartan `[X,Y]=2Z`, `[T,Z]=0`:
   ` [e0,e1]=-(Z(u)/u)T=-(p1/u)e0`, so `E` is involutive.
   ` [e2,e3]=2v^-2 Z + (lambda p3/v)e2 -(lambda p2/v)e3 = 2a/(uv^2)e0 + 2u/v^2 e1 + ...`, so `H` is not involutive because `2u/v^2 != 0`.
   If the Maurer-Cartan sign convention is reversed, these coefficients flip sign, but closure of `E` and nonclosure of `H` do not.

3. Since `T` and `Z` are complete commuting fields on `R x S^3`, and nonzero left-invariant `Z` generates a free `S^1` action on `S^3` with quotient `S^2`, the maximal `E`-leaves are `R x S^1`. Because the metric owns only the unoriented ruler line, it owns the leaf family, not a preferred orientation, winding, or chosen leaf [package derivation](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:120).

4. On any such leaf, `sigma1=sigma2=0`, `sigma3=dpsi`, hence
   `h00=-u^-2`, `h01=-a u^-2`, `h11=u^2-a^2u^-2`, `det h=-1`.
   Therefore `(-det h)/h00^2=u^4` and the banked terminal formula gives `phi_pair=(1/4)log(u^4)=phi` [package derivation](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_r17_intrinsic_pair_foliation_integrability_audit_2026-08-10/EXACT_DERIVATION.md:140), [terminal evaluator](/tmp/udt-r17-foliation-review-20260810-AiqqlV/udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/EXACT_DERIVATION.md:80). This justifies `delta_K=phi(q)-phi(p)` as a global endpoint coboundary from the shared Killing state, but not as a common connecting pair surface across different leaves.
