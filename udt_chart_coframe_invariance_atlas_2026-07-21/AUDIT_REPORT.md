# Chart/Coframe Invariance Atlas — Audit Report

Date: 2026-07-21

Status: `COMPLETE_VERIFIED_WITH_CAVEATS`

Maximum conclusion:
`BOUNDED_CHART_COFRAME_AND_SUPPLIED_SPLIT_INVARIANCE_ATLAS_CHARACTERIZED`.

## Result first

The complete registered atlas separates two things that the earlier ensemble map left entangled:

1. The full metric/curvature interaction structure is invariant under every registered invertible
   chart and Lorentz-coframe transformation. Component values and singular values change, but every
   full-tensor activity decision and every full-tensor interaction span rank is unchanged.
2. The slot/shear/twist account is invariant only while the same supplied 2+2 distributions are
   retained. If a chart mixes or re-seats which coordinate directions are called base and screen,
   those split diagnostics can acquire many new Möbius terms without any change in the underlying
   tensor geometry.

That is not a new mechanism. It is a clean representation/partition distinction.

## Complete bounded coverage

- Parent configurations: 6,144 = 48 carriers x 16 masks x 8 contexts.
- Parent Möbius targets: 5,760 = 48 carriers x 15 nonempty targets x 8 contexts.
- Registered transformations: 12 = 7 constant coordinate charts + 5 Lorentz coframes.
- Configuration-orbit rows: 73,728.
- Interaction-orbit rows: 69,120.
- Span-rank rows: 1,800.
- Discarded rows: zero.
- Numerical covariance failures: zero.
- Worst certification residual: `1.7763568394002505e-15` against `1e-10`.

The independent verifier performed 1,419,862 fail-closed checks and 14 exercised mutation catch-proofs. It
also recomputed 3,840 local-Lorentz metric-jet anchors, 112 coordinate-curvature anchors, and 768
cross/re-seated split interactions using a separate second-jet algebra. Its worst independently
recomputed split-interaction residual was `1.1102230246251565e-16`. In addition, 3,952 Cartan
curvature anchors were independently evaluated through the spin-connection/exterior-curvature route;
the worst Cartan and local-connection transformation residuals were `2.2204460492503131e-16` and
`3.0531133177191805e-16`.

## Transformation findings

### Full tensors

Across all twelve transformations:

- metric-two-jet active rows remained 1,536/5,760;
- Riemann, Weyl, Ricci, scalar, and Cartan-curvature active rows each remained 2,640/5,760;
- phi-two-jet active rows remained 384/5,760;
- activity discordances for every full-tensor payload were zero;
- all 15 target-by-target span ranks were identical for every full-tensor payload.

The constant and local internal boosts/rotation change the coframe components of Cartan curvature by
the registered Lorentz representation, while leaving the metric, coordinate curvature, conditional
split, and their Möbius activity exactly unchanged. Even the coframe boosts mixing an internal time
row with an internal screen-labelled row do not select or alter a coordinate base/screen split.

### Supplied 2+2 split

| transformation class | slot active | shear active | twist active | split domain |
|---|---:|---:|---:|---|
| identity, block-preserving charts, all Lorentz coframes | 1,152 | 1,104 | 384 | 5,760 defined |
| cross charts and depth/screen reseating | 2,640 | 2,496 | 2,496 | 5,760 defined |
| time/screen reseating | 0 | 0 | 0 | 5,760 undefined |

For each of the two cross maps and the depth/screen permutation, the activity decisions differ from
the original split in exactly 1,488 slot, 1,392 shear, and 2,112 twist rows. The two cross maps are
inverse probes, yet give the same activity census. The permutation gives the same census by a very
different map. This makes the qualitative partition dependence robust inside the finite design.

The time/screen permutation keeps the four-metric Lorentzian and every full tensor defined, but puts
the time direction inside the conditional positive screen block. Consequently all 6,144 supplied
splits and all 5,760 split interactions are correctly classified
`SUPPLIED_SPLIT_UNDEFINED_SIGNATURE`; none is imputed or discarded.

### A concrete contrast

For the base-screen target `M3`, the original and block-preserving split slot/shear/twist span ranks
are `0/0/0`. After a cross-sector chart followed by re-seating the split as the new first two versus
last two coordinates, they are `105/6/2`. Yet the Riemann span rank remains 19 in every chart.

Likewise, the original screen-shift target `M6` has metric-two-jet rank 105 and split-slot rank 0.
The re-seated cross splits keep metric-two-jet rank 105 but change split-slot rank to 150 (135 for the
depth/screen permutation). The added split interactions therefore do not represent added curvature
or a new solution; they are produced by the nonlinear reconstruction of a different supplied split.

## What survives the audit

- `OBSERVED`, bounded and independently verified: the parent ensemble's full curvature Möbius
  structure is not an artifact of the registered constant charts or local Lorentz coframes.
- `OBSERVED`, bounded and independently verified: slot, shear, and twist interaction assignments are
  conditional on the supplied 2+2 distributions.
- `OBSERVED`: an internal coframe row label cannot by itself select the physical base/screen split;
  local Lorentz gauge transformations can mix those rows without changing the metric.
- `OPEN`: whether UDT supplies an invariant projector/distribution that makes one split intrinsic.

## Caveats and premise audit

- The coordinate set is finite and constant. Nonlinear chart jets are not sampled, so this is not a
  proof over the full diffeomorphism group.
- The Lorentz set is finite, although it includes constant and local transformations with nonzero
  first and second parameter jets. It is not a group-exhaustiveness proof.
- Ensemble identities remain attached to the immutable parent histories. This atlas transforms those
  histories; it does not re-fit the eleven latent controls in each new chart/coframe.
- The first-two/last-two split remains `CHOSE`, not `DERIVED`. Re-seating it is an explicit diagnostic,
  not a claim that every coordinate split is physically equivalent.
- The component activity/rank threshold is the inherited `1e-9`. Full-tensor outcomes have no
  threshold discordances. The cross-split shear/twist activity ledger contains 22/3 and 22/6 rows,
  respectively, inside the preregistered broad `1e-11..1e-7` caution band. Separately, the
  `C05_SWAP_DEPTH_SCREEN/M4/split_slot_twojet` rank 130 is threshold-sensitive: its smallest retained
  singular value is `1.0766158328336954e-9` and its largest discarded singular value is
  `3.347707008015074e-10` at the `1e-9` threshold. This affects that exact conditional split rank
  only; it does not affect any full-tensor rank or the cited M3/M6 contrasts. No conclusion treats
  this margin as a selector.
- No action, field equation, source, carrier, boundary, scale, topology, or physical evolution was
  loaded.

## Four banking gates

1. Preregistered: **YES**, including a separately committed pre-compute correction of two manifest
   hash transcription errors.
2. Full space or bounded scope justified: **YES** for every parent row and every registered finite
   transformation; not exhaustive over all charts/coframes.
3. Independently verified: **YES** for the load-bearing tensor and split distinction. The corrected
   fresh adversarial review returned `PASS-WITH-CAVEATS`; its required caveats are the same finite-set
   and conditional-split limits stated here.
4. Every premise audited: **YES** in `PREMISE_STATUS_LEDGER.tsv`, with the preferred split and full
   group scope still `OPEN`.

This is a verified bounded atlas, not a physical split-selection theorem.
