# External G253 repair-only follow-up — accepted

Date: 2026-08-24

Reviewer: external Codex `gpt-5.4`, fresh zero-context read-only repair-only context

Authorized sealed intake:

- path: `/tmp/udt_g253_review_vzjdi13r`
- file count including scope: 51
- `REVIEW_SCOPE.json` SHA-256:
  `42d657740eb9baa54e8a6385b96556252b9a70807da307554be517091cb0b234`

## Verbatim landing

```text
REPAIRS_ACCEPTED
```

## Reviewer findings

- The scope hash matched and all 50 payload hashes matched before evidence review.
- Production, independent, and package verifiers implement the preregistered dual-layout,
  hash-aware, fail-closed source resolver.
- All 21 frozen sources existed only under the sealed `sources/` subtree and matched their manifest
  hashes.
- Repository-layout and sealed-layout positive controls passed. Missing, mismatched, and conflicting
  dual-layout mutations were all caught. The hostile replay returned 23 catches and two positive
  controls.
- All four registered commands exited zero.
- Production reproduced 17 nodes, 12 edges, three graphs, 4,096 rational trials, 21,510 formula
  assertions, 513 founded-depth samples, zero unsupported edges, zero observational values, and zero
  protected paths.
- Independent verification reproduced 12,000 trials and 49,602 assertions with no production import
  or stored-result read.
- The package verifier confirmed all three stored JSON results were unchanged and matched the
  no-write replays.

The bounded scientific landing is unchanged. No new source, node, edge, observational value, fitted
coefficient, protected input, or replay-visible scientific result entered.

## Disposition

The G253 repair is externally accepted. The package may now be graded
`EXTERNALLY_VERIFIED_WITH_CAVEATS` at its exact bounded, mixed-status ceiling. This certification
does not canonize G176 or solve the open history, germ-population, transfer, caustic, aggregation, or
absolute-value questions.
