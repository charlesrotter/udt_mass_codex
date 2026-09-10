# QC1 — exact quiet-residual control of specified readouts

INITIAL CANDIDATE / UNREVIEWED / UNPROMOTED.2026-09-10. No physical adoption.
All statements are conditional geometry in the G260 one-function static
spherical class. GR comparison is a filter, not a governing-law input.

## Scope, data and quantifiers

Fix supplied r0>0, x=r/r0 and K=[l,u],0<l<=1<=u, l<u. Let q(x)=f(r0x)
be C2(K). Its COMPLETE metric is

    g_q=-q c_E²dt²+r0² q^-1 dx²+r0²x²dOmega².

c_E is calibrated; r0, areal-radius/time identification and static observer
frames are supplied, not selected physical scales. We compare with
p(x)=1+A x²+B/x, fixed by two predeclared dimensionless reference data
d0=p(1),d1=p'(1): A=(d0-1+d1)/3, B=(2(d0-1)-d1)/3. Retain both constants.
Primes in this candidate are x derivatives. Assume p,q>=m>0 on K for the
nonlinear clock/acceleration bounds; the linear profile bounds do not need
positivity. This is a compact comparison window, not a material boundary.

Let y=q-p; initial errors delta0=y(1),delta1=y'(1), with |delta_i|<=eta_i.
Exact data matching means eta0=eta1=0. For arbitrary CONTINUOUS residual
c(x)=C_ang[q]=x²q''/2-q+1, assume ||c||_infinity,K<=epsilon. This is the
G260 angular sum, not an added response law or instrument-measured tolerance.
The reference has C_ang[p]=0 by the already accepted G260 identity. No
equation selects c(x), A,B, epsilon or a realized physical profile.

## QC1-PROFILE — exact representation and all-profile bound

Define U=(x²+2/x)/3 and V=(x²-1/x)/3. Then

    y(x)=delta0 U(x)+delta1 V(x)
         +(2/3) integral_1^x [x²/s³-1/x] c(s) ds.             (1)

Proof: U,V solve x²w''/2-w=0 and have data(1,0),(0,1) at1. The integral
has zero data and differentiates twice, for continuous c, to x²y_c''/2-y_c=c.
Uniqueness follows for this regular scalar linear ODE on K (or subtraction
and its two explicit homogeneous solutions). The signed integral is valid
on BOTH sides of the anchor, including one-sided endpoint derivatives.

For x>=1 the undifferentiated kernel and integration orientation are positive.
For x<=1 both reverse sign. Consequently

    |y_c(x)| <= epsilon [U(x)-1].

The x-derivative kernel (2/3)(2x/s³+1/x²) is positive, with only the integral
orientation changing across1; its integral against1 is U'(x). Thus

    |y_c'(x)| <= epsilon |U'(x)|.

Finally y_c''=2(y_c+c)/x² and U''=2U/x²>0 give

    |y_c''(x)| <= epsilon U''(x).

Here U>=1, U'=(2/3)(x-x^-2), U''=(2+4/x³)/3,
V'=(2x+x^-2)/3>0, V''=(2-2/x³)/3. Including data errors, define

    b0(x)=eta0 U+eta1 |V|+epsilon(U-1),
    b1(x)=(eta0+epsilon)|U'|+eta1 V',
    b2(x)=(eta0+epsilon)U''+eta1 |V''|.                      (2)

Then |y^(j)(x)|<=bj(x), j=0,1,2. No sampling or analyticity assumption is
used. Supremum constants are finite and fully explicit: let M_U=max(U(l),U(u)),
M_V=max(|V(l)|,|V(u)|), M_U1=max(|U'(l)|,|U'(u)|),
M_V1=max(V'(l),V'(u)), M_V2=max(|V''(l)|,|V''(u)|). Then

    D0=eta0 M_U+eta1 M_V+epsilon(M_U-1),
    D1=(eta0+epsilon)M_U1+eta1 M_V1,
    D2=(eta0+epsilon)U''(l)+eta1 M_V2                       (3)

bound the respective uniform norms. Endpoint maxima follow directly from
the displayed derivatives and their monotonicity on either side of1.

For EXACTLY matched data the three residual-only pointwise kernels are sharp:
c(x)=+epsilon gives y=epsilon(U-1), y'=epsilon U', y''=epsilon U''.
Thus each individual residual-to-Cj component norm in(3) is attained; no
optimality of all combined noisy-data/readout bounds is claimed. This
witness can be a positive metric, e.g. p=1 and epsilon>=0, since U>=1.

## QC1-READOUT — clocks, gradient and proper acceleration

Static proper-clock-rate ratio between x,z is R_q(x,z)=sqrt(q(x)/q(z)).
This is an ideal metric clock comparison, NOT a derived light-transfer or
instrument law. Comparing the same supplied events/normalization,

    |log(R_q/R_p)| <= [b0(x)+b0(z)]/(2m) =: d(x,z).         (4)

Proof: log has Lipschitz constant1/m on[m,infinity). The relative clock
ratio consequently lies in[e^-d,e^d]; |R_q/R_p-1|<=e^d-1. No reference upper
bound is hidden in this logarithmic/relative statement. It is not a claimed
absolute-ratio error bound uniform across arbitrary reference ratios.

Let H_q=r0 partial_r log(sqrt(f))=q'/(2q), and let
J_q=r0 a_hat_r/c_E²=q'/(2sqrt(q)) be signed static proper support acceleration
in dimensionless units. They are different quantities. Add/subtract the same
reference numerator and use Lipschitz inverse and inverse-square-root:

    |H_q-H_p| <= b1/(2m)+|p'| b0/(2m²),
    |J_q-J_p| <= b1/(2sqrt(m))+|p'| b0/(4m^(3/2)).          (5)

Uniform versions replace bj by Dj and |p'| by its finite SUPPLIED reference
bound M1=||p'||_infinity,K (or the explicit sufficient bound
2|A|u+|B|/l²). This dependence is disclosed, not fitted or presumed uniform
over unbounded reference data. These algebraic bounds hold without assuming
epsilon infinitesimal. Sufficient positivity certification is also available:
if p>=m0>0 and D0<=m0/2, then q>=m0/2; otherwise no such certification follows.

## QC1-TIDE — full-metric normalization and curvature control

Use signature(-+++) and R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
+Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb. In each metric use its own
aligned static orthonormal tetrad: e0=(c_E sqrt(q))^-1 partial_t,
e1=sqrt(q)/r0 partial_x, e2=(r0 x)^-1 partial_theta,
e3=(r0 x sin(theta))^-1 partial_phi. These are frame components at matched
radius, not an assertion that the two orthonormal vector fields coincide.

Direct Levi-Civita curvature yields the dimensionless electric tides

    r0² R_hat0 i hat0 j = diag(q''/2, q'/(2x), q'/(2x)).   (6)

For example the independent Christoffels Gamma^t_tx=q'/(2q),
Gamma^x_tt=c_E² q q'/(2r0²), Gamma^x_xx=-q'/(2q),
Gamma^x_theta theta=-q x, Gamma^theta_x theta=1/x give(6), with the full
sphere connection retained. The other independent orthonormal sectional
components are r0²R_1212=r0²R_1313=-q'/(2x),
r0²R_2323=(1-q)/x²; mixed components vanish in this aligned spherical frame.

Hence radial tidal difference <=b2/2 and each tangential difference <=b1/(2x).
The remaining sectional differences are <=b1/(2x), b0/x² respectively.
These are exact dimensionless GEOMETRIC curvature bounds. Restore curvature
units by r0^-2; a relative-acceleration tidal matrix has the corresponding
factor -c_E² in this convention. No physical device or geodesic ensemble
is adopted or derived by these normalization statements. Uniform bounds
use D2/2, D1/(2l), D0/l². Curvature estimates themselves do not use m or M1;
the static tetrad exists only on the positive domain.

## Meaning, provenance and maximum conclusion

The new result is a quantitative implication for ALL C2 profiles at these
specified controls, not another finite compatibility example. It reuses
G260's exact identity/zero family. G261's W4 physical-metric role remains
WORKING/POSIT_NOT_CANON; historical necessity/adoption labels in that source
do not override current G312 authority. All proof here is conditional geometry,
not a new law determining profiles, dynamics, populations, content or scale.

Smallness at finitely many points is not the uniform residual hypothesis.
No general nonspherical/time-dependent theorem, near-horizon uniformity,
global/infinite-domain claim, physical stability or observational tolerance
is made. An empirical application additionally needs an independently justified
residual/calibration information source with held-out consequences; shared
errors require justified joint treatment. This theorem supplies neither such
information nor a UDT-predicted epsilon. GR recovery may be exact or bounded;
no departure is prescribed. All results remain UNPROMOTED.

Discovery: parent explored the Euler Green kernel and readout estimates after
recording step1 and before CPU checks. This candidate freezes that argument;
a fresh reviewer is independently reconstructing from sources before direct
candidate exposure. Relevant exact/full-metric checks will support algebra,
not replace the analytic quantifiers or certify actual observations.
