# PC2 candidate — an invariant local recipe class from complete initial data

UNPROMOTED CONDITIONAL CANDIDATE; fresh direct review pending.
PC2-PARALLEL, PC2-RECIPE, PC2-INITIAL-SCALAR.
Dependencies: reviewed PC1 at2112f808 with REVIEW_RECORD/direct review, and
unchanged G312/G313/G303/G315/G321/G335/G355/G358 scopes. All owner-provisional
stamps and CHOSEN recipe limitations remain. This is NOT generic persistence
from arbitrary pointwise recipe compatibility.

## 1. Hypotheses and the explicit PDE-method condition

Let (M,g) be an ACTUAL smooth time-oriented four-dimensional Ricci-flat
development, with a smooth spacelike patch Sigma and a smooth future nonzero
null section ell=f n+Y satisfying PC1's FULL spatial-parallel equations.
In the PC1 route, Lambda0 is forced jointly by that seed class and the old
nonzero-real-root domain. It is not selected for the whole UDT arena.

Use the following standard mathematical method CONDITIONALLY:
local smooth existence and uniqueness for a linear normally-hyperbolic
connection wave system on a finite-rank vector bundle, with arbitrary smooth
Cauchy value and normal derivative on a spacelike patch. This is a method
import, not a new UDT law, field equation, physical premise or metric solve.
G303/G315/G321 explicitly retain conditional hyperbolic-method ceilings; their
compact registered examples do not themselves prove this general auxiliary
theorem. Our conclusion retains this explicit method hypothesis.

Its application is local: shrink to a precompact spatial ball and sufficiently
small regular Gaussian slab, then its domain of dependence. The metric is
smooth, gamma positive definite with positive lower bound on that compact
closure, the principal matrix is the Lorentzian metric times bundle identity,
and all connection/curvature lower-order coefficients are smooth and bounded
there. No physical timelike boundary data are added. Local auxiliary smooth
extensions used to apply a Cauchy theorem agree on the common domain by causal
uniqueness; they are not physical metric extensions or global completion.

The usual uniqueness estimate applies using ANY auxiliary positive definite
bundle norm (not the indefinite Lorentzian fibre norm). Reducing to components,
the wave system has energy controlling field, time derivative and spatial
gradient. On a sufficiently fast shrinking coordinate ball the boundary flux
is nonpositive, and bounded smooth coefficients give E'(t)<=C E(t). Zero
initial data imply zero energy by Gronwall, in both time directions. This
explains the uniqueness mechanism; no finite numerical check is a proof of
the general local existence theorem.

## 2. A genuine propagation equation (PC2-PARALLEL)

Write F_ab=R(e_a,e_b) as the curvature endomorphism of TM, with PC1/G358's
R=nabla_a nabla_b-nabla_b nabla_a-nabla_[a,b] convention. For an arbitrary
smooth vector V, put A_a=nabla_a V and Box=nabla^a nabla_a. The COMPLETE
bundle identity is

    Box A_a = nabla_a(Box V)
               +2 F^m{}_a A_m+Ric_a{}^c A_c
               +(nabla^m F_ma)V.                                 (1)

To see every term, first use nabla_m A_a=nabla_a A_m+F_ma V.
Apply nabla^m. Commuting nabla^m with nabla_a on the TM-valued covector A_m
produces one F^m{}_a A_m and +Ric_a{}^c A_c from its lower m slot.
Differentiating F_ma V produces the second F term and its divergence.
This proves(1) as a tensor identity with no missing derivative-curvature term.

For Ricci-flat g, contracted differential Bianchi gives nabla^m F_ma=0,
and Ric_a{}^c=0. Hence, if Box V=0,

    Box A_a=2 F^m{}_a A_m.                                        (2)

This is a closed homogeneous linear wave system for A. It does not discard
curvature; its algebraic action on A is present. The derivative-curvature
source vanishes by the ACTUAL equation/Bianchi, not by component inspection,
an approximate zero, a special wave profile, or a chosen future field.

Use the declared linear-wave method to construct V with

    V|Sigma=ell,    (nabla_n V)|Sigma=0,    Box V=0.                (3)

The second datum is the necessary value for a parallel extension, not an
independently populated physical normal field. We must prove the result, not
assume the whole extension is parallel. Spatial seed equations and(3) give

    A|Sigma=0                                                    (4)

as a FULL TM-valued covector, including the normal slot.

For tangent X, the commutator yields, on Sigma,

    (nabla_n A)(X)=(nabla_X A)(n)+R(n,X)ell=0.                    (5)

The first term vanishes because the entire tensor A is zero along Sigma.
The curvature term vanishes by reviewed PC1's FULL ambient annihilation on
its Lambda0 spatial-seed class. Differentiating an identity only at a point
would not suffice; the initial seed is smooth on an open patch.

Finally Box V=trace_g(nabla A)=0, and all tangential derivatives of A vanish
on Sigma by(4). In an orthonormal normal/spatial frame this leaves

    (nabla_n A)(n)=0.                                            (6)

Connection/frame derivative terms multiply A=0; none is silently omitted.
Equations(5)-(6) give the FULL zero initial normal derivative of A.
Uniqueness for(2) therefore forces A=0 on a smaller local domain.
Thus V is genuinely parallel, agreeing with ell, and is future-null/nonzero:
parallel transport preserves norm and nonzeroness, and continuity preserves
the supplied future component. A parallel extension is unique on this
connected local domain for its initial seed. No finite-jet induction is used.

The nonzero-Lambda seed counterbranch is not a counterexample to this proof:
it fails PC1's full root gate, and its R(n,X)ell term in(5) need not vanish.
Likewise a general root-compatible metric without the spatial seed does not
have the zero A-data in(4), and is outside this sufficient theorem.

## 3. Full root, recurrence and current (PC2-RECIPE)

Now, and only after(2)-(6), V is parallel in an ambient neighborhood.
Commuting its derivatives gives R(A,B)V=0 for all directions there. Apply
PC1's algebraic Ricci-flat conclusion at EACH event, using any local future
unit observer to normalize V: the old full Weyl/first-dual B is either zero
or a positive fourth power along V-flat. On its nonzero region, the
future-raised root is unique and smooth:

    beta=b V-flat,   b>0.                                       (7)

Smoothness follows directly from the old smooth timelike-extractor formula
on its positive denominator; its resulting root is observer-independent
on this full type domain. Equation(7) is the original fixed B root, with
its prescribed normalization, NOT an arbitrary rescaled phase.
Changing the auxiliary parallel seed by constant c>0 changes V to cV and
b to b/c, leaving B,beta,alpha,q_rec and D below unchanged.

A parallel V is Killing, so its local flow preserves g, orientation and B.
It therefore preserves the UNIQUE future beta. Since nabla V=0, the Lie
derivative of beta equals nabla_V beta, and(7) implies V(b)=0.
Consequently

    nabla beta=alpha tensor beta,   alpha=d(log b),  alpha(V)=0,
    q_rec=g^-1(alpha,alpha)>=0,
    C0=beta#=bV,                  D=q_rec bV.                     (8)

The recurrence is now FULL, including its normal derivative. Uniqueness of
alpha follows from beta!=0. Its nonnegativity follows because the annihilator
of a null V has a positive-semidefinite inverse-metric form with radical
span(V-flat). In an adapted orthonormal frame, alpha0=-alpha3, so
q_rec=alpha1^2+alpha2^2. Thus, pointwise,

    q_rec=0  iff alpha is proportional to V-flat
             iff d beta=alpha wedge beta=0.                    (9)

Closure on an open set requires these pointwise zeros throughout that set.
Alpha may be nonzero and null; closed beta is not automatically parallel.

Since the V flow preserves g,b and alpha, it preserves q_rec too:
V(q_rec)=0. Therefore the complete covariant equations are

    div C0=0, nabla_C0 C0=0,
    div D=0,  nabla_D D=0.                                      (10)

For example div D=V(q_rec b)+q_rec b div V=0; the acceleration has
V(q_rec b)V and nabla_V V factors, both zero. These statements include the
zero-current branch, but a positive ray-intensity construction requires
q_rec>0 separately. Neither conservation nor(10) proves a phase-independent
product or identifies physical carried content.

Because V is transverse to Sigma, its flow is locally a diffeomorphism
from an interval times a smaller initial patch onto a neighborhood. On this
flow tube, nonzero B and q_rec>0 (or q_rec=0) transport from the initial
point exactly: the flow is an isometry and b,q_rec are invariant. This is
stronger than a finite sampled sign test, but remains a LOCAL tube theorem.
There is no uniform lifetime over a family, global no-caustic/completeness
result, or robustness to perturbations leaving the spatial-seed class.
No continuation through initially zero B is supplied by the nonzero recipe.

## 4. Which initial derivatives are supplied and which are fixed
(PC2-INITIAL-SCALAR)

PC1 supplies beta|Sigma=b ell-flat with b>0. Put a=d_Sigma log b.
Since V|Sigma=f n+Y and V(log b)=0, the previously unresolved normal value is

    n(log b)|Sigma = -a(Y)/f,
    alpha|Sigma = a+[a(Y)/f] n-flat,
    q_rec|Sigma = |a|_gamma^2-[a(Y)/f]^2 >=0.                    (11)

Here the spatial extension of a annihilates n. Equation(11) is the squared
projection of a onto the two-plane orthogonal to Y. It is computed from
the smooth complete initial data and their spatial derivatives after the
proved propagation; an arbitrary extra normal recurrence derivative would
violate the equation. It is NOT an added physical constraint selecting all
input data uniquely. Smooth metric data include their higher spatial jets;
the equation and actual development supply the related ambient curvature.

For the PC1 harmonic graph, gamma=diag(L,1,1), f=L^-1/2,Y=-X_u/L.
With b=b(u,x,y), the a_u^2/L contributions in(11) cancel, giving exactly
q_rec=(b_x^2+b_y^2)/b^2, including variable u-normalization.
Thus positive q initially is an explicit additional NONZERO-domain condition
on these supplied data. It is preserved on the V-flow tube by(8)-(10), not
generated if absent. On q_rec>0, the ORIGINAL root cannot also equal dTheta.
A separately normalized aligned phase is a distinct later query.

## 5. Actual checking, discovery and ceiling

check_commutator.py computes all16 components of(1) from direct covariant
differentiation on the OFF-EQUATION control g=(t^2+2)^2 eta with a generic
polynomial V. All match exactly; Ricci/curvature-gradient/divergence-curvature
terms are genuinely active. Three actual omissions each leave nonzero
residuals. This off-equation identity control is not an admitted-metric
counterexample or a simulated UDT development.
The first exploratory control g=(t+2)^2 eta had identically zero curvature
divergence and failed the explicit activity guard. Its original code and
failure are preserved; only the freely explored diagnostic metric changed.
No premise/equation, tolerance or frozen candidate was repaired.

check_recipe_data.py gives11 grouped exact controls for(11), null/screen
algebra and the already admitted harmonic recurrence/current identities.
Actual free-normal and omitted-projection mutations fail. The stereographic
unit-vector control excludes one coordinate pole; the analytic cross-product
identity covers all unit vectors. These are implementation support, not a
proof of(2)-(6), PDE existence or generic geometric classification.

The conditional linear-wave proof, the full initial derivative argument and
the pointwise algebraic root theorem bear the quantifiers. No observer,
carrier, physical count, source, population, scale, recipe coefficient,
physical premise, accepted grade, manuscript or canon is adopted.
No assertion that every compatible recipe datum satisfies the seed is made.
A useful remaining question is whether a separately supplied aligned phase
and ONE fixed-label product compatible on the FULL initial slice persist
on this reviewed invariant class. Conservation alone has not answered it.
