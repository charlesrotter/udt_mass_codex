# Fresh adversarial return — general-screen neighborhood audit

Date: 2026-08-02  
Reviewer context: fresh subagent; read-only repository access; scratch work only under `/tmp`  
Initial grade: `PASS_WITH_CAVEATS`

## Independent replay

The reviewer built a fresh PyTorch `float64` coordinate/autodiff implementation without importing
production functions and replayed all 34 nondegenerate candidate/point jobs.

- all 32 exact nonzero invariant Jacobians reproduced;
- worst exact-versus-autodiff relative error: `2.3392144311358414e-11`;
- C14 numerical determinants: `2.36e-40` and `3.98e-39`, versus exact zero;
- maximum Ricci asymmetry: `2.274e-13`;
- independent centered finite differences on C08-C10 and C15-C17 agreed within `5.305e-6`;
- exact independent algebra reproduced screen tangent rank three, screen-shape determinant one,
  pair-block determinant minus one, the contact formulas, the `10/7/1` configuration classes, the
  nonzero wedges at both registered points, and the C16/C17 causal strata;
- the six intrinsic-projector plus nonzero-alternating cases reproduced exactly as
  C04, C08, C09, C10, C16, and C17.

Environment: Python `3.10.12`; PyTorch `2.5.1+cu121` on CPU; SymPy `1.13.1`.

Scratch artifacts:

| Object | SHA-256 |
|---|---|
| `/tmp/independent_general_screen_review.py` | `a87d7307cb7a1ce4e42ce41298468bc0124457d88bf6ec694c08f4da6083b467` |
| independent review result | `5681c67b1e9d0125c470e6b3a9fa483e83b404c6acc0481b7e3cdd2eef8c7063` |
| independent algebra script | `a01ea6809213011c3e3c220e02608e7105abcd3fde658922d30f06fd8e88a15e` |
| independent algebra result | `ddd79c6f107a419b98de9b4fd10b3d48a8aef6310155c5fc58c3a135cd23d3ee` |

The reviewer independently replayed all 48 frozen source identities and all 34 point-manifest
identities. No repository file was edited.

## Required scope repairs

The initial return required five guards before a clean final grade:

1. restrict the open `C^3` neighborhood to the stationary subspace retaining `K=partial_t`;
2. distinguish raw fixed-coframe configuration classes at C14/C15 from intrinsic contact objects;
3. state that a nonzero simple/decomposable two-form has antisymmetric-matrix rank two;
4. retain that one profile per mode does not exhaust the smooth `GL(2,R)` function space; and
5. distinguish exact/algebraic mutation catches from semantic scope guards instead of calling all
   synthetic boolean mutations substantive independent proofs.

These repairs are recorded in `PREREGISTRATION_SCOPE_CLARIFICATION.md`, the regenerated result and
status ledgers, the exact control output, and the typed catch-proof table. Final post-repair recheck
is recorded separately.
