# G308 preregistration — global chirality coherence and parity classification

Date: 2026-08-31
Parent HEAD: `5a199ca6600caf101bbb700c8eed97c5443bf0ff`

## Frozen question

Classify whether the two G307 members selected conditionally by one supplied directed germ both
form coherent global geometric fields on the positive G305 standard completion, and whether any
metric-native global criterion distinguishes them.

## Exact candidate landings

### Candidate A

```text
GLOBAL_COHERENCE_REJECTS_ONE_G307_CHIRALITY
__METRIC_SELECTS_ONE_PHYSICAL_HOPF_MEMBER
```

### Candidate B

```text
BOTH_G307_CHIRAL_MEMBERS_EXTEND_GLOBALLY_AND_CAUSALLY_ON_G305
__CONNECTED_REGULAR_CARRY_FORBIDS_LOCAL_CHIRALITY_SWITCHING
__TRANSVERSE_ORIENTATION_REVERSING_ISOMETRY_EXCHANGES_THE_TWO_SECTORS
__METRIC_ONLY_PHYSICAL_SELECTION_REMAINS_OPEN
```

### Candidate C

```text
BOTH_G307_CHIRAL_MEMBERS_EXTEND_GLOBALLY
__NO_GLOBAL_METRIC_ISOMETRY_RELATES_THEM_AFTER_ORIENTATION_IS_FORGOTTEN
__DISTINCT_PHYSICAL_PARITY_SECTORS_REMAIN_UNSELECTED
```

### Candidate D

```text
CURRENT_G305_G307_DATA_INSUFFICIENT_FOR_GLOBAL_CHIRALITY_COHERENCE_CLASSIFICATION
```

## Exact bounded regime

- G305 positive standard connected completion
  `g=-dT^2+X^2 cosh^2(T/X) dOmega_3^2`, for every `X>0` and every finite `T`;
- both G306 chiral Hopf families and the two G307 members reconstructed from every regular supplied
  ordered unit point/tangent germ;
- all oriented transverse screens and both choices of whether global spatial orientation is
  retained as marked data or forgotten;
- smooth topology-preserving carry only.

## Required derivations

1. Prove or refute global smoothness, unit norm, nonvanishing, and complete-circle spatial orbits
   for both reconstructed members on every slice.
2. Derive the exact time carry of the normalized fields through the G305 warped product. Do not
   call spatial Hopf fibers spacetime geodesics unless the four-dimensional connection proves it.
3. Construct or refute an `O(4)` isometry that fixes the supplied directed route plane and conjugates
   the two candidates while reversing the transverse orientation.
4. Determine whether `SO(4)` can exchange the two chiral components.
5. Derive pair-reversal action on member, chirality, and normalized helicity.
6. Prove or refute constancy of the discrete chirality label on a connected smooth regular family.
7. Compare all metric, curvature, causal-cone, and orientation-even field invariants available in
   scope. A signed pseudoscalar may distinguish labels but may not be called a selector.

## Certification and falsification contract

- Production must use exact standard-library algebra and cover both chiralities, noncommuting
  rational frames, positive radii/scales, pair reversal, and transverse reflection.
- An independent implementation must reconstruct the conjugating reflection and connected-sector
  tests without importing production functions.
- Hostile controls must catch at least: false one-sided global failure; orientation-preserving
  chirality exchange; local smooth chirality switching; pair reversal falsely changing chirality;
  screen-preserving parity; causal-cone difference; spacetime-geodesic overclaim; and physical
  population promotion.
- The current premise verifier and repository regression must pass before banking a verdict.
- Any metric, kernel, member-census, or ownership change fails the preregistration.

## Omitted and forbidden

Nonspherical deformations, nontrivial quotients, singular/cut/caustic strata, topology change,
field dynamics, stability, backreaction, physical query/route/screen population, action, source,
matter, mass, observation, fitted scale, physical `X_max`, and protected work.

## Maximum grade

`VERIFIED_WITH_CAVEATS` until an independent external adversarial review accepts the bounded result.
