# Pre-freeze dependency pin finalization — original failure retained

HB2 mathematical review was read in full at intake, hash4982cb33. The reviewer
subsequently appended only a return-HEAD/status paragraph before exiting0.
Its final whole-record hash is
`fbcef93d482f6b7546f4ecd450b52c2f88e66877a1035f6258a6bbab40122c81`.
The parent read that paragraph, removed it in memory, and verified EXACT
reconstruction of the original4982cb33 bytes. They are preserved in
step_02/REVIEW_RECORD_INTAKE_SNAPSHOT.md. The science, verdict and caveats did
not change; the reviewer final record itself was NOT edited by the parent.

HB3's first checker invocation17:11:07 exited1 at the dependency-hash gate,
before its algebra ran,0.1634822729974985s/54084KiB. It remains NOT_PASS in
author_check_initial.json/.stdout/.stderr. Original checker bytes are retained
as check_orbits_initial_pin.py, SHA-256
`98abed2731055dbeb7b9baef98fe2a02e1f89827520b42205af2a78af852dd5d`.
The live checker changes only the pinned review hash to the final record;
its first complete calculation has a separate output stem. This is a disclosed
pre-freeze provenance correction, not a mathematical candidate repair or a
waived source failure. Original failure and interim/final review history survive.

The HB3 question records the exact intake version read. Final candidate freeze
and downstream use refer to the final review including its status-only append.

The first multi-file patch attempt was rejected atomically because of an
unmatched unrelated context line. A premature second invocation under stem
author_check_complete therefore hit the SAME unchanged hash assertion and
exited1 at17:12:41,0.16043165398878045s/54140KiB. That failed receipt is also
preserved, not a completed calculation despite its chosen stem. The actual
one-line pin edit was then applied alone and verified before the final-pin run.

The parent also refreshed the single review-reference line of
step_02/REVIEWED_RESULT.md to cite the final whole review, after HB3's source
intake but before the HB3 candidate freeze. Its previous hash
`17471b521f6ba9347d7a6a58bc54fcf36b045c3eaface8d88f498d74b4919b28`
is exactly reconstructed by reversing that one reference-line substitution
from current hash
`414e8c42dd5b0cf7b7bc478f801fe822645c66e712dccec988f06dbffb218fbe`.
The old hash matches the HB3 reviewer's sealed SOURCE_AUTHENTICATION.json.
The mathematical wrapper text and conclusion are unchanged. HB2's later
109-payload seal includes the final wrapper; nothing in that seal was edited.
