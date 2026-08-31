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

Repair-only external follow-up is the sole remaining closure gate.

## Current grade

`EXTERNALLY_REVIEWED__REPAIRS_INTERNAL_PASS__FOLLOWUP_PENDING`

The exact bounded G308 landing is unchanged.
