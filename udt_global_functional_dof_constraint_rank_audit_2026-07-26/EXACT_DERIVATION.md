# Exact derivation and scope

## 1. What is being counted

This is a count of arbitrary local configuration functions before field equations, not a count of
physical particles or propagating polarizations. Write `F4[n]` for `n` scalar functions of four
coordinates. Coordinate and local-frame descriptions are gauge presentations; boundary functions,
one-dimensional profiles, continuous moduli, and discrete topology are kept in different columns.

## 2. Metric and coframe counts agree

A symmetric four-by-four metric has

```text
4(4+1)/2 = 10
```

independent component functions. Four coordinate functions change its presentation. At a generic
regular metric with no local stabilizer, the local configuration quotient therefore has signature

```text
F4[10] - G4[4] = F4[6].
```

The coframe presentation independently gives the same answer. An invertible four-by-four coframe has
16 functions. Its local Lorentz presentation group has

```text
4(4-1)/2 = 6
```

functional generators. Removing those six and the four coordinate presentation functions gives

```text
F4[16] - G4[6] - G4[4] = F4[6].
```

The independent verifier reconstructs the Lorentz-algebra dimension by solving
`eta X + X^T eta = 0` over exact rational arithmetic rather than importing the production count.

This does **not** say that UDT has six propagating gravitational modes. Such a statement requires a
complete response operator or action, its differential constraints and Noether identities, a gauge
choice, and an initial-value problem. None is presently available.

## 3. The ten “orchestra amplitudes” are one metric

Within the supplied regular `2+2` chart, the metric is written using:

```text
base symmetric block:    3 functions
screen symmetric block:  3 functions
shift block:             4 functions
                         -----------
                         10 functions.
```

Thus the base, angular-screen, and shift instruments are a complete nonlinear parameterization of
one regular metric, not three additional fields. The split remains supplied rather than intrinsically
selected, but no metric component is missing inside that chart.

The prior independent-amplitude atlas found tangent rank ten for the complete metric two-jet and rank
eleven only when an independently varied signed `phi` was appended. The present exact component
count explains that numerical result without promoting the bounded two-jet atlas to a global theorem.

## 4. The `phi` fork changes the count by one

Two sharply different cases remain:

1. If `phi` is an independent scalar, the local configuration signature is

   ```text
   F4[6] metric + F4[1] phi = F4[7].
   ```

2. If `phi` is a covariantly derived readout of the metric, it adds no independent field and the
   signature remains `F4[6]`—but only after the missing metric-to-`phi` map is actually derived.

Writing `phi` in the metric does not by itself decide which case applies. Treating it as both an
independent scalar and a metric-derived amplitude would double-count it; treating it as derived
without giving the map would silently impose the desired conclusion.

## 5. CSN is a sensitivity branch, not a primary subtraction

If strong **local** Common-Scale Neutrality were an actual gauge equivalence, it would remove one
additional local metric function:

```text
F4[10] - G4[4] - G4[1] = F4[5].
```

An independent scalar would then restore the total to `F4[6]`. But strong local CSN is currently
`CHALLENGED_OPEN`, particularly after restoring the observational `c`/`G` anchors. These are therefore
conditional sensitivity counts only. A constant common rescaling can remove at most one global
constant; it cannot be substituted for a local conformal gauge function.

## 6. Branch-specific extra data

The seven registered off-shell branches do not share one field census:

- `C01`: metric/conformal class with metric-derived `phi`; the derivation map is missing;
- `C02`: metric plus independent `phi`; exact anchored signature `F4[7]`;
- `C03`: coframe plus a reciprocal reduction; whether the reduction is derived or independently
  varied is not specified, so its addition remains uncounted;
- `C04`: metric plus a supplied nondegenerate rank-two plane. The Grassmannian dimension
  `2(4-2)=4` adds `F4[4]`, giving an anchored metric-plus-projector floor of `F4[10]` on that
  conditional branch. Whether `phi` within the plane is derived or independent is not supplied, so
  the complete branch signature remains `F4[10]+U[PHI_WITHIN_PLANE_STATUS]`;
- `C05`: multipliers and reciprocal constraints are not enumerated, so neither their fields nor
  independent constraint rank can be counted;
- `C06`: the pre-scale class, representative section, and two-stage bridge require an unsupplied
  map and cannot be collapsed into one count; and
- `C07`: the independent connection/torsion type is not fixed, so a general-affine, metric-compatible,
  torsional, or other field count may not be invented.

No branch is selected.

## 7. What the founded premises actually remove

The abstract reciprocal pair obeys `u v=1`, so two positive comparison channels reduce to one
relative character. Additive composition selects its exponential form. This is exact, but it has
zero spacetime-metric rank until UDT derives the physical slot/soldering map.

Regular Lorentz signature and positivity are open inequalities and remove no functional dimension.
Finite-cell ontology changes the global domain, not the point-local metric count. The observed `c`
and `G` calibrate clock-distance and mass-length conversion but are not local field equations.
Current bootstrap wording is an on-shell admissibility principle and supplies no present local rank.

On the static seal branch, `phi|_Sigma=0` removes one boundary trace `F3[1]`, and the allowed
variation has `delta phi|_Sigma=0`. The normal derivative and bulk `F4[1]` scalar remain free. This is
boundary information, not a bulk equation.

Therefore the registered foundations currently provide **zero complete bulk metric/`phi` equation
rank**. This does not mean they have no content; they fix relational algebra, calibration, domain,
and some boundary data. They do not yet supply a native response on the full field space.

## 8. The many geometric readouts do not enlarge the field census

Once the metric and any genuinely independent branch fields are specified, the following are
downstream rather than additive fields:

- the base/screen/shift decomposition;
- the Levi-Civita connection and curvature;
- spectral projector motifs and their Kato transport;
- the normalized angular metric;
- the torus shift connection when the toric split is supplied;
- its curvature, holonomy, and characteristic classes;
- the observer-pair clock cocycle when its typed path is supplied; and
- the conditional Hopf/Chern readouts when their global toric inputs are supplied.

A separately supplied projector is different and was counted in `C04`. An independent affine
connection is different and remains uncounted in `C07`.

## 9. Maxwell-like content, exactly scoped

On a supplied toric branch the metric supplies a torus connection `S`. Its curvature is defined by

```text
F = dS,
```

and consequently

```text
dF = d^2 S = 0.
```

Neither line adds an independent field or a dynamical constraint. The second is the homogeneous
exterior-calculus identity, not a native derivation of the inhomogeneous Maxwell equation. A selected
integral circle character `w` would give `A=w^T S` without adding a continuous field, but UDT has not
selected that `U(1)`, a Maxwell action, current, charge normalization, or source equation. Historical
pre-July claims have no affirmative authority under the provenance firewall.

## 10. Completion freedom is a different axis

For `FC01` through `FC11`, choosing a boundary, cap, seam, monodromy, stratification, or
nonintegrable distribution does not by itself reduce the generic local `F4[6]` metric signature (or
`F4[7]` with independent `phi`). Each class instead adds branch-dependent boundary functions,
profiles, continuous moduli, discrete lattice data, or topology. Their complete dimensions remain
uncounted because the embeddings, function spaces, and compatibility operators are not supplied.

`FC12` is different: inside its separately supplied reciprocal-toric diagonal ansatz, the bulk
metric is controlled by two positive one-dimensional profiles, `A(phi)` and `Omega(phi)`, plus
endpoint data. That is an exact `F1[2]` control count, but it is not the generic metric and is not a
selected universe.

## 11. What closure would have to cover

The missing native object is not merely one scalar equation and not merely a list of boundary
conditions. It is a complete off-shell response interface whose components pair with every allowed
variation in whichever branch UDT selects:

- all symmetric metric variations, with coordinate/gauge identities handled;
- `phi` variations if `phi` is independent;
- projector, reduction, multiplier, bridge, or connection variations if such data are independent;
- finite-cell boundary and corner variations; and
- global moduli/period consistency.

This does not require the response to eliminate every function or produce a discrete solution. A
differential law normally leaves initial and boundary data. It does require the law to be defined on
the whole chosen variation domain. Only then can its differential constraint rank, propagation,
solution space, and physical modes be calculated.

The audit therefore identifies the current closure type as

```text
COMPLETE_RESPONSE_INTERFACE_PLUS_GLOBAL_BOUNDARY_DATA,
```

not a one-equation join.
