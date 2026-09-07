# TM2 — scalar calibration is not the same as independent testability

Unpromoted conditional candidate; PLAN.md fixes the question and limits.
No measured samples, selected GOCE release or physical nuisance law is used.

## 1. Finite model and distinctions

G313/G358 and reviewed TM1 give a connected ideal scalar kappa=-c_E² Lambda.
For n registered queries let 1 be the n-vector of ones. Supply a FIXED LINEAR
P:R^n->R^m and a fixed nuisance design N:R^q->R^n. Consider

    y=P(kappa 1+N beta+delta)+epsilon,
    p=P1, Q=PN, M=[p Q], theta=(kappa,beta).             (1)

Here kappa and beta are free numbers. The admitted constant-trace model sets
delta=0; delta is a comparison departure, not an admitted new field. Errors
epsilon belong to a separately supplied bounded set, if a bounded-error claim
is made. Let epsilon=0 for §§2–4's identifiability statements.

The event/frame/velocity/clock choices are legitimate query data. N is a CHOSEN
finite nuisance class, not an established GOCE noise law and not ordinary
metric Cauchy data. P and error bounds need actual processing/metrology support.
They cannot be estimated against confirmation outcomes and called independent.
Unknown gains multiplying unknown signal, nonlinear/adaptive processing, and
unbounded physical corrections are outside (1) unless separately reduced to it
with a valid remainder bound. No supplied choice is adopted by this definition.
The lawful Weyl/history freedom is unrestricted by this scalar test; that
freedom cannot change the trace while retaining the admitted arena.

## 2. Absolute identifiability and genuine rejection directions

TM2-IDENTIFIABILITY. For the exact linear class (1), kappa is identifiable
from y despite arbitrary beta IF AND ONLY IF

    p not in col(Q).                                  (2)

Proof: two representations give p Delta kappa+Q Delta beta=0. A nonzero
Delta kappa exists exactly when p belongs to col(Q). If p=0, it belongs
to that column space, including when Q has no columns. Existence of a
solution y is understood; (2) concerns uniqueness of kappa, not existence.
The remaining beta need not be unique. When (2) holds there exists a row w
with wQ=0 and wp=1, so wy=kappa. Noise then produces w epsilon.

Choose C whose independent rows span the left nullspace of M. Then

    Cy=0 iff y belongs to col(M),
    dim(rows C)=m-rank(M),
    rank(CP)=rank(P)-rank(M).                          (3)

The first equivalence is elementary finite-dimensional annihilator duality:
ker(C)=col(M). For the last equality restrict C to im(P); its kernel there
is col(M), since col(M) is contained in im(P). Rank-nullity proves it.
Thus m-rank(M) is NOT automatically the number of independent geometric
constraints. The m-rank(P) redundancies of P may compare copies of the same
input and cannot detect ANY latent departure. Genuine scalar-signal rejection
directions have dimension rank(P)-rank(M).

A specified departure delta is distinguishable from the constant+nuisance
class in noiseless recorded space exactly when

    CP delta != 0, equivalently P delta not in col(M). (4)

This is the exact blind space for this chosen finite design, not a whole-theory
no-go or a statement about every physical departure. All rows C are fixed by
the declared designs, not optimized after observing a residual. Formula (3)
can yield useful contrasts even when (2) fails: scalar calibration and testing
are logically different. Conversely, identifying kappa does not guarantee
there is an extra constraint beyond the information used to identify it.

## 3. Training A and predicting B without selecting every parameter

Partition recorded rows into A and B before outcomes. Write M_A,M_B.
For a consistent noiseless y_A, ALL theta solving M_A theta=y_A give the
SAME prediction for y_B IF AND ONLY IF

    ker(M_A) subset ker(M_B).                         (5)

This follows by taking differences of all training solutions. Equivalently,
there is a matrix K with M_B=K M_A: every row of M_B lies in row(M_A).
Then y_B=K y_A for the joint model. No unique theta or universe is required.
For an inconsistent noisy y_A, (5) remains a design identity and the residual
below is valid; it does not assert an exact training solution exists.

    r=y_B-K y_A = C_AB y,     C_AB=[-K I]             (6)

(with columns returned to the original row order). A useful signal test
additionally needs C_AB P delta !=0 for a specified departure, not just a
nonzero matrix C_AB. If (5) fails, a kernel vector v with M_B v!=0 is an
explicit ambiguity witness; inventing a preferred training solution is not
an identified prediction. A fixed K is part of the preregistered estimator;
different K may weight errors differently even when their noiseless model
predictions agree. Error/conditioning justification must be supplied.

Row disjointness is not statistical or provenance independence. If a row
called A was already constructed using B raw inputs, it is not an unexposed
training set. A fixed algebraic contrast can still be tested mathematically,
but an empirical held-out label needs the upstream raw-support and exposure
audit, target-independent calibration and honest joint covariance. A target
condition enforced or fitted in B is not an unused B test.

## 4. A concrete prospective design and negative alternatives

Choose four registered query times t=(0,1,2,3) in declared time units and P=I.
As an ILLUSTRATIVE nuisance class let N=[1,t], i.e. an unknown constant
offset plus affine drift over this window. This class requires external
support before device use; it is not asserted true or small for GOCE.
The joint model is y_i=kappa+b+d t_i. Absolute kappa is unidentifiable,
but the two combinations kappa+b and d suffice to predict later readings.

Use A=(0,1), B=(2,3). A fixed prediction is

    K=[[-1,2],[-2,3]],
    r1=y2+y0-2y1,  r2=y3+2y0-3y1.                   (7)

This is symbolic training of a JOINT constant-trace/affine-nuisance model,
NOT independent calibration of a physical offset or Lambda. A target-free
device calibration is still required. rank(M)=2, rank(CP)=2. A comparison
delta=a t² gives (r1,r2)=(2a,6a); any affine delta is invisible because it
can be reabsorbed into the stated nuisance class. A non-affine departure
can also be invisible on these four samples, so this is not continuous-time
completeness. Using only A=(0) leaves d free and cannot predict B.

Other exact alternatives:

- P=I, only constant offset: absolute kappa is aliased with it, while n-1
  scalar constancy contrasts remain. If no nuisance column is supplied and
  offsets/errors are independently controlled, kappa can also be calibrated.
- Arbitrary independent nuisance offsets N=I_n: rank(M)=rank(P), so there
  is no genuine scalar rejection direction, for ANY fixed P.
- Centering P=I-11^t/n removes absolute kappa but retains n-1 constant-trace
  departure directions when N has only a constant column. Lost DC does not
  imply loss of every constancy test.
- Keeping only the mean P=11^t/n retains one unknown scalar but no unused
  scalar rejection direction. Pointwise scalar erasure P=0 retains neither.
- P=[[1,0],[1,0]], N absent: y_B-y_A is a nonzero row contrast but CP=0.
  It compares two copies of one latent event. A passing difference is only
  a processing consistency check, not a test across two physical events.

These are exact finite design controls, not simulated instrument sensitivity
or counterexamples to the admitted metric equations.

## 5. Error bounds and actual adverse evidence

If |epsilon_i|<=u_i has independent metrological justification, any fixed
row c gives |c epsilon|<=sum_i |c_i|u_i. Hence under the joint model

    |r_j| <= sum_i |(C_AB)_ji| u_i.                   (8)

For (7) and common u these limits are4u and6u. This uses no independence or
Gaussian assumption. If a valid full covariance Sigma is instead supplied,
Cov(C_AB epsilon)=C_AB Sigma C_AB^t, including A/B correlations. That
identity does not itself justify a probability model or significance level.

An observed residual exceeding the frozen justified bound contradicts the
joint domain/interface/constant-trace/nuisance/error model, not specifically
UDT in isolation. Given a fixed departure and the same error bounds under
the alternative, |c P delta|>2 sum|c_i|u_i guarantees crossing the null bound
even with worst-case signed errors. Merely nonzero response (4) proves
noiseless distinguishability, not attainable detection. Unbounded errors
cannot be hidden by a small tolerance. No numerical u or actual rejection
is asserted here.

## 6. Landing and prospective return point

This establishes an exact conditional finite-design criterion and a real
distinction: useful unused constraints can survive without identifying an
absolute scalar or every nuisance/initial parameter. It also identifies
precise designs with no such test. It does NOT certify a modern GOCE product,
select the affine-drift model, provide a finite-device error bound, measure
Lambda/scale, reconstruct a metric, or establish an empirical UDT signature.
The trace relation is shared with vacuum GR, not a unique UDT prediction.

A prospective real protocol must first freeze and justify the device/domain
map, actual processing/version/raw support, calibration observations, allowed
nuisance class, error/covariance model, A/B partition and nonzero target
response. Calibration A may then determine an identifiable scalar combination;
hold B untouched and evaluate its fixed contrast without retuning. Report
absolute Lambda only if (2), unit/domain assumptions and independent offset
information support it. Otherwise label the identified combination honestly.

Directional/off-diagonal tides remain useful complementary geometric records;
G358 already says one observer's E misses five mixed components, and scalar
data miss its directional trace-free part too. Neither this finite scalar
design nor calibration supplies the remaining functional geometry. A finite
boosted-timelike reconstruction remains a separate unproved option, not
necessary to this scalar test or claimed accomplished here. Any light/instrument
transfer remains supplied. Emergence and geometric testing remain parallel.

Author analytic exploration preceded candidate freezing and exact checks;
no TM2 reviewer finding or observation was read to choose the design. Shared
upstream TM1 exposure caveats persist. Review and checks must still adjudicate
the proof, novelty of signal constraints, examples and scope before use.
