# Checks for longer histories and production controls

This plan is fixed before new GPU history outcomes. Exposure consists of TDS1's
short histories, the generalized code/specification review, and CPU engineering
defect proofs. Initial worker editions are retained. The unchanged conditional
Ric=0 engine and pure harmonic gauge remain the supplied comparison method.

The13 scientific cases in specs cover axial1 and oblique1 at16,24,32 cubed,
24 cubed with half the maximum timestep, stronger axial3 and oblique3 at24 cubed,
one changed oblique relative phase at24 cubed, and exact Kasner at16 cubed with
both timestep ceilings and CFL bounds. All span t=1..2.5. Mode changes are supplied families;
they are not a proof of physical inequivalence or typicality. Initial constraints
are independently checked before evolution. Failed cases remain visible.

Numerical steps use the lattice dt_min=1/3200 and dyadic step ticks. The maximum
step is.005 or.0025. At each trial RK stage and endpoint, dt times the conservative
principal-frequency bound must be <=.25 in coarse cases and<=.125 in fine cases.
Actual accepted step schedules are recorded; ceiling-only refinement would not
necessarily halve steps when the CFL bound is active. A failed numerical trial may be halved;
unexpected implementation/CUDA errors propagate with their actual reason. The
bound is a frozen-coefficient principal-symbol bound, not a nonlinear stability
certificate. Every accepted step checks finite geometry and spacelike slices.
Original ADM/harmonic checks run at most.02 coordinate time apart and before each
published checkpoint; the residual limit remains2e-5. Scheduled step endpoints
also land exactly on checkpoint/window events. Restart state contains all numerical
history needed for this memoryless controller: g,v and integer time tick.

Checkpoint cadence is.25 with additional9-sample windows at t1.015..1.035,
1.74..1.76 and2.48..2.5, sampled every.0025. Original saved-g Ricci is independently
reconstructed at every spatial point and the five centered interior times in
each window. Window endpoints and gaps remain untested by that diagnostic.
The maximum original coordinate-component Ricci threshold is2e-5. Matched-event
spatial residuals should improve at least10-fold from16 to32 unless all are below
1e-8; unresolved behavior is reported, not retuned away. Final matched g/v changes
under timestep-ceiling halving and exact Kasner g/v errors must remain below2e-7.
Record all measured errors, not only pass/fail. This is finite floating-point
evidence with Fourier methods shared, not rigorous continuum certification.

Actual-clock checks use each late uniform window: emission at20% and reception
at80% of its span, supplied fixed-coordinate clocks, origin(.31,.47,.19), and
x,y,z,diagonal initial directions. The exact Kasner control uses x and y. A separate
Hamilton/RK45 calculation checks the Christoffel/DOP853 readout. Accepted-node and
25 dense-sample null residual threshold remains2e-7; internal trial maxima are
retained separately. Independent logZ agreement and matched mesh/time differences
must be below2e-7. No sign or curve is an acceptance target. These short late
queries do not measure a ray across the unsaved gaps or select physical observers.

Engineering cases use the same worker on8 cubed: actual pause/resume and SIGTERM
restart must reproduce final fields bit for bit; wall and step-floor stops retain
valid checkpoints; output-budget failure retains an explicit reason and the last
committed state. CPU catch proofs cover invalid/nonfinite specs, inconsistent
period, non-symmetric state, event bounds and unexpected error classification.
Old immutable checkpoint corruption guarantees remain attributed to SMK1; new
controller/schedule tests do not certify every crash or power failure.

The48 cubed load case spans t1..1.5 with the actual checks/output policy and a60s
worker cap. It measures resource behavior, not new mathematical coverage. A serial
sequence of representative32/48 cases provides a30–60s sustained-load measurement
if the declared10-minute total GPU/2GiB output caps allow it. Actual thresholds,
failure history, cadence and measured throughput must control the proposed
production dispatch; a load-only grid cannot be called scientifically certified.

Two fresh actual reviewer contexts independently check their assigned quantities,
review the scientific scope and production claims, then bind the central
integration. No different-model or independent general-data time-integrator
claim is made. An unresolved defect or exhausted budget yields a bounded return,
not a multi-hour launch.
