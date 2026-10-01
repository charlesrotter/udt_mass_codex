# TPP1 runtime and clock review

Reviewer `/root/tpp_runtime`, actual separate context, same inherited model.
Parent startup and synchronization are attributed; this context independently
verified launch HEAD `90d9bc49e2fed787d9068b0a50e13a62ac58021b`, branch and tracked
cleanliness. It read only the scoped package and load-bearing prior code/evidence.
Protected payloads were not read. All reviewer execution was CPU only and stayed
below180s/2GiB per check, within the dispatched180s/4GiB allowance.

**Disposition:** the changed worker's tested runtime controls and selected late
clock calculations pass with the limits below. This is not a production launch
or a substitute for the separate original-equation/refinement review. The final
dispatch and central integration receive a separate final review.

## Concrete defects and repairs

Before GPU outcomes, the initial guard accepted a nonsymmetric supplied metric.
`prove_initial_asymmetry.py` demonstrates that on a preserved exact source; it
does not claim malformed data evolved successfully. The parent added symmetric
g/v checks at1e-12, preserving roundoff tolerance. The original retry block also
caught arbitrary RuntimeError and could mislabel an implementation/CUDA fault as
a timestep-floor stop. The repaired whitelist retries only specified numerical
trial failures; unexpected faults propagate with their actual reason.

`guards.stdout` records42 actual worker CLI catches, including the repaired
g/v symmetry cases, nonfinite/invalid numerical parameters, shape/dtype/period,
schema, event windows, scoped paths and deterministic environment. To keep all
fixtures inside review ownership, only np.load for the declared fixture path was
redirected. Torch imports and directory creation were explicitly blocked. A valid
source-level schedule control confirms the base fixture is admissible. Thus these
are actual pre-GPU guard checks, not GPU tests. The later sole worker delta added
accepted-step telemetry; inspection shows no guard or equation change.

`retry_classification.stdout` executes the actual retry-loop AST with controlled
CPU outcomes: an unexpected error propagates on its first attempt; a stage-bound
failure halves its attempted step; a failed minimum step records a floor stop.
No CUDA failure was manufactured. A later wrapper repair lowers its outer child
timeout from195s to180s. All captured children, including those under the older
wrapper, actually completed below180s. This history remains visible.

## Saved runtime evidence

`runtime_artifacts.stdout` independently recomputes checkpoint metadata/payload
hashes, signatures, integer tick/time correspondence, dtype/shape/finiteness and
output sizes without importing producer checkpoint code. Pause/resume and actual
SIGTERM/resume have bit-identical final fields **and identical complete accepted
tick/jump sequences** to the uninterrupted engineering run. All scheduled
checkpoint/window ticks are present. SIGTERM is explicitly15; wall, floor and
output-limit reasons are distinct. Output exhaustion preserves prior committed
state and returns `OUTPUT_BUDGET`. The unchanged old immutable checkpoint module's
broader corruption tests remain attributed to SMK1; this review does not repeat
them or certify arbitrary crashes, power loss or every future input.

`resources.stdout` independently aggregates22 captured worker invocations:
295.543065551s total process wall, each below180s. The48³ representative workload
completed174 accepted steps from t1 to1.5 in31.389854893s process wall, with two
recorded stage-bound trial reductions. Its largest accepted stage product was
0.249025332, below0.25. Reported peak Torch allocation was1,122,550,272bytes;
peak reserved allocation1,912,602,624bytes; queried device usage2,473,394,176bytes.
Those distinct measurements must not be interchanged. Run output was187,259,797
bytes. Package size at this review was1,900,453,515bytes, below2GiB. The48³ result
is a load measurement, not independently certified scientific coverage, and the
31-second sample is not a guarantee of six-hour performance or long-time stability.

## Independent late clock calculation

The Hamilton/RK45 checker explicitly adapts the fixed prior separate reviewer
implementation. It imports no producer ray or evolution code. It shares saved
metric data and Fourier/Hermite mathematical interpolation with the producer,
so independence concerns ray equations/integration/implementation, not data,
discretization or the general metric evolution. Query rules were fixed before
new clock outcomes: supplied fixed-coordinate clocks, fixed origin and directions,
emission/reception at20%/80% of the late saved window.

The t2.484→2.496 Kasner control's maximum exact Z error is4.45e-16. For the fine
axial24³ history, maximum accepted/dense null residual is7.20e-14. Its four Z
values are approximately0.9961621212,1.0079057726,1.0080143053,1.0077705667;
no sign was selected or rejected. Separate producer Christoffel/DOP853 agreement
is within9.33e-13 in log Z and3.24e-14 in receiver position; Kasner log Z agreement
is within2.49e-13. Internal trial null residuals remain separately reported.
All18 queried frames were independently compared bit-for-bit with authenticated
committed g/v payloads. These are short late-window rays, not rays across unsaved
gaps, selected observer populations, an empirical distance curve or UDT selection.

## Separate argument review of the diagnostic repair

At the mathematical reviewer's request, this context inspected the outcome-
informed sixth/eighth-order time-differentiation diagnostic and its exact rational
stencil checks. Coefficients and signs are correct; replacing time-time and mixed
time-space jets is consistent. Subtracting central g preserves the zero-sum
stencils. The analytic nonvacuum anchors are substantive: for supplied harmonic
Kasner powers(.2,.3,.5), R00=1−(.2²+.3²+.5²)=.62; the supplied exponential FLRW
control has center Ricci diag(−3H²,3H²,3H²,3H²). These do not vanish by construction.
No producer equation or field changes. This is separate source/argument review,
not an independent rerun of all Ricci arrays. The new center helper assumes the
regular nine-sample histories already validated by the original all-window check.

The original failed five-point spatial-refinement gate must remain disclosed.
Higher-order agreement supports only the repaired three-center comparison; it
does not fill temporal gaps or restore the original five-point criterion.

## Scope retained

Ric=0/Lambda=0 remains a supplied conditional comparison under G312 GR FILTER
ONLY. The supplied torus, conformal CMC seed, harmonic chart, marked clocks and
finite family list remain restrictions. Runtime checks neither identify R9's
physical response nor supply native UDT equations, a preferred observer, source,
scale or boundary. No native scientific premise is promoted by this review.
