# G195 lay report

## What changed

G194 had turned on every **symmetric** two-dimensional screen distortion in the bounded metric
family: stretching, squeezing, shear, sign changes, and rotating principal axes.  G195 turned on the
first omitted **antisymmetric** degree of freedom—the part that rotates the screen itself.

## What the metric did

The rotation did not appear as another independent magnifying or focusing knob.  The metric put it
in the screen connection: it tells us how the measuring screen must rotate while it is carried
along the observer-pair relation.

When the calculation is expressed in that genuinely parallel-carried screen, the focusing equation
returns to the same form found in G194.  Rotation still matters when anisotropic strain is present,
because it changes which direction of the strain the carried screen sees.  But pure rotation by
itself does not change the observed area.

## Gears versus free knobs

This closes one more set of gear ratios:

- the metric fixes the rotation connection;
- the connection fixes the parallel screen;
- the parallel screen fixes how rotation and symmetric strain combine;
- the ordered matrix evolution fixes the Jacobi map;
- the Jacobi map cannot form a nonvertex caustic anywhere in this bounded family.

What remains free are the **profiles** `a(eta), A(eta), N(eta), B(eta), R(eta)`.  G195 did not choose
how loud those functions are at each distance or regime.  It showed that once they are supplied by
the metric history, they do not act as five unrelated post-processing controls: their coupling in
the observer-pair response is fixed.

## Evidence

- 22 exact symbolic metric/connection/curvature identities passed.
- A separately coded 266-history census passed 5,059 assertions.
- The largest direct metric-derived tide error was `1.1369e-13` against a `3e-8` ceiling.
- The largest screen-connection error was `2.9367e-15` against a `3e-8` ceiling.
- All 18 deliberate corruptions were caught.
- Fresh external review independently confirmed the load-bearing algebra. Its final repair retry
  completed two strict no-write replays with exact saved-result identity and no changed evidence.

## Honest limit

This is a theorem for one displayed complete-coframe family and one central outgoing observer-pair
germ.  It is not yet a theorem for every complete UDT metric, every observer pair, spatially varying
mixing, global topology, or a physical profile.  It does not use or derive SNe, BAO, CMB, transfer,
`X_max`, dynamics, matter, or source physics.
