# Fixed empirical curves and their conditional geometry

DRAFT, exposed follow-up after the immutable metric-led pass. No refit, new
family fit, coefficient retuning or physical adoption. Inputs, versions and
exact fixed coefficients are pinned in data_inverse_01.stdout.json. The parent
owns the observational source/transfer/calibration assumptions. Here F is
interpreted as h0 d_e only through the already declared homogeneous inverse.

The primary data span is 0.02303<=z<=2.26137, or
0.0227688121<=x<=1.1821473525. Everything about larger x is extrapolation.
This context saw the data-lane coefficients and parent BAO summary after
INITIAL_FREEZE; it makes no outcome-blind or independent-data claim.

## The quadratic exponent: a valid finite-range inverse, a singular flat tail

For the fitted point estimate

    F2=x exp(p),  p=a x+b x^2,
    a=0.24480409236803655, b=-0.15933068708454678,
    F2'=exp(p) P,  P=1+a x+2b x^2.

Exact rational root isolation of these saved decimal coefficients gives one
positive simple root

    x*=2.19675504721078240947...,  z*=7.995775220779238... .

P>0 on 0<=x<x*, so the full observed interval has a smooth expanding flat
compatibility metric. Beyond x*, F2'<0 and that same expanding inverse fails.
This is a coefficient-specific extrapolation, not an observed boundary.

The finite limit is more than a coordinate-denominator warning. Let
delta=x*-x>0 and define

    C=exp[x*-p(x*)]/[-P'(x*)]=9.8115617640... >0.

As delta -> 0,

    H/h0 ~ C/delta,
    T-T* ~ delta^2/(2 h0 C),
    dH/dT ~ -h0^2 C^2/delta^3.

The last equation uses the ORIGINAL inverse relation dx/dT=-H. The flat
homogeneous scalar curvature 6(dH/dT+2H^2), independently recovered from the
metric in author_01, therefore diverges negatively. Its Riemann-square
`12[(dH/dT+H^2)^2+H^4]` diverges positively. This is an actual curvature
singularity of this literal flat-history extrapolation, at finite scale factor
a*=0.1111632934 and finite normalized proper/affine extents:

    h0(T_o-T*)=0.8531528397,
    h0 lambda*=0.5129330857,
    F2(x*)=1.7434547020.

The outcome rejects this unchanged infinite-range FLAT reconstruction as a
regular global completion. It does not reject the fitted finite-range curve,
prove a UDT inconsistency, or establish a physical X_max.

## A curved turning point removes this particular obstruction

The curved inverse is `H/h0=e^x S'_k/F'`, with the sign of S'_k retained across
a transverse-distance maximum. The positive square-root formula in the initial
pass was expressly restricted to the increasing branch. Choose, as a supplied
mathematical alternative,

    kappa=k/h0^2=1/F2(x*)^2=0.3289869445... .

Then F2 has precisely the height of the first maximum of
`sin(sqrt(kappa) u)/sqrt(kappa)`, where u=h0 chi. Define

    u(x)=asin(sqrt(kappa)F2(x))/sqrt(kappa)       (x<=x*),
    u(x)=[pi-asin(sqrt(kappa)F2(x))]/sqrt(kappa) (x>=x*).

Near the nondegenerate maximum, the two branches join smoothly with

    u'(x*)=sqrt[-F2(x*) F2''(x*)]>0,
    lim H/h0=e^x*/sqrt[-F2(x*) F2''(x*)]=7.115133196... .

To see smoothness, write `F*=F(x)+(x-x*)^2 A(x)` with analytic A>0 locally.
The signed square root in the arcsine expansion removes the absolute value;
u is analytic with nonzero derivative. Thus T_x=-e^-x u'/h0 is nonzero and
the reconstructed metric is regular at this turn. It is NOT a caustic: F*>0.

This is an explicit alternative, not a new fit, native repair, curvature
measurement or global-completion claim. The curvature was supplied to match
the extrapolated maximum, outside the data range. It shows why a zero F' is
not a universal geometric impossibility. Other global issues remain open.

## The cubic exponent: a contrasting, regular past asymptote at its point estimate

For the saved F3 coefficients,

    F3=x exp(a x+b x^2+c x^3),
    a=0.2631133505233656,
    b=-0.22051746155027002,
    c=0.0491683028862887,
    P=1+a x+2b x^2+3c x^3.

Exact rational isolation of P has only one real root, which is negative.
Since P(0)=1, P>0 for every x>=0. Its nonnegative local minimum is
P(1.6281116835...)=0.8958945175... . Thus the fixed point estimate has a smooth
flat homogeneous inverse for ALL x>=0, not only a sampled finite interval.

Because c>0, asymptotically

    F' ~ 3c x^3 exp(c x^3+b x^2+a x),
    H/h0 ~ exp[-c x^3-b x^2+(1-a)x]/(3c x^3) -> 0.

Both integrals `int e^-x F' dx` and `int e^-2x F' dx` diverge; F and e^-x F
also diverge. Meanwhile H_T=-H H_x and all polynomial factors multiplying
H^2 tend to zero, so both the scalar and Riemann-square curvature tend to zero.
Consequently T(x) maps x>=0 onto the entire past interval (-infinity,T_o].
The scale factor tends to zero only at infinite proper past time, not at an
interior degenerate metric. Every point at finite x is regular.

There is a strong but explicitly conditional completeness statement here.
In this spatially flat homogeneous metric, each past null geodesic has fixed
spatial momentum and affine extent proportional to `int a dT`, which diverges
by the second integral. A timelike geodesic with finite conserved spatial
momentum p has proper length `int dT/sqrt(1+p^2/a^2)`. For p=0 it is the infinite
proper past time; for p!=0 its past integrand is asymptotic to a/|p| and its
integral also diverges. Thus this supplied complete-spatial-slice metric is
past null/timelike geodesically complete. No future completion is asserted.
This establishes a compatible unreachable past asymptote for these queries,
not merely a coordinate pole. It is still an empirically chosen expanding
geometry, not native UDT selection or the intended expansion-free explanation.

That conclusion applies to the exact extrapolated CENTRAL coefficients only.
The saved marginal error of c is 0.1467374630, substantially larger than c.
The data lane's z<1 sensitivity gives c=-0.1479900366 with still larger error.
Strong coefficient covariance is retained in its output. Hence neither a
positive cubic tail nor past completeness has empirical confidence established
by this campaign. The near equality of F2/F3 inside the data range coexists with
radically different unconstrained tails.

## Smooth extensions demonstrate the remaining freedom directly

One can preserve F2 EXACTLY throughout the observed interval without accepting
its singular extrapolation. Let x0=x_data,max and choose any x1 with
x0<x1<x*. These are mathematical transition labels, not physical boundaries or
new measured scales. Let w(x) be a smooth step equal to 0 for x<=x0 and 1 for
x>=x1, flat to all derivative orders at both ends. An explicit choice on the
interior, with t=(x-x0)/(x1-x0), is

    w=exp(-1/t)/[exp(-1/t)+exp(-1/(1-t))].

For any supplied A>0 and p>=0 set, for x>=x0,

    G_p(x)=[1-w(x)]F2'(x)+w(x) A exp[p(x-x1)],
    F_ext(x)=F2(x0)+int_x0^x G_p(u)du,

and use F_ext=F2 for x<=x0. Both terms are nonnegative and at least one is
positive: F2'>0 on the transition interval; after it G_p is the positive tail.
Flatness of w at the ends gives a C-infinity join. The extension is therefore
strictly increasing and preserves every in-range value and derivative exactly.

For p=0 its proper and affine past extents are finite. For p>=2 both diverge;
intermediate p reproduce the thresholds in the initial pass. These are explicit
compatible metrics with identical fitted-interval shape and different far tails.
They are mathematical nonidentifiability witnesses, not new fit families,
physical transition mechanisms or proposed laws. F2's global failure is therefore
not forced by the observed-range curve itself, even within the flat inverse class.

## Spline and uncertainty limits

The frozen F4 point estimate has `1+x S'(x)/(5/log(10))>0` over the entire
data interval; the float64 piecewise-polynomial minimum is 0.6532645095.
Its terminal polynomial has no additional positive derivative zero beyond
the final knot in this diagnostic, but spline extrapolation is an algorithmic
choice, not physical completion. The natural cubic is only C^2 across knots.
The literal inverse is therefore a C^2 metric there and a smooth metric on
each open knot interval; the smooth-metric premise is not silently upgraded.
No smoothing or refit is performed. Parent's Gaussian-propagation problem is
separate and its withheld F4 BAO quadratic is not restored here.

data_inverse_values.tsv records conditional H/h0, q_dec and AP plus local
Jacobian errors for F2/F3. The covariance is the saved marginal shape covariance;
h0 remains uncalibrated and normalization at x=0 is family-imposed extrapolation.
These bands omit family error and global-tail uncertainty. Analytic Jacobians
agree with three finite-difference steps; finest scaled discrepancy 7.12e-11.
The comparison plot shows the supported-interval overlap and literal tail
contrast, with no uncertain global band disguised as measurement.

Author run data_inverse_01 exited 0 in 2.02 seconds with empty stderr. A later
read-only output-summary command mistakenly passed a Path to json.load, failed
before reporting, and was corrected to json.loads(path.read_text()); saved
scientific outputs were unaffected. One draft patch failed atomically due to
a stale context line; the corrected patch was then applied. No scientific run
or unfavorable result was discarded.
