# G127 lay report

This is the clean “same instrument, different listening position” result we were looking for.

Take one nonlinear UDT metric and one regular event away from the center. A ray aimed along the
metric's symmetry-radial direction sees a round local screen. Tilt the ray at that same event and
the same metric curvature naturally stretches the two screen directions by different amounts.

That radial control agrees with the kind of isotropy established in G119, but this calculation does
not pretend that its finite-radius vertex is literally G119's center-vertex observer.

Nothing was bolted on. There is no separate angular formula, response amplitude, fitted
coefficient, or second history. The distortion is calculated from the same `phi`, its derivatives,
and the same curvature tensor that produced the radial view.

The precise local difference between the two **tidal curvature eigenvalues** is

```text
sin(alpha)^2 * Xi,
Xi = T - U + V - W,
```

where `alpha` is how far the query tilts away from radial and `T,U,V,W` are four adapted curvature
readings of that one metric. This tidal difference creates a Jacobi-map difference cubic in affine
distance. The actual optical shear is then calculated from `D' D^-1`; its leading difference is
`-lambda sin(alpha)^2 Xi / 3`.

This does not yet tell us which metric history Nature chose, nor does it reproduce the R5 angular
curve. It establishes the missing architectural point: radial and angular behavior can emerge as
different views of one metric rather than separate fitted sectors. SNe remains only a later
comparison check on the combined radial/redshift-facing prediction.
