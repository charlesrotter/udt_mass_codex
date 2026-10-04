# CGE1 direct fidelity and independent-quantity review

Verdict: **VERIFIED-WITH-CAVEATS**, within the conditional work-order scope.
No mathematical or source-fidelity repair to INITIAL_CANDIDATE.md is required
by this review. The repaired checker implements the correct arrival chain rule;
its initial failure remains preserved. Central integration has not yet been
reviewed, and this verdict does not adopt the class, alter a scientific grade,
establish native selection or confer canon.

Reviewer `/root/cge_fidelity`, actual fresh separate Codex context, 2026-10-04.
Exact model identifier unavailable; same/different-model axis is unclaimed.
Human review unavailable. SOURCE_FIRST.md/SOURCE_HASHES.json bind the actual
bounded source-first argument and exposure. DIRECT_PLAN.md and SAVED_PLAN.md
record later exposure; no other CGE1 reviewer's proof/code/output was read.
Parent startup/premise checks are attributed there, not misrepresented as this
reviewer's full historical reproof. This reviewer wrote only review_fidelity/.

## Version and hypothesis findings

Reviewed candidate SHA256:
`ce2b962bbf47e09dfd120036e1b06f2e6b06f0c18ac1e26766a490830e4fa8c9`.
Repaired parent implementation SHA256:
`954f7417eafcdb706a84dd2b33878dae56ee24a41cd9ddf937906828a282903f`.
Saved construction output SHA256:
`046f2b5bcda03828bc204c4e6bd3550845cf14914f2368e1ffa20da7dd03c174`.
Freezes bind the remaining files and scopes.

1. Conditional class ownership is faithful. G312 GR FILTER ONLY remains current;
   provisional DDR/locality are retained without treating them as enough to
   select the full G301 class. Ric=Lambda g is an admitted mathematical query
   here, not a native law reconstructed from the founding scalar kernel.
2. The full spherical Ricci calculation yields the candidate f and regular
   circular timelike clocks with h>0, Omega²>0 and f(a)>0. A source mass or
   interior is not thereby derived. The circular orbit is distinct from an
   irregular clock invented at the central singularity. Test-particle radial
   stability is correctly separated from disk/metric/global stability.
3. The actual outward-ray incidence retains both arrival radius and impact
   parameter variation. Independent differentiation gives determinant
   -I(E-vs)/(fv), nonzero on the declared regular branch, and the same positive
   proper arrival ratio as endpoint contraction. There is no global branch
   uniqueness assertion. The radial finite example cannot be differentiated
   by incorrectly fixing b=0 while the emitter continues orbiting.
4. The receiver tetrad and frequency normalization are consistent. Sky is minus
   future propagation; no extra systemic shift is appended. The calculated
   equatorial direction is not promoted to a full disk Jacobi map, scalar
   angular distance or a replay of the MCP estimator.
5. The single-radial-shift construction changes receiver preparation and retains
   its outward condition w²>f(R). It is not a degeneracy theorem for all time,
   angular or observed records. Free initial data are not proof that all UDT
   premises are insufficient or that a new postulate is necessary.
6. Source/clock/curvature selection, additional positional attribution, source
   readout, physical scale and X_max remain open. Conventional Kottler-method
   provenance is honestly identified. The first paper's publication metadata and
   charge-zero metric were checked directly; neither paper supplies UDT premises.

## Actual independent checks

Source-first source_checks.py passed 52 exact checks over twelve finite cases:
all four-dimensional Ricci components, circular geodesic/normalization,
receiver tetrad, nullness, signed sky formulas, radial incidence derivatives,
and explicit single-shift receiver degeneracy. direct_checks.py passed eleven
further exact checks plus two stability cases: original null and receiver
geodesic equations, incidence determinant/derivative and fixed-ell orbit
condition. At m=1,a=10, V'' is 1/875 for Lambda=0 and 19/21000 for Lambda=1e-4.
These scripts import no parent implementation and were frozen before execution.

After parent implementation/results exposure, saved_checks.py independently
recomputed all forty saved endpoint frequencies and sky directions by diagonal
metric contractions. It recomputed four midpoint incidences, receiver proper
arrival times and determinants using Gauss–Legendre quadrature rather than
the parent's default tanh–sinh quadrature. It also differentiated the implicit
incidence analytically to check spectral drift against saved finite differences.

Observed maxima:

| Quantity | Absolute discrepancy |
|---|---:|
| Saved endpoint frequency ratio | 3.56e-36 |
| Saved sky components | 4.26e-37 |
| Independently integrated incidence | 1.40e-58 |
| Independently integrated arrival proper time | 1.80e-58 |
| Independently integrated determinant | 3.12e-61 |
| Arrival finite-difference ratio vs endpoint ratio | 4.28e-11 |
| Arrival-derived drift vs spectral finite difference | 1.89e-12 |
| Analytic implicit-map drift vs spectral finite difference | 4.00e-12 |

Both frozen steps pass the original 1e-7 accuracy/.4 error-contraction bounds.
This is high-precision floating-point agreement, not interval certification or
an empirical test. Root solving was not independently repeated by this reviewer;
the other four midpoint quadratures test saved roots directly. Symbolic proof
establishes the local incidence identity without relying on those numerical
tolerances. No full Jacobi map or source estimator is claimed checked.

All three reviewer executions returned exit0, with actual stdout and empty
stderr preserved. Exact commands are the following, each with stdout/stderr
redirected to its same-named file in review_fidelity/:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 udt_conditional_source_geometry_2026-10-04/review_fidelity/source_checks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 udt_conditional_source_geometry_2026-10-04/review_fidelity/direct_checks.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 udt_conditional_source_geometry_2026-10-04/review_fidelity/saved_checks.py
```

Python3.10.12, SymPy1.13.1, mpmath1.3.0. Each imposed 2GiB RLIMIT_AS,
one BLAS/OMP thread, CPU only, no timeout or fit. Maximum reviewer RSS observed
51220KiB. Fourteen exact cases plus forty saved records: fifty-four finite
cases total. The reviewer used one floating precision, 60 digits; parent used
36/60 for actual solves and 65 only for saved-number crosscomparison. The latter
is arithmetic on already-computed records, not a third solve/refinement.

## Repair and false-pass scrutiny

Actual original and diagnostic captures both returned exit1. Their first drift
discrepancy was 0.0034964460. A(tau_e)=tau_o has Z=A', so dZ/dtau_o=A''/A'.
The original check mistakenly used A''/(A')². The diff shows only this
denominator was repaired; input values, candidate equations, precision and
tolerances stayed fixed. Independent recomputation reintroduces that wrong
denominator and again obtains 0.0034964460, above 1e-4, whereas the corrected
comparison passes. This is a real caught defect, not a tautological guard.

The original shared-code symbolic/numerical tests are not counted as a fresh
independent implementation here. My source-first/exact reconstructions and
later Gauss–Legendre/contraction postprocessing supply distinct argument or
implementation axes within shared premises. Check counts themselves do not
prove scientific coverage, truth, chronology, native status or physical value.

## Remaining caveats and return

The construction covers one declared static spherical exterior and local direct
outward equatorial null branches with circular test sources and outgoing radial
free receivers. Negative Lambda is included in reviewer radial algebra/examples,
but the parent's full ray family exercises only Lambda=0 and +1e-4. No full
metric family, turning ray, horizon passage, multiple image, finite-source
formation, source interior, physical mass coupling, disk self-gravity, nonlinear
stability, empirical parameter inference or native additional-effect selection
is inferred. Old proofs/classification packages and the complete registry were
not independently replayed. Protected local payloads were untouched.

Strongest survivor: the explicit conditional exterior really does join regular
source clocks, free received clocks, null timing and finite sky direction using
one geometry, with a precise free-preparation single-shift limitation. The
native response/source/positional joins remain open. Await the final central
integration text and bindings for a separate integration attestation.
