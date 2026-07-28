# P01 preflight numerical refinement

Status: `PREREGISTERED AFTER NUMERICAL CONTROLS; BEFORE PRODUCTION OR ATLAS OUTCOMES`

This append-only correction layer supersedes only the transport integrator and
unresolved-stop wording in the P01 preregistration.  The sampled coframe,
coefficient universe, shells, grid, loop, seed, dtype, batch size, and maximum
conclusion are unchanged.

## Why a correction was required

An eight-configuration numerical smoke test found that coordinate-basis RK4 at
64 steps per side passed the shell 0.3 transport tolerances but classified all
eight shell 1.0 transports as unresolved.  The local determinant and curvature
grid remained finite.  The failure was therefore traced to the severe
conditioning of coordinate components under large coframe scalings, rather
than to failure of the metric evaluation.

This was a numerical-method control.  It was not a production sample and it is
not admissible as a scientific atlas result.

## Frozen refinement

Parallel transport is evaluated in the complete orthonormal coframe.  From the
Levi-Civita coordinate connection and coframe `E`, the pathwise frame
connection is computed as

`omega = E Gamma(dot{x}) E^{-1} - dot{E} E^{-1}`.

The symmetric part of `eta omega` is recorded as a projection-error diagnostic.
Its antisymmetric part is the Lorentz-algebra generator used for transport.
Each of 64 equal steps per side is advanced by a midpoint matrix exponential.
The reverse loop is computed independently.  The registered 32/64/128
refinement check now tests second-order midpoint convergence; the expected
asymptotic error ratio is four, but no ratio is forced.

Checkpoint names use `MEXP64`, not `RK64`.  The CLI option `--rk4` is retained
only to avoid an unrecorded interface change; after this correction it means
the number of midpoint-exponential steps per side.

## Corrected unresolved policy

Local-grid and transport resolution are separate fields:

- `grid_unresolved`: at least one registered local invariant is nonfinite;
- `transport_unresolved`: the frame holonomy is nonfinite, violates the
  registered Lorentz/reverse tolerances, or has frame-connection projection
  error above `1e-10`.

The greater-than-25-percent stop rule applies to `grid_unresolved`.  A strongly
warped shell may produce transport matrices whose rapidities exceed reliable
float64 reconstruction while its local metric invariants remain resolved.
Those transport rows are retained and explicitly classified unresolved; they
do not erase the independently resolved local atlas.  No missing transport is
imputed, clipped, or treated as a physical singularity.

## Pre-production controls required

Before production:

1. neutral and constant-coframe cases must have curvature and holonomy below
   `1e-10`;
2. a bounded smoke test must show zero local-grid unresolved rows;
3. the shell 0.3 anchor values must be independently recomputed on CPU without
   importing the production evaluator;
4. production must still use CUDA device 0, float64, 1,024 configurations per
   shell, the five frozen shells, the 17 by 33 grid, 64 steps per loop side,
   and batch 64.

Maximum conclusion remains exactly a bounded off-shell configuration and
pathwise-geometry atlas.  This correction supplies no dynamics, action,
source, carrier, boundary selection, density law, or physical branch selector.
