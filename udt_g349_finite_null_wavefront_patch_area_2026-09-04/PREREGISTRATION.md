# G349 preregistration — finite null-wavefront patch area

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and domain

Let `(M,g)` be any supplied smooth time-oriented four-dimensional Lorentzian manifold, `p` a
supplied source event, and `u` a supplied future unit timelike observer at `p`. Let `U` be any
compact piecewise-smooth patch in the observer's celestial sphere. Every `n in U` labels the future
null ray with the observer-normalized initial tangent. Let `tau:U->(0,infinity)` be any supplied
smooth affine cut for which all labelled geodesics exist regularly and depend smoothly on `n`.

Freeze the finite map

```text
F(n)=gamma_n(tau(n)).
```

Include all rank-two, rank-one, and rank-zero points of `dF`, caustics, folds, cusps if present,
repeated images, and separately supplied path labels. Do not assume injectivity, a pre-caustic
domain, a field equation, symmetry, topology, or a physical ray population.

## Preregistered primary alternatives

1. `A__FINITE_METRIC_PATCH_AREA_CLOSES_WITH_MULTIPLICITY_AND_CAUSTICS`: G348 is the exact metric
   two-Jacobian of `F`; its integral equals sheet area counted by global preimage multiplicity;
   geometric union area is a distinct global quantity and all critical strata remain typed.
2. `B__ONLY_INJECTIVE_PRECAUSTIC_PATCHES_CLOSE`: the finite identity is valid only after deleting
   critical points or repeated sheets.
3. `C__INFINITESIMAL_JACOBIAN_DOES_NOT_DEFINE_ANY_FINITE_GEOMETRIC_AREA`: no coordinate-free
   finite integral follows even with the complete supplied map and multiplicity.
4. `D__FINITE_AREA_REQUIRES_A_PHYSICAL_LIGHT_OR_TRANSFER_PREMISE`: geometric integration cannot be
   separated from emission, detection, or transfer physics.

Alternatives B--D win if the direct derivation or a retained counterexample requires them. No
candidate may be discarded because its image folds, overlaps, or has zero local area.

## Preregistered secondary alternatives

- cut: `T1__CUT_GRADIENT_IS_PURE_NULL_LONGITUDINAL_AND_DROPS_FROM_AREA` or
  `T2__CUT_GRADIENT_ADDS_TRANSVERSE_AREA`;
- local-to-finite: `J1__G348_DIRECTIONAL_AREA_IS_THE_METRIC_TWO_JACOBIAN_OF_F` or `J2__OTHER`;
- multiplicity: `M1__AREA_FORMULA_COUNTS_EVERY_PREIMAGE_SHEET` or
  `M2__LOCAL_ABSOLUTE_JACOBIAN_DIRECTLY_EQUALS_UNION_AREA`;
- union: `U1__UNION_AREA_NEEDS_GLOBAL_PREIMAGE_IDENTIFICATION` or
  `U2__POINTWISE_JACOBIAN_FIELD_ALONE_DETERMINES_UNION_AREA`;
- equality: `E1__MULTIPLICITY_AND_UNION_AREAS_AGREE_IFF_N_EQUALS_ONE_ALMOST_EVERYWHERE` or
  `E2__AGREE_ONLY_FOR_STRICTLY_INJECTIVE_MAPS` or `E3__OTHER`;
- critical set: `C1__CRITICAL_POINTS_REMAIN_AND_HAVE_ZERO_LOCAL_TWO_JACOBIAN` or
  `C2__CRITICAL_POINTS_MUST_BE_DELETED`;
- sign: `S1__SIGNED_SHEET_INTEGRAL_IS_ORIENTATION_DEPENDENT_AND_CAN_CANCEL` or
  `S2__SIGNED_INTEGRAL_IS_POSITIVE_UNION_AREA`;
- observers: `O1__FINITE_SHEET_MEASURE_IS_SOURCE_OBSERVER_COVARIANT_POINTWISE` or
  `O2__OBSERVER_CHANGE_ALTERS_THE_GEOMETRIC_SHEET_MEASURE`;
- labels: `L1__PER_LABEL_RESULTS_AND_DECLARED_DISJOINT_UNION_CENSUS_ONLY` or
  `L2__METRIC_SELECTS_A_PHYSICAL_LABEL_WEIGHT_OR_SUM`;
- physical typing: `P1__FINITE_GEOMETRIC_AREA_ONLY` or
  `P2__LIGHT_TRANSFER_BRIGHTNESS_DISTANCE_OR_POPULATION_LAW_DERIVED`.

`M2`, `U2`, `C2`, `S2`, `L2`, and `P2` require derivation and may not be inferred from familiar
optics language.

## Frozen geometric definitions

For `v in T_nU`, let `J_v` be the source-vertex Jacobi field from varying the initial null direction
at fixed affine parameter. Differentiating the cut map must give

```text
dF_n(v)=J_v(tau(n)) + d tau_n(v) k_n(tau(n)).
```

Define the metric two-Jacobian relative to the celestial metric `s_u` by

```text
J_g F(n)=sqrt(det(F* g)_n / det(s_u)_n)
```

on the rank-two stratum and by zero on ranks one and zero. The determinant means the positive
spacelike quotient determinant. Its coordinate-free density is `J_g F dOmega_u`.

For the full supplied map define the measurable preimage multiplicity

```text
N(F,U;y)=number of n in U with F(n)=y,
```

allowing infinity on exceptional values. Freeze

```text
A_mult(F,U)=integral_U J_g F dOmega_u,
A_union(F,U)=integral_(F(U)_regular) 1 dA_g.
```

The target density `dA_g` is the Lorentzian metric's positive spacelike two-area density on each
regular image sheet. In a chart proof an auxiliary positive Riemannian metric may define
rectifiability; its density must cancel from the final formula and may not become physical input.

## Frozen analytic claims to prove or refute

1. Source-vertex variation obeys `g(J_v,k)=0`; therefore the `d tau(v) k` term changes neither
   `F*g` nor `J_gF`.
2. `J_gF` equals the G348 source-to-target directional area density at each supplied direction,
   with every endpoint metric and frequency factor retained.
3. The coordinate-free area formula gives

   ```text
   A_mult(F,U)=integral_(F(U)) N(F,U;y) dA_g(y).
   ```

4. Consequently `A_union<=A_mult`, with equality exactly when `N=1` for almost every regular image
   point of positive metric area. Isolated multiple points or critical values of zero two-area do
   not spoil equality.
5. Rank-one and rank-zero points have zero local two-Jacobian but remain in `F`; no claim that all
   rank-one points are folds is permitted without an extra genericity theorem.
6. With optional compatible orientations, the signed coefficient may flip and cancel; absolute
   sheet area and union area remain nonnegative and distinct from it.
7. For the same intrinsic ray patch under a finite source-observer change, G348 gives

   ```text
   J'_gF=D(n)^2 J_gF,
   dOmega'=D(n)^(-2) dOmega,
   ```

   so the product and its finite integral are unchanged. Target observer changes are quotient
   isometries. Null observers remain excluded.
8. Each supplied label has its own map and theorem. A declared disjoint union counts label
   multiplicity mathematically; it neither chooses labels nor supplies weights or probabilities.

## Required witnesses and evidence

The production route must retain at least these map classes:

1. injective anisotropic affine patches;
2. variable affine cuts on a Minkowski null cone, demonstrating cut-gradient cancellation;
3. a rank-one fold `F(x,y)=(x^2,y)`, whose absolute sheet area is twice its union area while its
   signed sheet integral cancels;
4. a rank-zero two-sheet map `F(x,y)=(x^2-y^2,2xy)`, whose absolute sheet area is twice its union
   area without a signed cancellation;
5. isolated self-intersections of zero target two-area, showing that strict injectivity is not the
   correct equality criterion;
6. two separately labelled identical sheets, reported per label and as an explicitly declared
   mathematical disjoint-union census;
7. finite and near-null source-observer changes with pointwise density cancellation.

Production must execute at least 25,000 dependency-free checks across coordinate changes,
quadrature meshes, maps, ranks, multiplicities, cut functions, orientations, and observers. An
implementation-distinct verifier may not import production code or read its result; it must use a
different quadrature/multiplicity construction and execute at least 8,000 checks.

Raw double-precision normalized tolerance is `5e-10` for exact algebraic identities, `3e-6` for
finite-difference cut metrics, and mesh-convergence errors must decrease by at least a factor of
three on each declared refinement where the exact integral is not algebraic. These are numerical
method tolerances, not physical filters.

Hostile mutations must catch at least: adding a transverse cut-gradient term; using signed instead
of absolute Jacobian for sheet area; identifying sheet and union area on a fold; demanding strict
injectivity for equality; deleting rank-one or rank-zero points; calling every rank-one point a
fold; treating a caustic as a singular spacetime; omitting multiplicity; counting only one sheet;
turning isolated crossings into positive-area overlap; making signed area universally positive;
using the wrong observer power; inserting a target-observer area factor; selecting or weighting
path labels; retaining an auxiliary Riemannian metric physically; or promoting the result to light,
brightness, flux, luminosity, probability, distance, population, history, scale, `X_max`, or canon.

Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package evidence
bytes. Any change to alternatives, formulas, witness classes, tolerances, or maximum conclusion
after first outcome execution is a preregistered failure and must be recorded before rerun.

## Maximum conclusion

This is one exact finite geometric-map tile. Conditional on alternative A, it upgrades G348 from a
pointwise area density to multiplicity-aware integration over a supplied compact ray patch. It does
not choose the metric, source, patch, cut, rays, labels, observers, or physical population and does
not supply radiative physics.

No light or transfer law, brightness, flux, luminosity, probability, detector response,
observational distance, preferred route/observer/path population, history, occupancy, stability,
matter/mass, physical scale, `X_max`, or canon may be selected.
