# G264 repair preregistration

Date: 2026-08-25
Trigger: fresh external disposition `ACCEPT_WITH_REPAIRS`

The bounded scientific landing is frozen unchanged. The only accepted defect is evidentiary:
`verify_independent.py` is result-blind and implementation-distinct but embeds the target curvature
formulas, so it is a consistency replay rather than a second metric-first derivation.

## R1 — metric-first dependency-free derivation

Add a new standard-library verifier that begins only with the metric components and their first and
second coordinate derivatives at a regular equatorial point. It must independently construct:

1. inverse metric and its first derivatives;
2. Christoffel symbols and their first derivatives;
3. Riemann and Ricci tensors;
4. scalar curvature and Kretschmann scalar;
5. the registered radial and angular mixed Einstein channels.

It must not import production code, SymPy, or saved results. Only after constructing the tensors may
it compare them with the registered closed forms. Use exact `Fraction` arithmetic on at least 200
nondegenerate arbitrary jets.

## R2 — evidence language alignment

Reclassify the existing `verify_independent.py` honestly as an implementation-distinct consistency
replay. Cite the new metric-first verifier as the independent derivation. Update package gates,
reports, counters, and fail-closed checks accordingly.

## R3 — hostile repair catches

Add altered-copy or package checks that fail when:

- the new verifier imports production code, SymPy, or saved results;
- metric-first coverage is removed or reduced;
- the tensor construction is replaced by direct target-formula assignment;
- the old consistency replay is again called the independent metric derivation;
- the unchanged scientific landing or ownership ceiling is altered.

## Closure contract

Run the metric-first verifier, the existing consistency replay, mutation catches, package verifier,
premise audit, and repository tests. Then submit a fresh sealed repair-only intake. The repair may
strengthen evidence but may not change the scientific question or landing.
