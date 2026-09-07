# TM2 independent source-first argument

Source and exposure scope: STAGE_A_CHECK_PLAN.md. This text was constructed
before seeing TM2's candidate argument, code or outputs. Its general claims are
elementary real linear algebra; finite exact checks support error detection.

## 1. Quotients separate the questions

Let x be n scalar values; under the connected-constant hypothesis x=kappa 1.
Supply fixed P:R^n->R^m, N:R^q->R^m and unconstrained real nuisance beta.
For now e=0. Define a=P1, D=[a N], theta=(kappa,beta), so y=D theta.
P,N are supplied independently of confirmation outcomes; their adequacy is
not a consequence of G313 or G358. Their physical origin remains conditional.

Absolute kappa is identifiable precisely when a is NOT in im N. Indeed,
two parameters have equal y iff a delta-kappa+N delta-beta=0. A nonzero
delta-kappa exists exactly when a belongs to im N. This includes a=0.
Equivalently there exists l with l^T N=0 and l^T a=1; then kappa=l^T y.
This is exact noiseless identifiability, not accuracy or calibrated units.
An unknown gain, nonlinear/adaptive P or changing N is outside the theorem.

Let W have rows a basis of ker D^T. Then Wy=0 iff y is in im D: one
inclusion is annihilation, and the other follows by finite-dimensional
orthogonal complement and rank-nullity. Thus there are m-rank D independent
recorded linear constraints. This does not require identifying kappa.

A crucial distinction: nonzero W need not test scalar constancy. Under
x=kappa 1+delta the residual is WP delta. Exactly the latent departures

    B = {delta : P delta is in im D} = ker(WP)

are invisible to the complete family of recorded constraints. There is a
latent-scalar rejection direction iff rank(WP)>0, equivalently im P is not
contained in im D, equivalently rank([D P])>rank D. Its independent dimension
is rank([D P])-rank D. Constants and ker P are always in B; nuisance-aligned
variations may also be in B. The residual test concerns only this supplied
model and does not classify metric developments or all physical departures.

For example, if P=(1/n)11^T and N has no columns, kappa is identifiable,
rank D=1 and m-1 nonzero record constraints exist. Yet im P=im D, so every
latent variation is invisible: equal recorded rows were imposed by processing.
These record constraints can diagnose interface/noise failure but cannot be
advertised as retained tests of latent scalar constancy. A fixed projection
into the target-plus-nuisance subspace has the same limitation. An adaptive
target-dependent projection is additionally outside the fixed-P hypotheses.

## 2. Training and held-out records

Partition the registered rows into A and B, writing D_A,D_B and y_A,y_B.
For noiseless y_A in im D_A, choose any theta0 with D_A theta0=y_A.
The allowed B records are exactly

    D_B theta0 + D_B ker D_A.

Thus ALL B predictions are unique iff ker D_A is contained in ker D_B,
equivalently row D_B is contained in row D_A, equivalently
rank([D_A;D_B])=rank D_A. This follows directly by differences of solutions.
When true there exists K with D_B=K D_A, yielding y_B=K y_A. Uniqueness
of theta, or of kappa alone, is unnecessary. K can be nonunique but all such
choices agree on exact compatible y_A; with errors their bounds may differ.

If full prediction fails, a B functional c_B^T y_B can still be predicted
iff c_B^T D_B is in row D_A. Choose c_A so that
c_A^T D_A+c_B^T D_B=0; this gives the fixed residual c_A^T y_A+c_B^T y_B.
Require c_B nonzero for any held-out claim, and require sensitivity to the
specified retained alternative; a constraint involving only A is no held-out
test. Free coefficients that act only on B can destroy prediction completely.

Concrete chosen design: P=I4, t=(0,2,5,7), N=[1,t], so
D=[1,1,t]. kappa and the constant offset alias; rank D=2. Train at 0,2 and
confirm at 5,7. Despite the alias, B is predicted by

    K=[[-3/2,5/2],[-5/2,7/2]],
    r_5=y_5+(3/2)y_0-(5/2)y_2,
    r_7=y_7+(5/2)y_0-(7/2)y_2.

All affine latent departures are blind because drift is allowed. The chosen
quadratic departure t^2 yields (15,35), so this design retains a rejection
direction. This is a finite algebraic fixture, not a flight/sensitivity claim.
With N=t only, kappa becomes identifiable. With N=I4, im D=R4 and every
residual vanishes. With P=I4-11^T/4, a=0 and absolute kappa is lost, while
nonconstant variations can still survive; the imposed sum-zero record identity
must again be separated from scalar-sensitive contrasts.

Counter-design: D_A=[[1,0],[1,0]], D_B=[[1,1]]. theta=(0,0) and (0,1)
both give y_A=(0,0), but give B=0 and B=1. Calling one chosen fit's B value
a uniquely trained prediction would be false. The exact permitted object is
the affine prediction set, or any surviving scalar functional above.

## 3. Errors, correlation, and data exposure

Supply deterministic pre-processing errors epsilon and recorded errors eta,
so e=P epsilon+eta. For separately justified boxes |epsilon_i|<=rho_i,
|eta_j|<=sigma_j and fixed contrast w,

    |w^T e| <= sum_i |(P^T w)_i|rho_i + sum_j |w_j|sigma_j.

No stochastic independence is needed. The bound is sharp for the declared
product boxes; if the allowed errors have extra restrictions their support
function gives the exact bound instead. Bounds themselves are physical inputs
not established here. Changing gain/registration/P/N needs a supported remainder
bound or a larger explicitly declared model, not an unreported refit.

For y_B-K y_A the error is e_B-K e_A. Dropping the training error is wrong.
For covariance Sigma, variance of fixed w is w^T Sigma w only after a genuine
second-moment model is supplied; off-diagonal A/B blocks cannot be discarded
from row names alone. For Sigma=[[1,-1],[-1,1]], contrast (-1,1) has variance
4, whereas incorrectly assuming independence gives 2. A covariance is neither
a deterministic bound nor a tail probability without added assumptions.
Several coordinatewise residual bounds are necessary consequences; their
separate satisfaction need not give one jointly compatible error vector.

The raw support of processing matters: if rows P_A use latent/raw B inputs,
training was exposed to B even if only A-labelled processed rows were read.
A/B row separation alone proves no observational independence. Any proposal
must freeze the raw dependency graph, target usage, coefficients, nuisances,
bounds, calibration windows and rejection rule before confirmation exposure.
Fitting or selecting these from B changes the protocol; the algebraic identity
cannot certify pristine held-out testing. Correlation may remain even with
disjoint raw support and must be handled by bounds or an explicit joint model.

## 4. Scientific ceiling

G313's connected scalar and G358's ideal trace identity act only in the admitted
owner-provisional Einstein arena. W4 is WORKING/POSIT and TM1's finite-device
identification remains conditional; released GOCE eligibility stays OPEN.
No claim here identifies a real noise model, clock scale, bias, domain, signal,
detector or physical contradiction. Calibrating kappa would still require the
supplied clock/ruler conversion to infer Lambda, and one scalar cannot recover
lawful Weyl/history freedom or choose the full metric. A violation rejects a
joint, explicitly supplied interface/arena/error model, not UDT alone.

The source-first argument will be sealed with exact checks before direct review.
No human, different-model, formal-assistant, complete source reproof, empirical
calibration, observation test, PDE solve or scientific promotion is performed.
