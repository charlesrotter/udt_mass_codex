<a id="r16pda"></a>

#### Prepared initial distance and actual fixed-ray reception — PDA1

The CCW1 successor is now answered at an explicitly conditional scope. Supply
the same UNADOPTED C3 Lorentz4 RG, g=x^-2 b, with nonzero timelike dx at a
future spacelike boundary, and normal collar b=-N²dx²+h. Fix one interior
emission event, its ordinary unit clock tangent, and a regular outgoing null
ray q(x)=(x,z(x)) ending at p=(0,y_p). Normalize that whole ray to omega_e=1;
its conformal affine tangent has a nonzero regular limit K. Nullness gives
|z'(0)|_h=N_*>0. Actual local emitter variations at each finite reception carry
R6's received-tick interpretation. This is one fixed ray through a prepared
population, not a distance-only law for all angles or arbitrary receiver paths.

Prepare free receivers on an interior spacelike surface Sigma with smooth
bounded timelike data and position labels a in a compact three-dimensional
patch. L(a) is the induced-metric proper distance from a specified origin,
smooth away from origin and cut locus. Surface, initial motions and branch
are query choices; they are not a physically selected observer population.
The following additional sufficient conditions remain explicit:

- H1: the actual tails share a compact normal collar for 0<x<=x0, with uniform
  metric/inverse/first-derivative bounds and uniformly bounded entry covectors
  w(x0,a). Transit from Sigma to that collar must actually exist.
- H2: the interior flow Y(x,a) is C1 and D_aY converges uniformly to a continuous
  J(a); its endpoint F(a_*)=y_p has det J(a_*)!=0. Uniform label-derivative
  convergence and nonsingularity are supplied and checked in the examples,
  not inferred from FCL's pointwise result or bare compactness.
- H3: d=D_aL(a_*) J(a_*)^-1 z'(0)<0 for the below-endpoint distance limit;
  put c=-d>0. The opposite sign describes approach from above; d=0 requires
  a separate attachment calculation. These are not necessary-and-sufficient
  conditions for every possible distance asymptote.

FCL's norm estimate now has one common constant C and entry bound W0:

    sup_a |w(x,a)| <= exp(Cx0)(x/x0)[W0+Cx0 log(x0/x)].

Consequently gamma->1 and Y_x=-Nh^-1w/gamma=O(x[1+log(x0/x)]) uniformly.
Integration yields a continuous endpoint map F and
Y(x,a)=F(a)+O(x²[1+log(x0/x)]). H2 plus the label line-segment integral gives
D_aF=J. Thus Y extends jointly C1 with Y_x(0,a)=0. No C2 boundary extension
or automatic label regularity is being smuggled into the argument.

The actual incidence equation Y(x,a(x))=z(x), with invertible J(a_*), supplies
a unique local C1 receiver-label curve by the one-sided implicit-function
theorem. Extending Y as F to x<0 is only a mathematical device. It gives

    a'(0)=J^-1 z'(0),
    L(x)=L_*+d x+o(x),
    x_o(L)=(L_*-L)/c+o(L_*-L),  L_*=L(a_*).

This is derived incidence, not a definition of x as distance. Nonzero d and
C1 continuity supply local invertibility. The uniform free-clock estimate
gives T=u/x->n_p along a(x), hence B=-b(kbar,T)->B_*=-b_p(K,n_p)>0. R6 gives

    Z=1/(x B),
    (L_*-L)Z -> c/B_* >0,
    (1+chi_clock)/(L_*-L)² -> 2B_*²/c².

The last expression evaluates the matched scalar clock leg only. Under a
regular gauge x'=a0x+o(x), c'=c/a0 and B_*'=B_*/a0, so the distance residue is
unchanged. L is initial surface distance, not radar distance, elapsed ray
length or source proper-time gap. No full-history monotonicity, global first
arrival, universal coefficient or echo follows from this local theorem.

**Exact supplied controls.** In g=x^-2 eta, future x decreasing, prepare on
Sigma x=1; its induced metric is Euclidean. A comoving source at the origin
emits at (1,0) along q=(x,1-x,0,0). Constant spatial momentum P gives

    gamma_x=sqrt(1+|P|²x²), u=(-x gamma_x,x²P),
    Y(x,a)=a+(1-x²)P/(gamma_1+gamma_x),
    F(a)=a+P/(gamma_1+1).

P can depend smoothly on the initial label but stays constant on each free
worldline. Original-metric Christoffel equations and normalization check this
flow. For P=0, L=1-x and Z=1/(1-L), 0<L<1. This normal/comoving preparation
is not PSW parallel preparation. Ambient transport along the straight path
in Sigma sends the source tangent to (-cosh L,-sinh L,0,0); PSW also uses an
ambient spacelike geodesic rather than this surface path in general.

For any fixed finite radial P=p e_y,

    D_x=p(1-x²)/(sqrt(1+p²)+sqrt(1+p²x²)),
    L(x)=1-x-D_x, L_*=1-p/(sqrt(1+p²)+1),
    Z=1/[x(sqrt(1+p²x²)-px)].

L'(x)=-1+px/sqrt(1+p²x²)<0, so the actual one-way range is 0<L<L_* and
(L_*-L)Z->1. Nonzero p includes ordinary motion-dependent Doppler comparison.
Immediate return to the source arrives at x_A=2x-1, so an echo requires x>1/2,
equivalently L<L(1/2); for p=0 this is L<1/2. Conformal Minkowski causality
establishes first arrivals in these controls only. The one-way endpoint is
not a physical relay event or a wall.

**Bounded noncrossing degeneracy.** The same metric and initial distance admit
a different exponent. On a sufficiently small label ball near a_*=(1,0,0),
write a=(1+r,v,w) and choose

    F(a)=(1-v,r+v²,w), dvec=F(a)-a,
    P(a)=2dvec/(1-|dvec|²), |dvec|<1.

This is a deliberately chosen mathematical preparation control, not a fitted
metric or native physical population. The exact flow above has this endpoint
map. At a_*, P=0 and J is a planar quarter-turn with the third axis fixed.
For every x in[0,1], D_aY=x²I+(1-x²)J, whose least singular value is at least
1/sqrt(2). Uniform continuity gives a small convex label ball where derivatives
differ from that base matrix by less than1/(2sqrt(2)). Integrating along label
segments gives a uniform lower Lipschitz bound and proves noncrossing there.
The flow is analytic and H1/H2 hold, but D L J^-1 z'(0)=0: H3 fails.

Since Y=F-Px²/(gamma_x+1), actual incidence implies a-a_*=O(x), P=O(x) and
F(a(x))=z(x)+O(x³). Therefore

    a_2=x+O(x³), a_1=1-x²+O(x³), a_3=0,
    L=1-x²/2+O(x³), B->1,
    (1-L)Z->0, sqrt(1-L)Z->1/sqrt(2).

Analytic implicit dependence also controls derivatives of these remainders.
Redshift still diverges; its initial-distance exponent changes. Initial motion
and direction vary along this selected label curve. This refutes automatic
H3 from bounded smooth preparation plus nonsingular/noncrossing flow; it does
not refute a specified radial parallel-prepared law or the founding asymptote.
CCW's Z=1 example instead needs unbounded initial momentum and fails H1.

PDA1 closes the conditional fixed-ray distance attachment, not physical RG
admission, generic H2/common-collar existence, arbitrary prescribed populations,
global source access, additional-effect attribution or a scale/X_max relation.
SGE's identical matched geometry/query contrast still vanishes; FCL/CCW's
pointwise and invariant results survive. The independent reviewers also found
wavefront/path formulations and other degeneracies; those remain scoped review
arguments, not additional maintained theorems or silently accepted premises.
[Initial proof](udt_prepared_distance_attachment_2026-10-04/INITIAL_CANDIDATE.md),
[reviewed scope](udt_prepared_distance_attachment_2026-10-04/REVIEWED_RESULT.md)
and [descendant review](udt_prepared_distance_attachment_2026-10-04/DESCENDANT_REVIEW.md)
retain the hypotheses, exact controls, exposure and limits.
