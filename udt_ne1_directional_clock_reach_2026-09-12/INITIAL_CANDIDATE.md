# NCR1 initial candidate — finite tilts change the clock-growth regime

2026-09-12. UNPROMOTED, adversarial review PENDING. Parent derived the
argument below from the supplied metric after the question freeze, before
new numerical outcomes or reviewer scientific disclosure. Standard metric
Hamiltonian and elementary differential-inequality methods are used; the
geometry and its Bessel estimates are reused from G394, not rediscovered.
The entire G415 scope and current G312 FILTER ONLY qualification remain.

## 1. Exact comparison and geodesic reduction

Use G394/G415's complete metric

    g=N^2(-dt^2+dξ^2)+t exp(P)dy^2+t exp(-P)dz^2,
    a=log N=λ/4-log(t)/4, P=εF(t)cos(kξ), k=3/4,
    λ_t=t(P_t^2+P_ξ^2), λ_ξ=2tP_tP_ξ.                 (1)

All explicit F,λ data and normalization are the source formulas, not free
new functions. Each fixed finite real ε is allowed; no expansion in ε is
made. Take t_e=1, a supplied source label ξ_e and unit source frequency in
the areal observer n=N^-1∂t. At this slice N_e=3/4 and P_e=0 for every ε.
Specify the same unit source-sky components in the ε and ε=0 geometries:

    (μ,ρ cosψ,ρ sinψ), μ^2+ρ^2=1, ρ>=0.

Both signs of μ and both/mixed transverse directions are included. The
longitudinal coordinate lift is evolved, not imposed to stay ξ_e±(t-1).
Compare at equal marked reception t>1. Receiver labels can differ between
geometries; this is not a fixed receiver or fixed apparatus comparison.
R=ω_e/ω_o is the geometric contraction ratio. A clock-query interpretation
requires a regular G220 branch; no off-axis absence of conjugacy is assumed.

The y,z translation symmetries give conserved covariant momenta

    p_y=ρ cosψ, p_z=ρ sinψ, p_ξ(1)=(3/4)μ.

The null Hamiltonian and positive reduced Hamiltonian are

    H_4=(-p_t^2+p_ξ^2)/(2N^2)+W/2=0,
    W=(p_y^2 exp(-P)+p_z^2 exp(P))/t,
    h=-p_t=sqrt(p_ξ^2+N^2 W), ω=h/N.                  (2)

For ρ>0 write B=N sqrt(W), b=log B, v=p_ξ/h and η=atanh(v).
Exact Hamilton equations in the marked parameter t give

    ξ'=v=tanh η, p_ξ'=-B^2 b_ξ/h,
    h'/h=(1-v^2)b_t,
    η'=-b_ξ-v b_t,
    ω=sqrt(W)cosh η, R=1/ω.                          (3)

Primes in (3) are total t derivatives; b_t,b_ξ are partial derivatives.
In particular h' is the partial-time Hamiltonian derivative along its
Hamiltonian flow. These equations allow v to reverse sign. They are not
a linearization in angle or amplitude. At ρ=0 the exact separate solution
is G415's ξ'=sign μ, p_ξ constant, R=N/N_e.

Put M=tW and r=(p_z^2 exp(P)-p_y^2 exp(-P))/M. Then |r|<=1 and

    b_t=a_t-1/(2t)+(r/2)P_t,
    b_ξ=a_ξ+(r/2)P_ξ.                                (4)

For ρ>0 all coefficients in (3) are bounded on every compact positive-t
slab, uniformly in ξ and ψ. Since |η'|<=|b_t|+|b_ξ| and |ξ'|<=1,
the initial-value solution extends through every finite future t slab.
This proves availability of the marked-parameter ray for all t>=1;
it does not assert affine completeness, maximal spacetime extension,
absence of conjugacy or any boundary statement at t=0.

The exact zero-amplitude comparison has constant covariant momenta:

    ω_0(t)=sqrt(μ^2 t^(1/2)+ρ^2/t), R_0=1/ω_0.        (5)

This follows directly from (2), N_0=(3/4)t^-1/4 and P_0=0; it is
the same-direction background, not the axial R_0 substituted at finite tilt.

## 2. Exact finite-time upper bound and necessary angular narrowing

Equation (2) gives ω>=sqrt(W)>=ρ exp(-|P|/2)/sqrt(t). Therefore, for
every t>1 and ρ>0, independently of any late-time ray estimate,

    R/R_0 <= exp(|εF(t)|/2) sqrt(1+t^(3/2) μ^2/ρ^2).  (6)

For any fixed finite tilt this excludes a positive exponential marked-time
growth rate of the contrast. It alone does not prove growth or a lower bound.

For μ≠0 compare with the axial ray of sign μ from the same ξ_e. Denote its
G415 contrast C_ax(t); for fixed ε≠0, C_ax=Theta(exp(βt)), β=ε^2σ/4>0.
If C=R/R_0 >= q C_ax for a supplied fixed fraction q>0, (6) requires

    ρ/|μ| <= t^(3/4)/sqrt(q^2 C_ax(t)^2 exp(-|εF(t)|)-1)
             = O(t^(3/4)exp(-βt)),                   (7)

whenever the denominator is positive. Thus a cone that retains a fixed
fraction of axial contrast must narrow at least as required by this upper
bound. Equation (7) is NECESSARY only: no sufficient cone width, exact
transition time or uniform joint angle/time asymptotic is claimed.

## 3. Bounded hyperbolic direction parameter off axis

G394's uniform large-positive-t Bessel bounds are

    F=D t^-1/2 cos(kt-δ)+O(t^-3/2),
    F'=-kD t^-1/2 sin(kt-δ)+O(t^-3/2), k^2D^2=2σ>0.

Using (1) and (4), at fixed ε≠0, uniformly in ξ and transverse mixture ψ,

    b_t=β[1-cos U cos V]+e_t,
    b_ξ=β sin U sin V+e_ξ,
    U=2kt-2δ, V=2kξ, |e_t|+|e_ξ|=O(t^-1/2).          (8)

This is a controlled late-t coefficient estimate of the exact equations,
not a replacement evolution law. The constants depend on fixed ε and the
supplied data. The |r|<=1 bound makes them independent of the nonzero
momentum magnitude and its transverse mixture.

Here is an explicit bounded-excursion argument. Choose T_* finite so each
|e_t|,|e_ξ|<=β/64 thereafter, and put v_*=7/8, η_*=atanh(7/8),
L=2π/k. On an interval with η>=η_* one has

    η'=-(b_t+b_ξ)+(1-v)b_t
       <=-β[1-cos(U+V)]+β/3.                         (9)

Indeed b_t<=2β+β/64 and the error/correction is at most
2β/64+(1/8)(2β+β/64)=145β/512<β/3.
Along such an interval, Φ=U+V satisfies
15k/4<=Φ'=2k(1+v)<=4k. Any interval of length L therefore
traverses at least two complete phase periods. Since 1-cosΦ>=0,

    integral_interval (1-cosΦ)dt >= (1/(4k))4π=π/k,
    η(t+L)-η(t) <= -βπ/(3k).                         (10)

For η<=-η_*, the same argument applies to -η with Φ=U-V and
Φ'=2k(1-v). Also |η'|<=3β+2β/64<4β everywhere after T_*.
Each excursion beyond either threshold can rise by at most4βL during
its first L interval, and each further full interval entirely outside
the threshold decreases its magnitude by (10). Thus

    |η(t)| <= max(|η(T_*)|,η_*)+4βL, t>=T_*.          (11)

Earlier finite times are bounded by (3). The bound is uniform on any
compact initial-direction set with ρ>=ρ_min>0, all source phases and
transverse mixtures, at a fixed nonzero ε. It is not uniform as ρ_min→0
or ε→0. The chosen 7/8,1/64,L are proof controls, not physical constants.

## 4. What replaces the axial exponential result

For every fixed ε≠0 and every fixed nonaxial initial direction ρ>0,
M/ρ^2 tends uniformly to1 because P→0. Equations (3)/(11) give

    ω=Theta(t^-1/2), R=Theta(t^1/2).                   (12)

If also μ≠0, (5) implies

    C=R/R_0=Theta(t^3/4),
    lim log(C)/log(t)=3/4, lim log(C)/t=0.             (13)

Thus an accumulated clock contrast survives throughout every fixed oblique
direction in this class, with a different growth order from the exactly
axial rays. Both initial signs, both transverse axes and their mixtures
are included. Constants can be chosen uniformly on compact sky sets away
from both the axes and μ=0. No limiting prefactor, monotonicity, onset time
or uniform angle/amplitude/infinite-time limit is asserted.

At μ=0, R_0=sqrt(t) and (12) yields only C=Theta(1). There is an exact
surviving exceptional control: choose ξ_e=0 and μ=0. Then P_ξ=λ_ξ=0
on ξ=0 for all t, so ξ remains0 and η remains0. For any ψ,

    C=[cos^2ψ exp(-εF(t))+sin^2ψ exp(εF(t))]^-1/2 →1.  (14)

Consequently no universal persistent contrast away from1 is proved for
the entire sky. Finite-time signs can differ; e.g. ψ=0 gives exp(εF/2),
which follows the changing sign of F. For other equatorial source phases
the bounded result is retained without an asserted universal limit.

At exactly ρ=0, G415's positive exponential rate β is unchanged. At each
fixed finite reception, the original Hamiltonian equations depend smoothly
on the initial direction, so taking the direction to the axis recovers
G415. The fixed-nonzero-tilt and infinite-time conclusions therefore do
not commute with simply imposing the exactly axial trajectory.

## 5. Scope, credit and evidence ceiling

New content is the finite-tilt bound, the bounded-excursion argument and
the resulting directional growth classification within the supplied NE1
family and declared comparison. The metric, source Bessel estimates,
axial result and generic clock-query interpretation remain prior results.
Current G312 membership is not repaired; no equation or physical choice is
adopted. Complete pair-kernel assembly and physical identification remain open.

This is not a beam/focusing result, an observational redshift prediction,
a preferred geometry, a fixed-apparatus experiment, a stability theorem,
or a result about all UDT solutions. Finite floating-point checks support
implementation and finite comparisons; the arguments above, if they survive
review, own the asymptotic statements. No interval/formal certification,
physical light, source/action/carrier, absolute scale or canon follows.
