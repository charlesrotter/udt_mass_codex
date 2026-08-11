# Preregistration — complete-pair instrument mixing solution-space atlas

Base commit: `8215a31578e571e29750daa53ccf26e436f7e582`

Date: 2026-08-10

## Whole question

For every regular ordered observer-pair tangent map supplied to the complete UDT metric, what
algebraic volume data describe how the reciprocal and angular sectors participate together, which
of those data are invariant, and where do the regular, crossover, null, and degenerate strata lie?

This is a metric-led solution-space map. It does not search for a desired micro, terrestrial, or
cosmological answer. It does not choose a pair family, physical path, source, action, boundary,
background density, or regime assignment.

## Bounded arena

Let `V_i^a` (`i=0,1`, `a=0,1,2,3`) be the complete time-live pair Jacobian in a local orthonormal
coframe with signature `(-,+,+,+)`. No time, angular, shift, or mixing component is frozen. The
induced pair metric is

`h_ij = eta_ab V_i^a V_j^b`.

The first atlas is pointwise and algebraic on the regular Lorentzian stratum. It studies the simple
bivector `B=V_0 wedge V_1` and its components relative to a supplied reciprocal/angular `2+2`
split. Global transport, equations of motion, and on-shell completion are outside this bounded
return.

## Ownership stamps

- `pinned-by-THEORY`: Lorentzian complete metric; ordered observer-pair query; complete pair
  pullback; the calibrated `c_E` normalization of the ordinary reciprocal reading.
- `free-and-explored`: every component of `V_0,V_1`; reciprocal, angular, and mixed bivector
  components; orientations; all regular and degenerate algebraic strata.
- `CONDITIONAL`: interpreting component sectors separately requires a metric-owned or explicitly
  supplied reciprocal/angular projector. R17 supplies such a split only on its stated conditional
  stationary branch.
- `OPEN`: physical pair-family owner, global path, dynamics, source, action, background density,
  positive observational weighting, and physical regime labels.
- `inactive`: strong local CSN. Common scale is retained.
- `pinned-by-HABIT`: none.

## Preregistered candidate landings

1. `INTRINSIC_PAIR_METRIC_ONLY`: all complete mixing information collapses without residue into
   `(kappa,phi,beta)`.
2. `SPLIT_RELATIVE_SIGNED_ORCHESTRA_ATLAS`: the metric supplies exact signed sector-volume
   invariants relative to an owned `2+2` split, but not positive physical weights.
3. `UNIQUE_POSITIVE_MIXING_LAW`: the metric uniquely supplies nonnegative instrument weights and
   their regime interpolation.
4. `TYPE_FAILURE`: no invariant sector-volume atlas survives even after the split is correctly
   typed.

The maximum allowed positive conclusion is candidate 2 unless a unique positive measure is proved
without an observer norm, absolute-value convention, dynamics, fitting, or physical regime labels.

## Preregistered falsification and certification contract

The load-bearing algebra must independently verify:

1. the Gram/Pluecker determinant identity and the four-dimensional simplicity relation;
2. covariance of the proposed sector scalars under the split-preserving group
   `SO^+(1,1) x SO(2)`;
3. the exact relation between their signed sum and `det(h)`;
4. constructive coverage, or an explicit incomplete classification, of the regular Lorentzian
   invariant region;
5. invariance or declared transformation of each scalar under common scale and orientation reversal;
6. failure of any claimed positive weight to be canonical if a counterexample or convention choice
   exists;
7. separation of pair-metric state `(kappa,phi,beta)` from split-relative plane-orientation data;
8. `c_E` remains a calibration anchor and is not used to manufacture sector weights;
9. exact boundary behavior at `det(h)=0`, pair rank loss, and projector loss;
10. no micro/cosmic/force/matter interpretation is inferred from dominance regions.

## Premise-change rule

If the reciprocal/angular split is not owned on a branch, every split-sector conclusion is regraded
to `CONDITIONAL CHARACTERIZATION`. If a later on-shell/global rule selects a split or positive
measure, this atlas may be regraded but must not be silently rewritten.
