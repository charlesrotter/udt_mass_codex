# G294 repair preregistration

Date: 2026-08-29

## R0 — exact matrix comparator

The first production attempt stopped before writing `DERIVATION_RESULT.json`. The generic `exact`
helper simplified a zero matrix correctly but then compared the matrix object to scalar zero, which
returned false.

Repair: branch only on matrix type and use SymPy's exact `is_zero_matrix` property. Scalar
comparison, every formula, all witnesses, tolerances, scope, falsifiers, and candidate landings are
unchanged. No scientific outcome was observed beyond the comparator exception.

## R1 — curvature polynomial transcription

The first run after R0 stopped before writing `DERIVATION_RESULT.json` because the independently
entered expected scalar-curvature polynomial for

```text
f(r)=1+a r^2/(1+r^2)
```

was incorrect. Direct differentiation of the preregistered metric gives

```text
R=-2 a (r^4+3 r^2+6)/(1+r^2)^3.
```

Repair the expected expression in both implementations. The center value `R(0)=-12a`, positivity
of `f`, inequivalence from flat space for `a!=0`, shared `t=constant` slicing, scope, falsifiers, and
candidate landing are unchanged. The stopped run produced no result artifact.
