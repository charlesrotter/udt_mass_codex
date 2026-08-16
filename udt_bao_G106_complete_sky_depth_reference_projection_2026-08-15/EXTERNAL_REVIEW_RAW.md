# G106 external-review response — intake-path-normalized record

The substantive response is preserved below. Repetitive absolute links into the ephemeral sealed
intake were normalized to repository-relative evidence names; the verdict, claims, caveats, and
numerical statements are unchanged.

**Verdict**

`PASS_WITH_CAVEATS`

Strongest valid landing:
```text
COMPLETE_SKY_DEPTH_REFERENCE_PROJECTOR_DERIVED_CONDITIONALLY
__PURE_RADIAL_MODULATION_REMOVED
__DEPTH_DEPENDENT_ANGULAR_RESPONSE_SURVIVES
__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED
__PHYSICAL_HISTORY_AND_OUTCOMES_OPEN
```

**Evidence**

- I independently recomputed the byte count and `SHA-256` for every payload listed in `REVIEW_SCOPE.json`. All `29/29` entries matched exactly.
- The covariant Jacobian claim is correctly stated on the declared regular finite-to-one class: `EXACT_DERIVATION.md` defines the pullback metric `M_AB`, gives `J_Psi=sqrt(det M/det gamma)`, gives the coordinate-change argument, and gives the finite-to-one density formula. The upstream local construction is consistent with G105.
- `R_s p = p_zeta s` is genuinely a positive, mass-preserving, idempotent projection if `s >= 0` and `integral s=1`; the derivation gives its range, kernel, and direct-sum decomposition.
- The supplied official-reference semantics justify that operator only as an idealized per-stratum reference model. The record states angular randoms follow footprint/completeness and random `Z` values are drawn from observed galaxy redshifts, while explicitly keeping finite-catalog factorization, shot noise, `FKP`, and `NZ` out of scope.
- Pure radial modulation is removed and zero-angular-mean depth-angle structure survives exactly within that reference class. The multimode formula turns this into a cross-window quadratic constraint.
- The full-sky witness checks out: positivity and normalization, `13/108, 1/108, 13/108` window means, the `P2(c)/5` identity, and pair-amplitude ratio `169`.
- There is no hidden promotion from G105's local all-sector witness to a selected global complete history. G106 explicitly says the opposite, and the premise ledger marks one-history across windows as only a working falsifiable hypothesis.
- I replayed all four executables under `UDT_READ_ONLY_REPLAY=1`. All exited `0`, and each printed JSON matched its sealed artifact exactly: `derive_sky_depth_projection.py -> DERIVATION_RESULT.json`, `verify_sky_depth_independent.py -> INDEPENDENT_VERIFICATION.json`, `run_catch_proofs.py -> CATCH_PROOF_RESULT.json`, and `verify_package.py -> VERIFICATION_RESULT.json`.

**Caveats**

- The operator semantics rely on a sealed prose summary of external SDSS documentation, not archival primary excerpts inside this intake, so the product form is justified here as a typed idealization rather than a proved exact property of the finite published random catalogs.
- The general Jacobian and finite-to-one theorems are argued in the derivation text; the executables validate exact witnesses and package consistency, not arbitrary-map theorem proving.
- `__ONE_HISTORY_CROSS_WINDOW_TEST_DEFINED` is supported as a falsifiable joint constraint, not as proof that one physical complete history has been selected or even shown to exist in the real survey arena.

**Smallest Next Gate**

Gate 4: final premise-verifier and startup-suite rerun before banking.
