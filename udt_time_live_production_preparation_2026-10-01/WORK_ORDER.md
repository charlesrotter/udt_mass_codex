# Production preparation for longer three dimensional metric evolution

TPP1 implements Charles's instruction to proceed after TDS1. The question is
whether the unchanged conditional harmonic Ric=0 engine can support broader
initial data, longer coordinate histories and a bounded production output policy,
with numerical and operational evidence sufficient to specify the first six-hour
survey. This stage returns reviewed readiness or a precise unresolved limitation;
it does not launch a multi-hour job. The intended larger survey remains the goal.

## Premises and choices

Scientific authority is UDT_DEVELOPMENT.md R9, R11, R12T and R18, under current
G312 GR FILTER ONLY. Ric=0 and Lambda=0 are supplied comparison assumptions.
There is no identification of R9's response E, new source, scale, carrier,
physical observer population, X_max realization or fitted clock curve. Earlier
scientific sources, registry grades and CANON remain unchanged.

Pinned-by-THEORY within this conditional arena: the original Ricci and vacuum
constraint equations, harmonic reduction, Lorentz signature and actual metric
clock readout. Pinned-by-HABIT for this stage: marked periodic three-torus,
period2pi, pure harmonic coordinates, flat conformal initial metric, tau=-1 and
the constant TT background used in TDS1. These remain disclosed restrictions,
not a claim that UDT selects them. Free-and-explored: mode amplitudes, phases and
non-collinear integer wavevectors in a finite frozen list. All ten symmetric
metric components evolve. No spatial Killing restriction, damping, filtering,
dissipation or physical equation change is introduced.

## Construction and verification

1. Reuse the reviewed TDS1 evolution and constraint code without editing it.
   Generalize the supplied TT initial-data list using explicit transverse,
   trace-free tensors, retain the positive conformal solve, and independently
   check the original constraints and TT properties.
2. Add a production worker with bounded checkpoint cadence and short uniformly
   sampled diagnostic windows. A dyadic time lattice allows adaptive step size
   while preserving the existing immutable checkpoint time convention. Compute
   a conservative principal coordinate-frequency bound from actual lapse, shift
   and inverse spatial metric. This controls a numerical timestep; it is not a
   proof of nonlinear stability or a physical signal-speed interpretation.
3. Freeze the finite case list, code, thresholds and comparison queries before
   GPU outcomes. Compare meshes and timestep ceilings on matched data/events.
   Use exact Kasner and prior TDS1 histories as controls; neither is a desired
   geometry. Recompute original Ricci from saved metric windows independently,
   plus actual evolved ADM constraints and a supplied-clock readout.
4. Exercise pause/resume, actual interruption, wall/output/time-step floor stops,
   invalid inputs, and new scheduling rules on the changed worker. Keep failed
   histories and initial implementations. A failure triggers a finite diagnosis
   and source-preserving same-premise repair; no tolerance is loosened or seed
   removed to obtain a desired result.
5. Measure a representative larger mesh and a short sustained serial workload,
   including diagnostics and checkpoint I/O. Record wall time, Torch allocation,
   total device readings when available, bytes and steps. Specify a concrete
   first six-hour dispatch only for workloads supported by these measurements.
   Unsupported extensions remain explicitly gated.
6. Two fresh actual contexts review numerical mathematics and runtime/scope,
   including independent saved-artifact calculations and the final integration.
   Update the central argument and its coverage in proportion to actual evidence;
   run required premise and maintenance checks, commit and push the logical stage.

## Resources and stopping conditions

Measured hardware at launch: Tesla V100-PCIE-32GB,32768MiB,8MiB idle, no compute
applications; available system memory122095MiB and disk692GiB. One GPU process,
float64. Initial meshes16,24,32;48 for representative load,64 only if the measured
48 workload leaves clear resource headroom and the declared load question needs it.
Preparation permits at most10 minutes summed GPU worker wall time, at most180s
per invocation, at most8GiB peak allocated Torch GPU memory, and2GiB total new
artifacts. The short sustained load target is30–60s within that cap. No job runs
for hours, no new compute is purchased, and no software is installed.

CPU scientific/reviewer checks each180s/4GiB; existing full repository audit
900s/2GiB. Construction and two scoped reviews, including ordinary implementation
repairs and one bounded substantive same-premise repair/re-review, are included.
The proposed production dispatch will have its own measured memory/output limits,
checkpoint cadence, finite case list, coverage, stops and review return point.

Stop on nonfinite state, lost spacelike slices/signature, original constraint
failure, unmet refinement, unresolved review objection, insufficient timestep,
memory/output/wall ceiling or exhausted preparation budget. Distinguish coordinate
failure and numerical limitations from physical nonexistence. Preserve diagnostics.
No desired redshift sign or curve is an acceptance criterion.

## Maximum conclusion and workspace

The maximum conclusion is reviewed readiness for a specified conditional numerical
survey, or a bounded diagnostic explaining why that survey is not yet qualified.
This is not native UDT equation selection, a full solution-space census, continuum
certification, empirical validation or long-time physical stability. The native
selection boundary remains separate from practical numerical progress.

Workspace: this package, then the relevant central/adaptor/dependency integration.
Original TDS1/SMK1 evidence stays fixed. Protected and unrelated local work is not
read, hashed, staged or modified. Repository documentation stays in its established
format and destination; this fixed work order is not another maintained theory
summary. The previous full406 audit passed at the unchanged launch inputs; a new
full audit is required at final banking.
