# Finite-cell reciprocal-survival and density-interface audit

Date: 2026-07-23

## Result first

Geometry alone now gives a sharper global result for the new
complete-metric reciprocal `3+3` structure.

The split exists exactly where

```text
dphi is nonzero
and
s = g inverse(dphi,dphi) is nonzero.
```

It can survive through a complete cell only if those conditions hold
everywhere on the supplied regular branch and the relevant bundles descend
through its gluing. This audit applied that invariant criterion to every one
of the 12 registered completion families.

The strongest new reduction is:

> An ordinary static real scalar `phi` on a compact boundaryless spatial
> completion must have a critical point (or be constant). Therefore the
> nonnull-`dphi` reciprocal `3+3` reduction cannot survive everywhere on
> such a static spatial cell.

That conclusion directly covers the registered two-cap `S2 x S1`, `S3`,
lens, and periodic torus-bundle rows. The compact mirror-double row has the
same global critical-point issue; additionally, a smooth mirror-invariant
scalar has zero normal derivative at a fixed seam. These are obstructions to
an everywhere-defined **static reciprocal split**, not rejections of those
topologies or of time-live branches.

Retained-boundary cells can mathematically support a monotone nonnull
`dphi`, but current UDT does not force one. A time-live scalar can evade the
static compactness obstruction by carrying an everywhere timelike or
otherwise nonnull spacetime gradient, but no current native equation selects
that behavior. On nonorientable completions the two real projectors can
descend if the `dphi` line descends, while ordinary global Hodge exchange
requires an orientation twist. At a true metric or manifold singularity the
construction is undefined.

Maximum geometric conclusion:

`FINITE_CELL_SURVIVAL_CRITERION_DERIVED_AND_COMPLETION_TYPES_CLASSIFIED__GEOMETRY_STOPS_AT_UNSUPPLIED_GLOBAL_FIELD_PROFILES`

## What was and was not a complete branch

`FINITE_CELL_BRANCH_ATLAS.tsv` covers all 12 registered FC families:

- 11 are parametric completion types with no complete `(g,phi)` field
  witness;
- one, the reciprocal-toric row, is an exact conditional open-profile
  control but still lacks a complete profile and endpoint solution; and
- zero rows currently supply a complete on-shell `(g,phi)` finite-cell
  solution.

This distinction is load-bearing. The earlier global atlas correctly
crossed local motifs with completion types, but explicitly warned that a
cross-row is not a complete metric witness. The present audit did not promote
those crosses, local two-jets, configuration-space paths, cap vectors, or
monodromies into solutions.

Consequently the registered alternatives are now classified by exact
survival conditions, but not ranked or selected. Geometry stops reducing the
space at the missing full field profile, boundary/cap/gluing data, and
static-versus-time-live law.

## Exact global behavior

`GLOBAL_SURVIVAL_THEOREMS.tsv` records 12 separate results and guards.

### Boundary and compact cells

On a finite interval with retained boundaries, `phi=x` in a regular
Lorentzian product control has spacelike norm `s=+1` everywhere. Likewise
`phi=t` has timelike norm `s=-1`. These are mathematical existence controls,
not UDT field-equation solutions.

By contrast:

```text
phi=x(1-x)       gives s=(1-2x)^2
phi=sin(x)       gives s=cos(x)^2
mirror-even phi=x^2 gives s=4x^2
```

and each has an exact zero. More generally, the extreme-value theorem and
Fermat's theorem force a critical point for every smooth real scalar on a
compact boundaryless static spatial domain.

### Static versus time-live

The compactness theorem is deliberately not applied to a general
four-dimensional time-live scalar. A spacetime such as
`R_time x compact_space` can carry `phi=t` with an everywhere timelike
gradient even though each spatial slice is compact. Whether a complete UDT
branch actually does so requires its native field equations and boundary
data.

This makes time-live dependence a genuine global branch distinction. It does
not yet make time-live behavior selected or physical.

### Caps, mirrors, orientation, and singularities

- For a smooth cohomogeneity-one scalar depending only on orbit depth, a
  smooth rotational cap forces the normal derivative to vanish at the cap.
  A general multi-coordinate or time-live scalar remains open.
- An odd scalar can have nonzero derivative across a smooth double, but it
  does not descend as an ordinary scalar to the reflection quotient. A
  sign-twisted field would be an additional bundle premise.
- The rank-three projectors do not themselves require orientation.
  Ordinary Hodge exchange does. On a nonorientable completion it is a
  twisted, not ordinary, global object.
- A true singularity blocks the inverse metric or smooth bundle construction
  at the singular stratum. The regular complement remains classifiable.
- `phi=0` at the seal only makes the reciprocal weights equal. It neither
  forces nor excludes `dphi=0`.

### Causal transitions

If the continuous scalar

```text
s = g inverse(dphi,dphi)
```

changes sign, it crosses `s=0`. The semisimple split therefore degenerates
at a null or zero stratum. The exact control `phi=t*x` has
`s=t^2-x^2` and displays the null loci directly.

## Total proper density bracket

The preregistered interface gate failed, exactly as the existing source
ledger warned.

Current geometry supplies no equation of the form

```text
F[g,phi,native fields,rho_tot] = 0
```

and no simultaneous closure containing all of:

- an off-shell native mass functional;
- same-solution proper volume;
- varied global closure; and
- a response map from total proper density to the branch equations.

The five registered density routes remain:

1. observed density: external comparison/calibration only;
2. conditional carrier mass divided by volume: conditional diagnostic;
3. native simultaneous fixed point: open because its native objects are
   absent;
4. dimensionless compactness loop: rank one and not scale selecting; and
5. assembly-atlas volume contribution: no density feedback.

Accordingly, a numerical density sweep would only relabel the same geometry
rows. No units or density center could be chosen without inventing a
normalization. The audit therefore bracketed the entire formal positive
extended domain

```text
rho_tot in [0,infinity)
```

and found the branch map constant **only because `rho_tot` is not an
argument of the current branch system**.

This is not an observation that physical density has no effect. It is the
stronger methodological result that branch appearance, disappearance,
merger, singularity, or finite viable windows are not yet defined as
density responses.

Maximum density conclusion:

`NO_DENSITY_DRIVEN_BRANCH_CHANGE_IS_DEFINED_IN_THE_CURRENT_GEOMETRY_ONLY_SYSTEM__NATIVE_MASS_SOURCE_AND_RESPONSE_JOIN_REMAIN_OPEN`

## Exact and independent checks

The pinned SymPy `1.14.0` production computation reproduces:

- timelike `dphi`: tangent rank one and complementary `3+3` two-form ranks;
- spacelike `dphi`: the same ranks;
- null `dphi`: tangent rank-one nilpotent and two-form rank-two nilpotent;
- zero `dphi`: no normalized projector;
- exact boundary, periodic, mirror, and causal-transition controls.

The independently structured verifier rebuilds the exterior action from
antisymmetric matrices rather than importing the production routine. It
passes all 12 completion rows, 12 global theorems, four density-domain rows,
14 source identities, and 20 exercised corruption catches.

The preserved fresh zero-context GPT-5.4 adversarial review returned
`VERIFIED` with no requested correction. It reran both scripts in a separate
copy with a separately installed pinned SymPy `1.14.0`, reproduced all seven
generated evidence artifacts byte-for-byte, replayed all 14 source
identities and 20 catches, and independently checked the static/time-live,
completion-type/witness, quotient/orientation, and density-interface
boundaries. Its full return and transcript are preserved.

## Honest status and next gate

The audit has reached the point requested in the dispatch where geometry
alone stops reducing alternatives.

What is now known:

- the exact global survival criterion;
- which static compact completion families necessarily contain degeneration
  of the split;
- which boundary/time-live possibilities remain mathematically open;
- the special orientation and singularity behavior; and
- why no density bifurcation scan is presently meaningful.

What remains open:

- a complete on-shell finite-cell `(g,phi)` field branch;
- native equations selecting its static or time-live profile;
- full boundary/cap/gluing completion;
- native matter and off-shell mass;
- the density-to-geometry response join;
- physical reciprocal-sector ownership;
- a selected Hopf section or carrier;
- absolute scale and unconditional mass.

The next scientifically meaningful density work is not a broader numerical
range. It is deriving the missing native source/mass/response interface—or
obtaining complete field equations whose solution family already contains
`rho_tot` as a same-solution output and feedback variable.

## Four banking gates

1. **Preregistered:** yes, commit `0618da7`.
2. **Full space or bounded scope:** complete for the 12 registered completion
   families and the exact current density-interface routes; not arbitrary
   four-manifolds or complete field equations.
3. **Independently verified:** yes, separate exterior-algebra
   implementation, source replay, 20 catches, and fresh zero-context
   adversarial `VERIFIED` review.
4. **Premises audited:** yes; static/time-live, boundary/cap/glue,
   orientation, singularity, density, action, source, carrier, and scale are
   separated.

Banking grade: `VERIFIED-BOUNDED`. The bounds are the registered completion
taxonomy and absent complete field equations, not an unresolved verifier
defect.
