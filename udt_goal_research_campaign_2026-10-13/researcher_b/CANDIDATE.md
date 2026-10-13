# GRC1 B2/B3 — clock-sign and optical-tide connection

EXPLORATORY, UNADOPTED, NOT YET ADVERSARIALLY REVIEWED. This is a candidate
source for the campaign, not another maintained development. Discovery and access
history are in RESEARCH_NOTES.md. The campaign authorized conjecture testing,
not adoption of these physical hypotheses.

## 1. The physical question and assumptions

Can an additional positional effect slow a specified initially parallel free-clock
comparison in every local laboratory, without prescribing the same numerical
coefficient in all frames? What would that require of optical tides?

Use PSW1's released-clock protocol and PCC1's matched comparison exactly. Supply
smooth Lorentz4 metrics g,g0, matched events and a time-oriented tangent isometry I.
Match proper initial separation L, unit laboratory frame, parallel initial velocity,
units c_E=1, and regular null branches; each experiment uses its own freely falling
worldlines. This is not an addition of metrics or a second physical spacetime.
The reference and matching remain physical choices, not selected native data.

Set A(X,Y,Z,W)=g(R(X,Y)Z,W), with R=[nabla_X,nabla_Y]-nabla_[X,Y], and

    D = A_g - I* A_g0,
    C(U,n) = lim_(L->0) 2 log(p_L/p0_L)/L² = -D(n,U,U,n).

U is any future unit timelike vector, n any unit spacelike vector perpendicular
to U. Existing PSW1 proves the coefficient for each fixed smooth comparison;
PCC1 proves this matching convention. No uniform finite-L remainder over all
boosts is used. C is additional leading clock contrast, not total received shift.

**S — unadopted sign trial:** C(U,n)>=0 for every U,n at the matched event.
This weakens PCC1's same-value-in-every-frame trial to same-sign only. It adds
the interpretation of this prepared L² coefficient as a positional contribution.
Neither no preferred observer nor a universal governing law supplies S.
An effect beginning at higher order is allowed at events where C=0.

For a null vector k, D induces the symmetric form

    Q_k([x],[y]) = D(x,k,k,y)

on the positive screen k-perp/span(k). Gauge x->x+ak changes nothing. Its trace
is Delta Ric(k,k), with all contractions performed using the common tangent
metric under I. This difference is not the stress tensor of a new UDT constituent.

## 2. Universal clock sign constrains optical tides

**Proposition B2.1.** S implies Q_k<=0 for every null k; hence
Delta Ric(k,k)<=0. Moreover, if q is the trace-free part of Q_k,

    ||q||_op <= -Delta Ric(k,k)/2.

Proof. Write k=u+v after positive normalization, with u unit future timelike and
v unit spatial. For a unit screen representative n perpendicular to u,v, take
U_eta=cosh(eta)u+sinh(eta)v. S says D(n,U_eta,U_eta,n)<=0 for every finite eta.
Multiply by exp(-2eta) and take eta->infinity in this finite-dimensional algebra:

    (1/4)D(n,k,k,n)<=0.

Every screen vector is represented this way; homogeneity and polarization give
negative semidefiniteness. This limit is taken AFTER the fixed-laboratory L->0
coefficient, so it makes no assertion about a common finite experiment size at
infinite boost. A null-frame contraction gives tr Q_k=Delta Ric(k,k). In two
screen dimensions, Q=(tr Q/2)I+q has eigenvalues tr Q/2 +/- ||q||_op; requiring
both to be nonpositive proves the quantitative inequality.

Conversely, the null inequality alone does not imply S: D=-B_g has Q_k=0 while
C=-1. The sign of the space-form component is invisible to null screens.

Under W4's conditional geodesic interpretation, the additional instantaneous
relative acceleration at the matched event, for matched separation data, is
-Delta T times that separation. Positive C is therefore expansive additional
timelike tidal acceleration in that direction. Each geometry's optical Jacobi
fields obey J''+T_g J=0 with its OWN total screen tide; Q is only the matched
difference T_g-I*T_0 at the source. A nonpositive Q thus means additional local
null defocusing in the initial curvature coefficient. It is not an evolution
equation for the difference of two propagated beams. This is curvature language,
not an adopted matter equation.
If one SEPARATELY uses the Einstein-tensor comparison, g(k,k)=0 implies
Delta G(k,k)=Delta Ric(k,k)<=0. Calling that an effective NEC violation requires
the extra Einstein/matter identification; no exotic UDT matter follows here.

### Operational optical statistic and approximation scope

At each matched source event choose the same normalized null k, -g(k,U)=1,
and an orthonormal screen. In each geometry follow its vertex pencil with
J(0)=0,J'(0)=I, and compare at the same affine parameter lambda. Smoothness gives

    J_g(lambda)=lambda I-lambda³ T_g(0)/6+O(lambda^4),
    det J_g/lambda²=1-lambda² Ric_g(k,k)/6+O(lambda³),

and the corresponding reference formula. Therefore the leading difference in normalized vertex area is
-Delta Ric(k,k)/6. The specified source normalization and affine cut are essential
query data; equal coordinate radius or redshift is not this comparison. This
geometric pencil is not a luminosity/flux law or instrument certification.
Finite lensing also depends on propagated paths, endpoint cuts and all intervening
geometry. Equal pointwise Q does not imply identical finite lensing.

For a hypothetical optical bound Delta Ric(k,k)>=-epsilon in one declared source
normalization, S gives -epsilon I<=Q_k<=0 and ||q||_op<=epsilon/2. This is a
conditional error-to-tide statement, not an empirical bound obtained here.

## 3. An optional optical condition recovers isotropic addition

**F — separate unadopted optical trial:** Delta Ric(k,k)>=0 for every null k.
This prohibits additional local null area defocusing. It is genuinely new and
oppositely directed to S's consequence, not a consequence of existing UDT
commitments, no preferred observer, exact GR recovery or ordinary clocks.
Its investigatory motivation is to test whether universal additional clock slowing
can coexist with unchanged or more focusing null vertex areas. Exact F is not
needed for the sign-only branch and is not imposed to hide that branch.

**Proposition B2.2.** In Lorentz4, S and F together are equivalent to

    D = kappa B_g, kappa>=0,
    B_g(X,Y,Z,W)=g(Y,Z)g(X,W)-g(X,Z)g(Y,W).

Proof. B2.1 and F give negative semidefinite Q_k with zero trace, hence Q_k=0.
Here is an explicit pointwise null-curvature rigidity argument. For any orthonormal
u,e1,e2 with u timelike, apply Q=0 to k=u+e1 and k=u-e1, with screen e2. Adding
and subtracting shows

    D(e2,u,u,e2)=-D(e2,e1,e1,e2), D(e2,u,e1,e2)=0.

Interchanging e1,e2 and using curvature pair symmetry makes the two electric
diagonal contractions equal. In the three-dimensional u-rest space, any two unit
directions have a common perpendicular direction, so the electric quadratic form
is -kappa(u) times its metric; polarization supplies the off-diagonal statement.
For any two timelike u,v, their common orthogonal space has dimension at least2
and is positive. Choose orthonormal n,m there. The same spatial contraction
D(n,m,m,n) equals both kappa(u) and kappa(v). Thus one kappa works for all U,n.
For F0=D-kappa B, F0(X,U,U,X)=0 for every X and timelike U by projection and
homogeneity. Polynomial identity extends in U, then polarization and algebraic
Bianchi force F0=0. S sets kappa>=0. Conversely B_g(n,U,U,n)=-1 and its null
screen contraction is zero, proving both S and F.

The all-frame equality is a CONCLUSION in this conjunction, not its starting
assumption. The isotropic branch is the already studied PCC1 curvature class;
this is a new conditional discriminator/route relative to the inspected repository,
not a claim of new general differential geometry. D is a matched difference;
ordinary nonuniform Weyl curvature may remain in g and g0.

Across a region the PCC1 Bianchi/matching qualifications still apply. General
pointwise kappa need not be constant under an arbitrary transferred reference.
With an Einstein reference Ric[g0]=Lambda0 g0, physical contracted Bianchi makes
kappa constant on a connected domain. No general metric realization theorem,
physical reference, field equation or scale is selected.

### Exact adverse controls

1. A Kottler-type algebraic tensor with electric entries
   (-2w-kappa,w-kappa,w-kappa), spatial entries
   (-w+kappa,-w+kappa,2w+kappa) has Ric=3kappa g and null Ricci zero.
   At w=1,kappa=2, one frame sees C=(4,1,1)>0. But U=(5/4,0,0,3/4), n=e2
   gives C=-11/16. One-frame sign and zero null trace do not replace all-frame S.
2. The supplied smooth metric -dt²+cosh²(t)(dx²+dy²+dz²), relative to a matched
   flat reference, has temporal curvature A=1 and spatial curvature B=tanh²t.
   Every unit timelike plane has C=A+(A-B)|m|²>=1. Yet Q_k=-sech²(t)I for
   k normalized by the comoving clock. Thus S alone permits non-spaceform
   curvature and fails F. This is an actual metric control, not admitted cosmology.
3. `checks/algebra_01` independently uses a 21-variable symmetric bivector
   tensor, algebraic Bianchi and54 exact rational null-screen equations. Their
   combined rank is20 and the remaining one-dimensional space is exactly B_g.
   This exact finite linear-algebra anchor supports the proof, not its physical
   assumptions or a finite numerical sampling theorem.

## 4. Spherical radial neutrality leaves a larger sign-only family

This section was developed AFTER the parent exposed researcher A's NAR avenue;
it is a collaborative follow-on, not independent initial discovery. NAR concerns
spherical radial rays. Its physical endpoint law and geometric equivalence remain
owned by A's derivation; the following computations require only the displayed
supplied reciprocal metrics and do not assume that NAR implies F.

On a common regular static annulus r>0, f>0,f0>0, use

    g=-f(r)dt²+dr²/f(r)+r²dOmega²,
    g0=-f0(r)dt0²+dr²/f0(r)+r²dOmega²,
    delta f=f-f0.

Match equal areal radii and oriented radial/angular orthonormal frames. A physical
reference f0 is still supplied. The matched curvature difference has electric
entries (-alpha,-beta,-beta), spatial entries (beta,beta,gamma), where

    alpha=-delta f''/2, beta=-delta f'/(2r), gamma=-delta f/r².

For a unit timelike plane (U,n), let b_i=U0*n_i-n0*U_i and
m=U_spatial cross n_spatial. Simplicity gives b dot m=0; normalization gives
|b|²-|m|²=1. Direct contraction then yields

    C=beta+(alpha-beta)b1²+(beta-gamma)m1².                 (B3.1)

**Proposition B3.1.** In this supplied spherical difference class, S is exactly

    beta>=0, alpha>=beta, beta>=gamma.                    (B3.2)

Sufficiency follows immediately from B3.1. The unboosted transverse plane tests
beta. For alpha<beta, take U=cosh(eta)e0+sinh(eta)e2,n=e1, obtaining b1²=cosh²
eta,m1=0 and a negative C at sufficiently large finite eta. For beta<gamma,
take U=cosh(eta)e0+sinh(eta)e2,n=e3, giving b1=0,m1²=sinh²eta and the same
contradiction. These are actual finite timelike planes; no completeness claim
rests on a finite sample.

For k=e0+e1, both null-screen differences vanish. For k=e0+e2, the screen
diagonal is (beta-alpha,gamma-beta), hence its trace is gamma-alpha<=0.
Radial neutrality therefore coexists with nonradial defocusing. F would force
alpha=beta=gamma; radial neutrality alone does not do so.

Write delta f=-r² q(r). Then B3.2 becomes

    q+(r/2)q'>=0, q'>=0, (r³q')'>=0.                     (B3.3)

Thus the proposed all-frame clock sign restricts the otherwise arbitrary radial
profile, but does not choose it. Once q' becomes positive, it cannot switch off
exactly at a later finite radius while these inequalities hold: r³q' is nonnegative
and nondecreasing. On an interval [r0,r1] this gives the quantitative consequence

    q(r1)-q(r0) >= (r0*q'(r0)/2)[1-(r0/r1)²].

No infinite domain is assumed. These inequalities alone do not prohibit a finite
asymptotic q limit: q' proportional to r^-3 can be integrable. They do not certify
regularity at a center or horizon. A regular spherical center requires an actual
smooth Cartesian extension; with finite even q there, beta(0)=q(0)>=0 and q'>=0
then give q>=0 outward. A Schwarzschild reference with nonzero mass is only an
annulus here; its singular center is not repaired by the comparison.

For delta f=-lambda r^4, lambda>0, q=lambda r² gives

    (alpha,beta,gamma)=lambda r²(6,2,1),
    C=lambda r²(2+4b1²+m1²)>0 for r>0,
    Q_radial=0, Q_tangential=lambda r² diag(-4,-1).

This exact anisotropic sign-only branch is a separator from PCC1. If f0 is supplied
Schwarzschild it still has the same matched difference on the common regular
annulus. No fitted mass, preferred universal center, matter interior, dynamics,
observational GR pass or selected lambda is supplied.

## 5. A finite released-clock witness in the quartic metric

Take the specific flat reference f0=1 and f=1-lambda r^4, lambda>0. Put
r_h=lambda^(-1/4). The metric has a smooth regular center: in Cartesian coordinates
the added spatial term is lambda r²/(1-lambda r^4)*(x_i dx^i)². We work strictly
inside the static patch 0<=r<r_h. r_h is a zero of this supplied lapse, not X_max,
a material boundary, or the radius of all physically admitted comparisons.

A is the central geodesic clock, with proper time t. At t=0 launch B from
r0=r_h/4, at rest in the static orthonormal frame. That velocity is exactly the
parallel transport of A's initial velocity along the t=0 radial spacelike
geodesic: the derivative of f^-1/2 cancels Gamma^t_rt=f'/(2f). Thus this is PSW1's
released preparation, with actual proper initial separation

    L=integral_0^r0 dr/sqrt(f(r)).

The ratio1/4 is a free control choice for a transparent exact bound, not a physical
scale selection. The flat reference uses the same proper L and parallel velocity,
so its first and future-return ratios are p0=q0=1.

B has constant Killing energy E=sqrt(f(r0))=sqrt(255)/16 and outward proper
radial velocity v=sqrt(E²-f(r)), since r''=-f'/2=2lambda r³>0. At a radial outgoing
signal's interception with B, the null conserved quantity and endpoint contractions
give exactly

    p=E+v, q=1/(E-v),                                      (B3.4)

where q is the actual immediate inward return to A, evaluated at the relay. It is
not an inverse arrow. In the static patch 0<v<E and both ratios are finite positive.

An emitted ray at t=0 has coordinate flight time t_gamma(r)=integral_0^r dr/f.
B has t_B(r)=integral_r0^r E dr/[f*sqrt(E²-f)]. Their difference is

    F(r)=-rstar(r0)+integral_r0^r dr/[v(E+v)],
    rstar(r0)=integral_0^r0 dr/f.

F starts negative and is strictly increasing. Using dr/dv=v/(2lambda r³),

    F(r_h) >= -rstar(r0)+r_h log(2)/2,
    rstar(r0)<=64r_h/255, log(2)>2/3.

Hence the limiting F at r_h is positive. There is one interception r_arr<r_h.
At p=1, v*=1-E; this threshold lies inside the patch since E>1/2. At its radius,

    F(r*) <= -r0+(1-E)/(2lambda r0³ E)
           =r0[-1+1/(2E(1+E))]<0.

The unique interception is therefore after the p=1 threshold. Consequently
p>1 and q>1, both on finite regular future null legs, while p0=q0=1. A nearby
emission family is regular because the interception is transverse and B is timelike.
This is a finite conditional existence witness, not an observational fit or a
proof about all initial separations.

The slowing is produced by the same geometry's lapse and induced motion. In the
static orthonormal frame at the relay, beta=v/E, eta=atanh(beta), so exactly

    p=sqrt(f_arr)*exp(eta), q=exp(eta)/sqrt(f_arr), pq=exp(2eta).

The outward geodesic acceleration increases the Doppler factor enough to overcome
the outbound static-lapse blueshift. This is a decomposition available in this
supplied stationary witness, not subtraction of ordinary GR/Doppler effects or
proof that a separately isolated positional mechanism has been observed. The
physical meaning of its matched contrast still belongs to the unadopted hypothesis.

At the center all curvature components vanish, so the local L² coefficient is0.
For a small separately varied preparation epsilon=lambda r0^4, rescale
r=r0 R,t=r0 T,tau=r0 S. On the O(1) flight interval,

    R_B=1+epsilon S²+O(epsilon²),
    E=1-epsilon/2+O(epsilon²), v_arr=2epsilon+O(epsilon²),
    log p=(3/2)lambda L^4+O(lambda² L^8),
    log q=(5/2)lambda L^4+O(lambda² L^8).

Smooth dependence of the rescaled regular ODE/incidence problem near epsilon=0
controls these expansions; initial proper L=r0+lambda r0^5/10+O(lambda²r0^9).
These are asymptotics, not numerical error bars for r0=r_h/4. They show how a finite
effect can survive a zero local quadratic coefficient; the old quadratic1:3 ratio
is not asserted at this different leading order.

For contrast, holding B static at radius R uses an accelerated clock and gives
the exact outgoing p_static=sqrt(1-lambda R^4)<1. It requires proper acceleration
2lambda R³/sqrt(f), growing without bound as R approaches r_h. Thus the same
geometry can give the opposite finite net sign under a different preparation.
Neither B3.4 nor the static comparison selects a universal observer population.

## 6. A weaker angular-mean trial in a declared Ricci-flat reference sector

The coordinator proposed this direction after B2/B3 were developed; it is not an
independent initial researcher idea. Its point is to test whether the physically
more limited mean observable avoids both full Weyl matching and the strong
per-direction sign condition.

In PSW1, one orthonormal triad or the angular mean at leading quadratic order gives

    M(U)=(1/3)sum_i C(U,e_i)=-Delta Ric(U,U)/3.

If the declared reference sector has Ric[g0]=0, this becomes -Ric[g](U,U)/3,
independent of which Ricci-flat reference and tangent matching are used. This
does not prove that the relevant physical comparison sector is Ricci-flat; it is
an explicit restricted reference choice. It does not remove reference dependence
from individual directions or finite clock records.

**M — unadopted mean-sign trial:** M(U)>=0 for every future unit U in this
declared comparison sector. **F0 — separate unadopted optical trial:**
Ric[g](k,k)>=0 for every null k. They are not implied by no preferred observer,
ordinary clocks, DDR or merely calling the sector quiet. In a conventional
Einstein-matter interpretation F0 would be a null-convergence/energy comparison;
that interpretation is not adopted as a UDT premise.

**Proposition B4.1.** On a smooth Lorentz4 region, M and F0 at every point are
equivalent to Ric[g]=Lambda g with constant Lambda>=0 on each connected component.

Proof. M gives Ric(U,U)<=0 on the timelike cone. Taking a rescaled timelike-to-null
limit gives Ric(k,k)<=0. F0 makes these null contractions zero. In an orthonormal
frame, a symmetric tensor S with S(e0+v,e0+v)=0 for every spatial unit v is
proportional to g: v=+/-ei first gives S0i=0,Sii=-S00; v=(ei+ej)/sqrt2 gives
Sij=0. Thus Ric=Lambda(x)g, and M=Lambda/3 sets Lambda>=0. Contracted Bianchi
gives dLambda=(1/2)d(4Lambda), hence dLambda=0. The converse is direct.

This keeps arbitrary Weyl tides. The w=1,kappa=2 tensor in section3 has
Ric=6g, so satisfies the mean and optical trials, despite its finite boosted
negative directional C. It separates B4 from the stronger directional S+F.
The cone and quartic witnesses instead satisfy M while having negative null
Ricci somewhere; they show the optical trial remains substantive.

The resulting Einstein class overlaps the older FE1/PSW1 response-identification
route, but no response E=aRic+lambda g or action is postulated here. The proposed
physical join is now two directly typed clock/optical inequalities. This does
not derive those inequalities natively, select Lambda, identify ordinary sources,
prove a finite-distance law, pass GR tests, or isolate an additional positional
effect. It cannot be extended silently into matter regions with positive null
Ricci. No claim of new Einstein algebra or a new field solution is made.

## 7. Meaning and open physical joins

The surviving connection is a covariant implication from a precisely specified
additional clock-sign hypothesis to timelike relative acceleration and null
optical defocusing, with an optional rigidity branch and a larger explicit
anisotropic radial family. It constrains supplied comparison geometries rather
than merely evaluating an arbitrary one, but the proposed sign rule is UNADOPTED.

The physical join is still substantial: why should the positional contribution
be the matched PSW1 coefficient in every frame, which reference/matching realizes
it, and does this hold only in a quiet sector or also amid ordinary sources?
The spherical family fixes no matter law or evolution outside its declared static
sector. Exact F is a separate physical proposal, not current authority. Relaxing
it preserves testable anisotropic possibilities with nonradial optical changes.
The finite quartic witness demonstrates a possibility, not uniqueness, typicality,
stability, a universal distance law, a native derivation or a complete UDT model.

The native scalar remains tanh(Phi) on the supplied completed pair. DDR's response
is not identified with Ricci or anything else in this candidate. No registry grade,
CANON entry, physical scale, source, X_max realization, or protected result changes.

## 8. Author check receipts and explicit omissions

`checks/algebra_01` and `checks/spherical_01` are exact SymPy checks described
above; both passed with empty stderr. `checks/arrival_01` independently integrates
the coordinate-time geodesic and null arrival maps, then differentiates the actual
proper-arrival data. At lambda=1,r0=1/4 the tighter float64 run gives
p=1.005909819619 and q=1.009917278384; changes under halved step/difference and
tighter tolerances are below8e-12, and endpoint-formula differences below3e-12.
The sampled conserved-energy residual is about1.1e-16. Proper normalization is
computed from the metric and is therefore an algebraic check, not independent
equation certification. Raw arrivals, equations, controls and versions are saved.
These numerical agreements are not interval bounds; the sign/existence proof in
section5 is analytic and does not depend on those decimal results.

Not performed: fresh adversarial review (parent will dispatch), an empirical
test, global PDE stability, matter/interior matching, generic metric realization
of the algebraic cone, full finite-clock classification, an asymptotic UDT
assignment or a physical reference-selection derivation. No absence/uniqueness
claim follows from the exploratory scope or these omissions.

