# G184 preregistration terminology clarification

Date: 2026-08-19

The preregistered phrase `KERNEL_EVALUATION_IS_NOT_FAITHFUL` used “faithful” in the informal sense
of “does not uniquely recover a realization.” In category theory, faithfulness properly means
injectivity on each morphism set. The fixed semicircle/helix and covering witnesses instead test
whether the completed pair output is a **complete invariant**, equivalently whether it separates
typed realization-isomorphism classes.

Before assembling or banking any result, the landing label is therefore corrected to

```text
TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT
```

No arena, equivalence definition, witness, computation, falsifier, physical-choice ledger, or
maximum conclusion changes. G184 makes no claim about injectivity on abstract hom-sets.
