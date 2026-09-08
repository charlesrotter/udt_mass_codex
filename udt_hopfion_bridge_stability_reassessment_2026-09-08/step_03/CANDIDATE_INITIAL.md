# HB3 initial conditional candidate — closed orbits versus smooth lines

UNREVIEWED, UNPROMOTED. Discovered after HB2 review; no physical carrier,
time-trajectory or stability theorem. QUESTION.md owns the prior scope.

## 1. Data, mathematical import and quantifiers

Use EXACT HB2 globally simple-gap, strict-root G331/G332 data on compact S3:
positive weights w1,w2, gamma_w, unit Killing xi=w1*d_phi1+w2*d_phi2,
eta=xi-flat, R=scalar(gamma), Delta=(6-R)/2 nowhere zero, and

    D0=b+C=epsilon sqrt[2(R+2C^2-2Lambda)],
    K=((C-b)/2)gamma+b eta^2,          epsilon=+1 or -1.

The radicand is strictly positive globally. C and finite Lambda are supplied
compatible data, not freely retunable once gamma,K are fixed. The unscaled
weighted-contact family is an admitted initial-data restriction, not selected
physical content. G310/G312 remain owner-provisional premises. Conditional on
the imported smooth marked Einstein-Cauchy existence/uniqueness and standard
isometry-extension consequence, take the local development in its Gaussian
normal collar, gamma-dot=-2K. G321 supplies the scoped interface, G330 explains
the general imported isometry method; neither is a proof of that PDE theorem.

Let P(t) denote the continued simple SPATIAL Ricci projector. Compactness,
smoothness and the initial uniform gap give it on some datum-dependent
two-sided collar. An orbit below means an integral curve of its line IN ONE
SPATIAL SLICE. It is not a physical time trajectory or a particle worldline.

Candidate: for ANY unequal positive weights in this strict class, there is
delta>0 such that, for EVERY0<|t|<delta, there are interior invariant tori
with closed line orbits and other interior tori with nonclosed orbits dense
in that torus. The tori may depend on t. This is not an assertion about any
one fixed torus at all times, all leaves, typicality or a uniform time bound.

For unequal rational w1/w2 every initial orbit is closed, but the all-closed
property consequently fails at every sufficiently small nonzero time.
Unequal rational weighted circles are generally exceptional-fibre Seifert
orbits, NOT an ordinary free Hopf bundle. For equal weights w!=1 the whole
local line is the Hopf line and retains its closed fibres while the gap remains
open. Thus all-closed persistence on a local interval, within this exact
family/domain/import, is equivalent to equal weights. This is not a statement
about arbitrary metric data or the independent old Hopfion carrier.

## 2. The actual development retains the needed symmetries

The initial metric is invariant under the standard angular T2 action and
simultaneous complex conjugation c:(phi1,phi2)->(-phi1,-phi2). R,b are
invariant; eta changes sign under c but eta^2 does not. Therefore BOTH gamma
and K, not merely gamma, are invariant. The imported isometry-extension
consequence applies to this complete initial datum. In normal coordinates the
extended transformations commute with normal geodesics and preserve time;
their spatial actions are the normally carried initial ones. Use a sufficiently
small common collar; the symmetry group is compact. No chosen non-Einstein
auxiliary metric curve is substituted for the actual development here.

On any compact interior annulus 0<a<=x<=b<1 the T2-invariant coefficients are
functions of t,x only. Conjugation forces gamma_x,phi_a=0. Tensor covariance
forces the same block splitting for Ricci and its raised endomorphism B(t).
Equivalently, after a compensating torus translation the conjugation fixes
each point with tangent action diag(1,-1,-1). The simple spectral line is an
eigenline for that involution. Initially it is in the negative, angular
eigenspace; continuity keeps it there for small time. It cannot change to
the radial eigenspace without violating continuity of that simple line.

Hence P(t) is tangent to each torus. A smooth T2-invariant unit representative
can be constructed as P(t)*d_phi2 divided by its norm. Initially its sign agrees
with xi since eta(d_phi2)=(1-x)/F>0, where F=w1*x+w2*(1-x). On a compact
annulus it remains nonzero and its phi2 component remains positive for a
uniform small interval. Write this representative V(t,x), and define

    q(t,x)=V^phi1(t,x)/V^phi2(t,x),       q(0,x)=w1/w2.          (1)

This ratio is independent of the representative's normalization/sign. On a
fixed torus its two components are constant, so its flow is the usual linear
torus flow. With the fixed2pi angular lattice, rational q means closed curves;
irrational q means nonclosed curves dense in that torus. These are elementary
torus-flow facts, not a new UDT transfer law. Integral changes of torus basis
preserve the closed/nonclosed classification. No observation is asserted.

## 3. Derive the rotation-ratio derivative, not just component drift

The reviewed HB2 formula is

    Y=Pi V-dot=5 A(grad b)/(2 Delta),       A(X)=D_X xi,
    V-dot=Y+(C+b)xi/2,       db=dR/D0.

The parallel term cancels when differentiating (1). From the initial metric,

    gamma_xx=1/[4x(1-x)F],
    eta=[x/F,(1-x)/F],     eta'=[w2/F^2,-w1/F^2],
    gamma_angular^-1 eta'=[1/x,-1/(1-x)].

Unit Killing gives d eta(X,Z)=2gamma(A X,Z). Substitution yields

    A(grad b)=2F b'[(1-x)d_phi1-x d_phi2],
    q-dot(0,x)=(Y^phi1*w2-w1*Y^phi2)/w2^2
               =5F^2 R'/(Delta D0 w2^2)
               =kappa/(Delta D0),
    kappa=-120*w1*(w1-w2)/w2.                                (2)

R'=-24w1w2(w1-w2)/F^2, as in HB2. All metrics, inverse metrics, parameters
and derivatives in (2) are initial ones. Both strict roots and either gap
sign remain. Flipping D0 flips q-dot, not generally the whole K at fixed C.

For unequal weights, kappa!=0 and R(x) ranges monotonically over a nontrivial
interval. If q-dot were constant on the whole interior, Delta D0 would be a
nonzero constant. Squaring would make

    (Delta D0)^2=(6-R)^2*(R+s)/2,        s=2C^2-2Lambda         (3)

constant on that open R interval. But (3) is a cubic polynomial in R with
leading coefficient1/2, for EVERY finite s. It cannot be constant on an open
interval. Thus q-dot is nonconstant in x. No choice of C, Lambda or root in
the strict class removes this dispersion. The proof does not require q-dot'
to be nonzero at every point; isolated critical points are allowed.

## 4. From a first jet to an actual local-time orbit conclusion

Choose two interior points x_a,x_b with q-dot(0,x_a)!=q-dot(0,x_b), possible
by Section3, and take a compact annulus containing them. Smooth development,
the symmetry argument and the continued gap give the smooth ratio (1) there.
Since q(0,x_a)=q(0,x_b), Taylor differentiation at these TWO FIXED points gives

    q(t,x_a)-q(t,x_b)
       =t*[q-dot(0,x_a)-q-dot(0,x_b)]+o(t).                   (4)

For all sufficiently small nonzero t, (4) is nonzero. At each such fixed t,
continuity in x gives a nondegenerate interval of attained slopes between
these two values. That interval contains rational and irrational numbers.
The corresponding invariant tori have respectively closed and dense nonclosed
line orbits. This proves the stated time/point quantifiers. No analyticity,
numerical orbit integration, finite-time estimate or convergence conjecture
has been substituted for smoothness and the intermediate value theorem.

A NONZERO but spatially CONSTANT q-dot would not establish this conclusion.
Nor would nonzero component/projector drift alone. The nonconstant ratio,
inherited block symmetries and two-point argument are essential extra steps.
No conclusion is made about which fixed torus has which type as time varies.

For rational initial w1/w2, every initial torus orbit and both axis orbits
close. At nearby nonzero times, the nonclosed interior orbit already rules
out all-closed structure and any circle-fibre quotient having THIS line as
its fibres. It does not rule out another Hopf map/line on the same S3.

## 5. Equal-weight control and exact scope of the alternative

For w1=w2=w>0 the initial metric is Berger with horizontal coefficient1/w
and vertical coefficient1/w^2. Exclude w=1 (no simple initial Ricci line).
R and b are constant. Both gamma and K, including K's anisotropic eta^2
term, are U(2)-invariant. This is broader than G330's pure-trace example,
but uses the same imported isometry method, not that example as a universal
theorem. Isotropy rotates the horizontal2-plane and fixes the vertical line;
an invariant spatial metric has exactly the two Berger coefficients and no
horizontal-vertical cross term. The actual local development retains U(2),
and therefore this form. Smoothness retains the nonround gap for short time.
Its simple Ricci line is the ordinary Hopf line and all its fibres are circles.
This symmetry argument, not zero first drift by itself, proves preservation.

For a rational unequal ratio p/q in lowest positive terms, the corresponding
effective initial circle action has integer weights p,q. Generic orbits have
period2pi; the two axes have primitive periods2pi/p and2pi/q. Unless p=q=1,
some exceptional isotropy occurs. Thus initial all-closedness is weaker than
a free Hopf action. The negative unequal-weight result must not be marketed
as destruction of the ordinary Hopf bundle of the equal-weight stratum.

## 6. Meaning, omissions and evidence freeze

This is an additional conditional consequence of admitted metric developments,
not of an independently chosen carrier action. It shows why smooth intrinsic
line robustness does not ensure a usable global periodic-fibre quotient in
this data family. The smoothly continued line has no demonstrated topology
change; all slices in the collar still have topology S3. There is no transfer
of the old static finite-box L2+L4 Hessian, no energetic or continuum stability
result and no particle/dynamical-persistence claim. The conditional Einstein
equation is satisfied throughout; loss of a chosen geometric property is not
a failure of UDT. No physical identification, scale or new premise is adopted.

Discovery: after HB2 review the parent examined torus-slope dispersion as a
distinct feasibility question; this proof was written before HB3 reviewer
findings were read. Small exact algebra and saved-quantity checks support
signs, ratios and domain controls, not the general PDE/symmetry/orbit proof.
Fresh source-first separate-context review must assess those load-bearing
implications before any conditional downstream use. Preserve initial history.
