# G277 audit report — observational scale-anchor ownership

Date: 2026-08-26

Grade:
`EXTERNAL_REVIEW_ACCEPT_WITH_REPAIRS__REPAIRS_IMPLEMENTED__FOLLOWUP_PENDING__BOUNDED_LANDING_UNCHANGED`

## Landing

```text
PANTHEONPLUS_CEPHEID_HOST_ROUTE_IS_A_CONDITIONAL_ABSOLUTE_SCALE_ATTACHMENT
__NOT_A_NATIVE_G276_CLOCK_ANCHOR
__PANTHEONPLUS_NONCALIBRATORS_DES_AND_THEIR_RELATIVE_COMBINATION_REMAIN_SCALE_DEGENERATE
__CMB_TEMP_IS_NOT_CURRENTLY_SCALE_TYPED
__NO_FIT_SCALE_HISTORY_KERNEL_OR_XMAX_SELECTED
```

## What was learned

The held Pantheon+ file contains 1,701 light-curve rows. Seventy-seven rows, representing 43 unique
candidate IDs, are marked as Cepheid-host calibrators. Every calibrator has a positive
`CEPH_DIST`; every noncalibrator has the release sentinel `-9`. The covariance is exactly
`1701 x 1701` and the collaboration states that it includes Cepheid-host covariance.

The primary release documentation and official likelihood give the decisive typing. `CEPH_DIST`
is the Cepheid-host distance modulus. On calibrator rows the likelihood uses it in place of a
redshift-derived cosmological distance and thereby calibrates the common standardized SNe absolute
magnitude.

Those two primary sources are now sealed and hashed inside `sources/`; their semantics no longer
depend on an unhashed URL citation.

That changes the exact identifiability rank:

| model | rank | columns | consequence |
|---|---:|---:|---|
| one relative SNe release: scale + free offset | 1 | 2 | scale not identifiable |
| two relative releases with separate offsets | 2 | 3 | scale not identifiable |
| two relative releases with one shared offset | 1 | 2 | scale not identifiable |
| Cepheid calibrators + Hubble-flow SNe: scale + shared absolute magnitude | 2 | 2 | conditionally identifiable |
| `cmb_temp`: scale + unknown source temperature | 1 | 2 | scale not identifiable |

Thus the Pantheon+ calibrator route can attach an absolute scale only after accepting two explicit
observational bridges:

1. the published Cepheid distance-ladder calibration;
2. a declared map between its photometric distance and the same UDT metric observable—currently the
   imported transparent luminosity/area transfer used in G236/G258.

This makes it a `CONDITIONAL_TRANSFER_OR_DISTANCE_ANCHOR`, not a native G276 proper-clock anchor.

The official likelihood mask selects 1,657 actual rows: 77 calibrator rows and 1,580 Hubble-flow
rows. The actual two-column design has rank two. The raw released covariance fails the
preregistered exact-symmetry tolerance: its maximum transpose defect is
`3.0000000000038676e-08`, above `1e-12`. That failure is retained. A separately preregistered
finite-serialization audit then used the symmetric mean, reflected lower triangle, and reflected
upper triangle. All three matrices are positive definite and give weighted rank two; their
smallest/largest Fisher-eigenvalue ratios are approximately `0.00402782`. Maximum route variation
is `3.06e-9` for Fisher entries and `1.83e-7` for eigenvalues, within the frozen `1e-4` robustness
tolerance. The dataset-weighted identifiability result is therefore robust across those three
declared symmetric interpretations, with the raw covariance asymmetry retained as a release-format
caveat.

DES-Dovekie alone remains relative in the UDT audit. Its release says `MU` assumes `H0=70`, and its
global nuisance parameters were determined in the collaboration likelihood. Importing that
normalization would not be deriving a UDT scale. Combining DES with Pantheon+ after removing the
calibrators also does not help: the common scale column remains in the span of the catalog offsets.

The current `cmb_temp` object remains `OPEN_NO_OWNER`. The conditional thermal readout constrains a
temperature ratio or reciprocal depth only after a source temperature and transfer law are
supplied. Constant metric homothety does not change the normalized projective state, so CMB
temperature does not presently fix `ell`.

## What did not happen

- no observational residual or fit was evaluated;
- no numerical `ell`, distance, `H0`, history, or `X_max` was inferred;
- no SNe state coefficient was changed;
- no angular term was fitted or added;
- no metric or reciprocal-kernel formula changed;
- no protected package or BOSS outcome was inspected.

## Recommended next gate

The scientifically strongest available empirical sequence is:

1. freeze a Pantheon+-only relative state at every already preregistered G236 resolution;
2. add only the Pantheon+ Cepheid-host rows and their full cross-covariance to determine the one
   absolute scale under the explicitly imported luminosity/area transfer;
3. freeze that scale and state;
4. test DES-Dovekie with no scale, offset, shape, or kernel retuning beyond the release's explicitly
   declared observational nuisance convention;
5. compare the recovered scale across resolutions and calibrator subsets as robustness checks.

This is an empirical calibration and held-out validation of a supplied dimensionless state, not a
native derivation of the UDT history. The cleaner direct route remains a same-object clock or
geometric record of the G276/G250 type, but no such local observational instance is presently
registered.

`cmb_temp` should come later as a high-depth consistency query, after its source-temperature and
transfer premises are made explicit. It should not set the scale in the current theory state.

## Evidence

- outcome-blind preregistration committed and pushed at `ee0f178c`;
- 18/18 source hashes verified, including the two sealed official Pantheon+ sources;
- exact schema checks: 1,701 Pantheon+ rows, 77 calibrator rows, 43 unique calibrator IDs, and
  `1701^2` covariance payload entries;
- eight candidate classes recorded;
- five exact structural design-rank classifications;
- the actual 1,657-row covariance-weighted design has rank two across all three preregistered
  symmetric covariance interpretations;
- implementation-distinct Cholesky-whitened verification reproduces the schema, actual weighted
  rank, covariance caveat, and all eight classifications from hashed source semantics plus computed
  ranks, without importing the production script or reading its output; same-object identity and
  operational-distance/transfer ownership are derived as distinct facts;
- eleven nonvacuous hostile ownership overclaims exercise and reject every registered acceptance
  criterion by name;
- three registered no-write replays preserve all six durable output hashes;
- repository-only purity suite: 181 passed, 1 documented xfail locally; this was outside the sealed
  external review scope and was not externally replayed;
- zero fits and zero numerical scale estimates.

## Scope ceiling

The result is a bounded ownership classification. Initial fresh hostile review retained the
scientific landing and identified evidence defects R1--R5. The zero-context repair-only follow-up
accepted the repaired source-derived classifier, complete hostile-criterion coverage, and corrected
wording while retaining the scientific landing. The result remains conditional because the Cepheid
distance ladder and luminosity/metric-distance bridge are supplied observational premises rather
than UDT-derived light physics.
