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

## R2 — restore the dimensionful radial scale

The post-pass adversarial read found that `1+r^2` in the metric counterfamily silently treated the
areal radius as dimensionless. Replace it with

```text
f(r)=1+a r^2/(ell^2+r^2),  ell>0,
R=-2a(6 ell^4+3 ell^2 r^2+r^4)/(ell^2+r^2)^3.
```

The independent implementation must vary exact rational `ell` as well as `a,r`. The family remains
positive for `a>=0`, regular at the center, shares the same `t=constant` slicing, and differs
invariantly from flat space for `a!=0`. This repair strengthens the dimensional gate and leaves the
scientific landing unchanged.

## R3 — physical foliation ownership wording

Replace “global foliation requires additional integrable timelike structure” with the narrower
statement “a physical global now requires an owned integrable timelike structure.” A special metric
could derive such structure; G294 proves only that an arbitrary chosen timelike one-form need not be
integrable and that current premises do not own a preferred foliation. Do not claim that a new field
is logically necessary.

## R4 — keep co-presence graph distinct from the comparison groupoid

The symmetric nontransitive witness is a pair-relative graph/relation. Do not call it a groupoid:
composable arrows in a groupoid would supply the composite arrow. G294 must keep co-presence
adjacency distinct from the already-owned path-labelled reciprocal comparison composition unless a
new compatibility rule relates them.

## R5 — hostile-catch token matching

The first hostile-catch run stopped before writing output because two mechanical assertions searched
for prose/case variants instead of the exact registered evidence: the active-screen catch searched
for the word `strict` in prose rather than the `active_screen_strict_gap` production check, and the
instant-response catch compared an uppercase token to the lowercase architecture table. Bind the
first to the exact check name and normalize table case for the second. No scientific claim, count,
scope, or landing changes.

## R6 — TSV separator token

The R5 rerun caught the screen promotion but stopped on the final catch because the assertion still
used underscore-separated status while `ARCHITECTURE_LATTICE.tsv` records ordinary spaces. Match the
exact uppercase phrase `REJECTED BY NO-SIGNALLING GATE`. No scientific content changes.
