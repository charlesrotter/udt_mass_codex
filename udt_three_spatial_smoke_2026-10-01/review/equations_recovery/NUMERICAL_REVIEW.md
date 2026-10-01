# TDS1 recovered equation and independent history review

Reviewer context: `/root/tds_equations_recovery`, a new actual context after the
daemon restart. Model inherited from the parent; no different-model claim. Parent
startup/synchronization is attributed at `d65a7ea0`; the reviewer independently
checked HEAD/status. The original `/root/tds_equations` files remain unchanged.
`RECOVERY_SCOPE.json` records exact source exposure and bindings. Protected files
were not opened. Work was CPU only, with each execution capped at180s/2GiB.

Disposition: the frozen original-equation and refinement gates pass for these
supplied short histories in the conditional Ric(g)=0 comparison. This does not
select a native UDT equation, certify continuum solutions, establish genericity,
or establish long-time stability or readiness for a multi-hour survey.

## Equations and independent implementation

I read the previous review's derivation and scalar-loop implementation, then the
producer `evolution.py` and `initial_data.py`. The tensor contractions in the
producer match the documented harmonic reduced equation, including both mixed
time-space terms, inverse-metric derivatives, and the two-Christoffel term. The
initial lapse/shift velocities match the four harmonic constraints. The supplied
CMC/conformal-flat construction uses the documented vacuum constraints and TT
seed. No equation/sign defect was found. This re-assessment inherits explicit
exposure to the previous derivation; it is not a second blind derivation.

The new `history_ricci.py` independently reconstructs original coordinate Ricci
from saved metric values alone. It imports neither producer code nor the previous
reviewer. Time derivatives use centered five-point formulas; spatial first,
second, and mixed derivatives use NumPy Fourier transforms. Christoffels and
their derivatives are formed directly, then contracted into the original Ricci
definition. Producer velocities and accelerations do not enter this calculation.
Harmonic residuals and normal projections of the original Einstein tensor are
computed from the same reconstructed metric jets. This is a different
implementation, sharing Fourier collocation as a method; it is not an independent
time integrator or formal proof.

Selftests recover the analytic original Ricci of a deliberately nonvacuum
exponential FLRW metric exactly in float64. Sampled analytic vacuum Kasner gives
Ricci maxima5.21e-10 and1.39e-10 at the two time steps; a nonvacuum Kasner exponent
choice gives0.62 and is detected. An attributed replay against the old scalar-loop
reviewer on12 fresh random metric jets agrees below1e-13. A fail-closed check for
nonfinite geometry was added before inspecting evolving histories; both initial
and final selftest sources/results remain saved. No tolerance was loosened.

## Saved-history evidence

All spatial points and all centered interior saved time slices were checked:
17 slices for dt=.005 and37 for dt=.0025. Two slices at each endpoint are omitted
by the centered time stencil. The period is2pi and the saved slab is t=1..1.1.
The history hashes were checked against the producer's completed source records
before reading arrays. `HISTORY_RICCI_RESULT.json` binds every input and records
per-time maxima. Maximum coordinate-component residuals are:

| History | Original Ricci | Harmonic | Normal Einstein projection |
|---|---:|---:|---:|
| N8 | 4.691e-7 | 4.652e-8 | 4.286e-7 |
| N12 | 9.275e-10 | 4.329e-10 | 2.860e-10 |
| N16 | 8.247e-10 | 4.328e-10 | 5.141e-11 |
| N16, dt/2 | 1.349e-10 | 2.729e-11 | 3.252e-12 |
| Kasner | 5.893e-10 | 3.020e-10 | 3.391e-11 |
| Kasner, dt/2 | 8.914e-11 | 1.909e-11 | 2.135e-12 |

The N8 history before and after the runtime-guard repair is bitwise identical in
g, v, and saved times. The maximum original Ricci decreases by586.78 times from
N8 to N16 when evaluated on their common marked events, exceeding the frozen10x
gate. Final N16 timestep-halving changes are2.775e-11 in g and7.209e-11 in v.
Every saved Kasner g/v value agrees with an independently constructed analytic
harmonic-time solution within4.038e-11 (coarse) and2.535e-12 (fine). These pass
the frozen2e-7 state/control threshold and2e-5 original-Ricci threshold.
The near1e-10 fine residuals include time-difference truncation and floating-point
cancellation; these data do not establish a universal convergence order.

The full seven-history check took5.16s with peak95848KiB; the explicit common-event
refinement/control check took1.70s with peak151480KiB. Commands, stdout, stderr,
versions, limits, source hashes, and machine-readable outputs are retained.

## Scope and omissions

The seed remains CMC/conformally flat and the supplied marked periodic topology,
coordinate period, harmonic gauge, Lambda=0 and small fixed case list remain
comparison choices. Full metric components and three-coordinate evolution are
supported by this implementation and this tested history; no complete search or
absence of arbitrary Killing fields is proved. This review does not independently
repeat the separate initial ADM-constraint checker, checkpoint/interruption
tests, or null/clock integration. It does not attest final central-document
integration until that exact candidate and source map are provided.
