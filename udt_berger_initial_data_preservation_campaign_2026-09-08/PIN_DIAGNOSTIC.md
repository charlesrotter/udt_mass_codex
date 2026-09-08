# Pre-review operational pin diagnostic

The first SOURCE_SHA256SUMS had a hand-transcription defect in run_capture.py's
hash. Initial malformed bytes are preserved separately. Command
`sha256sum -c udt_berger_initial_data_preservation_campaign_2026-09-08/SOURCE_SHA256SUMS`
returned exit0 and printed18 OK lines BUT stderr warned
`sha256sum: WARNING: 1 line is improperly formatted`.
This was NOT a complete source-authentication pass. No science depended on
that omitted check; the wrapper had been read and its actual hash computed.
A first exact-line patch failed verification without changing files; the next
patch used the actual line. Strict length/count/hash authentication follows.
This is packaging history, not a source change or scientific repair.
