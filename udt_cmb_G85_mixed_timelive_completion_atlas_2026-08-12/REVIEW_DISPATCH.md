# External cold-review dispatch — G85

You are a fresh adversarial reviewer. Inspect only the sealed intake defined by
`REVIEW_MANIFEST.tsv`. Do not edit files, continue the research, fit data, or inspect any path not
present in the intake.

## Required audit

Reconstruct the G85 question from the preregistration and frozen sources, then try to refute the
banked result. In particular:

1. independently derive the full determinant, temporal Schur complement, axial fixed-set gate,
   and induced seam determinant;
2. determine whether time dependence in `h` alone can repair the nonzero-mixing axial degeneracy;
3. check whether the smooth radial-shift and clock-norm-lift witnesses really define Lorentzian
   tensors across the equator, axes, and poles while preserving the exact G75 north cell;
4. check whether the nonzero-shift/nonzero-mixing seam genuinely changes causal type between
   off-axis and axial points;
5. check the zero-shift Kruskal calculation and whether `h=A*h_tilde` is sufficient; identify if a
   weaker or stronger order is actually required;
6. independently reconstruct the `196 x 5 = 980` census from the original rational profiles;
7. hunt circular verification, vacuous catches, hidden topology/profile/scale selection, and any
   overstatement of global smoothness, geodesic completeness, time-live dynamics, or physical
   `X_max`; and
8. report exact corrections, if any, without performing the next scientific step.

Return one primary verdict:

- `VERIFIED`;
- `VERIFIED_WITH_CAVEATS`;
- `CORRECTION_REQUIRED`;
- `REFUTED`.

Separate exact derivation, finite witness evidence, and interpretation. State the maximum justified
conclusion and the smallest next gate, but do not solve that gate.
