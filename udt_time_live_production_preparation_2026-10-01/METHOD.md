# TPP1 fixed numerical method and scope

This extends central R12T inside its supplied Ric(g)=0, Lambda=0 comparison
arena. G312 remains GR FILTER ONLY. All ten symmetric metric components evolve
using the unchanged TDS1 harmonic reduction, Fourier spatial derivatives and
RK4 stages. This does not identify R9's physical response E.

For each nonzero integer wavevector k and symmetric S with nonzero projected
TT part, set P=I−kkᵀ/|k|² and T=P S P−tr(P S P)P/2, then normalize T
to Frobenius norm sqrt(2).
Thus kᵀT=0 and tr(T)=0. The supplied conformal TT tensor is
diag(2/3,−1/3,−1/3)+sum a cos(k·x+phase)T. The positive conformal solve,
tau=−1 and compatible harmonic initial velocities are inherited from TDS1.
No preferred physical frame or observer population is inferred from these
marked numerical data. The finite supplied axial/oblique, amplitude and phase
families are explored; conformal flatness, periodic topology/period and initial
CMC background are retained restrictions. No mode is selected by a target shift.

With lapse alpha, shift beta and positive spatial metric gamma, the frozen
principal frequencies obey |omega| <= |beta·k|+alpha sqrt(kᵀgamma⁻¹k).
For the cubical Fourier band this gives the conservative bound

    Omega = (pi N / L) max_x [ |beta|_1 + alpha sqrt(3/lambda_min(gamma)) ].

The implemented maximum is over sampled collocation points, not all continuum
positions. Each RK stage and endpoint checks the supplied dt*Omega ceiling. Rejected
numerical trials halve the dyadic step, with no equation change or filter.
This is a bound on the frozen principal symbol, not a theorem of nonlinear
RK4 stability. Fine comparisons halve both the step ceiling and CFL ceiling.
Integer ticks represent t=1+tick/3200. Coarse maximum is16ticks and CFL.25;
fine maximum8ticks and CFL.125. Event alignment can shorten either.

Original ADM/harmonic checks occur at intervals no greater than.02 and at
published checkpoints; the unchanged threshold is2e−5. Full state checkpoints
occur at.25 intervals and the three nine-sample windows centered at1.025,
1.75 and2.49, with stride.0025. Checkpoints are immutable, hash-bound and resumable.
The saved windows do not support gap-spanning rays or uniform error bounds.

The original independent saved-g Ricci check uses all spatial points at five
interior times/window. Its residual threshold stays2e−5. The original separate
spatial-refinement gate failed: saved-time differencing masked fine-grid
improvement. The preserved, outcome-informed REFINEMENT_REPAIR.md changes only
that diagnostic to sixth/eighth-order time differences at the three centers.
Exact stencil moments and vacuum/nonvacuum analytic controls check the repair.
The unchanged10-fold-or-all-below1e−8 comparison is applied to matching marked
events. Passing this narrower replacement does not erase the first failure.

The producer clock readout and separately implemented Hamiltonian readout use
supplied fixed-coordinate clocks and only the late window, t2.484 to2.496.
Both share the saved fields and Fourier/Hermite interpolation mathematics.
No distance law, physical observer selection or sign criterion is supplied.

The worker enforces finite spacelike slices, initial g/v symmetry, schema, deterministic
environment, resource limits and checkpoint provenance. The serial supervisor
adds a persistent queue/deadline, source bindings and between-case stops.
Known numerical trial failures alone may be retried; unexpected implementation
or CUDA errors are retained. The actual scope of testing belongs to the fixed
review reports and receipts, not to the presence of these guards.
