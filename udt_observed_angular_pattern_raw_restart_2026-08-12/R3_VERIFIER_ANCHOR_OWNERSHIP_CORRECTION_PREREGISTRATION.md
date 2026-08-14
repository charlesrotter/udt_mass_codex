# R3 verifier leave-one-anchor ownership correction preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_SECOND_GATE_FAILURE__IMPLEMENTATION_REPAIR_ONLY`

## Observed failure

After the separately registered central-curve verifier repair, the independent verifier completed
all manifest, central-component, exact central-curve reconstruction, covariance-identity, rank, and
194-cell support checks.  It then stopped in the eight full leave-one anchors.  No
`R3_VERIFICATION_RESULT.json` was written.

Six anchors passed.  The `CMASS/South` `NSIDE=4` and `NSIDE=16` anchors each rejected two bins when a
Corrfunc leave-one curve was compared directly with the saved TreeCorr leave-one curve using the
same extra `rtol=5e-9, atol=2e-10` curve gate removed from the central replay.

A bounded component-level diagnosis of those two anchors found:

- direct TreeCorr reproduces each saved TreeCorr delete-one curve to maximum absolute difference
  below `4.6e-15`;
- TreeCorr and Corrfunc integer DD, DR, and RR vectors are exactly equal;
- their weighted DD and DR components differ by at most `8.70e-10` and `2.37e-10` relative,
  respectively, while RR is exact;
- the resulting Corrfunc-versus-saved curve differences are about `1.28e-9` because accepted
  component roundoff is amplified when the combined curve is near zero.

No covariance value, eigenvalue, rank, angular feature, significance, or physical result was
printed or interpreted during this diagnosis.

## Frozen repair

The eight anchors remain exactly the preregistered sample/cap/resolution/deletion cases.  Before the
next verifier run:

1. independently rerun each deleted catalog through Corrfunc and through an unpatched TreeCorr
   calculation with the already verified discarded `30.00`--`30.25` degree guard bin;
2. require exact equality of all deleted DD, DR, and RR integer vectors between the engines;
3. apply the unchanged whole-component cross-engine gate to each deleted weighted vector: maximum
   relative difference `<=5e-9` or maximum absolute difference `<=1e-7`;
4. construct the direct TreeCorr leave-one curve and require it to reproduce the saved
   patch-decomposition leave-one curve with the verifier's default algebraic floating tolerance;
5. retain the Corrfunc-versus-saved curve residual as reported diagnostic provenance, not as a
   redundant pass/fail gate;
6. leave all anchor identities, catalogs, deletions, normalizations, output arrays, covariance
   checks, and repository tests unchanged.

This gives the anchor two explicit owners: Corrfunc independently checks the deleted pair
components, while direct TreeCorr checks that the saved patch subtraction produced the same curve
as physically deleting the objects and rerunning the primary R3 engine.

The repair changes no R3 scientific or statistical output and cannot promote the final result
beyond `VERIFIED-WITH-CAVEATS`.  Both post-failure verifier corrections must remain disclosed.

