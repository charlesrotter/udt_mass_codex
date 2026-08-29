# G295 repair preregistration

Date: 2026-08-29

## R1 — frozen source resolution

After banking G295 in the live premise registry, `CURRENT_SCIENTIFIC_PREMISES.tsv` necessarily
differs from the source bytes frozen before outcomes at commit `d7253a9f`. Repair the package
verifier so each registered source first accepts current matching bytes and otherwise resolves the
exact frozen bytes with `git show d7253a9f:<path>`. No scientific result, count, landing, or source
hash may change.

## R2 — minimality wording guard

Require the exact report to retain that “one covariant condition” is the least-foliation-dependent
type and a packaging simplification only. It must not be read as fewer independent equations,
lower functional rank, a unique formula, or a derived field equation.

## Acceptance

The repaired package verifier must pass with all nine original source hashes, 39 production checks,
34,539 independent assertions, 12 hostile catches, and the unchanged bounded landing.
