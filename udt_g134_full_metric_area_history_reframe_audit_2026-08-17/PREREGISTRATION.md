# G134 preregistration — full-metric area rule and physical-history reframe

Date: 2026-08-17

Status: `PREREGISTERED_BEFORE_OUTCOME_EVALUATION`

## Whole question

Does the full-metric bivector area bilinear

```text
A_g(u wedge v,w wedge z)=g(u,w)g(v,z)-g(u,z)g(v,w)
```

add a nonidentity UDT restriction on the physical metric history, or does it faithfully evaluate and
reconstruct whichever regular Lorentz metric and observer planes are supplied?

The audit separates two logically different arenas:

1. **metric-first:** `g` is supplied and `A_g` is calculated from it;
2. **relation-first:** plane self-areas and cross-areas are supplied and must be tested for descent
   from one `g`.

## Exact bounded regime

- real four-dimensional tangent spaces and smooth regular Lorentz metrics;
- pointwise algebra and ordinary smooth tensor descent on supplied overlaps;
- complete symmetric bilinear data on `Lambda^2 T`, not only diagonal plane areas;
- supplied time/ruler sign convention when the global `g <-> -g` algebraic ambiguity matters;
- no singular, null-plane, cut-locus, boundary, topology-changing, or global-completion claim.

## Question type

`METRIC_LED`. The audit asks what the already derived full-`g` area object contains. It does not
target a desired cosmology, path, action, source, bootstrap closure, observational pattern, or
`X_max` realization.

## Preregistered tests

1. **Faithfulness theorem.** Prove or refute that equality `A_g=A_h` for two nondegenerate symmetric
   bilinear forms in dimension at least three implies `h=+g` or `h=-g`; classify the sign after the
   Lorentz signature convention is fixed.
2. **Local information rank.** Compute exactly the Jacobian rank of the map from the ten independent
   components of a four-metric to the twenty-one independent components of its symmetric six-by-six
   bivector area matrix. Register the local codimension of metric-induced area data.
3. **Scale test.** Verify the conformal weight and determine whether numerical `A_g` retains the
   common scale discarded by terminal reciprocal scalars.
4. **Reciprocity test.** Determine exactly what the determinant-one reciprocal action preserves in
   the area channel, and whether that preservation distinguishes the reciprocal subgroup from all
   area-preserving two-channel maps.
5. **Co-presence/overlap test.** Separate tensor descent and rank-complete reconstruction from a law
   assigning numerical values or selecting a smooth metric history.
6. **Countermodel gate.** Exhibit two inequivalent smooth Lorentz metric histories that both own
   lawful metric-induced area bilinears and satisfy the current structural Reciprocity/co-presence
   semantics. If they survive, the area rule alone is not a history selector.

## Preregistered landings

- `NONIDENTITY_UDT_AREA_HISTORY_CONSTRAINT_DERIVED`: only if an active founding premise supplies an
  additional area condition that excludes at least one otherwise regular Lorentz metric, without
  importing a desired answer.
- `AREA_BILINEAR_METRIC_FAITHFUL__RELATION_NETWORK_ADMISSIBILITY_REFRAMED__HISTORY_SELECTION_OPEN`:
  if complete area data are equivalent to full metric data and constrain arbitrary relation
  networks, while every supplied Lorentz metric automatically passes.
- `AREA_RULE_EVALUATOR_ONLY`: if it neither adds relation-network admissibility beyond existing
  full-pullback compatibility nor sharpens reconstruction.
- `TYPE_OR_ALGEBRA_FAILURE`: if the proposed full-metric object is not well typed or the G133 formula
  fails exact checks.

## Certification and falsification contract

- exact symbolic implementation with no floating tolerance;
- independent standard-library rational implementation for finite-dimensional ranks and witnesses;
- analytic proof for the global pointwise faithfulness statement;
- explicit counterexample against history selection;
- premise audit against the exact current registry;
- fresh read-only adversarial review before a banked high-confidence verdict.

The first local result will remain `LEAD` or `VERIFIED_WITH_CAVEATS` until the external gate passes.

## Maximum conclusion

At most this audit may classify the mathematical information content and ownership boundary of
`A_g` on the stated regular arena. It may not derive a physical history, evolution equation,
observer population, source, action, bootstrap law, observation, or `X_max` value.
