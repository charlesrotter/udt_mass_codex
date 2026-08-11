# External-review adjudication

Date: 2026-08-10

External landing: `VERIFIED_WITH_CORRECTIONS`

Adjudicated landing: `VERIFIED_WITH_CORRECTIONS`

No algebraic or typing defect was found. All three evidence-quality corrections are accepted.

1. **Independent 27-row reconstruction — accepted and repaired.** The pre-review verifier only
   checked stored residuals and flags. It now reconstructs every row from `R`, `A`, `M_signed`, and
   the bivector components, checks the closed-form root for `B02`, and independently recomputes the
   simplicity determinant, mixed norm, and Lorentzian Gram determinant.
2. **Catch-harness grade — accepted.** The 24 catches remain useful fail-closed algebraic, scope,
   and packaging guards. They are not counted as a fresh independent semantic proof.
3. **Sealed provenance replay — accepted and repaired.** `verify_sealed_intake.py` now recognizes
   both the repository layout and a self-contained `sources/` layout and checks all 15 exact hashes
   without writing.

After banking G59 in the live premise registry, the working-tree copy of
`CURRENT_SCIENTIFIC_PREMISES.tsv` necessarily differs from the source frozen before derivation.
The historical `verify_preregistration.py` remains unchanged and is replayed at preregistration
commit `162779cf`. The additions-only `verify_fixed_base_sources.py` independently replays all 15
manifest hashes from registered base `8215a31578e571e29750daa53ccf26e436f7e582`; the corrected
self-contained sealed intake remains the transport check. No historical hash is rewritten.

The original preregistrations and `PRE_REVIEW_REPORT.md` remain unchanged historical evidence.

## Final scoped theorem

Conditional on a correctly typed metric-orthogonal reciprocal/angular `2+2` split, the complete
pointwise pair Jacobian supplies the exact matrix decomposition `h=H_R+H_A`; `(H_R,H_A)` classifies
the generic continuous split-frame orbit; its simple bivector supplies the exact signed area locks;
and angular variation can modulate `kappa`, `phi_pair`, and `beta` in concert. Current premises do
not select a canonical positive scalar sector weighting or a physical time-live trajectory through
this atlas.

## Smallest remaining joint

Determine whether any already-owned complete branch both owns the reciprocal/angular split and
supplies an actual curve `s -> (H_R(s),H_A(s))`. No such physical curve is established here.
