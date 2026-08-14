# R4 data-only empirical relation atlas — preregistration

Date: 2026-08-14
Status: `PREREGISTERED__NO_R4_RELATION_OR_COVARIANCE_DESCRIPTOR_EVALUATED`
Parents: `R2_OUTCOME_REPORT.md`; `R3_OUTCOME_REPORT.md`

## Whole question

Which parts of the complete R2 observer-coordinate angular curves persist or change across the
already registered random-density, observational-weight, Galactic-cap, adjacent-redshift, and exact
shell-union relations, and how does North/South disagreement compare with every R3 covariance grid?

R4 is a complete relationship map over the frozen R2/R3 evidence. It does not ask for a BAO peak,
oscillation, expected angle, physical period, acoustic ruler, cosmology, UDT response, CMB relation,
SNe profile, `X_max`, or bootstrap parameter.

## Frozen parent evidence

The following tracked parent identities are frozen before R4 execution:

| Artifact | SHA-256 |
|---|---|
| `R2_CURVE_ATLAS.tsv` | `32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603` |
| `R2_OUTPUT_MANIFEST.tsv` | `6eb143be6c41d4047eab1714de322ce15b8530646456cb6bc0ed43f237333031` |
| `R3_OUTPUT_MANIFEST.tsv` | `3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa` |
| `R3_FINAL_EVIDENCE_MANIFEST.tsv` | `7c609d70b1d55122885c58705dcef9eeb81ca6ded17ec0d550985bd5ecc1913e` |

The 194 immutable R3 cell files are read from the separately hash-verified archive
`/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS/`. R4 must match each
cell to the exact selection key and does not alter that archive.

## Complete typed relation universe

Every R2 curve remains present. R4 constructs exactly these outcome-blind directed relation types:

1. `RANDOM_DENSITY`: `5x -> 20x` and `10x -> 20x` for every selection and lane — 1,552 relations;
2. `WEIGHT_LANE`: `W0 -> W1`, `W0 -> W2`, and `W0 -> W3` for every selection and random ratio —
   1,746 relations;
3. `CAP`: North to South for every exactly matched sample/factor/group/lane/ratio — 1,164 relations;
4. `ADJACENT_SHELL`: lower-group to next-group at fixed sample/cap/factor/lane/ratio — 2,184
   relations;
5. `COARSE_FINE_CONTAINMENT`: every factor-1 child to every factor-2 or factor-4 exact containing
   union at fixed sample/cap/lane/ratio — 2,640 relations.

Total: 9,286 relations. Direction fixes lag signs only; all norm and cosine descriptors are
symmetric. Adjacent, containment, lane, and random relations are not declared statistically
independent.

## Frozen complete-vector vocabulary

For every relation `a -> b`, retain the complete 119-bin inputs and report:

- raw RMS and maximum absolute difference;
- raw relative L2 difference, `||b-a||/sqrt(||a||^2+||b||^2)`;
- the same RMS and relative L2 readouts after removing each curve's own mean;
- the centered raw cosine;
- the RMS, relative L2 difference, and cosine of the complete first-difference vectors;
- each endpoint's raw and centered RMS;
- degeneracy flags rather than dropped relations.

No angular bin is removed or weighted. No threshold classifies a relation as a success or failure.

For every relation, also retain the full linear cross-correlation arrays of:

- the mean-centered 119-bin curves at every integer lag `-118..118`;
- the mean-centered 118-bin first differences at every integer lag `-117..117`.

The lag convention is the NumPy full-correlation order for `correlate(a,b,'full')`, normalized by
the product of the two complete-vector norms. This is a displacement descriptor, not an angular
feature selector. The complete arrays, not only their maxima, are evidence.

## Frozen all-grid cap-covariance readout

For each of the 97 matched North/South selections, four lanes, and all three R3 grids, R4 forms

```text
d = w_N - w_S
C_sum = C_N + C_S.
```

`C_sum` is explicitly a `CHOSE` zero-cross-cap-covariance scale. The caps are disjoint, but the
unmeasured cross-cap covariance is not proved to vanish. Therefore this surface is descriptive and
must not be called a sampling covariance, chi-square, sigma, likelihood, or significance.

After symmetrization, use the unchanged R3 numerical threshold

```text
tau = 119 * eps_float64 * lambda_max(C_sum).
```

Retain numerical rank, condition on the positive range, covariance RMS scale, raw difference RMS,
the fraction of `d` lying in the numerical range, the complementary unresolved/null fraction, the
range-space quadratic energy divided by rank, and the diagonal-standardized RMS over diagonal
entries greater than `tau`. No null-space component is treated as zero uncertainty. No grid is
preferred.

This produces exactly 1,164 cap-covariance records.

## Frozen summaries

R4 reports fixed quantiles (`min`, `q25`, `median`, `q75`, `q90`, `q95`, `max`) and counts:

- for every complete-vector metric, by relation type and by relation type/sample/factor-pair;
- for every cap-covariance metric, by NSIDE and by NSIDE/sample/factor/lane.

No individual curve, redshift interval, angular bin, lag, DCT coefficient, cap, lane, random ratio,
factor, or covariance grid is ranked or selected in the outcome report.

## Premise and method ledger

- Input catalogs, object selections, angular bins, weights, random prefixes, and central estimator:
  `pinned-by-THEORY` only in the operational sense of the banked R0--R2 contracts; they are not UDT
  theory.
- R3 covariance grids and numerical rank rule: `CHOSE`, frozen and all retained.
- Relation types: `CHOSE` because they are the exact registered control/containment/adjacency axes;
  no relation is introduced because its result looks favorable.
- Euclidean vector norms, centering, first difference, cross-correlation, and eigendecomposition:
  category-A numerical descriptions.
- Zero cross-cap covariance: `CHOSE` conditional descriptive scale, never a physical independence
  theorem.
- Cosmological conversion, physical ruler, expected period, UDT curve, and published target:
  absent.

## Execution and restart contract

- one CPU process; NumPy float64; no GPU;
- read-only access to the R2 atlas and archived R3 cells;
- refuse to overwrite any R4 output;
- write each output atomically;
- stop on parent hash mismatch, missing/duplicate curve, bin mismatch, nonfinite input, missing R3
  cell, cell-key mismatch, covariance nonfiniteness, materially negative `C_sum` eigenvalue, count
  mismatch, or manifest mismatch;
- elapsed time and memory are operational observations only.

## Certification/falsification contract

1. exactly 2,328 parent curves with 119 bins must reconstruct;
2. exactly 9,286 typed relations and 1,164 cap-covariance records must be emitted;
3. every registered relation class must have its frozen count;
4. every cross-lag row must retain 237 raw and 235 first-difference lags;
5. every output value must be finite except no missing relation is permitted; degeneracies use flags
   and zero arrays;
6. every `C_sum` must be finite, symmetric, and PSD within `-100*tau`;
7. every NSIDE remains visible; rank loss is recorded, never repaired;
8. a separate implementation must reconstruct every relation descriptor, cross-lag array, and
   cap-covariance record before banking;
9. the repository test suite must pass;
10. any count, identity, PSD, parent-hash, or independent-replay failure returns
    `R4_ASSEMBLY_OR_VERIFICATION_FAILURE_TO_AUDIT`.

## Maximum conclusion

At most:

> `OBSERVED`: within the frozen BOSS observer-coordinate R2/R3 atlas, the complete measured angular
> curves have the recorded continuous similarity, displacement, cap, lane, random-density,
> shell-adjacency, exact-union, covariance-rank, and covariance-resolution dependence.

R4 cannot establish a statistically significant feature, preferred angular scale, oscillation,
physical origin, BAO interpretation, cosmology, UDT agreement, CMB relation, or `X_max`.
