# Audit report — R17 endpoint depth and path-labelled angular holonomy

Date: 2026-08-10

## Result

On the supplied regular stationary R17/W01 family, the complete metric does supply an exact joint
geometric object:

```text
(endpoint reciprocal depth, path-labelled normal rotation).
```

Globally it composes as the product of the reciprocal-line groupoid and the oriented
normal-isometry groupoid. After endpoint frames are chosen it has a local direct-product
`R x SO(2)` representation. In conformal screen form,

```text
C_w(gamma)=exp(w delta_K(gamma)) U_gamma
```

composes for every real `w`. The supplied complete R17 coframe fixes `w=-lambda` on the original
screen-vector coefficients and `w=+lambda` on the dual screen coframe. This is a conditional
complete-coframe screen map, not the missing four-dimensional physical observer arrow.

## Scalar and gauge ruling

For one unframed open path, independent endpoint screen rotations erase every scalar dependence on
the open-path rotation. Among all continuous real additive characters of the order-zero joint
group, pure reciprocal normalization uniquely leaves

```text
chi=delta_K.
```

The angular information remains real geometry, but in a different type:

- a closed loop retains its `SO(2)` holonomy angle or `O(2)` conjugacy/cosine while its endpoint
  depth is zero;
- two paths with common endpoints retain their relative holonomy together with their common depth;
- an unwrapped real angle requires an added lift or trivialization.

There is no nontrivial continuous semidirect action of reciprocal depth on `SO(2)`. The metric-owned
order-zero join is commuting/direct-product. C08 gives an exact independence witness:
`delta(loop)=0` while `F23=-4097/2048`.

## Higher-jet correction and scope

The preregistered possibility that local curvature-depth terms are merely diagnostics is refuted
at the composition level. One-forms such as `I(F,...) dphi` have additive path integrals. The
non-exact rectangle is a general differential-form control, not an R17 solution witness; whether
stationary R17 itself realizes a metric-natural non-exact scalar one-form independent of `dphi`
remains open. The current foundation selects no member of this broad construction class.

## Evidence gates

1. **Preregistered:** yes, commit `996da387` before derivation.
2. **Full or bounded:** full for the 12 preregistered candidate families in the declared order-zero
   joint class, with representative higher-jet one-form families; stationary regular R17 only.
3. **Independently verified:** exact SymPy controller 12/12; independent standard-library complex
   group/path reconstruction 16/16; 17/17 exercised semantic mutations rejected; fresh external
   review returned `VERIFIED_WITH_CORRECTIONS` and its corrections are incorporated.
4. **Premises audited:** yes. Path, branch, `lambda`, physical arrow, action, source, bootstrap,
   `c_eff`, and dynamics remain unselected.

## Maximum conclusion

```text
CONDITIONAL_STATIONARY_R17_DEPTH_NORMAL_ISOMETRY_GROUPOID_FUNCTOR_DERIVED__
LOCALLY_DIRECT_PRODUCT__
COMPLETE_COFRAME_FIXES_SCREEN_CO2_WEIGHT_BY_VARIANCE__
UNIQUE_NORMALIZED_CONTINUOUS_REAL_ORDER_ZERO_CHARACTER_IS_ENDPOINT_DEPTH__
ANGULAR_DATA_REMAINS_PATH_OR_LOOP_VALUED__GENERAL_HIGHER_JET_LINE_INTEGRALS_COMPOSE_BUT__
STATIONARY_R17_NONEXACT_REALIZATION_OPEN__
PHYSICAL_PATH_AND_ARROW_OPEN
```

This is not canon and not a physical branch or observer-law selection.
