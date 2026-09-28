# Independent analytic review

Reviewer `/root/function_adversarial_review`; independent argument after the
source-first reconstruction and subsequent candidate exposure. This is ordinary
differential geometry conditional on supplied geometry/query data, not physical
adoption or proof that UDT selects a history. Code anchors are supplementary.

## Inverse and its hypotheses

On a flat homogeneous metric with positive smooth a(T), the conformal Killing
field conserves a times null frequency. For comoving observers with a(T_o)=1,
r=1/a(T_e). Null incidence gives chi=integral dT/a. An infinitesimal angular
variation has transverse length a_e chi at emission, hence d_o=a_e chi and
d_e=chi. These statements do not require an Einstein equation. They also do
not establish brightness transfer, which remains a separate declared interface.

For smooth F on an interval containing zero, F(0)=0 and F'>0, set
T_x=-e^-x F'/h0 and a=e^-x. The inverse function theorem gives a unique smooth
x(T) on the image interval. Then a_T/a=-x_T=h0 e^x/F' and
dT/a=-F' dx/h0. Integrating between emission and reception gives exactly
chi=F/h0. H(0)=h0 needs F'(0)=1. The candidate explicitly supplies this
normalization; it is not observed below the sample. Differentiating H gives
q_dec=-1+H_x/H=-F''/F'. The curved increasing-branch formula follows from
F=h0 S_k(chi), S_k'^2=1-kappa F^2, and the positive sign of S_k'. These are
valid restricted inverses, not native selectors or whole-universe uniqueness.

The AP relation follows from D_M=F/h0 and D_H=1/H. It requires the declared
flat homogeneous metric, comoving clocks, ruler/template and optical readout;
its amplitude cancellation does not remove those assumptions. No measured
absolute scale or separated positional depth follows. The documented fixed
observer congruence is a supplied query convention, not derivation of a
physically preferred observer.

For the general Jacobi formula d/dlambda=r d/ds directly gives
J_ll=r^2 J_ss+r r_s J_s, yielding the stated q=d log r/ds and T_null/r^2.
The initial observer normalization r(0)=1 gives J_s(0)=I. Observer boosts
rescale the source-frequency factors in the two directional screens, preserving
d_e=r d_o covariantly. Mathematical reversal stays on the same null segment;
the candidate correctly computes later returns at new events.

## Endpoint and completeness arguments

The independent integrals are S=integral e^-x F'/h0 and
lambda=integral e^-2x F'/h0. Thus no conclusion about one extent follows merely
from r going to infinity. An independent exact example is F=(e^(2x)-1)/2:
with h0=1,T_o=0 the metric has a(T)=1/(1-T), T<=0. Direct null incidence gives
chi=-T+T^2/2=(r^2-1)/2. Both proper past time and null affine extent
integral_0^infinity du/(1+u) diverge; direct metric curvature tends to zero.
This checks the p=2 threshold by a separately explicit metric, not a loop
around the numerical inverse.

For F2, the saved decimal coefficients define an exact rational polynomial
P=1+a x+2b x^2 with one positive simple root. Independent 65-digit evaluation
gives x*=2.19675504721078240947, z*=7.99577522077924,
lookback=0.853152839744288/h0 and affine=0.512933085727963/h0.
Near delta=x*-x, H~h0 C/delta, C=9.81156176404876, and
H_T=-H H_x~-h0^2 C^2/delta^3. The independently derived metric Ricci scalar
6(a_TT/a+(a_T/a)^2) diverges. The literal flat extrapolation is singular;
this does not reject F2 on the fitted interval or every geometry realizing it.

For the positive-curvature turning construction, let F*=F(x*) and
F=F*+F''* (x-x*)^2/2+... with F''*<0. Expanding
F* cos((u-u*)/F*) gives u'(x*)=sqrt(-F* F''*)>0 after changing inverse-sine
branches. The signed analytic square root removes the absolute value. Thus
T_x remains nonzero and H has finite limit 7.11513319598822 h0. This is a
regular local transverse-distance turn, not a conjugate point since F*>0.
The tuned positive curvature is visibly supplied outside the data; no native
or global-completion inference is licensed. The candidate keeps that limit.

For F3, exact rational root counting of the saved decimals finds no root of
P=1+a x+2b x^2+3c x^3 on [0,infinity) and one negative real root. P(0)=1 and
c>0 establish positivity on the entire claimed half-line. The positive cubic
in log F dominates both -x and -2x, so S and lambda diverge. H tends to zero,
and H_T=-H H_x is H squared times a rational/polynomial factor, tending to
zero as well. The quoted scalar and Riemann-square limits follow. With complete
flat spatial slices, translation momenta are conserved on every geodesic.
For null momentum p!=0, affine length is proportional to integral a dT;
for timelike momentum p, proper time is integral dT/sqrt(1+p^2/a^2).
For p=0 the latter equals the infinite comoving past time; for p!=0 its
integrand is asymptotic to a/|p|. Hence all past null and timelike geodesics
are complete in this supplied metric. This is a valid past-only assertion;
the positive cubic point estimate is neither empirically selected as a global
tail nor native UDT physics. No global inextendibility theorem or X_max
identification is claimed or established by this review.

The smooth-extension construction is also valid: the standard flat-ended
step has values in [0,1], and before the turn F2'>0. A convex transition to
A exp(p(x-x1)) therefore stays positive. Equality of all derivatives at the
two transition endpoints follows from flatness of the step. F_ext is exactly
unchanged throughout the data interval and has the stated tail thresholds.
These witnesses depend on smooth, rather than globally real-analytic,
continuation. Smooth supplied metrics are the declared class. For F4 the
literal inverse is only C2 across spline knots, as the candidate now explicitly
qualifies. It cannot be silently inserted into a smooth-metric theorem.

## Scope and omissions

The static control's conserved Killing frequency gives opposite endpoint
lapse ratios for the two future exchanges; its finite affine horizon and
constant curvature do not supply the desired UDT completion. The homogeneous
controls are expanding congruences and remain so after a reciprocal coordinate
change. The candidate does not use them as a native positional explanation.
The local geometric expansion is not measured solar-system correspondence.
There is no proof of native selection or a no-go result against such selection.

Independent code derives the Ricci scalar directly from the metric connection,
checks the separately explicit p=2 metric and exact root counts, and evaluates
F2 turn integrals at high precision. It does not reproduce the author's full
ODE/Jacobi tolerance sweep, all historical source proofs, all geometric metrics,
or a general global extension classification. Those are not claimed repeated.

The first reviewer symbolic run failed because SymPy returned `oo-I*pi` for
an integral on T<=0 using a complex logarithm branch. Rewriting it in the
positive variable u=-T gives the real positive integral and passes. The next
run passed the scientific assertions but failed JSON serialization of SymPy's
integer type; explicit int conversion repaired packaging. Both scripts/logs
are preserved under INITIAL_ and SERIALIZATION_FAILURE_ in review/. No
scientific candidate repair follows from those reviewer implementation faults.
