# G146 fresh adversarial review

Date: 2026-08-17

Verdict:

```text
PASS__BOUNDED_TO_NONUNIQUE_POSITION_PROJECTIONS__COMPLETE_ARROW_AND_SCREEN_SOLDER_OPEN
```

## Independent rerun

A fresh read-only context copied the package to a temporary mirror and reran all three routes:

- production exact algebra: `47/47`;
- independent `Fraction`/`Decimal` replay: `31/31`;
- package/source verifier: `48/48`.

The regenerated artifacts matched the repository artifacts exactly:

```text
DERIVATION_RESULT.json
ef0db5a69f35ba556f84fa2b4c147b9783aebab4546144ac02f0cb3288071c48

INDEPENDENT_RESULT.json
4ad6c54c7877d6f9cef079f339619f2a5bcf8478ff5958a74ed07c6d5b9c7985
```

## Adversarial findings

1. The two formulas are smooth and closed on the open ball; the global gap identities,
   `SO(3)` covariance, collinear reduction, and exact inequivalence witness are correct.
2. They refute uniqueness only in the declared class of **position projections** with identity,
   two-sided element inverse, closure, covariance, and the G137 collinear law. They do not refute
   uniqueness of a fully typed reversible or associative observer-arrow lift.
3. The reverse-order defects correctly expose that bare position projections do not own complete
   arrow reversal.
4. Boost-product nonsymmetry supports only a nontrivial rotation factor in the standard control
   factorization. It does not identify UDT depth with rapidity, select a ball law, or derive a
   physical screen rotation.
5. The positive three-space is supplied. No-center does not derive isotropy.
6. The registered third vector is parallel to the natural rotation axis and therefore supplies no
   general associativity result.
7. The proposed next joint is correctly staged: first derive a rank-two carrier solder
   `sigma:T_xi S^2 -> H_AB` from one complete metric/query, then compare the conjugated positional
   gyration with metric transport. No equality is presently claimed.

No repository file or protected package was modified by the reviewer.
