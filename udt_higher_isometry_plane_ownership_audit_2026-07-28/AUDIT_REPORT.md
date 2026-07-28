# Higher-isometry Killing-plane ownership audit

Date: 2026-07-28

Preregistration: `3e3eecc`

Final grade after an initial refutation, correction, and fresh corrected review:
`VERIFIED-WITH-CAVEATS_BOUNDED_UNIVERSAL_NONSELECTION_AND_IDENTITY_ROBUSTNESS`

## Result first

The complete metric does **not** universally select the registered reciprocal plane in the
admitted higher-isometry family. An exact smooth, complete, nonconstant-depth metric contains two
isometry-equivalent free reciprocal planes, so universal ownership is refuted.

For an arbitrary extra compact circle `Y`, every candidate observer/ruler subgroup is scanned as

```text
span(K+rV+sY, mV+nY).
```

Only `span(K,V)` keeps its reciprocal two-area constant as an identity under independent variation
across the entire free `(u,f,b)` configuration family. This is a real robustness result, but it is
not a generic fixed-metric theorem. A fixed cohomogeneity-one metric traces a single curve through
`(u,f,b)` space, along which derivative terms can cancel. Generic fixed-profile uniqueness remains
open.

The smooth countercontrol is a twist-off toric `S3` metric for which both the Hopf and anti-Hopf
free circles form exact reciprocal planes with the same clock. Smooth `S3` toric topology cannot
choose between them: every unimodular two-cap completion has exactly two unoriented primitive free
circle lines.

## A second distinction exposed by the complete metric

The whole three-direction Gram response and the scan of its two-direction symmetry subgroups are
not the same operation. When the extra circle's connection moment varies, the full `3 x 3` response
mixes `span(K,V)` into the extra direction. The restricted plane calculation instead establishes
family-wide identity robustness of `span(K,V)`. Both results are exact; neither may be substituted
for the other, and neither completes the missing fixed-profile selector.

Higher symmetry neither destroys the reciprocal pair everywhere nor leaves it universally unique.
The complete response degeneracy atlas preregistered for this audit also remains unfinished.

## Honest classification

```text
UNIVERSAL_SELECTION_REFUTED__FAMILY_IDENTITY_ROBUSTNESS_DERIVED__
GENERIC_FIXED_METRIC_SELECTION_OPEN
```

- `DERIVED`: principal-orbit `3 x 3` Gram form, determinant, inertia, response polynomial, and
  mixing for `b>0`.
- `DERIVED`: all-projective symmetry-plane determinant and clock-response formulas.
- `DERIVED IDENTITY LEVEL ONLY`: `span(K,V)` is the only constant-area plane robust under
  independent variation across the whole free `(u,f,b)` family.
- `DERIVED`: exactly two free unoriented toric circle lines for smooth two-cap `S3` topology.
- `DERIVED EXISTENCE`: smooth nonconstant-depth twist-off metric with two reciprocal free-circle
  planes.
- `REFUTED BOUNDED`: universal registered-plane selection.
- `OPEN`: generic fixed-profile uniqueness, the exhaustive response-degeneracy atlas, which branch
  a physical UDT solution occupies, and whether an equation or bootstrap closure selects it.

The fact that nonzero `alpha` distinguishes the registered pair in the explicit double-plane
witness is geometry, not a physical selection of nonzero `alpha`.

## Evidence gates before final banking

1. **Preregistered:** yes, commit `3e3eecc`, before the orbit response and countercontrol were
   calculated.
2. **Full or bounded:** the algebraic plane parameterization is complete for every projective
   `R x S1` subgroup in the descended stationary `R x T2` orbit algebra, and the free-circle theorem
   is complete for the smooth unimodular two-cap `S3` lattice. The fixed-profile solution strata and
   full response degeneracies are not complete.
3. **Independent:** 31 production symbolic checks plus 104 production cap checks; a separate
   standard-library `Fraction` implementation reconstructs the load-bearing matrices and formulas
   and checks 232 larger-range cap bases. The first hosted adversarial review returned `REFUTED` on
   the genericity quantifier; its exact criticism and this correction are preserved. The corrected
   hosted review returned `PASS_WITH_CAVEATS`; all three bookkeeping caveats are closed in
   `CAVEAT_RESOLUTION.md` without changing the bounded scientific conclusion.
4. **Premises:** every fixed domain, symmetry, topology, and dropped physical object is recorded in
   `PREMISE_LEDGER.tsv` and `COMPLETENESS_MAP.md`.

## Maximum conclusion

Within the bounded stationary descended higher-isometry family, universal plane selection is
refuted by an exact smooth nonconstant-depth countercontrol. The orbit algebra, topology theorem,
and family-identity robustness of `span(K,V)` are derived. Generic fixed-metric selection and the
complete response-degeneracy atlas remain open. No macro/micro regime, physical branch, action,
source, carrier, density/bootstrap law, dynamics, or mass emergence is selected.
