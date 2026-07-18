# R1F checkpoint integration audit

Date: 2026-07-18

Source tip: `3bb88a6b6cfc223d308b8bae6e27d69b1a1b119f`

Preregistration commit: `a5546429cf2c6606785b07173ac1bb69d2c6f5df`

Pre-integration `origin/grok`: `b59005dba9acaf6c575185876655bd6a5c792094`

## Outcome

The R1F checkpoint records R1E batch planning and R1F/B01 as complete. Five active artifacts have
moved byte-identically: the R1D S8 note and the four R1F macro SymPy verifiers. The current-path
authority is `research/_registry/CURRENT_ARTIFACT_PATHS.tsv`; R1F migration provenance is
`research/_registry/MIGRATION_LEDGER.tsv`. B02/B03 remain proposals, and no further migration is
authorized.

Only these six existing navigation/control files changed from the source tip:

- `LIVE.md`
- `HANDOFF.md`
- `INDEX.md`
- `README.md`
- `research/README.md`
- `research/_registry/README.md`

All other additions are confined to `reorganization_r1f_checkpoint/`. No scientific prose,
equation, claim label, verdict, `CANON.md`, evidence, script, data, manifest, research artifact,
migration registry, or R0–R1F historical/planning record changed.

## Fast-forward precondition

A fresh fetch observed `origin/grok` exactly at the required pre-hash. It is an ancestor of the R1F
source tip, their merge base is exactly the same pre-hash, and the source tip contains five commits
beyond it. The branch is therefore a clean fast-forward candidate.

## R1F identity and behavior replay

Migration commit `c4cf405bba49625a9352a022b60754e7249c27f9` contains four exact R100
renames. Every destination retains the preregistered Git blob and SHA-256; every old path is absent.
Fresh bounded CPU-only execution from repository root returned exit code zero and reproduced the
registered raw streams byte-for-byte:

| Verifier | stdout SHA-256 | stderr SHA-256 |
|---|---|---|
| `verify_center_escape.py` | `f3e0c8d0212d5c01e54abc8de013dd3b62a98b3f6b5583a254c135808c3deff9` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `verify_center_nogo.py` | `a9eae7d513ef994897f04e139f38281dd4372628c443d0d4d3180629e4cbed59` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `verify_eos_dS_window.py` | `310a145c46a66d82c3cbd99df568a41ec562a98b648a6fbacbb3dfd5522bc2d4` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `verify_wrl_canon.py` | `49864b66db59f6f5a4e053f70c4c051f9537d514bd2e3bc1631cfc68888714c8` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The migration ledger has four rows. Each names migration commit `c4cf405...` and its real first
parent `fa211047fd9d81fcc64c424376facc6378837dfc`; the ledger is absent from the migration commit,
so it is not self-referential.

## Navigation and preservation gates

- Current map: 1,114 rows, 1,114 unique original paths, 1,114 unique current paths; 1,109
  `ROOT_RETAINED`, one `MIGRATED_R1D`, and four `MIGRATED_R1F`.
- Markdown navigation: all checked links resolve.
- Current frontier: all 306 rows and 101 unique targets resolve.
- Frozen evidence: all six package manifests replay; all 133 tracked package paths are byte-identical
  to the source tip.
- Tests: 69 passed, one known hygiene-header failure, one xfailed—the established baseline.
- Original dirty checkout: all 54 frozen status/lstat rows match; dirty content remains `NOT_READ`.
- Catch-proofs reject remote advance/divergence, an unauthorized edit, a current-map mismatch, a
  behavioral hash mismatch, a non-R100 move, an invalid ledger parent, a broken link, a manifest
  mutation, and dirty-metadata drift.

Machine-readable results and retained streams are in `VERIFY_RESULT.json`, `behavioral_replay/`, and
`final_validation/` beside this report.

## Stop boundary

This checkpoint authorizes only the normal non-force fast-forward of `origin/grok` to the verified
integration tip. It authorizes no B02/B03 migration, physics work, canonization, or GPU work.
