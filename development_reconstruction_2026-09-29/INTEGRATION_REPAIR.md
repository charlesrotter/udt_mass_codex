# Integration repair round2 — source-preserving maintenance fixes

Initial integration bytes are retained under integration_initial/ with their
original freeze. Both independent integration critiques remain unchanged. The
mathematical body and all original source files are unchanged in this repair.

I1: Actual report_path/report_sha256 is now checked for each accepted reviewer
attestation. The earlier implementation pinned attestations but could accept
changed report bytes; both reviewers reproduced that false pass. The new test
modifies report text and verifies rejection. Metadata is still not proof that
review actually happened; the two real contexts/reports supply that evidence.

I2: R4→R5 proof, R4→R6 context and conservative D1→R1…R17 meaning-use links
close the recorded missing impacts. R5 uses h=C^T h_s C with C=diag(1,m),
not scalar multiplication. The G176 change now flags downstream reconstruction
and matched-clock uses. SOURCE_CORRECTIONS is pinned as a source for R9, so a
changed correction flags the same positive and negative response descendants.
New tests exercise both actual source changes and owner-meaning impact.

I3: G353–366, G374–375 and G395–401 ledger routes also name R18, where their
retained gains/omissions are actually summarized. W5/W6 also name D1 for explicit
definitions. No reconstruction depth or registry grade is upgraded.

I4: Seven original DCR1/FSR1/PJC1 review/repair files are pinned as typed
review_support, distinct from proof inputs. A support change flags the relevant
central review, including descendants; it does not derive a theorem or become
an accepted physical premise. The test exercises a changed historical review.

The repaired suite has24 tests and passed under the existing60s/512MiB limit.
Initial19-test outputs and reviewer counterexamples remain preserved. Strict
normal startup still requires actual accepted integration attestations; the
--draft construction check cannot satisfy it. Full after-audit remains pending.
