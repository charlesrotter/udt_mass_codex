# G266 repair-only follow-up request

Review only the preregistered G266 repairs R1--R4 and the unchanged bounded alternative-B landing.

Required checks:

1. Verify the sealed scope, manifest, payload hashes, and byte counts.
2. Run `verify_package.py` in the sealed layout without SymPy and confirm the dependency-free exact
   replay equals `DERIVATION_RESULT.json` with all 25 named checks.
3. Confirm live-repository and sealed `private_sources/` source-resolution logic is fail-closed and
   the wrong-hash mutation is rejected.
4. Confirm the 768 independent exact-rational assertions and 8 mutation catches still pass.
5. Confirm the SymPy and standard-library exact results are identical if SymPy is available; lack
   of SymPy must not prevent sealed certification.
6. Confirm the invariant wording is bounded to scalar readouts formed only from the determinant-one
   reciprocal kernel on the supplied relation.
7. Confirm `R` remains an invariant areal-radius descriptor while `ds=dR` remains only a freely
   explored physical-distance attachment.
8. Confirm alternative B, all formulas and counts, and the maximum conclusion are unchanged.

Return exactly one disposition:

- `REPAIRS_ACCEPTED`; or
- `REPAIRS_REJECTED`, with the exact failed repair and evidence.

Do not adopt `P_INF`, `P_MUT`, `sech(delta)`, a distance protocol, or a metric history. Do not alter
the scientific question, continue the research, inspect observational outcomes or protected
packages, or edit evidence files.
