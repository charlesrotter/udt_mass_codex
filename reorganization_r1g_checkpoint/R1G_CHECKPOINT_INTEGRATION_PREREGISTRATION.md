# R1G checkpoint integration preregistration

Date: 2026-07-18

Branch: `codex/reorg-r1g-checkpoint-integration-2026-07-18`

Source tip: `ec18725237d93e5821ce7eae555ba02b4e4ecbd7`

Required pre-integration `origin/grok`: `8015342a81b2d27cc310dde95ab7f386c6441a77`

## Precondition

A fresh fetch must leave `origin/grok` at the required pre-integration hash and
the R1G audit branch at the exact source tip. The grok hash must be an ancestor
of the source tip, their merge base must equal grok, the intervening history
must be linear, and every R1G path change must be confined to
`reorganization_r1g/`. Any advance, divergence, merge, or out-of-scope R1G path
stops integration.

## Bounded mutation

After this preregistration commit, the integration may edit only these six
existing navigation files:

- `LIVE.md`;
- `HANDOFF.md`;
- `INDEX.md`;
- `README.md`;
- `research/README.md`;
- `research/_registry/README.md`.

It may add audit, verifier, test, and replay records only under
`reorganization_r1g_checkpoint/`. It may not edit current registries, research
artifacts, equations, physics verdicts, frozen records, R1G evidence, scripts,
data, manifests, `CANON.md`, or fixed R0–R1F records.

## Required navigation statement

All six navigation edits must consistently record:

- R1G provenance audit and readout correction are complete;
- the prefix-based pre-native classification was false;
- the affected cascade set is 121 `NATIVE_2026-07-01`, zero `MIXED`;
- B02/B03 are 29 `NATIVE_2026-07-01`, two `MIXED`, one `OPEN`;
- reference-only GR/Einstein/Misner–Sharp readouts do not demote native
  operator provenance;
- `phi_source_derivation.py` and `homog_alpha_test.py` remain `MIXED` because
  alpha enters the tested action/EOM;
- the old B02/B03 `archive/pre_2026-07-01/` destinations are withdrawn;
- for affected paths, R1G supersedes the corresponding fixed-snapshot
  classifications in `ROOT_OWNERSHIP.tsv` and `MIGRATION_READINESS.tsv` until
  a separately authorized correction is applied;
- B02/B03 and all further migration remain unauthorized.

## Preregistered verification gates

Before the integration commit:

1. a fresh remote guard must still observe the two required hashes, exact merge
   base, ancestry, linear R1G history, and R1G-only path scope;
2. the diff from the source tip may contain only the six navigation files and
   additions under `reorganization_r1g_checkpoint/`;
3. every required navigation statement must appear in all six authorized files
   without changing their existing startup ordering;
4. every file listed in `reorganization_r1g/OUTPUT_SHA256SUMS.tsv` must match,
   the corrected totals must match the R1G tables, and all eight R1G
   catch-proofs must replay/pass;
5. all six frozen manifests and complete package path/blob states must match the
   source tip;
6. current Markdown links and all frontier targets must resolve;
7. CPU tests must retain the known 69-passed, one-known-failure, one-xfailed
   baseline;
8. the original checkout must retain the frozen 54-path status/lstat metadata
   inventory with dirty contents `NOT_READ`;
9. catch-proofs must reject remote drift, R1G scope drift, unauthorized edits,
   navigation omissions, R1G hash/catch-proof drift, manifest mutation, broken
   links, and dirty-metadata drift.

After the verified integration branch is pushed, `origin/grok` may advance only
by a freshly checked normal non-force fast-forward from the required pre-hash
to the integration tip. Remote grok must then equal that tip.

This checkpoint authorizes no registry correction, replacement batch planning,
B02/B03 migration, further migration, physics, canonization, or GPU work.
