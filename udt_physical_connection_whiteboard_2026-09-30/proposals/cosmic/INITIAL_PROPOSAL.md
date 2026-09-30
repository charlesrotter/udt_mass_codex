# PCW1 cosmic lane: radiation-defined comparison clocks

**UNADOPTED PHYSICAL-IDENTIFICATION PROPOSAL; author candidate, not review or
native derivation. Secondary lead: select/constrain the comparison congruence,
not a response law.** Frozen initial construction, 2026-09-30.

Parent startup is attributed: synchronized `grok`, HEAD
`ef00adf90d0389711289e4baed38bf00a047fd6d`, prior full406 audit and baseline
development validation passed; 52 unrelated/protected names were preserved.
This separate proposing context independently checked branch/HEAD and the then
clean tracked status, read AGENTS/WORK_ORDER and relevant sources. It did not
resynchronize, rerun full startup, inspect protected payloads, or independently
attest the parent's audit. Same inherited model; no different-model independence.

## Actual proposed connection

Could a freely propagating background radiation population determine which
ordinary clock flow enters a cosmic UDT comparison? Propose the following
**additional, free-and-explored physical identification**, restricted to a smooth
open region of one Lorentz4 geometry, signature −+++ and c_E=1:

1. A nonzero conventional massless distribution on the future null shell obeys
   collisionless Liouville transport `L[f]=0` along affine metric null geodesics.
2. For one smooth future unit congruence U, it has a common spectral shape
   `f(x,k)=F(omega/Theta(x))`, `omega=−g(U,k)>0`, `Theta>0`, isotropic in ALL
   directions throughout the region. F is smooth, with nonzero derivative on
   an open frequency interval, and finite positive radiation energy moment.
3. The bulk physical comparison clocks follow that radiation-isotropy U;
   peculiar clock motion would require its own measured assignment.

These are imported kinetic/physical-population assumptions, not consequences
of the scalar kernel, DDR, ordinary clocks, or measured CMB near-isotropy here.
Theta is a spectral frequency scale; no Planck spectrum, temperature-energy
law, photon thermodynamics, emission origin or radiation source equation is
assumed. All-observer isotropy is a strong additional commitment. The finite
positive isotropic moment gives a unique timelike rest eigenvector, so a
**supplied actual distribution** can identify U. It does not predict that
distribution. No universal preferred spatial center is introduced.

## Relationship and clock consequence

Let `beta=U/Theta`. Direct Liouville differentiation gives

    L[f] = −F'(omega/Theta) k^a k^b nabla_(a beta_b).

All-direction vanishing on a nonconstant spectral interval forces

    nabla_(a beta_b) = psi g_ab.                           (1)

This uses the null-quadratic-form lemma already proved in G402/NCI1, not a new
geometric theorem. With H=div(U)/3, acceleration a, spatial derivative D and
shear sigma, its projections give

    sigma=0,   a=−D log Theta,   H=−U(log Theta).           (2)

Consequently `omega/Theta` is conserved on each regular free null segment.
FSL1 then gives the actual received-tick ratio

    Z=omega_e/omega_o=Theta_e/Theta_o,
    Phi_clock=−log Z=log Theta_o−log Theta_e.              (3)

This proposes population/metric compatibility before calculating clocks; it
does not prescribe Theta(distance) or attach a second redshift function. A
global extension requires a globally smooth positive Theta and valid population,
not merely local integrability. No full pair/frame/screen assembly follows.

The classical isotropic-radiation/conformal-Killing connection is stated in
[Clarkson–Barrett, Theorem 1](https://arxiv.org/pdf/gr-qc/9906097).
Their stronger FLRW conclusions require further matter/dynamical hypotheses;
those are not imported. The exact proposal is not a controlled approximation
to an observed nearly isotropic sky. Small angular anisotropy alone does not
bound all geometric anisotropy; explicit conventional counterexamples exist in
[Nilsson et al.](https://arxiv.org/abs/astro-ph/9904252).

## Closest work and precise novelty ceiling

[G402/NCI1](../../../udt_null_clock_depth_integrability_assessment_2026-09-10/INITIAL_CANDIDATE.md)
already owns the exact endpoint-scalar/conformal-Killing class, with current
banked conditional scope supplied by the registry. [CGW1](../../../udt_common_geometry_whiteboard_2026-09-28/REVIEWED_RESULT.md)
already explores that class and expanding comparisons. Equations (1)–(3) add
**no new geometric restriction beyond G402 for supplied U**. The new proposal,
relative to these inspected sources, is to identify that U and scalar with an
actual collisionless radiation distribution. It is neither new mathematics nor
a literature novelty claim.

[SGE1](../../../udt_shared_geometry_extension_2026-09-29/REVIEWED_RESULT.md)
leaves its intermediate U auxiliary; this proposal makes one population-defined
U physically load-bearing. [FSL1](../../../udt_finite_separation_law_2026-09-28/REVIEWED_RESULT.md)
and [LKT1](../../../udt_lorentz_kernel_transport_2026-09-29/REVIEWED_RESULT.md)
already provide clock transport, not this identification.
[ICN1](../../../udt_interframe_clock_network_2026-09-28/REVIEWED_RESULT.md)
and [MGC1](../../../udt_machian_global_clock_feasibility_2026-09-28/REVIEWED_RESULT.md)
already separate timing/scale calibration from geometry selection. This lead
does not improve their scale conclusion: c_E and G_obs select no intrinsic
length; an independently measured spectral scale adds a datum, not a derived
cosmic scale. X_max remains untouched and open.

## Decisive small calculation and strongest degeneracy

The first calculation should ask whether this relation provides more than an
ordinary evolving conformal clock sector. In the additional freefall sector,
`a=0` makes `D Theta=0`. Where `U(Theta)≠0`, U is hypersurface orthogonal;
equations (2) locally give a warped product `−dt²+A²(t)h_ij(x)dx^i dx^j`.
Neither A(t) nor h is selected without further physics. Constant-curvature
spatial slices, Friedmann dynamics and Hubble expansion are not adopted as UDT.

An exact supplied control, already checked in this package, is

    g_kappa = −dt²+A²(t)[dx²+dy²+exp(2 kappa x)dz²],
    U=partial_t,   Theta=1/A(t),   beta=A(t)partial_t,
    R=6 A''/A+6(A'/A)²−2 kappa²/A².

A is any smooth positive function; kappa is any real supplied parameter.
All members obey (1), have geodesic U and zero shear. For fixed-x clocks joined
by the regular y=z=0 radial ray, `dx/dt=1/A`, so matched coordinate separation
and emission proper time give the same arrival maps and `Z=A_o/A_e` for every
kappa, while scalar curvature differs. The ray is affine with
`k=(1/A,1/A²,0,0)`. These are metric controls, not native-admitted solutions;
curvature freedom is not a theorem of UDT underdetermination.

The author symbolic check passed in 0.34 seconds, under 512 MiB/60 seconds;
see [plan](CHECK_PLAN.md), [code](checks/check_geometry.py),
[output](checks/geometry.stdout) and [capture](checks/geometry.json).
Its purpose is to expose residual freedom, not to confirm the proposed physics.

**Ranking/stop:** retain as a secondary clock-population identification or
consistency test. It cannot presently distinguish an additional positional
effect from ordinary expansion-like evolution, select a response, predict CMB
spectrum/acoustic features, or supply the requested distance law. For any later
candidate metric/population, compute the original Liouville residual and (1)
before reading out Z; incompatibility rejects this exact identification, not
UDT. With no adoption, the current open assignment remains unchanged. Any
broader campaign must first name the independently supplied population and the
extra relation that could select A or h, or return this degeneracy as the stop.
