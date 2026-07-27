# Preregistration — intrinsic-pair deformation neighborhoods

Date: 2026-07-27

Base: `ec5a241927b51b047d8bdbb3742cdaa5e464c880`

Question type: **METRIC-LED, OBSERVING LOCAL CONFIGURATION-SPACE STRUCTURE**.

## Whole question

The preceding audit exhibited six complete twisted `R x S3` metric configurations in which three
curvature-invariant gradients identify a unique stationary clock line and the twist of that same
line identifies the reciprocal ruler line. Are those all-gate witnesses isolated algebraic
accidents, or does each lie inside an open neighborhood of configurations with the same certified
intrinsic-pair structure?

This audit tests structural availability in the registered configuration family. It does not ask
which configuration is physical, on shell, dynamically stable, selected by bootstrap, or preferred
by observation.

## Premise stamps carried forward

Every result must retain exactly these distinctions:

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

Co-presence supplies no equation, action, operational signalling theorem, or solution selector. The
openness argument must remain mathematical if that interpretation is later abandoned.

## Frozen family and topology

Use the complete global coframe already audited on `R x S3`:

```text
tau     = dt + a sigma_3
theta_0 = exp(-phi) tau
theta_1 = exp(+phi) sigma_3
theta_2 = exp(lambda phi) sigma_1
theta_3 = exp(lambda phi) sigma_2
g       = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2.
```

The local configuration space is the product of smooth depth profiles, real `a` and `lambda`, and
positive coframe scale. Because first derivatives of curvature invariants use at most the metric
three-jet, the required profile topology is `C3(S3)`. No field equation or action is imposed.

The six exact base configurations C01–C06, their profile, and their invariant-gradient
determinants are frozen by the parent audit. No base value may be retuned after this preregistration.
The deformation axes are exhaustive only for this fixed topology/coframe family and are frozen in
`DEFORMATION_AXIS_UNIVERSE.tsv`.

## All-gate set

At the fixed north event `p`, define

```text
D_p = det[dI1, dI2, dI3],
I1  = scalar curvature,
I2  = Ricci_ab Ricci^ab,
I3  = Riemann_abcd Riemann^abcd.
```

The tested all-gate set requires simultaneously:

1. `D_p != 0`, certifying the unique continuous Killing line by the parent proof;
2. `a kappa != 0`, giving nonzero clock twist and the reciprocal ruler direction;
3. `osc(phi) > 0`, giving nontrivial reciprocal clock depth;
4. `min_S3(exp(4 phi)-a^2) > 0`, giving the displayed stationary slices positive metric;
5. a smooth, finite, nondegenerate global coframe with positive scale.

The production proof must identify the function-space topology in which each predicate is open and
must give exact positive base margins where the frozen evidence permits it. A bare sampled cloud is
not a proof of openness.

## Degeneration taxonomy

All registered strata in `DEGENERATION_STRATUM_UNIVERSE.tsv` must be reported. In particular,
`D_p=0` means only that this particular three-invariant certificate loses rank at this event. It
does **not** prove that the metric gains symmetry or loses every possible intrinsic clock
certificate. Conversely, `a kappa=0` really removes this twist-selected ruler route.

## Computation and verification contract

- CPU only; no GPU or long solve.
- Reuse frozen exact determinant evidence; do not recompute it with altered candidates.
- Prove continuity of the all-gate maps in the declared topology.
- Certify the frozen depth, twist, and slice margins with exact rational bounds.
- Report whether an explicit neighborhood radius is or is not certified.
- Independently reparse the determinant evidence and rederive the rational bounds without importing
  the production module.
- Exercise all preregistered catch-proofs.
- Do not modify startup controls, scientific artifacts, frozen evidence, registries, or `CANON.md`.

## Falsification and maximum conclusion

If every C01–C06 base determinant is exactly nonzero, the other gates have strict positive margins,
and each gate is continuous in the declared topology, the maximum conclusion is:

```text
ALL_GATE_INTRINSIC_PAIR_CONFIGURATIONS_CONTAIN_OPEN_C3_NEIGHBORHOODS_AROUND_C01_TO_C06_IN_THE_FIXED_COMPLETE_S3_FAMILY;
STRUCTURAL_AVAILABILITY_IS_NOT_FINE_TUNED_WITHIN_THIS_CONFIGURATION_TOPOLOGY;
NO_EXPLICIT_RADIUS_OR_PHYSICAL_SELECTION_IS_DERIVED.
```

Here “not fine tuned” means only “not an isolated point of this off-shell configuration family.” It
does not mean generic, dynamically selected, observationally viable, or physically necessary.

If continuity, a strict margin, or the parent determinant evidence fails, the maximum negative is
only:

```text
OPEN_NEIGHBORHOOD_NOT_CERTIFIED_AROUND_THE_AFFECTED_FROZEN_WITNESS.
```

It is not a no-go for the complete metric or for another invariant certificate.

## Completeness map

Covered: local `C3` deformations of the complete stationary `R x S3` coframe, joint profile and
parameter perturbations, the five registered gates, their elementary degenerations, and all six
parent all-gate witnesses.

Dropped: explicit radii for the curvature-rank neighborhoods, other topologies/coframes, time-live
fields, field equations, action, boundary variation, stability, carrier, matter, source, density,
bootstrap selection, mass, physical scale selection, `X_max`, and observation.
