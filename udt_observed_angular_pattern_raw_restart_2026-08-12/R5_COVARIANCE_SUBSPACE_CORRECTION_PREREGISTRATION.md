# R5 covariance-subspace correction — preregistration before rerun

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_FIRST_ASSEMBLY_METHOD_FAILURE__BEFORE_RERUN`

## Failure

The first assembly completed its frozen counts, but no outcome was interpreted and no verification
result was written. During design of the independent replay, the covariance annotation was found to
be incorrectly typed:

- the sign of an individual right singular vector is conventional;
- inside a degenerate singular-value block, the individual vectors can rotate without changing the
  data matrix;
- therefore signed individual-mode projections and individual-mode covariance readouts are not
  invariant evidence.

The superseded output files were moved intact to the temporary path recorded in
`R5_FIRST_ASSEMBLY_METHOD_FAILURE.json`. They are not scientific returns and will not be banked as
R5 evidence.

## Frozen correction

The curve transforms, 11 views, full singular spectra, 15 pair comparisons, all-rank projector
overlaps, spectral gaps, parent inputs, and every census remain unchanged.

Replace only the covariance annotation with cumulative top-`k` subspace quantities. For each global
basis `V`, transformed covariance `C`, transformed cap difference `d`, and every
`k=1..dimension`, retain:

```text
P_k = V[0:k]^T V[0:k]
covariance_trace(k) = trace(V[0:k] C V[0:k]^T)
covariance_trace_per_rank(k) = covariance_trace(k) / k
difference_projection_norm(k) = ||V[0:k] d||
range_overlap(k) = trace(P_k P_range) / k
projection_norm_to_trace_sd(k) = difference_projection_norm(k) / sqrt(covariance_trace(k)).
```

These are invariant under sign changes and rotations within the supplied top-`k` subspace. The
top-`k` subspace itself is not canonical at a degenerate boundary, so every row also retains the
global singular-value boundary gap. No gap threshold selects or removes a row.

If the covariance trace is exactly zero, the ratio receives numeric placeholder zero plus an
explicit degeneracy flag. It is never interpreted as zero uncertainty or agreement.

The corrected outputs are:

- `R5_COVARIANCE_SUBSPACE_ATLAS.tsv` — exactly 275,868 rows;
- `R5_COVARIANCE_SUBSPACE_SUMMARY.tsv` — exactly 2,850 rows.

The summary retains four metrics at every transform/grid/rank—trace per rank, range overlap,
difference-projection norm, and projection-norm/trace-SD—plus transformed-rank summaries. The
conditional zero-cross-cap-covariance scale and every no-significance caveat remain unchanged.

## Verification gate

The independent SciPy replay must reconstruct singular spectra and boundary gaps, compare ranked
projectors only with explicit gap-conditioned numerical ownership, and reconstruct every corrected
covariance-subspace field, summary, and manifest. No individual SVD-vector sign or degenerate-block
basis orientation may be treated as evidence.
