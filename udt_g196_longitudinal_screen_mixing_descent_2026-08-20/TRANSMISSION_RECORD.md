# G196 external-review transmission record

Date: 2026-08-21

Charles authorized transmission of the sealed 31-file intake
`/tmp/udt_g196_review_r1wy9u41`, defined by `REVIEW_SCOPE.json` SHA-256
`364e202405ef5abc55c1b355b2e234485e92500ab15c8a2a804422aed6433ef4`, to the
external Codex reviewer (`gpt-5.4`) for read-only adversarial review.

The successful reviewer session was `01a0241f-438f-7f80-8c59-f2699bf0bb61`. It inspected only the
sealed intake, did not edit evidence, and did not continue the research. The post-review digest
check found zero changes across all declared payloads.

The registered package replay and a fallback package replay both reached the same environmental
failure before the Torch/SciPy verifier ran: Torch's optional `dill` import asked Python for a
writable temporary directory, while the review sandbox was strictly read-only. This was not a
scientific assertion failure. Under the authorized bounded-read-only fallback, the reviewer then
ran:

- the direct no-write SymPy production derivation: 17/17 assertions passed;
- the no-write hostile-mutation proof: 9/9 catches passed;
- the no-write source-manifest verifier: 8/8 rows passed.

The external final has SHA-256
`dd786c57e7bb0448a3d6110a54a29f648491f227c375a807357240c1fe741cbb`. The successful plain-text
transcript had SHA-256
`6273ec95aae6ab0184a62f6b5a4d4b61a7d744a217e3f243bcfb75d52fe514ce`; its banked deterministic
gzip has SHA-256 `e42704d2d27727bf74a0686f4f303933a5f0a57fa0c59a7aa3590b5ab060b404`.

An earlier launch attempt failed before transmission because the current CLI rejected a retired
approval flag. It carried no scientific evidence and is not the preserved review transcript.

## Repair-only follow-up

Charles subsequently authorized the sealed 39-file intake `/tmp/udt_g196_review_myxg_x_1`, defined
by `REVIEW_SCOPE.json` SHA-256
`83f33f919c2dcf45655dfb1b1e5068329e5a6f264c9da8c5a0ac02c4951f84ad`, for repair-only read-only
follow-up. Reviewer session `01a0248a-02df-7d21-a72b-e951765ccad5` ran the exact registered replay
in the strict read-only sandbox. It exited zero in `1336.947` seconds; 38/38 declared hashes matched
before and after and `.review_runtime` had zero entries.

The repair follow-up final has SHA-256
`92beceef7c0a8d568e7e61de4a137b8ec375198aea699b1febb7c0a929fc2e8d`. The successful plain-text
transcript had SHA-256
`91530a0483d7b3275bdaaa9fbd2751071e131140a66628f20aeecbeb64dd0782`; its banked deterministic gzip
has SHA-256 `2d8c20c2862352793284d24b43b86afe487da16d5e493454c42aae4ef14d41c3`.
