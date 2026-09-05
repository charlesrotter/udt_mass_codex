# G349 map — finite null-wavefront patch area

Date: 2026-09-04
Status: outcome-unseen preregistration

## Whole question

Starting only from G348's metric-derived infinitesimal null-screen Jacobian, determine exactly what
finite geometric area information follows for a supplied compact patch of future null directions.
The finite map is the null-exponential/wavefront map obtained by following every supplied ray to a
supplied smooth affine cut. Caustics, folds, self-overlap, repeated sheets, and path labels remain in
the domain rather than being rejected.

This is `METRIC_LED` and observing rather than targeting. It asks what the metric's exact ray map
does. It does not seek brightness, a distance curve, a preferred history, or an observational fit.

## Exact bounded arena

- a supplied smooth time-oriented four-dimensional Lorentzian metric `g`;
- a supplied source event `p` and finite future unit timelike source observer `u`;
- a supplied compact piecewise-smooth celestial patch `U` on the observer's sky;
- the complete supplied family of future null geodesics from `p` labelled by `U`;
- a supplied positive smooth affine cut `tau(n)` lying inside the regular existence domain of every
  ray in `U`;
- the exact map `F(n)=gamma_n(tau(n))`, including every critical point and repeated image;
- optional supplied source/target orientations and separately retained path labels.

No injectivity, pre-caustic restriction, field equation, symmetry, topology, global history, or
observer population is assumed. Compactness and regular existence are domain conditions, not
filters on the image shape.

## Pure and easy routes

- Pure route used here: derive the differential of `F` from geodesic variation, quotient out the
  longitudinal cut term, and apply the coordinate-free area formula to the metric two-Jacobian.
- Easier but insufficient route: multiply one representative G348 area by a patch solid angle or
  assume the map stays injective. That would erase directional variation and repeated sheets.
- Forbidden route: import geometric-optics intensity, transparent flux, luminosity distance,
  detector response, probability, or an observationally fitted transfer rule.

The smooth-map area formula, partitions of unity, quadrature, and root counting are category-A
mathematical methods. They do not add physics to the metric.

## Candidate finite structure

For a sky tangent `v`, geodesic variation gives

```text
dF(v) = J_v(tau(n)) + d tau(v) k(tau(n)).
```

Because `k` is null and orthogonal to the source-vertex Jacobi field, test whether the longitudinal
cut term drops from the induced two-metric and whether

```text
J_2 F(n) = A_(target<-source)(n)
```

relative to source celestial solid angle. Then distinguish

```text
A_mult(U)  = integral_U J_2 F dOmega
           = integral_image N(F,U;y) dA_g(y),
A_union(U) = integral_image 1_(N>0) dA_g(y).
```

`N` is the number of supplied domain points, including declared path labels, that map to the same
regular image point. The first quantity counts every sheet; the second counts the geometric image
once. Test whether they agree exactly when `N=1` almost everywhere, not merely when there are no
isolated crossings.

## Caustic, sign, observer, and label branches

- retain every rank-two, rank-one, and rank-zero differential;
- critical points have zero local metric two-Jacobian but are not deleted from the map;
- do not assume every rank-one singularity is a fold or exclude cusps/higher map singularities;
- optional signed sheet area may cancel across folds and is not positive union area;
- under source-observer change, test pointwise cancellation between the G348 source factor squared
  and inverse-frequency-squared sky solid angle for the same intrinsic ray set;
- report every supplied path label separately. A declared disjoint-union census may count labels,
  but it is not a physical population sum or probability.

## Maximum conclusion

At most G349 may establish an exact finite **geometric** area theorem for a supplied compact regular
null-ray patch: the G348 Jacobian integrates to multiplicity-weighted sheet area; geometric union
area additionally uses the global preimage multiplicity of the supplied finite map; variable affine
cuts, caustics, observer changes, orientations, and labels are typed explicitly.

It may not establish a radiative field, finite-beam intensity, emission, absorption, brightness,
flux, luminosity, probability, detector law, observational distance, preferred ray/observer/path
population, metric history, occupancy, stability, matter/mass, scale, `X_max`, or canon.
