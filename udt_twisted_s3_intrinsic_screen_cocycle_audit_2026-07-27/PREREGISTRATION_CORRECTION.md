# Preregistration correction — control `lambda` values

Date: 2026-07-27

Original preregistration commit: `de6b2f7`

Before running the production or independent outcome calculations, a literal comparison with the
parent frozen candidate universe found that the newly transcribed C07 and C08 control rows said
`lambda=1`.  The parent rows both say `lambda=0`.

This correction changes only those two clerical cells in `CANDIDATE_UNIVERSE.tsv`:

```text
C07 lambda: 1 -> 0
C08 lambda: 1 -> 0
```

All questions, gates, formulas, six positive candidates, control roles, falsification contracts,
and maximum conclusions remain unchanged.  The corrected rows now reproduce the immutable parent
candidate universe.  No result was calculated or inspected before this correction was committed.
