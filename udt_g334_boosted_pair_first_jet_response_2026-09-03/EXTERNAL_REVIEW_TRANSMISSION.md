# G334 external review transmission

Date: 2026-09-03

Charles authorized the sealed 38-file intake at `/tmp/udt_g334_review_9y94a4f6` for fresh read-only
external `gpt-5.4` review, including read-only authentication-file use and network access solely to
launch it.

Authenticated before launch:

```text
REVIEW_SCOPE.json     6c37b71956818bb0c4fbbeb2874711b0799cab94cdf53294dd2cdc60bc15cb93
REVIEW_MANIFEST.tsv   3b7177a54b4c57d6ac5552b3e2f1955e2fabc7128bbdcc4a88cef7feb2206f34
detached seal         4cab7e5fd5636ad20f9bc6d4ed07eacb5bb3fb59b18f9343cff69522ac03809c
manifest payloads     36 PASS
```

The first attempted launch was rejected before transmission because it would have disabled the
reviewer's inner sandbox. The successful launch retained both the read-only outer mount and the
reviewer's own workspace sandbox. The reviewer received the intake read-only, writable ephemeral
work and return directories, the standalone Codex executable, and the authentication file
read-only. There was no repository or protected-package mount. Web search was disabled.

Returned verdict:

```text
ACCEPT__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED
```

No scientific repair was requested. During post-review adjudication, the driver found that an
earlier local preflight replay had written one unmanifested Python bytecode cache into the intake.
The reviewer did not rely on it and replayed registered evidence from a writable copy. The defect
is nevertheless an exact-seal failure and is being repaired under the separately committed
preregistration `1878b3d7`.

## First repair-only follow-up

Charles then authorized the sealed 46-file repair intake at
`/tmp/udt_g334_repair_followup_m9cl41yv`:

```text
REVIEW_SCOPE.json     ed8916c5b62238bf021e86225522555757cfb76c526f3cc77966894980e17902
REVIEW_MANIFEST.tsv   9cea6f731e29cb5e2713e76ed10b15cce8cda0aa0cef2cc5aa5151c0b5027dbe
detached seal         14aef7ccafafc1ecb4d453f38fb16b2d4e5a041f153c5bb045c8dc1c833f2e3e
manifest payloads     44 PASS
```

One launch was stopped before evidence access by a read-only-mount initialization conflict, and
two later launches stopped before model execution during an API 404 outage. A clean launch then
completed inside the same read-only outer boundary and writable ephemeral inner sandbox.

The reviewer independently confirmed that exact-file enforcement rejects a hostile extra, the
46-file intake remains byte-identical after the 103-gate aggregate replay, no bytecode is created,
and the scientific landing is unchanged. It returned:

```text
REPAIRS_INCOMPLETE__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED
```

The only finding was evidence typing: the bundled repair result described the 43-file repaired
fresh-review product without clearly distinguishing it from the 46-file repair-follow-up product.
R3 was preregistered in commit `2630c977` before repairing that distinction.

## Final R3-completion follow-up

Charles authorized the corrected sealed 46-file intake at
`/tmp/udt_g334_repair_followup_v0mcaar5`:

```text
REVIEW_SCOPE.json     43d01ea1deaf86b4a27d7eeb44e883131c29933453834f2648db0c725b1780da
REVIEW_MANIFEST.tsv   45c1b5c1096b9a3c0cca97bad8ed2423118a7470921c9496b1e9124a3634f56c
detached seal         0a261a60b99cd97ca4cf920072d43715937e4efb08fe595dbb1c52729bda1567
manifest payloads     44 PASS
```

The reviewer independently reproduced the 20-gate dual-product repair result byte-for-byte,
confirmed exact 43/46 file counts, hostile-extra rejection, no-bytecode byte-exact replay, and all
103 retained scientific gates. It returned
`REPAIRS_ACCEPTED__G334_BOUNDED_BOOSTED_PAIR_FIRST_JET_RETAINED`, with no remaining mechanical
defect and no scientific change.
