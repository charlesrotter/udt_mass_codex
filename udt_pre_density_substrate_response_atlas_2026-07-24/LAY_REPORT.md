# Lay report

We found something genuinely constructive.

The angular part of the UDT metric is not just a collection of separate knobs.
On the branches where its two angular directions close into a two-dimensional
torus, the metric already provides:

1. the shape of that torus; and
2. rules for transporting positions around it.

The first idea we tested was whether the torus's locally “long” or “short”
axis directly becomes the phase used by the Hopf structure. It does not. That
axis depends too much on how the local chart is drawn.

But the finite torus has an integer wrapping grid. That grid lets us ask a
chart-honest question: which primitive phase winding is geometrically
shortest? The metric answers that question. Usually there is one shortest
winding direction; sometimes two tie.

On our frozen 25-point map:

- 22 points had one distinguished winding direction;
- 3 were exact tie points;
- the result transformed correctly under every tested relabeling of the torus
  grid.

The cleanest result occurs with no angular shear. On one side of `phi=0`, one
angular winding is shortest. On the other side, the reciprocal winding is
shortest. At `phi=0` they tie. That flip follows directly from the metric.

This does **not** yet give us a particle. It gives us a natural geometric
candidate for “which phase direction matters,” plus the metric's existing
connection for transporting that direction. We still need UDT to say whether
this shortest direction is physically selected, how ties are handled, and
which actual phase value or matter field occupies it.

The bootstrap idea is now less vague: the global universe could influence the
local torus shape; the local shape changes which integral phase direction is
distinguished; and a conditional Hopf field would respond to that direction.
The missing link is the law that makes this geometric candidate physically
operative and relates global conditions—possibly later including total
density—to the local torus geometry.

