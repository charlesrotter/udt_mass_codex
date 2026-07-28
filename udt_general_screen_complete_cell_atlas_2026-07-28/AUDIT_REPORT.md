# General-screen complete finite-cell existence atlas

Date: 2026-07-28

Base: `73833fa4e75152e51d24f8056b6856dd835785f7`

## Result first

The preregistered outcome is `MIXED_BRANCH_AND_DEGENERACY_ATLAS`.

Within the stationary off-shell block-screen `R x S3` control:

1. a general smooth invertible screen exists globally and carries three metric degrees of freedom
   (area and two shears) plus one local coframe-gauge rotation;
2. both shear tangents survive at the isotropic screen—polar coordinates had hidden one;
3. screen anisotropy makes the inherited Maurer–Cartan angular generator display both shear
   components as well as rotation;
4. the full spatial first-jet Levi-Civita connection is exact and agrees with the inherited
   equal-screen result on that subfamily;
5. no choice of general `P` can make the reciprocal pair and angular screen an all-direction
   parallel splitting on this twisted `S3` family, because the nonzero contact coefficient
   `t1=kappa exp(phi)/det(P)` obstructs integrability.

The fifth result has two independent routes: explicit connection blocks and a Frobenius argument.
It is a bounded geometric no-go, not a no-go for UDT, other completions, pathwise screens, or a
non-block metric.

## What changed relative to the parent atlas

The parent atlas observed trace, rotation, and pair-screen mixing but left both shear directions
ansatz-frozen. This package releases the entire invertible `2 x 2` screen. The shear gap closes as an
ansatz diagnosis: both shear modes exist in global regular configurations. No physical coefficient
or branch is selected.

## Global and completion rulings

- `FC04_TWO_CAP_P1`: constructive global `S3` general-screen configurations exist.
- `FC11_NONINTEGRABLE_DISTRIBUTION`: realized as a property of the `S3` witness, not a separate
  disjoint metric.
- lens and other quotient/transition classes: conditional on exact equivariance and transition
  data.
- cap, seam, stratified, and other classes without actual joined coframes: blocked, not filled in.
- `det(P)=0`: retained as a true metric-degeneracy boundary.
- zero/negative induced slice sign: retained and distinguished from four-metric degeneracy.

“Complete” means a smooth global complete-cell configuration. Only a positive compact spatial slice
receives a Riemannian geodesic-completeness statement. Lorentzian geodesic completeness is open.

## Evidence gates

1. **Preregistered:** yes; scope and F01–F34 were committed and pushed before derivation. A separate
   clarification froze `E0(P)=0` before response calculation.
2. **Full or bounded:** full `GL(2,R)` screen and all three spatial first jets inside the explicitly
   bounded stationary block-screen `S3` family; not the generic spacetime metric.
3. **Independent:** production identities are checked by a non-importing implementation. The
   load-bearing parallel-split no-go is also checked by a different Frobenius argument. A fresh
   zero-context adversarial record is required by `verify_audit.py` before final banking.
4. **Premises audited:** every chosen, free, dropped, and open premise is in `PREMISE_LEDGER.tsv`;
   all ten completeness axes and all twelve FC types remain visible.

## Evidence map

- exact reasoning: `EXACT_DERIVATION.md`
- machine algebra: `derive_general_screen.py`, `GENERAL_CARTAN_RESULT.json`
- independent implementation: `verify_general_screen_independent.py`, `INDEPENDENT_RESULT.json`
- response and rank: `POLAR_RESPONSE_ATLAS.tsv`, `RESPONSE_RANK_ATLAS.tsv`
- global witnesses: `COMPLETE_S3_WITNESS_ATLAS.tsv`, `GLOBAL_EXISTENCE_ATLAS.tsv`
- contact no-go: `BLOCK_PRESERVATION_CONDITIONS.tsv`, `CARTAN_RESPONSE_ATLAS.tsv`
- completion gates: `COMPLETION_DESCENT_ATLAS.tsv`
- falsification: `FALSIFICATION_CONTRACT.tsv`, `CATCH_PROOFS.tsv`

## Maximum conclusion

`VERIFIED-WITH-CAVEATS`: exact stationary off-shell complete-`S3` general-screen existence,
response, and bounded parallel-split no-go only. The complete UDT action, equation, source, carrier,
bootstrap, matter emergence, boundary completion, physical scale selection, and branch selector
remain `OPEN` or retain their prior premise-scoped status.
