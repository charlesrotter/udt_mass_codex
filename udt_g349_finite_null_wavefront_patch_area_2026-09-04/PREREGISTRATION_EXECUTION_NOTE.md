# G349 preregistration execution note

Date: 2026-09-04
Preregistration commit: `84cb5264`

The first registered production execution returned `44314/44314` with no failure. The first
implementation-distinct execution returned `14314/14314` with no failure.

The first hostile execution returned `20/21`. The sole failure was
`call_every_rank_one_a_fold`: its implementation searched for the exact phrase
`do not assume every rank-one singularity is a fold`, while the frozen preregistration expresses
the same guard as `no claim that all rank-one points are folds is permitted without an extra
genericity theorem`. This was a text-hook defect, not a mathematical counterexample or a failed
scope condition.

The repair replaces that wording lookup with the explicit cusp control

```text
F(x,y)=(x,y^3+xy).
```

At the origin its differential has rank one. The kernel is tangent to the critical curve
`x=-3y^2`, so it is the standard non-fold rank-one cusp condition. This directly catches the
forbidden mutation without depending on prose. No alternative, definition, witness set, numerical
tolerance, physical premise, maximum conclusion, production result, or independent result changed.
