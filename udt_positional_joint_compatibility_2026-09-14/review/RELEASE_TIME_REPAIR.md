# Documentary repair: scientific-slot release timestamp

The parent identified a precision mismatch after accepting the scoped scientific
review. The original RECORD and FINAL_REVIEW stated release at 00:20:32 UTC.
That was the whole-second tool clock accompanying the release message, not a
recorded exact message instant.

The final scientific capture parent_replay.json started at
2026-09-14T00:20:32.435681+00:00 and measured 0.3114963830448687 seconds. Adding
those metadata values places capture completion at 00:20:32.747177383 UTC to
nanosecond display precision. This is a metadata-derived completion timestamp,
not a separately sampled wall clock. The release message was issued after the
capture tool returned. Its exact fractional-second timestamp is unavailable.
The parent confirms it performed no overlapping scientific computation.

Original RECORD.json, FINAL_REVIEW.md and SHA256SUMS bytes are preserved under
release_time_repair_original/. The current RECORD replaces the ambiguous exact
release field with explicit coarse-clock, ordering and final-capture fields.
FINAL_REVIEW now makes that distinction in prose. The review manifest is refreshed.

No scientific check was rerun, no argument or verdict changed, and all seven
reviewed candidate/maintained document hashes remain unchanged. The original
scientific-review completion remains 00:24:49.396256 UTC. The documentary repair's
final completion clock and total elapsed allocation appear separately in RECORD.
This repair falls inside the original 00:45:32 UTC review deadline.
