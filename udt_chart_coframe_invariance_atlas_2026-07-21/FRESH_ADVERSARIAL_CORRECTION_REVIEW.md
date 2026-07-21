PASS-WITH-CAVEATS

- HEAD directly resolves to `codex/udt-chart-coframe-invariance-atlas-2026-07-21`.
- All 61 manifest entries replayed successfully; recursive coverage is exact and duplicate-free.
- Read-only scientific replay passed 1,419,862 checks and 14 exercised mutation catches, including K06, K07, and K10.
- Independent Cartan/spin-connection route passed 3,952 anchors; worst Cartan/connection residuals were \(2.22\times10^{-16}\) and \(3.05\times10^{-16}\).
- Compact verification output is 1,434 bytes. The sole uncertain rank is correctly recorded as C05/M4 split-slot rank 130, with retained/discarded margins \(1.077\times10^{-9}\) and \(3.348\times10^{-10}\).
- Five source hashes, six frozen manifests/127 entries, 66 prior manifests/1,665 entries, and navigation targets 1,114 plus 306/101 all replayed.
- All 54 dirty-checkout paths still match recorded sizes/types; contents were not read.
- Recorded tests show 69 passed, one known hygiene failure, and one xfail. Exact test rerun was prevented by the enforced read-only temporary filesystem; this does not affect the independently replayed scientific verifier.

Required caveats: finite charts/coframes are not a full-group proof; split findings are conditional and select no physical split.