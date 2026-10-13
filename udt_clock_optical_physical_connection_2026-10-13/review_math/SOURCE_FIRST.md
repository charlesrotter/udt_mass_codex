# COC1 mathematical review — source-first checkpoint

Status: independent source-first argument, saved before COC1 candidate/proof/code/output or sibling-review exposure. This is not final review attestation or physics adoption.

Reviewer: `/root/coc_review_math`, fresh separate context, inherited model/runtime (no separately exposed exact model identifier; same model as coordinator, not different-model or human review). Parent startup/synchronization/full406 pass are attributed to the coordinator. Locally checked branch `grok`, HEAD `1fca5f6962169b680d7726564a3a62f95ee0277a`; status displayed the campaign plus LIVE/HANDOFF edits and unrelated names, whose payloads were not opened. No Git mutation or global verification. The specified central sources were read at their retained grades. In particular GRC1's prior null-screen algebra and PCC1's reference-Bianchi caveat were visible; the new clock-duration derivation and two-boost argument below were reconstructed here. No claim of total ignorance of earlier mathematics.

## 1. Scope and supplied choices

Smooth time-oriented Lorentz4 metric, signature -+++, curvature convention R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]. At p let U be unit future timelike, n unit spatial, k=U+n and e=A(n,U,U,n), with A(X,Y,Z,W)=g(R(X,Y)Z,W). The central geodesic is A(tau), p=A(0), q=A(2l). Null generators are source-normalized by -g(k,U)=1. Their affine parameter is a calculation device, not the proposed measured distance. Initial direction/solid angle is in the emitting rest frame. Each relay is the regular intersection of that generator and the past null cone of q; the two-surface carries its induced metric. This requires a sufficiently small regular convex chronological neighborhood, no caustics, and the direct branch. Relays and rulers are ideal geometric queries, not a demonstrated material apparatus.

The metric/clock/null interface is pinned to W4's working scope and R6. Choice of this experiment is free-and-explored, not pinned by a native selection law. c_E=1 is clock/ruler unit conversion; its observed value supplies no curvature coefficient, new speed or source equation. Neither photon flux nor a maximal spatial hypersurface is needed. No preferred population, field equation, physical reference, additional physical source, or scalar attribution is silently selected.

## 2. Actual directional cut from two-point geometry

Use Riemann normal coordinates at p, so q=2l U and x=lambda k exactly along the outgoing affine null geodesic. The quartic expansion of squared geodesic distance between x and q is

    2 sigma(x,q) = 4l(lambda-l) -(4/3)l² lambda² e + O(l^5),

uniform on the compact sky for a fixed U, with lambda=O(l). The sign follows by expanding the normal-coordinate metric along the zeroth-order straight segment; endpoint variation of its flat action vanishes, so path bending contributes only above quartic order. The curvature term is -A(x,q,q,x)/3. Solving the regular rescaled incidence equation gives

    lambda_*(U,n,l) = l + e l³/3 + O(l^4).

The normalized vertex Jacobi map on the outgoing cone is

    J(lambda) = lambda Id - lambda³ Q_k/6 + O(lambda^4),
    Q_k(x,y)=A(x,k,k,y),

and its determinant is lambda²[1-lambda² Ric(k,k)/6+O(lambda³)]. Angular variation of lambda_* adds a multiple of the generator to each cut tangent. These multiples have zero inner products with all cone tangents, so they do not alter the induced two-metric. Consequently the actual source-angle area density is

    a(U,n,l) := (dA/dOmega_source)/l²
              = 1 + l² alpha(U,n) + O(l³),
    alpha(U,n) = (2/3) A(n,U,U,n) -(1/6) Ric(U+n,U+n).

This is not the fixed-affine-cut coefficient. Dropping the e-dependent change of cut changes the observable. Also no argument has restricted the ray to a totally geodesic 2D surface: normal-coordinate incidence and the two-screen Jacobi map are fully four-dimensional.

For fixed U, rescale coordinates and lambda by l. The flat incidence derivative in lambda/l is nonzero; smooth dependence/implicit function and Jacobi ODEs support the stated remainders uniformly over the compact source sky. The constants depend on bounded local metric jets and the prepared frame/regularity domain. This is an asymptotic statement, not a supplied finite-error constant. No uniformity over unbounded boosts follows. Curvature can be evaluated at p; replacing it by its value at the midpoint changes only the O(l³) normalized remainder. An improved midpoint/even-order remainder would require a separately stated symmetry/regularity argument; it is not needed here.

## 3. Integrated area loses the directional data at this order

Average over n using <n_i>=0 and <n_i n_j>=delta_ij/3. Since tr T=Ric(U,U) and sum_i Ric(e_i,e_i)=R+Ric(U,U),

    <Ric(U+n,U+n)> = (4/3)Ric(U,U)+R/3,
    <alpha> = -R/18,
    Area(p,q) = 4pi l²[1-R(p)l²/18+O(l³)].

Thus this experiment offers another geometric scalar-curvature readout; CMF1 already reconstructed total R from prepared clocks. It is not a first reconstruction, and different source-frame total areas have the same leading scalar coefficient. They can differ at higher orders.

After independently obtaining this result I inspected Gibbons and Solodukhin, *The Geometry of Small Causal Diamonds*, arXiv:hep-th/0703098v3, section 3, Eq. (29): their duration tau=2l gives the same area correction. Their section 2 uses sufficiently close tips and a unique connecting timelike geodesic; the paper's later Einstein-equation interpretation is not an input here. Its de Sitter and Einstein-static exact areas also confirm the sign. Source: https://arxiv.org/pdf/hep-th/0703098 (version shown 12 Aug 2015). This bibliographic agreement is separate from the source-first derivation, not an independent apparatus or UDT law.

## 4. Two different sign proposals

Supply matched g,g0, time-oriented tangent isometry, source clocks, units, proper half-duration and direct protocol. Pull both curvature tensors into the same Lorentz tangent space; write D=A-I*A0 and S=Delta Ric. The leading normalized directional area contrast is

    delta alpha(U,n) = [4D(n,U,U,n)-S(U+n,U+n)]/6.

The leading logarithmic ratio gives the same coefficient. Comparisons without the physical matching data are not defined by coordinate equality.

**Integrated proposal:** nonpositive leading total-area contrast, even for every U, is merely Delta R>=0. It does not imply Einstein Ricci, constant sectional curvature, all-direction signs, or a source decomposition. Total-area frame repetition adds no pointwise leading information.

**Directional proposal:** suppose delta alpha(U,n)<=0 for EVERY future unit U and EVERY unit n perpendicular to U. This alone implies D=kappa B with kappa>=0; the converse holds. Here B(X,Y,Z,W)=g(Y,Z)g(X,W)-g(X,Z)g(Y,W).

Proof using two separate finite-boost families, after each frame's l->0 limit:

1. Fix orthonormal u,v and boost both in their plane: U_eta=cosh eta u+sinh eta v, n_eta=sinh eta u+cosh eta v. The timelike sectional contraction D(n_eta,U_eta,U_eta,n_eta) is constant, while U_eta+n_eta=exp(eta)(u+v). Let eta->+infinity in 4D-S(k_eta,k_eta)<=0. This forces S(k,k)>=0 for every null k.
2. Fix k=u+v and a unit screen vector x perpendicular to u,v. Keep n=x and boost only U_eta in that plane. Divide the same inequality by exp(2eta)/4 and take the limit: 4Q_k(x,x)<=S(k,k), where Q_k(x,x)=D(x,k,k,x). Summing over two screen directions yields 4S(k,k)<=2S(k,k). Together with step 1, S(k,k)=0. Therefore Q_k is negative semidefinite with zero trace and is identically zero.
3. For null u+/-v and x perpendicular to them, Q=0 implies D(x,u,u,x)=-D(x,v,v,x), and the odd cross contraction vanishes. Interchanging spatial x and v shows equality of electric diagonal entries in each frame; allowing rotations gives an isotropic electric form. Any two timelike frames share a positive two-plane, whose sectional value fixes the same isotropic coefficient. Subtract kappa B: every timelike sectional contraction vanishes. Polynomial continuation from timelike vectors, polarization and algebraic Bianchi annihilate the full remaining tensor. The original inequality then reads -4kappa<=0, so kappa>=0. Conversely such D has S=3kappa g and delta alpha=-2kappa/3.

This does not require importing GR or adding the old S and F proposals as separate premises; it is an algebraic consequence of the new, stronger directional area-sign trial. The trial remains UNADOPTED. No finite list of boosts establishes its universal quantifier. No fixed nonzero l can be passed through these unbounded-boost limits using the local remainder alone. With kappa=0 the leading contrast vanishes and finite signs remain undetermined.

## 5. Controls, contamination and precision

Minkowski gives exactly a=1 for the stated inertial clock. In constant sectional curvature K>0, the geodesic-center de Sitter cut has areal radius tanh(sqrt(K)l)/sqrt(K), hence alpha=-2K/3, agreeing with T=-K and Ric(k,k)=0. For the ultrastatic product -dt²+h_K, the cut radius is spatial proper radius l and area density sin²(sqrt(K)l)/K, so alpha=-K/3; total R=6K but this metric is not Einstein for K!=0. Thus scalar area does not classify geometry.

A sharper anisotropic control is dS2(K) times Euclidean2. At a symmetric event, for n_x the component in the curved spatial factor, T(n,n)=-K n_x² and Ric(k,k)=K(n_x²-1), so alpha=K(1-5n_x²)/6. Its integrated coefficient -K/9 is negative, yet the transverse directional coefficient is positive. A separate original-geodesic/induced-cut check is planned below, rather than another contraction loop of this formula.

Central acceleration is a real contaminant. In flat spacetime for a uniformly accelerated clock with proper acceleration magnitude a, the exact source-normalized affine cut is

    lambda_*(n,l) = sinh(al)/[a(cosh(al)-n_x sinh(al))].

This follows directly from q=A(2l), x=lambda(U+n) and (q-x)^2=0. Consequently

    a(U,n,l)=1+2a n_x l+a²(3n_x²-2/3)l²+O(l³),
    Area/(4pi l²)=1+a²l²/3+O(l^4).

The first directional contamination is linear, and even angular averaging leaves an acceleration-squared term at curvature order. Therefore free central motion (or a controlled removal) cannot be omitted. Likewise relay delay, angular calibration, finite patches, caustics and protocol mismatch change the observable.

For measured normalized density error epsilon(l), coefficient extraction has error epsilon(l)/l² plus the O(l) truncation remainder, so epsilon=o(l²) is sufficient in an ideal limit. Absolute area-density error must instead be o(l^4). A proper-duration error delta l contributes at order delta l/l to the normalized density: without cancellation/control require delta l=o(l³) to extract the coefficient. Angle and frame errors need comparable calibrated bounds. Fixed readout noise is not cured by taking l->0. No instrument/noise budget is proved.

## 6. Scalar data and physical attribution

Measuring total R, or even the full Riemann tensor, does not distinguish its physical causes without an admitted assignment. Algebraically Riemann splits into Weyl, trace-free Ricci and scalar parts; identifying its scalar piece with an additional positional cause is an extra physical interpretation. GR comparison controls illustrate the distinction: Ricci-flat Schwarzschild has nonzero Weyl and tides with zero total scalar; Einstein metrics can retain Weyl; trace-free GR sources can have R=0 but nonzero Ricci; and the GR traced field equation would mix scalar curvature with matter trace and a cosmological term. Such equations remain comparison-only here, not native UDT premises.

Pointwise D=kappa B implies Delta Ric=3kappa g, Delta R=12kappa and Delta Weyl=0. It constrains the difference, not total constant sectional curvature. With a smooth regional event/tangent matching and S0=I*Ric[g0], physical contracted Bianchi supplies only

    3 d kappa=div_g S0 -(1/2)d tr_g S0.

The reference connection's identity cannot be subtracted as if it were the physical connection's identity. In particular arbitrary matched reference differences need not have constant kappa. With Einstein reference Ric[g0]=Lambda0 g0, constant Lambda0, the right side vanishes and kappa is constant on each connected regular region. Total Einstein Ricci still permits nonzero Weyl. With flat reference the full difference theorem does give total constant sectional curvature; that conclusion uses the flat reference as a real extra choice. None identifies the source, scale, sign premise, reference or positional meaning physically.

No candidate verdict is issued at this checkpoint. Next: finish the predeclared direct geometric control, save the exact source pins/check artifacts, then request the candidate for adversarial inspection.
