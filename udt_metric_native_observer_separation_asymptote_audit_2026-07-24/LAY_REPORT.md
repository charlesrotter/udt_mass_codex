# Lay report

Yes: the metric contains a direct way to calculate the distance associated
with clock dilation, and it does not require the old `tanh` assumption.

The important quantity is how quickly the dilation field `phi` changes per
unit of actual spatial distance. The metric measures that rate—including
the angular geometry and all the cross-couplings we have called the
“orchestra.”

- If `phi` changes rapidly per unit distance, an infinite amount of clock
  dilation can be packed into a finite distance.
- If it changes too slowly, the distance to infinite dilation is infinite.

Mathematically, the distance increment is:

```text
distance increment
  = phi increment / metric-measured spatial steepness of phi.
```

Adding those increments all the way to infinite dilation gives the
asymptotic reach.

This produces a clean test for every complete metric solution. It also
shows why `tanh` should not be assumed: `tanh` is only one possible
distance-versus-dilation curve.

In the old restricted WR-L metric, the direct proper-distance calculation
does something particularly clear:

```text
clock dilation -> infinity
proper radial distance -> 2X
coordinate radius -> X
optical depth -> infinity
```

Those are different measurements of the same geometry. The proper distance
is not the old `X tanh(phi)` quantity.

What is still missing is global rather than local. The greatest possible
distance between any two observers also depends on the angular shape and
topology of the whole universe. Two geometries can have exactly the same
clock-dilation law in the depth direction but different widths around the
angular directions, giving different maximum pair separations.

So we have not calculated the final numerical `X_max` yet. We have done
something immediately upstream and more useful:

> We now have the exact metric formula that will calculate it from any
> complete branch, and a precise test telling us when one universal
> distance-versus-dilation law exists.

The next job is to apply that test to every surviving complete finite-cell
branch. Branches where the angular sectors make the result vary around a
single `phi` level cannot support one universal `X_max` through this route.
For survivors, we integrate the distance and then compute the full global
diameter.
