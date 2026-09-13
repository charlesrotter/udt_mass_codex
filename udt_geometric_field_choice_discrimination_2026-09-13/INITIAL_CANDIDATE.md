# NR2 — fixed-geometry field records and a symmetry-breaking survivor

INITIAL CONDITIONAL UNPROMOTED candidate, not yet reviewed. Parent hand algebra,
NR1 source exposure and the logged primary abstracts preceded this freeze. No
new confirmatory mathematical run or NR2 reviewer outcome has been exposed.
Current G312 FILTER ONLY and NR1's UNPROMOTED status govern all geometry use.

## 1. Fixed complete geometry and stated four-parameter family

On u>0 supply g=-2du dv+dx²+dy²+H0 du², H0=2(x²-y²)/u². This is NR1's
full nonconstant Ricci-flat example; it is not a frozen slice or linearization.
Coordinate/clock origin u0=1, unit display L=c_E=1 and transverse marking are
supplied diagnostic conventions, not a selected physical scale or frame.
The finite family studied is

 K=q(u)partial_x+r(u)partial_y+(q'x+r'y)partial_v,
 q''=2q/u², r''=-2r/u²,
 F=d(K-flat)=2du wedge(q'dx+r'dy).                       (1)

A constant multiple of partial_v may be added; its two-form is zero. This
family does not include every Killing field of this metric and is not every
Maxwell-form field. The state z=(q0,p0,r0,s0)=(q(1),q'(1),r(1),r'(1)) ranges
over ALL real4-tuples. With nu=sqrt(7)/2,

 q=(q0+p0)u²/3+(2q0-p0)/(3u),
 r=sqrt(u)[r0 cos(nu log u)+(s0-r0/2)sin(nu log u)/nu].   (2)

These exact functions satisfy the original ODEs and initial data. K is Killing,
Ric(K)=0 and F satisfies both source-free Maxwell-form equations by NR1;
original tensor equations are also checked here. Zero and nodal forms are retained.

Fix the same metric and supplied observer/query protocol before changing z.
On Sigma={x=y=0}, U=(partial_u+partial_v)/sqrt(2) is a unit timelike geodesic
observer field; ex=partial_x,ey=partial_y form a parallel transverse frame there.
The chosen signed mathematical record is

 e=(F(U,ex),F(U,ey))=sqrt(2)(q',r').                     (3)

Observer proper time obeys ds=sqrt(2)du on these central worldlines. All u
record derivatives below refer to this stated calibrated coordinate, not a
silently substituted proper-time derivative. Clock/null/Jacobi data from fixed
g and fixed protocol contain no z; the G179 pair evaluator at fixed pair likewise
contains no K. This is a property of these separate inputs, not a theorem that
UDT cannot ever relate them. Transforming supplied frames transforms components;
relative orientation is not a preferred universal observer frame.

## 2. What the finite-family readouts identify

Let A=2/u². At any u>0,

 e'=sqrt(2)(Aq,-Ar),
 q=e'_x/(sqrt(2)A), p=e_x/sqrt(2),
 r=-e'_y/(sqrt(2)A), s=e_y/sqrt(2).                    (4)

ODE uniqueness then recovers the initial four-tuple. Thus the signed record
(e,e') identifies this stated finite family, including an event where e=0.
It does not identify a physical field, all solutions or the central zero-form
addition to K. A=0 would invalidate this inverse; here A is nonzero everywhere.

Two signed e measurements, at1 and at b>0, give the coefficient matrix with
q0 coefficient in q'(b) equal to 2(b-b^-2)/3, and r0 coefficient in r'(b)
equal to -(2/nu)b^-1/2 sin(nu log b). Their joint four-state map is invertible
iff b!=1 AND sin(nu log b)!=0. In particular b=2 works; exact blind return
spacings b=exp(m pi/nu), nonzero integers m, lose the r0 direction. These are
sampling blind spots of the stated map, not a physical forbidden wavelength.
Near the blind set an algebraic inverse may be ill-conditioned; no numerical
operating interval or measurement-precision claim is made.

Define mathematical squared-projection data Q=e e^T, I=tr Q and, where I>0,
Pi=Q/I. No detector, optical Stokes law, energy or physical intensity is adopted.
For e!=0, Q chooses e up to global sign. Given such an e,

 e'=[Q'e-e(e^T Q'e)/(2I)]/I.                            (5)

Therefore (Q,Q') identifies z up to the SAME sign in this class. At e=0,
Q=Q'=0 does not identify the two unconstrained position data q,r. Here
Q''=2e'e'^T restores them up to sign; if e=e'=0 the finite-family solution
is identically zero. Pi alone is undefined at zeros and is unchanged by any
common nonzero rescaling of z. No normalization is selected by this diagnostic.

I alone misses relative component sign for the entire history: z and the state
obtained by changing (q0,p0) to (-q0,-p0) have identical I(u) for every u>0,
while their Q_xy signs differ where q'r'!=0. For example z=(1,1,1,1) and
(-1,-1,1,1) have the same geometric records and I(1)=4, but Q_xy(1)=+2/-2.
Global z->-z is invisible to all Q histories. These are exact exhibited
ambiguities, not a complete classification of all scalar-I-history fibres.

## 3. Two different meanings of phase

For nonzero transverse r profile, let c=r0,d=(s0-r0/2)/nu. Then
r=R sqrt(u)cos(nu log u-delta), R=sqrt(c²+d²)>0,
(c,d)=R(cos delta,sin delta). This profile phase delta, relative to supplied
u0/clock marking, changes r and generally F; signed e/e' data recover it modulo
2pi. Quadratic data retain their common-sign ambiguity. At R=0 delta is undefined.
No physical oscillation frequency, optical carrier or absolute phase is selected.

A phase used only to factor the SAME two-form is different. For any smooth
monotone theta=f(u) with f'!=0, write

 F=dtheta wedge a_theta,
 a_theta=2(q'dx+r'dy)/f'.                               (6)

Changing f while compensating a_theta leaves F and all its contractions exactly
unchanged. For instance theta=-u and theta_hat=-u² on u>0 both describe the
same F this way. These factorization labels cannot be recovered from F alone.
Their gradients are null, but nullness does not identify them with a chosen
G352 count phase. If one separately supplies either as that count phase, the
G352 phase/readout protocol has changed; its conditional rule is retained, not
refuted or silently equated to a quadratic field record.

## 4. Break the sufficient symmetry and check the field itself

Supply the full exact control

 g_epsilon=-2du dv+dx²+dy²+[H0+epsilon C(x,y)]du²,
 C=x³-3xy², epsilon real.                              (7)

The transverse Laplacian of both H0 and C vanishes, so the entire Ricci tensor
vanishes for every epsilon. This is a supplied conditional metric, not established
native dynamics or a specified empirical GR-filter survivor. No approximation,
finite-cell boundary, global completion or u=0 extension is asserted.

For the OLD family K in(1), the sole remaining Lie component is

 (L_K g_epsilon)_uu=epsilon[3q(x²-y²)-6rxy].             (8)

For epsilon!=0, every nonzero transverse-generator member fails the Killing
condition somewhere on any open transverse patch. The central partial_v remains
Killing; no absence of all isometries is claimed. Yet K-flat and F are unchanged
because K^u=0. Original divergence and exterior closure still vanish!

Indeed the larger exact sufficient family is already visible: for ANY smooth
v-independent H(u,x,y) in this Brinkmann form and ANY smooth real functions
a_x(u),a_y(u), the two-form

 F_aligned=du wedge[a_x(u)dx+a_y(u)dy]                            (9)

is closed, divergence-free and null wherever nonzero. The determinant is -1;
raising gives only F^{vx}=-a_x, F^{vy}=-a_y and antisymmetric partners, so the
original divergence is zero by v/transverse independence. This proof does not
use the Killing ODE or Ricci-flatness. It is a sufficient explicitly aligned
family, NOT a classification of all Maxwell fields, all metrics, native UDT
responses or actual radiation. Functional profiles and the special Brinkmann
structure remain supplied. This is not a replacement source/field law.

Consequently(4)'s finite-family identifiability must not be promoted to(9).
Adding (u-1)^3 du wedge dx changes the field while preserving its e,e' data
at1 and the metric. Finite records cannot identify the entire newly admitted
arbitrary-function family. This is an explicit survivor and limit, not a claim
that a new physical postulate is necessary.

## 5. A concrete geometric blind spot, with a way to expose it

On all of Sigma the cubic C and every derivative through order2 vanish.
Thus g, its connection and full curvature coincide there for every epsilon.
With the same central observers, paths and endpoint data, central clock/null
records and infinitesimal Jacobi beam maps therefore coincide. Equality follows
from identical geometric coefficients along those paths; no finite sampling
is used as a whole-curve proof. The old F and its central records also coincide.

The actual screen curvature difference away from Sigma is

 delta R_uiuj=-3epsilon [[x,-y],[-y,-x]].                (10)

At Sigma its transverse derivative is nonzero for epsilon!=0, for example
partial_x delta R_uxux=-3epsilon. Connection corrections there vanish in this
comparison, so a supplied neighboring-curvature/curvature-gradient diagnostic
can distinguish epsilon. This makes no finite-beam, remote-reach, global
observability or detector claim. A central infinitesimal probe does not exhaust
the complete geometry; the field surviving symmetry loss does not make the
metric change invisible to every possible observation.

## 6. Result ceiling and verification plan

This maps actual conditional information gains and ambiguities in a declared
family, and expands an exact field survivor within the full metric control.
No photon, Maxwell action, physical polarization/energy/detector, coupling,
normalization, native response membership, selected history/scale or G424 is
established. All mathematical projections and profiles are free-and-explored
choices; Levi-Civita/ODE identities are pinned-by-THEORY only as mathematical
methods with stated hypotheses. No pinned-by-HABIT physical choice is used.

Checks: full original Ricci/Lie/exterior/divergence/coframe/null tensors; exact
ODE/initial data/inversion and rank formulas; explicit zero/sign/phase/control
witnesses; full central two-jet and off-axis curvature difference. Symbolic
identities are regression of the analytic proof; independent review must
reconstruct load-bearing arguments and implement distinct checks. If a numerical
illustration is used, it is finite descriptive support, not certification.
Freeze candidate/code/parameters before results; preserve failures and repairs.
