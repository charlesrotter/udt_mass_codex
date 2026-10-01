# ECS1 initial argument — a finite echo discriminator with transverse ambiguity

This is a frozen candidate for review, not physical adoption. It uses the
PSW1/FPC1 preparation and conditional null-clock interface already integrated
in UDT_DEVELOPMENT R6/R8. Curvature and alternative metrics are supplied controls.
The question is what the two measured clock rates can distinguish, not which
geometry the complete UDT postulates select.

## 1. Quantities and independent reconstruction

Let s be A's emission proper time, tau B's reception proper time, and a A's
proper time at the immediate future return. Keep the prepared worldlines fixed
when differentiating nearby emissions. At the initial first signal s=0 define

    p = d tau/ds,  q = da/d tau at its matched relay,  E_echo = da/ds = p q.

q is not the independently emitted reverse first signal and is not the total
echo stretch. All are positive on their specified regular future branches.
Use length units for proper time (c_E=1). Initial proper spacelike separation is
L>0; B receives the parallel transport of A's initial velocity and is released.
The ideal relay maps arrival to immediate re-emission without an added delay law.

Reconstruct on the space form's radial two-dimensional sheet using its static
metric h=-f(r)dt^2+dr^2/f(r), f=1-kappa r^2. A lies at r=0, so t is its proper
time. At t=0 the initial preparation is spacelike geodesic within this sheet;
parallel transport gives B initially at rest. Write r0=S_kappa(L) and
c=sqrt(f(r0))>0. B's conserved Killing energy is c. Proper-time equations are

    t_dot=c/f,  r_dot=v,  v^2=c^2-f,  v_dot=kappa r.

Let r_*=integral_0^r du/f(u), u=t-r_*, w=t+r_*. Radial outgoing and incoming
null incidences have u=s and w=a. On B's worldline, normalization gives

    u_dot=(c-v)/f=1/(c+v),   w_dot=(c+v)/f=1/(c-v).

Consequently p=c+v_b and q=1/(c-v_b) at the first relay. These equations come
from the original metric and its null/proper-clock equations. They already show
the more general static-sheet identity p+1/q=2c; they do not yet impose p=1/c.
That additional statement must be obtained from first incidence in this metric.

### Positive curvature and chronology

Set kappa=k^2, alpha=kL, c=cos alpha, s_alpha=sin alpha. We reconstruct the
common finite-echo sector 0<alpha<pi/4. This is narrower than FPC1's extended
first-signal branch; no static-chart calculation is used beyond its domain.
The released trajectory before its static horizon is

    r=(s_alpha/k)cosh beta, v=s_alpha sinh beta,
    t=atanh(tanh beta/c)/k, beta=k tau.

These solve the above equations and initial data. Put x=tanh beta. The patch
requires 0<=x<c. Outgoing incidence t=r_* is

    x/c = s_alpha/sqrt(1-x^2).

Squaring yields (x^2-s_alpha^2)(x^2-c^2)=0. With x>=0 and c>s_alpha, the
regular first root is x=s_alpha. The apparent root x=c is the excluded static
horizon, not an additional finite incidence. At the first root

    r_b=s_alpha/(kc), v_b=s_alpha^2/c,
    p=1/c, q=c/(2c^2-1), a=2atanh(tan alpha)/k.

Thus the return loses finite future reception at alpha=pi/4 while p approaches
sqrt(2). FPC1 independently established that a first signal can still arrive
on the extended geometry for pi/4<=alpha<pi/2; this static reconstruction does
not reprove that extension. Continuing the return expression beyond its domain
would not describe an admissible future echo.

### Negative curvature and flat limit

For kappa=-k^2 set alpha=kL>0, c=cosh alpha, s_alpha=sinh alpha. Before B's
first crossing of A, beta=k tau is in [0,pi/2), and

    r=(s_alpha/k)cos beta, v=-s_alpha sin beta,
    t=atan(tan beta/c)/k.

Now r_*=atan(kr)/k. With x=tan beta>=0, incidence is
x/c=s_alpha/sqrt(1+x^2), hence (x^2-s_alpha^2)(x^2+c^2)=0.
The unique nonnegative real root is x=s_alpha. Therefore

    r_b=s_alpha/(kc), v_b=-s_alpha^2/c,
    p=1/c, q=c/(2c^2-1), a=2atan(tanh alpha)/k.

Every finite L>0 has these direct first and immediate return branches. This
uses the AdS cover and selected direct paths, not periodic time or reflected
boundary rays. For flat h=-dt^2+dr^2, B remains at r=L and p=q=1.

## 2. What is independent of the supplied scale

Eliminating c yields, on the common regular echo branch,

    q = p/(2-p^2),   E_echo = p^2/(2-p^2),   0<p<sqrt(2).

Positive curvature gives 1<p<sqrt(2), negative curvature 0<p<1, and flat p=1.
The identity by itself therefore selects neither curvature sign nor scale.
Its zero-residual form F=(2-p^2)q-p is algebraically convenient, but physical
use still requires p,q>0 and the branch. The relation is an implicit consequence
of the prior FPC1 formulas, not a new field equation or discovery of the space form.

Two actual readings are needed for a test: e.g. outgoing p and measured total
echo E_echo, or outgoing and return-leg ratios. Generating q from the same formula
only checks algebra. Timing noise and shared-clock covariance would require an
observational model; no measured data or tolerance is provided here. No external
GR subtraction or numerical curvature calibration appears in this diagnostic,
but the clock preparation and the supplied family remain essential assumptions.

## 3. A discriminating comparison from the existing Kasner control

Use exactly FPC1 math/DERIVATION.md's one supplied Kasner metric, exponents
(-1/3,2/3,2/3), t0=1, its spacelike preparation and transported initial velocities.
These are not arbitrary comoving clocks. Write P=log p and Q=log q. Near p=1,

    log[p/(2-p^2)] = P-log(2-exp(2P)) = 3P+4P^2+O(P^3).

P=O(L^2). Its logarithmic echo residual H=Q-P+log(2-exp(2P)) therefore has
cubic coefficient Q3-3P3. The saved source's exact coefficients give

    H = -16 L^3/27 + O(L^4), axis exponent -1/3;
    H =   8 L^3/27 + O(L^4), either exponent 2/3.

The original analytic small-L scope guarantees a nonzero residual for each of
these directions at sufficiently small positive L; no explicit finite-L error
bound is claimed. All directions still obey PSW1's leading 1:3 ratio. Thus the
finite relation is not a tautology of that leading theorem or of the null-clock
interface on all smooth geometries. Do not average away the result: the cubic
coefficients cancel in the triad mean. Higher-order spherical averages are not
inferred. This is a supplied comparison, not a native-admitted countermodel or
an empirical failure of UDT. Original Kasner worldline work is retained at source;
the present check can recompute its saved outputs without claiming a new solve.

## 4. An exact continuum of transverse mimics

A converse from this restricted clock record to the full four-dimensional
geometry is false. Let h_kappa be the above regular Lorentz sheet, let x=(t,r),
y=(y1,y2), and supply any smooth positive-definite two-by-two H_AB(x,y). Define

    g_H = h_kappa,mu nu(x) dx^mu dx^nu + H_AB(x,y) dy^A dy^B.

There are no mixed dx dy terms and h is independent of y. Direct connection
identities give Gamma^mu_nu rho[g_H]=Gamma^mu_nu rho[h] and
Gamma^A_mu nu[g_H]=0. Each fixed-y sheet is therefore totally geodesic. Every
base-tangent preparation geodesic, parallel-transported velocity, free clock and
selected radial null leg remains in that sheet and satisfies the same equations.
Its proper intervals and endpoint frequency contractions are identical. On a
regular direct branch, all p,q and arrival maps, not just two numbers or a finite
series, agree for the continuum of allowed L in the chosen sheet. Nearby emission
derivatives use those same fixed worldlines. Arbitrary transverse H remains
unmeasured by this restricted family. Positive transverse metric also makes the
base projection of any causal tangent base-causal; no transverse shortcut can
arrive outside the base causal future. This is not a claim of global uniqueness
of rays; the selected local/direct branch is retained.

An explicit constant transverse metric H=I makes g=h_kappa+dy1^2+dy2^2.
For kappa!=0, its base sectional curvature is kappa while mixed sections are
flat, so it is not a four-dimensional space form. Ric_g=kappa h_kappa on the
base and zero on the transverse plane; scalar curvature is 2kappa, not the
4D space form's 12kappa with the same base curvature. Its trace-free Ricci is
nonzero. This is consequently not an Einstein-sector or Ric=0 mimic for nonzero
kappa, and is not asserted to satisfy a selected DDR response or native UDT.
It is an exact smooth Lorentz kinematic witness refuting full-metric uniqueness
from the restricted record. The witness extends only as far as its supplied
regular domain; no physical X_max, source or global completion follows.

The quantifier matters: a continuum of aligned tests within a sheet can agree
without every direction, every four-dimensional observer, every preparation or
every optical/transverse measurement agreeing. In the explicit product, changing
preparation into a flat transverse direction gives a different experiment.
No exhaustive classification of metrics satisfying an all-laboratory echo law is
attempted. No extra observer-invariance or all-germ isotropy premise is adopted.

## 5. Maximum conclusion and source/exposure boundary

This supplies a nontrivial necessary clock-consistency relation for the chosen
signed space-form experiment, a known same-protocol failure outside that family,
and an exact nonunique four-dimensional realization of its restricted records.
Passing may test that experiment's consistency, not establish unique geometry,
native physical admission, an additional effect beyond GR, scale or X_max.
Failure under the same justified protocol rejects that supplied model/assignment,
not the complete UDT founding interpretation. Physical branch admission remains
open; compatibility, observational calibration and selection are separate.

Parent had prior FPC/FST formulas, the discussion corollary/Kasner subtraction,
and source-review feedback before discovery. Parent developed the static-energy
and transverse-mimic arguments, then received ecs_math's brief synchronous-route
outline before this written freeze. No unexposed or different-model discovery is
claimed. Current reviewer proof/code files were not read before this freeze.
Exact original sources, conditions and review limits remain controlling.
