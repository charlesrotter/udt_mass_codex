# What July's optical-time relation actually requires

Status: CONDITIONAL MATHEMATICAL APPLICATION, UNPROMOTED; direct review pending.
Scope/authorization: WORK_ORDER.md. Source hashes: SOURCE_PINS.json.
This reconstructs consequences of supplied geometries and an existing clock
identity. It does not select a UDT field equation or physical history.

## 1. The historical clue and the actual question

July's P-opt was `d ell_opt = kappa d phi`, with positive constant kappa,
on the stationary reciprocal radial metric. Its derivation document explicitly
called P-opt a working principle, not a consequence of bare reciprocity.
The subsequent WR-L result selected it under an additional affine areal
recentering and wall-regularity package. Those historical assumptions are not
current inputs to the local kernel. Neither a spherical physical center nor
the July boundary/scale is restored here.

The useful content is a precise possible relation between null travel timing
and received clock contrast. The tests below distinguish that relation from
the founding interpretation that positional dilation IS causal geometry.
The latter does not, as a matter of units or terminology, assert constant
logarithmic redshift per unit optical time.

## 2. Exact stationary calculation

Supply the smooth longitudinal block

    g_long = -f(x) c_E^2 dt^2 + f(x)^-1 dx^2,   f>0,
    phi(x) = -log(f(x))/2.

This is a diagnostic class. Keeping an areal angular sector gives the F4
static spherical branch; other stated transverse sectors below are controls,
not silently substituted F4 geometry. No field equation is imposed.
Use a compact interval inside f>0. For x>x0, define the positive optical length

    O(x0,x) = integral_[x0,x] dx/f,
    D(x0,x) = phi(x)-phi(x0).

Null travel takes coordinate time O/c_E. The receiver fixed at x0 has normal
proper clock `d tau_0 = sqrt(f0) dt`, so its travel-time equivalent length is

    L_0 = sqrt(f0) O,    f0=f(x0).

For an inward received-clock query from x to x0, stationarity and G220 give

    r_(x->0) = d tau_0/d tau_x = sqrt(f0/f(x)),
    log(1+z_(x->0)) = log r_(x->0) = D.

The positive optical length is not itself a received tick-rate ratio. The
coordinate arrival map is t_receive=t_emit+O/c_E, whose derivative is one;
the endpoint proper-clock factors supply the nontrivial ratio here.

Impose historical P-opt on every subinterval in the increasing-x direction:

    dx/f = kappa d phi,   kappa>0 constant.

Since `d phi = -f' dx/(2f)`, this is equivalent to

    f' = -2/kappa.                                          (1)

Thus the consequence is exactly the affine family

    f(x) = f0 - 2(x-x0)/kappa

on its positive interval. Conversely this family satisfies P-opt. Taking
f0=1, x0=0 recovers July's local expression; its zero need not be included,
identified with X_max, or endowed with a global boundary interpretation.
The constant remains supplied. The calibration c_E does not supply kappa.

If f is any decreasing positive profile, defining the variable
`kappa(x)=-2/f'(x)` rewrites the differential equality. That identity does not
select a profile. Constancy of kappa is the extra restriction.

Counterprofile: for supplied a>0, `f=exp(-2ax)` is smooth, positive and
reciprocal, but `dO/dphi=exp(2ax)/a` is not constant. This refutes deduction
of P-opt from this reciprocal form alone. It is not an all-UDT countermodel:
no full current response-class membership or physical realization is claimed.

## 3. Changing the observer and the direction

For the affine family write b=2/kappa>0 and f=C-bx. The proper-clock version is

    L_0 = kappa_0 D,    kappa_0 = sqrt(f0) kappa.             (2)

One can verify the same factor by using the normalized reciprocal coordinates

    t_0=sqrt(f0)t,    y=(x-x0)/sqrt(f0),
    f_tilde(y)=f(x)/f0=1-(b/sqrt(f0))y.

Here kappa_0 has the same length units but a different value for different
static reference clocks. This is a conversion between specified queries,
not evidence for a preferred observer. A single numerical coefficient in all
those clock normalizations is not a consequence of P-opt. A physical law
could specify the transformation; this calculation does not select one.

For the reverse future exchange, with these same stationary worldlines,

    r_(0->x) = sqrt(f(x)/f0) = 1/r_(x->0).

Travel duration is positive in either direction. Therefore a universal rule
`log r = positive constant times positive travel duration` for BOTH exchanges
does not follow from this static construction. Its signed endpoint depth
must not be relabeled as the same positive received redshift both ways.
This retains ordinary gravitational redshift/blueshift in the combined
geometry. It does not exclude mutual redshift on other observer histories.

## 4. A flat control and the importance of the transverse geometry

For f=1-bx, append flat Cartesian transverse directions and set T0=c_E t.
Use coordinates

    rho=2 sqrt(f)/b,
    T=rho sinh(b T0/2),    X=rho cosh(b T0/2).

Direct pullback gives

    -dT^2+dX^2+dy^2+dz^2
      = -f dT0^2+dx^2/f+dy^2+dz^2.

Thus the longitudinal P-opt relation occurs in exactly flat spacetime with
accelerating stationary-coordinate observers. It does not distinguish a new
positional contribution from already permitted acceleration effects.
This is a control, not the proposed UDT universe or the areal F4 branch.

Appending `x^2 dOmega^2` instead gives the supplied spherical tensor with
Ricci scalar `6b/x` and Kretschmann scalar `8b^2/x^2` on x>0. The same
longitudinal timing relation therefore does not determine the angular/area
geometry used in supernova brightness predictions. On fixed b, curvature
labels x: merely recentering the same radial formula cannot provide identical
overlapping observer charts of that one tensor. This is the historical
branch-specific obstruction, not a prohibition on observer-relative distances
or arbitrary coordinate origins.

## 5. What survives in a covariant accumulation statement

Use the exact G402/G403 identity on a supplied smooth unit observer field U
and a regular future null branch, c_E=1 proper-length time units. Write

    k=omega(U+n),   omega=-g(U,k)>0,   |n|_U=1,
    ds_U=omega d lambda>0,
    H=div(U)/3,    a=nabla_U U,    sigma=spatial symmetric trace-free shear.

Then, for the actual received-clock ratio,

    log r_AB = integral_A^B [H+a.n+sigma(n,n)] ds_U.          (3)

This is an exact geometric accumulation formula, already owned by the sources.
No Hubble law, Einstein field equation, density, matter source, or additional
redshift mechanism is used. H is the expansion of the SUPPLIED observer
congruence. Its appearance in a kinematic identity neither selects a cosmology
nor requires that all observed redshift come from expansion.

The measure ds_U is accumulated local rest-length along the ray. It is not
automatically an endpoint radar distance, areal radius, or one observer's
optical timing coordinate. In the static example, U=f^-1/2 partial_T0 gives

    ds_U=|dx|/sqrt(f),    dO=ds_U/sqrt(f),
    dL_0=sqrt(f0/f) ds_U.

Consequently July's constant rate per optical length is not a constant rate
per local rest-length. Their conversion factor changes along the ray.

There is a useful exact test of a tempting strengthening. Suppose one demands
at an event that the TOTAL accumulation rate in (3) be a single scalar K,
independent of every unit spatial direction n. Then

    H+a.n+sigma(n,n)=K for all n
    iff a=0, sigma=0 and H=K.                               (4)

Proof: compare n and -n to remove a; a quadratic form constant on the unit
sphere is a scalar multiple of the spatial metric, and trace-free sigma then
vanishes. Its remaining value is H. The converse is immediate.
Requiring K to be constant throughout a region is a further condition.
Positive K requires expansion of that chosen observer family in this test;
it is not imposed or inferred for the founding UDT postulate.

As a conditional witness, `g=-dT^2+exp(2hT)(dx^2+dy^2+dz^2)`, U=partial_T,
has a=sigma=0 and H=h. The rate (3) is constant h. For two comoving points
on a regular radial null segment, `log r=h(T_B-T_A)`. h is freely supplied;
this mathematical control does not adopt Hubble expansion or GR dynamics.

Equation (4) must not be applied to an invented isolated 'positional term'.
Equation (3) describes the total received-clock observable. Separating it into
independently physical positional, velocity and gravitational terms requires
additional justified structure, not a label attached to one summand.

## 6. Bounded outcome and next dependency

The July idea yields a sharp, testable restriction: constant optical advance
per depth selects an affine lapse in its stationary reciprocal class. The
relation survives as a conditional description, with explicit observer-clock
normalization and direction. It is not a new selection from the founding
postulate, a universal mutual-slowing law, or a supernova prediction.

The useful general survivor is the actual null-clock accumulation (3), together
with a clear warning against replacing its variable, directional integrand
by a constant without a derivation. The old radial fit does not determine the
transverse optical area, and a preferred center cannot fill that gap.

This exploration reaches an ownership stop: derive or otherwise justify the
complete metric/physical observer-and-path assignment determining the rate in
(3). No such assignment is supplied by P-opt or its reformulations here.
The result narrows this particular lead; it is not proof that all existing UDT
premises are insufficient, that another postulate is necessary, or that the
founding positional interpretation is false. Current source grades, native
response identification and the no-required-Hubble-expansion aim are unchanged.
