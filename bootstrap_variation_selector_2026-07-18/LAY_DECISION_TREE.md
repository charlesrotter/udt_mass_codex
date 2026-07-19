# Lay decision tree — what bootstrap currently selects

Start with the exact role assigned to bootstrap.

```text
Is bootstrap only a condition on which completed global solutions are physically realized?
|
+-- Yes --> It filters completed solutions but does not say which variables were varied
|           or which local equations generated them. Pre-scale-first and post-scale-first
|           constructions remain possible.
|
+-- No; bootstrap is part of the off-shell variational law --> Which role is derived?
            |
            +-- A varied global constraint --> Derive its functional, multiplier equations,
            |   boundary terms, and allowed variations. This may change the equations but
            |   does not automatically choose C-squared or EH.
            |
            +-- A representative-selection map --> Prove that it exists, is unique and
                differentiable, and respects the finite cell. A selected metric permits a
                post-scale action but still does not choose EH.
```

Then ask whether a two-stage bridge exists.

```text
Was a physical representative selected?
|
+-- No --> No post-scale bridge has started.
|
+-- Yes --> Was a separate matching theorem derived that maps fields, variations,
            principal operators, sources, and finite-cell boundary generators?
            |
            +-- No --> Representative selection only; bridge remains OPEN.
            |
            +-- Yes --> Does the controlled regime actually produce the claimed
                        post-scale law with normalization and error bounds?
                        |
                        +-- No --> Conditional bridge proposal only.
                        |
                        +-- Yes --> A scoped effective bridge may be reported, without
                                    promoting it beyond its regime or deriving a carrier.
```

The present record stops at the first tree. Bootstrap is a global realized-solution principle with
no declared off-shell role. The derivation therefore returns `UNDERDETERMINED`: neither pre-scale nor
post-scale variation is selected, and no two-stage bridge is derived.
