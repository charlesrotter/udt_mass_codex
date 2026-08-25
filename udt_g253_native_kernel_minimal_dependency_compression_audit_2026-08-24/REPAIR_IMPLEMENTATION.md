# G253 repair implementation

Date: 2026-08-24

## Implemented scope

Only the preregistered sealed-source replay defect was changed.

1. `derive_native_kernel_compression.py` now resolves manifest and edge sources from either the
   repository root or the sealed `sources/` subtree. Every existing candidate must match the frozen
   manifest SHA-256.
2. `verify_native_kernel_compression_independent.py` contains an independently written resolver with
   the same fail-closed contract and no production import.
3. `verify_package.py` uses the same dual-layout contract when checking the source manifest and then
   invokes all registered no-write replays.
4. `run_catch_proofs.py` adds two positive layout controls and catches missing, mismatched, and
   conflicting dual-layout sources. The hostile count increases from 20 to 23 for this certification
   repair only.

## Scientific noninterference

The production result remains 17 nodes, 12 edges, three typed graphs, 4,096 exact rational trials,
21,510 formula assertions, 513 founded-depth samples, and zero unsupported edges. The independent
result remains 12,000 trials and 49,602 assertions with no production import or result read. No
scientific source, premise status, formula, node, edge, historical-control disposition,
observational value, or protected path changed.

## Replay gate

Repository-layout replays pass. A fresh 50-file sealed-layout intake at
`/tmp/udt_g253_review_mjtlwrd8`, with `REVIEW_SCOPE.json` SHA-256
`3cbdc9e9acfb1b63617235e12d6eddc137dd2d7e99440563ddc71eee793b59a1`, passed all four
registered commands. Production and independent outputs remained unchanged, the stored hostile
result matched, and the package verifier returned `PACKAGE_PASS`.

External repair-only follow-up remains required.
