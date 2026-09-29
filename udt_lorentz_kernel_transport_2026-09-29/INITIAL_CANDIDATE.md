# LKT1 initial candidate — how reciprocal geometry meets Lorentz transport

CONDITIONAL, UNPROMOTED. WORK_ORDER owns scope. This frozen candidate recovers
several existing source results and develops an explicit differential bridge in
a declared two-dimensional sector. It does not select native metric dynamics.
Use c_E=1 by measuring time in length units. Signatures are (-+) or (-+++).

## 1. Exact hyperbolic correspondence, with both bilinear forms retained

R1 derives D(delta)=diag(exp(-delta),exp(delta)) on supplied ordered depth,
preserving the dual evaluation pairing K=[[0,1],[1,0]]. The physical quadratic
readout in these original clock/ruler channels is eta=diag(-1,1). Put

    S = (1/sqrt(2)) [[1,1],[-1,1]],
    B = S^-1 D S = [[cosh(delta),-sinh(delta)],
                   [-sinh(delta),cosh(delta)]].                    (1)

Direct multiplication gives S^T K S=eta and B^T eta B=eta. Thus the positive
reciprocal character really is conjugate to a one-parameter Lorentz boost
representation; its tanh law is not merely visual resemblance.

But the same basis change sends the ORIGINAL physical readout to
S^T eta S=-K. In the original basis D^T eta D=diag(-exp(-2delta),exp(2delta)),
which equals eta only for real delta=0. Changing basis does not erase this
distinction. Preserving K cannot be renamed preserving the physical interval.
This re-expresses the founding ownership audit section5; it does not refute the
founding metric, or prohibit a nontrivial relation to physical transport.

## 2. What already matches on an actual null comparison

FSL1/G220/G269/G272/G274 already give, on supplied regular geometry, branch and
ordinary endpoint clocks,

    Lambda=E_o^-1 P E_e,  Lambda^T eta4 Lambda=eta4,
    Lambda(1,n_e)=f(1,n_o), f>0,
    Z=omega_e/omega_o=1/f,
    Phi_clock=-log Z=log f, chi_clock=tanh(Phi_clock).      (2)

The Phi_clock identification is G176's matched comparison-clock leg with the
source proper clock as parameter. It does not construct the full pair plane or
identify a pointwise presentation phi with measured pair depth. Full-frame
rapidity magnitude also retains transverse information; only the transported
planar, oriented case identifies signed boost rapidity with this clock depth.

For subdivision of the same ray, the intermediate direction is carried:

    f(Lambda2 Lambda1,n)
       =f(Lambda2,A(Lambda1,n)) f(Lambda1,n).               (3)

This supplies an exact additive logarithmic depth on that specified ray. The
coordinate/query dependence does not make it arbitrary once geometry and clocks
are fixed. It is a constructive existing join, not a second redshift profile.
Later future return, changed path and physical relay remain distinct protocols.

One stronger identification can be rejected precisely: there is no nonzero
smooth homomorphism ell:SO^+(1,3)->(R,+) depending on the Lorentz arrow alone.
Its derivative kills every Lie bracket. Spatial generators J_i and boosts B_i
obey [J_i,J_j]=epsilon_ijk J_k, [J_i,B_j]=epsilon_ijk B_k,
[B_i,B_j]=-epsilon_ijk J_k, so all generators are brackets and d ell=0.
Connectedness gives ell=0. This concerns the full group and smooth scalar
characters, not the null-direction cocycle(3), planar subgroup, path-labelled
relations, or physical UDT. It explains why stripping direction/frame data
cannot turn the existing full Lorentz law into a universal additive scalar.

## 3. Positive differential bridge from full pair geometry

Supply an ACTUAL smooth Lorentz2 metric on a coordinate patch, with the ordinary
proper clocks of the x=constant curves. Alternatively use a totally geodesic
Lorentz2 surface in a supplied four-metric, containing the clocks and rays.
A rank-two pointwise pullback alone does not ensure this surface or its
Levi-Civita transport equals ambient transport. These are restricted-sector
hypotheses, not derived physical symmetry or observer selection.

Write the complete triangular coframe and metric

    theta0=T(dt+b dx), theta1=L dx,  h=-(theta0)^2+(theta1)^2,
    T(t,x)>0, L(t,x)>0.                                   (4)

The metric-unit clock is U=T^-1 partial_t. The shift b is retained; it need not
be small. Set a=(T_x-(Tb)_t)/(TL), H=L_t/(TL). Exterior differentiation gives

    d theta0=-a theta0 wedge theta1,
    d theta1= H theta0 wedge theta1.

The unique torsion-free metric-compatible connection has equal off-diagonal
one-forms varpi=omega^0_1=omega^1_0, zero diagonal, and Cartan's equations give

    varpi=a theta0+H theta1
          =[T_x-(Tb)_t]/L (dt+b dx)+(L_t/T) dx.            (5)

This is a CALCULATED connection of h, not an independent physical field.
It retains the complete first derivatives of clock, ruler and shift data.
For a supplied path gamma, with J=[[0,1],[1,0]], frame components of parallel
transport satisfy v'=-varpi(gamma') J v. The generator is fixed in this sector,
so its signed boost rapidity is exactly

    alpha_gamma=-integral_gamma varpi,
    Lambda_gamma=exp(alpha_gamma J).                      (6)

For an affine future null branch, k_frame=omega(1,epsilon), epsilon=+1 or -1
constant on its regular connected segment. Contracting the transport equation
gives d log omega=-epsilon varpi. With endpoint clocks equal to U,

    log Z=epsilon integral_gamma varpi,
    Phi_clock=-epsilon integral_gamma varpi
              =epsilon alpha_gamma.                      (7)

Thus this sector explicitly joins the completed comparison CLOCK LEG to an
actual Lorentz boost computed from the full metric. Neither endpoint rapidity
nor a distance curve has been supplied independently to force the answer.
Changing the physical endpoint clocks changes the query. An intermediate
frame boost changes varpi by an exact differential; if that boost is zero at
both endpoints, (6)-(7) are unchanged. General endpoint frame changes require
transforming clock components too, not applying (7) to different time columns.

## 4. The density and shift cannot be silently removed

G176 gives m=TL, Phi_local=-log T and L=m/T for each supplied local record with
these clock labels. Substituting into(5) retains m and its derivatives. The
one-dimensional spatial normalization m dx is not automatically an integrable
spacetime coordinate retaining t when m_t is nonzero (R4/G180). Therefore a
determinant-one chart is not silently inferred from completed-pair normalization.

A supplied diagnostic has T=1, b=0, L=1+t on t>-1. Its local completed scalar
is Phi_local=0 at every point, but varpi=dx. Fixed-x clocks at x=0 and x=log 2
have null reception t_o=2t_e+1, hence Z=2. Their matched comparison-clock leg
has Phi_clock=-log 2. There is no contradiction: these are different queries.
The density m=1+t retained in the full record carries the omitted information.
This is a G220 specialization, not new UDT dynamics or an admitted positional
cosmology; the supplied metric is flat and the observers have relative motion.
It refutes the proposed scalar-only reconstruction in this supplied control
class, not the completed record or a physical UDT population.

## 5. A precise test in an additional reciprocal coordinate sector

Now explicitly RESTRICT to an actual zero-shift chart with T=e^-phi(t,x),
L=e^phi(t,x), so TL=1. This is a chosen reciprocal-coordinate presentation;
its phi is not asserted to be an intrinsic scalar of the complete geometry.
Equations(5)-(7) reduce to

    varpi=-e^(-2phi) phi_x dt+e^(2phi) phi_t dx,
    dx/dt=epsilon e^(-2phi),
    Phi_clock=Delta phi-2 integral_gamma phi_t dt.          (8)

The last equality follows by substituting the null tangent into(5), using(7),
and integrating dphi=phi_t dt+phi_x dx. It shows exactly when the tempting
identification Phi_clock=Delta phi holds on a given null segment: its displayed
time-derivative integral vanishes. Requiring that equality on EVERY sufficiently
short ray segment of either fixed null orientation throughout an open patch
forces phi_t=0 there. Conversely phi_t=0 supplies that equality locally.

This is a scoped differential consequence of an EXTRA identification, not a
premise already imposed by UDT. A finite segment's cancellation need not force
stationarity. In the time-only sector phi_x=0, (8) gives Phi_clock=-Delta phi,
the opposite sign from the static spatial reduction. G220 already owns both
endpoint limits. The distinction explains why carrying the static depth-
difference formula unchanged into an evolving geometry would be a mistake.

When the extra equality forces phi_t=0, these particular x-fixed clocks follow
the same timelike Killing field. SGE1's stationary-clock theorem then excludes
net redshift on both legs of an actual immediate return in this sector.
No stationary hypothesis is imposed on general UDT; moving clocks, other
presentations, transverse geometry and a masked positional contribution remain
outside this negative conclusion.

## 6. Curvature is the integrability condition, not a chosen field equation

In Lorentz2 the generator commutes with itself, so curvature is J dvarpi.
For the convention R(X,Y)=nabla_X nabla_Y-nabla_Y nabla_X-nabla_[X,Y],
the scalar curvature of(4) is

    R_h=2 (partial_t varpi_x-partial_x varpi_t)/(TL).       (9)

On a contractible patch, transport in this oriented frame is path-independent
for all curves iff dvarpi=0. Local necessity follows from arbitrarily small
loops; sufficiency is the ordinary exact-form theorem. Global topology can
retain periods even if dvarpi=0, so no global path-independence theorem follows.
Comparisons of two alternative paths with the same endpoints measure the boost
difference -integral dvarpi over a spanning surface in this sector. Such loops
are mathematical comparisons, not closed future causal signaling protocols.

For the reciprocal-coordinate sector(8),

    R_h=2[partial_t(e^(2phi) phi_t)
          +partial_x(e^(-2phi) phi_x)].                    (10)

Equations(9)-(10) are curvature identities. Setting R_h to a selected value,
requiring zero holonomy, or prescribing phi(t,x) would add conditions not
selected here. Likewise in four dimensions Cartan compatibility and Bianchi
identities constrain any connection belonging to the metric but do not by
themselves specify UDT's physical metric history. Transverse transport generally
does not stay within the one-generator sector(6).

## 7. Return and limits

The Lorentzian lead gives an exact representation correspondence, a recovered
direction-retaining clock cocycle, and an explicit metric-derivative-to-boost
bridge on a declared sector. Its nontrivial restriction is that identifying the
actual clock depth with the SAME presentation-potential difference on all short
null segments would impose stationarity in that sector, with the corresponding
limited two-way obstruction. No additional postulate is silently adopted.

The remaining native assignment must determine admissible complete geometry and
physical comparisons, or extract further restrictions from existing premises.
The scalar tanh shape alone does not supply those derivatives, density, shift
or physical query assignment. This route does not prove that the full premises
are insufficient, that a local field equation is necessary, or that Lorentzian
methods have been exhausted. Ordinary initial/query data remain legitimate.

Sources: founding ownership audit sections1,5,6; G176/G180; G220; G269/G272/G274;
FSL1 initial candidate with orientation repair and reviewed result; SGE1 repaired
stationary result. Central R1–R8 owns their maintained explanation. General
Cartan/Levi-Civita mathematics is used only as a method: David Tong section3.4.2,
https://www.davidtong.org/teaching/general-relativity/grhtml/S3 . No Einstein
equation, matter/light model, Hubble model, physical distance attachment or X_max
profile is used. Candidate frozen after the disclosed source recovery/exploration;
actual checks and fresh reviews will determine its final accepted scope.
