# R5 full-spectrum common-subspace atlas — preregistration

Date: 2026-08-14
Status: `PREREGISTERED__NO_R5_SPECTRUM_OR_SUBSPACE_RESULT_EVALUATED`
Parents: `R2_OUTCOME_REPORT.md`; `R3_OUTCOME_REPORT.md`; `R4_OUTCOME_REPORT.md`

## Whole question and bounded frame

Does the complete frozen observer-coordinate curve ensemble contain shared angular-vector
subspaces beyond its dominant broad variation, and how do those subspaces change across every R4
control/relation class and every R3 covariance grid?

R5 is data-led and metric-neutral. It characterizes the complete solution space of the frozen
curves; it does not target a BAO peak, oscillation, angle, period, physical ruler, cosmology, UDT
response, CMB relation, SNe profile, `X_max`, or bootstrap parameter.

## Frozen parents

| Artifact | SHA-256 |
|---|---|
| `R2_CURVE_ATLAS.tsv` | `32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603` |
| `R4_RELATION_ATLAS.tsv` | `1badac0c2eeedb2932a8d53f6116d4bfa247774c76f5750ad652da9f35696184` |
| `R4_VERIFICATION_RESULT.json` | `1028f4f80578995c20e5f020db4fbfafc9b73e64589e2fd055f0f3763469b05b` |
| `R3_OUTPUT_MANIFEST.tsv` | `3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa` |

The 194 R3 covariance cells remain the separately hash-verified read-only archive at
`/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS/`.

## Frozen transforms

Every one of the 2,328 complete 119-bin curves is retained. R5 uses two separate vector spaces:

1. `CENTERED_UNIT`, dimension 119: subtract each curve's own 119-bin mean, then divide by its
   Euclidean norm;
2. `FIRST_DIFFERENCE_UNIT`, dimension 118: take all 118 consecutive first differences of the raw
   curve, then divide by their Euclidean norm.

Any zero-norm vector remains as an all-zero row and is counted. No angular bin is removed or
weighted. The two transforms are never pooled.

Centering, differencing, Euclidean normalization, and SVD are `CONDITIONAL` category-A numerical
descriptors. They are not a physical mode definition or derivative law.

## Frozen view universe

For each transform, build exactly 11 row ensembles in the common angular-coordinate space:

- `GLOBAL`: every unique R2 curve exactly once;
- endpoint `A` and endpoint `B` matrices for each complete R4 relation class:
  `RANDOM_DENSITY`, `WEIGHT_LANE`, `CAP`, `ADJACENT_SHELL`, and
  `COARSE_FINE_CONTAINMENT`.

Endpoint matrices retain the exact R4 relation census and relation order. Repeated endpoint curves
remain repeated because relation incidence is the object being characterized. This relation-degree
weighting is `CHOSE` and cannot be promoted to a physical measure.

Each matrix receives a full right singular-vector decomposition. Retain the full singular spectrum,
every singular value, and all 119 or 118 right-singular directions. No rank truncation,
explained-variance cutoff, elbow,
mode count, or preferred view is permitted.

This produces exactly:

- `11 * 119 + 11 * 118 = 2,607` view-spectrum rows.

## Frozen subspace comparisons

For each transform, compare exactly 15 view pairs:

1. the `A` and `B` endpoint bases within each of the five relation classes;
2. each of the ten endpoint bases with `GLOBAL`.

For every pair form the squared cross-Gram matrix internally,

```text
G_ij = (v_i^A dot v_j^B)^2
```

and, for every rank `k=1..dimension`, retain:

```text
overlap(k) = sum(G[0:k,0:k]) / k
normalized_chord(k) = sqrt(max(0, 1-overlap(k)))
smallest_principal_cosine(k) = sigma_min(V_A[0:k] V_B[0:k]^T).
```

Also retain each view's singular-value gap at the `k` boundary. A top-`k` projector is canonical
only where its boundary is spectrally separated; individual singular vectors and mode-to-mode
cross-Gram entries inside degenerate blocks are basis-convention dependent and therefore are not
banked as evidence.

The complete rank-indexed overlap curves, not a selected rank, own the evidence. This produces
exactly:

- `15 * (119 + 118) = 3,555` ranked-overlap rows.

Rank `dimension` is algebraically trivial and remains visible. No threshold labels an overlap as
successful, common, replicated, or physical.

## Frozen all-grid covariance annotation

The covariance layer annotates only the single `GLOBAL` basis for each transform. It does not
select that basis or validate a mode.

For every 97 matched North/South selection, four lanes, three NSIDE grids, and every global mode:

1. form the already registered descriptive scale `C_sum = C_N + C_S` and difference
   `d = w_N - w_S` at the frozen ratio-20 central readout;
2. transform both with the exact linear operator for the vector space:
   `P = I - 11^T/119` for `CENTERED_UNIT`, and the 118-by-119 first-difference matrix for
   `FIRST_DIFFERENCE_UNIT`;
3. symmetrize the transformed covariance and use
   `tau = dimension * eps_float64 * lambda_max`;
4. retain transformed numerical rank, each mode's covariance variance, covariance standard
   deviation, numerical-range fraction, signed North/South projection, and absolute
   projection-to-standard-deviation ratio.

If a mode has exactly zero covariance standard deviation, the ratio field uses numeric placeholder
zero and an explicit degeneracy flag; it is never interpreted as agreement or zero uncertainty.

The ratio is a conditional descriptive scale only. Zero cross-cap covariance remains `CHOSE`; no
entry is a chi-square, sigma, likelihood, significance, or independent replication test. Every
grid and every mode remains visible.

This produces exactly:

- `1,164 * (119 + 118) = 275,868` covariance-mode rows;
- 2,850 fixed covariance-summary rows: four metrics by transform/grid/mode plus transformed-rank
  summaries by transform/grid.

## Execution and output contract

- one CPU process; NumPy float64; no GPU;
- read-only parent inputs and R3 archive;
- refuse to overwrite outputs; atomic writes;
- fixed lexical key and relation-ID order;
- stop on parent hash mismatch, missing/duplicate curve, bin-grid mismatch, relation mismatch,
  missing covariance cell, nonfinite value, materially negative transformed covariance eigenvalue,
  count mismatch, orthonormality failure, or manifest mismatch;
- elapsed time and memory are operational observations only.

Outputs are frozen as:

- `R5_VIEW_SPECTRA.tsv`;
- `R5_RANKED_SUBSPACE_OVERLAPS.tsv`;
- `R5_COVARIANCE_MODE_ATLAS.tsv`;
- `R5_COVARIANCE_MODE_SUMMARY.tsv`;
- `R5_RESULT.json`;
- `R5_OUTPUT_MANIFEST.tsv`.

## Certification and falsification

1. reconstruct exactly 2,328 curves and 9,286 typed relations;
2. emit exactly 2,607 spectra, 3,555 ranked overlaps, 275,868 covariance-mode rows, and 2,850
   summaries;
3. require every view basis to be orthonormal within `5e-12` maximum absolute error;
4. require every singular spectrum nonincreasing within floating-point tolerance;
5. require every ranked overlap finite and within `[0,1]` to `5e-12`, with both boundary gaps
   retained;
6. require full-rank overlap to equal one within `5e-12`;
7. retain all covariance grids and numerical rank loss;
8. require an independent SciPy-SVD/SciPy-eigh implementation to reconstruct spectra, subspace
   projectors, overlap curves, covariance-mode fields, summaries, and manifests;
9. require hostile mutation catches and repository tests;
10. any failure returns `R5_ASSEMBLY_OR_VERIFICATION_FAILURE_TO_AUDIT`.

## Maximum conclusion

At most:

> `OBSERVED`: within the frozen R2--R4 observer-coordinate atlas, the complete singular spectra,
> rank-indexed cross-view subspace overlaps, and all-grid covariance-mode dependence have the
> recorded continuous values.

R5 cannot declare a surviving mode, reduced rank, feature, oscillation, preferred angular scale,
significance, physical origin, BAO interpretation, cosmology, UDT agreement, CMB relation, or
`X_max`. Any reduced-rank or feature claim requires a separately frozen discovery/confirmation
split after the complete R5 atlas is banked.
