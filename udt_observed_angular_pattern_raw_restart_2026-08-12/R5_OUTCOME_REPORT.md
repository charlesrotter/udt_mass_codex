# R5 full-spectrum common-subspace atlas — outcome

Date: 2026-08-14
Grade: `OBSERVED_VERIFIED_WITH_CAVEATS__ONE_DOMINANT_SHARED_DIRECTION__ADDITIONAL_SUBSPACE_ALIGNMENT_CONTROL_DEPENDENT__COVARIANCE_RANGE_PARTLY_UNRESOLVED`
Initial preregistration commit: `08bfbe1c`

## What completed

The corrected complete R5 universe contains:

- all 2,328 R2 curves and all 9,286 R4 relations;
- two separate complete vector spaces, with no zero-norm curve;
- 2,607 full-spectrum rows across 11 views per transform;
- 3,555 all-rank subspace-overlap rows across 15 view pairs per transform;
- 275,868 all-grid cumulative covariance-subspace rows;
- 2,850 fixed covariance summaries.

Corrected assembly took 13.78 seconds and about 0.78 GiB maximum RSS. No parent artifact changed.

## One leading direction dominates

In the global ensemble, the first singular direction carries:

- `0.977517` of centered-unit squared energy;
- `0.950970` of first-difference-unit squared energy.

The first ten directions cumulatively carry `0.995620` and `0.978207`, respectively. These values
describe the full spectra; they do not select ten as a physical or preferred rank.

The leading direction is almost identical between the A/B endpoint ensembles of every
preregistered relation class:

| Relation class | Centered rank-1 overlap | First-difference rank-1 overlap |
|---|---:|---:|
| random density | 0.999992 | 0.999955 |
| weight lane | 0.999960 | 0.999981 |
| North/South cap | 0.998903 | 0.996109 |
| adjacent shell | 0.999895 | 0.999782 |
| coarse/fine containment | 0.995355 | 0.998625 |

Together with R4, this identifies one dominant shared whole-curve direction. It does not establish
that this direction is a physical mode, signal, ruler, or UDT response.

## Additional subspace structure is conditional, not one universal reduced rank

All 3,555 rank-indexed overlap rows are independently owned under the frozen spectral-gap rule. The
overlap curves do not collapse after rank one, so the ensemble contains additional aligned
structure. But its persistence differs materially by relation class.

For compact display only, the table below gives the minimum overlap across every proper rank
`1..dimension-1`; it does not choose the rank where the minimum occurs, and the complete curves
remain the evidence:

| Relation class | Centered proper-rank minimum | First-difference proper-rank minimum |
|---|---:|---:|
| random density | 0.921924 (`k=15`) | 0.865557 (`k=24`) |
| weight lane | 0.910466 (`k=11`) | 0.904259 (`k=18`) |
| North/South cap | 0.585710 (`k=16`) | 0.416726 (`k=20`) |
| adjacent shell | 0.860910 (`k=8`) | 0.832150 (`k=8`) |
| coarse/fine containment | 0.700712 (`k=42`) | 0.538790 (`k=22`) |

Thus the residual subspace is comparatively stable to random-density and weight choices, and still
substantially aligned across neighboring shells. It changes much more across disjoint sky caps and
exact shell aggregation. R5 therefore does not own one universal compact rank or one common fine
feature.

## All-grid covariance annotation

The transformed covariance ranks reproduce the R3 resolution structure:

| Transform | NSIDE 4 rank | NSIDE 8 rank | NSIDE 16 rank |
|---|---:|---:|---:|
| centered unit | 68--75 | 118 | 118 |
| first difference unit | 68--75 | 118 | 118 |

All 275,868 covariance-trace and difference-projection rows are independently verified. The
covariance-range projector is independently owned for 91,568 rows and numerically unresolved for
184,300 rows under the preregistered threshold-gap rule. After the external review caught an
evidence-schema omission, every atlas row now saves the covariance threshold gap and explicit
global-subspace, covariance-range, and joint range-overlap ownership flags. The unresolved values
remain saved and are labelled `range_overlap_owned=0`; they are not dropped, regularized, or
interpreted as zero uncertainty.

The 2,850 summary rows are also ownership-aware: 2,369 are `OWNED`, 475 are
`UNRESOLVED_NUMERICAL`, and six transformed-rank summaries are `NUMERICAL_BOOKKEEPING`. Every row is
numerically reconstructed, but unresolved range-overlap summaries do not own a scientific
covariance-range statement.

The covariance layer remains descriptive because `C_N+C_S` assumes zero unmeasured cross-cap
covariance. No covariance-subspace value is a p-value, sigma, likelihood, significance, or proof of
replication.

## Method corrections and independent verification

The first assembly was rejected before interpretation because signed individual-mode covariance
projections depend on SVD sign and degenerate-block basis conventions. The correction, banked before
rerun, replaced them with cumulative top-`k` projector invariants.

The independent SciPy `gesvd`/`evr` replay then required two disclosed verifier corrections:

1. normalized chord distance is a deterministic display transform of overlap and is ill-conditioned
   at overlap one;
2. the complete-space identity projector must use the fixed base tolerance, not conditioning on its
   tiny final singular value.

The accepted verifier reports:

- maximum singular-value difference `4.27e-14`;
- maximum resolved overlap-field difference `8.11e-13`, versus maximum allowed `1.18e-6`;
- maximum resolved covariance-field difference `3.99e-14`, versus maximum allowed `3.99e-7`;
- all 2,850 ownership-labelled summaries and all output-manifest identities reproduced; only the
  2,369 `OWNED` summaries support their corresponding numerical ownership statement.

Five hostile mutations—spectrum, ranked overlap, covariance subspace, summary, and result census—
were all caught even after the corresponding output-manifest row was refreshed.

## Four evidence gates

1. **Preregistered:** yes. R5 was frozen at `08bfbe1c`; the covariance-subspace correction and both
   verifier corrections were each banked before rerun.
2. **Full or bounded scope:** full within the frozen R2--R4 curves, relations, two transforms, 11
   views, 15 comparisons, all ranks, and all R3 grids.
3. **Independently verified:** yes for every spectrum, every relation-overlap row, every
   covariance trace/projection row, all summary values and ownership labels, and manifests.
   Covariance-range overlap remains explicitly unresolved and row-labelled on 184,300 rows.
4. **Premises audited:** yes. Relation-degree weighting, transforms, SVD, gap ownership,
   zero-cross-cap covariance, and numerical eigenthresholds remain conditional numerical choices.

## Maximum conclusion and next gate

`OBSERVED`: the frozen observer-coordinate atlas contains one numerically dominant shared
whole-curve direction plus additional subspace alignment whose strength depends on cap, shell
aggregation, adjacency, weighting, and random-density relations.

R5 does not establish a reduced rank, individual recurring feature, oscillation, preferred angle,
significance, physical ruler, BAO origin, cosmology, UDT response, CMB relation, or `X_max`.

The next justified step is a separately preregistered cross-fitted residual atlas using the fixed
sample-by-cap blocks as held-out folds. It should retain every rank and ask where residual angular
structure predicts a disjoint fold, without choosing a mode count or feature from the validation
fold. Only a later frozen discovery/confirmation rule could promote an individual residual pattern.
