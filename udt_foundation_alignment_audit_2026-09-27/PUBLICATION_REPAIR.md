# Publication packaging repair

The first local checkpoint is `7e4f21509bb876b6e6618614eeec2cb8c59a10b5`.
It was not pushed before the following checks were resolved.

A staging assertion expected 57 files and failed: only 56 had staged. The exact
missing file was the empty `checks/PATCH_CHECK_FINAL.stdout`, ignored by the
repository's `.gitignore:38` rule `*.stdout`. The on-disk manifest check had passed
because the file existed locally, but the committed tree would have lacked it.
The parent's multi-call tool script continued to the local commit despite that
failure. That was an orchestration mistake; the failed gate is retained rather
than represented as passing. The repair explicitly stages this authorized empty
receipt and verifies the Git-staged tree, not just local file existence.

The same batch's raw `git diff --cached --check` exited 2. A repeat against the
first commit is retained in `checks/RAW_PUBLICATION_WHITESPACE_CHECK.txt`. Its
warnings concern frozen patch context-space lines and TSV serialization (CRLF
and trailing empty columns). These bytes are preserved: deleting patch context
or TSV separators to silence a text-style check would damage or alter evidence.
An intermediate `core.whitespace=cr-at-eol` check still flagged legitimate empty
TSV fields. The format-aware check verifies those categories separately and
retains the raw failure; it does not claim that the raw check passed.

No reviewed candidate, scientific source, registry field, reviewer verdict, initial
freeze, or outside local file is changed by the packaging repair. The additive
repair commit also retains this record and the diagnostic output. Source and
candidate hashes remain the previously reviewed hashes. Final publication must
verify every manifest entry from the committed Git blobs and the exact package
membership before pushing.
