# PC2 independent source-first reconstruction

Pre-candidate argument; no new PC2 author proof/code/results read. This is
conditional mathematical review work, not a scientific promotion.

## Parallel extension

Let Q_abcd=g(R(e_a,e_b)e_c,e_d), with vector convention
[nabla_a,nabla_b]V^d=R_ab c^d V^c and Ric_bc=g^ad Q_abcd.
Thus [nabla_a,nabla_b]v_c=-R_ab c^d v_d for a covector.
Use Box=g^cd nabla_c nabla_d, including every tensor slot in the second
covariant derivative. All quantities below are smooth on the actual metric.

PC1, on the admitted Ric=0 sector, gives R(A,B)ell=0 for ALL ambient A,B
on the open initial slice patch. Its spatial-commutator conclusion alone
would not suffice outside that sector. PC1's initial equations include both
Xf=K(X,Y) and D_XY=fK#X, with ell=f n+Y, |Y|=f>0.

Shrink around an initial event to a local globally hyperbolic domain with a
spacelike Cauchy patch, avoiding influence of its edge. Conditional on the
standard smooth linear normally-hyperbolic Cauchy theorem, construct a
covector v with

    Box v=0, v|Sigma=ell-flat, nabla_n v|Sigma=0.

The metric is fixed and smooth Lorentzian, its connection is smooth, the
principal symbol is g^ab xi_a xi_b times the identity on a finite-rank bundle,
and the hypersurface is noncharacteristic. Smooth local data can be extended
outside a smaller patch for the theorem; local uniqueness/domain of dependence
removes that arbitrary extension. No global compactness or metric-development
existence is claimed. G321's particular compact family is not the theorem.

Put A_ab=nabla_a v_b. Directly commuting the derivatives gives

    Box A_ab = nabla_a Box v_b + Ric_a^c A_cb
               -2 g^cd R_da b^e A_ce
               -(nabla^c R_ca b^d) v_d.                    (A1)

To derive the coefficient2, first interchange nabla_c and nabla_a on v_b,
then interchange nabla_d and nabla_a on the two-covector tensor nabla_c v_b.
Curvature acting on its c slot contracts to +Ric_a^e A_eb; curvature on its
b slot gives the second identical negative R*A term. Forgetting the c slot
or one of the two interchanges changes the formula.

Contracted differential Bianchi, with the same Q convention, is

    nabla^c Q_ca b f = nabla_f Ric_ab - nabla_b Ric_af.     (A2)

It follows from first-pair differential Bianchi and pair interchange. Hence
the last term is (nabla_b Ric_a^d-nabla^d Ric_ab)v_d. On the ACTUAL Ricci-flat
metric both it and the Ric*A term vanish, so

    Box A_ab +2 g^cd R_da b^e A_ce=0.                     (A3)

This is a homogeneous normally-hyperbolic system on T* tensor T*. It uses no
symmetry of A and no initially assumed ambient parallelism.

All initial Cauchy data of A vanish. A|Sigma=0 follows from the full spatial
seed and the chosen nabla_n v=0. Since the zero tensor vanishes along an OPEN
patch, nabla_X A=0 there for all tangential X. The identity

    (nabla_n A)(X,Z)-(nabla_X A)(n,Z)
       =-v(R(n,X)Z)=g(R(n,X)ell,Z)=0

then gives (nabla_n A)(X,Z)=0, including all Z. Finally Box v=0 gives

    -(nabla_n A)(n,Z)+sum_i(nabla_ei A)(ei,Z)=0,

so the remaining (nabla_n A)(n,Z) vanishes. These are tensorial evaluations
of covariant derivatives: normal-frame acceleration/extrinsic-curvature terms
are already included, and terms multiplying A disappear only because A=0.
No initial normal derivative is discarded.

Conditional uniqueness for (A3) gives A=0 locally. Thus V=v# is parallel and
agrees with ell. Its norm is constant zero, and it remains nonzero and future
on the retained connected neighborhood. Two parallel extensions agreeing on
the patch agree locally by parallel transport. This establishes a local
sufficient class, with no quantitative lifetime or transverse stability claim.

## Full recipe and curvature transport

Ambient parallelism implies R(A,B)V=0. By curvature symmetries contraction of
Q with V in ANY slot is zero. Differential Bianchi contracted with V, using
nabla V=0, therefore gives

    nabla_V Q=0.

For example, V^e[nabla_e Q_abcd+nabla_a Q_becd+nabla_b Q_eacd]=0;
the last two terms are derivatives of zero contractions. Ric=0 makes W=Q
up to the harmless overall convention sign. The parallel metric and volume
form imply nabla_V B=0 for the unchanged full Weyl/first-dual quadratic B.

At every event, PC1's Ricci-flat algebraic classification applies after
choosing n,e3 with V=f(n+e3). Therefore the entire tensor is

    B=b^4 V-flat tensor4, b>=0.

At a nonzero-root initial event b>0, continuity supplies a smaller neighborhood
with b>0. One can define the scalar b smoothly there by contracting B with a
smooth auxiliary timelike vector and dividing by its nonzero V contraction;
the full tensor identity makes the result independent of that auxiliary.
The two real covector fourth roots are separated by time orientation:

    beta=b V-flat, C0=beta#=b V.

At the initial slice b=[4(p^2+q_PC1^2)]^(1/4)/f. The subscript avoids confusing
PC1's curvature parameter with q_rec. Rescaling the parallel seed by a positive
constant rescales b inversely and leaves beta fixed. A varying seed multiplier
would generally violate the spatial seed and is not root normalization freedom.

Since nabla_V B=0 and V-flat is parallel, V(b)=0 on b>0. Full recurrence is

    nabla beta=alpha tensor beta, alpha=d log b,

with unique alpha because beta is nonzero. This is AMBIENT recurrence, including
normal derivatives. No phase closure was used. The old intrinsic recipe becomes

    q_rec=g^-1(alpha,alpha), D=q_rec b V.

The identity alpha(V)=0 puts alpha in the annihilator of a nonzero null vector.
The Lorentzian quadratic form is positive semidefinite on that annihilator, so
q_rec>=0. Its nullspace is span(V-flat). Consequently, pointwise,

    q_rec=0 iff alpha is proportional to V-flat iff d beta=0.

Closure on an open patch needs this condition throughout that patch; q=0 at
one event is not a neighborhood statement. q=0 does not imply alpha=0 or
parallel beta, because the proportionality coefficient need not vanish.

Also nabla_V alpha=d(V log b)=0, since V is parallel. Thus V(q_rec)=0, and

    div C0=0, nabla_C0 C0=0, div D=0, nabla_D D=0.

D is smooth even where q_rec=0, but is nonzero future-null only where q_rec>0.
A positive initial value remains positive on some neighborhood by continuity;
all coefficients are constant along each local V generator. This supplies no
uniform normal-time interval for an unrestricted noncompact data patch and no
extension through a zero of B.

## The actual initial scalar data

Write a=log b|Sigma. Tangential recurrence fixes alpha(X)=X(a). Since
alpha(V)=0 and V|Sigma=f n+Y,

    alpha(n)=-Y(a)/f,
    q_rec|Sigma=|D a|_gamma^2-[Y(a)/f]^2.                 (A4)

The last expression is the squared spatial gradient perpendicular to Y/f.
Thus it is nonnegative and determined by the spatially varying complete datum
and the fixed-root coefficient. The normal derivative of b is constrained by
n(b)=-Y(b)/f, and the normal derivative of beta is alpha(n)beta. These are not
free additional recipe data once propagation has been proved. Likewise
n(q_rec)=-Y(q_rec)/f follows from V(q_rec)=0 wherever the derivatives exist.

No extrinsic-curvature term should be appended to alpha(n): b is a scalar and
V is parallel; connection terms belong in the full derivative of beta. The
spatial derivatives of b do require the actual spatially varying curvature
data, not only an isolated p,q,f tuple at one event.

## Limits and independence

This source-first argument is a separate reconstruction, not a claim to a new
physical field or derived recipe. It relies on PC1's reviewed algebra and the
explicitly conditional auxiliary local wave theorem. The finite checks in this
review can detect sign and source omissions; they do not machine-prove general
PDE existence, uniqueness or propagation. The theorem quantifier comes from
(A1)-(A4), their full initial data and the declared PDE hypothesis.

General recipe-compatible data lacking the seed, generic necessity, global
completion/zeros/caustics, compact embeddings, physical population, product
factorization or a preserved supplied phase/label measure remain outside.
G355/G356's positive and failed products do not settle those later boundaries.
Owner-provisional G312/G351/G352 and CHOSEN recipe stamps remain unchanged.
