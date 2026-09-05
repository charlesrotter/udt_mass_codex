# G348 preregistration — generic Lorentzian null-screen area theorem

Date: 2026-09-04
Outcome status: analytic, computational, and independent-replay outcomes unseen

## Frozen question and domain

Let `(M,g)` be any supplied smooth time-oriented four-dimensional Lorentzian manifold. Let
`gamma:[lambda_0,lambda_1]->M` be any supplied regular affinely parameterized future null geodesic
with nonzero tangent `k`. No field equation, symmetry, topology, coordinate chart, global
hyperbolicity, or special solution is assumed. Conjugate endpoints are included.

At each endpoint allow every finite future unit timelike observer. Cover arbitrary positive common
affine rescaling, arbitrary endpoint `GL(2)` screen coordinates, both endpoint orders, all ranks of
the Jacobi position block, ordinary coincidence, and finite-order conjugate crossings. Path labels
remain supplied and separate.

## Preregistered primary alternatives

1. `A__GENERIC_METRIC_NULL_SCREEN_AREA_THEOREM_CLOSES_WITH_SINGULAR_STRATA`: the metric quotient
   supplies the connection, self-adjoint tide, symplectic phase flow, reversal, directional areas,
   and arbitrary-observer covariance; conjugate points change only the endpoint chart/rank stratum.
2. `B__LOCAL_QUOTIENT_AND_OBSERVER_LAWS_CLOSE_BUT_BILOCAL_RECIPROCITY_FAILS`: the pointwise screen
   structure is general but at least one phase, reversal, or directional-area law needs the prior
   exact spacetime.
3. `C__METRIC_ALONE_DOES_NOT_SUPPLY_THE_REQUIRED_SCREEN_CARRY`: an extra transport or screen
   structure is required even on a supplied affine null geodesic.
4. `D__NO_COMPLETE_RANK_AND_ORIENTATION_CLASSIFICATION_CLOSES`: regular or conjugate cases remain
   untyped or contradictory.

## Preregistered secondary alternatives

- quotient carry: `Q1__LEVI_CIVITA_QUOTIENT_CONNECTION_IS_CANONICAL` or `Q2__EXTRA_CARRY_REQUIRED`;
- phase flow: `J1__SELF_ADJOINT_TIDE_GIVES_SYMPLECTIC_FLOW` or `J2__FAILS_OR_REQUIRES_EXTRA_LAW`;
- reversal: `R1__B_REVERSE_EQUALS_MINUS_METRIC_ADJOINT` or `R2__OTHER_OR_FALSE`;
- area: `A1__SOURCE_FREQUENCY_SQUARED_TIMES_ABSOLUTE_JACOBI_DETERMINANT` or `A2__OTHER`;
- observers: `O1__G347_SOURCE_FACTOR_COVARIANCE_IS_POINTWISE_GENERIC` or `O2__SPACETIME_SPECIFIC`;
- singular strata: `C1__FULL_PHASE_FLOW_REGULAR_WHILE_AREA_RANK_DROPS` or
  `C2__CONJUGATE_POINT_INVALIDATES_FULL_TRANSPORT`;
- crossing order: `X1__WRONSKIAN_FORCES_ZERO_ORDER_EQUAL_TO_KERNEL_DIMENSION` or
  `X2__HIGHER_ORDER_DEGENERATE_METRIC_JACOBI_CROSSING_EXISTS`;
- orientation: `S1__ABSOLUTE_AREA_IS_INTRINSIC_AND_ORIENTED_SIGN_NEEDS_ORIENTATION_DATA` or
  `S2__UNIVERSAL_POSITIVE_ORIENTED_DETERMINANT`;
- sewing: `W1__TYPE_I_STATIONARY_SEWING_IS_CHARTWISE_ONLY` or `W2__GLOBAL_BARE_SEWING`;
- physical typing: `P1__INFINITESIMAL_METRIC_GEOMETRY_ONLY` or
  `P2__LIGHT_TRANSFER_DISTANCE_OR_POPULATION_LAW_DERIVED`.

`S2`, `W2`, and `P2` require derivation. They may not be inferred by continuity from G343--G347.

## Frozen definitions and sign convention

Use signature `(-,+,+,+)` and curvature convention

```text
R(X,Y)Z = nabla_X nabla_Y Z - nabla_Y nabla_X Z - nabla_[X,Y] Z.
```

On `Q=k^perp/span(k)`, freeze and test

```text
D_k[X] = [nabla_k X],
T[X] = [R(X,k)k],
D_k^2 x + T x = 0.
```

Use quotient metric `q`. On phase space `Q plus Q`, freeze

```text
Omega((x,p),(y,r)) = q(x,r)-q(p,y).
```

For `M_10=[[A,B],[C,D]]`, freeze and test

```text
M_20=M_21 M_10,
M_01=M_10^-1,
B_01=-B_10^*,
|det B_01|=|det B_10|.
```

For endpoint observers `u_i`, frequencies `omega_i=-g(k,u_i)`, and quotient metric determinants
written in arbitrary screen coordinates, freeze

```text
mathscr_A_(1<-0)=omega_0^2 |det B_10| sqrt(det q_1 det q_0),
mathscr_A_(0<-1)=omega_1^2 |det B_01| sqrt(det q_0 det q_1).
```

Here component `det B` is paired with the metric area coefficients exactly as in G346. In
orthonormal quotient frames the square-root factor is one.

For endpoint observer replacements define `D_i=omega_(v_i)/omega_(u_i)>0` and freeze

```text
mathscr_A'_(1<-0)=D_0^2 mathscr_A_(1<-0),
mathscr_A'_(0<-1)=D_1^2 mathscr_A_(0<-1).
```

## Frozen rank/orientation classification

1. `rank B=2`: both directional areas are positive, `B^-1` exists, and G344/G345 type-I formulas
   are finite on the noncoincident chart.
2. `rank B=1`: both positive directional areas vanish; the full `M` remains invertible and
   symplectic; the type-I generator and inverse determinant scalar are singular.
3. `rank B=0`: the same singular-chart conclusion holds with a two-direction rank loss. Coincidence
   is one rank-zero example but need not be the only one.
4. On any interval where `det B` is nonzero, its oriented sign is constant. Freeze as a candidate,
   not an assumption, that the Wronskian maps `ker B` injectively onto the metric-orthogonal
   complement of `im B`; if proved, the determinant-zero order equals `dim ker B`. In two screen
   dimensions rank one then gives a simple sign-changing zero, while rank zero gives a double zero
   with no sign change. Alternative `X2` wins if any genuine metric Jacobi counterexample exists.
5. An oriented determinant is intrinsic only after compatible endpoint orientations are supplied.
   Under reversal in those transported orientations, two screen dimensions make
   `det(-B^*)=det B`. Under arbitrary independent orientation changes, only `|det B|` is invariant.
6. Stationary determinant sewing is asserted only when every inverted `B` and join Hessian exists.
   The full symplectic composition law remains the cross-stratum statement.

## Required derivation and evidence

1. Rederive the quotient connection, positivity, metric compatibility, curvature endomorphism, and
   its self-adjointness from `g`; no optics theorem or field equation may serve as proof.
2. Derive symplecticity by differentiating the quotient Wronskian, then derive composition,
   reversal, and the `B` adjoint law.
3. Derive affine, arbitrary `GL(2)`, orientation, observer-screen, sky-area, and directional-area
   transformations without assuming a preferred orthonormal frame.
4. Exhibit rank-two, simple rank-one, transverse rank-zero, coincidence, and nonconjugate
   negative-tide witnesses. Prove `X1` or exhibit a genuine higher-order/degenerate `X2` witness.
   A branch is characterized, never rejected for zero area or a singular type-I chart.
5. Production must execute at least 20,000 standard-library-only checks across noncommuting
   symmetric two-screen tidal profiles, exact constant-tide witnesses, endpoint orders, affine
   scales, endpoint coordinates, observer changes, and all rank strata.
6. An implementation-distinct verifier may not import production or G343--G347 code. It must use a
   different integrator/parameterization and execute at least 7,500 checks, including direct smooth
   variable-tide phase integration and independent conjugate-crossing classification.
7. Raw double-precision normalized tolerance is `2e-9` for exact algebraic/constant-tide checks,
   `2e-7` for variable-tide independent integration, and `2e-6` near multiple/degenerate zeros.
8. Hostile mutations must catch at least: wrong Jacobi curvature sign; nonsymmetric tide;
   nonsymplectic flow; wrong reversal transpose/sign; forced `det B>0`; deletion of rank-one or
   rank-zero cases; treating singular `B` as singular `M`; finite inverse determinant at a caustic;
   false global stationary sewing; missing absolute value; orientation-free signed determinant;
   wrong conjugate zero order or an unproved degenerate crossing;
   wrong affine power; target observer factor; numerical observer invariance; summed path labels;
   or promotion to light, distance, population, scale, `X_max`, or canon.
9. Every executable must run with `python3 -S`, support `UDT_NO_WRITE=1`, and preserve package
   evidence bytes during no-write replay.

Any change to the alternatives, formulas, rank classification, tolerances, or maximum conclusion
after first outcome execution is a preregistered failure and must be recorded before rerun.

## Completeness and maximum conclusion

This is one general differential-geometric theorem tile, not a spacetime solve. It covers every
supplied regular affine null geodesic in every smooth four-dimensional Lorentzian metric and every
endpoint rank stratum, conditional on the derivation succeeding. It does not choose which metric,
geodesic, observer, or path is physical and does not supply finite-beam propagation or radiative
physics.

The maximum landing is the generic coordinate-free infinitesimal quotient-screen/area theorem—or
its scoped refutation—with singular strata explicit. No light/transfer law, observational distance,
preferred observer/route/population, history, stability, matter/mass, scale, `X_max`, or canon may
be selected.
