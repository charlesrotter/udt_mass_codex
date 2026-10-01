# TDS1 — reviewed short three-coordinate numerical return

Status: CONDITIONAL_NUMERICAL_EVIDENCE_UNPROMOTED, with the finite limits below.
TDS1 evolves all ten symmetric spacetime metric components with variation in
three spatial coordinates, releasing NGD1's imposed two-Killing spatial sector.
The equation remains the supplied Ric=0 comparison, not native UDT dynamics.
The current G312 authority and R9's unidentified response remain controlling.

The explicit harmonic reduction, conformal CMC initial construction, original
constraints and clock convention are in EQUATIONS.md. Their independent
metric-jet checks preceded history outcomes. N8,N12,N16 histories span harmonic
coordinate t=1..1.1; N16 has a timestep-halved check. One supplied three-direction
seed and exact flat/Kasner/oblique-gauge-wave controls were tested. This is a
solver extension and short validation, not a parameter survey or long-time map.

Independent original Hamiltonian residuals of the initial data fall from
1.203e-6 at N8 to2.185e-13 at N16. The three-direction derivative Gram has rank3,
excluding a shared constant-coordinate translation for these data; arbitrary
nonlinear Killing fields were not classified. Initial conformal flatness and
constant mean curvature remain restrictions on the seed, not the subsequent metric.
Lapse and shift evolve; independent later constraints use their actual values.

From saved g alone, an independent NumPy implementation reconstructs original
four-dimensional Ricci at every grid point and every centered interior saved
time. Max coordinate-component residuals are4.691e-7 (N8),9.275e-10 (N12),
8.247e-10 (N16), and1.349e-10 (N16,dt/2), against2e-5. Common-event N8–N16
improvement is586.78x. Final N16 timestep halving changes g by2.775e-11 and
its velocity by7.209e-11, against2e-7. Exact Kasner g/v comparisons also pass.
Original evolved ADM constraints were independently recomputed from g,v with
the actual lapse/shift and converge similarly. These are finite floating-point
checks, not rigorous continuum error bounds or an independent general-data
time integrator. Fourier spatial mathematics is shared; two slices at each
time endpoint are omitted by the centered Ricci stencil.

Supplied fixed-coordinate clocks were queried along computed null geodesics
with emission t=1.02, reception t=1.08, and declared directions. A separate
Hamiltonian covector/RK45 implementation agrees with the producer's Christoffel/
DOP853 logZ within1.414e-11 across the independently repeated queries. Spatial
Fourier and time Hermite interpolation mathematics and saved fields are shared.
The four N16-half queries give Z approximately0.9795774,1.0376661,1.0452029,
1.0190435. Both signs relative to1 survive; no redshift sign/curve was targeted.
Receiver positions are computed ray arrivals, not selected cosmological clocks.
Exact homogeneous Kasner ratios and mesh/time readout comparisons pass. No
generalization of NGD1's two-Killing longitudinal sign identity is asserted.

Actual pause/resume and SIGTERM/resume give bit-identical final metric/velocity
arrays to the uninterrupted new-solver run. A tiny wall budget yields a committed
stop, and deliberately invalid constraint data yields diagnostics with no committed
checkpoint. NaN/invalid tolerance, inconsistent initial period and invalid budget
specifications are caught before CUDA entry. The old source and all failed
diagnostics are retained. This is finite operational evidence, not all-crash or
power-loss certification. Full short-run/code/resource evidence is in WORK_RECORD.

Two original reviewers were interrupted by a daemon restart; their completed
artifacts remain. Two new actual contexts completed independent equation/data,
history, runtime, readout and scope review, with that exposure explicitly attributed.
All share the inherited model. Reports are review/equations_recovery/NUMERICAL_REVIEW.md
and review/data_recovery/SUBSTANTIVE_REVIEW.md; actual final attestations control
integrated-byte acceptance. No different-model, formal, empirical or full-corpus
reproof is claimed. The repaired null diagnostic tests accepted integration nodes
and fixed dense samples, retaining internal Runge–Kutta trial-stage norms separately.

Remaining restrictions: periodic topology/marking/period, harmonic gauge,
Lambda=0, CMC/conformally-flat initial seed, this small supplied family and short
time slab. No matter/source, native response identification, physical scale,
X_max completion, genericity, full solution-space coverage or long-run stability
is established. Multi-hour production remains gated: validate longer slabs,
broader data, production output cadence and representative mesh/resource loads.
