# R5 external adversarial semantic review

Date: 2026-08-14
Reviewer: external Codex `gpt-5.4`, fresh ephemeral read-only context
Sealed intake: `/tmp/udt_r5_semantic_review_rpxJc1`
Scope SHA-256: `a1738971a7937cd89df9379d0061d78bdf4a5900f3f2ac499d1da6ec1b50f5dd`
Primary landing: `COVARIANCE_CAVEAT_INSUFFICIENT`

The reviewer accepted the load-bearing spectral conclusions:

- the single numerically dominant shared direction is owned;
- the bounded control-dependent additional-subspace statement is owned;
- the assembly correction and two verifier corrections are honest and nonvacuous.

The blocking issue is narrower. The independent verifier computed `91,568` owned and `184,300`
unresolved covariance-range-overlap rows, but the production covariance atlas did not preserve a
row-level covariance threshold gap or ownership flag. The draft outcome therefore overstated that
the unresolved rows were individually labelled. In addition, all-row range-overlap summaries mixed
owned and unresolved numerical values without carrying their scientific ownership status.

## Blocking repairs requested

1. Expose row-level covariance-range threshold gaps and ownership in the production atlas, or state
   only the aggregate verifier totals.
2. Do not describe every range-overlap summary as scientifically owned when unresolved numerical
   rows contribute to it.

## Optional clarifications requested

- Keep the proper-rank minima only as explicitly postselected shorthand and display their minimizer
  ranks.
- A future cross-fitted residual atlas must freeze folds, residualization, scoring, full-rank
  retention, and the prohibition on rank/feature promotion.

The review did not refute or weaken the R5 spectral return. It blocked final banking until the
covariance evidence schema and prose agree.
