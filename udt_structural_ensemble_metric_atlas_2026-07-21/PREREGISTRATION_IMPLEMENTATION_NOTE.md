# Pre-outcome implementation note — raw-ledger sharding

Date: 2026-07-21

The committed preregistration requires a complete raw JSONL ledger for 6,144 configurations. The
parent raw records average approximately 28.7 KB, so one combined file would be about 176 MB and
would exceed the safe GitHub per-file size.

Before any ensemble geometry is evaluated, freeze this storage-only refinement:

- write exactly eight JSONL shards, one for each registered bank/point context;
- name them `RAW_CONFIGURATION_JETS_<bank>_<point>.jsonl`;
- require exactly `48*16 = 768` records in every shard and 6,144 in their union;
- add `RAW_SHARD_REGISTRY.tsv` with context, path, row count, byte count, and SHA-256;
- require disjoint configuration identities and complete union coverage; and
- independently replay every raw identity and shard hash.

Record order remains carrier, mask within each context. No configuration, payload, precision,
interaction, check, or maximum conclusion changes. “Complete raw JSONL” in the preregistration means
this exact eight-shard union.

