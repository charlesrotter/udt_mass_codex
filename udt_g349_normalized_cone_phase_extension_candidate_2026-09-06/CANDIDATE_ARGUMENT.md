# Local phase extension preserving a supplied G349 cone normalization

Status: `CANDIDATE_ONLY_NOT_INDEPENDENTLY_REVIEWED_OR_PROMOTED`.
Date: 2026-09-06. Source snapshot: `5ef2f971805ee23383cad694c5cb058124614a5d`.
This is a mathematical compatibility argument, not a new accepted theorem or a
physical realization. The previous phase/measure candidate's separate review
does not review this argument.

## 1. Exact domain and candidate landing

Write the G349 source family as K(n,r)=gamma_n(r), with its prescribed affine
k=partial_r K and k(p)=u+n. Restrict to a locally embedded branch N, away from
the vertex, with transverse screen rank two throughout the retained patch.
The vectors k,J_1,J_2 span TN, and G349's g(k,J_A)=g(k,k)=0 gives

    TN=k-perp, beta=k-flat != 0, beta|TN=0, nabla_k k=0.

Thus N is a smooth null hypersurface on this restricted branch. This does not
replace G349's broader allowance of caustics, repeated sheets and rank strata.
In this document a restriction of an ambient covector at points of N is NOT
the pullback of that covector to TN.

Candidate conclusion: for every point q of this branch, after shrinking around
q there is a smooth Theta with

    g^-1(dTheta,dTheta)=0, (dTheta)# future and nonzero,
    Theta|N=0, dTheta_q'=beta_q' for all q' in the retained N patch.       (1)

No rescaling of G349's k occurs. The neighborhood extension is not unique.
Theta here is a real-valued mathematical scalar in the prescribed geometric
normalization. This does not turn G349's numerical source normalization of one
into a physical phase/frequency unit. Assigning operational meaning and units
to a supplied dimensionless G352 phase remains part of its supplied realization,
not a calibration derived here. The readout comparison is conditional on using
the same scalar normalization and spacing in both compared realizations.
The conclusion is about a germ/local patch, not a single global phase covering
an arbitrary cone, both widely separated cuts, a vertex, intersecting branches,
or all of G349's compact input patch. Any readout comparison below requires its
retained cut images to be inside the common domain of the compared extensions.

## 2. Initial scalar data on a mathematical proof slice

Choose a small spacelike three-surface S through q, with future unit normal n_S.
Because k is nonzero null, it is transverse to S. The intersection C=N intersect S
is a spacelike two-surface. In local S coordinates (rho,y^1,y^2), take C={rho=0}.
The restriction beta_S of beta to TS along C annihilates TC and is nonzero.
Consequently beta_S=a(y)d rho with a smooth nonzero function a. A reversal of rho
may make a positive on a small connected patch; this is a chart convention.

For ANY smooth b(rho,y), set on S

    phi(rho,y)=a(y)rho + rho^2 b(rho,y).                            (2)

Then phi|C=0 and d_S phi|C=beta_S. These are mathematical Cauchy data for a
scalar extension problem, not a chosen physical source, emission history or
initial metric development. Shrink S so d_S phi remains nonzero.

Let h=g|TS and extend Q=d_S phi to an ambient covector annihilating n_S. The
unique future-raised null covector extending Q is

    P=Q+|Q|_h n_S-flat.                                          (3)

Indeed g^-1(P,P)=|Q|_h^2-|Q|_h^2=0, and P# has positive n_S component |Q|_h.
On C, (3) equals the FULL beta, because beta has the same tangential part and
the same future-null branch. This establishes the normalization at the initial
two-surface; a merely intrinsic condition beta|TC=0 would not establish it.

## 3. Local characteristic construction without adding a physical equation

On T*M use the mathematical Hamiltonian H(x,P)=g^{ab}(x)P_a P_b/2 and the
canonical one-form lambda=P_a dx^a. Its equations are

    dx^a/ds=partial H/partial P_a,
    dP_a/ds=-partial H/partial x^a.                               (4)

This is the Hamiltonian form of Levi-Civita affine geodesics for the supplied g,
not a matter action or a selected physical evolution equation. Smooth g gives
smooth local ODE flow. Start (4) from the three-dimensional lift (x,P(x)), x in S,
defined by (3). H=0 initially and remains zero. At s=0 the differential of the
base projection from (s,x) spans TS and P#, which is transverse to S. The inverse
function theorem therefore makes this projection a diffeomorphism after local
shrinking. Nonzero/future orientation persist there by continuity. This is the
noncharacteristic step; no arbitrary spacelike slice is assumed to be a global
Cauchy surface and no uniform caustic-free lifespan is asserted.

For completeness, the one-form identity verifies that the projected covector is
an exact gradient, rather than just a null geodesic congruence. With the signs
in (4), i_XH d lambda=-dH and lambda(XH)=2H, so

    L_XH lambda=dH.

If G(s,x) is the lifted characteristic flow, H composed with G is identically
zero. Thus the derivative in s of G_s^*lambda vanishes on TS; initially it is
d_S phi. Also lambda(partial_s G)=2H=0. On the full parameter space,

    G^*lambda=d(phi(x)).

Define Theta at the projected point G_base(s,x) to be phi(x). The local
diffeomorphism then gives dTheta=P on the projected neighborhood, so (1)'s
eikonal, nonzero and future conditions follow exactly. This is an analytic
construction; no numerical PDE solution was attempted or required.

## 4. Matching the entire retained cone patch, not only C

For x in C the initial covector is exactly beta_x. The lifted G349 curve
(gamma(s),k-flat(s)) satisfies (4), since k is affine and the connection is
metric-compatible. Uniqueness of the smooth ODE makes these characteristics
coincide, with the SAME affine normalization, with those constructed in section
3. Transversality supplies a short local flow tube of N from C. On that tube,

    Theta=phi|C=0, dTheta=k-flat.

Both normalization and scalar value have therefore propagated on the original
cone patch. Normal derivatives away from N were not prescribed by G349.

Affineness is genuinely needed for this fixed-normalization problem: a null
gradient satisfies

    K^a nabla_a K_b = K^a nabla_b K_a
                    = (1/2) nabla_b(g^-1(dTheta,dTheta)) = 0.

Replacing k on N by a nonaffine generator can defeat (1). This is a control on
the proposed extension, not a defect in the accepted G349 affine construction.

## 5. Residual freedom and exact witnesses

The function b in (2) is free mathematical extension data. No result here says
that all neighboring foliations differ only by a phase reparameterization.
For a fixed foliation, f(Theta) with f(0)=0, f'(0)=1 and f'>0 locally preserves
the full gradient on N; f(Theta)=Theta+c Theta^2 is a simple example. At fixed
DeltaTheta this is generally NOT G352's affine phase/spacing gauge. Agreement
on N is weaker than agreement at other phase levels.

An explicit example also changes the neighboring foliation. In Minkowski
coordinates (t,x,y,z), let r=|X|, retain N={r=t>0} near a regular point, and use
Theta_0=r-t. Its raised gradient is exactly the G349 outgoing affine tangent
with source observer partial_t and k(p)=partial_t+n, away from the vertex.
For a free mathematical parameter a define a second scalar c=Theta_a implicitly:

    |X-a c^2 e_x|-t-c=0.                                        (5)

At c=0 on N, the derivative of the left side with respect to c is -1, so the
implicit-function theorem supplies a smooth local branch. Put

    R=|X-a c^2 e_x|>0, m=(X-a c^2 e_x)/R,
    D=1+2 a c m_x>0.

Direct differentiation gives

    dTheta_a=(-dt+m dot dX)/D.                                   (6)

It is exactly null and future-raised. On N, c=0, D=1 and m=X/r, so the full
covector equals dTheta_0. For c != 0, the level surfaces have different
mathematical centers a c^2 e_x and generally different normals. They are not
merely f(Theta_0). These centers are witness geometry, NOT physical source
events selected for UDT.

For example, a=1, c=1/10, X=(1/100,1,0), t=9/10 gives R=D=1 and
dTheta_a=(-1,0,1,0). The base gradient there is
(-1,1/sqrt(10001),100/sqrt(10001),0), not parallel. The path with c varying from
zero and X=(c^2,1,0), t=1-c has D=1, connecting this witness to the c=0 branch.
Such points exist arbitrarily close to N. No global branch choice is needed.

## 6. What original-cut readouts can and cannot depend on

Compare ANY two extensions satisfying (1) on a common retained patch. Keep the
G349 label/cut maps X_i, endpoint observers u_i, G351 supplied measure mu and
G352 fixed positive spacing DeltaTheta and chosen product conditions fixed.
At every original-cut point in N, the full gradient agreement implies

    omega_i=-dTheta(u_i)=-g(k,u_i), independently of the extension.

G349 supplies the same metric sheet-area Jacobian J_i; neither it nor the
supplied label density s is changed. On the absolutely continuous regular part,

    Gamma_i=(omega_i/DeltaTheta) s/J_i,
    Gamma_j/Gamma_i=R_ji/A_ji on common nonzero support.            (7)

Thus even absolute local Gamma_i, not just its ratio, is extension-independent
with these inputs fixed. Zero density has no ratio, and singular content is not
assigned an ordinary density. The weighted pushforwards also agree on these
cuts because their maps, weights and mu agree; finiteness still requires
integrability of omega_i/DeltaTheta against mu. This argument does not extend
the existence claim through rank loss or beyond the common phase domain.

The zero value Theta|N does NOT make omega or Gamma zero: observers are timelike
and transverse to N, whereas dTheta annihilates tangent vectors in TN. Reading
only the pullback would lose the entire clock-rate datum. Similarly, 2Theta has
the same zero level and zero pullback on N but twice the full gradient and twice
Gamma at fixed spacing. It is an excluded normalization change, not extension
freedom allowed by (1).

Values/readouts at neighboring phase surfaces, finite observer-worldline
intervals, phase-label identification and phase-dependent populations are not
fixed by this one-cone statement. Equation (2) supplies possible local scalar
extensions only; it neither derives nor uniquely selects G352's product.

## 7. Honest decision boundary

The candidate argument finds local compatibility, not a need for a new physical
premise or a derivation of physical content. The metric plus G349's supplied
cone data can support a mathematical phase extension with the prescribed
normalization; the arbitrary extension function, phase spacing, populated label
measure and physical interpretation are not thereby selected.

G349 does supply geometric measures (source solid angle and metric sheet area).
Identifying one with G351's conserved carried measure is an additional choice,
not an absence of geometric measure and not a consequence of this argument.
G351/G352 keep their owner-provisional premise stamps and chosen-product scope.

Actual attacks on this route must address full-covector matching, affine
transport, the local projection/exactness step, or equation (7) with ALL declared
inputs held fixed. A counterexample requiring a vertex, multiple crossing cone
branches, screen-rank loss, global extension, nonaffine tangent, or changed
measure/spacing is outside this claim, though it may motivate a different test.

No independent review of this new argument has occurred. Exact witnesses and
same-context checks below are supporting/regression evidence, not a proof of
the general smooth construction, an empirical confirmation or acceptance.
