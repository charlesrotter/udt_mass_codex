# Startup/orientation quarantine audit report

Date: 2026-08-05

Preregistration commits: `b9915713`, scope correction `2d3ae85c`

Scientific scope: none; navigation and provenance only

## Result

`VERIFIED_STARTUP_ORIENTATION_QUARANTINE`

The regression risk was architectural, not a newly discovered physics error. Mutable startup files
had accumulated many generations of valid-but-superseded status prose. A fresh instance could obey
the nominal “read current first” rule and still ingest thousands of lines of older routes and
conclusions from the same control surface.

Nine effective orientation controls were cleaned. Their complete pre-cleanup forms—394,108 bytes
and 5,528 lines—are preserved in nine byte-identical snapshots under
`archive/startup_orientation_history_2026-08-05/`. The live surfaces now contain 62,760 bytes and
960 lines. No historical text was deleted from the repository.

## Live/archived split

- `LIVE.md` and `HANDOFF.md` retain their exact preregistered marked current blocks; all embedded
  prior layers moved to their full archived snapshots.
- `MEMORY.md` retains its exact current TOP and one archive pointer.
- `INDEX.md`, root `README.md`, and `research/README.md` are now concise navigation surfaces rather
  than chronological scientific ledgers.
- `AGENTS.md` retains the synchronization contract and every binding operational section. Its dated
  25-step science tour was replaced by a nine-step source-of-truth route plus a compact semantic
  regression guard required by the current premise verifier.
- `CLAUDE.md` retains all method text before `## Orientation` byte-for-byte. Its orientation section
  now points to current controls and carries no dated frontier or pinned test count.
- `research/_registry/README.md` retains its durable registry/migration semantics byte-for-byte and
  receives a lean current-source header.

The first compatibility replay rejected an over-aggressive draft because LIVE/HANDOFF used `.tsv`
shorthand rather than the exact `CURRENT_SCIENTIFIC_PREMISES.tsv` token, AGENTS had lost compact
semantic catch guards, and README had lost the current law-order pointer. Those items were restored
without restoring historical tours. This is evidence that the dependent guards remain effective.

## Compatibility exception

`UDT_SCIENTIFIC_FRONTIER_2026-07-19.md` remains byte-identical at root with SHA-256
`9128ddf72b32ef761295dcc6c370e7eb563ade8b34201c82f17989701887baef`. Many dated source inventories
and verifiers read its exact path and specific tokens. It is therefore classified
`IMMUTABLE_HISTORICAL_COMPATIBILITY_PATH`, removed from generic startup, and opened only when dated
evidence makes it load-bearing.

## Verification

- deterministic builder: 9 exact snapshots and 9 rebuilt controls;
- quarantine verifier: PASS; 9 snapshot hashes/sizes, exact retained fragments, current-authority
  hashes, current links, and protected dirt all pass;
- exercised quarantine catches: 6/6 (archive mutation, current-block mutation, duplicate marker,
  stale prior marker, July-19 frontier mutation, current-program mutation);
- current premise guard: PASS, 27 premise guards across 9 startup controls and 754 historical
  candidate dispositions;
- current law-order audit verifier: PASS, including all 16 semantic mutation catches;
- six frozen native-action manifests: 127 entries replayed; all 133 tracked package paths remain
  byte-identical to the R1H base;
- current artifact map: 1,114 unique identities and current paths (`1109 ROOT_RETAINED`,
  `1 MIGRATED_R1D`, `4 MIGRATED_R1F`);
- current frontier registry: 306 rows / 101 unique existing targets;
- tests: `70 passed, 1 xfailed`;
- protected unrelated work: 83 untracked paths, metadata-only SHA-256
  `131a923e58322166ab247d8f1d8216ca23c8c3119e9c22d126f1efeeb2d61c69`, unchanged and unread.

Machine evidence is in `VERIFICATION_RESULT.json`; `startup_dress_rehearsal.py` independently reads
only the bounded current route and must reproduce the open scientific state without historical
context.

## Four gates

1. Preregistered: yes, including the discovered research-navigation scope correction.
2. Full bounded scope: yes, all nine routed startup/orientation controls plus the historical
   compatibility exception.
3. Independently verified: yes, by the current premise/law-order consumers, frozen-manifest replay,
   test suite, and separate startup dress rehearsal in addition to the audit verifier.
4. Premises audited: yes; this task changes no premise or scientific claim.

## Maximum conclusion and authority boundary

The current startup path is bounded, reversible, and provenance-preserving. This audit does not
alter or strengthen any UDT result, authorize the proposed conormal-response derivation, reopen
repository reorganization, adopt a response/action/source/carrier, launch GPU work, or canonize
anything.
