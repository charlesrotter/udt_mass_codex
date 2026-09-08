# RD1 — response/support contract and its present limitation

Exploratory conditional mathematical candidate, frozen 2026-09-08 UTC before
adversarial target review. No acceptance, physical adoption or new observation.
The final review, not this heading, owns subsequent review status. The approved
work order and exact upstream pins are in ../CAMPAIGN_LOG.md and
../SOURCE_LEDGER.md. All statements below inherit their premise and domain
restrictions. No strain samples were opened in this step.

## 1. Question, supplied choices and maximum conclusion

Can the fixed three-channel/two-function design support an informative contrast
once its response and finite-support approximations are explicit? Quantifiers
matter: an identity for every pair in a finite cyclic vector space is not an
identity for every smooth continuum waveform measured over a finite interval.

Admitted geometry supplies the conditional vacuum arena and arbitrary wave
profiles of CO1, under W4 WORKING/POSIT and later owner-provisional G312/G313.
Weak local plane tensor waves, apparatus coupling, sky/time convention and
instrument/processing model are SUPPLIED measurement/regime assumptions.
They are not UDT derivations, selected physical content or generic UDT waves.
Clock/ruler c_E is observed calibration; no absolute geometry or waveform
scale is selected. The two waveforms and their allowed size/support are
ordinary initial/query data. A quantitative restriction on those data can be
a declared conditional hypothesis without becoming a new physical law; it
must not be hidden, asserted for an unknown source or tuned after confirmation.

Physical choices: the named weak-wave measurement class and nominal apparatus
map are supplied, not pinned-by-THEORY. Waveform functions remain
free-and-explored. The finite cyclic representation, 30--500Hz query, training
split and norm are supplied analysis controls, not physical boundary conditions.
No choice pinned-by-HABIT is promoted into evidence. Mathematical inequalities
are methods. Omitted physical mechanisms, metrology, nonlinear wave regimes,
generic polarization, source identification and empirical coverage stay open.

The result below is (i) a conditional leakage contract that can eliminate an
unknown waveform amplitude when stable training is justified; (ii) a precise
finite-support reason that static rank does not provide that justification;
(iii) a sharp size-budget alternative that does not demand a unique waveform;
and (iv) a source-based finding that the present physical error budget has
not been instantiated at the old 1e-21 strain sqrt(second) query. These are
one response/support eligibility question, not three new research directions.

## 2. Conditional training-to-contrast bound

Let H, Y_T and Y_V be real or complex Hilbert spaces with declared norms.
H is the pair of waveform functions on the FULL domain needed by the response,
not automatically just the retained 90 seconds or retained Fourier bins.
Let bounded nominal operators A_T:H->Y_T, A_V:H->Y_V admit a bounded left
inverse B:Y_T->H, B A_T=I_H. Set S=A_V B. All maps and budgets are frozen
independently of the reserved confirmation outcome. Under the measurement null,

    y_T = A_T h + d_T(h) + n_T,
    y_V = A_V h + d_V(h) + n_V.

The disturbances d may depend nonlinearly on h or fixed nuisance inputs; no
automatic fixed-linearity claim is made for data-dependent noise subtraction.
The following bounds must hold uniformly on the declared waveform/nuisance
class, for the actual composed response and analysis operations:

    ||B d_T(h)|| <= kappa ||h||,        0 <= kappa < 1,
    ||d_V(h)-S d_T(h)|| <= rho ||h||,   rho >= 0,
    ||B n_T|| <= eta_B,
    ||n_V-S n_T|| <= eta_r.

Deterministic bounds are one interpretation. If they hold on a specified joint
probabilistic event, the conclusion holds on that same event; no confidence
level, Gaussianity, independence or simultaneous coverage is manufactured.
Nonzero additive response budgets can be included explicitly in eta_B/eta_r
with their dependence disclosed, not silently called random noise.

Applying B to training gives By_T=h+B d_T(h)+B n_T. Triangle inequality yields

    H_train := (||B y_T||+eta_B)/(1-kappa) >= ||h||.

Since A_V-S A_T=0, the contrast r=y_V-S y_T obeys

    ||r|| <= rho H_train + eta_r.                         (RD1.1)

This is a direct proof for all inputs satisfying the hypotheses. For fixed
linear errors Delta_T, Delta_V with ||Delta_T||<=delta_T and
||Delta_V||<=delta_V, sufficient budgets are

    kappa=||B|| delta_T,  rho=delta_V+||S||delta_T,
    eta_B=||B|| eta_T,   eta_r=eta_V+||S||eta_T,

when ||n_T||<=eta_T and ||n_V||<=eta_V. Direct composite bounds can be much
sharper: errors satisfying d_V=S d_T contribute zero contrast leakage.
For static common scalar filtering this cancellation may hold; it is not
automatic after noncommuting varying response, unequal delays or windows.

In the static point-response L2 model, CO2's H/L matrix is invertible and B is
its pointwise inverse: ||B||=6.6244861376, S=(-0.4723561064,-0.9125510037),
||S||=1.0275551691. Thus the simple sufficient training error threshold is
delta_T < 1/6.6244861376, approximately 0.150955. These are dimensionless
operator values in that model, not a bound on the actual pipeline. Physical
unweighted waveform norms have units strain sqrt(second); whitening changes
the norm and requires transporting every operator/error budget consistently.

Nonvacuity: in independent channel coordinates with finite fixed budgets,
y_T=0 leaves a finite right side in (RD1.1), whereas arbitrarily large y_V
violates it. Thus this training bound is not algebraically true for all data.
It does NOT establish an achievable target, a physical alternative, population
power or independent noise. In contrast, a full-data bound epsilon||y||/
(gamma-epsilon) with epsilon/(gamma-epsilon)>=1 and unit-norm contrast is
automatically satisfied, so merely writing an inequality is insufficient.

B and kappa<1 are sufficient, not necessary for useful prediction. For example
A_T(h1,h2)=h1, A_V(h1,h2)=2h1 predicts y_V=2y_T exactly with no left inverse
for the whole pair. More generally it may suffice to control the quotient or
component relevant to leakage. Failure of this sufficient test is not absence
of another contrast, lack of a physical source or failure of UDT.

## 3. Finite support: why two functions are not two sampled parameters

Consider the explicit diagnostic class H_Omega of real L2 functions on R with
Fourier support Omega=[-b,-a] union [a,b], 0<a<b<infinity, using exp(2pi i f t).
Point evaluations are bounded on this Hilbert space. Its real kernel is

    K(s)=integral_Omega exp(2pi i f s) df
        =2 integral_a^b cos(2pi f s) df,  K(0)=2(b-a).

For ANY finite distinct times t_1,...,t_m, G_ij=K(t_i-t_j) is positive definite.
Indeed c*Gc is the integral over Omega of the squared modulus of a finite
exponential sum. Zero integral makes that continuous sum zero on an interval.
Analytic continuation makes it identically zero; derivatives of orders
0,...,m-1 give an invertible Vandermonde system for distinct times. Thus c=0.
For every real target vector v, h=sum_j (G^{-1}v)_j K(.-t_j) interpolates v,
and ||h||^2=v^T G^{-1}v. Compact Fourier support also gives smoothness and
bounded derivatives for this finite construction.

Consequently, in the SIMPLIFIED static point-detector model
d_{i,k}=F_{i,+}h_+(k/fs-tau_i)+F_{i,x}h_x(k/fs-tau_i), if all sampled
geocentric times are distinct and F_{i,+} are nonzero, set h_x=0 and interpolate
h_+ to d_{i,k}/F_{i,+}. Every finite real channel vector is in this idealized
map's range when no uniform waveform-size budget is imposed. CO2's supplied
decimal delay differences are not integer multiples of 1/4096 seconds; its
plus coefficients are nonzero. This establishes the condition for that nominal
point-sampling example without reading its strain or constructing a fit.

This is NOT a surjectivity claim for finite-arm, rotating, filtered, calibrated
or cleaned flight products. Their actual finite measurement functionals and
Gram/range would need analysis. It is also NOT a claim that an arbitrary fixed
record fits within the weak-wave class: interpolation norms can be enormous.
Scaling any one constructed waveform sufficiently small preserves its nonzero
contrast direction while making it weak; hence no universal exact linear
annihilator appears merely by imposing a positive small-norm ball in this
diagnostic model. Quantitative approximate constraints can nevertheless be
strong under a fixed, finite norm budget.

Nor does this refute the FW1 finite cyclic identity. FW1 chooses two vectors
in a common finite Fourier representation; the exact physical continuum has
additional degrees of freedom outside that representation/support. Finite
samples from an unrestricted infinite-dimensional H cannot have a left inverse
on all H: the finite measurement map has a nontrivial kernel. Band limitation
alone does not change that dimension fact. Infinite noiseless sampling or a
justified finite-dimensional approximation are different hypotheses.

Windowing multiplies in time and convolves in frequency. Therefore zero input
in a retained band does not imply zero windowed output there. A retained-band
or core-only waveform bound cannot simply be used as a full-response bound.
Padding, interpolation and truncation errors need their actual support/norm or
justified error control, not physical periodicity inferred from a DFT.

## 4. A sharp bounded-data alternative, without unique waveform selection

For the same real Hilbert model, take finitely many independent training
functionals T:H->R^m with Gram G=TT*>0, and one holdout functional
ell(h)=<k,h>. For exact noiseless training y, the minimum-norm interpolant is
h0=T*G^{-1}y. Every solution is h=h0+z, z in ker T, with h0 orthogonal to z.
Let p=k-T*G^{-1}T k be the projection of k onto ker T. If the externally
specified class has ||h||<=H_max and H_max>=||h0||, then

    |ell(h)-ell(h0)| <= ||p|| sqrt(H_max^2-||h0||^2).       (RD1.2)

Proof: ||z||^2<=H_max^2-||h0||^2 and ell(z)=<p,z>; Cauchy--Schwarz.
Equality is attained by z in the positive or negative p direction if p!=0.
If p=0, training predicts ell exactly despite unresolved waveform freedom.
If H_max<||h0||, the declared bounded class is incompatible with training.
For a distinct point evaluation in the kernel example, the enlarged Gram is
positive definite and ||p||>0. As H_max grows without bound, the interval
becomes unbounded. These are necessary-and-sufficient range statements for
this exact noiseless Hilbert problem ONLY. No necessity is asserted for UDT,
actual products, noisy data or a different class/measurement.

This identifies a potentially informative ordinary-data bridge: a justified
size/support/approximation bound, not unique specification of every waveform
and not necessarily a new physical premise. Actual inference would need a
prospectively fixed admissible budget or independent bound and expansion for
noise/response uncertainty. No value of H_max, physical prior or event fit is
chosen here, and (RD1.2) does not itself provide such a bound.

## 5. Documented arm response: an analytic bound, not the whole certificate

The pinned official DetResponse.c and its actual LALSimulation.c caller define,
with x=pi f L/c_E, mu the propagation-direction dot arm and sinc(z)=sin(z)/z,

    T(x,mu)=1/2 [e^{ix(1-mu)}sinc(x(1+mu))
                 +e^{-ix(1+mu)}sinc(x(1-mu))].

The caller uses beta=f L/c_E; the callee multiplies beta by pi and GSL's
sinc is normalized sin(pi beta)/(pi beta), as confirmed by the installed GSL
header. A nearby source comment uses a different beta expression. We follow
the actual definitions together, report a convention discrepancy neutrally,
and infer no flight-data bug or historical processor configuration from master.

For |mu|<=1 this T is an average of e^{ix alpha}: equally mix the uniform
parameter s in [-1,1] in alpha=(1-mu)+(1+mu)s and
alpha=-(1+mu)+(1-mu)s. Thus |alpha|<=2, E alpha=-mu,
E alpha^2=4(1+mu^2)/3 and |T|<=1. Using |e^{iz}-1|<=|z| and
|e^{iz}-1-iz|<=z^2/2 gives the global analytic bound

    |T-1| <= min(2, 2|x|, |x mu|+(2/3)x^2(1+mu^2)).       (RD1.3)

The integral proof establishes the continuum bound, not a frequency grid. For
ideal unit arms and the usual normalized plus/cross tensors, the two-component
response-weight vector of a single signed half-arm has norm <=1/2. Therefore
the detector row's finite-arm/static difference is bounded by the maximum of
the two arm bounds. In the stationary whole-line band-limited model, Fourier
Plancherel transfers a uniform frequency bound to an L2 operator bound. It
does not transfer without checking a time-varying/filter/window composition.

As a supplied sensitivity illustration ONLY, L=4000m and 3000m at |f|<=500Hz
give uniform row budgets e_L=x_L+(4/3)x_L^2 and e_V=x_V+(4/3)x_V^2, about
0.02155 and 0.01605. In that ideal static band model alone,
delta_T<=sqrt(2)e_L, kappa<=||B||sqrt(2)e_L and
rho<=e_V+||S||sqrt(2)e_L. These are finite and potentially useful, unlike
leaving this known transfer unmodeled. They are not actual metrology, not a
joint budget for calibration/cleaning/rotation/astrometry/support, and not a
sensitivity claim at 1e-21. Mean-arm approximation and published-decimal unit
vectors require their own declared controls if used beyond this illustration.

## 6. Evidence sufficiency and the RD2 gate

The calibration release gives pointwise median and +/-1sigma curves with a
true/model convention. It does not give the simultaneous deterministic bounds
used above; its inverse describes uncorrected released/true response. Joint
stochastic assumptions, correlations and bias treatment must be explicit for
a probabilistic alternative. Neither a full covariance nor every raw sample
is demanded if justified aggregate error control suffices. The subtraction
paper's documented safety/calibration checks support intended instrument use,
but finite signals/lines do not certify arbitrary-waveform uniform error; its
data-dependent transfer estimates and transient/narrow-line caveats matter.
Model-assisted processing neither automatically destroys nor certifies a test.

At this step no supported complete response/support error coefficient, relevant
waveform-size bound, or joint noise allowance has been established at the old
target. The arm-only bound is one controlled component, not a license to set
all remaining terms to zero. Static rank and the 33 exposed records cannot
supply the missing continuum/support hypotheses by themselves. In particular,
an after-cleaning software injection cannot certify earlier signal retention.

Proposed disposition for review: RD1 has useful conditional mathematics and a
precise present limitation, but the approved RD2 practical gate is NOT CLEARED.
Stop this particular unrestricted-waveform finite-window procedure before a
robust-statistic redesign or new data. This is a scoped evidence/design stop,
not a proof no useful GW test exists, not a demand for a new physical law, and
not a project-wide blocker. A future decision may authorize a declared bounded
waveform/support class with error control, a sharper prediction-only quotient,
or a different observational route. No such class or campaign is selected here.

## 7. Discovery, checks and review limitations

This candidate was explored before freezing; no confirmation outcome was read.
Prior FW2 failure/outlier, CO1/CO2 arguments and old release assessments were
known. A fresh reviewer read controlling sources before target exposure and
sent operator-domain cautions, a training-bound refinement/nonvacuity warning,
and an independent integral reconstruction of the arm bound before this freeze.
Those contributions influenced sections2/5 and are disclosed, not presented as
no-communication independent discoveries. Sections3/4 were developed by the
author before target review. Fresh context, independent implementation, shared
sources and mathematical collaboration are separate independence axes.

checks.py provides finite exact/floating anchors and deliberately defective
alternatives, not a continuum proof or actual instrument certification. General
arguments are above. Resource/command/version/stdout/stderr records accompany
each run. No source theorem suite, new strain, actual operator/uncertainty
estimation, empirical noise distribution, astrometry or 2017 calibration is
recomputed here. The full349 startup premise audit passed separately. Scientific
acceptance and promotion remain unauthorized; no manuscript or canon change.
