# Fixed TDS1 conditional equations and data

Ric(g)=0, Lambda=0 is the supplied comparison branch, under the current
G312 GR FILTER ONLY authority. R9 does not identify its response E with Ricci.
This package releases the evolution code's spatial Killing restriction; it
does not release every initial-data, gauge, topology or physical assumption.

With signature(-+++), write C_mu=g^{ab}partial_a g_bmu
-(1/2)g^{ab}partial_mu g_ab. Pure harmonic coordinates require C_mu=0.
The reduced metric equation used here is

    W_mn = g^{ab}partial_a partial_b g_mn
         +(partial_n g^{ab})partial_a g_mb
         +(partial_m g^{ab})partial_a g_nb
         +2 Gamma^a_bn Gamma^b_am = 0.

The independent metric-jet identity is

    W_mn = -2 Ric_mn + partial_m C_n + partial_n C_m
           -2 Gamma^a_mn C_a.

Here W is this supplied reduced differential operator, not R9's response E.
The original constraints and harmonic-compatible initial data are indispensable
for the usual continuum equivalence; solving the reduced PDE numerically does
not by itself certify Ric=0. Original Ricci is checked separately from saved g.
The coefficient g^{00}<0 allows solving the reduced equation for partial_t^2 g.
All ten symmetric components evolve; the 16 stored entries retain symmetry.

On the supplied period2pi three-torus, the initial conformal metric is flat and
tau=-1. The supplied TT tensor is

    Abar=diag(2/3,-1/3,-1/3)
        +.06 cos(x+.17) diag(0,1,-1)
        +.045 cos(y+.43) diag(1,0,-1)
        +.03 cos(z-.29) (e_x tensor e_y + e_y tensor e_x).

Each mode is transverse/traceless. Solve for psi>0:

    -8 Delta psi - |Abar|^2 psi^(-7) +(2/3)tau^2 psi^5 = 0,
    gamma_ij=psi^4 delta_ij,
    K_ij=psi^(-2) Abar_ij +(tau/3)gamma_ij.

This is the existing G316 conformal construction within the conditional arena.
Constant tau and TT Abar satisfy the momentum construction. The original
Hamiltonian and momentum equations are independently reconstructed from gamma,K;
the scalar-solver residual is not substituted for that check. Three independent
mode directions and a rank-three derivative Gram exclude a common constant
coordinate translation for these data, not every possible nonlinear Killing field.

Initially lapse=1 and shift=0. With K=-1/2 L_n gamma, harmonic compatibility gives

    partial_t g_ij=-2K_ij,
    partial_t g_00=2tau,
    partial_t g_0i=gamma^{jk}(partial_j gamma_ki-1/2 partial_i gamma_jk)
                  =-2 partial_i log psi.

Lapse and shift subsequently evolve through the full metric; they are not frozen
at their initial values. Harmonic elapsed time s=t-1 is a coordinate choice.
The homogeneous control g=diag(-exp(2s),exp(-2s/3),exp(4s/3),exp(4s/3))
is exact Kasner with proper time exp(s). Flat and finite-amplitude oblique
gauge-wave metrics check the code; their symmetries are not imposed on the
three-direction data. No null curvature requirement is inferred from a test.

For supplied fixed-coordinate timelike clocks u=partial_t/sqrt(-g_00),
omega=-g(u,k). A regular affinely parametrized null ray yields
Z=omega_e/omega_o. Numerically the geodesic is reparametrized by coordinate t,
dx^i/dt=k^i/k^0 and dk^a/dt=-Gamma^a_bc k^b k^c/k^0. Proper ticking is still
computed with the metric. Receiver coordinates are the ray's computed arrival
position at the supplied final time, not a selected cosmological observer.

Provenance: UDT_DEVELOPMENT.md R9,R11,R12N; G316 EXACT_DERIVATION.md read under
udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md. Mathematical method
comparison: [Pretorius equations7–14](https://arxiv.org/html/gr-qc/0407110v2),
[harmonic evolution methods](https://arxiv.org/abs/gr-qc/0512093), and
[standard numerical controls](https://arxiv.org/abs/gr-qc/0305023). These references
are methods, not UDT premises. Independent derivation preceded saved-history
outcomes; this fixed explanatory transcription follows the checks.
