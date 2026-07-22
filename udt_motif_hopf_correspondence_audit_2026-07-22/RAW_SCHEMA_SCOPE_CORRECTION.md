# Raw-schema scope correction

Date: 2026-07-22

The immutable production ledgers and `ATLAS_RESULT.json` retain the historical schema field
`stable_projector_path`. In that schema, `YES` means only:

1. all 17 registered nodes were numerically classified;
2. all 17 nodes had the same motif label; and
3. each adjacent sampled pair admitted a minimum-distance projector assignment.

It does not mean a continuous stable projector bundle. Current derived navigation uses
`sampled_all_node_match_17_nodes`; `REVIEW_CORRECTION_RESULT.json` is the authoritative scope
overlay and records `17_NODE_SAMPLED_MATCH_NOT_CONTINUOUS_BUNDLE_THEOREM`.

The raw ledgers are not rewritten because their bytes are the exact inputs independently replayed
and adversarially reviewed.

