# Intrinsic clock/transverse solder audit

Date: 2026-07-24

Preregistration: `4ceac0f880edf3e3ffe1c8caa8805a00a826595b`

Conservative generator-scope clarification: `a12cab2`

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The complete metric supplies a real longitudinal–screen relation, but not
the full clock/transverse solder being sought.

Given an oriented observer/path `2+2` split, Hodge duality maps the
longitudinal area bivector to the screen area bivector and is preserved by
Levi-Civita transport. This is exact geometry. It cannot carry the
reciprocal dilation parameter because both the reciprocal boost and screen
rotation preserve plane area. It also maps spacetime two-forms, not Jacobi
phase-space states.

Without a selected screen direction, independent `SO(2)` screen gauge
forces every linear clock-to-screen or clock-to-Jacobi map to zero.

After a screen line is supplied, its separation-plus-direction phase
subbundle is preserved exactly when the line is parallel and the tidal
operator preserves it. A nontrivial pointwise match between that scalar
Jacobi generator and the reciprocal clock generator exists precisely when

`K_screen=-(d delta/d lambda)^2`.

This gives a sharp candidate condition and an exact negative-curvature
mathematical witness. No registered complete UDT branch realizes it.

## Branch result

- B19: complete transverse transport and area duality, but `Q=1` while the
  positive-curvature transverse propagator is nontrivial.
- WR-L: exact local centered scalar relation
  `R=X(1-Q^-2)`, but positive radial screen curvature prevents pointwise
  natural-frame generator similarity with its nonzero hyperbolic clock
  rate. This does not exclude an arbitrarily chosen path-dependent basis;
  it shows that the metric has not supplied an intrinsic one.
- squashed `S3`: no selected parallel screen line or matched representation;
  clock is trivial and the branch is off shell.
- temporal-`phi`: the clock solder and complete branch remain open.
- constant-curvature static control: local area structure, but positive
  screen curvature and incomplete clock patch.
- universal physical UDT: no complete nontrivial all-observer solder
  witness.

No cross-branch splice was used.

## Relation to earlier positive structures

The nonnull-`dphi` reciprocal `3+3` remains exact, real, and Hodge
exchanged. It does not select a rank-two Jacobi phase subbundle. Its
Levi-Civita transport mixes sectors whenever the off-stabilizer connection
block is nonzero, and it degenerates at null/zero `dphi`.

The earlier reciprocal-angular intertwiner theorem also remains exact and
conditional: if a matched angular representation and mirror are supplied,
the linear map is rigid up to relative scale. No complete metric branch
selects those premises.

## Honest status

`DERIVED`: typed normal/screen area Hodge duality; the parallel
tidal-invariant screen-line criterion; the pointwise negative-curvature
generator condition; and the local WR-L scalar clock/area relation.

`OBSTRUCTED_WITHOUT_SCREEN_REDUCTION`: a screen-gauge-equivariant linear
clock-to-Jacobi map.

`OPEN_NO_REGISTERED_WITNESS`: an intrinsic irreducible clock/transverse
solder across a complete physical branch.

`DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY`: the reducible direct-sum
same-path cocycle from the parent audit.

## Evidence

- production exact checks: 80/80 pass;
- independent standard-library `Fraction` checks: 60/60 pass;
- independent exercised catches: 15/15 reject the mutation;
- candidates: 12/12;
- generator controls: 5/5;
- registered branches: 6/6;
- causal classes: 5/5;
- finite-cell completions: 12/12;
- equation families: 28/28;
- frozen source identities: 21/21.

Repository-wide gates are in `REPOSITORY_GATES.json`.

## Scientific consequence

The missing join is not merely an unnoticed Hodge identity. The metric has
now exposed an exact candidate signature for a genuine pointwise linear
join—negative screen curvature matched to clock rate, plus a parallel
tidal-invariant screen line—but has not selected a complete branch carrying
it.

The next justified step is a source/equation-availability audit: determine
whether any already registered complete-metric equation or admissibility
condition can enforce those two requirements without inventing a profile,
screen direction, action, or cross-branch assembly. If none can, local
linear soldering has reached its current metric-only selector boundary.
