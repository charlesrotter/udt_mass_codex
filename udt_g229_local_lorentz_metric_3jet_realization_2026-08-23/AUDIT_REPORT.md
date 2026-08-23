# G229 audit report — local Lorentz-metric 3-jet realization

Date: 2026-08-23

## Primary landing

```text
FULL_LOCAL_3JET_REALIZATION
__ONE_SUPPLIED_EVENT_AND_FIXED_TANGENT_FRAME
__C2_RANK20_KERNEL80
__C3_RANK60_KERNEL140
__KERNELS_EXACTLY_HIGHER_COORDINATE_GAUGE
__NORMAL_SLICES_ISOMORPHIC
__SMOOTH_LOCAL_LORENTZ_POLYNOMIAL_REPRESENTATIVE
__G188_G227_G228_PROJECTIONS_RECOVERED
__NO_VALUE_GENERATION_OR_REGIONAL_GLOBAL_HISTORY
```

## Result

The apparent gap between the G227/G228 curvature algebra and an actual local metric closes at one
event. Every supplied algebraic curvature tensor and every supplied differential-Bianchi-compatible
first curvature derivative is realized by a smooth Lorentz metric through cubic Taylor order in
geodesic normal coordinates.

The whole locally inertial metric arenas were retained:

| map | domain | exact rank | kernel | kernel owner |
|---|---:|---:|---:|---|
| `C2: H -> R` | 100 | 20 | 80 | cubic coordinate changes |
| `C3: K -> nabla R` | 200 | 60 | 140 | quartic coordinate changes |

The normal-coordinate constraints have ranks 80 and 140, leaving 20- and 60-dimensional slices.
Both restricted curvature maps are isomorphisms. The exact inverse formulas and all composition
checks pass.

## Independent certification

The production implementation uses the G227 20-slot basis and the G228 reduced 80-slot derivative
arena. The independent implementation uses only Python standard-library `Fraction`, keeps all 21
symmetric-bivector curvature slots and all 84 derivative slots, and imposes Bianchi constraints as
separate rows. It finds:

- curvature-map rank 20;
- derivative-curvature-map rank 60;
- combined derivative constraint rank 24, hence target dimension 60;
- cubic/quartic gauge ranks 80/140 and exact kernel inclusion;
- normal-constraint ranks 80/140;
- restricted normal-slice ranks 20/60;
- complete-basis inverse identities with the frozen signs.

The four shared gauge/normal matrices also reproduce the production SHA-256 hashes exactly. An
additional independent agent used a different eliminated Bianchi slot and returned the same ranks
and inverse signs.

## Projection and sign bridge

Composition through the realized metric jets reproduces the G227 rank-19 null tide, its rank-20
timelike augmentation, and the complete 15-subset G228 projection census. A nonzero exact witness
gives tidal matrix `diag(1,0)` and Jacobi lower-left block `diag(-1,0)`, matching the frozen G188
equation `D'' + T D = 0`.

## Smoothness and coordinate scope

The explicit cubic polynomial metric is smooth and satisfies the exact radial normal-coordinate
identity. Lorentz signature holds on a sufficiently small neighborhood whose radius depends on the
supplied finite coefficients. The theorem does not claim a common radius.

The tangent frame is fixed. Residual linear Lorentz transformations only change components and are
not counted in the higher-coordinate kernels.

## Hostile controls and disclosed repair

All nine valid hostile controls pass: wrong `C2` and `C3` signs, omitted normal constraints,
truncated coordinate gauge, one-sided gauge wiring, non-Bianchi target data, unsymmetrized cubic
inverse, an unfixed-frame overclaim, and a global-history overclaim.

The first hostile draft attempted to mutate Lorentz-sign lowering. That control correctly failed to
detect a difference because, on the full free gauge domain, the sign change is an invertible column
reparameterization and leaves the image unchanged. It was retired as an invalid mutant and replaced
by the genuine one-sided index-wiring defect. The scientific outcome and preregistered alternatives
were unchanged.

## Exact scope boundary

G229 proves local realizability of **supplied point jets**. It does not generate curvature values,
does not realize an arbitrarily prescribed curvature field over a region, and does not select a
metric history. Observer/null population, transport, dynamics, action, source, matter, bootstrap,
boundary, `X_max`, transfer, observation, mass, and signalling remain outside this gate.

## Lay conclusion

The bend and the first change of bend found in G227/G228 are not merely abstract bookkeeping. Every
allowed combination can be played by an actual smooth local metric. The many extra Taylor
coefficients are exactly coordinate labeling; after normal coordinates are fixed, only the genuine
20-plus-60 geometric notes remain.

This closes the local “can a metric do it?” question. It does not yet answer “which notes does the
physical UDT metric play across an extended region?”
