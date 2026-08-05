# Scope correction 01 — research navigation surfaces

Date: 2026-08-05  
Parent preregistration: `PREREGISTRATION.md`, commit `b9915713`

The dependency/link audit found that root `INDEX.md` routes to `research/README.md`, making that file
part of the effective orientation surface. It contains 335 lines of dated current/parent/prior
scientific narration and would reintroduce the exact startup regression this audit is intended to
remove. `research/_registry/README.md` is also a routed navigation control; most of its registry
semantics remain current, but its opening scientific checkpoint is one audit behind the active
program.

This correction expands only the navigation-control scope:

| path | Git blob | SHA-256 | bytes | disposition |
|---|---|---|---:|---|
| `research/README.md` | `b4f1073e34597e1393382c408768abfdc616043e` | `d0f6284a607e7d6f4c1cebcef3c65a75e6f8db5bdf4070a127443e97ac9e1b2c` | 23190 | archive exact snapshot; rebuild lean lane navigation |
| `research/_registry/README.md` | `2b4cda6aa105bf400466c61817423f2856fb6cae` | `aeead8a0d928cbec33ad29f47f85440f63d43e790e05c3753100a3ae7efb50a4` | 4734 | archive exact snapshot; retain registry semantics with lean current-source header |

The exact snapshots will join the same dated archive. No registry TSV, lane inventory, migrated
artifact, research result, evidence, or fixed R0-R1H record may change. Certification is extended to
require both archive hashes, removal of dated science tours from the live research index, retention
of the complete current registry-count/migration boundary, and passing current links/tests/manifests.
