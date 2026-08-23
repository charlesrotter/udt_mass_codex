# G233 external-review packaging repair preregistration

Date: 2026-08-23

The fresh sealed gpt-5.4 review returned `VERIFIED_WITH_CAVEATS` and found no scientific
repair. It identified one packaging-only defect: the displayed scalar-curvature formula in
`EXACT_DERIVATION.md` contains a form-feed control character where the LaTeX command
`\frac` should appear.

Frozen repair:

- replace only that control character with the literal LaTeX text `\frac`;
- preserve every equation, coefficient, scope, script, result, and scientific landing;
- record the reviewer verdict and exact bounded scope;
- rerun the registered package replay, premise verifier, and repository tests.

The repair fails if the corrected formula differs from the already verified code formula or if any
scientific evidence changes.
