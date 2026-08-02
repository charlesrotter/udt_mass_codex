# Complete-metric global-data/local-fiber audit — preregistration

Date: 2026-08-01  
Base: `e9754af8f93f6f3cd37d2c46fa0247c3c0e7e46d`  
Mode: CPU-only exact algebra and source adjudication; metric-led; no solve

## Whole question

Do complete-metric global curvature, holonomy, or completion data already and naturally
parameterize a changing family of locally admissible coframes or metric germs,

```text
C or K  ->  F_C or F_K subset X_local,
```

without inventing an integral, action, scalar weighting, normalization, desired filter, carrier,
or field equation?

This is not a request to select a completion or physical universe.  It is an existence and typing
question: whether distinct independently stated global data impose distinct local compatibility
fibers by the metric's own descent, regularity, or integrability requirements.

## Bounded frame

- `X_local` consists of local coframe/profile/screen germs in a stated chart or overlap.
- `C` consists only of registered global completion data: topology/quotient class, transition or
  monodromy action, cap degeneration data, seam/glue data, and compatible holonomy data.
- `K` consists only of metric-derived curvature data.  A global curvature scalar, spectrum,
  average, or level is not admitted unless its domain and construction are already native and
  choice-free.
- A natural local fiber must arise from global well-definedness, chart descent, cap regularity,
  overlap matching, or an already required geometric property.  It may not be manufactured by
  declaring an invariant equal to a preferred number.
- Completion values may remain supplied or unselected.  Parameterizing fibers does not select the
  parameter.
- The parent projector neighborhood is tested only for compatibility with any derived fiber map;
  it is not used to force a positive answer.

## Frozen candidate classes

`CANDIDATE_GLOBAL_DATA_LEDGER.tsv` freezes twelve routes:

1. pointwise curvature tensors/scalars;
2. prescribed curvature level;
3. curvature spectrum/distribution;
4. curvature integral or normalized average;
5. path/loop holonomy;
6. discrete topology/completion label;
7. overlap transition/monodromy representation;
8. smooth cap degeneration data;
9. seam/glue matching data;
10. completion-scoped `R_geom`;
11. completion-conditioned projector neighborhood;
12. combined curvature/completion selector.

## Gates

A route earns `NATURAL_PARTIAL_LOCAL_FIBER` only if it passes all applicable gates:

1. the global datum and its action are registered metric/completion data;
2. `C` or `K` is independently variable before imposing same-configuration compatibility;
3. local admissibility follows from descent/regularity/integrability, not a chosen objective;
4. at least two admissible global values give provably different nonempty or dimensionally
   different local fibers;
5. the construction is chart/observer natural in its exact stated scope;
6. the same completed configuration can recompute or identify the datum;
7. no integral, action, weighting, normalization, carrier, source, or desired outcome enters;
8. the ruling does not call a supplied completion selected, on shell, stable, massive, or physical.

`FORWARD_READOUT_ONLY`, `SUPPLIED_LABEL_WITHOUT_LOCAL_ACTION`, `BLOCKED_CHOICE_REQUIRED`, and
`OPEN_INCOMPLETE_DESCENT_DATA` are valid outcomes.

## Exact algebra controls

If registered transition/monodromy data act linearly on a local component vector `v`, the audit may
test the choice-free descent condition

```text
v_after = M v_before,
v_after = v_before around a closed identification,
(M-I)v = 0.
```

The fixed subspace `ker(M-I)` is a local compatibility fiber.  This control counts only if the
source record actually registers the corresponding completion/transition interpretation.  It does
not make `v` a physical field or select `M`.

Curvature-to-holonomy controls may be used only to test an already required parallel/reduced
structure.  Parallelism may not be added merely to obtain a curvature constraint.

## Falsification and maximum conclusion

- If all candidate data are merely outputs or labels, return `NO_NATURAL_CHANGING_LOCAL_FAMILY`.
- If completion descent supplies changing fibers but no dynamics, return
  `COMPLETION_PARAMETERIZES_PARTIAL_KINEMATIC_FIBERS_ONLY`.
- If curvature supplies a choice-free family, state its exact object/domain and why no level,
  averaging, operator, or parallelism was chosen.
- Missing seam, transition, cap, or chart data remain open rather than being filled by habit.

At most the audit may derive a partial kinematic global-to-local fiber family.  It may not derive
the bootstrap law, select a completion, adopt a boundary, define matter, infer stability/mass,
promote the projector into a carrier, or launch GPU/numerical work.
