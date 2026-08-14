# R4 fresh-context external adversarial review

Date: 2026-08-14
Reviewer: external Codex `gpt-5.4`, sealed read-only 16-source intake
Primary landing: `VERIFIED_WITH_CAVEATS`

## Required repair

The original sentence saying the curve relation was "not a random-density or observational-weight
artifact" was too categorical. The controls support only this narrower statement:

> Broad whole-curve alignment persists across the registered random-density and
> observational-weight control relations at the measured level.

They do not exclude every possible random-catalog or weighting artifact. The outcome report now
uses the narrower wording.

## Surviving conclusions

- The full-census evidence supports broad whole-curve persistence only. It does not establish an
  oscillation, peak, angular scale, or physical interpretation.
- The covariance language is properly bounded: the diagonal-standardized scale is comparatively
  consistent across grids, while the full inverse-like readout is grid- and conditioning-dependent.
- The three verifier-method corrections are acceptable on the supplied record because every
  failure stopped before a result was written, every repair was preregistered before rerun, and no
  production output changed.
- Exact relation, cross-lag, cap-covariance, and summary counts all reconcile.

## Transparency clarification

The final verifier JSON should split the conditioning-sensitive range-projector maxima by field,
rather than reporting only one aggregate maximum. That clarification is incorporated in the final
verifier replay.

## Minimum gate for the proposed next step

An outcome-blind common-subspace atlas is legitimate only if its complete input universe,
centering/normalization, raw-versus-first-difference handling, all control axes, full singular
spectrum, and all-grid reporting are preregistered. No preferred mode count, grid, cap, subgroup, or
feature location may enter the primary claim. Any reduced-rank claim requires a frozen validation
split or a separate discovery/confirmation protocol.
