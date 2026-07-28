# Lay report

We checked whether the current metric is ready to be put into an ODE solver
without borrowing old equations.

It is ready for one kind of ODE but not the other.

If someone hands us a complete candidate geometry, the metric tells us exactly
how an observer, direction, screen arrow, or small neighboring path moves
through it. Those are honest transport ODEs. They can show bends, twists,
caustics, path dependence, and holonomy.

But the metric does not yet tell the candidate geometry itself how to change.
In the current bounded chart there are eight independent knobs. Geometry tells
us what connection and curvature result from turning those knobs, but it does
not yet supply an equation saying which settings or changes are realized.

The distinction is like having exact rules for how a test cart rolls over any
landscape while still lacking the rule that formed the landscape. Simulating
the cart is legitimate. Simulating the landscape would require us to invent a
terrain-forming rule.

This explains some of the circling: algebra has repeatedly calculated what a
chosen geometry does, while the missing object is the rule selecting or
assembling the geometry. Coarse numerics can still help, but first as an
unbiased transport/stratification atlas over freely supplied geometries—not as
a claimed time evolution of the UDT universe.
