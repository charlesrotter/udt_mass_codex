# Post-preregistration generator-scope clarification

Date: 2026-07-24

State: conservative scope correction before banking

The preregistered scalar-generator test compares

`A_J=[[0,1],[-K,0]]`

with

`A_R=diag(-a,a)`

by a pointwise real intertwiner in the natural parallel screen frame. Its
exact condition is a local algebraic/connection-preserving condition.

An arbitrary path-dependent matrix `H(lambda)` can instead be defined after
the two propagators are already known by solving

`H'=A_J H-H A_R`.

That construction is not a metric-selected solder: it requires initial
`H`, depends on the retained path/trivialization, and exists by ordinary
ODE transport rather than by a local invariant reduction.

Accordingly, F07 and every WR-L obstruction in this package mean:

`NO_POINTWISE_NATURAL_FRAME_GENERATOR_SIMILARITY`.

They do not claim that no path-dependent change of variables can ever be
written. The universal intrinsic solder remains `OPEN_NO_REGISTERED_WITNESS`,
not globally refuted.
