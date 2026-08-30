# G302 repair preregistration

Date: 2026-08-30
Trigger: fresh external `VERIFIED-WITH-CAVEATS` review

The scientific landing, equations, solution family, channel separation, domain table, and scope
ceiling are frozen.  Only certification coverage and matching wording may change.

## R1 — exhaustive independent domain census

Replace representative-only positive-root checks with an independent exact exhaustive certificate
covering every row of `DOMAIN_CLASSIFICATION.tsv`.

The repair must:

1. nondimensionalize the cubic

   \[
   P(r)=r+b-R_0r^3/12
   \]

   separately for `R0>0`, `R0=0`, and `R0<0`;
2. derive the discriminant and the exact threshold `b=-4/(3 sqrt(R0))`;
3. partition parameter space at every place where a positive root can be created, destroyed, cross
   `r=0`, or become repeated;
4. use exact Sturm/root isolation on one point in each connected open cell, together with exact
   boundary factorization and endpoint/leading-sign logic, to certify root count and positive-`f`
   interval orientation throughout that cell;
5. compare all eight derived rows field-by-field with the production TSV;
6. write a machine-readable independent result and add hostile mutations for at least wrong
   threshold, wrong interval orientation, missing double-root multiplicity, and false positive
   interval at the repeated root.

The independent domain verifier must import no production function.

## R2 — exact certification wording

Until R1 passes, the domain table is `EXTERNALLY_MANUAL_ALGEBRA_VERIFIED` and internally
representative-checked.  If R1 passes, wording may be upgraded to
`INDEPENDENT_EXHAUSTIVE_PARAMETER_CELL_VERIFIED`.  The external review's original caveat and first
failure remain preserved.

## Frozen scientific content

No change is permitted to:

- shape rank 9 or complete rank 10;
- `NO_G301_CLASS_SELECTED`;
- `f=1+b/r-R0 r^2/12`;
- curvature or angular formulas;
- smooth-center condition `b=0`;
- quiet-window condition;
- field-equation, mass, history, observation, physical-query, nonspherical, or time-live ceilings.

## Repair certification

- repair preregistration committed before the exhaustive verifier exists;
- independent script and package verifier pass;
- hostile domain mutations are caught;
- original core production, independent curvature/rank, and 11 hostile checks remain green;
- fresh repair-only external follow-up is required before closing the caveat.

