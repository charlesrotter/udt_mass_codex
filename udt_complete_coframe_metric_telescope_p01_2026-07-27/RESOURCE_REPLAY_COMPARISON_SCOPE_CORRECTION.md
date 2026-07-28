# Resource-replay comparison scope correction

Status: `CORRECTION AFTER FAILED VERIFIER; BEFORE FORMAL RESOURCE VERDICT`

`RESOURCE_REPLAY_VERIFICATION.json` is preserved as the result of the first,
fail-closed replay verifier.  It correctly rejected the replay, but its
continuous comparison included transport values already classified
`transport_numerically_unresolved`.  Requiring unstable values to reproduce is
inconsistent with the preregistered rule that unresolved transport is retained
and not promoted.

The corrected verifier does not weaken any resolved-data tolerance.  It
requires:

- exact coefficients, names, shapes, and local features for all 1,024 rows in
  every shell;
- an exact transport-resolution mask;
- exact finite class and exact nontrivial-holonomy class on rows resolved in
  both runs;
- scaled continuous transport disagreement at most `2e-10` on those resolved
  rows; and
- replay peak memory below 6 GiB.

Unresolved transport values remain present in both raw packages but are not
asked to agree numerically.  Their count and identities must agree exactly.
The original failed verifier, its output, and both raw runs remain unchanged.

