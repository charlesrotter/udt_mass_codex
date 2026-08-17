# G130 repair adjudication

Date: 2026-08-16

All seven fresh-review repairs were accepted and implemented.

1. The exact countermodel now uses `s=1/4` and `s=4`, corresponding to nonzero depths
   `+log(2)` and `-log(2)`. Production and independent curvature routes return `3/2` and `-6` at
   `r=1`.
2. Reports and the landing now say that co-presence denotes event co-membership conditional on a
   supplied solution `S`; it does not own or construct that solution.
3. Representation equivalence is explicitly typed as `(A_a,h_a,overlap data) <-> g` on a smooth
   regular covered region. Reciprocal scalar depths alone are declared insufficient.
4. The production reconstruction check now evaluates a fixed rational ten-component metric,
   solves for separate unknowns, and verifies the exact left inverse
   `(M^T M)^-1 M^T M = I_10`.
5. Both countermodel metrics are checked directly to have one negative and three positive diagonal
   entries at the exact witness point.
6. The source guard requires exactly the nine preregistered unique paths and their SHA-256 hashes;
   phrase checks are labelled lexical anchors rather than source ownership proofs.
7. The package verifier copies the package and exact manifest sources into a fresh temporary root,
   reruns both implementations, and demands byte identity with the banked outputs.

The committed preregistration was not rewritten. Its strengthened execution witness is recorded in
`PREREGISTRATION_EXECUTION_NOTE.md`.
