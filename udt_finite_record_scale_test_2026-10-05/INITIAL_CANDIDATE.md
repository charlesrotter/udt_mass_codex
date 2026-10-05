# FRI1 initial finite-record argument

CONDITIONAL candidate. Algebraic discovery precedes confirmation freeze. Parent
disclosed preliminary bounding/witness leads to both fresh reviewers; their
matching interval/derivative arguments were exposed during discovery. A first
absolute-parameter box was replaced BEFORE confirmation by the dimensionless
shape domain below, avoiding a hidden supplied absolute scale. Neither is a
native postulate or an empirical prior. TSI1/CPR1 source grades stay unchanged.

## 1. Domain and finite records

Use calibrated receiver proper length ell=c_E tau_seconds. H>0 is unknown.
Dimensionless variables are mu=mH, A=aH, y=1/(HR), B=Hb and
w=Omega/H=sqrt(mu/A^3-1). A here is dimensionless source radius, not the
earlier receiver frequency A; call that frequency A_rec. Adopt this conditional
class, free-and-explored rather than selected by UDT:

 mu in[1/200,1/100], A in[1/20,1/10], E in[1,10],
 principal B_*=0, 0<y<=1/50000.                         (D)

All support intervals AND the gaps between them must stay in(D). These shape
and tail hypotheses are scale invariant; H is not bounded in advance. Their
physical admission is not inferred from the tested finite record. In particular
y<=1/50000 is not an observed onset certificate. h=1-3mu/A>=.4,
f(a)=1-2mu/A-A^2>=.59, and 2<=w<9, so the inherited source is regular.
E>=1 escapes. The actual principal incidence branch is used, not frozen b=0.

The timing readout is a finite equal-width translated window mean of
Y(ell)=log Z(ell)-log(nu_e(ell)/nu_ref):

 Ybar(ell_i)=(1/delta) integral_[ell_i-delta/2,ell_i+delta/2] Y(s) ds.

nu_e is composed with the actual emission map. nu_ref is any constant positive
normalization. Impose the CONDITIONAL source bound |dlog nu_e/dell_o|<=q in
RECEIVER proper length, not emitter time. A source-time bound would require the
1/Z conversion. A labeled proper-clock arrival map or stable source sets q=0.
Observed z_i=Ybar(ell_i)+e_i, |e_i|<=epsilon_z. A finite arithmetic mean of
the signed principal angle theta has analogous error epsilon_theta. This is
neither an instantaneous differential measurement nor mean log-angle.
The angular reference is TSI1's declared parallel radial frame. Real instruments,
finite pulse counts and source visibility must separately justify these error
bounds; no such physical detector is derived here.

Measured window-center times are ellhat_i; true ell_i=ellhat_i+xi_i with
|xi_i|<=sigma. Equal widths and translations refer to true calibrated time;
width miscalibration is not silently included. Bounds are deterministic, not
Gaussian likelihoods/confidence intervals. Unknown source normalization cancels.
q, errors and class admission are explicit inputs, not deduced from c_E/G alone.

## 2. A uniform finite timing-rate bound

Write W=sqrt(1+(E^2-1)y^2+2mu y^3),
s(z,B)=sqrt(1+B^2-B^2z^2+2mu B^2z^3), and

 P=int_y^(1/A) B/s dz, Uhat=int_y^(1/A) B^2/[s(1+s)] dz,
 dhat=int_0^y dz/[W(Ez+W)], I=int_y^(1/A) dz/s^3.

Principal incidence is P-w Uhat=w dhat. On 0<=B<=1/10000,
.999<=s<=1.001 throughout the ray: 1/z>=A>3mu ensures
-z^2+2mu z^3<=0; the lower bound follows B/A<=.002. Also
W>=1 and dhat<=y. The derivative of the left side is (1-wB)I,

 I>=I0=(10-1/50000)/1.001^3,
 J0=(1-9/10000)I0>0.

At B=0 the left side is0; at B=1/10000 it exceeds9/50000.
Thus for all y in(D) there is a unique root in this small-B interval,
0<=B<=9y/J0. This proves a uniform actual branch and margin; no global image
uniqueness outside it is claimed. Smoothness follows the nonzero Jacobian.

Set D=Ey+W, alpha=1/D+WB^2/(1+s), j=WD B^2/(1+s), so
alpha=(1+j)/D, A_rec=y alpha,
F=(1-wB)/(sqrt(h)alpha), Z=F/y. Here s is evaluated at the receiver y.
The exact incidence derivative is

 B'=[B/s+w alpha/(W(1-wB))]/I.

Elementary bounds give W<=1.00000002, |W'|<.002,
1<=D<=1.00020002, D'<=10.002, alpha<=1.000000006,
0<B'<1, |s'|<.000101, |j'|<.000101. The derivative bounds
include the actual B' term. Therefore

 |(log F)'| <=9/(1-9/10000)+10.002+.000101 <20.

Since dy/dell=-H y W, TSI1's identity becomes

 K/H := (dlog Z/dell)/H = W[1-y(log F)'],
 |K/H-1| < .00000002+1.00000002*(1/50000)*20
          =.000400020008 < eta=1/2000.                (1)

The associated rational inequalities are checked exactly; the argument, not
finite sampling, owns the continuum bound. Angular derivatives can be bounded
without asserting a universal finite logarithmic angle law: alpha>=1/1.00020002,
|alpha'|<10.003, n_phi=B/alpha and positive n_r>.999 imply
|theta'|<2, so |dtheta/dell|<H/20000 throughout(D).

## 3. A finite, error-controlled H enclosure

(1) and the source bound imply Y' between H(1-eta)-q and H(1+eta)+q.
The derivative of an equal translated window mean is the mean of Y'. Thus the
SAME bounds apply to Ybar': finite width adds no extra bias term here, provided
the whole support hull is admitted. Arbitrary unrelated window shapes would
require different bounds. Only the interval length and errors enter inversion.

For any two centers let T=ellhat_2-ellhat_1>2sigma, d=z_2-z_1, and
Tminus=T-2sigma, Tplus=T+2sigma. Handle signs explicitly:

 rlo=min((d-2epsilon_z)/Tminus,(d-2epsilon_z)/Tplus),
 rhi=max((d+2epsilon_z)/Tminus,(d+2epsilon_z)/Tplus).

Every admitted history giving these records must satisfy

 H in [max(0,(rlo-q)/(1+eta)),(rhi+q)/(1-eta)] intersect (0,infinity). (2)

If the upper bound is nonpositive the class is incompatible with those data;
if the interval is wide it is uninformative. This enclosure is conservative,
not a claim that every enclosed H is attainable or that all other parameters
are identified. It permits the full mu,A,E ranges in(D). c_E converts seconds
to ell; equivalently c_E H is the timed rate. G provides no second constraint
without its still-open physical mass/density interface.

## 4. A substantive ambiguity with a factor-of-two scale change

Choose fixed synthetic units and histories

 model0: m=1,a=10,H=1/200,E=1,R(0)=20000000;
 model1: m=2,a=20,H=1/400,E=1,R(0)=40000000.

They have the SAME dimensionless mu=.005,A=.05 and y(0)=1e-5, and hence
the same initial Z and angle. They are homothetic preparations but are evaluated
on the SAME physical ell schedule, not rescaled timestamps. Source frequency
is constant in both. Future y decreases. For centered windows of width delta=.1,
the slight backward support remains y<1.001e-5: using exp(t)<=1/(1-t),
y(0)/(1-H0*1.00000002*delta/2)<1.001e-5. Bootstrap of this bound prevents an
exit through the assumed margin. This verifies the entire support hull.

On this narrower witness shape, w=sqrt(39)<25/4, I>19.94, B<=1e-5,
B'<.314, |theta'|<1/3, and hence |dtheta/dell|<H/290000.
These are explicit inequalities, not a fitted optical profile.

Use five centers 0,T/4,T/2,3T/4,T, with fixed T_short=8/5=1.6,
epsilon_z=.003, epsilon_theta=5e-8 radians, sigma=.001T, and delta=.1.
Define each reported value as the midpoint of the TWO model center values.
This is an explicit synthetic construction, not undisclosed empirical tuning.
Realized time error is0 in this witness, permitted by the declared bound.

For clock records the center separation is at most
H0(.5+1.5eta)T; adding each model's window-to-center bound gives

 |reported z-Ybar_j| <= H0(.5+1.5eta)T/2
                         +H0(1+eta)delta/2 < .003.

For angle records use the common initial angle and the two derivative bounds:

 |reported theta-thetabar_j| <= (3/4)H0*T/290000
                              +H0*delta/(2*290000) <5e-8.

Thus an exact inequality argument proves compatible finite window records for
both scales, even with stable sources and correctly calibrated clocks. Numeric
solves supply explicit values and original-equation checks; they are not the
proof of compatibility. The length1/H differs by factor2. The witness disproves
universal reliable recovery at these finite uncertainties/coverage; it is not
an exact equality of noiseless curves or a no-go for every finite experiment.

## 5. A longer finite control and limits of the conclusion

Use the same fixed errors, delta=.1, q=.000005 per receiver proper length,
and a separate fixed schedule T_long=200, sigma=.001T. H0 is merely the frozen
reference used to choose numerical controls; schedules/errors are explicit
numbers, not adapted to inferred H. At each center take the model0 central
Y plus offsets .002*(-1,1,0,-1,1); angle reports use central theta. Derivative
bounds guarantee these are possible finite-window records within the stated
measurement errors. Actual source drift is0, while inference allows |drift|<=q.
Repeat the long control for E=10 to retain a nontrivial motion change.

Apply(2) before knowing confirmation outcomes. The test asks whether its finite
interval contains the true supplied H and is materially narrower than a factor2.
Also compare model1 on the same long schedule. No optimization, likelihood,
known source ruler, fitted asymptotic limit or continuous infinitetime record
is supplied. Any narrow interval is conditional on(D), the source/readout
bounds and the clock calibration, not inferred native geometry or real data.

Finite source ticks, resolving power and physical admission of the tail remain
separate gates. Permitting arbitrary source drift or arbitrary angular frame
motion can destroy the bound; neither freedom is silently allowed in this
declared experiment. Restricting them here is a labeled conditional interface,
not a derived law of light or matter. Matched GR gives the same observations.
No physical mass, X_max or extra UDT effect is selected by successful inversion.
