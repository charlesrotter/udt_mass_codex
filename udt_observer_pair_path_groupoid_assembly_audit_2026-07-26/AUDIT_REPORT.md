# Observer-pair path-groupoid assembly audit

Date: 2026-07-26

Preregistration: `f7073f2`

Grade: `VERIFIED_WITH_CAVEATS_BOUNDED_PAIR_FRAME_PATH_GROUPOID_CLASSIFICATION`

## Result first

The corrected local alignment closes the observer-pair **kinematic assembly** at the properly typed,
path-labelled level:

```text
The natural objects are ordered observer/ruler pairs, not bare events.
On those objects, metric transport and explicit pair changes form an exact path groupoid
for every real lambda.
```

The middle mismatch found by the earlier triangle audit is the vertical arrow between two different
pair frames at the same event. It is required when an outgoing comparison resets the observer or
ruler direction. Including it gives exact composition. Omitting it while silently changing the pair
creates the mismatch.

The scalar-screen endomorphism

```text
X_lambda(u,n)=-P_u+P_n+lambda(I-P_u-P_n)
```

is independent of the unresolved screen `SO(2)` orientation. A full oriented screen coframe still
has that gauge, but the reciprocal endomorphism does not need an endpoint coframe section merely to
exist or compose.

## What this corrects

The earlier statement that the smallest missing object was always an “endpoint solder or connection
section” was too broad after the local pair-alignment correction.

- A supplied complete metric already supplies Levi-Civita path transport.
- A supplied ordered pair supplies `X_lambda` modulo screen rotation.
- A reset between two supplied pairs is an explicit vertical arrow.
- A one-frame-per-event section is needed only to collapse this richer path groupoid onto bare
  endpoints or to claim one global full coframe.

Historical calculations remain exact and unchanged. This package adds the corrected type overlay.

## The remaining missing object

For signed additive depth `delta_gamma`, define

```text
D(delta_gamma)=exp(delta_gamma X),
T_gamma=U_gamma D(delta_gamma).
```

The full comparison composes and reverses exactly for every `lambda` if `delta` is an additive
cocycle on the typed path arrows. But the metric has not yet derived which physical `delta` belongs
to an observer-pair arrow.

Levi-Civita transport cannot fill that role: it is metric-isometric, while nonzero aligned
reciprocal dilation is not. The smallest remaining kinematic join is therefore:

```text
a metric-native signed depth assignment on typed observer-pair path arrows.
```

## Exact depth alternatives

- Any endpoint-only real additive cocycle is necessarily `phi(B)-phi(A)` up to an additive
  constant.
- The prior round-branch result says such a scalar difference cannot also encode every positive
  isotropic pair-distance magnitude.
- A one-form integral always composes on paths, but endpoint independence requires zero loop
  periods.
- The real exponential reciprocal character is faithful, so a nonzero depth period produces a
  nonidentity reciprocal loop.
- A symmetric nonnegative distance magnitude cannot itself be the signed reversal-odd depth except
  trivially; it needs an orientation lift and generally an angular composition law.

## Lambda and global status

No `lambda` is selected. `lambda=1` removes ruler-direction dependence for one fixed observer, but
observer dependence remains. No value makes `X_lambda` a function of a bare event.

Noncentralizing two-path holonomy does not break the path groupoid; it prevents an ordinary
path-independent endpoint collapse. Cut-locus path families remain valid distinct arrows.

## What remains open

- the metric-native signed depth law and its dimensional normalization;
- whether the physical type is endpoint, path, observer-chart, or nonadditive bilocal;
- physical path/event pairing, cut-locus choice, and complete finite-cell branch;
- `lambda` and any full screen coframe section;
- `X_max`, density/bootstrap feedback, action, carrier, source, boundary, mass, and dynamics.

## Evidence gates

1. **Preregistered:** yes, commit `f7073f2`, before outcome algebra.
2. **Full or bounded:** complete for all real `lambda`, ordered orthonormal pair projectors, scalar
   screen rotations, metric-isometric path maps, vertical pair changes, additive real path depths,
   endpoint cocycles, and real loop periods. It does not classify arbitrary anisotropic screen
   responses or select a complete solution.
3. **Independent:** a no-SymPy `Fraction` implementation checks five `lambda` values, five typed
   path compositions, five vertical compositions, 125 endpoint-potential triangles, five positive
   character factors, and centralizing/noncentralizing loop witnesses.
4. **Premises audited:** local alignment, observer/ruler inputs, screen gauge, path, vertical reset,
   depth type, path independence, holonomy, `lambda`, and excluded physics are separate.

No fresh external-model review was authorized.

Maximum conclusion:

```text
ORDERED_PAIR_FRAME_PATH_GROUPOID_KINEMATICS_DERIVED_GIVEN_COMPLETE_METRIC_PATH_AND_PAIR_INPUTS;
MIDDLE_MISMATCH_RESOLVED_AS_EXPLICIT_VERTICAL_PAIR_CHANGE;
SCREEN_SO2_DROPS_OUT_OF_SCALAR_SCREEN_RECIPROCAL_ENDOMORPHISM;
TYPED_COMPOSITION_NONSELECTING_FOR_ALL_LAMBDA;
METRIC_NATIVE_SIGNED_DEPTH_ASSIGNMENT_REMAINS_OPEN.
```

