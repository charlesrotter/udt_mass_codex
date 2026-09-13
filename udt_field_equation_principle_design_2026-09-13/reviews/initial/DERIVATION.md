# FE1 mathematical content and physical boundary

Initial candidate argument. Standard local geometry applied to the proposed
response, not a new UDT theorem of physical ownership. Source pins control.
All statements below concern a smooth regular four-dimensional Lorentz metric
and a sufficiently small normal neighborhood of an arbitrary event p.

## 1. Intrinsic density and covariance

The metric defines a positive density dmu_g through sqrt(abs(det g)). It does not
require orientation. The tangent metric g_p defines a constant positive density
on T_pM. Pull back dmu_g by exp_p, divide by that constant density, and call the
positive smooth ratio D_p(v). Shrink the domain so exp_p is a diffeomorphism.
Then D_p(0)=1 and its first derivative at0 vanishes.

This construction is natural: for a diffeomorphism f relating the pulled-back
metrics, exponential maps intertwine with df_p and both volume densities transform
together. A change of tangent basis is linear. Consequently the vector-space
Hessian at0 of log D_p is a symmetric covariant two-tensor at p. No derivative
with respect to the physical metric is being taken. Its use as a response to
DDR metric-shape tangents is a separate constitutive identification.

There is no Lorentz-invariant positive norm or finite invariant average hidden
in D. For Taylor estimates only, choose any fixed reporting frame and component
norm, not a preferred physical observer. A compact small coordinate neighborhood
bounds the third derivatives, giving the stated O(||v||^3) remainders there.

## 2. Exact coefficient from the complete metric

Use RF1 CANDIDATE sections2–3 with its repository curvature convention. In metric
normal coordinates,

    g_ij(v) = eta_ij - (1/3) R_i a j b(p) v^a v^b + O(||v||^3).

This is the normal Taylor expansion of an arbitrary smooth full metric, not a
symmetry ansatz or weak-curvature restriction. Set h2 to its quadratic term.
Since h2 is of degree2, the determinant/log identity gives

    log D_p(v)
      = (1/2) log det(I + eta^-1 (g(v)-eta))
      = (1/2) tr(eta^-1 h2(v)) + O(||v||^3)
      = -(1/6) Ric_ab(p) v^a v^b + O(||v||^3).

The logarithm is of the positive determinant ratio near0. The curvature
contraction eta^ij R_i a j b is Ric_ab in the stated convention. Therefore

    Hess_0 log D_p = -(1/3) Ric(p),
    E_vol = -3 Hess_0 log D_p = Ric(p).

The equality of tensors is EXACT; the Taylor remainder vanishes after taking
two derivatives at0. Off-diagonal, shift, screen and angular components are all
included. No approximation to the resulting Ricci equation is being made.

An independent geometric reading uses RF1 section5. Along gamma(t)=exp_p(tv),
parallel transport the Jacobi map to p. With A(0)=0, A'(0)=I and
A''+K A=0, K(0)w=R(w,v)v, one has

    A(t)/t = I - (t^2/6) K(0) + O(t^3),
    D_p(tv) = det(A(t)/t)
             = 1 - (t^2/6) tr K(0) + O(t^3).

Parallel transport preserves metric density; det(A/t)>0 sufficiently near0.
Taking its logarithm gives the same Ric(v,v) coefficient. This is a second
argument from existing geometry, not an independently run numerical certification.
The timelike, spacelike and null separation cases follow from the same vector
polynomial; no division by g(v,v) is needed.

## 3. What DDR then says

G310/G311 show that the full locally admissible reciprocal tangents span the
nine-dimensional trace-free symmetric space. For specified symmetric E,

    <E,H(u,n)>_g=0 for every regular pair iff TF(E)=0.

Insert the PROPOSED identification E=E_vol, and only then use section2:

    DDR[E_vol] iff S_ab := Ric_ab - (R/4)g_ab = 0.

This is not DDR[E]=E=0. A nonzero multiple of g satisfies the shape balance.
The geometric identity div Ric=(1/2)dR gives div S=(1/4)dR in dimension4.
Thus S=0 implies dR=0 and Ric=Lambda g on each connected region, with Lambda
supplied by a solution's scalar datum. We do not posit div E_vol=0 identically;
Ricci itself is not identically divergence-free. No action/Noether argument enters.

Any nonzero constant response normalization gives the same homogeneous equation.
An arbitrary trace addition q g is also invisible to DDR. Those equivalent zero
sets do not determine a response normalization or source coupling. The explicit
E_vol representative is a proposal, not a uniqueness theorem for physical E.

## 4. Relation to prior conditional branches and limits

The geometrically defined E_vol is a natural, unoriented, smooth symmetric
metric-two-jet tensor, linear in algebraic curvature with a=1,b=0 and a nonzero
Ricci principal coefficient. Thus it is a representative of G301's already
classified class. The normal-volume construction DERIVES those mathematical
properties of its own definition, not UDT's physical choice of that definition.
It is not an independent derivation of current G312 class membership.

RF1/GL1's broader leading-limit theorem permits general differentiable finite-jet
responses, including a=0 and higher-order remainders. It does not identify the
complete response with E_vol. Equating the exact law to the leading term of an
unknown response would add a further assumption; the present candidate instead
states its exact response identification openly. No claim that this identification
is necessary or sufficient for every empirical GR limit is made.

No new Cauchy proof is required merely to recognize the same conditional equation.
Any later use of G311/G313 development inherits its gauge, initial-data, regularity,
locality and physical-interpretation limits. FE1 does not rerun those theorems or
provide a new unique-history, stability, source or observational result.

## 5. Nonidentity and information boundary

At a point, the Kulkarni–Nomizu curvature of eta and a symmetric tensor A has
Ric=2A+(tr_eta A)eta in dimension4. Choose nonzero trace-free A. Its normal metric
jet is realizable by RF1 on a sufficiently small regular neighborhood, and the
new volume-response balance has S=2A!=0 there. It is a nonidentity restriction
on the diagnostic metric arena, not evidence that this metric is native-admitted.

Conversely constant-curvature data yield Ric=3k g and pass the trace-free law for
any k. Weyl curvature need not vanish: G296's actual Ricci-flat wave witnesses
already retain tidal geometry. The volume coefficient traces curvature; the
full normal metric and its finite-distance density retain additional information.
No scalar-only reconstruction claim, elimination of Weyl physics, flatness law,
finite-distance neutrality or global volume conservation follows.

Proof status: exact argument conditional on the stated geometric definitions and
proposed physical identification. The identification is the unresolved physical
step, not an algebraic consequence to be certified by a passing implementation.
