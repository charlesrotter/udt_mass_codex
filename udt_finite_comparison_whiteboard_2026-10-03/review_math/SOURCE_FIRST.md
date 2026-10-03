# Source-first mathematical reconstruction — FCW1

Reviewer `/root/fcw_math_review`, 2026-10-03. This record is written before any
FCW1 proposer or parent proof, code, output or verdict is opened. The test design
and its exact exposure record precede the calculation. Parent continuing startup
is attributed to WORK_ORDER/BASELINE; own grok HEAD/status inspection agreed.
No protected payload was inspected or hashed. This is a fresh context with the
inherited GPT-6 model family; a distinct model/library is not claimed.

## 1. Actual boosted incidence in the product

Write gamma^2=1+u^2, gamma>0. The initial connecting path is (0,x,0,0),
0<=x<=L. Its length is L and its connection coefficients along the path vanish
at t=0, so parallel transport preserves U=gamma partial_t+u partial_y. The two
supplied curves are geodesic and have unit proper-clock speed. Thus the boost
does not silently change the initially parallel preparation.

The two-dimensional base embeds as

    X(t,x)=k^-1(sinh(kt), cosh(kt) sin(kx), cosh(kt) cos(kx))

in ambient signature (-,+,+). Pullback gives precisely
-dt^2+cosh(kt)^2 dx^2. In a convex normal neighborhood, a future timelike base
geodesic with proper duration T satisfies k^2<X_e,X_o>=cosh(kT). On the product,
the transverse displacement is u(b-s); the product null condition requires
T=|u(b-s)|. The u=0 limit is the base-null condition. Hence actual incidence is

    F(s,b,L)=cosh(kgamma s)cosh(kgamma b)cos(kL)
             -sinh(kgamma s)sinh(kgamma b)-cosh(ku(b-s))=0.

The first arrival solves F(0,b,L)=0. Because the base has x translation and
reflection isometries, the actual immediate return solves F(b,a,L)=0. Endpoint
variation, with these worldlines and L held fixed, gives

    p=-F_s(0,b,L)/F_b(0,b,L),
    q=-F_s(b,a,L)/F_b(b,a,L).

These expressions come from null incidence, not from inserting the tested echo
identity. A second independently emitted reverse first signal is not used.

For regularity, scale s=L sigma,b=L beta and divide F by L^2. At L=0 the result
is k^2[(beta-sigma)^2-1]/2, with nonzero beta derivative at beta=sigma+1 for
k!=0. The analytic implicit-function theorem selects the local future branch.
The k=0 flat limit is elementary. Time reversal plus L reversal makes arrivals
odd in L and p,q even. Consequently Taylor remainders below are analytic at
fixed finite u,k; no uniform boost range or numerical finite-L bound is claimed.

The script uses ell=kL, v=u^2 and dimensionless proper arrivals. Its reconstructed
series begin

    kb = ell +(v+1)ell^3/6 +(v+1)(11v+15)ell^5/360 + O(ell^7),
    ka = 2ell +4(v+1)ell^3/3 +(v+1)(221v+240)ell^5/180 + O(ell^7),
    p = 1 +(v+1)ell^2/2 +(v+1)(4v+5)ell^4/24
          +(24v^3+106v^2+143v+61)ell^6/720 + O(ell^8),
    q = 1 +3(v+1)ell^2/2 +(18v^2+37v+19)ell^4/8
          +(734v^3+2386v^2+2573v+921)ell^6/240 + O(ell^8).

The seventh-order arrival coefficients, retained in the machine record, are
needed to compute the displayed sixth-order stretches. Cancellation through
fourth order is exact. The result is

    D=log q-log[p/(2-p^2)]
     =-u^2 gamma^4 (kL)^6/3 + O((kL)^8).

For every fixed u!=0,k!=0, the scalar echo identity therefore fails for all
sufficiently small positive L. On this branch p tends to1 and q tends to1, so
0<p<sqrt(2), q>0 and both receptions are future and finite. The unboosted case
has exactly p=sec(ell), q=cos(ell)/cos(2ell) on its allowed echo domain, and
satisfies the identity. Flat k=0 gives p=q=1 for every common inertial boost.

For gamma=5/4,u=3/4 the coefficient is -1875/4096. Five independent high-precision
actual incidence solves at L=0.1 down to0.00625 give D/L^6 from -0.4794985593
to -0.4578458343, tending toward -0.457763671875. Incidence residuals are below
9e-82, against a frozen1e-70 threshold. These finite floating-point anchors do
not certify arbitrary-distance roots or a rigorous finite error threshold.

Survivor: this supplied product is distinguishable from the corresponding
space-form echo law by a boosted prepared experiment. This breaks only a
universal agreement assertion for this mimic. It does not prove all-frame
rigidity, uniqueness, native admission, or a universal physical echo law.

## 2. The regular conformal endpoint

Supply the four-metric g=Omega(eta)^-2 diag(-1,1,1,1), Omega>0 on[0,E),
Omega(0)=1, with the comoving ordinary proper clocks and conditional R6 interface.
Here eta0=0 and the receiver is at coordinate/initial proper separation L.
Null incidence is eta_o=eta_e+L and d tau=d eta/Omega, so the emission-period
ratio at eta_e=0 is p(L)=1/Omega(L). A direct four-dimensional Christoffel/Ricci
calculation independently yields

    R=12(Omega')^2-6 Omega Omega'',
    H=-Omega',   d/dt=Omega d/deta,
    R=6 p''/p^3.

No field equation is used. Suppose Omega has a C2 one-sided extension to E,
Omega(E)=0 and Omega'(E)=-h<0. Then Omega=h(E-L)+O((E-L)^2), so

    p(L) ~ 1/[h(E-L)],     R(L) -> 12h^2,
    H -> h,                Hdot=-Omega Omega'' ->0.

The proper time diverges logarithmically: t(L)=-(1/h)log(E-L)+O(1). The finite
conformal endpoint is consequently at infinite comoving proper time. The C2
extension is load-bearing: it controls Omega Omega''; a bare divergent p alone
does not force a finite positive scalar-curvature limit.

Controls expose the limits. For Omega=(1-L/E)^beta,

    R=6 beta(beta+1) E^-2 (1-L/E)^(2beta-2).

Beta=1 has a simple zero and R=12/E^2. Beta=2 has a double zero, violates
Omega'(E)<0, and R tends to0 despite p diverging. If the dispatch shorthand
beta1/2 meant beta=1/2 instead of beta=1 and2, the same general formula gives
R=(9/2)E^-2(1-L/E)^-1, diverging; this Omega lacks a C1 endpoint extension.
None is asserted to be a native history.

For explicit interior freedom, let z=4(L-E/2)/E and let f=exp[-1/(1-z^2)]
on E/4<L<3E/4 and0 elsewhere. It is smooth and compactly supported. With
0<epsilon<1, Omega_epsilon=(1-L/E)(1+epsilon f) remains positive, has the
same initial normalization, and agrees exactly with the affine Omega near the
endpoint. Thus h and the asymptotic curvature are unchanged while p differs in
the interior. At L=E/2,

    Omega_epsilon=(1+epsilon/exp(1))/2,
    R_epsilon=12 E^-2(1+epsilon/exp(1))(1+5epsilon/exp(1)).

The machine string uses SymPy's E for Euler's number and the endpoint symbol E;
the explicit expressions here disambiguate that display-only overlap.

Survivor: a regular simple conformal zero forces this asymptote within this
supplied homogeneous conformal sector. It selects neither h nor E, neither the
interior metric nor its response/source equation, and proves no native X_max
realization or global physical admission. Calling the added endpoint hypothesis
UNADOPTED is essential. No general tensor rigidity or field equation follows.

## Evidence and omissions

One script, six declared symbolic/control families, five numerical cases;
Python3.10.12, SymPy1.13.1, mpmath1.3.0. Captured run returned0 in16.590724s,
max RSS69600KiB,2GiB virtual limit, one BLAS thread, no elapsed/CPU timeout,
no GPU. Seven exact zero checks and the actual incidence anchors passed. The
entire arguments, not check counts, own the local quantifiers and hypotheses.
No prior FCW1 scientific implementation was imported. The embedding argument
and original conformal tensor construction were source-first independent routes.

Not performed: generic metric census, global arrival/caustic classification,
all-frame rigidity proof, physical light/carrier model, native field/source
selection, observational fit, formal proof, human or different-model review,
full-corpus reproof, and central integration review. Exposed candidate review
has not yet occurred; this is not a final candidate acceptance verdict.
