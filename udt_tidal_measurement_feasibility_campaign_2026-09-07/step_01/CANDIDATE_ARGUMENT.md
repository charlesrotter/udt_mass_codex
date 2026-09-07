# TM1 — conditional instrument interface, not released-data certification

Unpromoted candidate. Question/quantifiers/resources: PLAN.md and WORK_ORDER.md.
Source IDs below resolve in SOURCE_LEDGER.tsv. No flight data are inputs.

## 1. What geometry supplies

Use exactly U4's Q_abcd=g(R(e_a,e_b)e_c,e_d), signature(-+++),
R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y], and unit future U=e0.
E_ij=Q_i00j is symmetric. For affine proper length s, Jacobi separation obeys
J''=-E J. If s=c_E tau with measured clock/ruler conversion c_E, define

    T=c_E^2 E,       d²J/dtau²=-T J.                   (1)

This is a negative-relative-acceleration matrix, in s^-2, NOT a voltage.
U3 and U4 give tr(T)=-c_E² Lambda for every event and every unit timelike U
on a connected admitted Ric=Lambda g development. Lambda is not selected;
its connected constancy is an equation consequence, not a fitted profile.
The proposed Earth-orbit application is not thereby known to occupy this
bounded vacuum arena. W4 supplies ideal coupling, not proof-mass suspension,
electromagnetism, star-camera light transfer, calibration, or error bounds.

## 2. Explicit conditional metrology interface

Supply a small instrument frame rotating at omega relative to the local
nonrotating frame. Define Omega x=omega cross x. Let A_d have columns
one-half of the calibrated pair-acceleration differences, and let
L=diag(L1,L2,L3), positive signed-axis baselines fixed by the pair order.
Let S=2 A_d L^-1. The ideal engineering model in E2 eqs6,15,19,32 is
S=-V+Omega²+dotOmega, where V is the conventional acceleration gradient.
To use this for the metric query, explicitly SUPPLY the identification
V=-T in the local, infinitesimal, comoving slow-relative-motion limit.
It is not a derivation of the finite GOCE instrument from UDT.
Equivalently, a held pair has inertial relative acceleration
(dotOmega+Omega²)xi; subtracting freefall acceleration -Txi gives its
specific holding-force difference (T+dotOmega+Omega²)xi. Thus under this
stated sign convention and idealization,

    S=T+Omega²+dotOmega,
    T=sym(S)-Omega²,
    dotOmega=skew(S),
    tr(T)=tr(S)+2|omega|².                             (2)

The final identity follows from Omega²=omega omega^t-|omega|² I and
tr(dotOmega)=0. No trace condition was used to obtain it. Full matrices,
not just their trace, must match. Reversing a pair changes its signed
baseline and difference together; changing just one is a sign defect.
Using half-differences with full baselines without the factor2 is a defect.

In an actual interface write corrected S=T+Omega²+dotOmega+D, with D
including residual calibration, common-mode leakage, proof-mass self-gravity,
finite-baseline/finite-body, frame/clock, nongravitational and relativistic
model errors as applicable. Equation(2) recovers T only if these are
independently removed or bounded in the exact query regime. Treating D as
arbitrary and then declaring it small would hide an extra assumption.
If the angular-rate estimate differs by delta omega, the trace error is
tr(D)+4 omega·delta omega+2|delta omega|². No numeric bound is claimed.
The weak-field/slow-motion bridge and residual treatment are conventional
supplied measurement assumptions, not additional UDT field equations.

## 3. What the documentation establishes — and does not

E1 is prelaunch and contains inconsistent signs: its eq4 gives -V, whereas
its displayed component matrix/eq5 gives +V. The image was inspected;
this is not resolved by silently choosing the desired sign. The independent
holding-force derivation above and E2 eqs6,19,32 consistently give (2).
Actual channel orientation must still be version-verified.

E2's ideal model assumes calibrated gains/alignment and neglects self-gravity
and magnetic effects (§3.1); it treats imperfections through calibration
matrices (§3.2). Its redundancy construction uses a zero-trace condition
(§5 eq74/78); the §5.4 proposed adjustment uses that condition. In contrast,
its described baseline and revised calibration use band-specific negligible
gradient assumptions (§§5.3,6.2). These are distinct algorithms, not proof
that every Level1b gradient has been projected to zero trace. Its angular-rate
high-pass operation removes an integration constant, not automatically the
gravity-gradient DC channel. The 2019 method summary E3 identifies gravity-model
inputs in the 2018 calibration. That is a dependency to audit, not proof that
every target deviation is removed. No actual modern release has been certified
here. Missing 2018 algorithm access leaves that dependent eligibility OPEN.

## 4. What survives without choosing a data product

The geometric scalar is kappa=tr(T)=-c_E² Lambda. Suppose only the scalar
channel is z_a=kappa+b+e_a with an unknown constant bias b. The transformation
(kappa,b)->(kappa+d,b-d) leaves all noiseless readings unchanged. Even many
events cannot calibrate absolute Lambda from those readings alone. That is
a nuisance degeneracy, not failure of the Einstein arena. Independent offset
information could remove it; uniqueness of every initial field is unnecessary.

A fixed difference z_a-z_b removes constant kappa and constant b, leaving
an available constancy test IF time-dependent errors and processing response
are independently bounded and the proposed deviation is retained. Likewise,
a fixed linear operator H with H1=0 is blind to constant kappa, while a pointwise
trace-free projection removes the scalar at every event. Neither is a claim
that these operators describe every released GOCE product. A trace fitted
or enforced in calibration is not an unused confirmation of that same trace.

## 5. Landing and next admissible question

TM1-INTERFACE is exact conditional algebra for the explicitly supplied ideal
model. TM1-ELIGIBILITY remains unresolved for a particular released GOCE
channel; old documents and current abstracts do not close version-specific
transfer, DC/bias, nuisance and calibration-dependence requirements.
No physical adoption, empirical success/failure, sensitivity estimate, or
generic impossibility follows. c_E converts units; a nonzero measured Lambda
could characterize a curvature scale, but neither selects the full geometry.

The useful next mathematical question is which scalar contrast retains a
genuinely independent rejection direction after specified calibration and
nuisance elimination. This can be answered conditionally without fitting
observations or requiring physical selection of all initial/query data.
If no rejection direction survives, stop that specified protocol; do not
turn it into a verdict against UDT, every instrument, or geometric testing.

## 6. Verification/discovery disclosure

Argument developed before author checks and before reviewer results. Source
reading was not perfectly outcome blind: searches/abstracts and overly broad
PDF extraction incidentally exposed qualitative historical performance prose
and graph labels. No numerical flight residual, observational payload, fit,
outcome-selected model, or empirical success claim is used. Exact details
are in SOURCE_ACCESS_AND_EXPOSURE.md. This is a feasibility audit, not a
preregistered empirical experiment. The general algebra above is the argument;
exact finite checks are error-detection evidence, not a device validation.
