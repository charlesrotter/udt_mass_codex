`G196_REPAIRS_ACCEPTED__BOUNDED_LANDING_RETAINED`

No repair-scope defect found.

Strongest retained theorem: for the displayed `a(eta), M(eta,z)` affine coframe family and one supplied central outgoing germ, the sealed package still supports only the bounded claim that longitudinal dependence descends to `D_+ = partial_eta + partial_z`, with `C_s = 2 Omega`, coordinate factorization `(D_+ - 2 M^T)(D_+ + 2 M)Y = 0`, ordered representation `D = a L K` with `L' = -2 M_bar L`, `K' = L^-1 L^-T`, pure rotation contributing connection carry but no independent focusing tide, and `det D > 0` off the vertex on each connected regular outgoing-ray interval; no broader family, direction, observer, transfer, or `X_max` conclusion is supported. See [EXTERNAL_REVIEW_ADJUDICATION.md](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/EXTERNAL_REVIEW_ADJUDICATION.md:17), [PRODUCTION_RESULT.json](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/PRODUCTION_RESULT.json:1).

R1 status: pass. The original independent preregistration remains visibly preserved with a dated correction, and current prose now narrows the IVP evidence to formula-level regression from shared `candidate_matrices(...)` coefficients rather than a fully independent metric-to-Jacobi derivation. This matches the code path where both IVP legs share `candidate_matrices(...)`. See [INDEPENDENT_PREREGISTRATION.md](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/INDEPENDENT_PREREGISTRATION.md:7), [AUDIT_REPORT.md](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/AUDIT_REPORT.md:69), [verify_longitudinal_screen_mixing_independent.py](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_longitudinal_screen_mixing_independent.py:444), [verify_longitudinal_screen_mixing_independent.py](/tmp/udt_g196_review_myxg_x_1/udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_longitudinal_screen_mixing_independent.py:492).

R2 status: pass. I ran the exact registered replay from [REVIEW_SCOPE.json](/tmp/udt_g196_review_myxg_x_1/REVIEW_SCOPE.json:1) in the read-only sandbox:
```bash
TMPDIR=.review_runtime TMP=.review_runtime TEMP=.review_runtime G196_NO_WRITE=1 PYTHONDONTWRITEBYTECODE=1 python3 udt_g196_longitudinal_screen_mixing_descent_2026-08-20/verify_package.py --no-write
```
It exited `0` after about 21m47s, so the required wait ended by early process exit. Live replay status: `fresh_artifact_identity=true`, `production_assertions=17`, `independent_histories=204`, `independent_assertions=5313`, `mutation_catches=9`, unchanged ceilings/results, and stale-artifact mutation caught. Torch imported successfully in no-write mode via the preregistered `tempfile.tempdir` path without requiring a writable temp directory. Post-run, `.review_runtime` existed and had `0` entries.

Pre/post hash status: all `38/38` declared hashes in `REVIEW_SCOPE.json` matched before replay and all `38/38` matched after replay. No sealed evidence file changed.

Exact defects: none remaining within the allowed R1/R2/unchanged-landing review scope.

Maximum honest conclusion: the two preregistered repairs close the prior evidence-description and read-only replay defects without changing the bounded scientific landing. The package remains accepted only at the original bounded family/germ level, with the IVP leg correctly understood as formula-level regression evidence rather than an independent metric-to-Jacobi derivation.