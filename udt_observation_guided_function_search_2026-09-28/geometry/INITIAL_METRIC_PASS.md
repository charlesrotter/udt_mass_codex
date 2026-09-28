# Metric-led clock and beam construction

DRAFT / conditional mathematical construction / UNPROMOTED. Initial pass before
empirical coefficients or new observational arrays. No native physical response
equation, additional premise or unique history is adopted. Source scope and
prospective checks: NUMERICAL_FREEZE.md. The three tiles below are the maximum
serious geometric shortlist; controls within a tile are not new adopted laws.

## 1. A clock–beam relation that survives without a selected history

Supply one regular future null geodesic e -> o of a smooth Lorentzian four-metric,
with finite future unit endpoint observers and Levi-Civita connection. Use
proper-length time T=c_E tau. G220 gives the received interval ratio

    r = 1+z = omega_e/omega_o > 0.

On this SAME segment define d_o as the square root of the intrinsic quotient
screen area at e per infinitesimal solid angle at o, and d_e as the square root
of area at o per angle at e. They are metric screen radii, not automatically
observational angular/luminosity distances. G348's adjoint relation between
forward/backward Jacobi blocks gives, on the nonconjugate stratum,

    d_e = r d_o.                                             (1)

Both vanish at a conjugate endpoint; the quotient of their zero values is not
defined there, although the equality remains valid. Reversal in this proof is
the mathematical inverse on the same null segment. It is NOT a later future
return signal. No energy, number conservation, flux or detector appears in (1).
It is general metric geometry, not uniquely diagnostic of UDT.

Changing the endpoint observers gives omega'_i=D_i omega_i, D_i>0. Then
r'=(D_e/D_o)r, d'_e=D_e d_e, d'_o=D_o d_o: (1) is covariant. Thus the formula
does not choose a preferred observer. It also does not claim these radii are
numerically invariant when the actual observers change.

There is a useful differential construction. Trace the same curve to the past
from o with affine tangent l, normalized by omega_o=g(U_o,l)=1. Supply a smooth
future unit U along it, with omega=g(U,l)>0, r(s)=omega(s), and

    ds=omega d lambda,   q(s)=d log r/ds.

s is accumulated local rest-length, not an asserted unique finite separation.
In a parallel orthonormal quotient frame, the Jacobi matrix J obeys

    J_ss + q J_s + (T/r^2) J = 0,
    J(0)=0, J_s(0)=I,   d_o=sqrt(abs(det J)).                 (2)

This is G348's original affine equation J_ll+T J=0 after an exact change of
parameter, since d/dlambda=r d/ds. In the isotropic screen tile T/r^2=F I,
J=d I, so

    d'' + q d' + F d = 0,    d(0)=0, d'(0)=1.                (3)

This tile is sufficient for the symmetric examples below; general shear
requires the matrix equation. If q is C^2 and F is C^1 near the vertex,

    r(s)=1+q0 s+(q1+q0^2)s^2/2+O(s^3),
    d(s)=s-q0 s^2/2+(q0^2-q1-F0)s^3/6+O(s^4).               (4)

In particular, clock slope and area cannot be assigned independently after a
metric/query and its null tide are fixed. Conversely r alone leaves the tide
and area undetermined. Algebraically F=-(d''+q d')/d away from d=0, but that
inverse does not prove arbitrary records have a full metric realization.

The asymptotic target also has an exact necessary condition. With
x=log r=int q ds, the redshift-oriented scalar chi_z=tanh(x) tends to 1 only
when x -> +infinity. If |q|<=Q on a ray of finite s-length S, then |x|<=QS:
the saturation cannot occur on a bounded regular comparison with these bounds.
It needs unbounded accumulated length/rate or loss of the specified regularity.
This does not equate x to the signed supplied pair depth on every dynamic query
or prove X_max is a physical boundary. Infinite redshift is not itself a test
of affine geodesic completeness.

## 2. A constructive nonstationary family, including the remaining function

Take the declared conformally static class

    g=a(eta)^2[-N(x)^2 d eta^2+h_ij(x) dx^i dx^j],
    a>0, N>0,   U=(a N)^-1 partial_eta.                     (5)

a is dimensionless, eta and the spatial chart carry length units; h is
Riemannian. These are supplied smooth data, not a field equation. Null paths
and their optical coordinate duration L are those of the static base gbar;
L is the length of the relevant path in h/N^2, with its regular branch fixed.
Actual forward incidence is eta_o=eta_e+L. Differentiating this incidence and
converting both clocks dT=a N d eta gives

    r=[a(eta_e+L) N_o]/[a(eta_e) N_e].                      (6)

Equivalently partial_eta is conformal Killing and g(partial_eta,k) is conserved
on each affine null geodesic, exactly the G402 integrability criterion. There
is no additional redshift mechanism. The apparent product follows from the
declared separable geometry; it is not a general independent physical split.

For the same null segment, conformal angles do not change and screen lengths
at an endpoint multiply by a at that endpoint. Hence

    d_o=a_e dbar_o,   d_e=a_o dbar_e,
    dbar_e=(N_o/N_e)dbar_o,   d_e=r d_o.                    (7)

The nonstationary clock and beam therefore come from the same geometry.
An immediate future return on the reverse static spatial path has

    r_return=[a(eta_e+2L) N_e]/[a(eta_e+L) N_o],
    r_out r_return=a(eta_e+2L)/a(eta_e).                   (8)

This generally differs from 1. Positive a growth can produce mutual redshift;
the individual lapse ratio and epochs still matter. No preferred spatial
observer follows: for a homogeneous h and N=1 every spatial point is isometric.
The observer congruence remains supplied; spatial homogeneity does not remove
that query choice or require temporal homogeneity.

### 2a. Homogeneous clock plus area, without an evolution equation

Specialize N=1 and

    h=d chi^2+S_k(chi)^2 dOmega^2,
    S_k(y)=sin(sqrt(k)y)/sqrt(k), y, sinh(sqrt(-k)y)/sqrt(-k)

for k>0, k=0, k<0 respectively. This is spatial constant curvature k, with
no preferred spatial center; the radial origin is the chosen observer. Stop
before a conjugate point and, where inversion uses S'_k>0, before its turning
point. With a_o=1 by coordinate normalization,

    chi=eta_o-eta_e=int_[T_e,T_o] dT/a(T),
    r=1/a_e,   d_o=S_k(chi)/r,   d_e=S_k(chi).              (9)

The conformal metric can be written with a reciprocal longitudinal block by
the legitimate coordinate change dt=a dT=a^2 d eta:
g_long=-a^-2 dt^2+a^2 dchi^2. This re-expression does not select a or turn the
history into a native UDT result. The transverse sector stays attached.

If an explicit conventional source/transfer interface is separately supplied,
one may compare D_L=r^2 d_o=r d_e. That brightness statement is NOT derived in
this geometry lane. Parent/data work owns its assumptions and calibration.

Two constructive restrictions produce actual functions:

* Require the forward r at fixed conformal separation chi to be independent of
  emission epoch for ALL short epochs and separations. Then
  a(eta+chi)/a(eta)=R(chi); differentiating at chi=0 forces a'/a=b constant.
  Conversely a=A exp(b eta) works, so r=exp(b chi). Continuity also gives this
  exponential from R(chi1+chi2)=R(chi1)R(chi2). In proper time a is affine,
  a=b(T-T_B). This is an investigated temporal-symmetry restriction, not a
  consequence of no preferred spatial observer or reciprocal normalization.
  b>0, b=0 and b<0 are allowed on their positive a domains. At a_o=1 and k=0,
  d_e=log(r)/b, d_o=log(r)/(b r). Under the optional transfer comparison,
  D_L=r log(r)/b. Both future directions for comoving endpoints have r=e^(b chi)
  and the immediate echo slope is e^(2b chi). This extends the known affine
  ruler control to a jointly specified 4D screen; it is not newly discovered
  non-expansion physics.
* Require instead constant proper-time logarithmic rate H=d log(a)/dT>0.
  Then a=exp[H(T-T_o)] is forced within this supplied restriction. For k=0,
  r=1+H D_now=1/(1-H D_emit),
  d_e=(r-1)/H, d_o=(1-r^-1)/H. Under the optional interface,
  D_L=r(r-1)/H. Here D_now=chi and D_emit=chi/r are distances on the specified
  homogeneous slices. A source at emission separation D_emit<1/H has a future
  arrival. A later reverse trip exists only if its NEW emission separation is
  <1/H. When both legs exist they redshift; the return is not generally the
  reciprocal or numerically equal to the outward ratio. The H horizon is a
  property of this supplied congruence/patch, not adopted X_max.

These are mathematically compatible controls. Their congruences expand; neither
establishes the intended native positional explanation without required Hubble
expansion. A constant rate was exposed, never inferred from a good fit.

### 2b. Exact inverse from a proposed clock–area function

This is a constructive result, not just an unspecified-function statement.
Use x=log r, a_o=1, a_e=e^-x, and supplied h0>0 of inverse-length dimension.
In the flat homogeneous class let

    F(x)=h0 d_e(x),  F(0)=0, F'(x)>0.                      (10)

On any smooth interval satisfying these conditions, define

    H(x)/h0 = e^x/F'(x),
    T_o-T(x) = (1/h0) int_0^x e^-u F'(u) du,
    a(T(x))=e^-x.                                        (11)

T'(x)<0 makes a unique smooth history on the image interval. Directly,
dT/a=-(F'/h0)dx, so its null integral gives chi=F/h0, while (9) gives exactly
the supplied d_e and r. Thus every such F has a concrete compatibility metric
in this restricted expanding class. F'(0)=1 is needed for H(0)=h0; otherwise
h0 is only a normalization. Multiplying h0 changes the dimensional scale.

The usual dimensionless deceleration readout q_dec=-a a_TT/a_T^2, merely a
geometric diagnostic here, is

    q_dec(x)=-F''(x)/F'(x).                                (12)

This q_dec is DIFFERENT from the accumulation q(s) in (2). Restoring seconds,
H_time=c_E H and the lookback proper time is int dx/H_time. No Friedmann,
Einstein, source, fluid or action equation was used.

For nonzero spatial curvature put kappa=k/h0^2, F=h0 S_k(chi). On the increasing
S_k branch (1-kappa F^2)>0,

    H/h0=e^x sqrt(1-kappa F^2)/F',
    q_dec=-F''/F' - kappa F F'/(1-kappa F^2).              (13)

The branch restriction is real: at a closed-space turning point a single
F(x) need not invert the spatial coordinate. Curvature is not determined by
brightness plus clock shape alone without extra information.

The remaining freedom is exact: F (equivalently a), curvature k and scale h0
remain supplied, along with observer and physical signal identification.
Fitting F chooses a history in (11); it does not prove UDT selects that history.
This construction has no claim of novel mathematics or all-UDT generality.

### 2c. The asymptote depends on more than r -> infinity

For the flat inverse at fixed reception, the independent distances and affine
extent are

    D_now=F/h0,  D_emit=e^-x F/h0,
    S_past=(1/h0)int_0^x e^-u F'(u)du,
    lambda_past=(1/h0)int_0^x e^-2u F'(u)du.              (14)

The affine normalization is omega_o=1. These integrals follow from dT and
dT/dlambda=-r. They distinguish proper lookback, current/emission slice
separation and affine accessibility instead of reading a coordinate pole.

For the affine-scale flat control F=x (h0=b), x -> infinity gives unbounded
D_now but D_emit -> 0, S_past -> 1/b and lambda_past -> 1/(2b). Its flat-space-
slice four-metric has a curvature singularity at a=0; it fails an interpretation
as a complete nonsingular unreachable physical boundary. The k=-b^2 Milne
member instead has flat spacetime and an extendible patch, so that member cannot
be called a novel positional mechanism either.

For exponential proper-time scale F=e^x-1 (h0=H), the same limit gives
D_now -> infinity, D_emit -> 1/H, S_past=x/H -> infinity but
lambda_past -> 1/H. The constant-curvature geometry is regular; the flat patch
is null incomplete and extendible. Infinite lookback for this observer family
does not establish a spacetime-ending barrier or native X_max.

More generally, the analytical control F_p=(e^(p x)-1)/p, with F_0=x,
illustrates distinct tails without fitting: for p>=0, D_now diverges;
D_emit tends to zero, 1/h0 or infinity as p<1, p=1 or p>1. Proper lookback is
finite iff p<1; affine extent is finite iff p<2. This is a tail diagnostic
inside tile 2, not an additional proposed physical law or empirical fit family.
Finite-range observations cannot select these infinity limits.

## 3. A center-free constant-curvature control with a static query

Supply the maximally symmetric metric in a static patch

    g=-(1-K R^2)dT^2+dR^2/(1-K R^2)+R^2 dOmega^2,
    K>0,  0<=R<1/sqrt(K).                                (15)

The spacetime itself has no distinguished center; choosing a central geodesic
and static observers is query data. This is a constant-sectional-curvature
mathematical class, not an imported GR field equation, source or adopted scale.
For a static source at R and central receiving clock, put

    rho=asin(sqrt(K)R)/sqrt(K),
    L=atanh(sqrt(K)R)/sqrt(K).                            (16)

rho is radial proper distance on the static slice and L is the central radar
distance (half central proper round-trip time in length units). They differ.
Conserved Killing frequency and the central spherical beam give

    r=(1-K R^2)^-1/2
     =sec(sqrt(K)rho)=cosh(sqrt(K)L),
    d_o=R,  d_e=rR,  chi_z=K R^2/(2-K R^2).              (17)

The outgoing future central-to-static-R signal has ratio sqrt(1-KR^2)=1/r;
the immediate central echo has slope 1. Therefore this candidate is REJECTED
as a universal mutual-positional-redshift explanation. It survives as an exact
comparison of distinct invariant query distances and areas. K<0 gives the
opposite inward clock contrast and no positive-K static horizon; nothing here
selects the sign from UDT.

The central nearby limit is r=1+K R^2/2+O(K^2 R^4), and in regular local charts
the curvature corrections are O(K L_local^2). This supplies a tunably small
metric correction to a flat local reference. It does not demonstrate agreement
with all terrestrial/solar GR tests or add a sourced gravitational field.

As R -> 1/sqrt(K), r and L diverge but rho -> pi/(2sqrt(K)); curvature invariants
remain Ricci scalar=12K and Riemann squared=24K^2. A radial affine null tangent
has |dR/dlambda|=E constant, so that endpoint is at finite affine distance.
The static observers' acceleration K R/sqrt(1-KR^2) diverges. The static chart
and congruence cease there; constant-curvature spacetime extends. Thus there
is a proved limiting central radar time, but no proved unreachable material
or global physical boundary. The intended UDT asymptote remains unestablished.

## 4. Local GR correspondence and what is actually retained

The exact contractions/Jacobi equations automatically reproduce the metric
readouts of ANY supplied GR metric using the same geodesics and observers;
that is a consistency property of geometry, not derivation of the GR metric
from UDT. At a point every smooth Lorentzian metric permits ordinary local
proper clocks and the calibrated c_E. Neither fact proves measured local
correspondence of an unselected cosmological completion.

Tile 3 gives explicit O(KL^2) metric and redshift corrections near a chosen
geodesic. Tile 2 admits a static base with its complete gravitational geometry;
letting a be constant returns that base exactly. Controlling a derivatives on
a small tube gives a controlled local perturbation, but no numeric terrestrial
bound is supplied here. The native response membership gate G301/G312 remains
unclosed under GR-as-filter; no sourced dynamics are adopted.

The constructive gain is (1)–(3), a joint nonstationary clock/area family (6)–(9),
the complete restricted inverse (10)–(14), and exact static distance functions
(17) with their actual failure/limit. No complete native positional function
is selected by the premises used here. This is a scoped nonselection after
actual construction, not a claim that a new premise or whole-universe uniqueness
is logically necessary before future progress.
