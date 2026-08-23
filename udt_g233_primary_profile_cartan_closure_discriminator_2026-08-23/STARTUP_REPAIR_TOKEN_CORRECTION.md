# G233 startup repair — token-preservation correction

Date: 2026-08-23

The final-scope compression incorrectly replaced the individually guarded string
`G206/G207/G208/G209/G210` with a range, causing the premise verifier to stop at `G207`. `INDEX.md`
also remains one line over budget and the premise guide 23 words over.

Restore the individual G206--G210 identifiers in compact slash form, collapse one INDEX pointer
line, and shorten at least 24 non-load-bearing words in the premise table. No status or scope may
change. Then require the full root suite to pass.
