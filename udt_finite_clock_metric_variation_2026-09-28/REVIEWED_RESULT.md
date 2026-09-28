# FCV1 — full metric variation of a finite clock comparison

**VERIFIED-WITH-CAVEATS; CONDITIONAL, UNPROMOTED.** The frozen
[initial candidate](INITIAL_CANDIDATE.md) is the controlling derivation;
[direct review](review/DIRECT_REVIEW.md) found no load-bearing defect and
required zero repairs. This summary preserves its hypotheses and scope.
The result does not identify a native field equation or promote registry grades.

## Exact conditional comparison response

Take a smooth Lorentz4 metric family, signature (-+++), h=delta g, and supplied
smooth timelike observer families with increasing labels s,t. Let W_e,W_o be
their fixed-label displacements, N_i their proper-clock rates per label and
u_i their unit tangents. Proper time uses length units, c_E=1. Require a
convex-normal neighborhood or a justified smooth nondegenerate geodesic branch,
commuting derivatives, regular future-null arrival t=A(s), A'>0 and F_t!=0.
These are supplied conditional null-clock queries, not a derived universal
physical protocol. No caustic, branch switch or global continuation is included.

For the actual received-clock ratio and its logarithm,

    Z(s)=N_o(A(s)) A'(s)/N_e(s),     D=log Z,

use the affine baseline ray x(lambda), lambda in [0,1], k=dx/dlambda and
omega_i=-g(k_i,u_i)>0. Define

    I[h] = (1/2) integral_0^1 h(k,k) d lambda,
    J = I - g(k_e,W_e) + g(k_o,W_o),
    V = delta A = J/(N_o omega_o),
    b_i = delta log N_i = -h(u_i,u_i)/2 - g(u_i,nabla_{u_i} W_i).

The full fixed-source-label response is

    Q(s) = delta D(s)
         = b_o(A)-b_e + (partial_t log N_o)(A) V + V'/A'.

Geodesic stationarity removes the interior ray-displacement term in the first
variation of the world function. It does not freeze the physical ray. The
source-label derivative of I retains the baseline ray family, and V carries
arrival-event movement. If both baseline labels are proper time along their
relevant curves, N_e=N_o=1 and this becomes

    Q = [h_e(u_e,u_e)-h_o(u_o,u_o)]/2
        -g(u_o,nabla_{u_o}W_o)+g(u_e,nabla_{u_e}W_e)
        +(1/Z) d(J/omega_o)/ds.

Normalizing at one event alone does not remove receiver-rate drift. If the
comparison is instead held at a fixed numerical source proper time, with a
declared common label origin s0, an additional event relocation gives

    delta s|tau = -integral_s0^s N_e(q)b_e(q)dq / N_e(s),
    Q|tau = Q + D'(s) delta s|tau.

When source proper-time parametrization is already carried in W_e, do not add
this relocation again. For a pure coordinate change h=L_xi g, W_i=-xi, the
integral and endpoint terms cancel, b_i=0, and V=Q=0. This covariance check
supplies no metric-only off-shell conservation law for a physical response.

## Reciprocity does not select a geometry in this calculation

The inverse of the same regular correspondence obeys
D_rev,epsilon(A_epsilon(s))=-D_epsilon(s). At the moving matched event its
variation is -Q. At a fixed receiver label t=A(s), it is instead

    Q_rev(t) = -Q(s) + D'(s)V/A'.

Composition similarly retains the intermediate argument's movement. These
relations hold for every smooth regular comparison and impose no metric field
equation. This neither discharges nor refutes owner-adopted provisional DDR:
physical stationarity of a specified response E against reciprocal shape
variations is stronger than inverse-clock algebra. The physical E remains OPEN.

## A precise failed direct identification

In a supplied flat baseline with endpoint clocks x=0,L, choose a nonnegative
nonzero smooth bump b compactly supported strictly inside (0,L). On the ray tube,

    g_epsilon = -exp[-2 epsilon t b(x)] dt^2
                +exp[2 epsilon t b(x)] dx^2 + dy^2 + dz^2.

Small epsilon on a bounded emission window admits the regular branch; smooth
cutoffs can make the change compact while preserving the tube. Its determinant
in the clock/ruler plane is exactly -1, and h=t b(x) H(u,n) is the full factor-two
G310 reciprocal tangent. Every endpoint neighborhood and metric jet is unchanged.
With B0=integral b>0 and B1=integral x b,

    I=2L(s B0+B1),     V=2(s B0+B1),     Q=2B0>0.

The direct null ODE independently yields the same first variation. Thus endpoint
geometry alone cannot determine this finite response. The polynomial controls
check the algebra only; the smooth compact-bump argument owns the endpoint-jet
claim. This is a supplied geometric witness, not a UDT-admitted cosmology.

For one fixed regular query with W=0, Q[h] has distributional support on its
compact ray, including endpoint terms. A nonzero example therefore cannot be
represented for all compact smooth h by a smooth spacetime-volume coefficient
C through integral C^{ab}h_ab dV: testing off the ray forces C=0 there, and
smoothness forces C=0 everywhere. Trace-free tests give the corresponding
contradiction for TF(C), using the nonzero trace-free witness above.

This excludes that direct identification of one measurement derivative with a
smooth local response. It does not exclude local field equations, nonlocal
observables under local dynamics, a justified local limit or reconstruction
from multiple queries. No such reconstruction, averaging measure, stationarity
principle or physical population is supplied. A new postulate has not been proved
necessary; the missing physical identification remains open.

## Evidence and limits

The author checked 29 exact identities and eight rejected wrong formulas.
A fresh separate-context reviewer reconstructed the argument before candidate
exposure and ran 30 independent controls: 23 identities and seven wrong formulas
rejected. Implementations are distinct but both use Python3.10.12/SymPy1.13.1;
no different-model, different-library, human or formal-proof review is claimed.
Later producer replay is regression only. No scientific repair was needed.
The full 406-row premise audit passed; receipts, freezes and exposure records
are retained. These checks support the scoped argument, not physical adoption.

W4/W5, G176's open full-pair assembly, the conditional null-clock interface,
DDR/G312 authority and GR-as-filter remain unchanged. There is no new dynamical
candidate on which to claim solar precision, cosmological fit, microscopic light,
matter emergence, stability, a selected scale or global/asymptotic completion.
The return is the full comparison-variation formula and the rejected direct
join above. No successor research is automatically authorized.
