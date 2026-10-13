# Independent original-coordinate numerical freeze

This freeze precedes all B scientific executions and exposure to A coefficients.
The parent approved one CPU slot. After INITIAL_APPROACH, the parent disclosed
its own proposed conformal recovery witness f=epsilon(t-1)^2/2,
g_epsilon=exp(2f)g_Kasner and its predicted initial Ricci contraction. That
deformation is therefore exposed parent work, not B's independent discovery.
Vacuum first-signal reconstruction remains independent of A's series.

## Equations

Allow the supplied diagonal metric -N(t)^2 dt^2+sum a_i(t)^2 dx_i^2.
For vacuum Kasner N=1, a_i=t^r_i. For the optional exposed deformation,
N=exp(f), a_i=exp(f)t^r_i. Spatial geodesic momenta are constant by translations.

For spacelike preparation parameter s, momenta c_i=n_i, and x_i'=c_i/a_i^2,

    t''=-(N'/N)t'^2-sum_i a_i a_i' (x_i')^2/N^2,
    (U^t)'=-(N'/N)t'U^t-sum_i a_i a_i' x_i'U^i/N^2,
    (U^i)'=-(a_i'/a_i)(t'U^i+x_i'U^t).

Initial data are t=1,t'=0,x=0,U^t=1,U^i=0. Integrate to s=L.
Receiver momenta P_i=a_i(T)^2 U^i(T), gamma=sqrt(1+sum P_i^2/a_i^2),
and dx_B^i/dt=N P_i/(a_i^2 gamma). Receiver proper normalization is
U_B^t=gamma/N, U_B^i=P_i/a_i^2.

For a null ray with constant spatial momenta q_i, W=sqrt(sum q_i^2/a_i^2),
k^t=W/N, k^i=q_i/a_i^2 and dx_ray^i/dt=N q_i/(a_i^2 W).
Solve endpoint incidence for arrival t and q direction; |q|=1 fixes its
irrelevant positive scale. Actual endpoint frequency is
omega=W gamma-sum_i q_i P_i/a_i^2. For A, P=0 and gamma=1.
p_+=W(1)/omega_B(arrival); p_-=omega_B(T)/W(arrival at A).
The independent reverse ray starts at B0, not at the outgoing reception.

Axisymmetric r_2=r_3 and spatial reflections are isometries fixing A and its
time axis. They map the whole preparation, transport, free clocks and first
null branches. Therefore a representative n=(mu,sqrt(1-mu^2),0), 0<=mu<=1,
retains the full sphere, with mean integral_0^1 dmu. This is an exact symmetry
reduction of this supplied control, not a general angular replacement.

## Planned runs and numerical decision

Initial grids: L=0.08,0.06,0.04,0.03,0.02; Gauss-Legendre angular orders24 and48;
time-integral orders32 and64. DOP853 preparation rtol2e-12/4e-14,
atol2e-14/4e-16 for baseline/fine. All computations use float64.
Roots use scipy hybr with xtol1e-11 and save actual incidence residuals.
Controls: Minkowski exponent triple zero, both principal directions, the
published FPC outgoing axis coefficient through fourth order, and full 3D
momentum/norm/orthogonality residuals. No sibling coefficient is a control.

Required numerical acceptance: all roots future, max endpoint incidence residual
<2e-12; preparation spacelike norm, clock norm and orthogonality residuals
<2e-10. Scientific signs require absolute means >50 times the maximum observed
baseline/fine discrepancy at that L and the flat mean floor. That discrepancy
is a convergence diagnostic, not a rigorous error enclosure. A finite-order
coefficient extrapolation is descriptive and cannot establish an exact coefficient.
Preserve any failures and change no tolerances without recording why.

If vacuum signs and numerical error permit, use the same original equations on
the parent's explicitly supplied conformal correction as an exposed check of
the recovery regime. Freeze its epsilon/L grid separately before execution.

Use unique TPS1 capture prefixes, one thread, 2GiB virtual memory, no timeout,
initially under five CPU-minutes of the shared20. Save JSON full angular records,
commands, versions, hashes, stdout/stderr. No GPU or physical admission claim.
