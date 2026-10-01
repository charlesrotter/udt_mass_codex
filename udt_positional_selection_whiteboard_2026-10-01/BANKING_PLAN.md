# PSW1 compact evidence banking

Stage only this package's explicit allowlist and the seven reviewed central files:
UDT_DEVELOPMENT.md, CURRENT_RESEARCH_PROGRAM.md, LIVE.md, HANDOFF.md,
development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json,
development_reconstruction_2026-09-29/RECENT_DISPOSITIONS.tsv and REVIEW_RECORD.json
in that same directory. CANON and the exact registry remain unchanged.

The package contains fixed notes/candidates/repair, source hashes, three small
check implementations and captures, actual review reports/attestations, the
prior review record, common integration freeze, descendant/decision/work records,
final repository check receipts and a SHA-256 manifest. Retain stdout explicitly
despite the generic ignore rule. No raw TPS1 field, protected payload, pycache,
temporary helper, new dependency or unrelated untracked path belongs here.

INTEGRATION_FREEZE.json binds the proposed accepted file map; final reports and
attestations are excluded from that map to avoid recursion and are bound through
the parent REVIEW_RECORD.json. Later check receipts and SHA256_MANIFEST.tsv are
also outside their own recursive binding. The manifest binds compact final
files and central edits; staging must use those exact paths and compare every
staged blob to the recorded SHA before committing. The manifest itself is staged
and its path must be explicit in the staging list.

The new package ceiling is64MiB. Inherited accepted files retain old hashes
except the six central/adapter/graph/disposition changes directly reviewed here;
the seventh edit is the parent final-review record, bound after actual completed
attestations. No old accepted source is dropped to make verification pass.
Preserve all76 pre-existing untracked names recorded in SNAPSHOT.json without
reading protected bytes. Commit one evidence change and push synchronized grok.
Saving does not adopt the response proposal or promote a scientific grade.
