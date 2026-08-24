# G244 preregistration parity-type correction

Date: 2026-08-24

Status: `CORRECTED_BEFORE_G244_DERIVATION_OR_OUTCOME`

The first committed preregistration incorrectly called `sign(det(D))` invariant under independent
endpoint `O(2)` basis changes. If

```text
D_new = Q_s^T D Q_o,
```

then

```text
sign(det(D_new)) = det(Q_s) det(Q_o) sign(det(D)).
```

Therefore parity is naturally valued in the tensor product of the source and observer screen
orientation lines. It becomes an ordinary invariant sign only after compatible endpoint
orientations are supplied, equivalently for `SO(2)` basis changes.

The fully unoriented outputs are unchanged:

```text
H = D^dagger D,
A = abs(det(D)),
C = H/A,
shear_power = tr(H)^2/[4 det(H)] - 1.
```

This correction changes no outcome, tolerance, witness, or conclusion ceiling; no derivation code
or result existed when it was made.
