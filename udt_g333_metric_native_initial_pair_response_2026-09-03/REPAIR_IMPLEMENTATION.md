# G333 repair implementation

Date: 2026-09-03

All four externally requested repairs were implemented without changing any coefficient, branch,
classification, or scientific landing.

## R1 — contraction typing

`EXACT_DERIVATION.md`, `AUDIT_REPORT.md`, `EVIDENCE_GATES.md`, and the production result vocabulary
now define the directional scalar as

```text
gamma(Hv,v)=(1/2)(L_n gamma)(v,v).
```

The historical preregistration carries an explicitly marked post-review notation clarification;
its candidate list and gates are unchanged.

## R2 — load-bearing vector transport

The exact theorem now displays the general derivative

```text
n[gamma(v,v)] = (L_n gamma)(v,v)+2gamma(L_n v,v)
```

before imposing the declared calculation convention `[n,v]=L_n v=0` at the evaluation point. The
transport convention is not promoted into physical data.

## R3 — verification scope

The exact report and evidence gates now distinguish the production analytic all-`mu` proof from
the independent implementation's representative rotated-matrix and centered-first-jet checks.

## R4 — seal meaning

The audit and transmission records now say explicitly that the seal establishes internal payload
integrity and replay consistency, not third-party authorship or external provenance.

## Unchanged result

The exact coefficients, both square-root branches, 360-case coverage, two classifications, scope
boundary, and landing token are unchanged. The production JSON changes only two descriptive field
labels implementing R1/R2; its 6,882 checks and all numerical/algebraic records are unchanged.
