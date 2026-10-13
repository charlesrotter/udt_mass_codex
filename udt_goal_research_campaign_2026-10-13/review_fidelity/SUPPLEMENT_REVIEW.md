# GRC1 fidelity review — A supplement

2026-10-13. Actual researcher_a/SUPPLEMENT.md, corrected check implementation,
preserved initial implementation, failed stdout/stderr and passing normalized
stdout/capture have now been inspected. This follows INITIAL_FINDINGS and is
still before sibling-review exposure. No additional scientific process was
needed: the load-bearing additions admit short independent analytic checks.

**VERIFIED-WITH-CAVEATS conditional supplement.** No substantive objection to
the displayed arguments under their explicit hypotheses. This verdict neither
adopts the sign/comparison/completeness assumptions nor transfers full review to
unseen central text.

1. Differentiate `D_e=r_e r int(ds/r²)` directly. The two cross-derivative terms
   cancel, leaving `D_e''=(r''/r)D_e`; the vertex derivative is1. Reversing the
   integration limits makes the endpoint propagator antisymmetric for arbitrary
   r''. This establishes the claimed limited optical reciprocity and explains
   why it cannot enforce NAR. For `r=e^(H lambda)/H`, direct elementary
   integration gives `(e^(H delta)-e^(-H delta))/(2H)`; its derivative equations
   and nonzero tide follow without the producer simplifier. Endpoint angular
   launch factors are proportional to the separately normalized frequencies.
   The resulting reciprocal map ratio Z is not a second future clock exchange,
   brightness law or finite-angle beam theorem.
2. Setting the conformal exponent to `-log psi` in the standard Ricci identity
   gives the supplement's expression; the gradient-square terms cancel in the
   null contraction, leaving `Ric_g(k,k)=Ric_0(k,k)+2psi''/psi` along a
   REFERENCE-affine null ray. The matched difference contains
   `Ric_0(Ik,Ik)=psi^-2 Ric_0(k,k)`. Zero reference null Ricci is precisely what
   removes that otherwise nontrivial reference term. The S boost limit then
   gives concavity, not convexity. For any nonzero tangent slope a globally
   positive concave function on R has an upper tangent line becoming negative
   at one end, a contradiction. Constancy on all complete reference null rays
   kills dpsi on the entire null cone and hence on the full tangent space.
   Connectedness gives one constant. This is necessary, not a sufficient full-S
   theorem for curved reference, and does not set the constant to1.
3. In the slab example, integrating `dt/deta=sec(H eta)` gives the stated cosmic
   time and `a=cosh(Ht)`. The electric/spatial sectional entries give
   `C=H²+(H²/cosh²(Ht))|m|²`, so the control checks full directional S rather
   than only null Ricci. Spatial translation conservation gives the stated
   timelike/null time derivatives. Since a>=1 on all real t, proper/affine
   lengths diverge at both ends and finite-t continuation has bounded
   velocities. The physical geometry is causally geodesically complete while
   its reference slab is null incomplete. It is therefore a valid adverse
   control against replacing reference completeness by physical completeness.
   No spacelike-completeness or finite universal-redshift theorem is needed.

The supplement's original failed comparison is a genuine preserved failed
automatic assertion. The implementation diff only rewrites the same sinh
residual in exponentials and records the zero result. The elementary derivation
in item1 independently verifies why that repair is legitimate. The final
capture is a successful19-group author check in1.2435s,50808KiB maximum RSS;
it is not nineteen independent proofs or a generic-psi computation. I did not
rerun the author implementation.

Primary-source access: [Folkestad–Hernandez-Cuenca](https://arxiv.org/pdf/2106.09037),
v1, equations2.2–2.3 and3.1, supplies the conformal transformation, but its
nonnegative-curvature focusing theorem has the opposite inequality and is not
invoked here. [Korzyński et al.](https://arxiv.org/html/2405.05105v1), optical
map reciprocity discussion and sectionV.4, supplies method context; the scalar
formula above is independently proved. [Gover–Nurowski](https://arxiv.org/html/math/0405304),
section2.2, was checked for the conformal Weyl weight used in coordinator C2;
their conformally-Einstein obstruction theorem is not used. No imported energy
condition, matter field or GR dynamics has entered this review.

The supplement improves the campaign's physical discrimination: reciprocal
optics does not select F/NAR, and preserving null paths introduces a separate
global comparison-domain choice. The causally complete cosh control is useful
as that adversarial boundary example, not a recommendation for an arbitrary
supplied cosmology. The next physical question remains attribution and the
admissible optical sign/comparison structure; the supplement does not answer it.
