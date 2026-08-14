# R4 complete empirical relation atlas — outcome

Date: 2026-08-14
Grade: `OBSERVED_VERIFIED_WITH_CAVEATS__BROAD_SHAPE_PERSISTENCE_WITHOUT_FEATURE_SELECTION__FULL_COVARIANCE_METRIC_GRID_DEPENDENT`
Preregistration commit: `b4179086`

## What completed

The complete preregistered R4 universe completed:

- all 2,328 R2 curves and 119 angular bins;
- 9,286 typed relations across random density, weight lanes, North/South caps, adjacent redshift
  selections, and exact coarse/fine containment;
- 4.38 million full cross-lag entries;
- 1,164 North/South covariance-scale records across all four lanes and NSIDE 4/8/16;
- 972 fixed aggregate summary records.

Assembly used saved R2/R3 evidence only. It took 7.25 seconds, used at most about 0.78 GiB RSS, and
changed no parent data.

## Bounded observation: one broad curve shape persists

The complete centered curves are strongly aligned across every registered relation class. Median
centered cosine and median first-difference cosine are:

| Relation class | Count | Centered cosine | First-difference cosine |
|---|---:|---:|---:|
| random density | 1,552 | 0.999806 | 0.998521 |
| weight lane | 1,746 | 0.999907 | 0.999599 |
| adjacent redshift shell | 2,184 | 0.991263 | 0.968102 |
| North/South cap | 1,164 | 0.989582 | 0.963034 |
| exact coarse/fine containment | 2,640 | 0.992937 | 0.979911 |

This is not driven by one sample/factor subgroup. Across the preregistered subgroup summaries,
median centered cosine ranges are:

- random density: 0.999780--0.999890;
- weight lane: 0.999790--0.999974;
- adjacent shell: 0.990770--0.992204;
- North/South cap: 0.987507--0.992560;
- coarse/fine containment: 0.990477--0.995418.

Broad whole-curve alignment persists across the registered random-density and observational-weight
control relations at the measured level. A broad angular shape also persists across neighboring
redshift selections, disjoint caps, and exact shell aggregation. These controls do not exclude
every possible random-catalog or weighting artifact.

The statement is deliberately about the **whole measured curve shape**. R4 does not identify an
oscillation, peak, angular scale, lag, or physical origin. A dominant common envelope can produce
high cosine even when no smaller repeated feature is established.

## Amplitude and fine structure still change

High shape alignment does not mean identical curves:

- median centered relative L2 difference is about 0.0148 for random density, 0.0141 for weight
  lanes, 0.1135 for adjacent shells, and 0.1135 for caps;
- coarse/fine containment has median centered relative L2 difference 0.4448 even though its median
  centered cosine is 0.9929;
- first-difference relative differences are larger than whole-curve differences in every class.

Thus exact shell unions substantially change amplitude while preserving a dominant shape, and
bin-to-bin detail is less stable than the broad envelope. R4 characterizes that distinction; it
does not filter the less stable structure away.

## Covariance-grid result

The simple diagonal covariance scale is comparatively consistent across grids. Median
North/South diagonal-standardized RMS is:

- NSIDE 4: 0.769;
- NSIDE 8: 0.746;
- NSIDE 16: 0.778.

The full covariance-range quadratic is not grid-stable:

| Grid | Combined rank | Median positive condition | Median range quadratic / rank |
|---|---:|---:|---:|
| NSIDE 4 | 68--75 | 750,152 | 54.37 |
| NSIDE 8 | 119 | 9,246 | 2.53 |
| NSIDE 16 | 119 | 1,384 | 0.82 |

NSIDE 4 also leaves a median 7.63% of the North/South difference outside its numerical range. The
fine grids span the full 119-bin space, but their full-covariance quadratic still changes strongly.

Therefore R4 does not support a grid-independent inverse-covariance significance statement. The
stable diagonal-scale observation is descriptive only; it is not a p-value or proof of cap
replication.

## Independent verification and disclosed repairs

The final independent replay used batched SciPy FFT convolution and SciPy's symmetric eigensolver.
It reconstructed:

- all 9,286 relation descriptors to maximum absolute difference `4.44e-16`;
- every cross-lag entry to maximum absolute difference `1.22e-15`;
- all 1,164 cap-covariance records and all 972 summaries.

Three post-failure verifier-method corrections are preserved. The first implementation used one
short FFT per relation and an unconditional tolerance for ill-conditioned range quadratics. The
next two stops exposed that range fractions and the reported condition number share the same
eigensystem conditioning. Before each rerun, the exact repair was preregistered. Production outputs
never changed. The final verifier records the full condition-aware bounds and passes.

Five hostile mutations—relation descriptor, lag array, cap descriptor, summary, and final census—
were each caught even after their file manifest entry was refreshed. Repository tests return
`89 passed, 1 xfailed`; the xfail is the known unrelated matter-sector habit-pin guard.

A sealed fresh-context external review returned `VERIFIED_WITH_CAVEATS`. Its one blocking wording
repair is incorporated above. It also requested fieldwise reporting of the conditioning-sensitive
verifier maxima; the final verification JSON now records those fields separately.

## Four evidence gates

1. **Preregistered:** yes, at `b4179086`, before any R4 relation or covariance descriptor was
   evaluated. All verifier corrections were separately banked before rerun.
2. **Full or bounded scope:** full within the frozen 2,328-curve R2 and 1,164-record all-grid R3
   relation universe. It remains limited to the registered BOSS catalogs and observer-coordinate
   estimator.
3. **Independently verified:** yes, including different FFT/eigensolver paths and hostile mutation
   catch proofs.
4. **Premises audited:** yes. Relation classes, numerical transforms, grids, rank rule, and the
   conditional zero-cross-cap-covariance scale are explicit. No cosmological or UDT parameter
   entered.

## Maximum conclusion and next gate

`OBSERVED`: the frozen BOSS observer-coordinate atlas contains a highly persistent broad complete-
curve shape across all registered control and neighboring-selection relations, while amplitude and
fine structure vary. Full inverse-covariance readouts remain strongly grid- and conditioning-
dependent.

R4 does not establish a statistically significant oscillation, preferred angle, physical ruler,
BAO origin, cosmology, UDT response, CMB relation, or `X_max`.

The next justified data-only step is an outcome-blind common-subspace atlas: decompose the complete
curve ensemble symmetrically across North/South and redshift selections, retain the full singular
spectrum, and ask whether any structure beyond the dominant broad envelope reproduces across caps,
lanes, factors, random controls, and covariance grids. No mode count or feature location may be
chosen in advance or after inspection without a new validation split.
