# TSI1 initial conditional identifiability argument

Status: CONDITIONAL candidate, not native selection or observation. Discovery
preceded this freeze. The parent proposed the late logarithmic drift to both
fresh reviewers at dispatch; no claim of their being blind to that formula.
All calculations inherit CPR1/OAA1/OJM1's actual regular incidence branch.

## 1. Records and units before inversion

Use ell_o=c_E t_o for receiver proper time in length units, and ell_e=c_E t_e^p
for emitter proper time. Coordinate emission time remains t_e (length units),
so ell_e=sqrt(h)t_e. H has units inverse length; c_E H has inverse seconds.
The receiver carries an ordinary calibrated proper clock. Nothing changes its
local physics. The following are distinct supplied record protocols:

T: the smooth arrival map between labeled emitter proper-clock readings and
receiver proper time, giving Z=dell_o/dell_e. Equivalently a stable source
frequency can furnish Z up to an unknown positive constant. A varying unknown
source frequency is NOT this record. A known source size is unnecessary.

A: the angular position of the same specified pointlike circular source,
recorded against receiver proper time in the radial parallel transported
orthonormal frame. This requires a declared angular reference and track
identification; arbitrary frame rotation or unknown source centroid motion
would add freedoms. No angular size or material ruler is assumed.

U: only the ordered, untimed Z/angle curve, without calibrated proper-time
intervals or independently known length. It can include angular-size records
only if the source size remains free to co-scale. An angle is not a length.

These ideal records are conditional interfaces, not claims that an actual
astronomical source supplies them. Continuous derivatives/asymptotic data are
stronger than finitely many ticks or finite noisy observations.

## 2. Timed redshift gives a conditional curvature scale

Keep f=1-2m/r-H^2r^2, a>3m, h=1-3m/a>0,
Omega=sqrt(m/a^3-H^2)>0, finite fixed E>0 and escaping receiver. Let x=1/R,
V=sqrt(H^2+(E^2-1)x^2+2mx^3), and on the actual branch b=b(x) define

 s=sqrt(1+H^2b^2-b^2x^2+2mb^2x^3),
 alpha=1/(Ex+V)+Vb^2/(1+s), A=x alpha,
 F=(1-Omega b)/(sqrt(h) alpha), Z=F(x)/x.

Strict |b_*|<a/sqrt(f(a)) gives a uniform positive ray margin. CPR1's limiting
incidence Jacobian I_infty(1-Omega b_*)>0 gives smooth b(x) near x=0 by the
implicit function theorem. Thus F is smooth, positive and
F(0)=H(1-Omega b_*)/[sqrt(h)sqrt(1+H^2b_*^2)]>0. This smoothness, not a bare
asymptotic equivalent, licenses differentiating. Since dx/dell_o=-xV,

 K_length := d log Z/dell_o = V(1-x F'/F) -> H,
 K_seconds := d log Z/dt_o -> c_E H.                    (T1)

Consequently an ideal T record determines H=lim K_seconds/c_E, and the
conditional scale 1/H=c_E/lim K_seconds. The limit is independent of m,a,E,
and strict regular b_*; it does not determine those remaining parameters.
It is a geometric consequence of the supplied model, with no fitted curve.
A constant unknown normalization of Z cancels. Identical properly matched GR
histories give the same result; this is not an additional UDT prediction.

Derivative control is explicit: if 0<=x<=x0 has |F'/F|<=B, then

 |K_length-H| <= |V-H| + V B x,
 |V-H| <= (|E^2-1|x^2+2mx^3)/(V+H).                  (T2)

B depends on the admitted branch and is not a universal known observational
error bar. Near a tangency margin, large boost or small H the useful onset can
be late. For a finite proper-time interval, [log Z(t2)-log Z(t1)]/(t2-t1)
is the time average of K_seconds and inherits a uniform bound only if one is
supplied on that interval. Finite numerical examples do not certify that bound
for an unknown source. No practical detectability or noise forecast follows.

The emitter proper-time endpoint is finite while receiver time diverges. A
fixed nonzero tick spacing produces only finitely many ticks within a finite
emission interval: it cannot realize an infinite asymptotic derivative record.
A continuous ideal phase/clock map is a mathematical interface; actual cadence,
resolution, persistence and source variability must be assessed before empirical
use. If source frequency nu_e varies, received frequency is nu_e/Z and
 -dlog(nu_o)/dt_o = K_seconds - dlog(nu_e)/dt_o.
Arbitrary unmodeled drift can mimic a finite timing record. Smooth nonzero
nu_e at the finite emission endpoint with bounded log derivative in emitter
proper time makes the contaminant decay as 1/Z; those are extra source
regularity conditions, not a generic astronomical guarantee.

## 3. An independent angular route, with narrower preparation

In outgoing EF coordinates u_o=(1/(E+v),v,0,0), and the radial unit vector is
e_r=(-1/(E+v),E,0,0), with e_phi=(0,0,0,1/R) at the equator. These vectors are
parallel transported along the radial geodesic (fixed angular axes). The future
photon direction components are

 n_phi=b/(R A)=b/alpha,
 n_r=[s/(E+v)-v b^2/(R^2(1+s))]/A, n_r^2+n_phi^2=1.

The incoming sky direction is opposite. Define theta=atan2(n_phi,n_r), with
the sign convention kept fixed. Its limiting value satisfies
tan(theta_*)=H b_* and n_r,*=1/sqrt(1+H^2b_*^2). This untimed endpoint
alone fixes only dimensionless H b_*.

For the inherited principal preparation b_*=0, incidence gives
b(x)=Omega a x/H^2+O(x^2), hence
theta=Omega a x/H+O(x^2). Omega a/H is nonzero in this scope. Therefore

 -dlog|theta|/dt_o -> c_E H.                           (A1)

The derivative has controlled O(x) error on a smooth branch after factoring
theta=x T(x), T(0)=Omega a/H>0, as in (T2). This uses a timed position track,
not angular size or a known ruler. It requires the specified radial angular
reference and principal preparation. No universal logarithmic angle formula
is asserted for arbitrary b_* or a freely rotating observational frame.

## 4. What the untimed record cannot fix

For any lambda>0, map m,a,R,b,u,t_e,ell_o,ell_e -> lambda times themselves,
H,Omega -> divided by lambda, with E unchanged. Then h,s,v,A,Z and sky angles
at corresponding incidences are unchanged; U ->lambda U, P unchanged,
I ->I/lambda. The EF metric is carried to lambda^2g. OJM1's B and J scale
by lambda, while any supplied unknown source size can co-scale. Thus U has
an exact scale degeneracy, including untimed combined angular/redshift data.
This is a family of supplied conditional geometries, not an adopted native
UDT scaling symmetry or a passive change of units.

Timed records transform as Z_lambda(t)=Z(t/lambda), theta_lambda(t)=theta(t/lambda)
after corresponding origins, so their rates scale by 1/lambda. A fixed calibrated
proper-time record removes this homothety through (T1), or (A1) in its narrower
scope. Re-labeling that physical time would change the record. This proves
asymptotic scale identifiability within this family; neither uniqueness of all
parameters nor identification from an arbitrary finite data set follows.

## 5. c_E and G_obs contribute different things

c_E is essential to express the measured inverse-time rate as an inverse length,
and the conditional endpoint in length units. The timing datum is the additional
dimensional information missing from c_E,G_obs alone. Their unit-covariance
obstruction in ICN1/MGC1 survives: [c_E]=L/T, [G_obs]=L^3/(M T^2), and simultaneous
unit rescaling L,T,M leaves both constants' numbers unchanged. They alone cannot
choose a nonzero length or time; this does not forbid measurements supplying it.

Given a measured K=c_E H>0, the combination c_E^3/(G_obs K)=c_E^2/(G_obs H)
has mass units. It is a dimensional mass equivalent, not a derived physical
mass or source. Likewise identifying metric m=G_obs M/c_E^2 requires a justified
physical interface and independently obtained M; the conditional vacuum metric
alone does not provide it. If that interface and an independently fixed M were
authorized, it could fix m along a supplied scale family. An independently fixed
density plus an independently justified MGC1 relation could also constrain H.
Neither relation, cosmic density, volume factor nor a definition of X_max is
adopted here. G cannot supply a second independent constraint by defining a
mass from this same K. A co-scaling geometric mass preserves the degeneracy.

## 6. Maximum conclusion and remaining gate

There is a positive, testable conditional data interface for scale: receiver
clock timing can replace a known source ruler in an ideal specified experiment.
Untimed data retain an exact scale freedom. Neither result selects this metric,
identifies it with the native pair assignment, proves empirical applicability,
or establishes the founding additional positional effect beyond GR. The next
gate is an actual finite-record/physical-source interface or native selection,
with a separately stated question; no automatic follow-on is authorized.
