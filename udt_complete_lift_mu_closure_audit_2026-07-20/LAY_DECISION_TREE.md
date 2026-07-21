# Lay decision tree

## What we tested

We tried every currently registered way of extending the finite-cell mirror through the two angular
directions. We allowed the clock/radial and angular coordinates to mix wherever mirror parity permits
it. We then tested both candidate mixing amounts, `mu=4` and `mu=9`.

Every mirror extension accepts both.

## Why repeated mirror composition cannot help

After the local clock and ruler have been normalized, the mirror looks exactly the same for every
value of `mu`: keep the clock direction, reverse the radial direction.

The value of `mu` remains in how reciprocal dilation acts relative to that clock/ruler frame. It is
not written on the mirror itself. Combining mirrors therefore cannot recover information that each
mirror no longer contains.

This is why orientation, an even number of mirror reversals, corner angles, and cap-lattice integers
all fail to choose `mu`. They classify how pieces are glued, not the metric amount of reciprocal
mixing inside each piece.

## Does the Hopf option help?

Not yet. Its local exchange mirror also accepts both `mu` values. Globally, Hopf/S3 closure becomes
unique only after extra spatial-period and cap assumptions are supplied. Those integer closure rules
still contain no equation for `mu`.

## What is actually missing

We now need a global rule that depends on the metric, not just on mirror bookkeeping. Such a rule
might eventually involve smooth global regularity, metric holonomy, a boundary equation, or a
derived bootstrap functional. The repository does not currently contain one.

So this path is closed cleanly: more algebra with the existing mirror group will not determine the
remaining number.
