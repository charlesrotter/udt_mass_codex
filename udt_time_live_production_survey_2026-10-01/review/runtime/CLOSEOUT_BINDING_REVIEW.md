# Runtime attestation closeout binding review

The final attestation remains my actual **ACCEPT_WITH_LIMITS** review of the
first-dataset/launch checkpoint:
`eff2caed73a2d3e849f30c2427b65ee2597a4fe34347397359241de10aa4235d`.
This is the same actual reviewer context, `/root/survey_runtime`, explaining and
checking its own metadata repair. It is not another independent scientific review.

I caused the binding mismatch. I first wrote FINAL_ATTESTATION.json with hash
`182d3798cef7537acc36ba7e393e2a27991c062f2d04b3806b36ecb6660d9724`.
I then edited three prose fields for readable spacing and wording before sending
the final acceptance message and final hash to the parent. The parent had already
captured the first hash. Those fields were `exposure`, `limits`, and
`verification.final_additional_text_review`. The review verdict and scope did not
change. Publishing the file before its prose was settled created an avoidable
race between the artifact and its parent binding.

I did not preserve a separate original file before overwriting that first edition.
The recorded tool calls retain the exact replaced strings. During this closeout
review I reconstructed the initial JSON using those strings and the unchanged
final fields. The reconstructed bytes exactly match the previously recorded
`182d3798…` SHA-256. They are saved as
`closeout_binding/INITIAL_ATTESTATION_RECONSTRUCTED.json`, with provenance in
`closeout_binding/RECONSTRUCTION_RECORD.json`. This is a reconstruction made now,
not a claim that the initial file had been separately preserved or that a checksum
establishes chronology. No missing initial byte content remains after the exact
hash match; the original preservation failure remains part of the history.

Direct comparison shows the 7,707-path accepted map, verdict, freeze hash, report
hash, review-output hashes and every numerical verification field are identical
between editions. Only the three identified prose fields differ. The current
final attestation still matches the common freeze's accepted map and remains at
the final announced hash. No frozen source, report or current final-attestation
byte was changed during this repair. No scientific computation was repeated or
regraded for this metadata-only defect.

The appropriate closure repair is to preserve the initial parent record and failed
full406 audit, bind the parent record to the announced final attestation, and rerun
the required closure checks. Parent reports that preservation and rebinding are
underway; their actual files and rerun receipts own those claims. This closeout
review does not assert that the new full audit, staging, commit or push has passed.
Whole-survey results and automatic candidate outputs remain outside the reviewed
launch checkpoint.
