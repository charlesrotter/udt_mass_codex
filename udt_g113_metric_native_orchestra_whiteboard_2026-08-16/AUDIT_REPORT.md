# G113 audit report — metric-native orchestra whiteboard

Date: 2026-08-16

Status:

```text
MULTIAGENT_ADVERSARIAL_SYNTHESIS_WITH_EXACT_CHECKS
__ONE_FULL_OBSERVER_DIFFERENTIAL_IS_THE_SMALLEST_LOCAL_ASSEMBLY
__STATIC_CENTRAL_SPHERICAL_CHORD_DERIVED_CONDITIONALLY
__P1_STATIC_PROFILE_INVERSION_FAILS_SMOOTH_CENTER
__G112_REMAINS_CONDITIONAL_NONREGRESSION
__COMMON_SOURCE_MULTI_OBSERVER_QUERY_IS_NEXT_GATE
```

## Result

The recent simplification is real, but its meaning is narrower and cleaner than “we found the
orchestra score.”

For one supplied metric history and one typed point-observer query, the metric naturally supplies
one exponential map and its full differential,

```text
(g,z,u,k) -> F(tau,lambda,n) -> dF=(T,K,J1,J2) -> H=F* g.
```

The terminal pair metric, sky Jacobi map, shear, mixed contractions, and path transport are typed
readouts of that one object. They are not independent knobs and they are not one scalar. Along one
fixed ray, the smallest closed compositional carrier is the Jacobi phase-space propagator carrying
`(J,nabla_K J)`. Across several observers or rays, those carriers meet at calibrated source/event
junctions; equal matrix size does not authorize multiplication or identification across the
junction.

This is a genuine removal of scaffolding. It does not select the physical complete metric history,
source intersection, observational transfer, or global relation family.

## Exact spherical chord

On the supplied static, central, spherical, radial-null subclass

```text
ds^2=-f(r)c_E^2 dt^2+f(r)^-1 dr^2+r^2 dOmega^2,
f=exp(-2 phi),
```

the radial null graph gives, in `y0=c_E tau` and `y1=r`,

```text
h_pair=[[-f,-1],[-1,0]],
det(h_pair)=-1,
phi_pair=-(1/2)log f=phi,
D_sky=r I2
```

in matched sky/screen bases. Therefore G112's isotropic screen form is metric-derived on this
precise subclass. It is not a general result of G110/G111.

## Exact obstruction to static P1 promotion

Promoting the observed P1 null-cone chord

```text
r(phi)=n X_eff [1-exp(-2 phi/n)]
```

to that static spatial metric gives

```text
phi(r)=-(n/2)log[1-r/(n X_eff)],
f(r)=[1-r/(n X_eff)]^n.
```

At the proposed observer center,

```text
phi'(0)=1/(2 X_eff),
f'(0)=-1/X_eff.
```

A smooth rotationally invariant scalar has zero first radial derivative at a regular center. The
failure is invariant: direct four-dimensional curvature reconstruction gives

```text
lim_(r->0) r R = 6/X_eff,
lim_(r->0) r R_hat(theta,phi,theta,phi) = 1/X_eff.
```

Thus the exact P1 inward extrapolation is a punctured static congruence with a curvature singularity,
not a smooth point-observer metric. The observed SNe interval does not contain the center, so this
does not invalidate P1 as an empirical annular/null-cone chord. It invalidates only its silent
promotion into a smooth static spatial profile.

## What the two SNe datasets established

G112 shows that the G110/G111 type correction is numerically non-regressive:

```text
Pantheon+ maximum pointwise change: 4.44e-15
DES maximum pointwise change:        1.78e-15
```

Under the inherited conditional transfer, SNe magnitudes constrain only

```text
2 Phi(z) + (1/2) log det D_sky(z)
```

up to one magnitude offset. They do not separately identify terminal pair depth, screen area,
shear, rotation, mixed blocks, or one-`F` realizability. Pantheon+ is the calibration set; DES is
the cross-reduction holdout and retains its low-chi-square/effective-DOF warning.

## The exposed category error

The frozen P1 object is an observed relation along a past observation cone. It is not automatically
a static function on a spatial slice. A regular time-live geometry can generate a linear
redshift-distance relation through source/intersection history while its spatial center remains
smooth, but current evidence does not derive that realization.

On the G110 point-observer query, a smooth central geodesic observer has

```text
phi_pair'(0)=<U,nabla_U K>=-<a_U,K>=0.
```

Therefore the observed linear low-distance SNe slope cannot be assigned to this terminal pair
block alone without reopening the source congruence/intersection and observable-transfer slots.
That is not a failure of the metric. It says the SNe query has not yet been completely typed.

## Next bounded gate

Before another solve or fit, define one common-source, three-observer query with:

- three observer worldlines and one source worldline/event;
- every exponential preimage retained as a path-labelled branch;
- one Jacobi phase-space propagator per ray;
- terminal pair metrics kept distinct from sky maps;
- explicit observer and source screen/covector calibration at each junction;
- source transfer and branch weights sealed as `OPEN`.

This is the minimum three-observer loop network that tests descent and loop consistency rather than
another pair identity. After that contract is frozen, run an outcome-blind regular time-live spherical jet
census. Only afterward compare its already-determined light-cone series with the frozen SNe chord.

## Maximum conclusion

```text
THE_METRIC_NATURALLY_ASSEMBLES_TYPED_PAIR_ANGULAR_AND_MIXED_READOUTS_THROUGH_ONE_FULL_OBSERVER_DIFFERENTIAL;
NO_EXTRA_SCALAR_ORCHESTRA_SCORE_IS_REQUIRED_FOR_LOCAL_ASSEMBLY;
THE_STATIC_CENTRAL_SPHERICAL_REDUCTION_BINDS_PHI_PAIR_AND_D_SKY_BUT_THE_EXACT_P1_STATIC_INVERSION_IS_CENTER_SINGULAR;
G112_IS_OBSERVATIONAL_NONREGRESSION_NOT_HISTORY_SELECTION;
PHYSICAL_HISTORY_SOURCE_QUERY_TRANSFER_XMAX_BOOTSTRAP_ACTION_AND_MATTER_REMAIN_OPEN.
```

No canonization follows.
