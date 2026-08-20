# G190 lay report

## What changed

We did not return to the old G116 model.

The completed observer pair already contains a local clock direction and a local ruler direction.
Together they determine the two possible lightlike directions—outward and inward. Once we choose
the orientation, the metric carries that ray forward.

The same trip through the metric produces two readings:

1. how the ray's frequency compares between the endpoint clocks; and
2. how a tiny bundle around the ray expands, contracts, or shears on the observer's screen.

So we no longer need to bolt a chosen radius-versus-redshift curve onto the calculation. A supplied
time-live metric produces a path through a graph whose coordinates are frequency and apparent
area. If frequency changes steadily, that path becomes an ordinary area-versus-frequency curve. If
frequency turns around, the honest result has multiple branches instead of one forced curve.

## Why this is more native

All the instruments enter through the complete metric before the ray and screen are propagated.
There is no P1 chord, fitted angular coefficient, static `phi(R)` shortcut, or `X_max` input in the
core calculation. G116 is used only afterward to confirm that its valid near-center limit is still
reproduced.

## What remains conditional

We still have to supply the complete metric history and the actual observer family being sampled.
The calculation does not yet provide a native theory of emission or radiative transfer. It gives a
cleaner geometric engine on which those later observational bridges can be tested.
