The tensor algebra passes, but the package’s verification status is not reproducible.

Blocking certification defect:

- [SOURCE_LINEAGE.tsv](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/SOURCE_LINEAGE.tsv:16) declares a frozen `PREREGISTRATION.md`, but that file is absent.
- [verify_p01_evaluator.py](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/verify_p01_evaluator.py:257) requires every lineage path to exist. A read-only replay therefore terminates with `AssertionError: source path`.
- This contradicts the recorded `source_status_and_coverage_ledgers: PASS` at [VERIFICATION_RESULT.json](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/VERIFICATION_RESULT.json:41). Consequently, the `TOOL_VERIFIED` statuses in [STATUS_LEDGER.tsv](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/STATUS_LEDGER.tsv:2) are presently overstated. The preregistration gate is not evidenced by the delivered package.

Correctness findings:

- Metric, derivative-of-connection, Riemann, Ricci, scalar, spin-connection, and both Cartan conventions are mutually consistent. An independent generic off-diagonal two-jet calculation agreed to \(1.39\times10^{-17}\).
- The conditional ten-slot \(2+2\) forward/reverse maps, block inverse, determinant, and derivative channels are correct inside the supplied split. Independent finite-difference agreement was \(7.21\times10^{-9}\).
- A coordinate-dependent local Lorentz test, including derivative gauge terms, agreed to \(4.16\times10^{-17}\).
- Full value/first/second-jet, connection, and Riemann transformation under a nontrivial linear coordinate map agreed to \(1.11\times10^{-16}\).
- CSN weights and the variable conformal connection transformation are correct.
- No action, GR equation, preferred \(\phi\)-join, reciprocal-plane selection, or desired-result leakage was found. The stated conclusion ceiling is appropriate.

Coverage caveats:

- The packaged Lorentz test checks only a constant transformation and metric-jet invariance ([run_p01_evaluator.py](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/run_p01_evaluator.py:148)).
- The coordinate roundtrip uses the same transformation routine forward and backward; only the metric value is independently predicted, not transformed derivative jets, connection, or curvature ([run_p01_evaluator.py](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/run_p01_evaluator.py:163)).
- The verifier’s SymPy coordinate curvature and exact split identities are genuinely independent, but its Cartan/coframe checks reuse the production evaluator and fixtures ([verify_p01_evaluator.py](/tmp/udt_startup_rehearsal_20260719_h0zjlA/repo/udt_canonical_geometry_evaluator_p01_2026-07-21/verify_p01_evaluator.py:230)).
- Malformed/singular mutation coverage is partial; several validation paths exist in implementation but are not exercised by the recorded catch suite.

The derivation replay itself reproduced byte-for-byte with SHA-256 `29de377f8bc50d0a1a3ca189ce0305e9c980d7b654f050583c2473744a71d236`. No files were changed.

FAIL_BLOCKING