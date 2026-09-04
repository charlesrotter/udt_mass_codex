# G347 preregistration — arbitrary endpoint-observer angular-area covariance

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and domain

Freeze the G340 metric-null frequency definition, G343 intrinsic quotient-screen propagator and
affine typing, G345 observer-calibrated scalar, and G346 directional infinitesimal angular-area
pair. The supplied exact spacetime, endpoint events, affine null generator, projective ray
direction, and compact lift do not change. Independently replace each normal endpoint observer by
every future unit timelike observer represented by a finite three-velocity `|beta_i|<1`.

Cover longitudinal, transverse, oblique, zero, near-null, and independently chosen endpoint boosts;
all mixed and principal ray directions; arbitrary common affine rescalings; arbitrary
well-conditioned endpoint `GL(2)` coordinates; all noncoincident endpoint orders and nonidentity
stationary triples; the coincidence limit; and each compact lift separately.

## Preregistered primary alternatives

1. `A__EXACT_FINITE_TIMELIKE_ENDPOINT_OBSERVER_COVARIANCE_CLOSES`: the quotient-screen change is an
   isometry, the sky map is conformal by the inverse frequency ratio, each directional area gains
   the squared source-end Doppler factor, and reversal, inverse-G345 mean, and stationary sewing
   retain exact covariant form.
2. `B__LOCAL_SKY_AND_SCREEN_MAPS_CLOSE_BUT_ONE_BILOCAL_IDENTITY_FAILS`: the local observer change is
   metric-owned, but at least one proposed directional-area, reversal, mean, or sewing factor is
   false.
3. `C__OBSERVER_CHANGE_REQUIRES_EXTRA_SCREEN_OR_TRANSPORT_STRUCTURE`: the quotient construction does
   not canonically relate arbitrary observer screens on the frozen ray.
4. `D__NO_FULL_FINITE_TIMELIKE_OBSERVER_CLASSIFICATION_CLOSES`: at least one regular boost, ray
   direction, coordinate gauge, endpoint order, or compact label is untyped or contradictory.

## Preregistered secondary alternatives

- quotient screen: `Q1__CANONICAL_METRIC_ISOMETRY` or `Q2__OBSERVER_DEPENDENT_EXTRA_STRUCTURE`;
- sky: `S1__DOMEGA_V=(OMEGA_U/OMEGA_V)^2_DOMEGA_U` or `S2__OTHER_OR_NONCONFORMAL`;
- directional areas: `A1__SOURCE_DOPPLER_SQUARED_ONLY` or `A2__TARGET_FACTOR_OR_OTHER`;
- reversal: `R1__NEW_SQUARED_FREQUENCY_RATIO` or `R2__BROKEN_OR_OTHER_FACTOR`;
- mean: `G1__INVERSE_CHANGED_G345_EXACTLY` or `G2__PARTIAL_OR_FALSE`;
- numerical status: `N1__COVARIANT_NOT_OBSERVER_INVARIANT` or `N2__OBSERVER_INVARIANT`;
- null boundary: `B1__SINGULAR_LIMIT_CLASSIFIED_NOT_INCLUDED` or `B2__REGULAR_EXTENSION_DERIVED`;
- physical typing: `P1__INFINITESIMAL_CAUSAL_GEOMETRY_ONLY` or
  `P2__PREFERRED_OBSERVER_LIGHT_OR_DISTANCE_LAW_DERIVED`.

`N2`, `B2`, and `P2` require an actual derivation from the frozen inputs. They may not be inferred
from a successful covariance check.

## Frozen local definitions and candidates

Use signature `(-,+,+,+)`. For a fixed nonzero future null `k` and future unit observers `u,v`,

```text
omega_u = -g(k,u),
omega_v = -g(k,v),
s_u = k/omega_u-u,
s_v = k/omega_v-v,
S(u,k) = u^perp intersect k^perp.
```

For `X in S(u,k)`, freeze and test

```text
I_(v<-u) X = X + g(X,v) k/omega_v,
g(I X,v)=g(I X,k)=0,
g(I X,I Y)=g(X,Y),
I_(u<-v) I_(v<-u) X = X.
```

For a projective null-direction variation represented at fixed `omega_u` by `delta k=omega_u
theta_u`, freeze and test

```text
theta_v = delta(k/omega_v) = (omega_u/omega_v) I_(v<-u) theta_u,
dOmega_v/dOmega_u = (omega_u/omega_v)^2.
```

Relative to the normal observer write `v=gamma(u+beta)` and `k=omega_u(u+s_u)`. Freeze and test

```text
D := omega_v/omega_u = gamma(1-beta dot s_u) > 0.
```

At endpoints let `D_i=omega_(v_i)/omega_(u_i)`. Freeze

```text
A'_(1<-0) = D_0^2 A_(1<-0),
A'_(0<-1) = D_1^2 A_(0<-1),
A'_(1<-0)/A'_(0<-1) = (omega_(v_0)/omega_(v_1))^2,

Dhat'_(10) = Dhat_(10)/(D_0 D_1),
sqrt(A'_(1<-0) A'_(0<-1)) = 1/Dhat'_(10).
```

For a stationary join through endpoint 1, freeze

```text
hhat'_1 = hhat_1/D_1^2,
A'_(2<-0) = hhat'_1 A'_(2<-1) A'_(1<-0).
```

Observer-induced screen maps must be composed with arbitrary passive endpoint `GL(2)` coordinate
changes rather than mistaken for them. Under common affine `k -> a k`, every `D_i` and every final
area identity must remain unchanged.

## Required derivation and evidence

1. Derive all local formulas directly from the metric inner product; no imported aberration or
   optical theorem may serve as proof.
2. Prove the quotient representative map is well defined, isometric, inverse under observer
   exchange, and transitive through a third observer.
3. Derive the two-dimensional sky area factor from the full tangent map, including transverse
   boosts; checking only collinear Doppler factors fails the preregistration.
4. Derive both directional areas with independent endpoint observers. Explicitly disprove numerical
   observer invariance when `D_i != 1` if alternative `A` holds.
5. Recompute reversal, G345 transformation, geometric mean, and stationary sewing algebraically.
6. Production must execute at least 12,000 checks across logarithmic endpoint/ray samples, at least
   1,000 general finite boosts including `|beta|>0.99`, arbitrary screen `GL(2)` frames, affine
   rescalings, all principal/mixed directions, and both independent endpoint changes.
7. An implementation-distinct verifier may not import production or G340/G343/G345/G346 code. It
   must reconstruct the local Lorentzian observer algebra and bilocal determinant identities by a
   different parameterization for at least 4,500 checks.
8. Raw double-precision relative tolerance is `8e-10` for local metric identities, `8e-9` for
   bilocal/quadrature identities, and `8e-8` for near-null and general-frame determinant checks.
9. Hostile mutations must catch at least: reverse the Doppler factor; use one sky power; add a
   target Doppler factor; declare numerical observer invariance; omit the null-rotation term in
   the screen map; use a nonisometric projection; reverse a screen dual map; omit either endpoint
   factor in G345; use an arithmetic mean; leave `hhat_1` unchanged; use `D_1^2 hhat_1`; break
   affine invariance; delete transverse boosts; include the null observer boundary as regular;
   select a preferred observer; sum/select compact lifts; or promote the result to light,
   brightness, distance, scale, or `X_max`.
10. Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package
    evidence bytes during no-write replay.

Any correction to the frozen formulas, alternatives, tolerances, or maximum conclusion after first
execution is a preregistered failure and must be recorded before rerun.

## Completeness and maximum conclusion

This is one exact-spacetime, fixed-ray, infinitesimal endpoint-observer tile. It covers the full
future-timelike observer hyperboloid at both endpoints but not finite beams, generic spacetimes,
physical observer populations, emission/detection, transfer, observational distance, matter,
stability, occupancy, scale, or global completion.

The maximum landing is exact finite-timelike observer covariance—or its scoped refutation—for the
G346 directional metric angular-area pair. No preferred frame, physical protocol, route,
population, light law, observational prediction, scale, `X_max`, or canon may be selected.
