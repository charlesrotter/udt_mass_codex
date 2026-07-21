# P01 in plain language

We built and checked the ruler that will be used to explore the complete UDT metric.

The ruler accepts the metric at one location, plus how every one of its components is changing in
every direction and how those changes are themselves changing. It does not assume the geometry is
round, static, diagonal, or free of angular mixing. In the optional `2+2` bookkeeping view, it keeps
all ten metric components alive, including the four terms that mix the two sectors.

It correctly computes the local geometric consequences: inverse metric, volume/determinant,
connection, curvature, and the equivalent frame/Cartan description. It also keeps track of how those
quantities behave when we change coordinates, rotate or boost the local measuring frame, or apply
UDT's Common-Scale rescaling.

The main implementation passed 36 checks. A separately written verifier passed 15 independent checks
and 33 deliberate corruption tests. A fresh adversarial review found no remaining blocking problem.

What this did **not** do is discover UDT's solutions. It did not choose the reciprocal plane, decide
what `phi` is inside the full metric, select an action, or find matter. It gives us a trustworthy,
non-myopic instrument for that exploration. The next mapped stage, P02, would characterize local
metric-jet possibilities with this instrument, but it requires separate authorization.
