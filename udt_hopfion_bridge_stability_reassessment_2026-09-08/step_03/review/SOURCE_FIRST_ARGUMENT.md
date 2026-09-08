# Independent HB3 reconstruction before author exposure

Conditional on the original G331/G332 definitions, whole reviewed HB2 and
the imported smooth marked Einstein-Cauchy/isometry-extension method.

## Symmetry is stronger than T2 alone

The angular translations preserve gamma and eta, and preserve R,b and K.
Simultaneous complex conjugation j:(z1,z2)->(bar z1,bar z2) preserves x,
reverses eta and zeta, and preserves gamma and K=((C-b)/2)gamma+b eta^2.
It reverses xi but not xi tensor eta. This is a spatial isometry of the
complete data with the same normal orientation, not time reversal.

Apply the general imported smooth Cauchy uniqueness theorem to the marked
embeddings composed with these isometries. The extensions carry initial unit
normals and their geodesics into themselves, so in a sufficiently small
Gaussian tube they act with the SAME time and the original spatial action.
Compact initial S3 permits a datum-dependent common tube. No uniqueness of
physical occupancy and no machine proof of this imported theorem is asserted.

On 0<x<1 torus invariance makes the spatial metric coefficients independent
of both angles. Conjugation changes signs of both angular differentials,
forcing both dx dphi terms to vanish. Thus gamma(t)=a(t,x) dx^2+
H_ab(t,x)dphi^a dphi^b. The same symmetry makes Ricci block diagonal.
The initially simple angular eigenline remains angular: the block projection
commutes with its simple spectral projector, and its rank in the radial block
cannot jump from zero while the gap stays open. This can be applied on each
interior compact strip; the global Ricci gap itself is retained by compactness.
The line is T2-invariant, so on each torus its integral curves have a constant
angular direction. Rescaling a representative changes speed, not its leaves.
At each axis the stabilizer circle rotates the normal two-plane and fixes only
the axis tangent; a real simple invariant line must therefore be tangent to
the axis. The axes remain closed leaves in the common local interval.

## Ratio derivative from the actual metric normalization

Write F=w1 x+w2(1-x), U=(1-x,-x), angular eta=(x,1-x)/F,
zeta=(w2,-w1)/F. Then eta(U)=0, zeta(U)=1, and

    H=x(1-x)/F zeta zeta^T+eta eta^T,
    eta'=(w2,-w1)/F^2,
    H^-1 eta'=U/[x(1-x)].

The Killing identity d eta(X,Z)=2 gamma(A X,Z), with
gamma^xx=4x(1-x)F, gives

    A grad R=2 F R' U.

HB2 then gives the transverse unit-vector derivative

    Y=5 F R' U/(Delta D0),
    V_dot=Y+(D0/2)xi,    V(0)=xi=(w1,w2).

For r(t,x)=V1/V2, differentiating the quotient cancels the D0/2 parallel
term exactly. Positive initial w2 allows this chart on any chosen compact
interior strip for sufficiently short time. The result is

    r_dot(0,x)=5 F^2 R'/(w2^2 Delta D0)
              =-120 w1(w1-w2)/(w2 Delta D0),
    R'= -24 w1 w2(w1-w2)/F^2.

This is a geometric direction ratio relative to the supplied torus action,
not a unit angular speed or a physical transport equation.

## An all-parameter nonconstancy argument and the time quantifier

For unequal weights the numerator is nonzero and R is strictly monotone on
(0,1). Let d=2C^2-2Lambda. The denominator never vanishes on the declared
strict domain, and

    (Delta D0)^2=(6-R)^2(R+d)/2.

As a polynomial in R this has cubic coefficient 1/2. It cannot be constant
on a nontrivial R interval for ANY fixed finite C,Lambda. Therefore r_dot(0,x)
is nonconstant. This proof treats both root signs and both gap signs.

For each datum choose interior xa,xb with distinct r_dot(0,xa),r_dot(0,xb).
For f(t)=r(t,xa)-r(t,xb), f(0)=0 and f'(0)!=0. Smoothness implies
f(t)!=0 for EVERY sufficiently small nonzero positive or negative t.
After shrinking to one interval where the gap and denominator remain regular
on [xa,xb], the continuous x->r(t,x) has a nontrivial interval as image at
each such t. It contains both rational and irrational numbers. On a torus
with irrational ratio its linear leaves are nonclosed (indeed dense); with
rational ratio the leaves are closed. Thus every nearby punctured time slice
has nonclosed interior leaves, and cannot be all-closed. It also has some
closed interior leaves. No orbit integration or finite rationality test owns
this analytic statement.

For unequal rational initial weights this obstructs retention of all-closed
structure on ANY neighborhood of t=0. Unequal irrational initial weights
already fail all-closed at t=0; the punctured-time result is the same.
It does NOT say every initially irrational torus stays irrational at every
nearby time: for fixed x the nonzero r_dot allows nearby rational crossings.
It does not say every torus becomes irrational or topology changes.

## Equal nonround weights and exceptional fibres

For w1=w2=w!=1, the initial metric is Berger with full U(2) symmetry,
R and b are constants, and BOTH gamma and eta^2 are U(2)-invariant. Hence
the full (generally non-pure-trace) K is invariant. Apply the general
isometry-extension method, not G330's pure-trace conclusion by substitution.
The evolving invariant spatial metrics have Berger two-function form.
The initial nonround gap stays open for a short time, so the simple line is
the same Hopf fibre distribution and every leaf is a circle. This uses the
full symmetry argument; zero HB2 drift alone would be insufficient.

Initially rational positive weights proportional to coprime m,n generate
a weighted circle action. The two axis stabilizers have orders n and m,
respectively; if one is greater than one the action has exceptional fibres.
It is free only when m=n=1, i.e. equal positive weights. Unequal rational
all-closed is therefore not an ordinary free Hopf bundle assertion.

Maximum survivor: conditional local orbit-structure distinction in this
specific supplied metric-data family. No physical carrier, old finite-box
Hessian, stability, matter, topology-change, common target identification,
absolute scale, generic perturbation or long-time conclusion is supplied.
