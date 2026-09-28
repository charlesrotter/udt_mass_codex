# CRD1 — an explicit clock–curvature relation and its closure boundary

Initial candidate for fresh adversarial review. CONDITIONAL, UNPROMOTED.
The construction below obtains differential equations from the complete supplied
pair geometry. It does not derive a native UDT response law. Standard Cartan,
Gauss and Ricci identities are being applied, not claimed as new mathematics.
Exact work scope and authority: WORK_ORDER.md; source snapshot: LAUNCH.json.

## 1. Domain and source ownership

Positional dilation remains the founding interpretation of the common geometry
behind observed c_E, clocks, causal cones and signal timing. Ordinary local
proper clocks and received-tick redshift remain. Set c_E=1 by using length units
for proper time; no numerical value or second local signal speed is derived.

G176/G178 conditionally supply completed reciprocal calibration only after all
metric contributions enter the pair. G220 supplies the received-frequency ratio
on a specified regular null branch. G310's current DDR is owner-provisional;
current G312 authority leaves identification of its response functional open.
GR is a filter, not a field-law input. Historical source wording is read with
those current authority overlays; original grades are unchanged.

Use a smooth time-oriented four-metric of signature (-+++). Where a smooth
timelike immersed pair surface is supplied, its induced metric is written

    h = -N(t,x)^2 (dt+b(t,x)dx)^2 + L(t,x)^2 dx^2,
    N>0, L>0.                                                   (1)

Extending a pair germ to such a surface and choosing its observer field are
supplied query data, not an existence or population theorem. All N,L,b already
include their actual full-pullback contributions; no angular correction is added
afterward. Neither x nor t is a universal physical separation/history parameter.
We retain both directions and time dependence. No spherical center, source,
action, asymptotic cutoff, physical observer family or response equation is chosen.

## 2. Derivation from the full shifted pair

Define an orthonormal coframe and its dual:

    theta0=N(dt+b dx), theta1=L dx,
    u=N^-1 partial_t, n=L^-1(partial_x-b partial_t).

Direct differentiation gives

    a = [N_x-(Nb)_t]/(NL),       H=L_t/(NL),
    d theta0 = -a theta0 wedge theta1,
    d theta1 =  H theta0 wedge theta1.

The induced Levi-Civita connection is w=a theta0+H theta1; it gives
`nabla_u u=a n` and `nabla_n u=H n`. Here H is one-dimensional observer strain,
not a postulated Hubble law. Adopt
`R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y] Z`.
Define the induced sectional tide
`T_h=h(n,R_h(n,u)u)=-R_scalar[h]/2`. Taking d w yields the exact identity

    T_h = n(a)+a^2-u(H)-H^2.                                   (2)

This is already a differential connection between the clock/ruler comparison
and curvature, with all shift terms present. It is a geometric identity for (1),
not a criterion admitting some N,L,b and rejecting others.

For future induced-null directions `ell_epsilon=u+epsilon n`, epsilon=+/-1,
direct differentiation gives

    nabla_ell ell = B_epsilon ell,    B_epsilon=H+epsilon a.

Writing a future affine tangent as `k=omega ell`, with `omega=-h(k,u)>0`, gives

    ell_epsilon(log omega)=-B_epsilon,
    ell_epsilon(zeta)=B_epsilon,   zeta=log(omega_e/omega).       (3)

The reference emitter is fixed along this ray. This derivative is not the drift
obtained by following one source through successive observation times. For a
regular emission/reception comparison `1+z=exp(zeta)`, automatically. There is
no added redshift-response function. Opposite directions are evaluated at their
own events; equation (3) imposes no later-return inversion.

Eliminating a,H between (2) and these directional rates gives a useful explicit
nonlinear interlocking relation:

    (u-n)B_+ + (u+n)B_- + 2 B_+ B_- = -2 T_h.                 (4)

Together with (1)-(3), this describes how both directional clock gradients must
fit the same local geometry. It does not turn a supplied T_h into a native source.
The frame commutator `[u,n]=a u-H n` is part of the geometry; u,n must not be
treated as commuting partial derivatives in (4).

## 3. What reciprocal calibration contributes

G176's WORKING rule gives `m=NL`, `Phi=-log N`, `L=m exp(Phi)`.
Let `M=log m` and `q=b_t/L`. Then

    a=-n(Phi)-q,                 H=u(Phi+M),
    u[u(Phi+M)] + [u(Phi+M)]^2 + n[n(Phi)] + n(q)
                  - [n(Phi)+q]^2 + T_h = 0.                  (5)

Thus there is a fully explicit nonlinear differential equation in calibrated
pair variables. Both M and q are dictated by the supplied complete metric;
they are not optional independent post-readout corrections. In particular,
`d(m dx)=m_t dt wedge dx`: replacing m dx by an exact coordinate differential
while retaining t and its observer curves requires m_t=0. A different coordinate
choice must carry its induced shift and observer changes.

Phi is the local completed clock coefficient. It is not generically the same
as the integrated received-clock depth zeta. G220 identifies the appropriate
terminal pair depth with -zeta only on the same supplied comparison-clock
correspondence; that identity neither constructs the full pair nor drops M,q.

## 4. A scalar-only closure attempt and an exact warning

For the ADDITIONAL restricted class b=0, m=1 in actual coordinates (t,s),
put F=exp(2Phi)>0. Equation (5) becomes

    h=-F^-1 dt^2+F ds^2,
    F_tt - (F^-1)_ss = -2 T_h.                                (6)

This is derived, not guessed. But if one now treats T_h as a prescribed
derivative-free forcing and tries to evolve F alone, the principal part is

    F_tt + F^-2 F_ss,
    principal symbol: xi_t^2+F^-2 xi_s^2 > 0 for xi!=0.         (7)

It is elliptic on this regular class, not a metric-causal hyperbolic scalar
evolution equation. About constant F0, the homogeneous linearized equation is
`f_tt+F0^-2 f_ss=0`; `cos(k s)cosh(k t/F0)` is an exact linearized mode.
This is a principal-type calculation, not a nonlinear stability theorem.

If instead T_h is computed from F itself, (6) is an identity and determines no
evolution. A derivative-dependent closing law could change the principal part,
but no such law has been derived here. There is no conclusion that the complete
UDT metric has elliptic dynamics or violates causality. The precise failed step
is promoting this restricted curvature identity to a closed scalar Cauchy law.

The omitted terms are demonstrably active: N=L=1,b=t gives Phi=M=0 yet T_h=1;
N=1,L=exp(t),b=0 gives Phi=0 but T_h=-1. These are supplied control geometries,
not newly admitted UDT solutions. They change the complete pair relation and
must not be described as physically identical geometries with different answers.

## 5. Restore the ambient geometry before calling this propagation

Let II be the normal second fundamental form of the timelike pair surface.
Its normal space is positive definite. The Gauss identity, with our convention,
gives

    T_h = T_g + <II(n,n),II(u,u)> - ||II(u,n)||^2,
    T_g = g(n,R_g(n,u)u).                                     (8)

An affine induced-null ray is an ambient affine geodesic only if `II(k,k)=0`
along it. Without that condition, (3) describes intrinsic sheet-null transport;
it is not automatically the ambient G220 null query. Even BOTH null directions
being ambient geodesics does not remove the extrinsic term in (8).

Explicit control in flat four-space:
`X(t,s)=(sinh t, cosh t cos s, cosh t sin s,0)` has induced
`h=-dt^2+cosh(t)^2 ds^2`. Its T_h=-1 while T_g=0. A unit normal is X;
II(u,u)=X, II(n,n)=-X, II(u,n)=0. Hence both II(ell_+,ell_+) and
II(ell_-,ell_-) vanish, but their Gauss correction is -1. This is a local
supplied immersion with a free unit scale, not a cosmic model or an X_max.

The two-dimensional pair also does not reconstruct transverse screen curvature.
For an ambient parallel screen basis, Jacobi propagation uses the separate
contractions `O_AB=g(e_A,R_g(e_B,k)k)` and `D''=-O D` on the supplied regular
null ray. Their common origin in R_g is essential; setting them to zero because
they do not appear in a scalar pair equation would discard geometry.

## 6. A full four-dimensional clock–curvature relation

The same calculation can be stated without a pair surface. For any smooth
supplied unit observer field U, define `M^a_b=nabla_b U^a`,
`A^a=U^b nabla_b U^a`, `T^a_b=R^a_cbd U^c U^d`. Ricci commutation and the
product rule give

    U^c nabla_c M^a_b + M^a_c M^c_b
                 = nabla_b A^a - T^a_b.                     (9)

Proof: commute `U^c nabla_c nabla_b U^a`, differentiate `U^c nabla_c U^a`,
and use antisymmetry in the last two curvature slots. No field equation enters.
For a supplied affine null k,

    omega=-g(U,k),   d omega/dlambda=-k^a k^b nabla_a U_b.    (10)

Equations (9)-(10), ambient Jacobi propagation, and (8) specify the actual
clock/curvature/optical dependencies that a response law must close. Observer
motion and initial/query data can remain legitimate free data; they are not
automatically extra physical fields or a selected population. These identities
alone neither determine R_g nor choose the realized metric history.

## 7. Try the owned reciprocity condition at this exact step

DDR concerns a specified symmetric response tensor, call it E[g]. On its
registered full all-pair domain, it gives `TF(E)=0`. This is an adopted
provisional postulate and is retained, not downgraded to an unadopted idea.

However, neither the connection calculation above nor G176 identifies E[g]
with the tidal tensor in (9), the scalar T_h in (5), or Ricci. Substituting one
of those objects by name would be the unsupported step. In particular:

- T^a_b in (9) depends on the supplied observer U, whereas the conditional G301
  response is a natural metric-only symmetric rank-two object. They are not
  the same typed response.
- T_h additionally depends on the pair immersion and its normal bending.
- Local Metric Sufficiency excludes a separate hidden-history label after the
  relevant local metric jet is fixed, but selects neither jet order nor these
  identifications.

If the ENTIRE conditional G301 class is independently established,
`E=a Ric+b Rg`, a!=0, then DDR gives `Ric-(R/4)g=0`; Bianchi leaves R constant
on a connected region. That existing conditional derivation survives. Reusing
it here would not establish the still-open class membership under filter-only
GR. We have not supplied a replacement membership argument.

**Exact return:** (4)-(5) and (9)-(10) construct the clock–curvature differential
relation. The scalar-only closure attempt fails as a causal evolution law at
(7), in its declared restricted architecture. The native derivation stops at
identifying the admitted full-metric response E[g] that would constrain the
ambient curvature, with pair/observer data correctly distinguished. This is
the known ownership boundary now attached to explicit equations and a concrete
failed shortcut, not a newly proved universal impossibility or proof that a
new postulate is necessary. No physical asymptote, measured solar precision,
native equation, mathematical novelty, source coupling or canon is claimed.

## Checks and discovery history

Author frame derivation preceded exact coordinate checking. check_derivation.py
reconstructs original Christoffel/Riemann, both null directions, full calibration,
the restricted principal type and an immersed-surface control. The initial Gauss
check failed on an unsimplified zero hyperbolic expression; the original code,
failure and exact normalization repair remain preserved. check_four_geometry.py
checks every component of (9) at three rational points of a supplied shifted
four-metric with transverse dependence. It is implementation evidence, not a
general proof or whole-solution search. Fresh source-first review is separate;
its direct verdict, any objections and final qualifications control this draft.
