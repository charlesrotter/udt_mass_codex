# G351 lay report

Date: 2026-09-05
Status: internally reproduced; external review pending

## What changed

Charles provisionally added one new rule: in an empty region, the amount assigned to a fixed set of
ray labels is carried forward without being created or destroyed.

This did not change the metric or reciprocal kernel. The metric still determines how ray bundles
spread or focus and how endpoint clocks compare.

## What follows

Imagine drawing permanent labels on a smoothly filled collection of rays. If those rays spread
over twice the area while carrying the same total amount, the amount per unit area is halved. If
they focus into half the area, the density doubles. Therefore the area part of a smooth nonzero
density is no longer arbitrary: it must be inverse area.

```text
measured transfer = (frequency change)^p / (area change).
```

The exponent `p` is still open. It says what kind of observer readout is being discussed. A bare
amount, an amount whose measured value changes with clock rate, and a rate per observer time are
different quantities. Conservation alone does not decide among them.

There is one important boundary. The conserved content could include concentrated point-like or
singular pieces rather than a smooth spread. Such a piece is still carried by its labels, but it
has no ordinary amount-per-area function and therefore no ordinary area exponent. The inverse-area
result applies to the smooth, absolutely continuous part wherever that density is nonzero. Zero
content stays zero but cannot reveal an exponent by itself.

## Why caustics do not break the rule

At a focus, the local area can shrink to zero and density can become infinite. The conserved total
does not have to become infinite. We retain the amount on the permanent ray labels rather than
dividing by zero. Past the focus, the same labels continue. If several labelled rays land at one
place, the mathematical measure remembers all of them even though the geometric outline of the
image does not.

This does not decide whether a physical detector adds, cancels, or interferes contributions from
different paths. Such a rule would require more structure.

## What remains missing

The result does not create light or any other content. It does not choose which rays are populated,
how much is emitted, what `p` is, what a detector measures, or how different path families combine.
It is therefore not yet a brightness, luminosity, or SNe prediction.

The advance is precise: after the newly adopted provisional conservation premise, the area weight
of any nonzero smooth regular density is fixed. The remaining smooth-density ambiguity has been
reduced from two exponents `(p,q)` to one exponent `p`, plus the still-supplied source and
population data. Singular carried content remains measure-valued rather than density-valued.
