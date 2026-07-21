# Fresh adversarial correction review request

The initial read-only review is preserved in `EXTERNAL_ADVERSARIAL_REVIEW.md`. It correctly found
that the delivered tensor algebra passed and identified under-tested transformation paths. Its one
blocking provenance finding was produced after the reviewer executed `git checkout grok` at the
pre-P01 tip `7476fe3`, which removed the already committed P01 preregistration from that worktree.
The preregistration actually exists in commit `c2264f9` and must be visible in this correction review.

Since the initial review, the package now includes:

1. a production local-Lorentz two-jet transformation with Lorentz-group value/first/second-jet
   validation;
2. metric-two-jet invariance, inhomogeneous spin-connection gauge transformation, and Cartan
   curvature covariance under a coordinate-dependent Lorentz boost;
3. independently predicted metric value/first/second jets, connection, and Riemann transformation
   under a nontrivial linear coordinate map;
4. an independent generic off-diagonal two-jet connection/curvature implementation;
5. independent exact symbolic `2+2` value/first/second-jet differentiation; and
6. expanded malformed, singular, signature, split-domain, CSN, and local-Lorentz catches.

Start afresh. Follow `ADVERSARIAL_REVIEW_REQUEST.md` in full, inspect the actual preregistration, and
independently determine whether the initial coverage caveats are now closed. Do not assume either the
initial `FAIL_BLOCKING` or the new `PASS` records are correct. Do not edit files.

End with exactly `PASS`, `PASS_WITH_CAVEATS`, or `FAIL_BLOCKING`.
