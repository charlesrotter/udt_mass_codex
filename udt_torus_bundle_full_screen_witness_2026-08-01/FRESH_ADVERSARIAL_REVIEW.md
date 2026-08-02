# Fresh zero-context adversarial review

Date: 2026-08-01  
Agent: `/root/fc07_cold_adversary`  
Verdict: **VERIFIED-WITH-CAVEATS**  
Mode: read-only; no repository mutations

## Independent ruling

The reviewer independently sustained:

1. eight unimodular controls and positive-definite convex full-screen interpolations;
2. exact `C-infinity` mapping-torus descent under the declared `s=1 -> s=0` convention;
3. spatial completeness by compactness/Hopf-Rinow and Lorentzian completeness by exact product
   geodesic splitting;
4. 27 unequal metric congruence-operator pairs and only `C_I=C_-I`, hence seven equality classes
   for the eight frozen representatives;
5. exact lattice-basis covariance;
6. six global oriented coframes and two nonorientable local reflection-transition coframes after
   fixing positive-oriented square roots;
7. invariant positive screens in six controls, with only parabolic and hyperbolic monodromy forcing
   variation in the chosen block/lattice presentation;
8. descent and integrability of the coordinate vertical projector, without identifying it with the
   parent metric-response projector or requiring parallelism.

## Required repairs closed during review

- Replaced malformed tab-containing source anchors with exactly four-field, tab-free rows.
- Made anchor schema/overflow/role validation fail closed.
- Specified positive-oriented square-root coframes before deriving `det(O)`.
- Fixed the endpoint plus/minus convention to remove an apparent `M` versus `M^-1` ambiguity.
- Scoped seven classes to equality of endpoint congruence operators for the frozen representatives,
  not conjugacy, diffeomorphism, or infinite-family classification.
- Reran stale captured outputs and narrowed “topology forces variation” to registered bundle
  monodromy in the chosen block/lattice presentation.

After repair: 22/22 source identities, 116 production checks, 302 independent checks, 33/33
semantic catches, six frozen manifests / 133 paths, and tests `70 passed, 1 xfailed` reproduce.

## Maximum defensible conclusion

```text
COMPLETE_OFFSHELL_FC07_METRIC_WITNESSES_EXIST_FOR_THE_EIGHT_FROZEN_CONTROLS
IN_THE_CHOSEN_CONSTANT_DEPTH_BLOCK_EXTENSION
SEVEN_FROZEN_ENDPOINT_CONGRUENCE_OPERATOR_CLASSES
NO_EXTENSION_OR_MONODROMY_SELECTION_DYNAMICS_STABILITY_BOOTSTRAP
RESPONSE_PROJECTOR_OR_MATTER_CLAIM
```
