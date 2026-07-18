# R1G checkpoint integration audit report

Date: 2026-07-18

Branch: `codex/reorg-r1g-checkpoint-integration-2026-07-18`

R1G source tip: `ec18725237d93e5821ce7eae555ba02b4e4ecbd7`

Pre-integration `origin/grok`: `8015342a81b2d27cc310dde95ab7f386c6441a77`

Preregistration commit: `15f2b8632127b4c01ed66c3ba0478b936d363957`

## Scope result

PASS. A fresh fetch found the required remote hashes. The R1G source is four
linear commits beyond `origin/grok`, has that exact grok tip as its merge base,
and changes 26 paths, all under `reorganization_r1g/`. The integration changes
only the six authorized navigation files plus additions under
`reorganization_r1g_checkpoint/`. The current registries, research artifacts,
fixed R0–R1F records, R1G evidence, frozen packages, scripts, data, manifests,
physics verdicts, equations, and `CANON.md` are unchanged.

The six navigation files now record the completed R1G provenance audit and
readout correction, the corrected 121/0 and 29/2/1 counts, the reference-only
readout rule, the two action/EOM alpha-coupling exceptions, withdrawal of the
old B02/B03 pre-July archive destinations, R1G's temporary supersession of the
affected fixed-snapshot classifications, and the stop boundary.

## Verification result

The machine-readable result is [`VERIFY_RESULT.json`](VERIFY_RESULT.json).

- R1G output index: 25 indexed files passed; index SHA-256
  `2defa65f404d982a5212bc3e4e0fe2b1802f91ab59b2f29caa2fff3291bb8ad2`.
- Fresh R1G replay: byte-identical to the retained independent result, SHA-256
  `920b09b87248877a2a5c9a204ee1ba041f9f9f006fe885307d16ff916557b426`;
  all eight R1G catch-proofs passed.
- Integration catch-proofs: all nine passed, rejecting remote drift, R1G source
  scope drift, unauthorized edits, navigation omission, R1G hash drift, R1G
  catch-proof drift, manifest mutation, broken links, and dirty metadata drift.
- Frozen packages: all six manifests replayed; all 133 tracked package paths
  remain byte-identical to the R1G source tip.
- Navigation: 92 local Markdown links and all 306 frontier rows / 101 unique
  targets resolved.
- Tests: 69 passed, one known hygiene-header failure, one xfailed; baseline
  match PASS.
- Original dirty checkout: 54 status/lstat rows matched the frozen inventory;
  content policy remained `NOT_READ`.

## Authority boundary

This checkpoint is navigation only. It authorizes no registry correction,
replacement batch planning, B02/B03 migration, further migration, physics,
canonization, or GPU work. B02/B03 remain paused.
