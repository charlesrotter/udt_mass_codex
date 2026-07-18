# R1F active macro SymPy verifier quartet audit

Date: 2026-07-18

Base: `14ba31a77aed1553c5df8ecd59b0f7a000c10e20`

Preregistration commit: `fa211047fd9d81fcc64c424376facc6378837dfc`

Migration/navigation commit: `c4cf405bba49625a9352a022b60754e7249c27f9`

Rollback parent: `fa211047fd9d81fcc64c424376facc6378837dfc`

## Outcome

The authorized B01 quartet moved from repository root to matching paths under `research/macro/` as
four R100 renames. Every destination has the preregistered Git blob and SHA-256; every old path is
absent; no duplicate blob copy exists. No verifier byte, scientific prose, equation, claim label,
result, control, evidence, data, manifest, or R0–R1E record changed.

The current-path registry remains one-to-one across 1,114 original/current paths with exactly 1,109
`ROOT_RETAINED`, one `MIGRATED_R1D`, and four `MIGRATED_R1F`. Only those four current-map rows and
the four corresponding macro-inventory path cells changed.

## Bounded behavior replay

Every script was run from repository root before and after movement with `CUDA_VISIBLE_DEVICES` empty,
`PYTHONDONTWRITEBYTECODE=1`, a 30-second `timeout`, Python 3.10.12, and SymPy 1.13.1. Exact commands,
versions, elapsed times, exit codes, raw stream paths/sizes, and hashes are retained in the two
`BEHAVIOR_RUNS.tsv` files. All exit codes were zero; post-move stdout and stderr are byte-identical to
pre-move output.

| Verifier | stdout SHA-256 | stderr SHA-256 |
|---|---|---|
| center escape | `f3e0c8d0212d5c01e54abc8de013dd3b62a98b3f6b5583a254c135808c3deff9` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| center no-go | `a9eae7d513ef994897f04e139f38281dd4372628c443d0d4d3180629e4cbed59` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| EOS/dS window | `310a145c46a66d82c3cbd99df568a41ec562a98b648a6fbacbb3dfd5522bc2d4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| WR-L canon | `49864b66db59f6f5a4e053f70c4c051f9537d514bd2e3bc1631cfc68888714c8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Dependency and provenance audit

Fresh AST and repository checks reconfirmed external SymPy imports only, stdout-only behavior, and
zero file opens, generated outputs, runtime-relative paths, operational inbound dependencies,
frontier hits, manifest hits, test hits, or frozen-package hits. The candidates themselves are not
frozen or manifest paths.

Historical old-basename occurrences remain provenance, not current navigation. The final occurrence
classification explicitly distinguishes fixed R0–R1E records, R1F pre-move/migration records,
retained informational references, current-map original identities, and destination suffixes. There
are zero `STALE_CURRENT_POINTER` rows.

`research/_registry/MIGRATION_LEDGER.tsv` follows the registered R1E schema. Its four entries were
created only after the migration commit existed; all name that commit and its real first parent.

## Final gates

The independent final verifier rejects injected missing-move, artifact-mutation, wrong-destination,
behavioral-output-mismatch, duplicate-current-path, stale-pointer, and invalid-ledger-commit faults.
It also replays links/frontier targets, all six frozen manifests and complete package states, the full
test baseline, and the original 54-path dirty-checkout status/lstat metadata without reading dirty
contents.

This is one organization tile. It authorizes no B02/B03 migration, `grok` integration, physics work,
canonization, or GPU work.
