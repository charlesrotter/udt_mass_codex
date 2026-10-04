# FCL1 initial candidate — free-clock endpoint control

Conditional mathematical candidate, not yet reviewed. RG remains UNADOPTED.
No Einstein equation, physical geometry selection or native UDT prediction is
asserted. The scope is the exact CPW1 SUCCESSOR_SCOPE authorized after cleanup.

## 1. Claim and supplied objects

Let g=x^-2 gbar with x=Omega>0 inside a C3 Lorentz4 conformal completion. At the
chosen future boundary point p, x=0 and dx is nonzero timelike for gbar. Supply
one future unit timelike g-geodesic with finite interior initial data, eventually
in the regular collar and approaching p. No bound on T=u/x is assumed.

Then T approaches the future gbar-unit normal n at p. In the normal collar
coordinates constructed below, its spatial covector w satisfies

    |w(x)| <= exp(C x0) (x/x0) [|w(x0)| + C x0 log(x0/x)],   (1)

for a finite local coefficient bound C and a fixed interior collar value x0.
In particular w=O(x[1+log(x0/x)]) and T has a finite timelike limit. The
physical future proper time diverges, with

    tau(x) = -N(p) log(x/x_ref) + O(1).                     (2)

For the supplied regular conformal-null family from a regular interior emitter
and consistently normalized physical emission frequency omega_e=1, let K be
the nonzero future limiting conformal-affine tangent at reception after that
normalization. Then

    lim x Z = 1 / [-gbar_p(K,n_p)] > 0,   Z=omega_e/omega_o. (3)

Thus Z tends to positive infinity within this specified experiment. This is
neither a monotonic full-history theorem nor a distance curve. It quantifies
each geodesic/regular branch satisfying the supplied endpoint assumptions;
existence of those global preparations and uniform population bounds are not
proved. x is a defining function, not operational distance or X_max.

## 2. A collar that follows from RG, not a metric ansatz

Choose x=Omega. Since dx is timelike and nonzero at p, it stays timelike in a
small neighborhood. Flow coordinates along

    V = grad_bar x / gbar(grad_bar x,grad_bar x),  V(x)=1

carry spatial coordinates y^i from a boundary patch along its normal curves.
Vectors tangent to x-level sets are orthogonal to V. Hence in this chart

    gbar = -N(x,y)^2 dx^2 + h_ij(x,y) dy^i dy^j,             (4)

with N>0, h positive definite and future normal n=-N^-1 partial_x.
The given curve approaches p, so its final segment lies in a relatively compact
subpatch of this chart. Shrinking the chart if necessary supplies finite uniform
upper/lower bounds on N and the eigenvalues of h, and bounds on their first
coordinate derivatives. C3 original data give at least the C1 coefficients
needed here after the normal-coordinate construction. No bound on the clock's
velocity is part of those metric bounds. This is a coordinate choice available
for every admitted completion near p, not a homogeneous/diagonal restriction
on the spatial metric, field equation or preferred physical observer.

Because dx is past-oriented on future timelike curves on this side, x strictly
decreases along the receiver. Write

    T=u/x,  w_i=h_ij T^j,  gamma=sqrt(1+h^ij w_i w_j),
    T^x=-gamma/N,  T^i=h^ij w_j,  dx/dtau=-x gamma/N.         (5)

These are exact consequences of g(u,u)=-1 and future orientation. w at any
chosen interior x0 is finite; its eventual boundedness is still to be proved.

## 3. The geodesic supplies the missing estimate

The physical spatial covector is P_i=g_ia u^a=w_i/x. Metric geodesic motion
gives the exact lowered equation

    dP_i/dtau = (1/2) partial_i g_ab u^a u^b
              = -(partial_i N) gamma^2/N
                + (1/2) partial_i h_jk T^j T^k.            (6)

The cancellation of x factors uses partial_i x=0 in the chosen chart, not an
assumption of spatial uniformity. Combining (5) and (6) gives

    dw_i/dx = w_i/x + F_i,
    F_i = (partial_i N) gamma
          - [N/(2 gamma)] partial_i h_jk T^j T^k.           (7)

All spatial variation remains in F. With the ordinary Euclidean coordinate
norm r=|w|, the compact metric bounds imply

    |F| <= C(1+r).                                        (8)

Indeed gamma is bounded above by 1+c r and below by sqrt(1+c' r^2), with
positive finite constants from h. T^i is bounded in norm by c'' r. The second
term in (7) is therefore bounded by a constant times
r^2/sqrt(1+c' r^2), itself at most a constant times r. All constants arise
from the supplied metric on this compact chart; they are not physical scales.

Set s=log(x0/x), so x=x0 exp(-s). Equation (7) reads

    dw/ds=-w-x F.

At r>0 take its norm derivative; at r=0 use the upper right Dini derivative.
Both give

    D^+ r <= (-1+C x0 exp(-s)) r + C x0 exp(-s).            (9)

Multiplying by the positive integrating factor
exp(s-C x0[1-exp(-s)]) and integrating yields (1): the remaining forcing
integral is bounded by C x0 s. This is a scalar comparison estimate on every
finite s interval; it never assumes r is bounded at late times. Its right side
is finite and tends to zero as s tends to infinity. Large but finite initial
velocity changes its constant, not its vanishing limit. No uniform-in-initial-
data assertion is made.

It follows that gamma->1, T^i->0 and T^x->-1/N(p), since the curve approaches
p. Thus T->n_p, proving the first claim. Also

    dy^i/dx = -N h^ij w_j/gamma = O(x[1+log(x0/x)]).

Integrating to the already-supplied endpoint gives
y(x)-y(p)=O(x^2[1+log(x0/x)]). Bounded first metric derivatives then give
N(x,y(x))=N(p)+O(x), while gamma-1=O(x^2[1+log(x0/x)]^2).
Therefore d tau/dx=-N/(x gamma) differs from -N(p)/x by an integrable
remainder at zero. This proves (2), in fact a finite limiting additive
constant after subtraction of the logarithm. The completion endpoint is not
an event reached in finite receiver proper time.

## 4. Attach the actual signal family

The conformal connection relation already checked by CPW1 gives, for each
bar-affine null tangent kbar, the physical affine tangent k=x^2 kbar.
For a unit physical clock u=x T,

    omega=-g(k,u)=x[-gbar(kbar,T)].                         (10)

Start with any consistently normalized smooth conformal-affine family in the
supplied regular extension. The emitter approaches a regular interior event
e*, x_e stays bounded away from zero, and its unit clock has a regular timelike
limit. The unnormalized physical emission frequency
x_e[-gbar(kbar_e,T_e)] consequently has a finite strictly positive limit.
Multiplying each entire ray by its reciprocal enforces omega_e=1. That
normalization has a finite positive limit and preserves the supplied nonzero
regular limiting tangent K at reception. It inserts no emitted energy or
microscopic light law and cannot independently rescale the two endpoints.

Section3 supplies T_o->n_p. Smoothness and nonzero future null K then give

    B_o=-gbar(kbar_o,T_o) -> B*=-gbar_p(K,n_p),  0<B*<infinity.

The inner product is strictly negative because n_p is future unit timelike
and K is future nonzero null in a nondegenerate Lorentz space. By the existing
proper-clock/null-incidence theorem R6, Z=omega_e/omega_o=1/(x_o B_o), proving
(3). This is an actual comparison of varying interior emissions received by
one late free clock, not a choice of arbitrary unrelated unit vectors.

Under a smooth finite positive conformal gauge x'=a x, gbar'=a^2 gbar,
the physical Z is unchanged, T'=T/a, and its normal limit rescales likewise.
The limiting residue x' Z is a(p) times the old residue. Hence the divergence
is invariant under these regular gauges, but a numerical residue in x is not
a gauge-independent measured distance scale. No classification of singular
or vanishing conformal gauges is supplied.

## 5. What the proof does and does not connect

This closes CPW1's specified receiver-limit question under RG and the regular
null/clock preparation. It does not derive RG from positional dilation or from
the native scalar kernel. Boundary regularity and the existence of the chosen
branch remain supplied. No curvature-response equation has been inserted, and
the free spatial dependence of N,h was retained. The result therefore checks
robustness beyond FCW1's homogeneous/comoving calculation without selecting an
interior history or declaring that known GR-shaped geometry is a new UDT effect.

FCW1's zero-gradient beta=2 example still lies outside the stipulated regular
transverse completion. Its interior-bump freedom still defeats uniqueness.
CPW1's pointwise unbounded-rapidity illustration is not a free-geodesic
counterexample; (7) is the missing differential restriction. Accelerated clocks
are outside the present receiver quantifier and may behave differently. No
all-clock theorem, fixed-emission range, caustic/global existence, reciprocal
pair-plane reconstruction, physical X_max, selected scale, canonical statement,
or proof that complete UDT needs another premise is obtained.

This candidate was constructed before reading either fresh reviewer's
source-first argument. Exact short controls and exposed review follow a
separate freeze; their outcomes do not replace the general estimate above.
