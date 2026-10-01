# TDS1 data, runtime, readout and scope review

**PASS within the declared short conditional scope.** This continues
`INITIAL_REVIEW.md` in the actual separate context `/root/tds_data_recovery`.
Same inherited model, source-exposed review, no different-model or blinded
independence claim. Parent startup/synchronization evidence remains attributed;
this reviewer performed the checks below directly on current saved artifacts.
All reviewer computations were CPU only, captured under 180s/2GiB per command;
no installations, GPU worker, protected payload access or source mutation outside
`review/data_recovery/` occurred.

## Original constraints after evolution

`check_late_constraints.py` imports the interrupted reviewer's independent
metric/connection constraint evaluator, not producer code. It reconstructs K
independently using (-partial_t gamma+Lie_beta gamma)/(2 alpha), with
alpha=(-g^00)^-1/2 and beta^i=gamma^ij g_0j. Thus it does not mistakenly keep
the initial lapse1/shift0 assumption on evolved slices. Lapse ranges approximately
1.104884–1.105457 and max shift is .001294 at the final general-data slice.
Original Hamiltonian, momentum and harmonic quantities were recomputed at both
t=1.05 and t=1.1 for N8,N12,N16,N16-half-step and both Kasner histories.

| Final general-data mesh | max Hamiltonian | max momentum | max harmonic vector |
|---|---:|---:|---:|
| N8 | 1.18267045e-6 | 3.48643513e-7 | 3.75101058e-8 |
| N12 | 3.05092951e-10 | 2.08285802e-10 | 1.37949886e-11 |
| N16 | 9.63007452e-13 | 8.56615126e-13 | 5.17598574e-12 |
| N16, half timestep | 1.93622895e-13 | 1.42004464e-13 | 3.34158657e-13 |

The independent implementation shares Fourier differentiation and saved data
with the producer; no independent spatial discretization or continuum bound is
claimed. The original four-dimensional Ricci check belongs to the separate
equation-review context; these constraint results do not replace it.

## Guard defects, repairs, and actual runtime evidence

After the first N8 run and before the remaining batch, the reviewer identified
two pre-repair input-guard gaps: a NaN constraint limit
could disable a numerical comparison, and a spec period could differ from the
saved initial-data period. Positive integer resource validation was also requested.
The parent preserved the old source and froze the guard repair without changing
the equation, amplitudes, numerical threshold, or positive histories.

All 12 CPU catch proofs in `guard_repairs.stdout` reject NaN/nonpositive/too-loose
constraint limits, mismatched/nonfinite periods, and zero/negative/floating GPU
or output budgets. Every child returned2 with the expected reason before creating
a run directory. An explicit import blocker ensured no Torch/CUDA entry was
possible. These catches validate the repaired gates, not all conceivable inputs.

`runtime_artifacts.stdout` independently reads final saved arrays: ordinary
pause/resume and actual SIGTERM/resume yield bit-identical final g and v against
the uninterrupted repaired N8 run. The wall-stop receipt returns75, timeout=false,
with committed evidence; the deliberately bad-constraint fixture returns2 with
diagnostic-only evidence and zero committed checkpoints. Metadata and payload
hashes were checked. Current worker source rechecks constraints before committing
initial, resumed and evolved states. The new driver serializes its GPU workers.
These are scoped interruption/stop tests, not exhaustive crash or power-loss proof.

## Distinct clock/geodesic check

The parent computes frequency from supplied fixed-coordinate timelike clocks,
with Z=omega_emitted/omega_received. The initial null direction and frequency
normalization are consistent with that observer choice. Harmonic coordinate time
s=t-1 gives the exact axis-aligned Kasner comparison Z=exp(p*(s_o-s_e)), with
p=-1/3 or2/3. No cosmological observer or UDT physical clock population is selected.

`check_clock_hamilton.py` independently integrates null-ray covector momenta:
dx^i/dt=k^i/k^0 and dp_mu/dt=(partial_mu g_ab)k^a k^b/(2k^0), k=g^-1 p.
It bypasses the parent's Christoffels and contravariant geodesic ODE, uses RK45
instead of DOP853, and implements metric interpolation with SciPy's Hermite spline.
The saved fields and Fourier/Hermite mathematical methods remain shared.

Two Kasner and four N16-half-step queries pass. Their largest difference from the
parent logZ is1.414e-11 for Kasner and1.311e-11 for general data. Independent Kasner
Z errors are2.94e-13 and4.78e-13. Largest sampled null norm on the accepted
Hamiltonian trajectory is1.66e-12. General-data logZ values are approximately
-0.0206340,0.0369740,0.0442110,0.0188644 for the four declared directions. Both
red and blue signs survive; no desired sign or shape was used to admit cases.

The parent and this reviewer both initially tested null norm on internal
Runge–Kutta trial stages. Those intermediate algebraic approximations are not the
accepted geodesic trajectory and need not lie on the null manifold: the independent
maximum trial norm was about7.75e-5 despite accepted norms near1e-12. Initial
code and failed captures are preserved. The repair applies the unchanged2e-7
null tolerance to accepted integration nodes plus25 fixed dense-output samples,
while retaining trial maxima diagnostically. Neither ray equation, integrator,
integration tolerance, geometry, observer choice nor frequency target changed.
The accepted/dense sampling is a finite diagnostic, not a continuous null bound.

## Scope and remaining integration

The evidence supports this numerical tool on a short t=1..1.1 slab, one supplied
three-direction amplitude1 initial family and its listed controls/refinements.
The rank-three argument excludes constant-coordinate translation symmetry of
the supplied data; it does not prove absence of every Killing field. The code
imposes no spatial Killing symmetry, but periodic topology, harmonic gauge,
Lambda=0, CMC/conformally-flat seed, and finite numerical resolution remain
explicit restrictions.

No native UDT response-law selection, full solution-space map, physical scale,
source, long-time stability, continuum certification or multi-hour production
readiness follows. Current G312 GR FILTER ONLY still qualifies the conditional
Ric=0 comparison branch. Central/operational integration and its exact source
bindings remain a separate pending proportional review; this scientific review
does not automatically approve later wording or upgraded claims.
