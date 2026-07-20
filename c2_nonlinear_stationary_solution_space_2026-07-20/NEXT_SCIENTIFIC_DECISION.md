# Next Scientific Decision

The bounded nonlinear census found one broad round basin but left 51 preregistered attempt basins
unresolved. Forty-eight of those 51 begin at coefficient norm `0.20`, whereas almost every norm
`0.05` seed returns to round. That pattern is a solver-completeness question before it is physics.

The next bounded action should use pseudo-arclength or homotopy continuation along the exact failed
seed directions, starting from their certified small-amplitude neighbors and increasing amplitude
without changing the equations. It should group symmetry-related directions, retain all folds and
runaways as characterized output, and directly evaluate the full Bach residual on any nonround
reduced root. A turning point, loss of regularity, or second branch would then be visible rather than
hidden behind a failed Newton step.

This package does not authorize that continuation. It also does not authorize a GPU sweep, physical
boundary choice, coframe selection, other action, carrier, scale, mass, or startup-control edit.
