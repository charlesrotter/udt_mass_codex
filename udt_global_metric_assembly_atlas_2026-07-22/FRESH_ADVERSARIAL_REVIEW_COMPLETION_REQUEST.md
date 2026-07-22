# Fresh adversarial-review completion request

Date: 2026-07-22

Complete the fresh audit requested in `FRESH_ADVERSARIAL_REVIEW_REQUEST.md` after reading the full
preserved `FRESH_ADVERSARIAL_REVIEW_TRANSCRIPT.txt` from the interrupted first reviewer.

The first reviewer reproduced the package verifier, source manifests, raw counts, candidate
provenance, and selector limits. It found two concrete defects:

1. exact monodromy `-I` was classified with trace-minus-two parabolics rather than finite elliptic;
2. the CSN selector rows cite an unpinned dispatch even though the already frozen
   `angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md` contains the required consequence.

It also began an optional post-outcome DOP853 replay of all 83 anchors. Thirty passed before one
anchor became disproportionately slow; the optional expansion was terminated. The required three
preregistered independent anchors had already passed. Do not rerun the all-83 expansion and do not
treat its interruption as evidence either for or against the registered result.

Return `PASS`, `PASS-WITH-CAVEATS`, or `FAIL` for the draft package. State whether the two defects
require correction, whether the conservative global-nonselection and Stage-6/7 stops survive, and
the strongest honest maximum. Do not edit evidence or inspect the original dirty checkout.
