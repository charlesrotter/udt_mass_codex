# G276 repair result

Date: 2026-08-26

Landing:

```text
R1_IMPLEMENTED__PHYSICALLY_FAITHFUL_UNIT_RELABEL_CONTROL__SCIENTIFIC_LANDING_UNCHANGED
```

The external reviewer correctly found that the old control multiplied both dimensionless `C_bar`
and `tau_star` while calling the operation a unit change. R1 replaced that control with independent
positive rational numeric length and time unit factors:

```text
C_bar'    = C_bar
tau_star' = a_T * tau_star
c_E'      = (a_L/a_T) * c_E
ell'      = a_L * ell
```

For every one of 20,000 exact-rational cases, the verifier now separately requires `C_bar'` to equal
`C_bar` and recovers `c_E' * tau_star' / C_bar' = a_L * ell`. This raises the exact assertion count
only by the preregistered 20,000 fixed-`C_bar` checks, from 300,003 to 320,003.

The 22 production checks, 20,000 inconsistency/self-evaluation/segment-mismatch rejections in each
class, six implementation mutation catches, two typed-scope catches, metric, kernel, and bounded
scientific landing are unchanged. External repair-only follow-up remains pending.
