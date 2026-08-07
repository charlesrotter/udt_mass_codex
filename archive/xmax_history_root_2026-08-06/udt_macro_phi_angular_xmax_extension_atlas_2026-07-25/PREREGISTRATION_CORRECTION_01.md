# Preregistration correction 01 — triangular orientation

Date: 2026-07-25

Parent preregistration commit: `a618524`

This append-only correction is made before generating the atlas or evaluating
either new modulation witness.

The illustrative matrix in `PREREGISTRATION.md` used the transposed convention
for the triangular angular block. The controlling complete-coframe derivation
uses the observer-rest spatial coframe

```text
A = [[w,  0, 0],
     [l2, r, e],
     [l3, 0, t]],
```

where rows are orthonormal coframe legs and columns are coordinate
differentials. This is the convention the production and independent
calculations must use.

The preregistered T1 expectation is unchanged:

```text
dphi = p dchi  =>  B = dphi^T (A^T A)^-1 dphi = (p/w)^2.
```

The seven direction labels will follow the already frozen generator convention:
three upper-triangular angular-generator entries and four lower
base-to-angular mixing entries. No outcome, branch classification, or maximum
conclusion is changed by this convention correction.

