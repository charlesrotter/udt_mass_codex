# G296 repair preregistration

Date: 2026-08-29

External verdict: `G296_ACCEPT_WITH_REPAIRS`.

This repair pass may verify and repair only the three findings below. It may not alter the frozen
scientific question, add a residual formula, import observations or a field equation, or strengthen
the bounded landing.

## R1 — sealed chronology proof

Add a self-contained sealed provenance artifact that permits the follow-up reviewer to verify that
commit `f7a050f0` contains only the four G296 preregistration files and precedes the implementation
and outcome artifacts. Certification requires direct object/hash evidence rather than an
uncheckable prose assertion.

Failure: chronology remains dependent on access to the live repository or an asserted text file.

## R2 — dependency-free sealed production replay

Replace the production replay's mandatory `sympy` dependency with a standard-library exact
implementation, while preserving the preregistered 32 checks and the scientific landing. The
production implementation must remain algorithmically distinct from the independent pointwise
`Fraction` reconstruction and must not read its code or output.

Restrict `COMMANDS.md` to commands runnable from the sealed intake. Repository-wide premise and
test-suite gates must be identified separately as post-repair integration gates, not sealed replay
commands.

Certification requires all registered commands to pass in a clean isolated Python environment and
reproduce the sealed JSON evidence.

Failure: an undeclared third-party dependency, missing sealed input, same-code false independence,
or changed mathematical landing.

## R3 — bounded scalar wording

Replace universal-sounding “scalar residual” claims with “tested scalar-only residual lane” where
the proof uses only scalar curvature, Ricci square, and Kretschmann scalar. Preserve the exact
positive statement that nonscalar Riemann curvature carries the trace-free screen information.

Failure: any claim to have classified every scalar construction without a new preregistered proof.

## Follow-up ceiling

If R1–R3 pass without changing the science, the maximum follow-up verdict is
`G296_REPAIRS_VERIFIED__BOUNDED_SCIENTIFIC_LANDING_RETAINED`. Banking and startup-surface updates
remain separate post-review actions.
