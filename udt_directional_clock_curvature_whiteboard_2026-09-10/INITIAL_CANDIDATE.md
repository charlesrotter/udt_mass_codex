# DCI1 — directional clock information and one timelike curvature component

Initial candidate, 2026-09-10. CONDITIONAL MATHEMATICAL APPLICATION; UNPROMOTED;
fresh adversarial review pending. Work order/data freeze control. Preserve these bytes.
This reconstructs a known kinematic identity in the repository's clock-depth variables;
it is not a new field equation or a claim of novel differential geometry.

## 1. Inputs, quantifiers and excluded information

Use any supplied smooth local time-oriented 4D Lorentzian (g,U), signature (-,+,+,+),
with U future unit timelike and Levi-Civita connection. At p choose an orthonormal rest
frame and all unit rest directions n. The regular future null query with initial
k=U+n has omega=-g(U,k)=1 at p. On its affine parameter lambda, G220 gives

    delta_AB=log(omega_B/omega_A),    q(n)=(1/omega) d delta/d lambda at p.

The normalization quotient is invariant under a constant positive affine rescaling.
Local angular and infinitesimal-parameter calibration are part of the ideal record
definition. They are not assumed to be obtained from an unlabelled list of clock ratios.
Smoothness gives local regular branches; no distant endpoint, caustic or global claim.

The inverse data map supplies q(n), the observer-time derivative dot m=U(<q>) at p,
and separately A=div a and W=w_ab w^ab, where a=∇_U U and w is spatial vorticity.
The complete metric derivative array, curvature tensor, branch endpoint coordinate map,
flight times, screen/frame transport and complete pair pullback are not supplied data.
g and U are underlying comparison objects, not known full inputs to the inverse map.
Local frame/units are matched across comparisons. No Einstein equation is imposed.
Time is in proper-length units (c_E=1); no physical length scale is selected.

The angular mean is computed with normalized uniform rest-sphere measure. Its derivative
uses nearby events on the same observer worldline. It is unchanged by a smooth rotation
of the spatial frame, so no direction-transport law is silently made physical.

## 2. Clock slope and its angular components

Define h_ab=g_ab+U_a U_b, theta=div U, H=theta/3 and the standard decomposition

    ∇_a U_b = -U_a a_b + H h_ab + sigma_ab + w_ab,

where sigma is spatial symmetric trace-free and w is spatial antisymmetric, with bracket
conventions including 1/2. Parallel transport of null k gives

    d omega/d lambda = -k^a k^b ∇_a U_b,
    q(n) = -H - a_i n_i - sigma_ij n_i n_j.                 (1)

This directly reconstructs the directional identity in NCI1; no endpoint potential or
its integrability condition is assumed. The vorticity term cancels by antisymmetry.
The normalizing omega in q is essential: q=d log omega/(omega d lambda), not the
unnormalized logarithmic slope away from initial omega=1.

Let

    m=<q>,  e(n)=[q(n)+q(-n)]/2,  V=<(e-m)^2>.

The exact sphere moments <n_i n_j>=delta_ij/3 and
<n_i n_j n_k n_l>=(delta_ij delta_kl+delta_ik delta_jl+delta_il delta_jk)/15 give

    H=-m,
    a_i=-3<q n_i>,
    sigma_ij=-(15/2)<q(n)(n_i n_j-delta_ij/3)>,
    sigma_ab sigma^ab=(15/2)V.                              (2)

The pointwise clock data recover the symmetric expansion/shear and acceleration dipole;
they do not recover vorticity. These are exact all-direction identities, not a finite
sampling/convergence or instrument-reconstruction claim.

## 3. Conditional curvature formula

Use R^a_bcd=∂_c Γ^a_db-∂_d Γ^a_cb+Γ^a_ce Γ^e_db-Γ^a_de Γ^e_cb,
Ric_bd=R^a_bad. The Levi-Civita commutator and product rule give

    div a = (∇_a U^b)(∇_b U^a) + U(theta) + Ric(U,U).

The decomposition in section 2 yields

    (∇_a U^b)(∇_b U^a) = theta^2/3 + sigma_ab sigma^ab - w_ab w^ab.

Consequently

    Ric(U,U) = -3 U(H)-3H^2-sigma_ab sigma^ab+A+W
             = 3 dot m - 3 m^2 - (15/2)V + A + W.          (3)

This is the standard nongeodesic timelike Raychaudhuri identity expressed in the declared
clock records. The proof uses metric compatibility, a torsion-free connection, unit U,
smoothness and exact data. It uses no GR field equation, source stress tensor, energy
condition, action, observer-population law or angular-cancellation response postulate.

**Sufficiency claim:** any two such underlying geometries/congruences with identical
declared {q(n),dot m,A,W} at their matched events have the same Ric(U,U) there.
No claim is made that every arbitrary tuple of records is realizable or determines
the full curvature, metric, history or response law. Algebraically only A+W enters this
scalar target; separate A and W are transparent motion channels, not an absolute
minimum-data theorem. A=0 or W=0 may be used only if independently justified in the
specified example/congruence, never imposed as a generic UDT property.

## 4. Actual metric witnesses for omitted information

All examples are smooth local Lorentzian metrics with supplied observer U, not solutions
claimed to follow from a native field law. They are counterexamples to reconstruction
from particular reduced record maps, not a metric census or statements about typicality.

### 4a. Omitting dot m

Take g_beta=-dt^2+exp(beta t^2)(dx^2+dy^2+dz^2), U=∂_t, at t=0.
The positive scale factor is exp(beta t^2/2). For all real beta,

    q(n)=0,  A=W=0,  m=V=0,
    dot m=-beta,     Ric(U,U)=-3 beta.

Thus the same full instantaneous angular clock-slope data and the same A,W do not fix
the target without a suitable temporal record. Comparing beta=0 and beta=1 suffices;
symbolic beta states a family, not a fitted physical parameter.

### 4b. Omitting A, even when acceleration at the observer is supplied

Take N=1+(kappa/2)(x^2+y^2+z^2),
g_kappa=-N^2 dt^2+dx^2+dy^2+dz^2, U=N^-1 ∂_t on a small N>0 patch.
On the central worldline x=y=z=0, for every t,

    q(n)=0 for all n, dot m=0, a=0, W=0,
    A=Delta N/N=3 kappa,     Ric(U,U)=3 kappa.

The central clock data and all their central time derivatives agree with kappa=0;
the observer acceleration itself and its central time derivative also vanish. Its
neighborhood divergence does not. A single-worldline accelerometer value is not A.
Away from the central line q need not vanish; spatial clock-gradient data are extra
records excluded by this reduced map.

### 4c. Omitting W, even with all local q derivatives supplied

Set B=(b/2)(x dy-y dx) and

    g_b=-(dt+B)^2+dx^2+dy^2+dz^2,    U=∂_t.

The coframe (dt+B,dx,dy,dz) is nonsingular and exhibits signature (-,+,+,+).
U is smooth future unit Killing, hence a=H=sigma=0. Therefore q=0 in every direction
throughout the local domain, all derivatives of q vanish, and A=0. Direct geometry gives

    W=b^2/2,     Ric(U,U)=b^2/2.

In particular b=0 and b!=0 agree on the entire local scalar-slope field and A yet have
different target curvature. Rest frames may be explicitly identified using
E_i=∂_i-B_i∂_t; at the origin they coincide with the coordinate spatial frame.

Since U is Killing, g(U,k) is constant on each of that metric's affine null geodesics.
Thus every individual regular finite null-depth value is also zero. This is a statement
about scalar values on each metric's own branches. It is NOT equality of endpoint
incidence domains, event-pairing offsets, flight times, paths, full frame transport or
the complete reciprocal kernel. Such information would be additional inverse data.

### 4d. Losing directional shear information

Take g_s=-dt^2+exp(2s t)dx^2+exp(-2s t)dy^2+dz^2, U=∂_t.
In the natural orthonormal frame,

    q(n)=-s(n_x^2-n_y^2),  m=dot m=A=W=0,
    V=4s^2/15,             Ric(U,U)=-2s^2.

The scalar mean and its drift agree with flat space; the even directional quadrupole
does not. NCI1 already owns this family's expansion/shear kinematics. The additional
application here is the explicit reduced-data curvature ambiguity and its connection
to (3). This does not rebrand a known family as a newly selected UDT structure.

## 5. Interpretation and circularity boundary

The exact positive result is factorization of one curvature component through a declared
ideal record map. It is conditional on motion data that carry information absent from
the scalar clock readout. Those data must remain labeled supplied; deriving them from
the full metric and calling curvature independently recovered from clocks is circular.
Actual physical access to normalized null-clock gradients, temporal/angular labels,
vorticity and neighborhood acceleration divergence is not established here.

The counterexamples explain why those distinctions are substantive: a twisting metric
can have uniform zero scalar null-depth values while its Ric(U,U) is nonzero. This is
compatible with the complete metric/pair evaluator retaining information beyond a scalar.
It is neither failure of UDT nor closure of its native dynamics/physical-content question.
No field equation was used to distinguish these geometries.

## 6. Source attribution and review ceiling

G220 owns the regular null-clock arrow; NCI1 INITIAL_CANDIDATE.md plus REPAIR.md provides
the reviewed UNPROMOTED directional bridge, re-derived here. G215/G216, G333 and G358
provide typing/nonduplication comparisons, not additional field hypotheses. Current
G312 authority remains unchanged. See SOURCE_NOTES.md and SOURCE_MANIFEST.tsv.

The standard identity is credited to Abreu and Visser, *Some generalizations of the
Raychaudhuri equation*, arXiv:1012.4806v1, section II, equations (1)–(9), and the
Levi-Civita commutator argument above. Their discussion explicitly covers arbitrary
unit timelike congruences as geometry. No gravity equation or physical fluid premise
from that paper is imported. The repository source-map search is bounded and does not
prove exhaustive novelty. All numerical/symbolic checks support, rather than replace,
the analytical proof and concrete metrics. Review pending; no registry/canon promotion.
