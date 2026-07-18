# July 1 native-field-equation boundary

The exact boundary is commit
`f7664786d1e2340262ea5aa22336cf0c2f8b0dfc`, whose parent is
`78939836326cb822e22b2a72bfd8097365185aa6`. Git ancestry, not a filename or a
calendar-only rule, establishes this boundary.

The boundary commit was made on `2026-07-01T10:18:06-04:00`, is titled
“Native UDT field equations derived (constrained-two-player, G/P regimes) + CAS
+ blind verified,” and introduces
`native_field_equations_constrained_two_player_results.md` and
`verify_native_fieldeq.py`. Its result record says the derived system
supersedes the live scalar-tensor system as the native frame. The later
`af286a6` native-geometric-action commit extends that lineage; it does not move
the first-native-field-equation boundary.

The operator-contamination ledger independently distinguishes the earlier
scalar-tensor/Einstein-Hilbert operator from the `f766478` native geometric
source equation. The July 4 pursuit charter likewise names the July 1 native
field equations as the foundation. The machine record is
[JULY1_NATIVE_BOUNDARY.json](JULY1_NATIVE_BOUNDARY.json).

Consequently, a file introduced after `f766478` is not automatically native,
but it also cannot be classified pre-native from its name. It requires
path-specific operator lineage. A mixed use of the native operator and an
imported/reference operator is `MIXED`; insufficient operator evidence is
`OPEN`.
