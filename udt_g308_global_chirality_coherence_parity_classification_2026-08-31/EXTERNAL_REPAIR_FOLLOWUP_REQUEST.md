# G308 repair-only external follow-up request

Review only the sealed intake. Verify only preregistered repairs R1--R4 and whether the bounded
scientific landing remained unchanged. Do not continue the research.

## Required checks

1. Run every registered standard-library replay in a writable ephemeral copy. Confirm that
   `verify_package.py` passes directly in the sealed `frozen_sources/` layout without symlinks or
   manual source staging.
2. Inspect the repaired resolver. Confirm that repository-only and sealed-only layouts resolve
   uniquely and that missing and ambiguous layouts are rejected.
3. Independently inspect the new Hodge/group-orbit verifier. Confirm that it imports no production
   code, does not use the production outer-product candidate construction, and genuinely tests the
   same load-bearing globality, chirality, parity, pair-reversal, connectedness, time-carry,
   geodesic-typing, causal, and ownership claims by a distinct method.
4. Confirm that the old 79,200-check verifier is now described only as a constructive randomized
   cross-check and that the 121,600-check Hodge/group-orbit implementation carries the independent
   gate.
5. Confirm byte-stable production, constructive randomized, hostile, and census outcomes, and
   verify that the exact landing, metric, reciprocal kernel, and physical-population boundary did
   not change.

## Required verdict

Lead with one exact token:

- `G308_REPAIRS_ACCEPTED`
- `G308_REPAIRS_INCOMPLETE`
- `G308_REPAIR_SCIENTIFIC_REGRESSION`
- `G308_REPAIR_UNCLASSIFIED`

List findings by severity and report every command run. Do not edit evidence files or continue the
research beyond this repair-only adjudication.
