# Fresh adversarial review — R3 patch cardinality

Date: 2026-08-13
Reviewer: fresh zero-context agent `/root/r3_patch_adversary`
Final verdict: `VERIFIED`

The reviewer traced TreeCorr `5.1.3` source and confirmed that `Catalog._set_npatch()` overwrites a
configured cardinality with `max(patch)+1` for per-object patch arrays. It independently verified
that explicit lists of scalar-patch child catalogs retain nonconsecutive global IDs, the common
cardinality, central totals, result-key ownership, and literal deletion identities.

The first pass returned `VERIFIED-WITH-CAVEATS` and required stronger checks for child membership,
internal holes, both one-sided occupancy directions, DD/DR/RR deletion, honest weighted-residual
wording, exact contract reads, all `48` legacy cells, wrapper exit propagation, and pinned engine/code
versions. Those corrections were implemented.

The second pass confirmed the substantive semantic deficiencies closed and required two final
fail-closed checks: exact legacy hashes/field absence/filename identity, and mandatory repository
tests whenever real cells are requested. Those corrections were implemented.

The final narrow pass returned `VERIFIED` with no remaining required code correction. The reviewer
did not run real cells or inspect covariance outcomes. The main verifier separately reran the South
trigger, North regression, wrapper exit test, and repository suite.
