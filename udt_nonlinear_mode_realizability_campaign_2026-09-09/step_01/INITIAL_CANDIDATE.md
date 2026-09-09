# NR1 initial candidate — compact momentum obstruction

Discovery candidate, UNPROMOTED; not yet independently reviewed. 2026-09-09.
Sources: current G310/G312 adoption; G303 constraints; G324 quotient; G327 exact
first variation and reviewed limits. Baseline454bd6ff. No accepted source changed.

## Claim and quantifiers

Fix one registered compact split-lattice G324 quotient and T0>0. Let

    g0=-dT²+a(T)² dX²+b(T)²(dy²+dz²),
    a=C1 T^(-1/3), b=Cperp T^(2/3), k=2pi/LX>0.

The complete G327 real first variation has spatial transverse block
δγ_AB=2b² H_AB, other spacetime components zero, where

    H = [[f+,fx],[fx,-f+]],
    (f+,fx)=u_c(T) cos(kX)+u_s(T) sin(kX).

Each of four scalar phase/polarization amplitudes solves G327's ODE
u''+u'/T+(k/C1)²T^(2/3)u=0. Write v_c=u_c'(T0), v_s=u_s'(T0),
and u_c,u_s at T0. If this perturbation, modulo smooth periodic spacetime gauge,
is the tangent to a C2-parameter family of smooth exact S(g)=0 geometries on a
common neighborhood of the WHOLE compact slice, then necessarily

    Q := v_c · u_s - v_s · u_c = 0.                    (NR1)

No symmetry/ansatz restriction is placed on any second-order correction. The
connected scalar Lambda(epsilon), homogeneous fields and higher harmonics may
vary. Necessity is local in time but global on this supplied compact slice.
This step does NOT assert sufficiency or a complete adjoint-kernel census.

## Full momentum pairing, not a truncated metric equation

Use K_ij=-(1/2)∂T γ_ij in the G327 synchronous representative. For any exact
datum define τ=γ^ij K_ij and tensor density

    π^ij = sqrt(detγ) (K^ij-τγ^ij).

The Einstein momentum constraint D_j(K^ij-τγ^ij)=0 follows for all Lambda,
including when Lambda is supplied by the trace-free scalar constraint. On a
compact boundary-free slice, integration by parts gives, for any smooth global X,

    ∫ π^ij (L_X γ)_ij d³x = 0.

Choose the background translation X=∂X, which descends to the supplied quotient.
It need not remain a Killing field of the deformed datum. In these coordinates
L_Xγ=∂Xγ, so the exact identity is F(epsilon)=∫π_epsilon^ij ∂Xγ_epsilon,ij=0.
Expand γ=γ0+epsilon h+epsilon² q+o(epsilon²),
π=π0+epsilon π1+epsilon² π2+o(epsilon²). At the homogeneous background,
∂Xγ0=0 and π0 has constant coordinate components. Therefore

    F2 = ∫π1^ij ∂X h_ij + ∫π0^ij ∂X q_ij
       = ∫π1^ij ∂X h_ij.                            (1)

The second term vanishes by periodicity for EVERY smooth periodic q, not just
axial/tensor q. No π2 term survives. Lapse, shift and embedding corrections at
second order only change these eliminated higher-order data. This proof makes
no division by an unknown correction or use of an endpoint boundary condition.

## Evaluate the first-order datum without freezing momentum variables

Let B=b'/b=2/(3T0), τ0=-1/T0 and V0=sqrt(detγ0)=ab². Direct differentiation gives

    h_AB=2b²H,       δK_AB=-b²(Hdot+2B H),
    δsqrt(detγ)=0,   δτ=0,
    π1^AB=(V0/b²)[-Hdot+2(B+τ0)H].                (2)

The inverse-metric variations in both raised K indices and in τγ^ij are included.
Thus (1), after the total derivative tr(H H_X) integrates to zero, is

    F2=-2 V0 ∫tr(Hdot H_X)d³x
      =-2 V0 A_perp k LX (v_c·u_s-v_s·u_c).       (3)

A_perp is the positive coordinate area of the transverse lattice fundamental
cell; it is supplied quotient data, not a material wall or physical size.
The nonzero prefactor establishes NR1. For X=∂y,∂z the same pairing has zero
quadratic coefficient in this sector. This fact alone is not a classification
of every possible constraint obstruction.

## Bessel coefficients and preservation of the obstruction

With J=J0(3nu T^(4/3)/4), Y=Y0(3nu T^(4/3)/4),

    u_c=A_c J+B_c Y,  u_s=A_s J+B_s Y,
    Q=(J Y'-J'Y)(B_c·A_s-A_c·B_s),
    J Y'-J'Y=8/(3pi T).

Consequently the condition is equivalently

    A_c·B_s-A_s·B_c=0.                            (4)

The ODE gives Q'=-Q/T, so TQ is constant; the obstruction does not depend on
which positive regular reference slice is used. This is a mathematical identity
of the linear modes, not identification of physical momentum or carried content.

One excluded linear solution: plus-cosine J and plus-sine Y, other coefficients
zero; (4)=1. It remains a valid G327 linearized solution but cannot be the stated
exact-family tangent. Surviving necessary controls include a cosine-only mode,
the zero mode amplitudes, and two polarizations whose nonzero contributions to
(4) cancel. Do not exclude either G327 time branch or demand each polarization
contribution vanish separately. Actual existence for survivors is not claimed here.

## Gauge, assumptions, and exclusions

For a tangent given up to an allowed smooth periodic infinitesimal diffeomorphism,
pull an assumed exact family back by the inverse parameter-dependent flow. On a
smaller common time neighborhood of the compact slice this removes that gauge
term and gives the G327 representative, to which (1)--(3) apply. Hence an exact
family cannot be rescued by a mere change of representative. No nonperiodic
coordinate rescaling or changing the quotient class is silently counted as gauge.

C2 parameter regularity is used to take the quadratic coefficient; smoothness
and compactness justify differentiating the integral and the periodic integration
by parts. The local time interval stays away from T=0; there is no infinite-time,
endpoint-uniform, smooth stability, physical population, source, scale or canon claim.
Allowing extra FIRST-order modes changes the question and could alter the pairing;
NR1 concerns exactly the eight-real-parameter G327 tangent sector.

General mathematics is used as method. The metric equation remains conditional
on the admitted owner-provisional arena; no new law is adopted. The original
linear census is not repaired or refuted. NR1 narrows its possible nonlinear
realization on the supplied compact quotient, if the argument survives review.

## Evidence plan and history

The integrated constraint pairing and candidate algebra were explored before this
mathematical freeze. New check code differentiates the actual spatial inverse,
raised K and density, and recomputes the Fourier integral; algebraic identities
support the proof but finite checks do not prove its arbitrary-correction scope.
Three arithmetic corruptions of the candidate coefficient will be actually run.
Fresh reviewer works source-first before this candidate, then attacks the full
proof. A passing regression is not independent review or an existence theorem.
