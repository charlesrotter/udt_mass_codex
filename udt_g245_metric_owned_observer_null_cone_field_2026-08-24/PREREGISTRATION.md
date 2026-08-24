# G245 preregistration — metric-owned observer null-cone field

Date: 2026-08-24

## Question and scope

On the bounded regime in `MAP.md`, determine whether the metric plus one calibrated observer germ
owns the local direction-labelled null sheet and therefore the G244 area/shape field, without a
separately supplied ray family, source population, angular coefficient, or observational outcome.

## Preregistered theorem candidates

1. **Null-direction ownership.** The observer celestial sphere is the unit sphere in `U^perp`, and
   `k(n)=U+n` is the unique future null vector in direction `n` satisfying `-g(U,k)=1`.
2. **Local-sheet ownership.** `F(lambda,n)=Exp_o(lambda k(n))` is uniquely metric-derived on its
   maximal exponential domain. It is a regular local null sheet before rank loss; no preferred
   endpoint or path is selected because every direction-labelled geodesic is returned.
3. **Jacobi identification.** For `v in T_n S_o^2`, `J_v=dF(v)` satisfies
   `D_k^2 J_v+R(J_v,k)k=0`, `J_v(0)=0`, and `D_k J_v(0)=v`. Thus the angular differential of `F` is
   exactly the G188 vertex-normalized matrix `D`.
4. **Induced-field identity.** The angular pullback metric on a constant-affine cross-section is
   `H=D^dagger D`; its area ratio, normalized shape, shear, and orientation-line parity are exactly
   G244's outputs.
5. **Native evolution.** With `V=D'` and self-adjoint tide `T`, derive without linearization:
   `D'=V`, `V'=-T D`, Wronskian conservation, `H'=D^dagger V+V^dagger D`, and the corresponding
   regular optical area/shape equations. The full phase, not `H` or `D` alone, remains the evolution
   and composition object.
6. **Vertex asymptotics.** For differentiable tide, derive the exact leading series showing that
   trace tide first controls area and trace-free tide first controls shape. This is a local series
   classification, not a finite-distance approximation or physical loudness law.
7. **Degenerate/global classification.** At conjugate points `H` stays semidefinite and the full
   phase stays lawful while normalized shape leaves scope. Cut self-intersections remain
   direction-labelled. Geodesic incompleteness and global branch aggregation remain open.

## Exact checks

- symbolic two-by-two derivation of null normalization, Wronskian conservation, Gram evolution,
  determinant/shape identities, and the vertex series;
- exact isotropic-tide control: shape remains identity;
- exact anisotropic and rotating-tide controls: full matrix response survives and scalar-mode
  deletion fails;
- exact caustic control `D=diag(sin(lambda),lambda)`: `H` and full phase remain lawful while
  normalized shape fails at `lambda=pi`;
- passive endpoint `O(2)` covariance and orientation-line parity;
- independent standard-library rational reconstruction with no production-code imports or saved-
  output reads;
- hostile mutations for fitted coefficient insertion, preferred-ray selection, scalarized tide,
  position-block multiplication/inversion, parity scalarization, source-law promotion, and outcome
  access.

## Certification contract

- every symbolic residual must simplify exactly to zero;
- every exact rational equality must match identically;
- production and independent routes must agree on all registered finite invariants;
- every hostile mutation must be caught;
- the source manifest must match exactly;
- `BOSS/CMB outcomes == CLOSED_AND_UNREAD` and `fitted_angular_coefficients == 0` in every result.

## Failure conditions

The proposed landing fails if the local cone requires data beyond `(g,o,U,time orientation)`, if
the angular differential does not reproduce the G188 IVP, if a scalarized or post-readout angular
term is required, or if any global/source/detector ownership is silently promoted.

## Maximum conclusion

At most:

```text
OBSERVER_GERM_AND_METRIC_OWN_LOCAL_DIRECTION_LABELLED_NULL_CONE_FIELD
__G244_AREA_SHAPE_ARE_INDUCED_CONE_GEOMETRY
__SOURCE_POPULATION_GLOBAL_BRANCH_AND_PHYSICAL_HISTORY_REMAIN_OPEN
```

No observational feature, fit, cosmology, `X_max`, source law, signalling law, or global physical
history may be claimed.
