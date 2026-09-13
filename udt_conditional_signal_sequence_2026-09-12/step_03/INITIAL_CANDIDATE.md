# CSS3 — repeated free signals at fixed observer worldlines

INITIAL CONDITIONAL CANDIDATE, UNREVIEWED, UNPROMOTED. Before numerical outcomes
or evolving-reviewer disclosure. Reuse the entire G394/NE1 geometry and G348
screen theorem; NCR1/NTB1 remain explicitly conditional UNPROMOTED dependencies.
Original sources and current FILTER ONLY authority control every inherited label.

## Metric and prescribed protocol

Use g=L² g_tilde with L,c_E>0 supplied and

    g_tilde=N²(-dt²+dxi²)+b_y²dy²+b_z²dz²,
    b_y²=t exp(P), b_z²=t exp(-P), P=epsilon F(t)cos(3xi/4),
    N=exp(lambda/4)t^(-1/4), F''+F'/t+(3/4)²F=0,
    F(1)=0,F'(1)=3/2,
    lambda=4log(3/4)+epsilon²[L_F(t)+t F F' cos(3xi/2)/2],
    L_F=t²(F'²+(3/4)²F²)/2+t F F'/2-9/8.                 (1)

The complete metric/data are G394's supplied exact conditional development,
not a newly selected response law. t is marked orbit area, not proper time.
All calculations below first use g_tilde; physical lengths multiply by L,
proper times by L/c_E and geometric areas by L². No absolute size is selected.

Prescribe two distinct fixed spatial labels x_A,x_B in a chosen covering lift,
and areal observer worldlines U_A,U_B. Unit observers for g_tilde are N^-1∂t.
Define dimensionless proper clock readings, with supplied origins at t=1,

    sigma_i(t)=integral_1^t N(u,xi_i)du, i=A,B.            (2)

N>0 makes each clock strictly increasing. Prescribed emission readings s give
t_e=sigma_A^-1(s). The chosen source schedule is the SAME proper-clock schedule
in each comparison geometry; the coordinate emission time is allowed to change.
Fixed clock origins are supplied; interval/slopes do not depend on additive origins.

Conditional faux-light: distinguishable probes follow future null geodesics,
with proper-clock tags and local sky readout; backreaction is neglected. Neither
observers nor signals are selected by UDT; no physical energy or EM law follows.
Choose a regular path branch between the worldlines. Do not move B to the endpoint
of a ray whose initial direction was independently frozen.

## Endpoint, clock and beam equations

Let ell=diag(N,b_y,b_z), A=diag(1,N²/b_y²,N²/b_z²) and

    h=sqrt(p^T A p), x'=h_p, p'=-h_x,
    omega=h/N=|ell^-1 p|.                                (3)

Primes denote coordinate t, not physical evolution of a signal field. These
are exact null-geodesic Hamilton equations in the FULL metric; the profile and
lapse are not linearized. At emission choose a unit local sky vector s_e and
p_e=ell_e s_e, fixing the arbitrary affine scale to omega_e=1. Let M be the
six-dimensional canonical first variation, initialized at I at t_e; NTB1's
complete Hessian formula is reused with the actual lower endpoint t_e.

The boundary equations are

    x(t_o;t_e,s_e)=x_B, t_o>t_e.                           (4)

Two sky coordinates and t_o are the three unknowns. With oriented orthonormal
source screen E_e perpendicular to s_e, K=M_xp, v_o=x'(t_o), the local endpoint
Jacobian is

    J_end=[K ell_e E_e | v_o].                            (5)

The first two columns use infinitesimal unit-sky components; a numerical sky
chart must include its own coordinate derivative. Assume det J_end!=0 on the
selected branch. The implicit function theorem gives local smooth dependence
of the arrival/launch-direction map on emission time and supplied data, not
global uniqueness, generic reach or a multiple-image classification.

Put X=ell_o K ell_e E_e, s_o=ell_o^-1 p_o/omega_o and choose the oriented
target screen E_o. The two-dimensional geometric beam map and forward area are

    D=E_o^T X, A_eo=|det D|, widths=singular_values(D).     (6)

These are per unit infinitesimal source solid angle; physical area is L² A_eo.
The source normalization/ell_e depend on the ACTUAL t_e. NTB1's source-t=1
shortcut ell_e=(3/4,1,1) must not be reused at later emission. Fixed-t target
variations differ from affine-endpoint Jacobi fields by a null multiple, removed
by G348's quotient screen. The full finite ray is evolved; the beam is its
exact infinitesimal derivative, not a finite bundle or brightness calculation.

The fixed-worldline gate and beam rank coincide in this declared setting:

    det J_end=det D/t_o,                                  (7)

using the same screen orientation. Indeed ell_o v_o=N_o s_o, det ell_o=N_o t_o,
and det[X_1,X_2,N_o s_o]=N_o det D. Therefore a nonzero screen determinant gives
the needed local endpoint regularity. This is a local rank statement, not a
universal nonfocusing theorem. Zero sampled determinant would require a diagnostic,
and positive finite samples do not prove absence of intermediate/later conjugacy.

G220's regular null correspondence gives the actual proper-clock slope

    R(s)=d sigma_B(t_o(s))/ds=omega_e/omega_o=1/omega_o>0,
    dt_o/dt_e=N_e/(N_o omega_o), delta=-log R.             (8)

This compares physically supplied observers and paths; it is not a preferred-frame
postulate. Compatible chi=tanh(delta) retains G176's WORKING clock-leg scope,
and does not reconstruct the full native pair or event/path assembly.

For a separate analytic derivative check, at fixed source sky define V_e as the
six-dimensional Hamiltonian vector field and

    w_e=(0,ell'_e s_e)-V_e,
    J_end (dtheta_e/dt_e,dt_o/dt_e)^T = -[M w_e]_x.        (9)

This is differentiation of a nonautonomous flow with a changing initial time.
The metric derivatives are

    (log ell)'=(-1/(4t)+t(P_t²+P_xi²)/4,
                1/(2t)+P_t/2,1/(2t)-P_t/2).             (10)

Dropping the -V_e term or freezing source ell_e changes the endpoint derivative.
Equations (8),(9), independently varied emission times and original-geodesic
replay offer different checks; the constructed Hamiltonian null identity alone
would be circular validation of the geodesic integration.

## Exact axial control for arbitrary emission time

For x_A=(xi_A,0,0), x_B=(xi_A+d,0,0), d>0 on the supplied lift, the positive
axial branch is exactly xi=xi_A+t-t_e, t_o=t_e+d, p_xi=N_e, p_y=p_z=0.
The clock ratio is N_o/N_e. Its independent screen widths are

    D_j=b_j(t_o)b_j(t_e)/N_e
          * integral_te^to N(u,xi_A+u-t_e)²/b_j(u,xi_A+u-t_e)² du,
    j=y,z.                                               (11)

Every factor is positive on a finite regular slab, so both widths are positive
for all such t_e,d,epsilon. G415/NTB1 own the underlying axial screen construction;
this changes its lower endpoint and fixed-receiver interpretation, not the
previous asymptotic theorem. Direction is constant on this control, so generic
directional drift must be assessed on the nonaxial endpoint examples separately.

## Bounded comparisons and maximum conclusion

Numerical examples will use the same spatial endpoints and same source proper
clock readings in each amplitude, solving (4) rather than moving the detector.
Record arrival clock, initial/final skies, R, both widths, area and regularity
checks together. Exact/generic signs or monotonicity are not prescribed.

A frozen-at-emission metric g_tilde(t_e,x), retaining its spatial dependence,
is a separately labeled stationary diagnostic for each pulse. Its null boundary
problem may be compared with the full flight; it is not a single competing
history across all emission times or an asserted G394/Ricci-flat solution.
Coordinate-flight contrasts carry the stated marking; local angles and screen
maps are read with each metric's own endpoint tetrad. Source/receiver clock-history
matching must not be silently copied between the full and frozen controls.

Return an exact endpoint/clock/beam contract plus finite controlled realizations
or diagnostic failure, not a general reception theorem, finite-image or flux law,
absolute calibration, native light/response selection, stability, cosmological
history or observational constraint. Unknown branches remain unknown.
