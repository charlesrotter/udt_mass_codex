# G333 audit report — metric-native initial pair response

## Bounded result

For every datum in the exact G332 unit-Killing construction and every unit spatial direction `v`,
write `H(v,v)` only as shorthand for the bilinear contraction
`gamma(Hv,v)=(1/2)(L_n gamma)(v,v)`. The first normal response is

```text
gamma(Hv,v)=(b-C)/2-b gamma(v,xi)^2.
```

Its trace-free eigenvalues are `(b/3,b/3,-2b/3)`, with squared norm `2b^2/3`. This is an exact
common-plus-directional response fixed by the lawful metric initial data. It uses no orbit period,
Hopf quotient, or topology input.

For the bounded Gaussian normal--spatial pair germ, the complete pair metric records
`n(h11)=2gamma(Hv,v)` while `n(Phi)=0`, provided the chosen extension obeys
`[n,v]=L_n v=0` at the evaluation point. Without that transport convention the general derivative
has the additional term `2gamma(L_n v,v)`. This establishes only that the complete pullback
contains more first-jet information than its terminal scalar in this germ class.

## Four evidence gates

1. **Preregistered:** PASS at commit `c56714b3`, pushed before execution.
2. **Bounded space:** PASS for the full G332 construction, all unit directions, both square-root
   branches, and the strict radicand stratum; nonzero time and other pair-germ classes remain open.
3. **Independent verification:** PASS locally by a rotated-matrix and centered-first-jet method on
   representative directions that imports no production code and reads no production result. The
   exact production derivation, not the sampled verifier, carries the analytic all-direction proof.
   Fresh external review retained the result with four repairs. The repair-only follow-up
   authenticated all 41 payloads, replayed the registered evidence byte-exactly, and accepted all
   four repairs without changing the bounded result.
4. **Premise audit:** PASS locally in `PREMISE_LEDGER.tsv`; adopted response equation, sign
   convention, gauge control, and all omissions remain explicit.

## Numerical and algebraic evidence

- exact production: 6,882 checks across 360 cases;
- implementation-distinct verification: 146 checks;
- hostile suite: nine scientific mutations caught;
- final aggregate package verification: 105 gates;
- floating point is used only in the independent rotated-matrix reconstruction, with exact
  production as the load-bearing result;
- no long solve, GPU, fitting, cutoff, action, source, mass model, or observational outcome.

The detached manifest seal establishes internal payload integrity and replay consistency for the
sealed intake. It does not establish third-party authorship or provenance outside that intake.

## Current grade

`DERIVED_CONDITIONAL_BOUNDED__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS`.

The fresh reviewer found no refuting defect and the repair-only reviewer accepted all four
scope/typing repairs. The accepted result does not select Hopf structure, a physical history, a
branch, a scale, or a universe.
