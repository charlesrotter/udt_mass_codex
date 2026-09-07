# CO1 final review

2026-09-07 22:13 UTC. Reviewer `/root/co1_geometry_review`, fresh separate
context; exact model UNKNOWN. Different-model, human-specialist and formal
verification are UNTESTED.

VERIFIED-WITH-CAVEATS. The one grouped same-premise repair is closed. No
unresolved load-bearing objection remains within CO1's conditional geometry,
measurement-map and fixed-sky information scope. This verdict permits the
already authorized CO2 finite design step; it establishes no empirical null
result, instrument certification, scientific promotion or distinctive UDT
evidence. The exact candidate retains the supplied measurement laws and all
physical ownership limits.

## Exact reviewed artifacts and preservation

| Artifact | SHA256 |
|---|---|
| CANDIDATE.md | c5dd7945858f287845ebfbf6f38e0bdf9bc929e66463abd8b08105959a3d7ad0 |
| geometry_checks.py | 48766db54bbff840ac3fad54c54f8d18061bcc9290480694e6f02f8ebbdc6819 |
| repair_run.stdout | 37854cc5c016d268181f8fd071c078f1b94abd1b40be8a01832416c90fefd9c5 |
| INITIAL_CANDIDATE.md | 478100481ea75cc363b8c0c60c0f7e2338fbdc600db0bee140b1a2d16feb92b4 |
| INITIAL_geometry_checks.py | df61009c19d4755e3ec17fcc60219ae0e0f01aa0f66045531d75dc588a5a02a1 |
| geometry_run.stdout, initial | 1ce4666a64540ee8eec49bc82ffc1b64a9264e0e9eb68752244612c527a4e9e5 |
| review/SOURCE_FIRST_SEAL.md | 39f13d608c7c205782f481c02227dc50d81c7917ab8ad8db0b3cf3a25251dab2 |
| review/INITIAL_REVIEW.md | 67f45bebef4c6742e288b08f3a16f69fc60b57cbf234332c9390bf432e913582 |
| review/focused_rereview.py | 53d87c7fe148bddd6bd382e08ea59acb2c048b5934932ca5ae660077421fd76a |
| review/focused_rereview_run.stdout | 217941036f6b6c8c9a40b16e0949b8943216520e57703cfe6c3d974ec3c7dd8d |

All hashes above were independently checked. Paths are relative to step_01.
The final diff changes the Z basis dimensions, complex covariance convention,
explicit centering/bias qualification, row-space holdout clarification and R1
history only. The first repair wording had SHAa80ac278590784d95b0430ac60eb76a44ae153569514a1257d7e3d0bc3e8807f;
the final wording completes the originally requested centered-error qualifier.
This is one grouped R1 repair, not a new scientific hypothesis or result cycle.
Code/output remained unchanged during that final wording completion. Source-first
seal, initial objections, original bytes and covariance counterexample survive.

## Substantive finding

The current adopted bounded vacuum equation admits the local Ricci-flat
two-function family H=A(u)(x²-y²)+2B(u)xy. Direct metric geometry gives
Ric_uu=-(H_xx+H_yy)/2=0 and R_uiuj=[[-A,-B],[-B,A]]. Arbitrary smooth A,B
are allowed locally, subject to the stated arena; no source or global history
is selected. In the declared weak TT measurement regime, linearized Riemann
gives R_hat0i hat0j=-h_ij,tt/(2c_E²). A calibrated equal-arm differential
response supplies D:h and hence its band-limited tidal projection. This
probes a curvature channel absent from a single effective stationary clock
gradient. It does not infer a joint laboratory/source metric or apply a
stationary-Killing identity to a nonstationary wave.

For fixed direction, delays, response and waveform sample/frequency, the
N-by2 matrix F has N-rank(F) algebraic null directions. This is rank-nullity,
not an empirical finding. Rank2 recovers two arbitrary tensor values; rank1
recovers one combination. A holdout row is predictable exactly when it lies
in the training row space; full rank2 is sufficient for any tensor holdout.
Small singular values can make an algebraically identified waveform unusable
in noise. No null contrast sees an alternative component lying in col(F).

A supplied EM direction can remove a same-strain direction fit, conditional
on astrometry and counterpart association, while GW-triggered follow-up and
published outcome exposure remain. Fitting sky using the same proposed test
contrast requires accounting for the resulting fitted residual/selection;
it is not an untouched contrast. Joint sky inference can still retain
constraints across multiple samples, so no blanket loss-of-all-information
claim follows. The inspected [LVC GW170817 tests paper](https://dcc.ligo.org/public/0150/P1800059/008/main.pdf)
retains GR phase templates and pure-mode comparisons; those published odds
are not a waveform-free null result. The [official detector response](https://lscsoft.docs.ligo.org/lalsuite/lal/group___create_detector__c.html)
agrees with the supplied tensor map. [GCN21529](https://gcn.nasa.gov/circulars/21529)
provides the optical-coordinate route, not a theory-free association proof.

## Objections, repair and independent checks

R1a, parent-disclosed and independently confirmed: Z must have N-by(N-r)
dimensions with COLUMNS spanning ker(F^dagger) to use z=Z^dagger d. Closed.

R1b, independently discovered: residual coefficient row b=(-F_J F_T^-1,1)
has variance b C b^dagger for centered stochastic error covariance C. The
initial unconjugated-column convention gives1 instead of3 for the explicit
Hermitian positive-definite complex covariance in INITIAL_REVIEW. Closed.
The final candidate also distinguishes nonzero bias b mu and an uncentered
second moment from variance. This distinction required no new physical
premise or code change.

The independent source-first implementation uses Fraction arithmetic, direct
linearized Riemann, physically normalized rational detector arms and rank
elimination. It recovers the tidal factor/sign, nine waveform cases, a null
vector, rank1 holdout separators, nuisance saturation and a null-invisible
nonzero alternative. A near-aligned full-rank example converts0.001 channel
error into250.00000000075 spurious cross-mode amplitude. This is an exact
design counterexample with rounded display, not real detector metrology.
A separate direct Christoffel/Riemann reconstruction verifies three exact
pp-wave metric jets with independent A,A',A'',B,B',B''. These are independent
finite anchors; the analytic argument and symbolic calculation own the
arbitrary-function quantifier. The source-first seal uses acceleration tide
c_E² R in s^-2 while the candidate names R in m^-2; the conventions agree.

The parent implementation was actually replayed and reproduced byte-identical
output. After repair, focused_rereview.py checks all preserved initial hashes,
reproduces repair output exactly and verifies that every original result field
is unchanged except the added covariance block and rejection label. It then
reinserts the wrong conjugation directly into the producer expression IN
MEMORY and observes its numerical assertion fail with1 instead of3. A separate
standard-library dyadic-complex evaluation reproduces3 versus1 without SymPy.
The new finite guard therefore has an actual defect catch, not only a copied
pass label. No exhaustive validation of all expressions/instruments is claimed.

All computational runs used the inspected existing run_capture.py utility,
512MiB AS and60s CPU/wall, one short CPU child at a time, no GPU/install.
Python3.10.12; parent replay SymPy1.13.1. Independent runs took0.016971s and
0.298730s, initial replay0.309344s, covariance diagnostic0.014464s, focused
repair replay/catchproof0.371055s. All exited0 with empty stderr and no timeout.
Commands, versions, timing, outputs and limits are preserved in their run
triples. Passing same-code replay is regression, separate from independent
argument and implementation.

## Controlling limits and omitted work

W4 remains a working physical-metric premise; G312's premises remain
owner-adopted provisional, not derived or canon. Laser/actuation/calibration,
proper units, free-mass response, timing, detector worldlines and event/query
data remain supplied. Finite-frequency, rotation, background/plane-wave and
nonlinear corrections need transfer computation or bounds before a precision
test; small parameters alone are not metrological error bounds. No DC/full
Weyl/full metric reconstruction follows from band-limited projections.

Rank is not sensitivity, statistical independence or a significance. Noise
covariance/centering, calibration leakage, sky uncertainty, training error,
event/band/window selection and nuisance freedom must be justified for a real
test. Arbitrary detector errors erase restrictions. Gaussian independence is
only an example under additional hypotheses, not adopted. The [GWOSC release](https://gwosc.org/events/GW170817/)
has processing and channel limitations; none was empirically recertified.
CO2 must distinguish static geometric conditioning from release eligibility.

The parent's actual349-row startup audit was inspected and independently
hashed31691c686f06aca6b5eafe221b4d760b5b5ff4b81a9f17b78f7e58f438cfb48c:
exit0/PASS, empty stderr,401.315662s under2GiB/900s. It was not independently
replayed here. Source theorem suites, raw strain/PSD arrays, real detector
conditioning, metrology, source dynamics and generic statistical coverage
were not replayed or inferred. No protected payload, GOCE evidence, fit,
physical adoption, scientific grade, canon, fixed manuscript or git change.

HEAD independently remains9ed73efe3d7d24a5fd6666bd904557cf0b24e0fd on grok.
Parent-owned status-file edits appeared during shared review; this reviewer
modified only step_01/review/. No host-wide process or remote-sync claim is
made. Review completed within30minutes. CO1 is complete at its conditional
scope; CO2 remains a separate already authorized design step requiring its
own source checks and fresh review.
