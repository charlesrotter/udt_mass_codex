# Lay report

This audit found that the “missing angular rotation” was partly the wrong problem.

In the developed complete twisted-`S3` geometry, the metric itself identifies the clock direction,
the ruler direction, and therefore the two-dimensional sheet perpendicular to both. That sheet is
global across the whole cell.

The metric's finite reciprocal scaling treats every direction in that sheet equally. Consequently,
we can rotate the two measuring sticks drawn inside the sheet without changing the metric at all.
The metric does not need to choose one stick as “the” angular axis.

It also gives a natural steering rule for the sheet: project the metric's ordinary connection back
onto the sheet after each infinitesimal step. This tells a screen frame how to rotate along a chosen
path. It is geometric and frame-covariant.

But the sheet is not rigidly parallel inside the full four-dimensional geometry. Ordinary metric
transport tilts it into the clock/ruler directions, and going around a loop can return a different
four-dimensional orientation. The projected steering rule corrects back into the sheet, so it is
path-dependent; it does not provide one universal compass direction or an endpoint-only answer.

In short:

```text
global screen: yes, on the registered complete twisted branch;
finite metric lift without an angular flag: yes;
metric-derived screen rotation connection: yes, along a supplied path;
globally selected angular axis: no;
ambient parallel or path-independent complete lift: no;
physical branch or law selection: still open.
```
