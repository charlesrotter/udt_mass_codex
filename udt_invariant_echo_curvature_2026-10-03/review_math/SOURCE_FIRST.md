# Source-first mathematical finding — sealed before IEC1 candidate exposure

The universal sixth-order-only guess is refuted by a regular parallel-prepared
clock experiment in a supplied locally symmetric Lorentz4 metric. This does not
refute FCW1's restricted result: its absent transverse electric-tidal component
is nonzero in the following control. No physical equation or UDT admission follows.

## Exact geometry and protocol

Use the product metric `-dt² + dS²_unit-sphere + dz²` (the symbol S denotes a
Riemannian sphere here, not de Sitter). Work in a small geodesically convex
neighborhood, with z fixed. Let P be a unit sphere point, e1,e2 tangent
orthonormal vectors, and e0 the time direction. Set

    U=gamma e0+u e1, gamma²-u²=1,
    m=u e0+gamma e1, n=a m+b e2, a²+b²=1,
    h²=a² gamma²+b²=1+a²u², r=a gamma/h.

All parameters and this product are supplied FREE-AND-EXPLORED. The sphere's
connection is tangential projection of the ambient derivative. Applying that
projection twice gives R(X,Y)Z=<Y,Z>X-<X,Z>Y. Thus its curvature is parallel;
the product connection gives nabla R=0 in Lorentz4. This establishes the needed
geometry directly, without importing a classification theorem or field equation.

The initial separation geodesic has time coordinate a u L and sphere endpoint
PB=cos(hL)P+sin(hL)N, N=(a gamma e1+b e2)/h. Parallel transport of e1 along it is

    e1B=e1+(cos(hL)-1)r N-sin(hL)r P.

This follows by rotating its component r N within the (P,N) plane, keeping its
orthogonal tangent component fixed; the covariant derivative is zero. A(s) has
time gamma s and sphere position cos(us)P+sin(us)e1. B(t) has time
a u L+gamma t and sphere position cos(ut)PB+sin(ut)e1B. They are unit free clocks
and exactly implement PSW's parallel preparation, without re-preparation.

Product null incidence is equality of the small sphere distance and the absolute
time difference. Dotting the sphere endpoints gives the exact equation

    F(s,t,L)=cos(us)cos(ut)cos(hL)
      +sin(us)sin(ut)[1+(cos(hL)-1)r²]
      -r sin(hL)sin(u(t-s))-cos(gamma(t-s)+a u L)=0.

Solve F(0,tB,L)=0 with tB/L→1. The actual immediate later return solves
F(sA,tB,L)=0 with sA/L→2. Then

    p=-F_s/F_t at (0,tB),
    q=-F_t/F_s at (sA,tB).

The outgoing and return future time increments have leading coefficients
gamma+a u and gamma-a u, both positive. We do not assume an exchange reflection
of the two future clocks. The parent's later reminder of that definition arrived
after TEST_DESIGN/code were written and before execution results; it exposed no
coefficient and agreed with the independently chosen construction.

## Exact result and remainder

At u=3/4,gamma=5/4,a=3/5,b=4/5, put z=L². Independent polynomial incidence
expansion through L8 and exact rational implicit substitution give

    tB/L=1-3z/50-533z²/50000-29963z³/33600000+O(z⁴),
    sA/L=2-12z/25+45581z²/200000-69521741z³/672000000+O(z⁴),
    log p=-3z(19200000+4948000z+557167z²)/320000000+O(z⁴),
    log q=-9z(19200000-12044000z+2889787z²)/320000000+O(z⁴),
    D=3483 L⁴/10000-1371951 L⁶/16000000+O(L⁸).

The first coefficients are -T/2 and -3T/2 with T=9/25, as PSW requires.
For the candidate universal comparison, V=perp R(n,U)U has
|V|²=729/10000 while W=perp R(n,U)n has |W|²=9/16. Thus
T|W|²/3=27/400 is neither a complete leading expression nor this sixth-order
coefficient. Reversing only a changes D4 to -567/10000, although T,|V|²,|W|²
remain identical: contractions retaining their relative orientation can matter.
In these two controls D4 happens to equal 2|V|²+<V,W>; that observation is not
a general formula proved by this review. Aligned a=0 yields D4=0 and
D6=675/4096=T|W|²/3, recovering the type of FCW restricted expression with
opposite curvature sign. The u=0 control gives p=q=1 exactly.

The incidence after s=Lx,t=Ly divided by L² is analytic and even in L; its
limit is ((y-x)²-1)/2. Its y derivative is1 at (0,1), and x derivative is1
at (2,1). Analytic implicit dependence supplies both actual branches and their
endpoint derivatives through the stated order. Nearby emissions are on the
same clocks. Positivity/future signs and small convex-neighborhood uniqueness
persist for fixed finite controls. This supplies differentiable Taylor
remainders, not merely a fit. No uniform boost range or explicit error bound.

## Checks and review limits

One independent scientific script used one geometric family, four rational
controls, sixteen finite incidence cases, SymPy exact algebra and mpmath80-digit
roots. Original incidence residuals are below1e-65, proper-clock p/q are positive,
the denominator2-p² is positive, and the computed D minus its degree6 polynomial
has finite L8-normalized limits in the displayed sequence. For the tilted
counterexample that normalized remainder approaches approximately -0.01486.
Capture returned0 in5.1s with57MiB peak RSS,2GiB virtual cap and no time cutoff.
Outputs, versions and commands are preserved. No source-first failed run or
repair occurred. Numeric checks do not prove the general invariant claim.

Actual independent axes: fresh context and independently authored argument/code;
shared model/Python/SymPy, same general endpoint-incidence method. This particular
sphere-product embedding and tilt were constructed without the parent IEC1
candidate. FCW supplied the qualitative sixth-order guess under test. No claim
of different-model review, independent formalism or human endorsement.

Smallest source-preserving repair to a universal sixth-order-only claim: admit
the quartic invariant question and at least this regular counterexample. A
general sixth-order tensor formula remains unproved here. Await exposed review.
