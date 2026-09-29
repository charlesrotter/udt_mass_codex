# Source-first mathematical reconstruction — CDR1

Verdict on the reconstructed tiles: **VERIFIED-WITH-CAVEATS**, conditional on
their stated inputs. This is not yet a review of UDT_DEVELOPMENT.md. The new
central candidate has not been read. This report is sealed before that exposure.

Reviewer: separate context `/root/development_math_review`, same inherited model
as parent; different-model identity, human review and formal proof are not
established. Parent continuing-session synchronization and full startup are
attributed. Actual HEAD independently verified as
`26da433f090a7c10717649a47c4f2383612f05cd`, branch `grok`; status inspected.
No protected payload opened, hashed or changed. Writes are confined to this
review directory. The parent full premise audit is attributed, not independently
rerun here. The exact selected registry rows and controlling source bytes are
pinned in SOURCES.json. Source audit verdicts and source checks were visible;
this is source-first relative to the new manuscript, not verdict-blind review.

The calculation scripts are independently written from tensor and matrix
definitions; they import no source-package scientific functions. They share
Python/SymPy and the existing capture launcher with repository work. Distinct
code and separate context are recorded separately from independent argument.

## 1. F1–F4: exactly what the character argument supplies

The mathematical domain is a positive diagonal action on a dimension-matched
clock/ruler pair. Let P(d)=diag(u(d),v(d)) and K have off-diagonal entries 1.
Multiplication gives P^T K P=uvK. Therefore the stated dual-pairing law is
equivalent to uv=1. This is the load-bearing content of F2. The numerical
invertibility of c_E alone gives no such law: a covariantly transformed
conversion can instead have u=v, and u=v=2 violates dual pairing.

Positivity permits a=log u. F3 composition becomes the additive Cauchy equation
a(d1+d2)=a(d1)+a(d2). Under continuity (or measurability on the additive real
group), the additive function is linear. Thus u=e^{kd}, v=e^{-kd}; nonidentity
ensures k is nonzero. Defining delta=-kd chooses sign and unit, rather than
measuring or deriving a physical distance. The trivial representation remains
allowed if nonidentity is removed. Reversal follows from the same group law.

F4 supplies the Lorentzian quadratic readout and the static spherical areal
sector. Applying the factors gives the declared primary metric

    g=-e^{-2 phi(r)}(c_E dt)^2+e^{2 phi(r)}dr^2+r^2 dOmega^2.

Its determinant is -c_E^2 r^4 sin^2(theta), so its positive volume density is
c_E r^2 sin(theta) on the usual oriented angular chart. The areal sphere,
signature and static-spherical restriction are readout inputs; they do not
follow from the two-dimensional character theorem alone. A general ambient
Lorentzian coframe is a supplied extension arena, not a theorem that all its
histories are physical UDT histories.

S^{-1}dS=diag(-dphi,dphi). The tensor quadratic form is
Tr(J tensor J)/2=dphi tensor dphi; its tangent evaluation is (X phi)^2.
Exterior multiplication instead vanishes. The current founding.md explicitly
repairs the older untyped J^2 notation. An invariant quadratic form on a
one-dimensional real representation algebra is unique up to a positive factor;
that fact is not a physical cost or action principle. No equation for phi,
depth versus measured distance, action, field equation or absolute scale follows.

The continuous account should preserve the positive chain
F1/F2/F3/F4 -> reciprocal character -> declared primary metric -> readout,
while keeping its inverse input assignment open. Positional dilation's owner
interpretation and ordinary proper clocks are compatible premises, not a proof
that any particular supplied profile realizes the intended mutual slowing.

## 2. G166 and G176–G180: control scalar versus completed scalar

Take a symmetric 2-by-2 matrix h with h00<0 and det h<0. Completing the square
gives, uniquely,

    T^2=-h00, beta=h01/h00,
    L_sigma^2=h11-h01^2/h00>0,
    h=-T^2(dy0+beta d sigma)^2+L_sigma^2 d sigma^2.

Consequently -det h=T^2 L_sigma^2. The arbitrary auxiliary-ruler scalar is
phi_control=(1/2)log(L_sigma/T). Its ratio q=T/L_sigma is positive and
chi=(1-q)/(1+q)=tanh(phi_control). For the founded reciprocal diagonal block,
det=-1 and these return its supplied delta exactly. G166 is this positive
algebraic descent, not a separate profile law. Multiplicative compatible q
gives the Mobius composition law; the existence of those compatible carried
relations is part of its domain.

Now add W1/G176. Keep the supplied clock coordinate and rescale only the ruler
by ds=m d sigma with m>0. Then L_s=L_sigma/m and beta_s=beta/m. The physical
completed reciprocity requirement T L_s=1 is equivalent to

    m=T L_sigma=sqrt(-det h), det h_s=-1,
    Phi=-log T=-log(-h00)/2.

This is a unique positive density theorem with fixed clock calibration. It is
not invariant under an arbitrary new choice of clock parameter. Clock/event
typing therefore remains necessary. Shift is present even though it cancels
from the determinant. Interpreting determinant normalization as a field
equation or a physical event selector would erase a hypothesis.

The pointwise relation ds=m d sigma is a ruler-coframe normalization. An actual
one-coordinate integral is supplied by the one-dimensional G180 family. On a
two-dimensional time-live surface with m=m(y0,sigma), this one-form need not
be exact: d(m d sigma)=(partial_0 m)dy0 wedge d sigma. A general coordinate
change would introduce an extra dy0 component. Pointwise normalization must
not be silently promoted into that stronger coordinate assertion.

G179 forms h=J^T E^T eta E J before this algebra, for supplied invertible E and
rank-two J. The rank condition alone does not imply h00<0; the stated regular
conditions are essential. There is no inverse of the two-dimensional base
projection Y in the proof. Our exact full multiplication reproduces

    h=[[-118,102],[102,822]], -det h=107400,

and the singular-Y regular witness

    h=[[-124,-132],[-132,225]], -det h=45324.

These include screen/mixing data and nonzero shift. They validate the assembly
identity and rule out a hidden invertible-Y hypothesis, not physical selection
of that particular coframe. Lorentz gauge changes cancel inside E^T eta E;
matched ambient coordinate changes cancel between E and J. A varying supplied
query satisfies hdot=Jdot^T gJ+J^T gdot J+J^T g Jdot and
Phidot=-hdot00/(2h00), by differentiation. This is kinematics, not dynamics.

For G180 the determinant is a smooth negative function on the supplied connected
regular interval, so m is smooth positive. Its integral s=s0+integral m is
strictly increasing, has nonzero derivative everywhere, and is a smooth
diffeomorphism onto its image. The interval hypothesis prevents a circular
parameter being silently replaced by a global real coordinate. It also does
not give compatibility across independently supplied families.

On the primary time-orthogonal family, direct pullback gives

    h=diag(-e^{-2phi}, e^{2phi}v^2+r^2 b^2),
    m^2=v^2+e^{-2phi}r^2 b^2, Phi(s)=phi(r(s)).

At a radial turn v=0 the density remains positive when r>0 and b is nonzero;
at a pure angular segment, tape accumulates while Phi stays constant. The
zero-tangent case is excluded. The derivative dPhi/ds=phi'(r)v/m explains
the angular dependence on completed separation without a post-readout score.
This does not establish a metric-space distance, selected family, singular
completion, or numerical X_max.

The principal seam to guard is common scale. For hhat=Omega^2 h, the arbitrary
control scalar cancels Omega, but the completed construction gives

    mhat=Omega^2 m, Phihat=Phi-log Omega.

Thus G166's control cancellation must not be used to erase the common scale
in G176–G180. Nor does sensitivity select its supplied profile. These two
statements are compatible after the query type is made explicit.

## 3. Null-clock comparison and full-frame composition

For a smooth regular branch of affinely parametrized null geodesics connecting
proper-clock curves, let J be a connecting variation and k the null tangent.
Torsion freedom and geodesicity give
d[g(k,J)]/d lambda=g(k,nabla_J k)=J[g(k,k)]/2=0. With source proper time as
variation parameter and fixed affine parameter endpoints, endpoint variations
are u_e and Z u_o. Hence

    Z=d tau_o/d tau_e=(-g(k_e,u_e))/(-g(k_o,u_o))>0.

This reconstructs G220/FSL1 independently of a PASS label. A smooth regular
branch and matched affine normalization matter. It is a conditional null query;
the microscopic light law, physical query population and full G176 pair plane
are not supplied by this proof. Finite source durations require integrating Z.

Using proper endpoint frames, P transports k and is metric. Lambda=E_o^{-1}PE_e
is Lorentz and future preserving; it lies in SO^+ when endpoint spatial
orientations are consistently chosen along the path. The original FSL1 frame
repair is essential to that determinant claim, though the frequency identity
does not need determinant +1. Define

    Lambda(1,n)=f(Lambda,n)(1,A(Lambda,n)).

The future time component f is positive and equals omega_o/omega_e. Applying
two matrices proves

    f(L2 L1,n)=f(L2,A(L1,n)) f(L1,n).

The independent exact noncollinear example gives f=1877/375; dropping the
intermediate direction instead gives 3939/625. This is a nonvacuous separator.
Inversion with the transported direction gives the reciprocal of f on that
same comparison. A later causal return has other events and generally another
branch, so it is not this inverse theorem.

For c=Lambda e0=(gamma,s), put chi=s/gamma. Metricity gives
gamma=(1-|chi|^2)^(-1/2). Contracting the actual received future null direction
n_o with c gives

    Z=gamma(1-chi dot n_o).

This uses the forward transported source clock; mixing it with G269's inverse
clock convention reverses signs. Applying the formula to W5 requires exactly
the same clocks, arrow, orientation and null query. The vector chi does not
determine full frame carry: our independent right-rotation example leaves the
two input projected clock vectors unchanged while changing their composition.
Thus no general projective-only binary composition law follows.

For rho=artanh|chi|, Cauchy–Schwarz gives e^{-rho}<=Z<=e^{rho}. Equality at
either endpoint has the matching parallel/antiparallel direction. The signed
planar case chi=tanh(alpha)n_o gives Z=e^{-alpha}; it is the exact tanh law on
that stratum, not a formula for arbitrary transverse relations. Separately,
decomposing the target clock into transported source clock, null direction and
screen W gives Gamma=cosh(delta)+(r/2)|W|^2, r=Z. The explicit r=2,W^2=1
separator yields 1/Gamma=4/9 versus sech(delta)=4/5. Calling 1/Gamma the
physical mutual-clock readout retains its source working-interpretation grade.

The FSL1 asymptotic criterion is a theorem with r=|chi| approaching 1:

    Z=sqrt(epsilon/(2-epsilon))
      +[(1-epsilon)/sqrt(2-epsilon)](1-mu)/sqrt(epsilon),
    epsilon=1-r, mu=chi dot n_o/r.

The first positive term tends to zero and the second coefficient to 1/sqrt(2).
This proves the stated infinite, positive finite and zero-limit equivalences;
no asymptotic series or uncontrolled error estimate is required. Conversely
Z->infinity forces r->1 by the rapidity bound. Saturation alone is insufficient:
c=(1+w^2/2,w^2/2,w,0) has norm -1 and Z=1 along n_o=(1,0,0), even as |chi|->1.
It is a supplied flat control, not an excluded physical UDT population. Nothing
here selects a physical distance attachment or realizes the intended X_max.

## 4. DDR, response class and current G312 correction

At a regular Lorentz tangent space, H(u,n)=2(u_flat tensor u_flat+n_flat tensor
n_flat) is trace-free for every orthonormal timelike/spacelike pair. Every such
plane is locally realizable by the exponential-map construction in G311: first
take a short spacelike geodesic, parallel transport u, then launch nearby short
timelike geodesics. At the base point the two derivatives are u,n, so rank two
and Lorentz signature persist after shrinking. This is local kinematic
admissibility, not a claim that every germ belongs to an actual global population.

Our independent rational planes give exact matrix rank nine. All tangents are
trace-free, and the trace-free symmetric space has dimension nine; therefore
their span is the full space, not just a sampled lower bound. Raising both
indices in the metric tensor pairing gives a nine-row balance matrix whose
exact one-dimensional nullspace is diag(-1,1,1,1). Consequently, for the
specified symmetric E, full all-pair DDR is equivalent to TF(E)=0, or E=lambda g.
The all-pair postulate remains owner-provisional, not a deduction from algebraic
F2. A single plane leaves eight shape directions. No conservation or value of
lambda follows from this pointwise annihilator argument.

An inherited displayed sign needs correction if reproduced. G310 section 3
writes the boosted half-tangent cross term with a negative coefficient in the
covector basis. For u'=C e0+S ei and n'=S e0+C ei, direct expansion gives

    H(u',n')/2-(C^2+S^2)H(e0,ei)/2
      =+2CS(e0_flat tensor ei_flat+ei_flat tensor e0_flat).

Its coordinate 0i entry is -2CS because e0_flat=-dt. Thus the printed covector
coefficient confuses the coordinate sign with the basis coefficient (with a
normalized symmetric-product convention, the magnitude also rescales).
The rank-nine result and annihilator survive. Smallest repair: use the explicit
two outer products above or give coordinate components. Original source bytes
are preserved; this does not justify regrading its theorem.

The positive G301 chain is also conditional and inspectable. A degree-one map
F on a star-shaped curvature domain, differentiable at 0 with F(0)=0, obeys
F(K)=DF_0(K) by taking t down to 0 in F(tK)/t. Differentiability, not just
directional derivatives, makes DF_0 linear. Unoriented Lorentz naturality then
reduces the linear map to metric contractions: Ric and Rg are the two types;
antisymmetric contractions vanish and other placements reduce to these.
This invokes the standard orthogonal invariant-tensor theorem as in the source;
its general proof and source 1200-by-200 certificate were not independently
replayed here. Their hypotheses cannot be replaced by locality alone.

Inside E=a Ric+b Rg with constant coefficients, TF(E)=a(Ric-Rg/4) exactly.
The check independently retains all ten tensor components. With a nonzero,
DDR implies Ric=Rg/4; Bianchi gives dR/2=dR/4 and therefore dR=0 on the
connected regular region. With a=0, DDR is vacuous. This fixes a trace-free
equation and a connected scalar datum, not an action, source or its magnitude.

Current G312 authority is decisive: GR is FILTER ONLY, not full quiet principal
response overlap as a construction premise. Local Metric Sufficiency remains
affirmed owner-provisional, but does not select order, tensor type, scaling or
nondegeneracy. Therefore class membership is unclosed; the conditional Einstein
mathematics survives. Old G312 language saying two additional premises are
required, or old W3 language treated as current full-GR building authority,
cannot replace the 2026-09-09 correction. No necessity for a new physical
postulate follows merely from this route remaining unclosed.

## 5. Conservation and action: constructive survivor and obstruction

For a specified smooth trace-free S on a fixed supplied Lorentz metric, every
same-shape representative is E=S+qg. Metric compatibility gives div E=j+dq,
j=div S. On a contractible neighborhood a smooth q exists exactly when dj=0;
necessity is d squared=0 and sufficiency is the Poincare lemma. On a general
domain exactness and periods matter. A primitive on each fixed metric does not
establish a natural finite-jet operator q[g], nor any variationality.

For S=a(Ric-Rg/4), constant a, Bianchi gives j=(a/4)dR, whence
q=-aR/4+C and E=aG+Cg. For universal a,C, inverse-metric variation of
integral sqrt(|g|)(aR-2C) yields that representative, with boundary terms absent
for compact support. DDR still imposes TF(E)=0; it does not impose E=0 or
stationarity under unrestricted variations and does not choose C or R.

The obstruction is substantive. For S=TF(R Ric), direct differentiation gives
j_b=Ric_ab nabla^a R. Independently building Christoffels, Ricci and covariant
divergence from all metric components of g=diag(-N^2,1,1,1) reproduces
dj_xy=16/3 at x=y=1 for N=1+x^2+y^3. A different supplied witness
N=2+x^2+y^4 gives dj_xy=-27/4 at that point. Both metrics are regular locally.
No scalar trace completion exists near either point. The counterexample is
outside the weight-zero/nondegenerate-flat-response class and is not a claimed
admissible UDT response. Testing only S=0 would miss this off-shell obstruction.

An assumed local metric-only diffeomorphism-invariant action supplies div E=0
by compactly supported infinitesimal diffeomorphisms and integration by parts.
Tensor covariance alone does not. The source's order-at-most-three inverse-
variational theorem is cited conditional mathematics, not independently proved
or checked against its external paper in this review; it must retain all its
natural/symmetric/tensor-density/off-shell smoothness hypotheses and cannot be
globalized to arbitrary finite order. The CRV1 same-action density correction
is independently checked: for inverse-metric E_ab, the covariant-metric Euler
density is -sqrt(|g|)E^ab. The plus sign corresponds to the opposite action.

These constructions leave physical response identification and an off-shell
conservation requirement open. G351 label-measure conservation is a different
object; no connection to tensor divergence is supplied by these arguments.

## 6. Evidence, exclusions and direct-review targets

Two captured independent scripts passed: 55 exact core assertions and 13 exact
conservation assertions. Counts include orthonormality and setup checks, not
68 separate scientific results. The core run used about 51 MiB and 0.27 seconds;
the conservation run about 48 MiB and 0.53 seconds, each capped at 60 seconds/
512 MiB, numerical threads 1. See saved stdout/stderr, metadata and machine JSON.
No failed run occurred. Explicit wrong-rule separators reject dropped null
direction, projective-only composition, conflated completed/control scale,
printed covector sign and covariant-variation plus sign. They are mathematical
separators, not claims of mutation coverage of parent maintenance machinery.

Not repeated: old large censuses, old reviewer scripts, full curvature-natural
classification certificate, external inverse-variational theorem proof,
observational/raw-array reanalysis, manifold/global existence, numerical PDE,
mass/carrier/stability or protected work. Source grades remain as registered;
G166/G176 original caveats are retained despite new bounded reconstruction.

Direct manuscript review should test these seams explicitly:

1. F1–F4 character/readout assumptions versus physical depth assignment.
2. Fixed clock typing, control scalar and completed normalization, common scale.
3. Supplied germ/family versus selected history; same-family versus network carry.
4. Scalar clock contrast versus W5 vector and full null ray/frame carry.
5. Actual received ticks versus transported-clock mutual-readout interpretation.
6. Algebraic reciprocity versus owner-provisional DDR; current G312 class gap.
7. Conditional Einstein geometry versus response representative/action adoption.
8. Fixed-metric primitive versus natural operator; conservation versus G351 labels.

The source-first seal is a correspondence receipt, not a proof of chronology,
scientific truth or adoption. Later direct exposure must be recorded separately.
