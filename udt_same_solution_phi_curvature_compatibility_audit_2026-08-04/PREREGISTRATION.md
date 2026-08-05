# Preregistration — same-solution founded-phi/curvature compatibility audit

Date: 2026-08-04

Base: `a353af410e84abc1982401d9367e0845a1b1458d`

## Whole question

Does the current UDT foundation define a local same-solution join between founded reciprocal depth
and complete-coframe curvature, and—where a registered local realization is supplied—does enforcing
that common origin reduce the algebraic curvature possibilities?

This is a metric-led, CPU-exact local jet audit. It does not ask for a desired branch, action,
source, carrier, boundary, density, particle, observation fit, or physical time evolution.

## Ownership architectures that must remain separate

1. **Abstract founded pair:** `D(phi)=diag(exp(-phi),exp(+phi))` with additive composition. This is
   `DERIVED`, but it does not itself assign `phi(x)` to a spacetime coframe.
2. **Supplied factorized realization:**
   `theta=E(phi,D,S) bar_theta`, with the registered positive-triangular screen block and general
   mixing block. This is a `DEFINED_CONFIGURATION_ARCHITECTURE`, not a selected physical section.
3. **Reference coframe ownership:** `bar_theta` is a presentation input. Its value and jets may be
   frozen for a conditional chart calculation or released to test factorization redundancy. Neither
   treatment may be silently promoted into a preferred frame.
4. **Independent scalar atlas:** a separately varied scalar is
   `CHOSE_COMPARISON_CONFIGURATION`, not an additional native field.
5. **Observer/query depth:** a supplied pair/path comparison is relational query data. It is not an
   ordinary spacetime scalar unless an assignment/descent rule is separately derived.

## Bounded local regime

- Dimension/signature: regular four-dimensional Lorentzian metric, `eta=diag(-1,+1,+1,+1)`.
- Point representative: finite `phi`, invertible coframe; evaluate exact jets at the factorized
  identity when a chart witness is needed.
- Founded generator: `H=diag(-1,+1,0,0)`.
- Depth first jet: all four covector components, with zero, timelike, spacelike and nonzero-null
  representatives retained.
- Depth Hessian: all ten symmetric slots, free where the supplied realization treats `phi(x)` as a
  local potential.
- Extension jets: every allowed first- and second-jet slot of each registered screen/mixing family.
- Curvature: full algebraic Riemann tensor with the already-registered convention.
- Rank loss, infinite `phi`, global overlap, path cut loci, boundaries, and third jets are classified
  as outside this local regular tile.

## Registered realization families

The audit must individually retain:

1. full independent factorized family: founded `H` + three screen + four mixing generators;
2. determinant-one screen family: founded `H` + two screen-shear + four mixing generators;
3. screen-invariant/mixing family: founded `H` + four mixing generators;
4. no-mixing/angular family: founded `H` + three screen generators;
5. direct-sum spectator family: founded `H` only;
6. locked one-parameter angular counterfamily;
7. locked one-parameter shift counterfamily;
8. released complete coframe/reference family;
9. independent-scalar comparison control.

No family may be omitted because it gives an inconvenient rank.

## Preregistered operations

1. Derive the exact factorization redundancy under a local reference-pair redefinition and determine
   whether `phi`, `dphi`, or its Hessian can be recovered from the complete coframe alone.
2. Derive the first- and second-jet product rules for
   `theta=E(phi,D,S) bar_theta`, including all cross terms.
3. With the reference coframe frozen, compute the exact curvature image rank of every registered
   extension family using all allowed symmetric Hessian slots.
4. For each supplied first jet, determine whether the curvature map is affine with a first-jet
   offset and whether its Hessian image rank depends on the causal type or amplitude of `dphi`.
5. Test same-solution local realizability: for each causal stratum and every attainable algebraic
   curvature, determine whether one local two-jet in the same supplied factorized family exists.
6. Release reference-coframe jets and compute whether arbitrary `dphi` can coexist with the same
   complete coframe jet through factorization redundancy.
7. Separate existence in a supplied chart from a metric-native, frame-independent assignment or
   selector.
8. Compare the resulting local join with the prior first- and second-jet atlases without claiming
   their previously separate axes were already physically identified.

## Preregistered hypotheses and falsifiers

- `H1`: founded pair algebra alone does not make `phi` an invariant function of a complete coframe.
  Refuted if an exact coframe-only extraction survives every allowed reference-pair redefinition.
- `H2`: a released reference coframe gives a nontrivial factorization kernel that can shift local
  `phi` jet data without changing the complete coframe jet. Refuted if the exact product-jet map is
  injective in the founded direction.
- `H3`: no curvature rank is assumed for any restricted family. Each rank must be calculated before
  a same-solution conclusion is made.
- `H4`: fixed first jets contribute an affine curvature offset while the second-Hessian image is
  controlled by the allowed metric tangent generators. Refuted if the exact curvature coefficient
  rank changes with a supplied first jet on the regular tile.
- `H5`: a conditional same-solution existence theorem, if found, does not derive the physical
  extension/observer assignment. Refuted only by a current source-backed invariant assignment rule,
  not by choosing a convenient chart.
- `H6`: local two-jet compatibility is not physical evolution or bootstrap closure. Refuted only by
  an independently typed current return/evolution operator.

## Required independence and catch-proofs

The primary implementation may use SymPy. A separate standard-library rational implementation must
rebuild the factorization kernel, family curvature ranks, causal-stratum rank invariance, and every
same-solution existence classification without importing production code.

Fail-closed mutations must catch at least: deletion of a realization family; promotion of a supplied
chart to a selected physical section; loss of the reference-factorization kernel; promotion of an
independent scalar to native; a frozen Hessian slot; a changed family curvature rank; omission of a
causal stratum; false first-jet rank dependence; same-solution existence promoted to unique
selection; physical-time/bootstrap promotion; source-hash drift; and a missing premise or operation.

## Certification contract

A load-bearing positive needs exact rank plus a constructive local jet witness or exact surjectivity
argument. A negative is scoped to its registered family and allowed jets. The audit must state
whether its domain is a supplied realization, a comparison control, or a metric-native quotient.

## Maximum conclusion

The audit may classify whether founded depth and algebraic curvature can be jointly realized in each
registered local coframe architecture and whether the complete coframe alone identifies the depth
jets. It may derive a conditional local compatibility or a precise ownership obstruction.

It may not derive or adopt a unique physical extension, preferred frame, global depth field,
response/evolution law, action, source, carrier, boundary, density feedback, bootstrap fixed point,
`X_max`, matter, mass, species, observation fit, or canon statement.

## Stop line

After exact verification and fresh adversarial review, stop and decide whether a surviving
same-solution local family justifies differential/global compatibility work. Do not launch a long
solve, GPU work, density scan, action search, or time-live system automatically.
