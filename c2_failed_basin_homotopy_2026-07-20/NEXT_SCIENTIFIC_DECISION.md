# Next Scientific Decision

The homotopy closes 29 former failures to round and leaves exactly 22 order-four paths unresolved.
Those 22 now have saved coefficient/tangent checkpoints, so the next solver-completeness test need
not repeat the first part of any path.

A future bounded dispatch may restart only those exact 22 paths from their final verified states,
use arclength rather than wall time as the primary stopping coordinate, and preserve every fold.
Symmetry-related even/odd-shift paths should be compared before spending on all copies.  Any path
reaching `lambda=0` must retain the same endpoint and direct Bach gates.

That continuation is not authorized by this package.  Nor is a GPU sweep: the present code is
fourth-derivative, small-matrix, CPU-dominated and would need an independently verified vectorized
implementation before GPU use could improve evidence rather than merely throughput.

The other honest choice is to stop chasing solver paths and move outward to a different completeness
layer—physical boundary completion or higher/nontoric metric modes.  The current result does not
select between those priorities.
