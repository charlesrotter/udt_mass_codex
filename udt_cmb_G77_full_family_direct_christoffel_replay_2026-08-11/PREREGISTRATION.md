# G77 preregistration — full-family direct-Christoffel replay

Date: 2026-08-11

Base: `4ccb785c6d1f7ba39a7124236f58acaa742cdc42`

Status before computation: not run; no G77 trajectory, endpoint, face, or refinement output exists.

## Whole question

Does an equation-independent direct metric-geodesic implementation reproduce the complete finest-
mesh G76 whole-sky relation atlas for all `591/591` frozen G75 profiles, and do higher time
resolutions numerically resolve the four G76 rows that exceeded its frozen `512`/`1024` Hamiltonian
endpoint-chord gate?

This is an evidence-strengthening calculation on the already frozen G76 bounded universe. It is
metric-led and outcome-neutral. It will not select, rank, fit, repair, discard, or physically
interpret any profile.

## Direct equation route

The replay starts from the supplied Cartesian metric, not the G76 Hamiltonian or its right-hand
side. With `X=(X,Y,Z)`, `s=X.X`, `A=1+a s`, `q=q(s)`, and
`w=q(-Y,X,0)`, use

```text
g_00 = -A,
g_0i = g_i0 = w_i,
g_ij = delta_ij - a X_i X_j/A.
```

The metric and its first coordinate derivatives are coded directly. For tangent `u`, the
contracted Christoffel equation is evaluated as

```text
g_mn du^n/dlambda = -[partial_a g_mb - (1/2) partial_m g_ab] u^a u^b,
dx^m/dlambda = u^m.
```

Each right-hand-side call uses a batched numerical solve of this `4 x 4` system. The production
implementation must not import `solve_complete_family.py`, `hamiltonian_rhs`, or any stored G76
trajectory endpoint. Before any atlas interpretation, an exact/full-Christoffel implementation at
registered algebraic control states must agree with the contracted implementation to `2e-12` in
maximum absolute acceleration.

## Frozen candidate universe and observer query

- all `591` frozen G75 profiles, in their frozen atlas order;
- the exact `2,562` G76 level-4 initial directions and `5,120` oriented faces;
- observer position `(1/4,0,0)`;
- complete metric-orthonormal initial direction sphere;
- first outward crossing of `|X|=1`;
- affine cap `4`;
- stationary axial G75 metric with `q_s` live;
- CPU `float64`, one process, vectorized over directions within one profile;
- direct-Christoffel RK4 with `2,048` steps for every profile;
- additional direct-Christoffel `1,024`, `2,048`, and `4,096` step runs for exactly the four frozen
  G76-unresolved identities.

The observer/query values are `CHOSE` historical controls inherited unchanged from G74/G76. The
step counts and tolerances are `CHOSE_NUMERIC` soundness controls. Runtime is not an acceptance
criterion. Per-profile memory-mapped checkpoints and a completion bitmap permit exact restart
without reducing the family.

## Outputs

The run must preserve:

- direct endpoints and crossing masks for all `591 x 2,562` rays;
- maximum null backward error and nonfinite count per profile;
- maximum direct-versus-G76 endpoint chord and crossing-mask mismatch;
- signed spherical face area, degree, negative/near-zero face counts;
- an independently coded tangent-plane face-map orientation census;
- the four-row direct time-refinement ladder and convergence ratios;
- exact command, Python/NumPy/SciPy versions, elapsed time, raw stdout/stderr, and SHA-256 manifest.

Missing, nonfinite, negative, near-zero, or disagreement rows remain in the census and are
classified. They are never filtered.

## Frozen numerical classifications

Cross-method endpoint agreement is classified uniformly, independent of the G76 status:

- `STRONG_DIRECT_AGREEMENT`: zero crossing mismatch and maximum chord `<=2e-5`;
- `REGISTERED_DIRECT_AGREEMENT`: zero crossing mismatch and maximum chord in `(2e-5,5e-5]`;
- `CROSS_METHOD_NUMERICALLY_UNRESOLVED`: any crossing mismatch or maximum chord `>5e-5`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`: source/type/equation/control failure.

The maximum null backward error gate is `<=2e-7`. Degree agreement uses
`|degree_direct-degree_G76|<=5e-4`. Absolute signed face area below `1e-2`, `1e-3`, or `1e-4` is a
diagnostic, not a rejection filter.

For each of the four frozen G76-unresolved rows, direct `2,048`/`4,096` maximum endpoint chord
`<=5e-5`, zero crossing mismatch, and null error `<=2e-7` permits the new G77 descriptor
`DIRECT_TIME_REFINEMENT_RESOLVED`. This does not rewrite the historical G76 classification.
Otherwise the row remains `DIRECT_TIME_REFINEMENT_UNRESOLVED`. The `1,024`/`2,048` chord and both
refinement ratios are always reported; monotonicity is descriptive, not a filter.

## Falsification and verification

The run fails closed on a changed source hash, missing/duplicate profile, changed direction/face
array, import of the Hamiltonian RHS, incomplete checkpoint, silently promoted unresolved row,
endpoint mutation, wrong comparison threshold, or physical-selection language.

Before a verdict is banked, a fresh verifier must:

1. independently reconstruct the metric derivative and full Christoffel symbols;
2. replay registered rays from all eight exact G75 strata and every one of the four G76-unresolved
   profiles with a separately coded solver;
3. independently recompute the complete saved endpoint/face census from raw arrays;
4. exercise every hostile catch-proof; and
5. audit the premise and completeness ledgers.

## Allowed landings

- `FULL_FAMILY_DIRECT_REPLAY_AGREES`;
- `FULL_FAMILY_DIRECT_REPLAY_MIXED_NUMERICAL_CLASSES`;
- `FOUR_ROWS_DIRECTLY_REFINED__G76_HISTORY_UNCHANGED`;
- `DIRECT_REPLAY_NUMERICALLY_UNRESOLVED`;
- `TYPE_OR_IMPLEMENTATION_FAILURE`.

## Maximum allowed conclusion

At most, G77 can strengthen or numerically qualify the sampled G76 whole-sky relation family under
the same supplied stationary query. It cannot establish continuum injectivity, select a physical
profile/source/endpoint/scale, determine `R` or `X_max`, populate a CMB sky, derive polarization,
bootstrap, action, matter, or a CMB observable.
