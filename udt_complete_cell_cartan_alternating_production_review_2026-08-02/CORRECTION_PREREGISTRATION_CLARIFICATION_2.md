# Second clarification — symmetric difference is not an additive count

Date: 2026-08-02

The first clarification described the eight-row symmetric difference as “eight additional” forward
rows. That inference was incorrect because the failed assertion printed a set symmetric difference,
not the forward count.

The independently computed exact situation is:

```text
FORWARD mixed rows = 12
REVERSE mixed rows = 12
symmetric difference = 8 identities (4 forward-only and 4 reverse-only)
narrow leg-aligned nonzero rows = 0 under both pivots
```

This strengthens the intended normal-form warning: the total raw mixed-row count happens to agree,
but four row identities move when the exact scalar-closure equations are solved in the opposite
direction. Neither the count nor the row placement is a tensorial mixed-curvature invariant.

The first clarification remains historical evidence of the failed interpretation; this layer
supersedes only its “eight additional” arithmetic wording.

