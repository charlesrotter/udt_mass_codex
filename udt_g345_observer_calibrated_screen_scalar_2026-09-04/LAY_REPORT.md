# G345 lay report

G344 found a precise number describing how a very narrow bundle of neighboring paths changes
between two endpoints. But that number still depended on two bookkeeping choices: how quickly we
counted steps along the path, and how we labeled the two sideways directions at each endpoint.

G345 finds that the metric already supplies exactly the missing bookkeeping corrections:

- the two endpoint observers' clock readings remove the arbitrary path-step scale;
- the metric's two endpoint screen areas remove arbitrary sideways-coordinate scale and skew.

After those cancellations, both directions of the same comparison give the same positive scalar.
The scalar also joins consistently across an intermediate endpoint, provided the intermediate
screen is eliminated with the required stationary joining factor. Simply multiplying the two
segment numbers is wrong.

This is useful progress toward metric-owned geometric light propagation: the result no longer
depends on an arbitrary ray parameter or screen coordinates. It is still only the geometry of one
supplied observer pair and one supplied labelled ray in one supplied spacetime. It is not yet
brightness, luminosity, flux, probability, observational distance, or a theory of light, and it
does not choose a path, universe, scale, or `X_max`.

A fresh external reviewer independently checked the formulas and replayed the evidence, then
accepted this bounded result. It noted a few weak bookkeeping assertions in the test harness, but
found no defect in the mathematical result. Those test-quality cautions remain visible.
