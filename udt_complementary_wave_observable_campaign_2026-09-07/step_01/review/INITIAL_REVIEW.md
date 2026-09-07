# CO1 initial direct adversarial review

2026-09-07 22:06 UTC. Reviewer `/root/co1_geometry_review`, fresh context;
exact model UNKNOWN, different-model/human/formal review UNTESTED.
Verdict: REPAIR_REQUIRED; bounded scientific landing retained. One grouped
source-preserving repair closes the two defects below. No next-step scientific
use is covered until the repaired candidate is checked.

Initial candidate SHA256478100481ea75cc363b8c0c60c0f7e2338fbdc600db0bee140b1a2d16feb92b4;
geometry_checks.py SHAdf61009c19d4755e3ec17fcc60219ae0e0f01aa0f66045531d75dc588a5a02a1;
geometry_run.stdout SHA1ce4666a64540ee8eec49bc82ffc1b64a9264e0e9eb68752244612c527a4e9e5.
All three supplied hashes were independently checked before reading the files.

The source-first seal was saved and sent before candidate/code/output intake.
After that seal, the parent supplied a candidate outline and later disclosed
the rows/columns typo before direct inspection. R1a below is therefore
parent-disclosed, independently confirmed; R1b is reviewer-discovered.
Independent standard-library rational/metric-jet checks were written and run
before candidate intake and import none of its implementation.

## R1a: null-basis dimensions

Initial candidate line78 says rows of Z span ker(F^dagger) while using
z=Z^dagger d. For F of shape N-by2, each null vector has N components.
That displayed multiplication requires Z to be N-by(N-r), with COLUMNS
spanning the null space. The null-dimension theorem is correct; this is a
dimension/conjugation presentation defect, not loss of the theorem.
Smallest repair: say columns and give Z's dimensions. If rows are retained,
the multiplication and conjugation conventions must instead be changed.

## R1b: complex residual covariance orientation

Initial lines95-99 use residual r=d_J-F_J F_T^-1 d_T, coefficients
w=(-F_J F_T^-1,1), and variance w^dagger C w. With w declared by those
entries, it is the coefficient ROW of the displayed residual. The correct
variance for centered complex error covariance C=E[e e^dagger] is
w C w^dagger. Equivalently define a column w as the ADJOINT of that row and
write r=w^dagger d, variance w^dagger C w. The distinction matters because
the candidate explicitly admits complex resolved-frequency response.

Concrete counterexample: F_T=I2, F_J=(i,0), coefficient row b=(-i,0,1), and
C=[[1,0,i/2],[0,1,0],[-i/2,0,1]]. C is Hermitian positive definite, with
eigenvalues1/2,1,3/2. Correct b C b^dagger=3; the literal transposed-column
interpretation of the initial expression gives1. This is a factor-three
variance error inside the stated mathematical class. It is not a measured
LIGO covariance or a claim of a data-processing bug.

The finite counterexample is preserved in complex_variance_diagnostic.py and
complex_variance_run.*. Every operation is exactly representable dyadic
complex arithmetic; the script gives3 versus1. The parent's existing six
finite defect checks do not exercise this formula and cannot certify it.
Smallest repair: explicitly use row b=(-F_J F_T^-1,1), r=b d, centered
C=E[e e^dagger], Var(r)=b C b^dagger, and add this complex positive-definite
case plus a wrong-conjugation rejection to the finite checks. Retain all
initial candidate/code/output evidence before repair. No physical premise,
event choice, source model or core rank/tidal conclusion changes.

## Survivor and optional scope clarification

The exact pp-wave calculation, weak tensor tidal map, fixed-sky rank-nullity
argument, calibration-leakage bound and distinction between geometry and
instrument/source law survive substantive scrutiny. The arbitrary-function
pp-wave generalization is applied to the admitted equation and analytically
leaves only Ric_uu=-(H_xx+H_yy)/2; the Hessian is trace-free at every u.
The TT formula follows directly from linearized Riemann in the declared flat
background/gauge, rather than from interpreting a coordinate lapse.

Candidate E means curvature in m^-2; the independent source-first seal uses
c_E^2 E in s^-2. Both yield the same factor1/2 and physical deviation law;
this is a recorded convention difference, not a defect.

Full-rank training is correctly a sufficient condition. For completeness of
the rank-deficient branch, an OPTIONAL useful sentence is that a heldout row
can be predicted whenever it lies in rowspace(F_T), even if F_T has rank1.
Example training rows(1,0),(2,0) predict holdout(3,0), but cannot predict
(0,1). This clarification is not required to repair a false statement.
If adding unknown-sky explanation, preserve that fitting sky can leave a
model residual over many waveform samples; it simply is not an untouched
contrast. There is no universal subtraction of two detector channels per bin.

The source-bound practical continuation is justified: inspect actual detector
geometry at a supplied EM sky and source-supported release/calibration route.
No claim of sufficient statistical power or empirical residual follows now.
External optical sky remains conditional on counterpart association and
astrometric errors, with GW-triggered selection exposure. The inspected
[LVC tests paper](https://dcc.ligo.org/public/0150/P1800059/008/main.pdf)
retains GR phase templates and pure-mode comparisons; its odds are not used
as waveform-free evidence. The supplied response tensor agrees with the
[official LAL detector documentation](https://lscsoft.docs.ligo.org/lalsuite/lal/group___create_detector__c.html).
[GCN21529](https://gcn.nasa.gov/circulars/21529) supplies an optical coordinate
route, not a theory-free counterpart-association proof.

## Actual checks and omissions

- independent_checks.py uses direct linearized Riemann and exact rational
  arm contractions/Gauss-Jordan rank checks: the electric acceleration matrix
  is[[-3,2,0],[2,3,0],[0,0,0]], Ricci zero, and the unit-arm detector null is
  (2016/4225,-120/169,24/25). Nine rational waveforms cancel exactly and are
  recovered by an invertible training pair. Rank1 predictable/unpredictable
  holdouts, nuisance saturation and an alternative signal invisible to the
  null are explicit separators. A physically normalized near-aligned rank2
  pair turns0.001 channel error into250.00000000075 cross-mode error.
- independent_ppwave.py directly reconstructs inverse metric derivatives,
  Christoffels and Riemann from three exact metric jets with independent
  A,A',A'',B,B',B''. Ricci is zero and R_uiuj is[[-A,-B],[-B,A]] each time.
  These are finite independent anchors; the analytic argument and symbolic
  source calculation own the arbitrary-function assertion.
- Actual candidate command replay exited0 in0.309344s; stdout is byte-identical
  to the parent output. This is regression, not independent implementation.
  Independent runs took0.016971s and0.298730s; covariance diagnostic0.014464s.
  Python3.10.12; replay SymPy1.13.1. Existing run_capture.py enforced512MiB AS,
  60s CPU/wall, preserved exact commands/stdout/stderr/timing and refused
  overwrites. All stderr files are empty, no timeout/GPU/install.
- The actual full349-row parent premise audit was inspected and independently
  hashed31691c686f06aca6b5eafe221b4d760b5b5ff4b81a9f17b78f7e58f438cfb48c:
  exit0/PASS, empty stderr,401.315662s,2GiB/900s. It was NOT independently
  replayed here. Only G261/G276/G312/G313 status/source fields were then queried.
- No strain arrays, real detector rank/conditioning, noise/PSD fitting,
  source-template analysis, source theorem suites, metrology recertification,
  global metric joining, protected payloads or GOCE evidence were read/run.
  No accepted grades, premises, canon, manuscript, roots or git were changed.

The candidate's six declared hostile checks are finite statement controls,
not an exhaustive detector or mathematical-expression validator. Their success
does not resolve R1b. No claim that all potential false passes were searched.
This reviewer writes only the assigned review directory. Full approval remains
conditional on checking the exact same-premise repair and preserved originals.
