# Smooth local conserved-current representation — initial candidate

Status at construction: UNREVIEWED, UNPROMOTED CONDITIONAL CANDIDATE.
Accepted-source snapshot: 3a31db478b094efc9bce5291349b552aed95059c.
The work order and source freeze were preserved at 8f4470dd before this argument.
This is mathematical discovery, not an outcome-blind observational test. The
current ansatz was exposed in the preceding proposal. No physical law is adopted.

## 1. Source ownership and exact local domain

G349 supplies metric null-screen/cut area geometry in its stated source-cone
domain. G351 supplies an OWNER_ADOPTED_PROVISIONAL conservation premise for a
supplied finite nonnegative countably additive label measure. G352 supplies an
OWNER_ADOPTED_PROVISIONAL readout and explicitly CHOOSES a continuous phase-
independent product on supplied phase and transverse labels. Their audit reports
own current accepted status over historical pending headers in derivations.

Here start directly with G352's supplied smooth scalar Theta, on a smooth
time-oriented Lorentzian 4-manifold of signature -+++, whose raised gradient
k=(dTheta)# is nonzero, null, and future. No cone-extension theorem is needed as
an accepted input. The previously reviewed cone extension remains an unpromoted
conditional candidate. No metric field equation or physical current is supplied.

Shrink to a flow box U diffeomorphic to I_r x I_theta x V, where both I's are
intervals and V is a regular two-dimensional label chart with compact closure
inside a larger chart. The chosen cross-phase identification is fixed throughout
a comparison. Choose transported coordinates (r,theta,y1,y2) with

    theta=Theta, k=partial_r, k(yA)=0.

This is possible locally: on a three-dimensional slice transverse to k,
dTheta restricts nontrivially (otherwise it would annihilate both the slice and
k, hence all of TM). Complete Theta to three coordinates on the slice and flow
them along k; use the k flow parameter for r. This supplies a proof coordinate
system, not physical emission or initial-data selection. k(Theta)=g(k,k)=0.
Exact null gradients are affine: nabla_k k_b=(1/2)partial_b(k^2)=0.

Supply DeltaTheta>0 and dmu=s(y)|dy1 dy2|, where s is smooth and nonnegative,
finite on the retained patch. Smoothness is a deliberate restriction beyond the
general accepted Radon--Nikodym setting. Zero is included without division by s.
The same abstract labels and the same mu on every phase are CHOSEN/SUPPLIED.

## 2. The metric volume factor is the sheet-area factor

Since g(k,.)=dtheta, in coordinate order (r,theta,y1,y2),

    g = [[0, 1,   0,   0],
         [1, H,  W1,  W2],
         [0, W1, h11, h12],
         [0, W2, h12, h22]].                         (A)

Here H,W_A,h_AB may depend on every coordinate. The h_AB block is positive
definite: span(partial_yA) projects isomorphically into the positive null
quotient k-perp/span(k). No zero shift, diagonal screen, symmetry, or field
equation is assumed. Expansion along the first row gives

    det g = -det h,       J=sqrt(det h)>0.             (B)

For a fixed phase theta=c and an arbitrary smooth cut r=tau(y), the tangent
vectors are e_A=partial_yA+(partial_A tau)k. Since g(k,k)=g(k,partial_yA)=0,

    g(e_A,e_B)=h_AB evaluated at the cut,
    dArea=J(tau(y),c,y)|dy1 dy2|.                      (C)

This is the same null-longitudinal cut-gradient cancellation as G349, derived
here directly for the supplied regular phase patch; G349's entire finite-cone
theorem is not widened to arbitrary global congruences. The cut location does
affect h and J; only its extra longitudinal gradient terms cancel.

Choose a local orientation for form notation, vol_g=J dr wedge dtheta wedge
dy1 wedge dy2. Its absolute density is independent of this proof orientation.

## 3. Product to current: a definition with a tested consequence

Let pi:U -> I_theta x V forget r. Give the supplied quotient product its local
oriented representative

    j = pi*[(s(y)/DeltaTheta) dtheta wedge dy1 wedge dy2].  (D)

The absolute quotient density is exactly dXi, not a signed replacement for
G352's |dTheta|. Define C by i_C vol_g=j. Contraction with a nonzero volume form
is an isomorphism from vectors to 3-forms, hence fixes C uniquely for THESE fixed
data. From (B),

    C = rho k,       rho=s(y)/(DeltaTheta J).          (E)

C is future null where s>0 and zero where s=0; it is smooth in this domain.
Changing proof orientation reverses both form representatives, not the vector
or nonnegative density. Alternatively all calculations use volume densities.

Because s depends only on y, d j=0. More explicitly, the Levi-Civita divergence
in (A) gives

    div(rho k) = (1/J) partial_r(J rho) = 0.           (F)

The formula follows from the metric volume identity, not an imported physical
continuity equation. The selected measure is transported by this representation;
the metric has not selected that measure. Along any local transversal graph
r=tau(theta,y), pullback j=(s/DeltaTheta)dtheta wedge dy1 wedge dy2, with no
tau-derivative correction. This represents the prescribed measure on ray space;
it is not a spacetime 4-volume population density and does not count a generator
repeatedly along its flow parameter.

## 4. Observer contraction and exact readout type

For any supplied finite unit future timelike u at a retained point, set
omega=-g(u,k)>0. Equations (C),(E) give

    -g(u,C)=rho omega=omega s/(DeltaTheta J)=Gamma.     (G)

This is exactly G352's continuous clock-rate density, with its premise/product
stamps intact, including at zero density. At fixed phase, two regular cuts with
the same label have Gamma_j/Gamma_i=R_ji/A_ji only on nonzero support. This does
not universalize observer weight one to every conceivable readout.

There is also a pointwise screen check. Any two orthonormal vectors E1,E2 in
u-perp intersect k-perp span the observer's screen. n=k/omega-u is a unit
spacelike vector orthogonal to u and that screen. Thus

    |j(u,E1,E2)|=rho omega.

For general screen basis the right side acquires its metric two-area. Projecting
a cut tangent e_A to that rest screen via E_A=e_A+g(u,e_A)k/omega preserves its
Gram matrix. This verifies the local time-times-screen-area reading, not a global
worldline interception theorem. No arbitrary detector orientation, timelike
detector worldtube law, energy interpretation, or physical source is supplied.

## 5. Exact local converse and the missing product restriction

Consider the declared comparison class of ALL smooth fields C=rho k with rho>=0
on this fixed flow box; no independent physical status is assigned to that class.
By (F), div C=0 if and only if

    F(theta,y):=J(r,theta,y)rho(r,theta,y)
    is independent of r.                             (H)

Connected r intervals matter. Thus the class is exactly

    C = [F(theta,y)/J(r,theta,y)] k,   F>=0 smooth.     (I)

Each such current corresponds to the quotient density
F(theta,y)|dtheta dy1 dy2|. For the fixed phase coordinate, fixed spacing, and
fixed cross-phase identification, it is G352's specified same-mu product iff

    F(theta,y)=s(y)/DeltaTheta with the specified s.    (J)

If s is not specified in advance, membership in SOME such product is exactly
partial_theta F=0 in this identification, plus the retained finite-measure
condition; then s=DeltaTheta F. This follows analytically from (H), not from
finite examples. Conservation imposes no theta derivative condition. In initial
data terms, a general current needs arbitrary F on the three-dimensional ray
quotient. The product reduces this to the supplied two-dimensional s and the
fixed spacing/identification. Equivalently one may freely specify rho on a
transversal r=r0(theta,y) and set F=J0 rho0. No numerical transport solve is needed.

Witness of strict inclusion: Minkowski (t,x,y,z), Theta=z-t, k=(1,0,0,1),
r=(t+z)/2, screen labels (x,y), J=1, DeltaTheta=1. On theta in (-1/2,1/2)
and the unit label square, C=(2+theta)k is positive and divergence-free because
(partial_t+partial_z)theta=0. Its phase-slice label mass is 2+theta, not constant.
It therefore cannot represent the specified uniform-in-phase G352 product at
fixed Theta/DeltaTheta. This example still factors with a NONuniform phase
weight; it is not called a genuine phase-label correlation.

A genuinely nonseparable comparison is C=(1+theta*x)k on the same box:
partial_theta partial_x log(1+theta*x)=1/(1+theta*x)^2, nonzero. It too is smooth,
positive and divergence-free. Both are comparison objects, not sourced processes
or newly adopted physical branches; separate phase sheets need not exchange
content merely because their supplied populations differ.

Initial data on one characteristic phase sheet do not determine F at neighboring
phases: k is tangent to that sheet. The three-dimensional transversal above is
transverse to k, not a single characteristic phase level.

## 6. Covariance and free-data audit

At fixed supplied g,Theta,DeltaTheta and abstract labels, any smooth finite
nonnegative s defines (E): zero, arbitrary total, and different same-total
distributions. Uniqueness FOR fixed product data is not metric selection of data.
The geometry does supply area/volume/solid-angle measures in their respective
domains. Their identification with conserved populated mu is not automatic.

For phase-independent passive relabeling y'=h(y), both s and J transform with
|det(dy/dy')|, so rho and C are unchanged. For phase-dependent passive relabeling
y'=h_theta(y), F' = F(theta,h_theta^-1(y'))|det(dy/dy')|; the same rule holds for
J at fixed theta. Such coordinates can make the coefficient phase-dependent
without changing C or the original abstract identification. Holding the numeric
y' fixed across phases would instead impose a DIFFERENT identification. Thus
partial_theta F=0 is an intrinsic product condition relative to the supplied
identification, not a coordinate test under arbitrary phase-dependent relabeling.
Total phase-slice mass on the full retained label set is unchanged by a bijective
passive relabeling; the varying-total witness cannot be repaired that way.

Under G352's positive affine phase gauge Theta'=b Theta+d, DeltaTheta'=b DeltaTheta,
k'=b k, choose r'=r/b. The screen metric at the same event is unchanged, rho'=rho/b,
and C'=C. Under a nonlinear increasing Theta'=f(Theta) while keeping the same
DeltaTheta and mu, the NEW chosen product gives C'=f'(Theta) C. It remains
divergence-free because k(Theta)=0, but generally changes -g(u,C). This is not
G352 gauge. Holding C fixed instead requires a compensating phase-dependent
quotient density in the new phase coordinate. No physical calibration is selected.

## 7. Scope, evidence, and scientific ceiling

The general local argument is (A)–(J), with arbitrary H,W,h and arbitrary smooth
nonnegative F on a fixed product flow box. Exact finite examples check determinant,
nullness, cut Gram cancellation, genuine divergence including a nonconserved
control, readout, phase dependence and coordinate/gauge handling. Those finite
checks do not prove the general claims or cover all possible code defects.

The current is a covariant repackaging of supplied smooth data in this domain.
The equation div C=0 alone is strictly weaker than the fixed same-mu product.
No physical current/carried object, positive population, phase unit, phase law,
source, detector, energy, action, field equation, history, matter, scale, X_max
or canon is derived or adopted. No claim excludes another metric-native route.
Nothing here extends the ordinary-density representation through a vertex,
caustic, branch crossing, singular measure, atomic crossing, or global topology.
Those exclusions do not weaken the existing G351/G352 measure-valued statements.

No accepted scientific source, grade, current frontier, fixed-snapshot manuscript
or CANON is changed. Review and banking preserve a conditional candidate only.
