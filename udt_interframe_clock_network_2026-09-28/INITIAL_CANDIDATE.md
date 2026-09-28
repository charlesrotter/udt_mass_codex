# ICN1 — two-way proper-clock data, radar geometry and network scope

Initial conditional candidate for adversarial review; UNPROMOTED.
WORK_ORDER controls. No field equation, source law or new physical premise is
adopted. The construction uses ordinary proper clocks throughout. It tests the
actual physical comparison protocol instead of equating one measurement with E.

## 1. Events, clocks and the conditional signal protocol

Let A,B,C be supplied freely falling timelike clocks in a smooth time-oriented
Lorentz4 geometry. Their parameters are proper times in seconds, with the same
observed c_E calibration. Select smooth future-null geodesic incidence branches
on a regular domain without caustic/branch switching. W4 coupling remains
WORKING/POSIT and G220's null-query interface remains conditional; the following
does not construct a microscopic light or instrument theory.

Write f_AB(s)=b for reception at B of emission s at A, and f_BA(b)=a for
reception at A of a signal emitted at B at b. These are distinct future maps.
Their positive derivatives are the existing G220 proper-interval ratios:

    p(s)=f_AB'(s)>0,       q(b)=f_BA'(b)>0.                 (1)

An ideal immediate relay pairs B's reception with emission at that SAME event.
It identifies the two infinitesimal proper-time intervals of its timing record;
it does not parallel-transport the incoming null tangent into the outgoing one.
The outgoing direction and null branch are separately specified. Define

    F(s)=f_BA(f_AB(s)),       F(s)>s,
    P(s)=F'(s)=p(s) q(f_AB(s))>0.                          (2)

G220 applies independently to each leg. The product follows from the chain rule
on the relayed event map, not from falsely treating a broken ray as one free ray.
For a known relay map b_out=l(b_in), replace F by f_BA(l(f_AB(s))) and P by
p l' q at the corresponding events. Even a constant positive waiting time changes
where q is evaluated. Variable latency contributes l' and cannot be called
positional dilation. The zero-latency protocol is a declared ideal query.

## 2. An operational separation and a necessary redshift restriction

For B's relay event define A's radar time and radar distance

    T(s)=[s+F(s)]/2,       R(s)=c_E [F(s)-s]/2.            (3)

T'>0, so T is a valid local parameter on these relay events. Direct
differentiation yields

    beta_rad := (1/c_E)dR/dT = (P-1)/(P+1),
    S := (log p + log q)/2,
    beta_rad=tanh S,       P=(1+beta_rad)/(1-beta_rad).    (4)

q in this section is evaluated at f_AB(s). Thus |beta_rad|<1 within the regular
domain. This is a radar-distance derivative, not automatically a local relative
velocity, projective position or independent propagation speed. Choosing A for
radar coordinates is a measurement choice, not a preferred physical observer.

Whenever BOTH actual legs have net received redshift, p>1 and q>1, equation(4)
forces dR/dT>0. A zero radar-distance derivative requires pq=1 and therefore
excludes strict net redshift on both matched legs. Conversely pq>1 does not
imply both p,q>1. This is a precise restriction on those observations, not a
theorem that every UDT observation is net redshift. No separately isolated
positional factor has been derived. Doppler and gravitational contributions stay
in the same metric/clock map; they cannot be divided out by declaration.

This relation is standard operational/kinematic geometry applied to the current
comparison. It does not establish Hubble expansion, physical recession of matter,
a distance-only redshift law or a native UDT metric. It does give a directly
stated consequence any candidate admitting this two-way protocol must respect.

## 3. What the two ratios separately recover in a declared longitudinal sector

For this section ONLY, assume the two clocks and both null branches lie in one
smooth totally geodesic Lorentz2 surface with valid double-null radar coordinates.
This is a conditional longitudinal sector, not a reduction of arbitrary4D
geometry or permission to drop angular/screen data. It may be embedded as the
totally geodesic factor of an explicit4D product control. In this sector,

    g_2=Omega(T,R)^2[-c_E^2 dT^2+dR^2],    Omega>0.        (5)

A is R=0, its proper-time normalization gives Omega(T,0)=1, and A's free fall
gives partial_R Omega(T,0)=0. On the selected side, outgoing and returning
null labels are s=T-R/c_E and a=T+R/c_E. If B has radar trajectory R(T),
its ordinary proper time satisfies

    db/dT=Omega_B sqrt(1-beta_rad^2),
    p=Omega_B sqrt[(1+beta_rad)/(1-beta_rad)],
    q=Omega_B^(-1) sqrt[(1+beta_rad)/(1-beta_rad)].         (6)

Consequently the data recover

    Omega_B=sqrt(p/q),    K:=(log p-log q)/2=log Omega_B. (7)

Omega_B is a metric coefficient in A's radar coordinates. It is not an anomalous
intrinsic ticking rate at B. Equation(6) derives its normal proper-time conversion
from the same metric. For arbitrary4D paths equations(2)-(4) still hold, but
sqrt(p/q) is only a timing diagnostic unless the additional sector hypotheses
needed for (5)-(7) are established.

Free fall of B also restricts the first derivatives of this metric. Put
phi=log Omega and let a dot denote the derivative along B with respect to T.
The T-parametrized geodesic equation of (5) is

    dot beta=-(1-beta^2)(c_E partial_R phi+beta partial_T phi).

Using beta=tanh S and dot K=partial_T phi+c_E beta partial_R phi gives

    partial_T phi|B=(dot K+beta dot S)/(1-beta^2),
    c_E partial_R phi|B=(-dot S-beta dot K)/(1-beta^2).    (8)

Thus two-way timing and its drift recover a metric value and first derivatives
along this specified free-fall curve within the sector. This is a constructive
data-to-geometry relation; it does not prescribe the data. Accelerated B requires
its actual acceleration terms and cannot silently use (8). A dense compatible
family could be tested for mixed-partial integrability; three separated curves
do not supply those transverse derivatives or an interior evolution equation.

No exact-reciprocal coordinate gauge is imposed on (5). Setting its determinant
to -c_E^2 by fiat would erase Omega. A coordinate/cell normalization is not the
physical equation determining the geometry.

## 4. Relation to the existing kernel and full frame information

Each actual leg separately has its G220/G176 same-correspondence clock leg

    delta_clock,AB=-log p,       delta_clock,BA=-log q.    (9)

These are associated with different event pairs. There is no requirement that
their sum vanish. The inverse of f_AB is not the future map f_BA. Equation(4)'s
S is minus one half the sum of THESE clock depths; resemblance to the terminal
tanh kernel does not identify beta_rad with W5's complete projective vector or
with either leg's scalar chi_clock. Sign, event, direction and object all matter.

FSL1 gives each leg's readout from its own full transport, matched frames and
actual reception direction. At a relay, an outgoing null direction is new query
data. Neither multiplying clock ratios nor knowing sqrt(p/q) constructs the
complete G176 pullback or the transverse/mixing/frame data it requires. The
radar construction attaches an explicit operational separation to this physical
query; it does not define W5's distance attachment universally.

## 5. Third-observer consistency without false path closure

For an immediate A-to-B-to-C relay,

    H(s)=f_BC(f_AB(s)),       H'=Z_AB(s) Z_BC(f_AB(s)).     (10)

Use actual intermediate events and outgoing directions. Further relays compose
associatively with the correct arguments, and their positive slopes multiply.
For a separately supplied direct A-to-C signal f_AC, define

    Delta(s)=H(s)-f_AC(s),
    Delta'=Z_AB Z_BC-Z_AC.                               (11)

On a causally convex domain where f_AC is the earliest causal arrival, a broken
future-null route cannot arrive before it, so Delta>=0. There is no general sign
restriction on Delta'. Neither equality of routes nor unity of loop products
follows. For a closed causal relay loop ending at A, F_loop(s)>s and the product
of its leg slopes is F_loop'; it is not the identity on one event at A.

An exact three-free-clock Minkowski control shows why derivative signs matter.
In c_E=1 units let A:x=0, B:x=2, C:x=1+v t, |v|<1, with C proper time t/gamma.
For a bounded emission interval about s=0 on which the stated paths are valid,

    f_AC(s)=(s+1)/[gamma(1-v)],
    H(s)=(s+3)/[gamma(1+v)],
    Delta'=-2 gamma v.

At v=+1/5 or -1/5, Delta(0)>0 in both cases but Delta' has opposite signs.
All clocks are inertial/free, and rays are the actual direct and relayed null
segments. This refutes an inequality for slopes inferred merely from a positive
arrival delay. It is not a native cosmology or a source of a physical UDT law.

Equations(10)-(11) are useful consistency checks, not a new geometry selector.
The founding network-potential and FSL1 composition warnings remain valid.

## 6. What a finite timing network cannot reconstruct by itself

Let a finite collection of free proper-clock worldlines and their null branches
be contained in a regular domain with an open region away from the worldlines.
Choose a smooth function psi with compact support in such a region, and let

    g_tilde=e^(2 psi) g.

The metrics agree on neighborhoods of every clock, including all local metric
jets. The clocks keep the same proper times and geodesic motion. Conformal
rescaling preserves unparametrized null geodesics and causal incidence. All
actual clock maps f_ij, their slopes, relayed routes and radar records therefore
coincide on the common regular domains, although interior curvature can differ.
Use sufficiently small deformation/regular domains when needed to preserve the
selected smooth branches. The result is a supplied-geometry comparison, not a
pair of metrics proved to satisfy every native UDT constraint or physical DDR.

For an explicit curvature check take flat g and, near an interior point away
from the clocks, psi=k(x-x0)^2, joined to zero with smooth cutoffs equal to one
on that small patch. At x=x0, psi=0, dpsi=0 and the four-dimensional scalar
curvature of g_tilde is -12k in c_E=1 length coordinates, whereas flat g has zero.
This follows either from direct Christoffels or the conformal curvature formula.
The compact smooth patch construction, not a global polynomial assertion, owns
the agreement on every clock neighborhood.

This establishes a specific ambiguity in reconstructing interior geometry from
a finite timing network, even when complete time records are available. It does
NOT prove nonuniqueness of a redshift law under all UDT premises, since the two
controls have the same timing records and native admission is unproved. Nor does
it claim full pair/frame/screen/tidal blindness. Additional justified information
or existing native constraints may distinguish them; none is invented here.

## 7. Nearby and limiting consequences

With S,K defined from positive p,q, exact algebra gives

    both p>1 and q>1  iff  S>|K|;
    both p,q -> infinity  iff  S-|K| -> infinity.          (12)

The latter forces beta_rad->1 but the converse fails: p=n^2,q=n^(-1) has
P=n and beta_rad->1 while q->0. These are algebraic controls, not physically
realized UDT families. Echo availability may fail at a limiting horizon; no
extension through a missing return branch is asserted. Nothing in (12) fixes
the limiting radar distance, observer proper time or X_max realization.

In the extra longitudinal sector, A's normalization/free fall give phi(T,0)=0
and partial_R phi(T,0)=0. If phi is C3 in R with |partial_R^3 phi|<=M on the
chosen compact interval, Taylor's theorem gives

    |phi(T,R)-[partial_R^2 phi(T,0)/2] R^2|<=M |R|^3/6.   (13)

This controlled nearby statement concerns the radar metric factor, not the
complete pair depth or the whole redshift. B can have a nonzero initial Doppler
contrast. At a moment when beta_rad=0, p=Omega_B and q=1/Omega_B; strict mutual
net redshift then fails in this sector. No solar detectability threshold or
general vanishing of finite-separation effects follows from (13).

## 8. What accepted c_E and G_obs supply

c_E already turns measured proper round-trip duration into R in (3); it is an
accepted calibration, not a fitted redshift scale. G_obs is equally allowed as
an input. In ordinary length/time/mass dimensions,

    [c_E]=L T^-1,       [G_obs]=L^3 M^-1 T^-2.

A monomial c_E^a G_obs^b has dimensions L^(a+3b) T^(-a-2b) M^(-b).
For a length, the mass condition requires b=0 and the time condition a=0,
contradicting a+3b=1. More generally, a unit-covariant length function of only
these two constants must be independent of G under arbitrary mass-unit rescaling,
and then independent of c under time-unit rescaling; it cannot have length weight.
The same argument excludes a nonzero intrinsic time from these inputs alone.
Dimensionless coefficients do not resolve the missing dimension.

This does not diminish either input or prevent their use once the geometry/data
provide another dimensional quantity. A measured duration gives c_E Delta tau.
IF a separately justified mass M becomes available, G_obs M/c_E^2 has length
dimension; IF a density rho is justified, c_E/sqrt(G_obs rho) does. These are
dimensional possibilities only, not adopted source laws, coefficients, horizon
radii or permission to open the paused matter/source lane. Neither is added to
the current calculation. A scale from measured data or free integration data
remains calibrated/supplied until the theory fixes it.

## 9. Maximum conclusion and remaining connection

We have an actual two-way interframe protocol, exact radar-distance/clock-ratio
restriction, conditional longitudinal metric/gradient reconstruction, and precise
third-observer and scale limits. Local proper clocks stayed ordinary throughout.
The physical comparison now has explicit events and an operational separation;
the full native pair assembly and a law selecting its separation dependence are
still OPEN. This pass neither demands a local E identification nor supplies a
replacement mechanism. It does not prove that another physical postulate is needed.

## Method credit and discovery

Radar time/distance and their regular-domain qualifications are standard methods:
Volker Perlick, On the radar method in general-relativistic spacetimes,
https://arxiv.org/abs/0708.0170 , sections1-3. We use the measurement definition
with proper clocks, not that paper's physical spacetime examples or field laws.
All algebra and sector qualifications used here are explicit above. Constants'
dimensions agree with NIST's SI entries; no numerical G estimate is used.
The candidate was developed analytically before exact controls and freezing.
The echo/dimensional route was disclosed before source-first review; the
longitudinal reconstruction and finite-network conformal control arose during
this authorized construction. No observed outcomes or fitted curves entered.
