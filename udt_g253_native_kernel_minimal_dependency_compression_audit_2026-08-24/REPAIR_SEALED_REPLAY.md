# G253 sealed repair replay

Date: 2026-08-24

First post-repair sealed intake:

- path: `/tmp/udt_g253_review_mjtlwrd8`
- file count including scope: 50
- `REVIEW_SCOPE.json` SHA-256:
  `3cbdc9e9acfb1b63617235e12d6eddc137dd2d7e99440563ddc71eee793b59a1`

All four registered commands were run from the intake root and exited zero:

| Replay | Result |
|---|---|
| production `--no-write` | unchanged 17 nodes, 12 edges, 3 graphs, 21,510 assertions |
| independent `--no-write` | unchanged 12,000 trials, 49,602 assertions |
| hostile `--no-write` | 23/23 caught plus 2 positive layout controls |
| package verifier | `PACKAGE_PASS`; all three stored results match |

The only result-count change from the original package is the preregistered hostile count increase
from 20 to 23 for missing, mismatched, and conflicting dual-layout sources. No scientific output
changed.

This file records the first repaired sealed replay. Because adding the record changes the payload,
the external follow-up must use a subsequently rebuilt fresh seal and independently repeat the same
registered commands.
