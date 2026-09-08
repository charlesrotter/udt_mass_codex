# RD1 final adversarial review

2026-09-08 00:52 UTC. Reviewer /root/rd1_response_review, fresh separate context.
Exact model UNKNOWN; different-model, human-specialist and formal-verification
axes UNTESTED.

VERIFIED-WITH-CAVEATS for the pinned conditional response/support mathematics
and the present evidence-based RD2 stop. No unresolved load-bearing objection
remains at this scope; no repair was required. RD2 is NOT CLEARED. This is
not a generic no-go for free-waveform GW tests or a UDT verdict, and it does
not certify an instrument, physical target sensitivity or observed constraint.

## Pinned target and sources

Paths are relative to step_01 except ../ entries. Pins were independently
checked; the source-first seal records exact upstream candidate/review and
scientific-source versions.

| Artifact | SHA256 |
|---|---|
| CANDIDATE.md |46e8002a6a0138eaf993476fdc1dd9bbf2a724413bd9558efead2e1229779803|
| checks.py |0be202298d3d5c523f53443786e3776b66196f4f9e461fd61d4ef1c767aeb152|
| checks_run.stdout |1c15a27b5d32888360746953a4782f88c7cf5ebd8ed8c0212bcb0c78c919915e|
| ../SOURCE_LEDGER.md |c943991656c092bd1eed2872863255704d2a20d9409af40fb1d40f2b94a93580|
| ../STARTUP_PREMISE_AUDIT.json |dc7e791fa60c6f5a83df35b90d99453b2c882873615ddd9decdd0edf5149a2c5|
| review/SOURCE_FIRST_SEAL.md |6facd694cbdb75c48e98fc8c8192bba065253b496eebf1458f91e639f9e2db3c|
| review/INDEPENDENT_SOURCE_NOTES.md |56b59a3be4571d8c4609ec49fd40f1846827a6643912d4f78d3b32308a28a33c|
| review/TRAINING_BOUND_NOTE.md |25a43bf31f24341a7987a81251cb567b09154ce3521c33e1e60c583229ac9cb3|

The independent source-first notes, four reviewer scripts, all run triples,
initial critique and machine verdict are covered by REVIEW_MANIFEST.tsv.
Hashes establish correspondence, not truth, independent chronology or
metrological certainty.

## General argument, not only examples

RD1.1 is valid on its actual declared Hilbert spaces. Applying the assumed
bounded left inverse B to training and bounding the two disturbances gives
(1-kappa)||h|| <= ||By_T||+eta_B. Applying the exact nominal prediction
S=A_VB gives the contrast bound rho H_train+eta_r. Uniform nonlinear
disturbance bounds are allowed; fixed linearity of upstream cleaning is
not silently assumed. A probability claim needs a justified joint event
on which all bounds hold. A nonzero mean is not hidden in centered covariance.

The training form can be nonvacuous in independent channel coordinates,
whereas a coarse full-data norm bound can be tautological. Neither fact
establishes power or an achievable physical error budget. The bounded left
inverse and kappa<1 are sufficient hypotheses; the rank1 prediction-only
example correctly demonstrates why they are not necessary for every useful
holdout or quotient. The same full waveform domain must be used throughout.

RD1.2 and its preceding interpolation argument are sound. In the real
whole-line L2 class with Fourier support [-b,-a] union[a,b],0<a<b, point
evaluation is bounded. The Gram quadratic form is a nonnegative integral
of a finite exponential polynomial's squared modulus. Its vanishing on
an interval forces the polynomial to vanish everywhere; derivatives at
one point give a nonsingular Vandermonde system for distinct sample times.
The Gram is therefore positive definite, all finite real targets interpolate,
and v^T G^-1 v is the squared minimum norm. This is an analytic argument,
not an extrapolation from numerical eigenvalues.

For fixed noiseless independent training functionals, orthogonal decomposition
h=h0+z, z in ker T, makes the remaining radius exactly
||p|| sqrt(H_max^2-||h0||^2). The positive/negative p directions attain its
endpoints; p=0 gives exact prediction despite unresolved input freedom.
An H_max below the minimum-norm requirement makes that stipulated class
incompatible. These are complete range statements for this exact Hilbert
problem, not noisy or physical-detector theorems.

The asynchronous point-sampling separator has explicitly checked conditions:
nonzero nominal plus coefficients and delay differences that are not integer
sample shifts. Its surjectivity claim belongs only to that simplified model
without a uniform norm cap. It does not say that arbitrary fixed data fit
within a weak-wave ball or that the real finite-arm/cleaned product is onto.
Small scaling preserves a nonzero output direction and gives a weak diagnostic
wave; quantitative approximate restrictions under a fixed size budget remain.
Band limitation alone does not make a continuum waveform finite dimensional.
A cyclic finite representation and all continuum band-limited functions are
different domains; finite observations cannot supply a left inverse on the
latter. Actual product measurement functionals and their range remain unproved.

RD1.3 follows independently from the arm-transfer integral. The characteristic
function has |alpha|<=2, mean -mu and second moment4(1+mu^2)/3. Triangle and
Taylor-remainder inequalities give the displayed all-real-x bound. For ideal
unit arms, a signed half-arm's plus/cross coefficient norm is
(1-mu^2)/2<=1/2, so the detector-row bound follows. Plancherel transfers a
uniform frequency bound only in the stated stationary whole-line domain.
Time-dependent response, filtering, cropping and waveform support need their
actual composition. No small parameter alone certifies a physical null.

## Source correspondence and practical stop

The independently read T2100313v3 README supplies hourly discrete LIGO and
run-wide Virgo pointwise median/one-sigma response estimates. It identifies
true/model ratios; uncorrected released/true response is their inverse.
These records do not themselves define a joint hard envelope or covariance.

The cached O2 subtraction paper's transfer estimation, safety/injection tests,
finite calibration lines and transient/narrowband qualifications were read
directly. They support intended processing use but not a uniform arbitrary-
waveform error theorem. Downstream software injection does not certify the
earlier processing response. Neither perfect retention nor automatic signal
destruction is inferred.

Official DetResponse.c and LALSimulation.c were read together; the actual
caller supplies beta=fL/c, the callee multiplies by pi, and the local GSL
header confirms normalized sinc. Their nearby comment inconsistency is
reported without alleging a flight-data bug. Mean-arm, interpolation,
segment and rotation approximations prevent treating present master code as
an exact2017 deployed transfer certificate. Exact source hashes and read
routing are in INDEPENDENT_SOURCE_NOTES and the parent source ledger.

The candidate has not instantiated complete response/support error, waveform-
size and joint-noise controls at1e-21 strain sqrt(second). Its arm-only
component cannot authorize setting every other error to zero. Prior static
rank and the exposed33 backgrounds do not establish the missing full-domain
hypotheses. Stopping before RD2 is therefore supported by the approved work
order at this evidence scope. This is not a claim that no adequate document,
bound, waveform class, quotient or other measurement design could ever exist.
No event or new validation data is needed to reach this bounded stop.

## Independent recomputation and defect checks

Before target exposure, independent_definitions.py used Fraction/scalar complex
code to check leakage scaling, common-filter noncommutation, window frequency
mixing, stable recovery and marginal-covariance nonidentification. The exact
wrong-order residual is-1/2; same error diagonals permit null variances0 and4.
Eighty finite stable-recovery cases passed. independent_arm_integral.py used
a separately coded integral route:25 Simpson anchors agree with the supplied
arm expression within1.12422e-9 at256 subintervals; the analytic integral owns
the uniform bound. A wrong extra-pi input differs by0.0270864 in the declared
500Hz/4km/mu0.6 comparator.

After target exposure, independent_target.py used no NumPy/producer imports.
It parsed the saved CO2 design input, computed the2-by2 inverse and its norm
through scalar Gram eigenvalues, and matched B norm6.624486137591258 and
the threshold0.15095510492888012. All nominal delay fractions match exactly.
Arm-only illustrative kappa0.201834809206096 and rho0.0473558256932398 agree;
these are not full physical error budgets.

Scalar Simpson kernel integrals and independent pivoted elimination give
minimum norm squared0.18380428527540804; direct spectral integration gives
0.18380428527546402. Independent holdout prediction is-0.65641587145736,
p norm squared2.8756685220802436, radius1.0725052022401091. Both endpoint
norms equal0.5396294186482855 within floating error. Moving to1.001 times
the radius requires norm squared0.5404298186482852 and violates the cap.
A different exact rational finite-dimensional example gives sharp endpoints
-3 and5 at H_max^2=5; its p=0 control retains exact prediction3.

replay_and_catches.py executes the actual parent script and reproduces stdout
byte-for-byte. It separately reexecutes all five invalid producer assertions.
Four in-memory formula defects—wrong training denominator, interpolant norm,
sharp radius and sinc normalization—fail the corresponding existing guards.
The parent source was never edited. These are same-code regression and finite
defect catches, distinct from the independent implementations and analytic
review; no exhaustive implementation certification is claimed.

## Independence, execution and omissions

The reviewer first read admitted sources and sealed its own requirements,
then performed independent definition/source checks before opening the target.
The parent received source-first domain cautions, training/nonvacuity bounds,
arm convention and integral contributions before freezing. Candidate sections2/5
disclose that collaboration. Source-first independence does not mean no
communication; the reviewed proof partly incorporates reviewer contributions.
Sections3/4 were first seen at target exposure and separately scrutinized and
computed. Shared sources/formulas remain shared foundations.

Exact model is UNKNOWN. Context is fresh; implementations are independently
authored where described; producer replays share code. Different-model,
human-specialist and formal-verification axes remain UNTESTED. The four runs
use inspected existing run_capture.py with512MiB AS/60s CPU/wall and explicit
OPENBLAS/OMP/MKL threads1, one CPU child at a time, no GPU/install. All exited0,
empty stderr/no timeout. Python3.10.12; producer replay NumPy2.2.6. Durations
0.023715578,0.023101556,0.031000569 and0.077625132 seconds; peak RSS15168,
15320,15552 and39636KiB. Exact commands/timing/outputs are retained. No
scientific numerical failure occurred; an initial malformed apply_patch
attempt is disclosed in the source-first seal and created no partial file.

The saved fresh full349 audit record was inspected/hash-checked, not
independently rerun: exit0/PASS,401.102625s, empty stderr,2GiB/900s.
Load-bearing G261/G312/G313 rows match registry SHA
ccd1fd2752a5884dfa2864fc9f3904f9dcc7e22557f6d4057e92ec2c54caf81f.
W4 stays working; G312 premises owner-provisional. Source theorem suites,
actual continuum detector map, physical error estimates, astrometry,
noise coverage, strain/PSD/calibration arrays and event contrast were not
recomputed or inspected. No new data support, fit or physical adoption.

HEAD independently remains grok/291bbd73584318f87697345cd86c48f17064e5de.
Only this review directory was modified. No reviewer git mutation/sync,
protected-payload mining/hash, GOCE work, contact, accepted-grade, canon or
fixed-manuscript change occurred. Remote freshness and host-wide process
inventory are not independently claimed. Review used less than40 active
minutes including startup and saved checks; time awaiting the target was idle.

Status-only closure and a faithful concise return packet may record this
verdict. Scientific changes need matching further review. The one authorized
repair allowance was unused; it is not permission to broaden the result.

