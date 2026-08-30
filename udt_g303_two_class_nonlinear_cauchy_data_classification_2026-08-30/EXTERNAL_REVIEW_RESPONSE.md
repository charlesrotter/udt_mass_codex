# G303 external adversarial review response

Model: `gpt-5.4`
Session: `01a05380-26df-7bf3-9506-f6d4f499f04f`
Final-response SHA-256: `16430afe0674d00d2f17cbea08ed856972cb1d5b8f840d41d466711c013e6d1e`

The text below is preserved verbatim from the valid replacement review.

---

VERIFIED_WITH_CAVEATS

The strongest retained bounded landing is: on a connected smooth local Cauchy slab, `S_ab=0` is exactly equivalent to `Ric_ab=\Lambda g_ab` with `d\Lambda=0`, the normal projections give `H=2\Lambda` and `M_i=0`, the raw trace-free harmonic symbol is rank 9 while each fixed-`\Lambda` completed sector has the same rank-10 quasilinear metric-wave principal part and the same null cone as the Ricci-flat class, and this bounded local analysis does not select either G301 class. That matches the derivation at [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:36), [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:75), and [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:117). I reran the four registered scripts from `/work` with `PYTHONPATH=/work/python_deps`; all passed, the sealed runtime hash matched, and the pinned versions were `sympy 1.13.1` and `mpmath 1.3.0`.

Every exact defect or caveat:
- The one-constant census is mathematically right, but only when stated as a union of fixed-`\Lambda` constraint surfaces. If `\Lambda` is not prespecified, the trace-free data must satisfy the compatibility condition that `H` be spatially constant, equivalently `D_i H=0`; the prose “four geometric constraints” wording compresses that point and should be stated more explicitly. See [PREREGISTRATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/PREREGISTRATION.md:58), [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:149), and [derive_cauchy_classes.py](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/derive_cauchy_classes.py:144).
- The rank-10 statement is legitimate only for the Bianchi-completed fixed-`\Lambda` sector, not for the raw `S_ab` operator itself. The intake mostly keeps that distinction straight, so this is a wording caveat, not a refutation. See [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:133).
- The “well-posedness does not select” claim is conditionally correct within the standard harmonic-gauge quasilinear-wave theorem and standard gauge-constraint propagation machinery, but those theorem-level ingredients are imported rather than independently proved in the replay artifacts. See [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:137).
- The reciprocal-kernel “no extra evolution residual” claim is retained only at bounded-document level from G302; G303 does not supply a fresh executable derivation of that absence. See [EXACT_DERIVATION.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:172).
- The hostile-catch suite is materially weaker than advertised. Several catches are tautological constant comparisons or hard-coded booleans rather than mutations of the production derivation, so that evidence gate is certification-weak. See [run_catch_proofs.py](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/run_catch_proofs.py:19) and [run_catch_proofs.py](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/run_catch_proofs.py:58).
- The independent replay does not import production code, which is good, but its projector formula is the same closed-form formula as production, so independence on the raw rank-nine symbol is partial rather than fully orthogonal. See [derive_cauchy_classes.py](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/derive_cauchy_classes.py:29) and [verify_independent.py](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/verify_independent.py:51).
- The prior external-review attempt was correctly invalidated for dependency/network-scope failure; I found no sign of outcome-driven scientific repair in the replacement package, only packaging repair plus one wording fix in a semantic guard. See [EXTERNAL_REVIEW_RUNTIME_REPAIR.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXTERNAL_REVIEW_RUNTIME_REPAIR.md:5) and [RUN_RECORD.md](/intake/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/RUN_RECORD.md:39).

The one-constant data census is valid in the bounded connected setting. I do not see a hidden extra scalar function, hidden normal derivative datum, or extra propagating residual. The extra burden is one connected-component constant, with the caveat that unfixed-`\Lambda` data must be characterized by `M_i=0` plus spatial constancy of `H`, not merely by repeating the fixed-`\Lambda` four-constraint count without comment.

Local well-posedness genuinely fails to discriminate, but only in the conditional sense claimed: once the trace-free branch is completed to a fixed-`\Lambda` Einstein sector, both branches fall under the same local harmonic-gauge quasilinear-wave framework, so the PDE theorem does not choose between them. This does not say anything beyond the local smooth boundary-free slab, and it is not a fresh proof of the theorem itself.

Scientific repair required:
- State the trace-free lawful-data condition explicitly as `M_i=0` and either fixed `H=2\Lambda` or, if `\Lambda` is not supplied, `D_i H=0` with one constant value.
- Keep the raw rank-9 versus completed fixed-sector rank-10 distinction explicit wherever “same principal system” is summarized.
- If stronger support is wanted for the reciprocal claim, add a direct derivation from the actual reciprocal identities showing no independent normal/evolution residual.

Packaging/certification repair required:
- Replace the current hostile-catch suite with real mutation tests against formulas or output artifacts; the present suite contains vacuous checks.
- Strengthen independence for the principal-symbol/rank claim by deriving the trace-free rank-9 projector through a different construction, not the same closed-form formula.
- Preserve the sealed runtime archive and manifest discipline now in place; the manifest seal and payload hashes checked out.
