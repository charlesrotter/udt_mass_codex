# Cold-review attempt log

The scientific criteria were unchanged across attempts.

1. The first CLI invocation used obsolete approval syntax and failed before model execution. Its
   raw terminal record is `COLD_REVIEW_ATTEMPT1_TRANSCRIPT.txt`.
2. The first repository-root cold run obeyed the full startup and exhausted its output budget before
   reaching the frozen source packet. Its incomplete record is `COLD_REVIEW_TRANSCRIPT.txt`.
3. Two isolated full/targeted-source attempts were externally authorized but hit the review
   harness output ceiling while printing evidence. They produced no verdict and changed no
   repository file.
4. The successful pass used a tool-free 398-line input assembled from exact line-numbered excerpts
   of all 20 hash-frozen sources, both generated tables, the next-step paragraph, and mechanical
   results. It returned the verdict preserved in `COLD_REVIEW.md`.
5. A separate tool-free closure pass received only the prior mandatory repair and the repaired
   technical and lay wording. It returned `CLOSED-PASS`; its exact return is preserved in
   `COLD_REVIEW_CLOSURE.md`.

The final input did not substitute a summary source for the frozen sources: its excerpts retained
original paths and line numbers; all full-source identities had already passed the local verifier.
