# G271 external-review repair ledger

Date: 2026-08-26

The external landing was `ACCEPT_WITH_REPAIRS`. No scientific equation or conclusion was rejected.

## R1 — sealed source-path containment

Status: `REVIEW_OBJECTION_REFUTED__DEFENSIVE_GUARD_ADDED`

The original sealed intake already contained every `SOURCE_MANIFEST.tsv` target. In the copied
package:

```text
ROOT       = <sealed intake>/udt_g271_primary_metric_null_screen_first_jet_interlock_2026-08-26
ROOT.parent = <sealed intake>
```

Direct resolution found all five paths under `/tmp/udt_g271_review_hwb1isn4`, and the original
registered package replay passed there. `verify_package.py` now names this directory `SCOPE_ROOT`,
resolves every source path, and requires `path.is_relative_to(SCOPE_ROOT)` before reading or hashing
it. The result records `source_paths_within_scope_root=5`.

This is a packaging-clarity repair only. It does not alter the theorem or evidence values.

## R2 — spherical-isometry coverage

Status: `ACCEPTED_AND_REPAIRED`

`EXACT_DERIVATION.md` and `AUDIT_REPORT.md` now state the missing reduction explicitly. For an
arbitrary local spatial null direction

\[
n=\cos\alpha\,e_{\hat r}+\sin\alpha\,e_{\hat\perp},
\qquad e_{\hat\perp}\in T(S^2),
\]

an `SO(3)` isometry maps the radial/tangential plane to the equatorial plane. It preserves the
metric, `r`, `phi(r)`, `U`, `a`, Levi-Civita transport, and every contraction in the theorem.
Therefore the equatorial calculation represents every regular finite-radius null germ modulo exact
spherical isometry. The radial degeneracy is covered by the exact radial calculation.

No preferred plane, history, distance, source, action, fit, transfer law, or `X_max` was introduced.

## Evidence-language clarification

The six typed overreach catches are textual scope-regression guards. They are retained as evidence
that prohibited conclusion strings are caught, not promoted as an independent physics derivation.

## Retained landing

The bounded G271 scientific landing is unchanged. A repair-only external follow-up remains required
before upgrading the external grade.
