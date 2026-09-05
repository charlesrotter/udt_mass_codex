# G349 external-caveat repair execution record

Date: 2026-09-04
Repair preregistration commit: `c2967132`

## Frozen defect

The sealed proof incorrectly treated ordinary endpoint-map rank two as equivalent to transverse
screen rank two. The external mixed caustic/cut counterexample showed an ordinary-rank-two null
plane with transverse rank one and zero Lorentzian two-area.

## Implemented repair

- The derivation now separates `r_F=rank(dF)` from quotient-screen rank `r_s`.
- `J_gF` is the nonnegative semidefinite Lorentzian Gram density, positive exactly for `r_s=2`.
- The auxiliary weight is nonnegative, vanishing on null ordinary-rank-two planes.
- Multiplicity is `N_s`, counting transversely regular spacelike preimages.
- Ordinary-critical and screen-critical strata are stated separately and all remain in the map.
- `CURRENT_RESEARCH_PROGRAM.md` now says geometric endpoint image-union area, not physical area.

## Fresh executions

The repaired production route passed `44321/44321`; the implementation-distinct route passed
`14321/14321`; and the hostile route caught `22/22` mutations. Both numerical routes explicitly
reconstruct the mixed stratum. The production route uses a weighted auxiliary metric; the
independent route uses different longitudinal Jacobi pieces, Euclidean auxiliary area, and Gaussian
elimination for both ranks. No tolerance was loosened.

Repaired script SHA-256 values:

```text
bdc85395a5c832077667f6c8a1e323514fd8b52af15ac1cbb7a2de696e5f6e5c  derive_finite_null_patch_area.py
246a6552cdfcd442739f2fe6d93fe03b0b2361829e5801414fca76693f9167c9  verify_finite_null_patch_area_independent.py
3d1f0727c8b426661c8553e68cada59ed3b9b1dfc4c3c97a4412f29c99a14287  run_catch_proofs.py
```

The first repaired aggregate replay failed before scoring because the production serializer did
not emit the historical `preregistration_commit` and `repair_commit` fields expected by the
aggregate. This packaging defect was recorded before correction. The verifier was retained; the
producer was repaired to emit the two already established identifiers. Final repaired script
hashes are recorded after that correction below.

The second aggregate replay scored `20/21`: all mathematical and scope gates passed, but a wording
hook spanned a Markdown line break. It was aligned to the unchanged statement that injectivity is
stronger than necessary. No equation, evidence, tolerance, or conclusion changed.

The original preregistration and original script hashes remain in Git history at `84cb5264`; the
first hostile wording repair remains at `134ecd4a`; and the external finding remains byte-exact in
`EXTERNAL_REVIEW_RESPONSE.md`. Corrected aggregate, repository, premise, and external repair-only
follow-up gates remained pending at this record's creation. They were then run: the aggregate
passed `21/21` without changing bytes; the full repository passed `221` tests with its one
registered expected failure; and the full premise verifier passed all `331` rows and `754`
historical dispositions. Only external repair-only follow-up remains pending.
