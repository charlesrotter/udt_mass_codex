# Direct adversarial review of positional geometry / received clocks

Verdict: **VERIFIED-WITH-CAVEATS**, at the frozen conditional mathematical and
documentation scope. No substantive mathematical or fidelity defect found;
no scientific repair requested. This verdict does not establish a native
positional response law, adopt a physical history, upgrade sources or confer canon.

## Context, exposure and frozen target

Reviewer: `/root/positional_connection_review`, a fresh separate Codex agent
context, same inherited runtime. Precise deployed model/version is not exposed;
no different-model, human or formal-proof independence is claimed. The source-first
assessment and ten independent exact checks were frozen before candidate exposure
in SOURCE_FIRST_FREEZE.json. The current direct stage was authorized by the parent
after its 13-path DIRECT_REVIEW_FREEZE.json, timestamp 02:51:33 UTC.

The reviewed candidate SHA-256 is
`58b02dc275c480856fc403a728815fa68edc6ce4529c7b0901dc447ce7921e36`.
I read the frozen candidate, decision brief, owner statement, work order,
check_connection.py, actual CHECK_RESULT/CHECK_EXECUTION, SCOPED_REGISTRY, and
all five live-document deltas. All 13 frozen files matched at direct-review opening.
No parent implementation was seen before the source-first assessment; the direct
checks below were written after exposure and are disclosed as such.

The parent startup verifier's preserved stdout and execution record were read:
exit 0, 406-row PASS, 408.729369 seconds, 900-second cap, empty stderr. That is
attributed execution evidence, not a reviewer re-run of the full premise verifier.
I independently compared every saved field for the six exact registry rows
G402/G403/G312/G269/G265/G220 against the current TSV; all matched. G402 and G403
are BANKED_DERIVED_CONDITIONAL / VERIFIED_WITH_CAVEATS with their exact caveats.
The historical UNPROMOTED headers in the original NCI1/DCI1 candidates do not
override those current grades. My earlier source-first assessment did not perform
this exact registry check; this direct-stage update supplies the current typing.

## Adversarial reconstruction of the mathematical join

1. **Received ticks and redshift.** The positive regular reception-map slope
   r=F' is the received/emitted differential proper interval ratio. Its inverse is
   the corresponding frequency ratio, so 1+z=r. The candidate expressly limits the
   pointwise identity to the differential observable and gives interval averaging
   for finite pulses. It does not silently add signal content or an instrument law.

2. **Moving endpoints.** Differentiating
   t(x_A(t_A);t_A)=t_A gives J_A=1-epsilon p_A v_A. Differentiating
   t(x_B(t_B);t_A)=t_B gives J_B=(1-epsilon p_B v_B)dt_B/dt_A.
   At fixed x the ODE variation is J_x=epsilon p_t J. Timelikeness makes both
   boundary factors positive. With ds=epsilon dx>0, integration gives the
   candidate's positive coordinate slope for epsilon=+1 and epsilon=-1.
   Multiplication by the actual endpoint proper-clock rates produces

       log r = log(N_B/N_A) + epsilon(eta_B-eta_A) + integral p_t ds.

   No acceleration term has been omitted from a supposed independent factor:
   arbitrary smooth endpoint acceleration influences the supplied endpoint events
   and velocities; geometry and null incidence own the full result.

3. **Equivalent fixed-coordinate expression and reciprocal specialization.**
   Along the ray, d log N/ds=epsilon partial_x log N+p partial_t log N.
   Adding p_t and using p=A/(c_E N) yields equation (2). Substitution
   N=e^-phi, A=e^phi yields (2R), including the minus sign on
   epsilon partial_x phi. p has time/length units; p_t ds and the logarithm are
   dimensionless. The text correctly labels the time-live phi specialization as
   a diagnostic, not an independently derived extension of the full areal branch.

4. **Coordinate cancellation.** For a positive time reparameterization T=f(t),
   Ntilde=N/f', ptilde=f'p and beta is unchanged. Since dt=p ds,

       integral partial_T ptilde ds = integral p_t ds + log(f'_B/f'_A).

   This precisely cancels the change in endpoint lapse. The lapse-only flat
   control therefore has r=1 despite changing coordinate slowness. Calling the
   integral alone physical positional redshift would be wrong; the candidate
   explicitly rules out that identification. General covariance belongs to the
   G220 observable; the diagonal formula retains its declared chart domain.

5. **General local bound.** I reconstructed the NCI1/DCI1 identity independently
   before candidate exposure. The sign in log r=integral(H+a.n+sigma(n,n))dell_U
   agrees with delta=-log r. The bound is an immediate integral/exponential bound
   on a regular tube with a uniformly bounded supplied congruence. The small
   parameter KS is dimensionless. The text keeps the path-length convention,
   boundedness and endpoint matching explicit, and excludes the false claim that
   a fixed nonzero relative-velocity Doppler factor vanishes at small distance.

6. **Mutual causal exchange.** The affine-scale arrival map has derivative
   exp(bL/c_E); both separate future directions share that slope, while a composed
   echo has its square. Neither is the inverse of the first event map. Positivity
   of a0+b tau at emission ensures the constructed reception also remains on
   the positive branch. The formula is valid for either sign of b on that domain;
   the continuous zero-b limit is stated correctly. Its Taylor error bound is
   correct for |bL/c_E|<=h0 and gives no native dimensional scale.

7. **Failure of the proposed native selection.** The independent map

       T=(tau+a0/b) cosh(bx/c_E),
       X=c_E(tau+a0/b) sinh(bx/c_E)

   pulls back -c_E²dT²+dX² to the affine metric for b!=0. This explicitly verifies
   local flatness and the ordinary-recession interpretation. dt=(a0+b tau)d tau
   gives the reciprocal longitudinal form but changes no physics. The candidate
   acknowledges both facts and declares failure to derive a distinct positional
   effect. That is a scoped ownership failure of this attempt, not a theorem that
   all UDT routes fail or that a new postulate is necessary.

## Independent calculations and false-pass audit

`direct_checks.py` uses a different mathematical and implementation route from the
author: exact conformal-Minkowski null incidence with nonlinear monotone time and
space coordinate maps, three supplied metric/observer controls, both future
directions, and accelerated observer curves. It solves the exact incidence equation
with Brent's method and compares the resulting proper-clock derivative against
independent path quadrature of the candidate formula. It also changes time
coordinate and directly integrates finite proper clock intervals.

Five exact symbolic residuals are zero, including all four components of the
explicit Minkowski pullback above and time-reparameterization cancellation. Six
floating-point controls pass: largest candidate/direct ratio difference is
1.3322676295501878e-15; largest final finite-pulse error is
8.628372016872277e-9. The nonconstant finite-pulse errors decrease consistently
with second-order centered intervals at the three declared interval sizes. This
is a convergence diagnostic, not a certified error bound for arbitrary metrics.
Omitting endpoint lapse, omitting the integral, and reversing the motion sign
are each rejected by separating controls at errors exceeding 1e-5.

The script uses explicit exceptions for its guards. Python 3.10.12, SymPy 1.13.1
and SciPy 1.15.3, CPU only, no grid/GPU, and 120-second caps are recorded with
exact commands, stdout/stderr and source hashes in the adjacent run records.
The source-first ten exact checks are a separate earlier stage, not extra samples
of the six direct controls or a claim of statistical evidence.

For reproducibility I copied the frozen author script byte-for-byte under
review/author_replay/ and ran it there, preserving the parent's files. It returned
12 exact checks, eight floating-point controls and three rejected wrong-formula
types; maximum formula/Hamiltonian difference was 2.220446049250313e-16 and final
pulse error 8.080935920418142e-11. CHECK_RESULT.json reproduced byte-for-byte at
SHA-256 `f7058cff99595298ee13a80e3c242551197ef5c60f1af89bae8836b429c81166`.
This exact-code replay is regression/reproducibility, not implementation independence.

The author's affine_reciprocal_time_change check is a simple coefficient-cancellation
identity, not by itself an independent test of a full coordinate transformation.
The substantive analytical coordinate argument and the independent checks above
supply that support. The author numerical guards use ordinary Python assertions;
the recorded unoptimized command exercises them. No optimized-mode or broad solver
guard claim is made. No new vacuous assertion was found carrying the conclusion.

## Documentation fidelity and retained limits

The five frozen live-document edits accurately foreground the owner's stated
interpretation, retain observed c_E and the units correction, put motion/gravity
and positional intent in one geometry, and identify slower received ticking with
redshift. They preserve the distinction between that identity and the unclosed
physical separation-to-clock-rate assignment. Solar-distance detectability remains
an owner expectation, without a cutoff, chosen scale or guaranteed net sign.
SR/GR correspondence remains an intended result to demonstrate; GR remains a filter,
not imported dynamics. No scientific grade, source equation or canon changed.

The reviewed maximum survivor is an explicit conditional received-clock connection
plus a correctly stopped, unsuccessful native-selection attempt and accurate owner
documentation. The construction is restricted to the declared regular supplied
geometry/query class. No empirical law, physical observer population, selected
history, signal-content identification, angular/screen completion, global result,
native response equation or solar onset is established. A reviewer cannot elevate
those claims by accepting the conditional algebra.

No historical source implementations, global PDEs or full prior reviews were
replayed. No different-model axis was available in this one-reviewer work order.
The source-first independent argument, direct different implementation and exact-code
replay are distinct evidence types. Protected payloads and parent/live files were
not altered by the reviewer. There is no unresolved substantive objection requiring
a same-premise repair. Later reviewed-status/closeout wording must be checked only
for correspondence to this frozen result before completion is claimed.
