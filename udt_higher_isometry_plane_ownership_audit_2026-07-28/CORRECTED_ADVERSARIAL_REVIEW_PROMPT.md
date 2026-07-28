# Corrected adversarial review dispatch

Perform a fresh read-only adversarial review of the correction layer in
`udt_higher_isometry_plane_ownership_audit_2026-07-28`.

The initial hosted review is preserved in `FRESH_ADVERSARIAL_REVIEW.md` and returned `REFUTED`
because a family-wide formal-jet identity was promoted to generic fixed-metric uniqueness. Do not
re-litigate that refuted claim as if it were still asserted. Determine whether the corrected
package now records the strongest supportable bounded conclusion without hiding the failure.

Required checks:

1. Confirm the initial refuted artifacts and review remain byte-identical to the hashes in
   `CORRECTION_LAYER.md`.
2. Rerun production and independent implementations from a temporary directory and compare raw
   hashes with `RUN_ENVIRONMENT.json`.
3. Verify that the corrected result distinguishes:
   - family-wide coefficientwise identity robustness;
   - fixed cohomogeneity-one profile constancy;
   - universal selection;
   - full-orbit response versus restricted plane response.
4. Reject any surviving claim that the identity calculation proves generic fixed-metric
   uniqueness. Confirm the verifier exercises mutations that reintroduce that promotion.
5. Confirm R01/R02 and `D3` are scoped to principal orbits `b>0`, with cap limits not silently
   treated as invertible orbit Gram matrices.
6. Confirm the exact smooth nonconstant-depth double-plane countercontrol and the exactly-two-free-
   circle toric theorem remain valid and support bounded universal nonselection.
7. Confirm the incomplete response degeneracy atlas is openly recorded and that the Berger/round
   illustration rows have no load-bearing status.
8. Check that no physical branch, macro/micro assignment, carrier, action, source, density,
   bootstrap law, dynamics, or mass emergence is claimed.
9. Audit `verify_audit.py` for circularity and run every read-only check possible. It is expected to
   stop only at the absence of your output file while you are reviewing.

Your first output line must be exactly one of:

```text
PASS
PASS_WITH_CAVEATS
REFUTED
```

Then give concise findings, exact replay hashes/counts, any remaining caveat, and the maximum
supportable conclusion. Do not edit repository files. Do not update controls, run GPU work, or
continue the science. Your output will be captured directly as `CORRECTED_ADVERSARIAL_REVIEW.md`.
