# Adversarial audit — Reciprocity off-shell constraint selector

Date: 2026-07-18
Mode: two fresh read-only reviewers; no delegated edits

## Reviewer 1 — covariant counterexample hunt

Reviewer: `/root/reciprocity_covariant_counterexample`
Verdict: `VERIFIED-WITH-CAVEATS`

The reviewer independently reproduced the chart weight
`a b -> a b/(alpha^2 beta^2)`, the CSN `sigma/phi` decomposition, the determinant-density
transformation, the flat-chart curvature counterexample, and the transitive fixed-signature
`GL(4)` orbit. The L0 theorem is exact for one metric, fixed dimension/signature, no derivatives,
and no extra structure. Oriented/pseudoscalar order-zero contractions add only zero or constants.

The strongest broader counterexamples confirmed the open scopes rather than defeating the theorem:

- Weyl/Bach conditions, curvature pseudoscalars, and curvature eigenframes are genuine L3
  metric-only covariant constructions, but are not derived from Reciprocity or equivalent to the
  raw product. Eigenframes branch or fail on degenerate/conformally-flat configurations.
- Global conformal functionals, holonomy/moduli, and representative-selection constructions are
  genuine L4 possibilities subject to the finite-cell boundary rules, but are absent from C1.
- Explicit `T,N` or coframe data make a covariant structured candidate, but it is L2 and requires
  transformation laws, normalization, and global extension.

The reviewer required the report to say “no nontrivial L0 scalar,” never an unqualified no-metric
constraint theorem. The report retains L2-L4 as exact open sectors and distinguishes natural
tensors/densities from scalar constraints.

## Reviewer 2 — variation and finite-cell audit

Reviewer: `/root/reciprocity_variation_boundary_audit`
Verdict: `VERIFIED-WITH-BOUNDARY-AND-WARD-CAVEATS`

The reviewer confirmed that, once a nondegenerate paired line/frame is carried, `a b=1` is locally
`sigma=0` and fixes the CSN representative rather than reciprocal depth. For a classical
metric-only pre-scale action invariant under local CSN, quotient/readout, hard `sigma=0`, and the
`lambda sigma` anchor have the same depth equation and zero bulk multiplier reaction.

The reviewer sharpened three limits now explicit in the report:

1. `lambda sigma` is gauge-fixing bookkeeping, not a CSN-invariant physical interaction. Global
   equivalence requires an admissible positive gauge transformation preserving mirror/boundary data,
   corners, and differentiability.
2. The Ward identity belongs to the complete differentiable action. If future vectors, coframes, or
   compensators carry Weyl weight, their Euler terms enter; they cannot be held fixed silently.
3. Vector norms use `g`, while one-form/coframe norms use `g^{-1}` and have the opposite unweighted
   Weyl sign. Either route needs its own declared transformation laws.

The strongest auxiliary-forcing attempt failed: L0 failure and flat-configuration isotropy do not
exclude readout or boundary/nonlocal routes, so no auxiliary requirement follows. The strongest
metric-only closure attempt also failed because a pre-scale CSN-invariant physical equation cannot
select the calibrational coordinate `sigma=0`.

## Reconciled verdict

Both reviewers agree:

- L0 is closed by theorem and the component product is a conditional CSN gauge/readout;
- L2-L4 remain genuinely open and can host emergent structure;
- internal reciprocal `uv=1` remains derived, while its metric readout and off-shell domain remain
  conditional/open;
- there is no auxiliary requirement and no metric-only off-shell closure;
- the finite mirror supplies seal-local parity/normal structure, not a bulk paired line selector;
- the smallest missing object is a native natural selector/realization of the paired directions,
  relative normalization, transformation law, degeneracy handling, and finite-cell extension.

Both reviewers left the repository unchanged. Their scope refinements were incorporated by the
primary before freezing; neither reviewer wrote or modified an artifact.
