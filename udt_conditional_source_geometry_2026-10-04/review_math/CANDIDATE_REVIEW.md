# CGE1 exposed mathematical candidate review

Verdict: `VERIFIED_WITH_CAVEATS` for the restricted conditional construction in
`INITIAL_CANDIDATE.md` SHA-256
`ce2b962bbf47e09dfd120036e1b06f2e6b06f0c18ac1e26766a490830e4fa8c9`.
No unresolved mathematical defect was found inside its declared domain. This
is not native response-class admission, physical source formation, empirical
validation or promotion. Final central integration review remains pending.

## Exposure and independent axes

Reviewer `/root/cge_math` is the same actual separate context that wrote the
preserved `SOURCE_FIRST.md`. Candidate review begins only after that report and
its independent symbolic/incidence anchor. I subsequently read the initial
candidate, numerical freeze, original parent code, initial/diagnostic capture
receipts, method references, corrected checker and selected saved result. The
parent disclosed its checker failure and its proposed explanation before this
exposed review. I did not read another review's contents/verdict. Listing package
filenames exposed their existence only. No different-model claim is established.

Independent mathematical arguments and implementations are documented in the
source-first report. For the exposed phase, `ode_crosscheck.py` performs direct
affine-ray/proper-receiver ODE shooting, using SciPy DOP853/root rather than the
parent's mpmath quadrature incidence. It imports no parent functions and used no
saved parent values as initial guesses. The subsequent saved comparison uses
separate Decimal arithmetic. Versions, commands, raw outputs and hashes are
saved. SymPy/mpmath backgrounds remain shared in the source-first stage; fresh
context does not imply a distinct model or an independent symbolic engine.

## Findings on the argument

The original Ricci components, integrated f=1-2m/r-Lambda r^2/3, circular clock,
free receiver, null ray and endpoint frequency agree with the independent
source-first derivation. The full conditional R10 hypotheses remain inherited;
the current G312 source does not allow adopting this equation as native UDT.
The candidate labels all source/environment and clock choices adequately.

The orbit's D=1-3m/a normalization and Omega^2=m/a^3-Lambda/3 are correct. Domain
conditions f>0,D>0,Omega^2>0 are separate and all retained. Finite-radius orbiting
clocks replace the unavailable central source clock. The fixed-angular-momentum
potential criterion is correctly confined to radial test-particle linear
stability; its positivity in the numerical examples is not a disk stability
claim.

Equation (5) solves two actual incidence conditions; neighbouring emission
events change both b and R. The Jacobian determinant is negative in the stated
(R,b) ordering and nonzero on R>a, f>0,s>0,v>0. My source-first determinant has
the opposite sign because it uses (b,R); this is consistent, not a disagreement.
This proves local regular correspondence and arrival/frequency equality, not
global uniqueness or absence of other images.

The observer tetrad is unit and orthogonal, and equation (7) gives propagation;
the source sky is its negative. ACP1's full angular-map restriction remains
open, as the candidate explicitly states. This finite equatorial incidence
does not silently become a two-dimensional disk Jacobi map or scalar distance.

The exact radial single-shift family correctly varies receiver preparation.
It is a witness against identification from that one observable with preparation
free, not an all-record degeneracy, a fixed-preparation degeneracy or a global
parameter-identifiability theorem. My independently derived exact cases also
include negative Lambda and demonstrate the same scoped phenomenon. Source
mass identification, physical class membership, scale/sign and data reduction
remain separate open joins. There is no arbitrary source law or fitted Z(D).

The Ric(k,k)=0 statement is correct in this branch, and the candidate correctly
keeps Weyl optical tides and full clock/angle dependence. Neither scalar Ricci
cancellation nor weak potential alone controls the full observable map or the
fractional orbital Lambda term. No theorem of native global insufficiency is
inferred from these examples.

## Checker failure and smallest repair

The initial checker, SHA-256
`1aebf5c0811d4bb52226c71d4a2a2703e195ba8d3b1c06111792b0cc0f2a0748`,
failed its drift comparison. With actual arrival map A(tau_e), Z=A', the chain
rule gives dZ/dtau_o=A''/A'. The original checker used A''/(A')^2; this is the
defective step. The candidate/ACP1 text already had the correct Z'/Z formula.

I inspected the exact original/corrected diff: the sole code change is
`from_arrival=arr2/(za*za)` to `from_arrival=arr2/za`. Corrected code SHA-256 is
`954f7417eafcdb706a84dd2b33878dae56ee24a41cd9ddf937906828a282903f`.
No input or tolerance change appears. The initial file and failed capture remain.
This is a source-preserving implementation repair; no equation, premise or
scientific conclusion changes.

I independently recomputed both formulas from all saved arrival/endpoint arrays,
with 50-digit Decimal arithmetic. All eight precision/query groups pass the
declared corrected error/convergence conditions. Corrected coarse errors range
from 7.93e-13 to 1.89e-12; half-step errors are one quarter, to the shown digits.
The original erroneous expression gives discrepancies approximately 0.00350
through 0.00696, far above the unchanged 1e-7 tolerance. This actual saved-data
countercheck catches the defect and supports the smallest repair.

The parent's 65-digit final arithmetic only compares saved 36-/60-digit strings;
all incidence solves and quadratures use two precisions. This exposed review
records that distinction rather than calling it a third solution refinement.
There is no additional solved-case result at 65 digits.

## Independent saved-incidence recomputation

Frozen input: m=1,Lambda=0,a=10,R0=50,E=1,phi0=-0.2,t_e=0. I integrated the
ray in affine parameter and the receiver in proper time, then matched t,r,phi
with three-variable shooting. No candidate code was imported. The independent
source-first derivation owns the reduced ODE equations. The solves preserve the
null and receiver norms to maxima 8.61e-14 and 5.78e-15; the endpoint coordinate
residual maximum is 1.67e-11. Against the candidate's saved 60-digit row:

| Quantity | Candidate | Absolute ODE difference |
|---|---|---|
| R | 59.9562183817957531 | 1.68e-12 |
| b | 2.37714470756410585 | 5.11e-11 |
| tau_o | 52.1825982872376093 | 3.84e-12 |
| Z | 1.30704670651245688 | 2.29e-12 |
| radial propagation component | 0.998900463017286264 | 1.10e-13 |
| azimuthal propagation component | 0.046881392725164609 | 1.01e-12 |

All are inside the predeclared 2e-9 finite-agreement threshold. This is a
different numerical method and independent implementation, plus original
constraint checks. It does not claim validated interval bounds, arbitrary
parameter coverage or full-data replication. It adds one case to the four
source-first cases: five reviewer physical cases total, no grid/GPU, below 100.
Only the declared 50-digit source-first and float64 ODE levels solve cases.

Exact commands:

    python3 udt_conditional_source_geometry_2026-10-04/review_math/ode_crosscheck.py > udt_conditional_source_geometry_2026-10-04/review_math/ode.stdout 2> udt_conditional_source_geometry_2026-10-04/review_math/ode.stderr
    python3 udt_conditional_source_geometry_2026-10-04/review_math/compare_saved.py > udt_conditional_source_geometry_2026-10-04/review_math/comparison.stdout 2> udt_conditional_source_geometry_2026-10-04/review_math/comparison.stderr

Both exited 0; stderr empty. NumPy 2.2.6, SciPy 1.15.3, Python 3.10.12. The ODE
process sets one BLAS thread and a 2GiB address limit, with no timeout. Saved
arithmetic is a small dependency-free Decimal pass. Exact reviewed versions and
all recomputed values are in `SAVED_COMPARISON.json`.

## Checks omitted and return boundary

I did not replay the complete parent 40-ray calculation, source-package historical
regressions, current premise verifier or external papers. I inspected the parent
equations/code and saved evidence, independently constructed the load-bearing
mathematics, checked a distinct finite anchor before exposure, recomputed one
saved ray by another method and recomputed saved drift checks. Parent orchestration
owns required repository/premise/banking checks; those are not inferred passed
from this review. No endpoint action or registry/CANON edit is reviewed here.

This verdict permits calling the mathematical candidate reviewed at its exact
conditional scope. Actual final central integration must still be inspected in
this separate context, with final versions recorded. It cannot promote native
physics or observational conclusions.
