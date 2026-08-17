# G135 lay report

The orchestra has produced a clean chord.

After every part of the metric—clock, ruler, angular screen, mixing, and the actual observer-pair
orientation—has contributed to the pair geometry, that geometry has two positive readings: a clock
reading `T` and a ruler reading `L`.

There are two natural ways to combine them:

- their overall size, which remembers scale;
- their normalized imbalance, `(L-T)/(L+T)`, which remembers reciprocal shape.

That normalized imbalance is exactly `tanh(phi_pair)`. More importantly, it is already hiding in
the original reciprocal kernel: when the clock/ruler basis is rotated into “together” and “against
each other” channels, the imbalance is the slope of the resulting ray. We did not choose `tanh`
because it gives a convenient ceiling.

It has the right skeleton for the `X_max` picture:

- coincidence is zero;
- reversing the ordered comparison changes the sign;
- finite pairs stay between minus one and plus one;
- infinite reciprocal dilation approaches the endpoints without reaching them;
- successive comparisons use the same fractional rule familiar from rapidity and bounded velocity.

But one honest joint remains. The math gives a canonical **anchored projective chart/readout**. The current
premises do not explicitly say that Nature calls this chart physical separation. Smoothly bending
the markings between the same three anchors preserves the underlying reciprocal geometry.

So the smallest possible completion is now very plain: clarify that UDT positional comparison means
the anchored projective reading of the complete clock/ruler pair. If Charles adopts that as the
intended meaning of the founding postulate, then

```text
separation/X_max = |tanh(phi_pair)|
```

follows; `tanh` itself is not a fitted add-on.

That still does not tell us the number `X_max`. `c_E` converts time and length but does not create a
standalone length. Nor does this scalar replace the full metric: it deliberately ignores common
scale and other pair information.

In short: we have uncovered a native bounded projective readout inside the completed reciprocal
kernel. We have not yet proved that this readout is the universe's operational distance ruler or
determined the ruler's total length.
