# Step3 candidate — harmonic-wave phase integrability and geometric conversion

UNPROMOTED; direct review pending. IDs CB3-ROOT, CB3-PHASE-CLASS,
CB3-CONVERSION-BOUNDARY. This is a new conditional mathematical extension in
the accepted vacuum arena, not a repaired/accepted G313 witness or physical law.
The original c19b5fb1 Weyl/first-dual recipe stays CHOSEN, not metric-selected.
Step1/Step2 enter only with their reviewed conditional scopes and caveats.

## 1. Local arena and full root (CB3-ROOT)

Take a smooth real H(u,x,y) on a regular product chart I x J x V, with I,J
intervals and V a connected transverse open patch. Shrink to a simply connected
local patch as needed; no global completion is inferred. Set

    g=-2 du dv+dx^2+dy^2+H du^2,       H_xx+H_yy=0.

Use supplied time orientation with partial_v future. The nonzero Christoffel
symbols are Gamma^v_uu=-H_u/2, Gamma^v_ui=Gamma^v_iu=-H_i/2 and
Gamma^i_uu=-H_i/2 for i=x,y. In particular Gamma^u_ab=0, det(g)=-1 and
du/partial_v are parallel. Direct curvature gives only

    R_uiuj=-H_ij/2

and its Riemann symmetries. Ric_uu=-(H_xx+H_yy)/2 and all other Ricci
components vanish. Therefore this proposed class satisfies Ric=0 inside the
G312/G313 owner-provisional vacuum equation, without asserting physical
population or repairing any accepted equation.

Write a=H_xx,t=H_xy, so H_yy=-a. Since Ric=0, W=R. Its transverse block is
-1/2 [[a,t],[t,-a]], of squared norm (a^2+t^2)/2. The first-pair dual rotates
this block and has the same norm. No lower v index occurs, so both contracted
indices in the original quadratic recipe must be transverse, leaving all four
free indices u. The FULL identity is

    B=(a^2+t^2) du tensor4.                               (1)

On a retained region N=a^2+t^2>0, set b=N^(1/4)>0. The only real covector
fourth roots are +/-b du; mixed components force every transverse/v component
to vanish, exactly as in the original fixed-recipe argument. Time orientation
chooses beta=-b du, C0=beta#=b partial_v. The root is smooth on N>0. At N=0
the recipe gives only zero; neither nonzero extension nor regularity through
such points is claimed.

## 2. Conservation is not phase closure

Since b is independent of v,

    div C0=partial_v b=0,       nabla_C0 C0=0.

Thus the root current is conserved and affinely geodesic even when beta is not
closed. Its complete covariant derivative and exterior derivative are

    nabla beta=-db tensor du,       d beta=-db wedge du.   (2)

Consequently beta is closed iff b_x=b_y=0. If so it is locally the null phase
gradient dTheta, with Theta(u)=-integral b(u) du plus an additive constant.
Parallelism is stronger: it additionally requires b_u=0. For example
H=(1+u)^2(x^2-y^2), u>-1 in supplied length units, has
b=sqrt(2)(1+u), Theta=-sqrt(2)(u+u^2/2), and nonparallel beta despite exact
closure, affine null flow and conservation. No varying profile is selected as
physical content by this example.

## 3. Exact phase-compatible class (CB3-PHASE-CLASS)

On each transverse slice a,t are harmonic. Differentiating H_xx+H_yy=0 also
gives a_y=t_x and t_y=-a_x. Hence the exact real identity is

    (partial_x^2+partial_y^2)(a^2+t^2)
       =4[(H_xxx)^2+(H_xxy)^2].                          (3)

If beta is closed, N=b^4 is transverse-constant, so the left side is zero.
Each real square must vanish. The other transverse third derivatives vanish
by harmonicity. Thus the Hessian is transverse-constant on connected V, and

    H=X^T M(u) X + ell(u).X + c(u),
    X=(x,y), M=M^T, trace M=0.                            (4)

Conversely(4) makes N a function of u only and gives closed beta on every
nonzero-root interval. Smoothness supplies all derivatives in(3) and smooth
coefficient functions. This is an if-and-only-if for THIS root and harmonic
metric class, proved by(2)-(3), not a coverage-checklist completeness claim.

Linear/constant terms do not defeat the local symmetry conclusion. Choose s(u)
and zeta(u) satisfying

    s''=M s+ell/2,      zeta'=ell.s/4+c/2,

and transform old coordinates by

    X_old=X+s(u),
    v_old=v+s'(u).X+s(u).s'(u)/2+zeta(u),  u_old=u.

Direct full pullback gives centered H_new=X^T M(u)X and preserves du/beta.
The vector ODE is a finite-dimensional linear inhomogeneous first-order system
for(s,s') with smooth bounded coefficients on a sufficiently short compact
subinterval. Its integral map is a contraction in the supremum norm when the
interval length times a coefficient bound is <1; arbitrary finite initial
data then have a unique local solution. Shrinking the chart controls the map;
its triangular coordinate Jacobian has determinant1. No global ODE completion
or boundary choice is used. The scalar zeta is obtained by integration.

For centered variable M(u), F_h=(u,h^2v,hX) still obeys F_h*g=h^2g and fixes
beta=-b(u)du. The transverse isometries in Step2 generalize to arbitrary vector
s''=M(u)s with the same compensating v shift. The same bounded local ODE argument
gives arbitrary values/derivatives at u0. Hence they connect the fixed axis to
each transverse/generator point at fixed u. All maps preserve time orientation.

It follows by Step2's reviewed fixed-point argument, now with these hypotheses
verified for(4), that EVERY local natural smooth scalar Q[g,beta,Delta] with
weight-2 under constant homothety (beta,Delta fixed) vanishes on this entire
phase-compatible class. Naturality includes pullback and restriction
compatibility; no extra boundary/observer/material scale is allowed in that
optional class. Phase dependence of Q does not evade the fixed-axis argument.
This does not prohibit supplied finite area measures, all physical content,
other metric classes or non-scalar/differently typed constructions.

## 4. A positive geometric conversion outside that class (CB3-CONVERSION-BOUNDARY)

On every nonzero-root region in section1, beta is recurrent:

    nabla beta=alpha tensor beta,       alpha=db/b.

The nonzero covector beta makes alpha unique. For any local Y with beta(Y)!=0,
alpha(X)=(nabla_X beta)(Y)/beta(Y); the equality shows independence from Y.
Thus alpha is an intrinsic natural covector of the metric and the CHOSEN root,
not a chosen observer or the non-scalar component b treated as a scalar.
The expression db/b is its coordinate representation. Define the CHOSEN scalar

    q=g^-1(alpha,alpha)=(b_x^2+b_y^2)/b^2 >=0.             (5)

Constant metric homothety preserves the connection and original lower B/root;
it therefore fixes alpha and gives q -> h^-2 q. This rule is observer-neutral
and has the requested conversion weight. Moreover, in this class,

    q=0 iff d beta=0.                                    (6)

The equivalence uses alpha_v=0 and the positive transverse metric; a u-component
of alpha is harmless to both sides. It does not follow on arbitrary recurrent
null geometries without checking their metric/domain.

For the exact nonquadratic harmonic witness H=x^3-3xy^2 in supplied length
units, on a local patch away from r^2=x^2+y^2=0,

    b=sqrt(6)(r^2)^(1/4),
    alpha=(x dx+y dy)/(2r^2),       q=1/(4r^2)>0.

At(x,y)=(1,2), q=1/20, alpha_x=1/10,alpha_y=1/5, and
(d beta)_ux=b/10, (d beta)_uy=b/5. These nonzero components explicitly refute
closure of the fixed recipe root. Both C0 and q C0 remain conserved, since
all their coefficients are v-independent. Their quotient densities are
|j|=b|du|dxdy and q|j|, with homothety weights+2 and0 respectively. On a
compact local product patch separated from r=0 these densities are smooth,
nonnegative and finite on bounded phase-coordinate intervals.

Restore a supplied length unit L by taking H=(x^3-3xy^2)/L^3 for this witness;
b has inverse-length units, alpha also has inverse-length components, q has
inverse-area units and q|j| is dimensionless. L here records the supplied
coordinate/unit normalization of the example, not a metric-selected physical
length or fitted scale. The intrinsic definition(5) contains no supplied L.

This is a positive geometric counterexample to extrapolating Step2's scalar
obstruction to all Ricci-flat metrics. It does NOT refute Step2, because this
geometry lacks that phase-compatible plane-wave structure. Multiplication by
q is still a chosen mathematical recipe, not physical count identification.

## 5. The joint boundary and what is NOT refuted

Within this harmonic-wave class, retaining the exact original curvature root as
the phase gradient forces(4), on which the optional natural scalar weight-2
conversion class is zero. A nonquadratic geometry can supply the positive
conversion(5), but its root then fails phase closure wherever q>0. These results
do not simultaneously supply nonzero count conversion AND that same normalized
root phase. Conservation alone survives both branches and is not sufficient.

Another null phase can exist even when this particular root is nonclosed. An
integrating factor or separately supplied phase could change its normalization
and must be treated as a different construction, not another root of fixed B.
The result does not exclude a G352 chosen-product realization of q C0 using
such a different phase. Nor does it rule out other metric classes/recipes,
extra data, singular/atomic content, or an accepted physical bridge not shown
here. Physical population/identity remains OPEN under G351/G352.

The full symbolic checker independently assembles Christoffel/Riemann tensors,
checks Ricci, all lower Riemann components, first dual and full B, harmonic
identity, recurrence, concrete closure defect, conversion scaling and full
coordinate gauge/homothety pullbacks.19 guard groups passed; all5 actual
deliberate mutations failed at their intended first guards. These algebraic
checks and exact examples supplement the analytic local-class argument; they
are not a census of vacuum solutions, independent review or physical evidence.
No unexpected author failure or correction occurred. No reviewer finding was
received before author construction. Direct fresh review is still required.
