# G343 lay report

Date: 2026-09-04
Status: externally accepted bounded result

G342 told us how a very small bundle of neighboring rays changes size when all of those rays start
together at one event. G343 asks the more complete question: if the bundle already has some width
and some opening direction at one point, can the metric carry both pieces of information to any
other point—and can several legs be joined without contradiction?

Locally, yes. On this one exact supplied spacetime, the metric gives one complete four-part rule:
two numbers say where the neighboring ray is on the screen, and two say which way it is heading.
The rule has three strong consistency properties:

1. Going from A to B and then B to C gives exactly the same result as going directly from A to C.
2. Reversing the mathematical transport exactly undoes the forward transport.
3. A conserved screen-area-in-position-and-direction quantity is preserved. This is the ordinary
   geometric Wronskian of the ray-deviation equation, not a claim about physical light intensity.

There is one subtlety. Each endpoint can reset its own affine clock so that the ray frequency is
called one there. Those two derivative units are generally different. If we compare them as though
they were the same, reciprocity appears to fail. Once the units are converted, the factor required
is exactly the metric's already-known frequency ratio between the endpoints. Nothing new was fitted
or added.

The first calculation draft accidentally hid a reference time by writing it as the number one. We
caught that before banking, discarded those runs, made the reference event explicit, and tested
that moving it changes only the bookkeeping—not the propagator. This is an important anti-scaffold
check: the result does not choose a physical time or distance scale.

The corrected production checks passed `8888/8888`; a separate direct-curvature and numerical
integration route passed `2960/2960`; and all 13 hostile mutations were caught. A fresh external
reviewer authenticated the sealed package, replayed its checks, ran another scratch reconstruction,
found no issue at any severity, and accepted the bounded result without repair.

What this does not do: it is not yet a brightness prediction, a luminosity distance, a selected
signal path, or a populated universe. It adds a complete and internally consistent geometric
transport layer on one supplied exact spacetime. Distinct compact windings remain distinct path
labels, and no scale, `X_max`, matter law, stability theorem, or canon claim follows.
