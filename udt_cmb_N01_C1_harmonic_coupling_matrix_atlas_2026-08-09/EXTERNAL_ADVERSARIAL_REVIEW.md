# Fresh zero-context adversarial review

## Provenance

- reviewer: fresh read-only Codex subagent `n01_cold_review`
- context fork: none
- repository HEAD inspected: preregistration commit `1537d669d411c1bb4c18c0814dc1aef3af7ea36d`
- mutation authority: none; the reviewer made no file changes
- verdict: `VERIFIED-WITH-CAVEATS`

## Independent work performed

The reviewer independently reconstructed the projected matrix equation and full radial `W(B(r))`
flux, checked the negative-`m` normalization/sign handling, proved the parity blocks, and reproduced
the round `K+H` cancellation. Direct symbolic integration reproduced all 180 values in the 36-row
first-order table. Exact expected key sets reproduced the 15,420 element, 120 summary, and 36
first-order row universes.

A separate full-table SciPy/Jacobi calculation was limited by double-precision endpoint cancellation
to `1.13e-10` maximum disagreement, including `9.11e-11` internal round error; this was treated as a
reviewer-method precision limit, not a contradiction. A separate 50-digit calculation of 18 hard
controls, including strong-`B` `L/K/H` entries, agreed within `1.82e-14`. All frozen source hashes
reproduced.

## Required repairs and disposition

1. The vacuous production coupling-reach key was replaced by reconstruction of substantive block
   summaries from every preserved element row.
2. The local verifier now compares exact expected element, summary, and first-order key sets and
   independently rebuilds substantive summary fields.
3. Captured verification counts are regenerated after the existing twentieth local check.
4. Round-limit prose now distinguishes `|m|>0` cancellation from the already diagonal `m=0` case.
5. Independence wording now separates all-table same-implementation convergence from selected
   independent adaptive/high-precision recomputation.
6. The finite-band statement is now supported by an exact nonpolynomial-column proof for `W`, `M`,
   and `L`, with `B=0` explicit.
7. The package manifest is generated only after these amendments and all replayed gates stabilize.

The reviewer re-ran the repair acceptance check, found the amended gates and tables consistent,
and required one final wording correction from “finite `B`” to the exact domain `B>0`. That
correction was applied before the final replay and manifest generation. `REPAIRS_ACCEPTED`.

## Authority boundary

The review accepts only the conditional, bounded C1 coupling architecture. It does not select C1,
promote scalar `Box_g` to UDT dynamics, solve a radial/eigenvalue problem, restart FD2, or authorize
population, polarization, observational fitting, or GPU work.
