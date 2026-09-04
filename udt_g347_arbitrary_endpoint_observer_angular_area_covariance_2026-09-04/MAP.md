# G347 map — arbitrary endpoint-observer angular-area covariance

Date: 2026-09-04
Status: preregistration stage

## Whole question

Starting only from G340, G343, G345, and G346, keep the supplied spacetime, endpoint events,
affinely scaled labelled null generator, and quotient-screen propagator fixed. Replace either or
both supplied normal endpoint observers by arbitrary future timelike unit observers. Determine
exactly how endpoint frequency, local celestial solid angle, observer screen representatives, the
two directional angular-area Jacobians, the squared-frequency reversal law, and the inverse-G345
geometric mean transform.

This is `METRIC_LED` and observing rather than targeting. It asks what the same metric-null relation
looks like to different local observers. It does not search for a preferred observer or add a light,
detector, transfer, distance, population, source, matter, scale, or observational model.

## Exact bounded arena

Use the supplied G340--G346 Taub/Kasner spacetime, one supplied nonzero future null generator `k`
on each fixed compact lift, all distinct positive endpoint pairs, all projective directions
including both principal limits, and the full G343 quotient-screen position block. At each endpoint
the original observer `u_i` is normal and the replacement observer `v_i` is any future unit vector

```text
v_i = gamma_i (u_i + beta_i),
gamma_i = 1/sqrt(1-|beta_i|^2),
|beta_i| < 1.
```

All longitudinal and transverse boost components are live. The null limit `|beta|=1` is a boundary,
not part of the timelike domain.

## Candidate local geometry

For any future unit observer `u`, freeze only the definitions

```text
omega_u = -g(k,u) > 0,
s_u = k/omega_u - u,
S(u,k) = {X : g(X,u)=g(X,k)=0}.
```

The metric quotient screen is `Q_k=k^perp/span(k)`. Test whether its representative in `S(u,k)`
changes by the metric isometry

```text
I_(v<-u)(X) = X + g(X,v) k/omega_v.
```

For a local sky tangent `theta_u`, test the exact aberration differential

```text
theta_v = (omega_u/omega_v) I_(v<-u)(theta_u),
dOmega_v = (omega_u/omega_v)^2 dOmega_u.
```

No special-relativistic aberration theorem may be quoted as proof; these formulas must be derived
from the supplied metric, null normalization, and observer definitions.

## Frozen transformation candidates

Write `D_i=omega_(v_i)/omega_(u_i)`. Test

```text
A'_(1<-0) = D_0^2 A_(1<-0),
A'_(0<-1) = D_1^2 A_(0<-1),

A'_(1<-0)/A'_(0<-1) = (omega_(v_0)/omega_(v_1))^2,
sqrt(A'_(1<-0) A'_(0<-1)) = 1/Dhat'_(10),
Dhat'_(10) = Dhat_(10)/(D_0 D_1).
```

Thus covariance, not numerical observer invariance, is the primary candidate. At a stationary
middle endpoint test `hhat'_1=hhat_1/D_1^2`, so the sewn directional law retains its form.

## Pure and easy routes

- Pure route used here: derive the observer screens, their quotient isometry, sky differential,
  frequency factor, and endpoint formulas directly from Lorentzian metric algebra and G343/G346.
- Easier but forbidden as proof: import textbook aberration, angular-diameter distance,
  Etherington reciprocity, geometric optics, flux, luminosity, or detector formulas.

## Required classifications

1. Cover every future timelike endpoint observer through finite boosts short of null.
2. Separate the observer-independent quotient-screen transport from observer-dependent frequency
   and celestial calibration.
3. Prove or refute quotient-screen isometry and the exact sky conformal factor.
4. Derive both independently changed directional areas and distinguish covariance from invariance.
5. Test squared-frequency reversal and inverse-G345 mean in the changed observer frames.
6. Test arbitrary endpoint `GL(2)` coordinates, common affine gauge, principal directions,
   coincidence limit, stationary sewing, and every compact path label.
7. Preserve singular or divergent behavior at the null-observer boundary as a classification,
   never as a discarded solution.
8. State all remaining observer, ray, path, spacetime, and operational dependence.

## Maximum conclusion

At most G347 may derive an exact finite-timelike-observer covariance law for G346's infinitesimal
directional metric angular-area pair on this supplied spacetime and labelled ray family. It may not
select a preferred observer, physical route, protocol, or population; establish a finite-beam or
light-transfer law; define brightness, flux, luminosity, probability, or observational distance;
or select occupancy, stability, matter/mass, a scale, `X_max`, or canon.
