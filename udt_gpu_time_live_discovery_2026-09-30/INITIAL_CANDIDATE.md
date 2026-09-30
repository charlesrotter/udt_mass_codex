# NGD1 — fixed numerical candidate, 2026-09-30

Status: CONDITIONAL_NUMERICAL_EVIDENCE_UNPROMOTED plus an exact conditional
clock-shift identity. This preserves the first scientific interpretation before
direct review. The maintained argument belongs in UDT_DEVELOPMENT.md R12.

## What was actually executed

PLAN's first bounded campaign is complete through numerical challenges: 12 GPU
runs,158 history executions including repeats. The initial survey has16 supplied
histories; the longer challenge has30 (the16,12 projected spatial-profile cases,
and two0.1% second-velocity-mode perturbations). Two changed periods use7 specified
cases each. Pilot N32/64; survey N64/128/256, separately halved timestep; longer
challenge t=1 to32 at N128/256, k=.75 plus comparison k=.5,1. Float64, one V100
process, RK4 time evolution/Fourier collocation, no relaxation or target fitting.
See SURVEY_FREEZE.json for every pre-outcome datum and gate; the earlier pilot
was exposed. PRE_SURVEY_SUPPLEMENT adds the independent reviewer's scaled Ricci
gate before survey execution. No scientific solver repair or discarded datum.

The original Ricci-flat equation is a supplied comparison, not native UDT
dynamics. G312's GR FILTER ONLY remains controlling. This explores a nonlinear
two-Killing, orthogonally transitive, periodic vacuum sector, not all metric
histories, full3D, matter, twist or native response selection. Releasing Q removes
one actual restriction of the earlier polarized example, not all restrictions.

## Argument joining geometry to the measured clock shift

Use the metric and four equations in EQUATIONS.md, independently reconstructed
from all16 original Ricci components in review/fidelity/check_original_ricci.py.
For supplied fixed-coordinate timelike clocks, N=exp(lambda/4)t^(-1/4). These
clocks need not be geodesic. Longitudinal affine null branches have dx/dt=+1 or-1;
choose a lifted branch of duration d>0 so to=te+d. Then

    log Z = [lambda(to,xo)-lambda(te,xe)]/4 - log(to/te)/4.

This is the ordinary metric proper-clock/null readout with supplied observers
and branch. It does not independently attribute the shift to UDT's positional
postulate. On the periodic x domain, d specifies the lifted branch and can carry
winding; it is not shortest distance, proper distance or cosmic distance.

The following identity was recognized during inspection of the survey, then
independently checked. It is an outcome-informed exact interpretation, not a
preregistered prediction or a replacement of the frozen numerical tests.
Adding/subtracting the two lambda equations gives exactly

    lambdat ± lambdax
      = t[(Pt ± Px)^2 + exp(2P)(Qt ± Qx)^2] >= 0.

Thus along either future longitudinal branch, Delta lambda>=0. Equality can
hold on a segment without establishing that the whole spacetime is homogeneous. Relative to the
constant-lambda,P=Q=0,zero-velocity Taub control on the same marked te,to query,
Delta log Z=Delta lambda/4>=0. Total Z can remain below1 because the control term
is negative. This does not compare with every homogeneous Ricci-flat metric;
the independent nonlinear homogeneous test has evolving lambda. Nor does it
order unpolarized versus otherwise matched polarized data. It is a conditional
identity of this comparison sector, not a newly discovered GR law or native UDT
prediction. Frame/coordinate polarization diagnostics are not invariant matter
energy or an added physical carrier.

## Numerical findings and reproducibility

All planned runs completed and all declared numerical gates passed. Parent
CAMPAIGN_DIAGNOSTICS.json and independent review/numerics results retain exact
values, commands, versions, full fields and sampled checks. Largest independent
CPU/GPU absolute saved-field difference3.676e-8; largest temporal-refinement
field difference3.447e-8 and matched-clock logZ difference5.364e-9. Spatial
refinement differences were near floating-point error in these smooth examples.
Original-metric Ricci, independently differentiated from saved metric histories
at declared centers and contracted in a local orthonormal frame, max4.621e-9;
the supplementary t²N²-scaled value max9.647e-7 (gates2e-5). These checks do not
use the production RHS to manufacture time derivatives. Independent momentum
check across all saved snapshots max4.395e-9. Initial states are independently
reconstructed from specifications/projection; maximum mismatch7.14e-14.

Actual sampled logZ includes both signs. At k=.75 the longer challenge spans
[-.5493062,1.389315] over its declared te,d,emitter-grid queries. Amplitude,
phase, admissible initial profile and period change the detailed response.
The mean lambda increase at t32 ranges from about.53 in the weak phase0 datum
to19.06 in its stronger counterpart. The figure shows three prelisted phase0
amplitudes and sampled-emitter bands, alongside the constant-lambda control.
All other cases remain in CLOCK_READOUTS.json, not selected out of the evidence.

Execution used32.345seconds summed evolution time (includes transfers/output),
peak PyTorch allocated GPU memory4,119,552bytes,118,247,476bytes of saved compressed
fields. This is a small validation campaign on a GPU, not a heavy use of the
device or a GPU-vs-CPU speed benchmark. Full capture durations include startup;
the largest process RSS remained below1GiB. There was no reason to exhaust the
45minute budget after the declared scope passed. Matplotlib's unwritable-cache
warning is retained; it used /tmp and both figure formats were produced.

## Coverage and limits

- Independent CPU integration is NumPy/SciPy DOP853; GPU is Torch/RK4. Both use
  Fourier spatial discretization. This is not independent discretization or a
  rigorous continuum error enclosure. Refinement and tails support this finite
  numerical scope; exact equation reconstruction is a separate mathematical check.
- Original metric residuals cover declared temporal stencil centers, every case
  and spatial node, not every continuum time. Two stencil widths reaching a
  roundoff floor are not a demonstrated convergence order. Constraint checks
  cover all saved snapshots. Sampled extrema need not equal continuum extrema.
- The12 spatial-profile cases enforce the periodic momentum integral by
  projecting V. That projection can be large (up to about0.81 relative L2 of the
  raw seed in the independent fidelity check); these are new admissible families,
  not small perturbations. Only the two specifically named perturbation cases
  have the stated0.1% second-mode change. Neither establishes general stability.
- Changing k changes supplied geometry/data/marking. It is not evidence of
  invariance under a coordinate change or infinite-volume convergence. General
  null directions are omitted; the pilot validates only longitudinal readouts.
- No universal distance-redshift shape, selected scale, unreachable X_max limit,
  physical light/matter identification, all-data behavior or asymptotic claim.
  No observational fit; no comparison here can refute the whole UDT proposal.

## Return and next decision

The gain is an independently checked evolving-metric engine, broader finite
conditional histories and an exact sign identity separating an added geometric
contribution from total redshift. The native selection gap is unchanged. Raising
GPU consumption or releasing3D symmetry inside Ric=0 alone would still explore
that supplied comparison law. Before a larger production campaign, the next work
order should state which evaluable native condition or explicitly unadopted
physical connection will distinguish histories, and whether the task is evolution
under a law or constrained metric-history search. The present data provide its
control benchmark; they do not supply a new law by appearance. Stop for discussion
after central integration, actual review, checks and banking.
