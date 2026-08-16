# G110 audit report — one observer map, distinct pair and sky blocks

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_CAVEATS__REPAIRS_VERIFIED`

## Result

The G93--G109 architecture simplifies, but not by identifying every `2x2` object. For the
conditional point-observer exponential query,

```text
supplied (g, observer, normalized sky direction)
-> F(tau,lambda,n)=Exp_z(lambda k)
-> full dF=(pair columns, angular columns)
-> terminal phi_pair + angular expansion/shear + branch atlas.
```

The terminal clock-distance metric and the angular Jacobi map are distinct blocks of this one full
relation. Their common owner is `F` and `g`, not a literal matrix identity.

## Decisive catch proof

For the exact flat observer sky

```text
F(tau,lambda,n)=(tau+lambda,lambda n),
```

the pair metric is regular and returns `phi_pair=0`. The transverse projection of its pair columns
has rank zero, while the true angular Jacobi map is `lambda I` and has rank two for `lambda>0`.
More generally, the null tangent is screen-orthogonal, so the canonical pair-screen map has rank at
most one. Therefore G108's explicitly conditional same-`W` solder is not the canonical observer-sky
map, and its regular rank-two pair-screen stratum is empty on this subclass.

## What survives

- G93 terminal `h -> phi_pair -> c_eff/c_E` survives unchanged.
- G108's pair-screen area identity survives algebraically but is rank-degenerate on this subclass;
  its Jacobi/Riccati propagation survives when applied to the true angular block.
- G109 endpoint `Delta phi_pair` survives on one matched calibrated relation family.
- The G109 depth-parameterized screen rate survives as a chain rule between distinct blocks only
  where `dot(phi_pair) != 0`.
- Full `2x2` expansion and shear remain live; the anisotropic analytic control has nonzero shear.
- At a caustic, the second-order Jacobi map continues while the inverse/Riccati chart fails.

## What was scaffolding

- arbitrary independent `J` is removed on the point-observer exponential subclass;
- point-vertex screen amplitude is fixed by `D(0)=0`; `D'(0)` is the sky/screen
  basis-identification map and is `I` in matched orthonormal bases;
- local branch evolution follows from the exponential initial-value problem;
- individual `E/J` and `S/Z` representatives are not instrument loudnesses when their product is
  unchanged;
- the query names the measurement being made and is not itself a missing physical selector.

## What remains genuinely open

- which complete metric history is physical;
- whether the null/exponential observer query is the correct universal UDT observation protocol;
- the time-dependent celestial trivialization/null field carried along the observer;
- general finite-beam and extended-source initial data;
- global endpoint preimage handling, source occupancy, transfer, and branch weights;
- source, flux, action, bootstrap, `X_max`, and observational prediction.

## Evidence

- exact symbolic production: all checks pass;
- separate finite-difference implementation of the same analytic controls: all checks pass;
- maximum flat pair-metric residual: `2.20e-13`;
- maximum independent Jacobi residual: `3.22e-7` against `2.0e-6` tolerance;
- maximum vertex derivative residual: `6.67e-11`;
- distinct-block joined-rate residual: `3.88e-11`;
- anisotropic shear norm at the registered point: `0.1971310464`;
- all five hostile catch proofs pass.

## Landing

```text
OBSERVER_EXPONENTIAL_FULL_DIFFERENTIAL_RECONSTRUCTION_DERIVED_CONDITIONALLY
__TERMINAL_PAIR_AND_SKY_JACOBI_ARE_DISTINCT_BLOCKS
__POINT_VERTEX_SCREEN_DATA_FIXED_UP_TO_GAUGE
__LOCAL_BRANCH_ATLAS_METRIC_DERIVED
__G108_G109_LITERAL_SAME_W_SOLDERING_REQUIRES_REGRADING
__PHYSICAL_METRIC_HISTORY_GENERAL_QUERY_GLOBAL_WEIGHTS_AND_SOURCES_OPEN
```

Fresh zero-context adversarial review returned `VERIFIED_WITH_CAVEATS`; its required precision
repairs were implemented and the bounded follow-up returned `REPAIRS_VERIFIED` with no failures.
