# G276 repair preregistration

Date: 2026-08-26

External `gpt-5.4` returned `ACCEPT_WITH_REPAIRS` with the bounded scientific landing unchanged.

## R1 — physically faithful unit relabelling

The original independent verifier multiplied both `C_bar` and `tau_star` by a common factor while
calling that operation a unit change. Since `C_bar` is dimensionless, that label and control are not
physically faithful.

Replace it with the exact unit-coordinate transformation

```text
C_bar'   = C_bar
tau_star'= a_T * tau_star
c_E'     = (a_L/a_T) * c_E
ell'     = a_L * ell
```

for arbitrary positive rational `a_L,a_T`. Require exactly

```text
c_E' * tau_star' / C_bar' = ell'.
```

## Required repair gates

1. `C_bar` remains byte-for-byte/numerically unchanged in every unit-relabelling case;
2. recovered numeric scale transforms with the length-unit factor `a_L`;
3. independent census remains at 20,000 cases;
4. exact assertion count changes only by the preregistered new fixed-`C_bar` assertion, from 300,003
   to 320,003;
5. production derivation and its 22 checks remain unchanged;
6. all eight prior hostile controls remain passing;
7. package and startup verifiers are updated only for the new exact count and external-review grade;
8. no scientific landing, metric, kernel, history, distance, or `X_max` statement changes.

## Falsification

Reject the repair if `C_bar` changes, if the recovery differs from `a_L*ell`, if the result depends
on a chosen clock value, or if any prior scientific guard changes.

Maximum repair landing:

```text
R1_IMPLEMENTED__PHYSICALLY_FAITHFUL_UNIT_RELABEL_CONTROL__SCIENTIFIC_LANDING_UNCHANGED
```
