# R2 complete central-pattern atlas — preregistration

Date: 2026-08-12
Status: `PREREGISTERED__NO_GALAXY_PAIR_COUNT_EVALUATED`
Parent: `PREREGISTRATION.md`; R1 gate: `R1_OUTCOME_REPORT.md`

## Whole question

What angular-correlation shapes are present in the frozen BOSS DR12 galaxy catalogs when measured
only in observed sky direction and observed redshift, and how do those complete shapes change across
the already registered redshift resolution, Galactic cap, observational-weight lane, and random
density?

This is an observer-coordinate data-characterization question. It is not a UDT fit and does not ask
for an acoustic ruler, preferred period, expected peak, comoving distance, physical source, or
`X_max`.

## Whole bounded space

R2 evaluates every combination below:

- samples: `LOWZ`, `CMASS`;
- caps: `North`, `South`;
- base fine shells: the 110 sample/cap cells registered in R0/R1;
- exact adjacent object-selection unions: factors 2 and 4 from each sample's fixed lower endpoint;
- terminal incomplete unions are retained rather than discarded (`CMASS` ends with one 0.01-wide
  factor-2 group and one 0.03-wide factor-4 group);
- weight lanes: `W0_UNIT`, `W1_SPECTRO`, `W2_IMAGING`, `W3_OFFICIAL_OBS`;
- deterministic nested random ratios: `5x`, `10x`, `20x`;
- all 119 angular bins from 0.25 to 30 degrees.

This produces 194 cap-visible shell selections and 2,328 complete central curves. North and South
remain separate primary outputs. No cap-averaged curve is used to decide whether structure exists.

Every coarser curve is recomputed from the exact union of its galaxies and random candidates, so
cross-fine-shell pairs are included. It is never obtained by averaging fine-shell curves.

## Deterministic random construction

Within each sample/cap/selection, official-random rows are ordered by the R1 SplitMix64 hash keyed by
the input file's pinned SHA-256. The lowest `20*N_D` hashes are retained. The `5x` and `10x` catalogs
are exact prefixes of that frozen `20x` catalog. No seed or prefix can be changed after a curve is
seen. Random weights remain unity.

## Exact estimator

For every curve,

```text
w(theta) = (DD_norm - 2 DR_norm + RR_norm) / RR_norm.
```

The weighted normalizations are

```text
DD_total = ((sum w_D)^2 - sum(w_D^2))/2
DR_total = (sum w_D) N_R
RR_total = N_R(N_R-1)/2.
```

Raw integer pair counts, raw weighted pair sums, normalization totals, and normalized components are
all retained. No integral-constraint correction, smoothing, baseline subtraction, model covariance,
feature template, or physical scale conversion is applied.

## Outcome-blind shape vocabulary

Every curve receives the same complete, frozen descriptor map:

1. the unaltered 119-bin vector;
2. mean, RMS, total variation, first-difference RMS, and second-difference RMS;
3. every strict adjacent-bin local maximum and minimum, every exact plateau, and every sign crossing;
4. every one of the 119 orthonormal type-II discrete-cosine coefficients;
5. mean-subtracted raw-curve autocorrelation at every lag 0 through 118;
6. mean-subtracted first-difference autocorrelation at every lag 0 through 117.

No extremum, crossing, DCT coefficient, or lag is designated as the feature. Nothing is smoothed or
ranked by resemblance to a desired oscillation. If a curve has zero centered energy, its lag-zero
autorrelation is defined as one and its positive-lag correlations as zero, with a degeneracy flag.

The following comparisons are summarized without pass/fail thresholds:

- `5x-20x` and `10x-20x` random-density differences;
- `W1/W2/W3-W0` weight-lane differences;
- North-South differences for exactly matched sample/shell/resolution/weight/random queries.

Disagreement is retained as observed dependence; it is not a license to choose the quieter lane.

## Engine and provenance

Primary pair counts use Corrfunc `2.5.3`, `DDtheta_mocks`, eight CPU threads, float64 coordinates,
`pair_product` weights, exact registered edges, no mean-angle output, and its declination/RA linking
enabled. Corrfunc is borrowed numerical machinery, not cosmological theory. The exact locally built
wheel is frozen in `R2_ENGINE_PROVENANCE.tsv`.

Independent anchors use TreeCorr `5.1.3` with `metric='Arc'`, linear bins, `bin_slop=0`,
`angle_slop=0`, and float64 inputs. Compact anchors also use direct all-pairs spherical separation.
Official documentation describes both packages as angular pair counters; that role supplies no
physical interpretation:

- https://corrfunc.readthedocs.io/en/stable/api/Corrfunc.mocks.DDtheta_mocks.html
- https://rmjarvis.github.io/TreeCorr/_build/html/nn.html

## Frozen execution and restart design

- one Python process, at most eight CPU threads, no GPU;
- checkpoint after every `DD`, `DR`, and `RR` component;
- existing checkpoints must validate their metadata before reuse;
- final outputs are written atomically and never overwritten;
- registered RSS stop: 16 GiB;
- stop on nonfinite coordinates/weights, nonpositive data weights, insufficient randoms, invalid
  count parity, nonpositive `RR`, checkpoint mismatch, or explicit user interruption;
- elapsed time is operational only and is never a scientific stop or result.

Real-footprint benchmark: the densest tested 20x CMASS-North `RR` component used 662,140 points,
about 89.2 seconds, and 1.63 GiB RSS in Corrfunc. TreeCorr required about 234.5 seconds on the same
component. The complete 194-selection R2 atlas is estimated at 8--24 hours; this is not a timeout.

## Frozen primary outputs

- `R2_PAIR_COMPONENT_ATLAS.tsv`
- `R2_CURVE_ATLAS.tsv`
- `R2_DESCRIPTOR_ATLAS.tsv`
- `R2_EXTREMA_CROSSING_ATLAS.tsv`
- `R2_DCT_ATLAS.tsv`
- `R2_LAG_ATLAS.tsv`
- `R2_CONSISTENCY_SUMMARY.tsv`
- `R2_RESOURCE_OBSERVED.tsv`
- `R2_RESULT.json`
- `R2_RUN.log`
- `R2_OUTPUT_MANIFEST.tsv`
- `R2_VERIFICATION_RESULT.json` (written only by the independent post-run verifier)

Temporary restart components live outside the evidence package and are not scientific outputs.

## Preregistered certification/falsification gates

1. exactly 194 cap-visible selections and 2,328 central curves must exist;
2. every curve must retain 119 bins and finite normalized components;
3. every `RR` bin must be positive;
4. all four data-weight sums and pair normalizations must be positive;
5. every coarser selection must reproduce its exact registered object union population;
6. Corrfunc and TreeCorr integer counts must agree exactly on the frozen independent anchors;
7. their weighted sums must agree to relative `5e-9` or absolute `1e-7`, whichever is looser;
8. brute force must agree exactly on compact integer-count anchors and to relative `5e-12` or
   absolute `1e-10` on their weighted sums;
9. a separate verifier must reconstruct every Landy--Szalay curve and every descriptor from saved
   raw components;
10. a failed engine/count gate blocks interpretation and returns
    `R2_PAIR_ENGINE_OR_ASSEMBLY_FAILURE_TO_AUDIT`.

Random-density, cap, weight, resolution, or shell differences do not fail R2. They are the measured
dependence R2 exists to characterize.

## Explicit exclusions

- no Lambda-CDM or other cosmological distance conversion;
- no acoustic scale, standard ruler, sound horizon, comoving separation, or wavenumber;
- no expected feature angle, published BAO bin, old repository BAO curve, or digitized peak;
- no SNe profile, `c_eff` curve, UDT angular response, `X_max`, or bootstrap parameter;
- no post-reconstruction catalog, `WEIGHT_FKP`, or `NZ`;
- no cosmology-generated mock correction or covariance;
- no fitting, smoothing, peak template, hand-selected baseline, or look-elsewhere significance;
- no physical origin assigned to any observed shape.

## Maximum conclusion

At most:

> `OBSERVED`: in the frozen BOSS observer-coordinate R2 atlas, the complete measured central angular
> curves and outcome-blind shape descriptors have the recorded dependence on observed-redshift
> resolution, cap, observational weights, and random density.

R2 cannot establish a statistically significant oscillation, a physical ruler or origin, UDT
agreement, a physical cosmology, or `X_max`. Those require the data-only covariance/replication gates
of R3 and a later preregistered comparison.
