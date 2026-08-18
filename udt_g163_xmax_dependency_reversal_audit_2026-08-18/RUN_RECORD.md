# G163 run record

Date: 2026-08-18
Branch: `grok`
Preregistration commit: `fb7e0f8e`
Source snapshot: `21ca77db`

Commands:

```text
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/derive_scale_free_kernel.py
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/verify_scale_free_kernel_independent.py
python3 udt_g163_xmax_dependency_reversal_audit_2026-08-18/run_catch_proofs.py
```

Results:

```text
production: PASS; 13 checks; X-free residual Jacobian structurally zero by construction
independent: PASS; 1,200 exact Fraction trials of the independently encoded algebra
catches: PASS; three genuine mutations plus five semantic/typing guards
dependency census: 20/20 G135--G154 rows
```

Fresh adversarial review returned `PASS_WITH_REPAIRS`. It preserved the central result and required
the structural-rank, evidence-type, dimensional-control, and dependency labels now recorded in the
package.

Final repository gates:

```text
premise verifier: PASS; 150 rows
pytest: 122 passed, 1 expected xfail
package verifier: PASS
git diff --check: PASS
```

No observational data, fit, GPU, long solve, action, source, bootstrap, protected package, or
stopped draft was read or used.
