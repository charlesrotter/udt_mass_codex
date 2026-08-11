# Pre-review report — co-present causal pair selector

Date: 2026-08-10
Preregistration commit: `86380447`
Current grade: `LEAD`

## Candidate result

On a supplied regular calibrated pair family, the complete shifted cone derives

```text
center=-beta,
half-width=exp(2 phi_pair),
c_eff^(pair)/c_E=exp(-2 phi_pair).
```

The complete pair metric retains time, angular, shift, and mixing dependence before readout.
Induced local causal preservation is automatic after the pair immersion is supplied and does not
select it. In local null coordinates, every smooth time-oriented causal diffeomorphism in the
identity component is

```text
u'=f(u), v'=g(v), f'>0, g'>0,
```

with a second component exchanging the null branches. Calibration at one observer, composition,
Reciprocity, and both infinite-depth limits leave explicit nonidentity families. The proposed
landing is therefore exact conditional causal/reciprocal unification plus local nonselection.

## Current gates

- symbolic derivation: `33/33`;
- independent standard-library reconstruction: `58/58`;
- catch-proofs: `16/16`.

## Primary review risks

- whether the local causal-map classification is genuinely exhaustive in the declared class;
- whether time orientation and null-branch exchange were typed correctly;
- whether `phi_pair` is really the centered cone opening with nonzero shift;
- whether the causal immersion statement is tautological but correctly scoped;
- whether the global-hyperbolicity counterfamily proves nonselection rather than only coordinate
  redundancy;
- whether global causal faithfulness is a meaningful open condition without being silently posited;
- whether any active UDT premise removes the `f,g` freedom.
