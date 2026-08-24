# G245 map — metric-owned observer null-cone field

Date: 2026-08-24

## Whole question

G244 derives the angular area/shape instrument on a **supplied** regular null sheet. G245 asks the
more native prior question:

> Given a smooth time-oriented Lorentz metric, one observer event, and that observer's unit clock,
> does the metric itself generate the local direction-labelled null sheet on which the G244 field
> lives?

This is metric-led. It does not target an observed angular feature or a fitted response.

## Pure and easy routes

- **Pure route used here:** construct every normalized null direction at the observer, apply the
  metric exponential map, and derive the full matrix Jacobi/area/shape field before any source or
  detector is introduced.
- **Easier route rejected as the primary derivation:** choose a radial shell, source catalogue, or
  fitted angular control and evaluate G244 only there. That would answer a later operational
  question while leaving local geometric ownership hidden.

## Expected mathematical object

For observer event `o`, unit future timelike velocity `U`, and unit spatial direction
`n in U^perp`, the normalized future null vector is

```text
k(n)=U+n,
g(k,k)=0,
-g(U,k)=1.
```

The candidate local sheet is the direction-labelled null exponential map

```text
F(lambda,n)=Exp_o(lambda k(n)).
```

No endpoint is selected. The entire local cone is returned. The angular derivative of `F` should
be the G188 vertex Jacobi map, making G244's `H`, `A`, and `C` the induced angular geometry of its
regular cross-sections.

## Bounded regime

- smooth time-oriented Lorentz four-manifold;
- one supplied observer event and metric-unit future clock;
- all celestial directions, not a preferred ray;
- the maximal local exponential domain ray by ray;
- regular finite noncaustic pieces for normalized shape;
- full phase retained at caustics.

Cut points, self-intersections, conjugate points, geodesic incompleteness, multiple images, global
branch aggregation, source incidence, detector response, and observational outcomes are classified
but not solved.

## Maximum possible conclusion

The metric and observer germ own the local direction-labelled null-cone geometry and its G244
area/shape evolution. They do not own source population, detector semantics, a global endpoint
quotient, a physical cosmological history, or an observed sky pattern.
