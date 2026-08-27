REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED

Manifest verification: `/intake/REVIEW_MANIFEST.sha256` matches the actual SHA-256 of `REVIEW_MANIFEST.tsv` (`66197802f68bb124652c1908a9ab1bbd2a5c7c2914069a39fb325c0cd1dab1e7`). All 38 payload entries in `REVIEW_MANIFEST.tsv` matched path, byte count, and SHA-256 exactly. I reconstructed the frozen layout only under `/work/reviewroot` by copying the contents of `/intake/sources/` directly into `/work/reviewroot` and placing the sealed G280 package directory beside them.

Exact checks run from `/work/reviewroot/udt_g280_projective_position_optical_area_bridge_audit_2026-08-27`:
```bash
python3 freeze_source_manifest.py
python3 derive_projective_optical_bridge.py
python3 verify_projective_optical_bridge_independent.py
python3 run_catch_proofs.py
python3 derive_projective_optical_bridge.py --no-write
python3 verify_projective_optical_bridge_independent.py --no-write
python3 run_catch_proofs.py --no-write
python3 verify_package.py
```
Replay results: all eight commands passed. The regenerated durable outputs were byte-for-byte identical to the sealed baselines:
`SOURCE_MANIFEST.tsv` `38c6dbe646ca96f7639b1c84137a25f2d3d2cb5c6e3fb9234d28f7d901b6188d`,
`DERIVATION_RESULT.json` `f332b831a915cf444f3dce47edfda6d8bc9cce39e65094c00f83b3ca0074650d`,
`INDEPENDENT_VERIFICATION.json` `ac3c3de112ccffacbc1ec59aefd8a2337dfbea960493e452ec12f3349937cc7b`,
`CATCH_PROOF_RESULT.json` `4888d3e7f03c4f21f3f2501cb92029420b1f4bcaa4e59485046baee85f3f7764`.

Repair findings:
- R1 passes. `run_catch_proofs.py` and `CATCH_PROOF_RESULT.json` separate exactly four executable mathematical mutation/counterchecks from exactly four premise-ledger provenance guards, and the labels match what each check actually does.
- R2 passes. The center check uses exact symbolic derivatives via `sympy.diff`, not an epsilon probe, and records `d(atanh(s))/ds|_0 = 1` and `d(s^2)/ds|_0 = 0`.
- R3 passes. The validator fails closed against all eight altered check-kind labels, one altered center derivative, and one altered class count, for exactly ten caught repair mutations.
- The bounded scientific landing is unchanged. Alternative `B`, the metric/Jacobi formulas, `36,883` production assertions, `4,096` independent cases, `40,960` independent assertions, `0` fitted coefficients, `0` observational outcomes used, the import exclusions, and the maximum conclusion all remained unchanged in the sealed package and in the regenerated outputs.

Remaining scoped defect: none.
