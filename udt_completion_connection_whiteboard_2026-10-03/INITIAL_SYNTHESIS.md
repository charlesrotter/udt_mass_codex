# CCW1 initial synthesis — invariant clocks, curvature and preparation

Candidate for fresh adversarial review. The three source-first reports were
sealed before this synthesis; parent read all three and their provisional
messages. No scientific script has run. RG remains UNADOPTED, GR FILTER ONLY.
The result is conditional diagnostics and two proposed connections, not a
native geometry selector or proof that new physics is required. Proper times
use length units c_E=1. Work order and source seals own scope/exposure.

## 1. An invariant connection between the limiting clock map and curvature

Supply FCL1's C3 Lorentz4 completion g=x^-2 b, x=Omega>0, x(p)=0, with
nonzero timelike dx at the future spacelike endpoint. Put q=b^-1(dx,dx)
and kappa=-q(p)>0. The source-owned conformal connection difference is

    C^a_bc=-x^-1(delta^a_b x_c+delta^a_c x_b-b_bc x^a).

Inserting this into Ricci (the R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y]
convention of the sources) gives

    Ric[g]=Ric[b]+2x^-1 Hess_b x
           +(x^-1 Box_b x-3x^-2 q)b,
    R[g]=x^2 R[b]+6x Box_b x-12q -> 12kappa.               (1)

The first two terms vanish by regularity on a compact neighborhood of p.
This is an identity for the supplied metric, with no field equation. Kappa
may differ at different endpoints. In FCL's normal collar b=-N^2 dx^2+h,
kappa=N_*^-2. Under x'=a x,b'=a^2 b with finite positive smooth a,
dx'=a dx at p, so kappa and N_* are invariant. The conformal residue xZ is
not invariant. Positive scalar curvature alone does not imply RG.

Now supply FCL's one finite-data free receiver approaching p and its regular
interior-emitter null family. With per-ray physical emission frequency1,

    Z=d tau/ds=1/(xB), B->B_*>0,
    dx/dtau=-x gamma/N, gamma->1, N->N_*>0.

Here s is the actual source proper time and s_* its regular limiting emission.
Combining the two exact equations and using this endpoint gives

    ds/dx=-NB/gamma,
    epsilon=s_*-s=integral_0^x NB/gamma dv,
    epsilon/x -> N_*B_*,   epsilon Z -> N_*=1/sqrt(kappa). (2)

This uses averaging of a continuous limiting integrand, not differentiation
of an uncontrolled remainder. FCL's stronger proper-time result has a finite
additive remainder. Consequently

    tau=-N_* log(epsilon/s_ref)+C+o(1),
    Z exp(-sqrt(kappa) tau)->A in(0,infinity),
    log Z/tau -> sqrt(kappa)=sqrt(R_*/12),
    epsilon Z sqrt(R_*/12)->1.                           (3)

The positive reference s_ref only makes the logarithm dimensionless; A and C
depend on origins/preparation, whereas the clock-gap residue N_* is intrinsic
to this endpoint. R_* means the actual scalar limit, not a field-law input.
No convergence of d(log Z)/dtau is asserted from the logarithmic limit alone.
No finite observation is claimed to confirm s_* or an asymptote without an
independent error/domain argument.

For the existing same-correspondence scalar clock leg, Phi_clock=-log Z,

    1+chi_clock=2/(1+Z^2),
    exp(2sqrt(kappa) tau)(1+chi_clock)->2/A^2.             (4)

This joins the conditional physical clock calculation to the existing scalar
readout, not the full completed pair plane or projective-vector norm. Neither
x nor epsilon is identified with spatial/radar distance or X_max.

### Necessary admission test and surviving adverse evidence

FCW's beta2 control has g=z^-4 eta with z=1-h eta_time and
R=36h^2 z^2->0 along its comoving future tail. Equation(1) excludes an RG
endpoint of the stated type for that SAME physical tail in any representation:
its invariant scalar limit cannot be both0 and positive. This strengthens
the earlier displayed-gauge check at exactly that curve/end; it is not a
classification of all conformal extensions or a native UDT countermodel.
Null/degenerate/less regular completions and other ends remain outside it.

The beta1 and beta2 actual comoving one-way clocks can both have Z->infinity.
For z_o=r, z_e=r+d, d=hD>0, Z=((r+d)/r)^beta. For beta1,
epsilon=h^-1 log((r+d)/d) and epsilon Z->1/h. For beta2,
epsilon=r/[hd(r+d)] and epsilon Z=(r+d)/(hdr)->infinity.
Thus mere divergent received slowing is weaker than(2). Interior deformations
preserving endpoint germs still defeat interior uniqueness. R9FST's conditional
local natural-response result still prevents using DDR alone to choose kappa
among space forms; no response E=Ric or nonzero trace condition is inserted.

## 2. A regular local signal family can be constructed

Retain RG and a receiver approaching p. For this local lemma use a C3
Lorentz extension of b to a neighborhood of p with a convex normal subneighborhood.
This technical extension is explicit: if RG is stated only one-sided without
such extendability, the lemma is conditional on it. The exterior is only a
mathematical construction, not an added physical region or boundary event.

Choose e_* in x>0 on a short past null segment from p. Choose an ordinary
timelike emitter through e_* with proper time s and a compact interval away
from x=0; it may be a local free geodesic. These are chosen query data, not
a physically selected emitter population. The null segment lies in x>0
except at p because x is temporal in the small neighborhood.

For the local world function F(s,q)=sigma_b(e(s),q), use affine span1 along
the chosen null segment. At (s_*,p),

    F_s=-b(kbar_e,u_e)=E_*>0.

The implicit-function theorem yields a unique local incidence s=s(q), with
smooth nonzero limiting null tangents. C3 metric gives a C2 geodesic flow and
local exponential map; its local inverse and squared-norm world-function
construction have the derivatives required here. Restriction to the interior
receiver curve has the regularity required by R6. FCL gives its C1 endpoint
extension r(x)=(x,y(x)), y'=O(x[1+log(x0/x)]), r'(0)=-N_* n_p.
For B0=-b(kbar_o,n_p)>0 this independently fixes the sign

    F_x=N_*B0>0, s'(0)=-N_*B0/E_*<0.

The physical affine tangent k=x^2 kbar has emission frequency
-g(k_e,u_e)=-b(kbar_e,u_e). Dividing the WHOLE ray by this positive frequency
therefore gives the finite nonzero limiting B_*=B0/E_* at reception. Thus the
constructed family satisfies FCL's ray hypotheses and gives (2). Uniqueness
is local, with no caustics in that normal neighborhood.

Quantifier: for each supplied receiver endpoint in this class, an emitter
and regular local family can be arranged. An independently prescribed remote
source need not qualify. In g=x^-2 eta, source y=0 with x_e in[0.9,1.1]
cannot send a direct future ray to a free receiver y=2: x_o=x_e-2<0.
This control has RG but lacks the particular requested source access.
Actual global source availability, later return and receiver existence remain
separate. No need for another light law is inferred from the local construction.

## 3. Why a prepared distance family needs its own theorem

In g=x^-2 eta fix emission at (x,y)=(1,0), kbar=(-1,1,0,0), omega_e=1.
For each a in(0,1), receive at q_a=(a,1-a) on a DIFFERENT free geodesic with
rapidity rho=log a at that event. Each geodesic has constant spatial momentum

    P_a=(1-a^-2)/2,
    u^x=-x sqrt(1+P_a^2 x^2), u^y=P_a x^2,
    dy/dx=-P_a x/sqrt(1+P_a^2 x^2).

At q_a, omega_o=a exp(-rho)=1 and Z=1. Each P_a is finite separately, each
receiver has a finite endpoint and satisfies FCL as x->0 along itself. Across
the population P_a->-infinity. Each extends to x=1 with finite initial data;
their initial positions tend to2 but their boosts are unbounded. The separately
differentiated proper-clock map gives

    x_e=x+y(x), s=-log x_e,
    Z=x_e/[x(sqrt(1+P_a^2 x^2)-P_a x)]=1 at q_a.

This is not FCL's accelerated-clock example and not a counterexample to
uniformly bounded preparations. It refutes only exchanging a pointwise limit
with an unrestricted receiver-population limit. FCL's bound becomes uniform
if the common collar/coefficient/initial-velocity bounds are actually supplied;
positive compact regular ray data then bound B away from zero and infinity.
A distance pole still requires deriving x_o(L) from actual incidence and
operational initial separation. Defining x=L_*-L would assume the answer.

## 4. Two candidate connections and the return decision

**A. Curvature and the received-clock asymptote.** Equations(1)-(4) give a
coordinate-independent diagnostic linking a proposed completion to the native
scalar clock leg. For a candidate geometry justified independently of RG,
compute R along the proposed end first. A zero/nonpositive/divergent/nonexistent
limit excludes this RG endpoint; a positive finite limit merely survives a
necessary test. Then test the actual clock map and signal access. The unproved
physical connection is that UDT's admitted geometry has this regular end and
that it represents the positional contribution. Adopting RG or an invariant
clock/curvature admissibility condition would be an explicit NEW UNADOPTED
physical proposal; neither is established by this whiteboard or equivalent
to the other here. No weakest-possible-premise claim is made.

**B. Prepared finite separation to the asymptotic comparison.** A specific
successor can fix ordinary freely falling clocks by a stated initial geometric
preparation, hold emitted events fixed, and derive their actual incidence
x_o(L), velocity bounds and available domains. This tests whether a candidate
geometry produces the intended distance-shaped observable with SR/GR motion
included. No new physical law is needed to pose that conditional experiment.
Physical use still requires native geometry and an appropriate preparation.
The population control above is a mandatory adverse check; local/late matching
or inverse-map reciprocity cannot bypass it. Echo availability is a separate test.

The parent recommends B as the next bounded mathematical test IF Charles wants
to continue evaluating RG; it addresses the unresolved distance quantifier
instead of repeating the single-receiver limit. A remains a necessary native-
admission diagnostic, not an automatic selector. This is a recommendation only,
not a consensus to adopt RG and not successor execution. No contributor found
a reviewed native implication supplying RG; the inspected routes leave that
specific physical join open without proving complete-postulate insufficiency.

SGE1 attribution remains essential: operationally matched (g,Q)=(g0,Q0) gives
D_pos=0 even if both have this pole. For matched emitter gaps epsilon in two
RG comparisons, (2) gives D_pos->log(N_*/N0_*), but the matching is extra query
information and a nonzero contrast still needs physical attribution. Universal
law does not require equal outcomes for different velocities/gravity. Separate
future one-way asymptotes do not guarantee an asymptotic immediate echo.

No-change option: keep these conditional diagnostics and leave RG unadopted.
No native scale, X_max, distance curve, field equation, empirical filter pass,
new local clock physics or scientific promotion follows. Fresh review, finite
exact controls and central descendant/integration checks precede the lay return.
