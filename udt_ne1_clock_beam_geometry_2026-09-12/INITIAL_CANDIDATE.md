# NCB1 initial candidate — clocks and beams in the exact fading-ripple family

2026-09-12. UNPROMOTED; adversarial review PENDING. Analytic exploration
preceded this freeze; no reviewer findings or new numerical outcomes were
received. This is an explicit readout extension of G394, not a new spacetime
construction, governing equation, general optical theorem or physical model.

## 1. Supplied geometry, observers and comparisons

Use the ENTIRE G394/NE1 metric and reviewed clarification, with current G312
GR FILTER ONLY authority qualifying historical equation-ownership wording:

    g = N²(-dt²+dξ²) + b_y² dy² + b_z² dz²,
    N = exp(λ/4)t^(-1/4), b_y = sqrt(t) exp(P/2),
    b_z = sqrt(t) exp(-P/2),   t>0,
    P = ε F(t) cos(kξ), k=3/4, λ0=4 log(3/4),
    λ = λ0 + ε²[L(t)+t F(t)F'(t) cos(2kξ)/2],
    L = t²(F'²+k²F²)/2+tFF'/2-9/8,
    F''+F'/t+k²F=0, F(1)=0, F'(1)=3/2.                  (1)

The positive-time, compact marked polarized family and its complete initial
datum are supplied. Every finite real ε is allowed. Its Ric=0 property is
already G394's conditional result, not a native response law established
here. All formulas retain the exact quadratic λ response in the exponential.
No small-amplitude truncation is used.

The endpoint observers are n=N^(-1)∂t at fixed spatial labels. They generally
accelerate. Take a longitudinal path lift with s=+1 or -1:

    ξ(t)=ξ_e+s(t-t_e), y=y_e, z=z_e; 0<t_e<t_o<∞.        (2)

The supplied ξ period is 8π/3; lifts/windings remain distinct. No earliest
arrival, population or sum of paths is selected. The two unit screen fields
are E_y=b_y^(-1)∂y, E_z=b_z^(-1)∂z. Compare ε and ε=0 at equal supplied
marked orbit areas t_e,t_o, same ξ_e,s and path lift. These choices are
geometric once the marking is supplied; they do not establish an unmarked
all-isometry comparison, preferred observer or physical baseline.

We distinguish long reception from one source (t_e=1,t_o→∞) and a fixed
marked path of length d>0 repeated at late emission (t_o=t_e+d,t_e→∞).
In the latter, the spatial coordinate lift and areal-time increment are
fixed, not proper path length, proper duration or apparatus size.

## 2. Exact clock comparison and a sign statement

Write a=log N and D_s=∂t+s∂ξ along (2). The affine null tangent is

    K = C N^(-2)(∂t+s∂ξ), C>0,
    dv/dt = N²/C, ω=-g(K,n)=C/N.                       (3)

The base conformal Christoffels give ∇_K K=0; transverse momenta vanish
and the other geodesic equations remain zero. Both screen fields are
parallel along K (in fact as vectors, not just quotient classes).

For a fixed receiver-label/lift branch, t_o=t_e+d and dt_o/dt_e=1. Thus
the proper clock slope agrees with the metric frequency ratio of G220:

    R := dτ_o/dτ_e = ω_e/ω_o = N_o/N_e,
    R0=(t_e/t_o)^(1/4),
    R/R0 = exp[(λ_o-λ_e)/4].                            (4)

This is a regular supplied null-query clock comparison. ω is an affine
metric contraction, not an identified photon energy. R is not a complete
pair plane, and no universal physical null protocol or kernel assembly is
derived. The ratio reverses on mathematical endpoint exchange; a later
causal return is a different leg and is not that inverse.

The original NE1 constraints give the useful exact identity

    D_s λ = t(P_t+sP_ξ)²,
    log(R/R0)=1/4 ∫[t_e,t_o] u(D_s P)² du ≥ 0.          (5)

For ε≠0 this is strictly positive on every nonempty finite leg. To see
strictness, zero integral would force D_sP≡0 on an interval. Analyticity
extends this constant-along-ray identity over t>0. G394's uniform P→0 then
makes that constant zero. But F(t)cos(kξ_e+sk(t-t_e)) cannot vanish on all
t>0: F is nonzero on some open interval and the cosine is not identically
zero on any open interval. This is a contradiction. At ε=0, equality holds.
R/R0>1 does not imply R>1 on every finite leg: the background ratio is <1.

## 3. Exact full infinitesimal screen map

Put C=N_e, so ω_e=1; this is an affine normalization, not a radiation law.
For i=y,z define positive integrals along (2):

    I_i(t_o,t_e)=∫[t_e,t_o] N(u,ξ(u))²/b_i(u,ξ(u))² du,
    D_i = b_i(e)b_i(o) I_i/N_e,
    D = diag(D_y,D_z).                                  (6)

D maps unit source-sky tangent variations to target quotient separation.
Both dimensions are retained. Conserved transverse covariant momenta p_i
give dy^i/dt=p_i N²/(C b_i²). At the longitudinal direction,
δp_i=b_i(e)δθ_i for ω_e=1. The base trajectory's first variation vanishes
to this order because its transverse-momentum dependence is quadratic.
Equivalently any affine-endpoint longitudinal displacement has zero screen
projection. This proves (6) as the fixed-affine screen Jacobi map.

There is also a direct metric-curvature check, independent of defining a
tide from the proposed solution. Let q_i=log b_i and use a prime for D_s
along the central ray. Levi-Civita/Riemann calculation in the original
diagonal metric gives the parallel-screen tide

    T_i = -C² exp(-4a)[q_i''+(q_i')²-2a'q_i'],
    T_yz=0.                                            (7)

Here the convention is G348's D_v²X+T X=0. The sum of the square brackets
is (D_sP)²/2-(D_sλ)/(2t), hence trace T=0 on the supplied NE1 solution.
Differentiating (6) with d/dv=C exp(-2a)D_s gives

    D_v² D_i + T_i D_i = 0,
    D_i(e)=0, (D_v D_i)(e)=1.                           (8)

These are the original metric Jacobi equations and vertex normalization;
the trace condition alone would not check the individual tides or maps.

Every b_i,N is positive and finite on each regular finite leg, and I_i>0.
Therefore D_y,D_z>0: no noncoincident conjugate endpoint occurs on these
longitudinal rays, for any finite amplitude. This does not exclude quotient
cut ties, other null directions' caustics, or finite-wavefront overlap.

The directional infinitesimal area is

    A_forward=D_y D_z=t_e t_o I_y I_z/N_e²,
    A_reverse=t_e t_o I_y I_z/N_o²,
    A_forward/A_reverse=R².                             (9)

The second expression is source-normalized from the other endpoint on the
same unoriented segment. This reproduces G348 reciprocity in this family;
reciprocity itself is REUSED, not newly discovered. For arbitrary C, the
unit-affine-slope Jacobi block is B_C=(N_e/C)D and ω_e=C/N_e. Thus ω_e²
|det B_C|=A_forward, explicitly independent of common affine rescaling.
No flux, luminosity, observational distance or finite physical beam follows.

## 4. Background control and long-reception asymptotics

For ε=0, N0=(3/4)t^(-1/4), b_i0=sqrt(t). Exact integration gives

    D_y0=D_z0=(3/2)t_e^(1/4)(sqrt(t_o)-sqrt(t_e)).        (10)

With T=t^(3/4), this is precisely G342's longitudinal source-normalized
Taub/Kasner result. In particular at t_e=1, A0=(9/4)(sqrt(t_o)-1)².
This limit must be recovered; it is not a new accepted-background result.

Fix ε≠0, t_e=1 and ξ_e,s. G394's accepted estimates, uniform in ξ, give

    P=O(t^(-1/2)), λ-λ0=ε²σt+O(1), σ>0.

Set α=ε²σ/2>0. Then N²=Θ(t^(-1/2)exp(αt)) and
N²/b_i²=Θ(t^(-3/2)exp(αt)). Constants can depend on the fixed amplitude
and supplied normalization but may be chosen uniformly in ξ_e,s. Positive
integration gives I_i=Θ(t_o^(-3/2)exp(αt_o)): an upper bound follows by
splitting off early times and exponential-tail bounds, and a lower bound
by integrating the final fixed positive-length subinterval. Consequently

    D_i=Θ(exp(αt_o)/t_o), A_forward=Θ(exp(2αt_o)/t_o²),
    lim [log(R/R0)/t_o] = ε²σ/4,
    lim [log(A_forward/A0)/t_o] = ε²σ.                  (11)

Thus both ratios diverge, although P fades. These are growth rates in the
marked orbit-area parameter t, NOT in source/receiver proper time or affine
distance. Bounded oscillatory factors have not been replaced by a claimed
constant prefactor. Finite numerical examples cannot establish these limits.

There is a simultaneous loss of transverse shape contrast:

    D_y/D_z → 1  (t_e=1).                               (12)

Indeed b_y(e)=b_z(e)=1 and b_y(o)/b_z(o)=exp(P_o)→1.
Writing I_y and I_z with common positive weight N²/u, their late integrands
have ratio exp(-2P)→1 uniformly. The integrals diverge, so every fixed early
contribution becomes negligible and I_y/I_z→1. This proves (12); it does
not infer vanishing instantaneous shear or tide. If t_e≠1 is held fixed,
the analogous limit is exp(P_e), not universally one. This source-shape
factor is another reason to keep the declared normalization and event.

At every fixed finite pair of endpoints ε→0 recovers (4)/(10) smoothly.
The unbounded nonzero-amplitude late-reception ratios therefore cannot be
obtained as a uniform all-time small-amplitude approximation. No generic
nonlinear instability or absolute-curvature blowup is claimed.

## 5. Fixed marked path at late emission: clock persistence

Let d=t_o-t_e>0 be fixed, retain ξ_e and s, and send t_e→∞. Write G394's
Bessel estimates as F=D_B t^(-1/2)cos(kt-δ)+O(t^(-3/2)) and
F'=-kD_B t^(-1/2)sin(kt-δ)+O(t^(-3/2)); k²D_B²=2σ.
The phase δ is fixed by the supplied F, not fitted. Along (2),

    u(D_sP)² = 2ε²σ sin²(2ku-kt_e+skξ_e-δ)+O(1/t_e)

uniformly on this fixed-length interval. Integrating (5) gives

    λ_o-λ_e = ε²σ[d - sin(2kd)/(2k)
      cos(2kt_e+2skξ_e-2δ+2kd)] + O(1/t_e).             (13)

The remainder constant depends on fixed ε,d,k. Since
d-|sin(2kd)|/(2k)>0 for d>0, the late clock contrast is bounded away from
one when ε≠0. More precisely its liminf and limsup are

    liminf R/R0 = exp{ε²σ[d-|sin(2kd)|/(2k)]/4}>1,
    limsup R/R0 = exp{ε²σ[d+|sin(2kd)|/(2k)]/4}.         (14)

The phase sweeps continuously with t_e; fixed phases attaining each cosine
extreme give the two limits. The same bounds apply to R because R0→1.
If sin(2kd)=0 the limit is exp(ε²σd/4); otherwise persistent oscillation
remains rather than a single limit. No amplitude-independent lower bound
or uniform d→0 statement is asserted; as d→0 the bound can approach one.

This prevents confusing (11) with the only kind of persistence tested.
It is still a marked-path comparison: proper baseline and proper travel
duration change with the metric. It is not a prediction for a fixed-size
laboratory instrument, cosmic Hubble curve or universal redshift mechanism.

## 6. Scope and evidence ceiling

The new content is exact NE1-specific clock/screen evaluation, positive
longitudinal Jacobi maps, and the stated persistence/shape limits. The
metric construction, Bessel estimates, background beam, generic quotient
geometry and reciprocity belong to their cited prior sources. Current
G312 membership, physical assembly, observer/path selection and identification
remain open. c_E supplies no size/wavelength; X_max, carriers, actions,
source laws, SNe data and optical transfer are unused.

Analytic arguments (1)–(14) are candidates for review. Exact algebra and
finite floating-point checks will be recorded separately. A passing source
hash or predicate count is not proof, certification or empirical evidence.
No claim about all UDT solutions, nonaxial rays, physical light or dynamics
adoption is within this result.
