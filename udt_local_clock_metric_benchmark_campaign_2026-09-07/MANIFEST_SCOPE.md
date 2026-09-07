# Final return snapshot correspondence

MANIFEST.sha256 covers all intentional files in this campaign package plus
the final LIVE.md, HANDOFF.md and CURRENT_RESEARCH_PROGRAM.md status owners.
It includes initial candidates, source-first seals, objections, actual failed-
guard evidence, repaired runs, final reviews and the packaging fidelity record.
The immutable LC1 freeze remains unchanged and is nested, not regenerated.

Exclude MANIFEST.sha256 itself and the later manifest_verification.stdout,
manifest_verification.stderr and manifest_verification.json capture, to avoid
self-referential hashes. Interpreter caches (__pycache__ and .pyc files) are
not evidence and are excluded if present. No protected or unrelated payload
is enumerated by this manifest, and no external cache/source PDF is attached.
Primary source bytes have their separate INPUTS/review hashes and provenance.

Paths are repository-root relative. Verify from that root with
`sha256sum --check --quiet udt_local_clock_metric_benchmark_campaign_2026-09-07/MANIFEST.sha256`.
The saved verification capture authenticates this final snapshot; later
authorized edits to current status owners require comparison at this commit,
not rewriting historical source evidence or inferring a scientific failure.
Git history supplies rollback/chronology. A checksum or commit does not confer
truth, independent review, source blindness, experimental eligibility, physical
adoption, an accepted scientific grade or canon.
