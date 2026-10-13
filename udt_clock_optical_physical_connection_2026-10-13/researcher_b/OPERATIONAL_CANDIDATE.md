# COC1 B — radar calibration and a directional optical trial

Exploratory candidate, unadopted and not yet adversarially reviewed. Initial
proposal and probe freeze preserve discovery order. This file supplies a focused
argument to the coordinator; it is not another maintained scientific summary.

## 1. What can be measured without an affine-distance assumption

Use W4's WORKING/POSIT common Lorentz metric for proper clocks/rulers, freely
falling clocks and null rays. Fix a smooth Lorentz4 metric and a freely falling
central clock gamma, with p=gamma(0), U=dot gamma(0). Work inside a sufficiently
small causally convex normal tube, with regular outgoing/return branches and no
caustics. In c_E=1 length units choose q=gamma(2l), and let S_l be the intersection
of the future light cone of p with the past light cone of q. Every point of this
cut is an ideal immediate-relay event for the same measured round-trip proper
interval2l. No distant clock synchronization is needed to specify that cut.

Supply its proper area density dA_l/dOmega, labeled by the source's ordinary
solid angle. This requires ideal local ruler/screen-area information; tick
ratios or unresolved source brightness alone are NOT this measurement. The
construction does not use a photon conservation, flux, luminosity or matter law.
The rulers/relays and central free fall are explicit query preparation, not an
assumed natural population. No second spacetime is needed for these TOTAL data.

Define e(U,n)=g(R(n,U)U,n) for unit n perpendicular to U, k=U+n, and rho(k)=Ric(k,k).
Use R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]. A source-normalized affine lambda obeys
-g(k,U)=1 at p. It is only an intermediate proof coordinate, not an input to
the proposed measurement.

In Fermi coordinates about gamma, the radial quadratic metric terms are
g00=-(1+e r^2), g0n=0, gnn=1; omitted terms are smooth cubic jets. Contracting the
null geodesic equation along its initial spatial direction gives

    t(lambda)=lambda-e lambda^3/3+O(lambda^4),
    r(lambda)=lambda-e lambda^3/6+O(lambda^4).

Transverse ray deviations begin at O(lambda^3) and affect radial travel time
only beyond the cubic term. For the return ray, the same frozen quadratic jets
give t_return-t_out=r-e r^3/6+O(r^4). Thus

    l=r-e r^3/6+O(r^4),
    lambda=l+e l^3/3+O(l^4).                         (B1)

The screen Jacobi equation J''+QJ=0, J(0)=0,J'(0)=Id, gives
det J=lambda^2[1-rho lambda^2/6+O(lambda^3)]. Replacing a fixed-affine cut with
lambda(l,n) adds a generator component to angular tangent vectors; it does not
change their induced inner products because the generator is null and orthogonal
to the screen. Therefore actual radar-cut area obeys

    dA_l/(l^2 dOmega)=1+a(U,n)l^2+O(l^3),
    a(U,n)=[4e(U,n)-rho(U+n)]/6.                   (B2)

This is a local asymptotic identity for each fixed frame with smooth bounded jets,
not a finite-distance error certificate. The remainder can be uniform on the
compact sky for that fixed frame; no uniformity under unbounded boosts is used.
PSW1 independently reads e=-lim 2log(p_L)/L^2 in its parallel-prepared released
clock experiment. Combining that measured coefficient with radar area yields

    Ric(U+n,U+n)=4e(U,n)-6a(U,n).                  (B3)

Thus a source-normalized affine focusing coefficient can be RECOVERED from
specified clock/angle/proper-area records without presuming the affine cut or
a whole supplied geometry. This remains ideal geometric tomography, not an
instrument proposal or physical attribution of the result to positional effects.

The calibration matters at exactly this order. Under an otherwise unspecified
s=lambda+b(n)lambda^3+O(lambda^4), normalized area acquires coefficient
-rho/6-2b. Matching s/lambda->1 does not fix it. B1 supplies the required cubic
correction from a concrete proper-time protocol. Blindly substituting radar
range for affine distance would infer rho_wrong=rho-4e.

## 2. A scalar measured by total radar-cut area

Average B2 over the source sky. In Lorentz4,
mean e=Ric(U,U)/3 and mean rho=(Scal+4Ric(U,U))/3. Hence

    Area(S_l)=4pi l^2[1-Scal(p)l^2/18+O(l^3)],
    Scal(p)=-18 lim_(l->0) [Area(S_l)/(4pi l^2)-1]/l^2.    (B4)

The leading scalar is independent of U. Replacing p by gamma(l), the midpoint,
changes only the stated remainder. The Euclidean coefficient4pi is tangent-space
normalization supplied by local SR/metric geometry; it is not an independently
selected reference universe. The TOTAL invariant is measured; its origin or
division into ordinary and additional effects is not.

Gibbons–Solodukhin hep-th/0703098v3 section3 eq29 already proves this known
small-Alexandrov-diamond area formula. The independent Fermi calculation above
adds the directional calibration needed here; it is not a literature novelty
claim. Wang1904.01034v2 distinguishes this cut from affine and geodesic-ball cuts.
No Einstein/matter interpretation in either paper is imported. COC1's parent
also identified prior repository CMF1 all-clock scalar recovery; B4 is an
alternative operational method, not a new geometry-selection result.

Controls are decisive for interpretation. In ultrastatic g=-dt^2+h_K, with h_K
constant spatial curvature K>0, all static initially parallel freely falling
clock rates and their signal arrival derivatives equal1. Yet Scal=6K and
Area=4pi sin^2(sqrt(K)l)/K has a leading deficit. B4 is therefore not automatically
a received-slowing observable. For a uniformly accelerated Minkowski clock with
proper acceleration a0, endpoints at proper times +/-l have edge area
4pi sinh^2(a0 l)/a0^2. Using its clock duration in B4 would spuriously return
-6a0^2 although Scal=0. Central free fall is essential preparation, not cosmetic.

## 3. A concrete operational version of GRC1's optical choice

Now SUPPLY a physically matched reference as in GRC1/PSW1: metrics g,g0, matched
events and time-oriented tangent isometry, same units/proper clock preparation,
same l and source directions, each experiment performed in its own geometry.
Write Delta e, Delta rho, Delta a for differences under that fixed matching.
The reference remains supplied. B2 gives

    6 Delta a(U,n)=4 Delta e(U,n)-Delta Ric(U+n,U+n).       (B5)

**RA1, UNADOPTED physical trial:** for EVERY future unit U and spatial unit n,
Delta a(U,n)<=0. Physical meaning: no extra leading growth of the directional
proper area density on the same round-trip-clock cut in any prepared laboratory.
This is stronger than an angular-average statement, one lab's area deficit or
ordinary optical reciprocity. Its invented motivation is to express a candidate
no-extra-spreading condition entirely in declared clock/area data, without an
unobservable equal-affine-cut prescription. Whether positional physics satisfies
RA1 is OPEN; it is not derived from the founding interpretation.

First informative test is exact equivalence or inequivalence to the already
explored S+F choice. It gives a precise answer:

    RA1  iff  [Delta e(U,n)<=0 for every U,n
               and Delta Ric(k,k)>=0 for every null k].   (B6)

Proof. For a fixed timelike plane, boost U_eta=cosh(eta)U+sinh(eta)n and
n_eta=sinh(eta)U+cosh(eta)n. Their simple bivector is unchanged, so Delta e is
unchanged; k_eta=U_eta+n_eta=exp(eta)k. RA1 implies

    4 Delta e - exp(2eta) Delta rho <=0 for every finite eta.

Taking eta->-infinity forces Delta e<=0; taking eta->+infinity forces
Delta rho>=0. These are finite-dimensional limits of already extracted local
coefficients, not a common finite experiment at infinite boost. Conversely those
two inequalities immediately give B5<=0 in every frame.

The right side is exactly GRC1's S+F. Its inspected algebraic-curvature proof
therefore gives

    RA1 iff D=kappa B_g, kappa>=0,                         (B7)

with D the matched curvature tensor difference and
B_g(X,Y,Z,W)=g(Y,Z)g(X,W)-g(X,Z)g(Y,W). This is a conditional operational restatement
of the old restricted class, not a native derivation or reduced physical strength
merely because two inequalities were packaged into one. Regional realizability,
matching/Bianchi, reference attribution and scale retain GRC1/PCC1's limits.

The distinguishing probe is substantive: a one-frame directional radar deficit
is NOT enough. GRC1's inspected local spherical tensor (alpha,beta,gamma)=(6,2,1)
has, in its unboosted frame, Delta e=-2-4n1^2 and Delta rho=-5+5n1^2, hence
Delta a=-(3+21n1^2)/6<0 across that sky. On a tangential timelike plane,
Delta e=-2,Delta rho=-5; a collinear boost exp(eta)=2 gives Delta a=2>0.
The proposed universal operational law would reject this wider S-only witness.

Replacing RA1 by a requirement only on TOTAL/sky-mean area gives merely
Delta Scal>=0, by B4. It cannot replace GRC1's F, and it does not recover the
Einstein Ricci class. Thus an operational optical condition must specify whether
it controls area density in every direction/frame or only the total area.

## 4. Return and exclusions

The positive gain is access and a discriminator: clock-defined radar cuts remove
the arbitrary affine-distance calibration, and a universal directional area
inequality has exactly the previously known S+F strength. Neither gain selects
the reference or identifies the measured total scalar with additional positional
physics. The ultrastatic control defeats that naive identification outright.
The next physical decision concerns RA1's attribution and every-laboratory
quantifier, or an independently justified weaker alternative. Another supplied
metric profile or an unresolved-brightness calculation will not make that choice.

No new field equation, matter/light constituent, flux law, physical population,
boundary, numerical geometry search, preferred observer, CANON or registry grade
is proposed. Exact checks below support finite controls; the general argument
and hypotheses require fresh source-first review. Initial proposal bytes remain
preserved. One CPU slot will be used for the frozen short exact controls only.
