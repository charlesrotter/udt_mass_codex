# G296 external adversarial review

Date: 2026-08-29

## Verdict

```text
G296_ACCEPT_WITH_REPAIRS
```

## Findings

1. The preregistration chronology is asserted but not independently verifiable from the sealed
   intake. `AUDIT_REPORT.md`, `EVIDENCE_GATES.md`, and `REVIEW_SCOPE.json` claim commit `f7a050f0`
   precedes implementations and outcomes, but the intake contains neither Git history nor a sealed
   ancestry artifact. Add a sealed ancestry/provenance artifact or downgrade the claim.

2. The registered replay is not fully reproducible in the isolated review environment.
   `derive_native_residual_order_map.py` imports unavailable `sympy`, so `verify_package.py` fails.
   `COMMANDS.md` also registers the repository premise verifier and test suite, neither of which is
   sealed. Include the replay assets and a dependency-free production fallback, or restrict the
   sealed command list and declare the dependency.

3. The scalar-language slightly exceeds the sealed proof. The Brinkmann witness directly tests
   scalar curvature, Ricci square, and Kretschmann scalar. It supports rejection of that tested
   scalar-only lane and demonstrates that nonscalar curvature carries information, but does not by
   itself classify every conceivable scalar construction. Narrow the wording or supply a broader
   theorem.

## Results retained by the reviewer

- All 37 intake-manifest entries and all 16 source-manifest rows hash-check exactly.
- The independent replay reproduced `INDEPENDENT_VERIFICATION.json` byte-for-byte: 3,080 exact
  assertions across 128 nonzero rational trace-free screen waves.
- The hostile replay reproduced `CATCH_PROOF_RESULT.json` byte-for-byte: 13 of 13 caught.
- The complete-coframe `16-6=10` count and source-owned rank-ten completed-network claim are
  consistent with the sealed evidence, including the required ruler-density and screen channels.
- No concrete mathematical refutation was found for the local order boundary: pointwise order-zero
  metric data are nonselective up to frame, first metric derivatives are removable in normal
  coordinates, and curvature is the first local metric-natural nonidentity home.
- An independent rational spot-check confirmed the Brinkmann convention and identities
  `R_uiuj=T_ij`, `Ric_uu=tr(T)`, and, for nonzero trace-free `T`, nonzero Riemann curvature with zero
  Ricci, Einstein tensor, scalar curvature, Ricci square, and Kretschmann scalar.
- The G286 characteristic-data correction and conditional G259 boundary were retained.
- The phrase “minimal faithful primitive state” was accepted within its explicit bounds: it does
  not claim unique variables, fewest equations, or derived dynamics.

## Scientific effect

No scientific landing was rejected. The required work is two evidence-packaging repairs and one
scope-wording repair. Until those repairs are independently checked, G296 remains unbanked.
