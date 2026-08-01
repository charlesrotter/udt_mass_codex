# Lay report

We found a more exact version of the missing-table-leg problem.

The earlier calculation had two ways to treat the angular part of the candidate structure:

- leave its edge free, and the central shape has one way to collapse;
- hold its edge tightly, and that particular collapse disappears—but the instability moves into a
  second, previously adjustable wall direction.

This audit gave the first support an ordinary adjustable test stiffness. Eliminating its internal
motion produces the continuous response used in the calculation: zero stiffness is the free edge,
while a perfectly pinned edge is reached only in the infinite-stiffness limit. We then calculated
what the second support would have to do.

The result is clean. Before a definite threshold, the angular support is too weak and nothing done
to the second support can save the shape. Exactly at the threshold, the two motions are coupled in
a way that no finite second support can fix. Above it, there is a precise minimum strength for the
second support. The stronger the angular support becomes, the less of the second support is needed.

So the apparent instability is not random, and it is not just one missing coefficient. The
geometry says a successful closure would need two coordinated responses. We now know their exact
conditional tradeoff for this candidate and these four local domains.

What we did **not** find is the law that supplies those supports. We did not choose a boundary,
action, carrier, or bootstrap rule. This is a blueprint for what such a law must accomplish, not a
claim that UDT matter is stable.
