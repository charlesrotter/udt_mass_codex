# G308 external-review repair report

Date: 2026-08-31
Repair preregistration: `d212fb42`
Scientific landing changed: no
Metric or reciprocal kernel changed: no

## R1 — sealed-source path portability

`verify_package.py` now resolves each manifest path from exactly one of the repository sibling
layout or sealed `frozen_sources/` layout. Missing and ambiguous layouts raise an assertion.

## R2 — method-distinct independent verification

`verify_chirality_hodge_independent.py` starts from canonical opposite-chirality complex blocks,
random `SO(4)` Givens conjugations, the four-dimensional Hodge-star split, and group-orbit flow. It
does not import production and does not use the production outer-product candidate construction.

Result: PASS; 121,600 checks over 1,600 random frames; maximum error
`1.7763568394002505e-15`. Both global fields, Hodge chirality, `O(4)` exchange, `SO(4)` nonexchange,
pair reversal, connected-stratum separation, normalized time carry, slice/spacetime geodesic
typing, causal equivalence, and unchanged metric/kernel all pass.

## R3 — evidence regrade

The original 79,200-check verifier remains useful and unchanged, but is now described as a
non-importing constructive randomized cross-check. It no longer carries the full independence
claim. The Hodge/group-orbit verifier carries that gate.

## R4 — portability gates

`verify_repair_portability.py` verifies all nine repository sources and passes repository-only,
sealed-only, missing-layout rejection, and ambiguous-layout rejection controls. A freshly rebuilt
51-file sealed intake then ran all six registered commands directly in its `frozen_sources/`
layout without symlinks or manual staging. Production, constructive randomized, Hodge-independent,
hostile, portability, and census outputs were byte-identical to repository outcomes.

The post-repair premise audit passed. The full repository regression returned 199 passed with one
expected xfail in 137.46 seconds.

The first repair-only external follow-up returned `G308_REPAIRS_INCOMPLETE`. It confirmed R1,
R2, and R4, all six sealed replays, byte stability, and the absence of scientific regression. Its
sole blocking finding was one stale `RUN_RECORD.md` heading that still called the original
79,200-check calculation an “Independent replay.”

The exact R3 evidence-language completion was preregistered and pushed at `71acf64f`. The run
record now describes that calculation only as a non-importing constructive randomized cross-check
and gives the independent gate to the separate Hodge/group-orbit calculation.

The Hodge verifier intentionally tests bounded geometry, not semantic physical-population
ownership. The unchanged nonselection boundary is audited separately by the derivation result,
status ledger, and semantic hostile controls; inserting a self-declared ownership boolean into a
numerical verifier would not independently establish that boundary.

The R3 completion-only external follow-up returned `G308_R3_COMPLETION_ACCEPTED` with no blocking,
medium, or low defects. It reran all six sealed checks, confirmed byte identity of all six
load-bearing outcomes, and accepted the unchanged landing, metric, kernel, census, and ownership
boundary.

After the completion, all six registered package replays pass, the 289-row premise audit passes,
and the repository regression returns 199 passed with one expected xfail in 136.93 seconds. The
six pre-existing load-bearing outcome files remain unchanged.

## Current grade

`EXTERNALLY_VERIFIED_AFTER_R3_COMPLETION`

The exact bounded G308 landing is unchanged.
