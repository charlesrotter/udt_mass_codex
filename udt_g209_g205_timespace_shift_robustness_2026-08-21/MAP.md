# G209 map — G205 time-space shift robustness

Date: 2026-08-21

## Whole question

Let `g_A=-f dt^2+h_A` be any already supplied positive-spatial metric over the declared G205
foliation. Turn on the full three-component ADM shift vector `b` by

\[
g_b(X,X)=-f\alpha^2+h_A(v+\alpha b,v+\alpha b),
\qquad X=\alpha\partial_t+v.
\]

This is the complete local shift sector for fixed lapse `f` and supplied spatial metric `h_A`.
Classify its signature, determinant, causal cone, Cauchy criterion, null-affine survivor/failure
classes, and completed-pair response.

## Dependency decision

Trace-changing spatial shape does not have to precede this tile. The local formula accepts every
positive supplied `h_A`, including determinant-changing spatial metrics. Shape controls the width
of the causal-velocity ellipsoid, while `b` translates its center. Common conformal scale also
composes exactly with the already assembled metric. The global theorems in this tile are then
specialized honestly to the supplied G205 `h_0`.

## Frame

- **Metric-led:** shift enters `g_b` before pair pullback and reciprocal readout.
- **Observing:** retain survivor, incomplete, and non-Cauchy growth classes; do not demand one.
- **Whole local shift sector:** all three smooth components of `b` are active in the local theorem.
- **Bounded global slice:** global affine proofs use the declared G205 family and explicit invariant
  or areal-radial growth hypotheses.
- **No selector:** `b`, its direction, amplitude, profile, and time law are supplied controls.

## Premise ledger

| Item | Provenance | Role |
|---|---|---|
| G205 `f,h_0` | `DERIVED_CONDITIONAL` | supplied complete base for global tests |
| arbitrary positive supplied `h_A` | `CONDITIONAL_CONFIGURATION_ARENA` | local shift theorem |
| declared G205 time foliation | `PINNED_BY_DECLARED_REALIZATION` | ADM decomposition |
| all smooth shift vectors `b` | `CHOSE_EXTENSION_CLASS` | full local shift sector |
| subluminal and growth bounds | `FREE_AND_EXPLORED` | survivor strata, not filters |
| explicit radial shift profile | `CHOSE_CONTROL` | failure witness only |
| Levi-Civita/Hamiltonian/causal tools | `STANDARD_GEOMETRIC_EVALUATOR` | classification |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | scalar after pullback |
| action/source/transfer/observations/`X_max` | `OMITTED_OPEN` | forbidden inputs |

## Omitted scope

Trace-changing and arbitrary full spatial histories, lapse freedom beyond supplied `f`, timelike and
spacelike completeness, maximal extension, physical observer population, field/history equations,
transfer, observations, matter, and `X_max` remain open.

## Maximum conclusion

At most: an exact conditional classification of the full local shift sector and stated G205 global
subclasses. No physical shift, direction, amplitude, profile, history, or downstream law is selected.
