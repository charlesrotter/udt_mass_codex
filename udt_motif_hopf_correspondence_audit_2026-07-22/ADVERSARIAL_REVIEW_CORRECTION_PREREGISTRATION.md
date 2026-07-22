# Adversarial-review correction preregistration

Date: 2026-07-22

Parent evidence state: `72ede1ab88b692c14b709b2e00626d41eb90c67e` plus the unbanked production
outputs reviewed in `FRESH_ADVERSARIAL_REVIEW_RAW.md`.

The fresh review returned `FAIL` for the draft package grade. The numerical census is retained as
candidate evidence, but `COMPLETE_VERIFIED_WITH_CAVEATS`, all four affirmative evidence gates, and
the phrase “coherent projector bundles” are withdrawn before banking. This correction may restore
only claims supported by the tests below; it may not erase or rewrite the failed review.

## Registered defects

1. The registered nonlinear-coordinate projector covariance gate was not exercised in this package.
2. Frobenius obstruction values use component Euclidean norms and therefore certify only the
   registered chart unless a separate transformation test is added.
3. The packaged toric check repeated production formulas instead of deriving them from the metric,
   and it did not execute or directly compare the checked-in `hopf_seed` implementation.
4. Several catch proofs tested assertions rather than corrupted inputs passed through validators.
5. `construction_used_carrier_or_action=false` conflated the absent matter carrier/action functional
   with the separately supplied diagonal circle action.
6. Seventeen-node motif agreement is sampled continuation, not a continuous projector-bundle
   theorem. No continuity threshold was preregistered.
7. The production builder's direct amplitude-family and invariant-subspace sources were only
   transitively pinned and must also be named explicitly in this package's lineage table.

## Correction tests

The correction implementation must:

1. independently transform metric/phi two-jets at the 64 frozen blind identities under both stored
   nonlinear coordinate transformations;
2. compare every all-family projector set at every registered path node with the tensor-predicted
   transformed set, retaining numerical uncertainty rather than forcing agreement;
3. report the maximum projector covariance residual and classification discordance count;
4. keep all Frobenius counts explicitly `REGISTERED_CHART_ONLY`; any transformed obstruction probe
   is diagnostic and cannot promote the full census to chart-independent certification;
5. derive Christoffels, the mixed phi Hessian, the gradient dyad, angular gap, and diagonal-generator
   metric-dual connection from the symbolic toric metric rather than from saved eigentuples;
6. directly execute the frozen `hopf_seed` function on a deterministic CPU tensor sample and compare
   it with the metric quotient after inverse stereographic reconstruction;
7. replace ambiguous construction provenance with separate fields for supplied circle action,
   imported `S2` matter carrier, and imported `L2+L4` action functional;
8. exercise mutation tests by passing corrupted in-memory records through the same validators used
   for the unmodified records; direct unconditional throws and tautological length comparisons do not
   count as catches;
9. use sampled-path language everywhere. Large adjacent component distances remain disclosed and no
   smooth bundle, global continuation, or holonomy claim is allowed;
10. add the direct amplitude-family and invariant-subspace manifests to `SOURCE_LINEAGE.tsv` and
    verify their manifest contents.

## Fixed thresholds and coverage

- Covariance anchors: the same 64 SHA-256-selected identities used by the frozen independent replay.
- Transforms: both stored nonlinear transformations from the frozen independent motif verifier.
- Families/nodes: all 31 families at all 17 nodes for each anchor and transform.
- Projector covariance gate: maximum relative set distance `<=1e-8` on numerically classified,
  classification-agreeing cases; every uncertain/discordant case retained and counted.
- Direct seed comparison: deterministic 1,000-point float64 CPU sample, maximum absolute residual
  `<=1e-12`.
- Symbolic equalities must simplify exactly to zero.

## Maximum corrected conclusion

At most the conjunction:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

and

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

Even if every correction test passes, the overall motif-to-Hopf correspondence remains a `LEAD`.
Global continuation, toric-stratum selection, circle action, orientation, caps, deformable carrier
space, action, relaxed field, dynamics, stability, source, mass, and matter emergence remain open.

