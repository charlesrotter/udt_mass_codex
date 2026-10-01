# FPC1 author derivation — finite prepared clocks on supplied space forms

Unreviewed fixed mathematical candidate. The geometry, curvature sign and scale
are supplied comparisons, not selected UDT histories. Parent derived the formulas
analytically before seeing the mathematical reviewer's independently obtained
space-form formulas. The latter's brief concordance was received before this file
was frozen; its full proof was not read. Primary-method inspection is separately
recorded. No literature-wide novelty or new physical premise is claimed.

## Preparation and interpretation

Use PSW1's preparation: A passes through o with future unit U. A unit spacelike
n orthogonal to U defines B0=exp_o(Ln), and B starts with U parallel transported
along that spacelike geodesic. Both clocks then follow timelike geodesics.
Neighboring emissions vary on the same worldlines; preparation is not repeated.
Proper time has length units, c_E=1. Physical seconds are restored by division
by c_E. L is initial spacelike geodesic proper length, not radar, optical or
redshift-inferred distance. Curvature k² has dimensions length^-2 and stays free.

Two physical comparisons must be distinguished:

1. First signals are emitted independently at A0 and B0. Each has its own later
   future reception. The same-preparation first-leg slopes are denoted p and p_rev.
2. An A0 signal is received at B, immediately relayed, and received later at A.
   Its second-leg slope q is evaluated at that later B relay, not at B0.

Neither is an inverse-map comparison. The second protocol is exactly PSW1's
echo. The first is a precise symmetric version of two clocks observing each
other; selecting it as the universal positional assignment is not proved here.

## Positive constant sectional curvature +k²

Embed de Sitter4 in ambient Minkowski5 as <X,X>=1/k². A0=X0 has norm1/k²;
U and n have norms−1,+1 and are mutually orthogonal and tangent at X0.
The intrinsic spacelike geodesic and the two proper-time clock curves are

    B0=cos(kL) X0 + sin(kL) n/k,
    A(s)=cosh(ks) X0 + sinh(ks) U/k,
    B(tau)=cosh(k tau) B0 + sinh(k tau) U/k.

The ambient constant U is tangent along preparation and parallel there. Each
clock has unit timelike tangent; its second ambient derivative is normal to the
quadric, hence intrinsic acceleration zero. The quadric's Gauss equation gives
constant curvature+k² and Ric=3k²g; no field equation is used to obtain the clocks.
The three-dimensional ambient span displayed is a totally geodesic Lorentz2
subspace of the full4D geometry. That restriction is valid for this experiment
by its constructed initial data, not assumed for arbitrary PSW1 geometry.

Two points on this quadric have a null straight chord when their ambient inner
product is1/k². The chord then remains on the quadric and is an affine null
geodesic. Writing alpha=kL, the incidence equation is

    cos(alpha) cosh(ks) cosh(k tau) − sinh(ks)sinh(k tau) = 1.       (P)

For s=0 and0<alpha<pi/2, its future root has

    tau_b = artanh(sin alpha)/k = asinh(tan alpha)/k,
    p = d tau_b/ds = sec alpha.                                  (1)

Here the derivative uses the full incidence equation(P), not the single-flight
time as a function of L. Interchanging the two prepared clocks preserves(P),
so the separately emitted reverse first signal has the same future time and
p_rev=sec alpha. Equivalently an ambient spatial reflection exchanges X0 and
B0 while fixing U. This proves symmetry of the stated experiment, not q=1/p.

For the later echo, apply(P) to A(a),B(tau_b). Since cosh(k tau_b)=sec alpha
and sinh(k tau_b)=tan alpha, the equation becomes

    cosh(ka) − tan(alpha)sinh(ka) = 1.

The root a=0 is the earlier emission event and must not be selected as a future
return. A finite future root exists only for0<alpha<pi/4:

    a = 2 artanh(tan alpha)/k,
    q = da/d tau at the matched relay = cos(alpha)/cos(2alpha).    (2)

The full moving incidence equation gives q, with L and worldlines fixed.
The p*q echo derivative therefore equals1/cos(2alpha). At alpha→pi/4 from
below, q and a diverge while p approaches sqrt(2). For pi/4≤alpha<pi/2,
both first signals still have finite future receptions, but that particular
immediate echo cannot return in finite A proper time. Continuing q past its
denominator zero would give an inadmissible branch, not a blueshifted echo.

As alpha→pi/2 from below, p=p_rev→infinity and each first reception proper
time diverges. At the limiting separation, the incidence equation has no finite
future root. This is a boundary of this comparison, not a material wall or a
curvature singularity: de Sitter curvature stays finite and the full geometry
continues. No native X_max identification is made. Initial proper separation,
first-leg observability and echo availability are distinct operational objects.

For each fixed k, as L→0,

    log p = k²L²/2 + k⁴L⁴/12 + O((kL)^6),
    log q = 3k²L²/2 + 5k⁴L⁴/4 + O((kL)^6).

These agree with PSW1 because T(n,n)=−k². Smallness requires |kL|≪1;
no observed solar threshold follows while k is unfixed. The exact formulas,
not truncated series, own the limiting boundary statements.

## Flat and negative-curvature controls

For flat spacetime the same preparation gives A(s)=(s,0),B(tau)=(tau,L):
tau=s+L and a=tau+L, so p=p_rev=q=1 for every regular finite separation.
Finite causal timing survives equal rates. No counterfactual removal of UDT's
foundational geometry is represented by this supplied flat comparison.

For sectional curvature−k², use the anti-de Sitter covering space and its
ambient quadric <X,X>=−1/k² in signature(−,−,+,+,+). Take

    B0=cosh(kL)X0+sinh(kL)n/k,
    A(s)=cos(ks)X0+sin(ks)U/k,
    B(tau)=cos(k tau)B0+sin(k tau)U/k.

Preparation/normalization/geodesicity follow as above. The direct first null
branch near the chosen clocks obeys

    cosh(alpha) cos(ks)cos(k tau)+sin(ks)sin(k tau)=1.

On the first future branch, for every finite L>0,

    tau_b=arctan(sinh alpha)/k,
    p=p_rev=sech alpha,
    a=2 arctan(tanh alpha)/k,
    q=cosh(alpha)/cosh(2alpha).

The unwrapped covering avoids treating periodic embedding time as physical
closed timelike curves. This is the direct branch, with no reflecting boundary
or late winding/return condition added. It is not a global AdS initial-boundary
problem. Both slopes are below one; positive curvature's sign is therefore a
genuine choice among these comparisons, not a consequence of ordinary clocks.
The small-L expansions have opposite quadratic signs and the same quartic signs
as the positive case. Curvature zero follows continuously at fixed finite L.

## Native-versus-comparison boundary

The space forms are homogeneous/isotropic geometric comparisons. Every freely
falling observer can construct the same experiment, so its observer-centered
coordinates do not designate a universal physical center. But covariance and no
preferred observer do not imply that every actual germ is a space form. G212
already records the extra all-germ isotropy route and its unadopted status.
DDR plus an unadopted Ricci-response identification allows the larger Einstein
class, not automatically this zero-Weyl subclass or positive/free k.

The factor sec(alpha) has an inverse-square-root form if y=sin(alpha):
p=(1−y²)^−1/2. That algebraic similarity does not identify y with physical
velocity or the completed UDT scalar. On the actual clock leg the latter is

    Phi_clock=−log p=log cos(alpha),
    chi_clock=tanh(Phi_clock)=−sin²(alpha)/(1+cos²(alpha)).

The proper initial separation and y are separately typed. No fitted response,
second propagation law, preferred observer, source or scale has been inserted
after the clock readout. A known comparison geometry can realize nonlinear
mutual first-leg slowing and an unreachable comparison limit. Its additional
positional interpretation and selection by native UDT remain open; the shape
alone cannot distinguish UDT from an allowed GR comparison.
