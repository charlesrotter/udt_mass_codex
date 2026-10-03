# Source-first return: a locally symmetric quartic counterexample

Disposition before IEC candidate exposure: **VERIFIED-WITH-CAVEATS conditional
control**, not a verdict on an unseen candidate. The general claim that D always
first starts at L6 in locally symmetric Lorentz4 geometry is false. FCW1 itself
did not make that claim: its source explicitly leaves the invariant formula and
failure order outside its one family open.

## Original geometry and preparation

The supplied metric is the ultrastatic product g=-dt2+h_K on R times a
three-dimensional space form. It has nabla Riemann=0 because the product
connection preserves both factors and their constant-curvature tensors. No
field equation is imposed. For K=1 the unit-sphere embedding uses X0,ex,ey as
orthonormal ambient vectors. Its spatial geodesics and parallel transport are
the elementary great-circle expressions in SOURCE_FIRST_DESIGN. One can check
parallel transport directly: the derivative of the transported tangent is
normal to the sphere, and the perpendicular spatial tangent remains constant.
The clock curves have constant spatial speed u and constant time speed gamma,
so their proper norm is -gamma2+u2=-1 and each is a product geodesic.

U=gamma e0+u ey, m=u e0+gamma ey, n=a ex+b m,
gamma2-u2=a2+b2=1. The preparation curve has time tangent bu and spatial
tangent a ex+b gamma ey of length h=sqrt(1+b2u2), so it is a unit spacelike
geodesic orthogonal to U at the initial event. Transporting U by its exact
spatial parallel transport gives the specified B clock. Thus this is the
actual PSW preparation, not arbitrary simultaneity/comoving preparation.

For an ultrastatic product a null geodesic has constant time speed and spatial
geodesic projection with matching speed. In a sufficiently small convex tube,
the unique future direct null incidence is time difference equal to spatial
distance. Taking the embedding inner product gives the F in the design, with
positive elapsed time selecting the future root. The return uses F(r,t,L)=0
with the opposite elapsed-time sign, and separately differentiates that root.
This proves the original equation used by the script without any target D.

Signed-curvature generalization uses C_K(z)=cos(sqrt(K)z) and
S_K(z)=sin(sqrt(K)z)/sqrt(K), extended at K<=0. Their power series are entire
in K. Replace the sine products in F by K S_K S_K and cos by C_K. The scaled
F/(K L2) extends analytically through K=0. It equals ((y-x)2-1)/2 at L=0,
so both direct future roots have nonzero root derivative. The analytic implicit
function theorem yields the even expansion and its proper-time derivative
remainder for each fixed finite supplied preparation. Actual positive elapsed
time persists for small L by continuity. p,q and2-p2 remain positive there.

## Exact finite-degree result

The one independent script expands this original F through total degree8,
solves its outgoing and swapped-return branches through scaled degree6, then
forms the actual p and q. For u=3/4,gamma=5/4,a=4/5,b=3/5 it obtains

    log p = -9 K L2/50 -3711 K2 L4/80000
            -1671501 K3 L6/320000000 +O(L8),
    log q = -27 K L2/50 +27099 K2 L4/80000
            -26008083 K3 L6/320000000 +O(L8),
    D = 3483 K2 L4/10000 -1371951 K3 L6/16000000 +O(L8).

For every fixed K!=0 the nonzero positive L4 coefficient defeats universal
quartic cancellation. In particular the FCW one-family expression
T(n,n)|W|2 L6/3 cannot be the general leading D under local symmetry alone.
This witness is a conditional supplied geometry, not a native-admitted UDT
countermodel or a no-go result for UDT/ULC1/DDR.

The curvature can also be computed directly from the product formula
R(X,Y)Z=K[<Y_sp,Z_sp>X_sp-<X_sp,Z_sp>Y_sp]. With v=b ex-a m,

    T=T(n,n)=K a2u2,
    V=perp R(n,U)U=K a b u2 v,
    W=perp R(n,U)n=K a gamma u v.

The tilted values give |V|2=729K2/10000 and T|W|2/3=27K3/400.
Thus the first tidal vector also leaves the initial clock plane. The equation
2|V|2+<V,W>=3483K2/10000 happens to hold in this control; this record does
not infer a general invariant formula by fitting one control.

For the distinct orthogonal preparation b=0 with the same u,gamma, the exact
series instead gives D=675K3 L6/4096+O(L8), agreeing with T|W|2/3 there.
That is a positive sign for K>0, contrasting with FCW's dS2-times-flat control.
The u=0 static-clock control has p=q=1 and D=0 exactly. These controls make
clear that geometric restrictions, rather than numerical order extraction,
determine which coefficients can survive.

## Evidence and independence limits

SOURCE_FIRST_RESULT.json saves the exact incidence polynomials, branch
coefficients and log coefficients for three symbolic preparation families.
Sixteen90-digit original-incidence cases cover two nontrivial preparations,
both curvature signs and L=1/10,1/20,1/40,1/80. All roots obey the future
elapsed-time conditions and original F residual<1e-70. Observed error orders
for truncation through L6 range7.9735 to8.0263; this is a numerical corroboration,
not the analytic remainder proof or a certified finite-distance error bound.

Captured run exits0, stderr empty, maxRSS52232KiB,2GiB address limit,
one-BLAS-thread environment enforced by the inspected existing capture utility,
and no elapsed or CPU timeout. No implementation repair was needed.

This is a fresh separate context, independently authored calculation and
argument, sharing the parent model and Python/SymPy/mpmath tools. The existing
FCW product formula and its open scope were exposed as sources, not the IEC
candidate. The sphere-embedding technique is standard elementary geometry and
shares the broad embedding method used by FCW, but neither its incidence nor
its coefficients were reused. No different model/library, independent formal
proof assistant, general tensor calculation, empirical validation or human
physicist endorsement is claimed. Parent full406/sync/host evidence is attributed;
this scoped reviewer did not rerun all source packages or inspect protected work.

Source fidelity: preserve W4's working/posit label; do not turn W5 projective
position or W6 nonsignalling co-presence into a geometry law. ULC1's original
owner clarification permits circumstance-dependent comparisons and does not
adopt FC. The exact central PSW/FCW definitions and their reviewed controls
survive at their stated scope. A general locally symmetric calculation must
allow both V and W and cannot assume a totally geodesic clock sheet or a
velocity-preserving clock-exchange isometry without proof.
