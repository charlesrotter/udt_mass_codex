# ALP1 B — angular normalization is a stronger, nonautomatic clock law

Draft conditional mathematical result, not reviewed or adopted. Analytic
discovery followed INITIAL_APPROACH. No native geometry or physical attribution
is asserted. Regional vacuum is a supplied hypothesis, not native UDT admission.

## 1. Fixed Lorentz comparison and the two endpoint spheres

Use R6/R7 and FSL1's forward convention: Lambda maps emission frame to reception
frame, Lambda l(n)=f(n)l(m), f=omega_o/omega_e=1/p, and p=Z is the reception
proper interval divided by emission proper interval. All directions in this
paragraph use ONE fixed Lambda. They are mathematical tangent skies; this is
not yet an ensemble of different finite FAC1 experiments.

For a tangent sky variation dn with n.dn=0, metricity gives
|dn|²=f²|dm|²: differentiating Lambda l(n)=f l(m), the terms containing l(m)
have zero Minkowski norm and zero inner product with dl(m). Therefore

    dOmega_m = f(n)^(-2) dOmega_n = p(n)^2 dOmega_n.

The inverse map consequently has Jacobian p(m)^(-2). For the reception sky,
write Lambda e0=(cosh rho,sinh rho e1), after rotations. R7 gives

    p(m)=cosh rho-sinh rho mu,  mu=e1.m,
    <p^-2>_m=1,
    <log p>_m=rho coth rho-1 >=0.

The last expression is0 at rho=0 by continuity, positive at nonzero rho,
and rho²/3+O(rho⁴) near0. The normalization follows either the inverse-map
Jacobian or integrating1/(cosh rho-sinh rho mu)² over mu in[-1,1]. The log
formula follows its elementary antiderivative; rho cosh rho-sinh rho has
derivative rho sinh rho>=0. Jensen also gives
<log p>_m >= -(1/2)log<p^-2>_m=0.

In contrast, on the uniform EMISSION sky, p(n)=1/f(n), so

    <log p>_n=-(rho coth rho-1).

Thus neither sign is an observer-independent sign of positional physics.
These are two uniform measures on different endpoint skies, not the same
measure carried through the aberration Jacobian. An inverse tangent map is not
FAC1's independently emitted future reverse signal.

Rotation invariance selects uniform solid angle for one local rest sphere.
It does not select a probability measure invariant under every Lorentz boost:
a finite rotation-invariant probability on S² is the normalized area measure,
and the displayed nonconstant boost Jacobian changes that measure. Observer
covariance instead carries the measure with its Jacobian. No preferred observer
does not require identical numerical means for physically changed laboratories.

## 2. A named possible bridge, stated before its use

The conjecture suggested by the fixed-map identity is **SCN2**, sky-clock
normalization: for each specified FAC1 preparation mean,

    N_±(U,L):=<p_±(L,n)^(-2)>_preparation =1.

SCN2 is UNADOPTED, free-and-explored, and not a consequence of R7: FAC1 changes
endpoint clocks, null paths and transport as n varies. The source is the
Lorentz-sky identity above; the proposed physical connection is that an
independently defined angular comparison might carry that same Jacobian law.
Its first discriminator is FAC1's established regional-vacuum expansion.
Maximum conditional conclusion is a restriction from SCN2, not its physical
justification. A weaker sufficient Jensen bridge is **SCB2**, N_±<=1; it too is
UNADOPTED. Both imply AMS for the corresponding mean, since

    M_±=<log p_±> >= -(1/2)log N_±.

AMS does not conversely imply SCB2 or SCN2. Arbitrarily choosing a density
proportional to p^-2 introduces the normalization N in the proportionality
constant, so it cannot prove N=1 or M>=0. Parent later supplied the general
relative-entropy formulation of this same distinction; initial route preceded
that exposure. No imported photon-population conservation or flux law is used.

## 3. Vacuum moment theorem and the decisive rejection

Use exactly FAC1's smooth regional-vacuum, fixed finite laboratory, free clocks,
parallel initial preparation, regular first-signal branches and original S²
measure. Its uniform small-L remainder, together with PSW/PRT1's reversed
preparation argument, supplies for BOTH separate first signals

    D_±(n,L)=log p_±=-E_ij n^i n^j L²/2+O(L³),
    M_±=(4 E²-3 B²)L⁴/360+O(L⁵).

Here E is the electric Weyl tensor and B the magnetic one relative to U;
E is symmetric tracefree, E²=E_ij E_ij>=0, and similarly B²>=0. E/B are curvature
parts, not extra physical fields. The preparation-sphere fourth moment is

    <n_i n_j n_k n_l>=(delta_ij delta_kl+delta_ik delta_jl
                     +delta_il delta_jk)/15.

This follows rotation symmetry and contraction of indices. Hence

    <D_±²>=E² L⁴/30+O(L⁵).

Because D=O(L²) uniformly, Taylor's theorem has uniform cubic error O(L⁶):

    N_±=<exp(-2D_±)>=1-2M_±+2<D_±²>+O(L⁶)
       =1+(8E²+3B²)L⁴/180+O(L⁵).                 (B1)

Thus at an event with nonzero Weyl, either E² or B² is positive for every
finite timelike U, and N_±>1 for every sufficiently small positive L of that
fixed laboratory. SCN2 and SCB2 both fail there. This remains true even where
FAC1's AMS coefficient is positive. The exact FAC1 controls give:

| Control at FAC1's stated event/frame | E² | B² | coefficient of N_±-1 |
|---|---:|---:|---:|
| Kasner | 8/27 | 0 | 16/1215 |
| symmetric plane wave | 1/2 | 1/2 | 11/360 |
| negative Kerr event | 0 | 2/9 | 1/270 |

These are substitutions in an analytic consequence of the reviewed FAC1
theorem, not new independent original-metric runs. They show the trial bridge
excludes positive-AMS Kasner/plane-wave as well as negative-AMS Kerr. A vacuum
point with E=B=0 leaves higher orders open; B1 alone does not prove finite
normalization there. Pointwise Ric=0 without regional vacuum is insufficient.

As a stronger conditional corollary, exact SCN2 at every event and every finite
observer throughout a region, for all sufficiently short preparations, forces
local flatness. Outside an assumed vacuum sector, PSW gives
N_±=1+Ric(U,U)L²/3+O(L³); SCN2 for all timelike U forces Ric=0 regionally by
polarization. B1 then forces Weyl=0. Conversely a locally flat sufficiently
small convex laboratory has p_±=1. This corollary concerns the exact UNADOPTED
SCN2 law with all these quantifiers; SCB2 alone does not first imply Ric=0.

## 4. What an actual angular map can and cannot add

For the reverse first-signal experiment, tag the preparation directions n.
Record the sourceward arrival direction at the central A clock for each ray,
and parallel-transport A's spatial frame along its own geodesic to compare the
records. At sufficiently small L, the map F_L from preparation S² to this
recorded direction sphere is a smooth degree-one diffeomorphism near the flat
identity. This follows regular endpoint incidence and smooth C1 dependence,
with compact S². Restrict explicitly to that regime: no caustics, folds,+multiple images or distant global claim is included.

Its positive angular Jacobian J_L is independently defined by directions,
and <J_L>=1 by change of variables. Setting

    Delta_L(n)=log p_-(n)+(1/2)log J_L(n)

gives the exact bookkeeping identity

    M_- = -(1/2)<log J_L>+<Delta_L>.

The first term is nonnegative by Jensen. The second term is not controlled
by angular normalization. It is a separately measured clock/angle mismatch,
not a new field, additive physical positional component or selected local law.
The nonautomatic pointwise trial closure J_L=p_-^-2 would force SCN2 and is
therefore excluded by B1 in every nonzero-Weyl regional-vacuum laboratory.
One must not define J from p and then call this an independently tested relation.
No explicit curvature expansion of this actual F_L is required for that exclusion.
For a distant map with folds or incomplete sky coverage, even <J>=1 in this
form needs replacement; no extrapolation is made.

## 5. Surviving conditional measurement relation

The new moment computation can be retained as an internal check of the
prepared regional-vacuum experiment rather than a sign-selection principle.
Define m4=lim M/L⁴ and n4=lim(N-1)/L⁴. Then

    E²=15(n4+2m4),     B²=20n4-80m4.             (B2)

Equivalently v4=lim Var(log p)/L⁴=E²/30 and B²=40v4-120m4.
Both directions have these limits under FAC1's hypotheses, although their
finite values need not agree. This is mathematical inference from ideal
asymptotic clock moments, not a finite-precision instrument model, independent
evidence for vacuum, geometry selection or positional attribution. It can
detect a mistaken angular-weight transfer without inventing a new physical law.

## 6. Scope and continuation decision

The avenue was not stopped at its initial measure objection. It supplied a
quantitative normalization test, its positive-square vacuum obstruction and
an actual angular-map formulation that shows exactly what physical closure
would be added. The closest inspected predecessors are central R7/FSL1,
PSW1/PRT1 and FAC1; no corpus-wide novelty claim is made. A broad registry
regex accidentally returned unrelated wide rows; those were not used as
premises or mined, and all load-bearing evidence here is the named sources.

The specific rejected identification is that FAC1's positive angular mean
follows automatically from fixed-Lorentz sky normalization/reciprocity.
This does not reject AMS, other justified measures, distant-onset laws, native
UDT, or all clarified founding commitments. Further arbitrary normalization
variants would not close the physical join. A useful next probe needs an
independent reason why actual clock and angle records obey a proposed relation
in a specified physical regime; otherwise this is a decision-ready negative
with a surviving conditional moment diagnostic. No full optical machinery,
preferred observer, physical population, source law, field equation or scale
has been introduced.

## Source ownership

- UDT_DEVELOPMENT.md D1, R6/R7, PSW1, R8PRT, R8FAC/R8FACP and R18: meanings,
  current dependencies and limits, inspected at parent HEAD d8171f96.
- udt_finite_separation_law_2026-09-28/INITIAL_CANDIDATE.md §§1–4: exact
  forward-vector convention, frequency ratio and direction-retaining map.
- udt_finite_angular_clock_probe_2026-10-13/REVIEWED_RESULT.md and central
  invariant proof: regional-vacuum quartic theorem, uniform remainder and controls.
- Parent suggested primary symplectic-optics references after INITIAL_APPROACH;
  these were not used as theorem inputs here. The displayed results are direct
  finite-dimensional geometry, elementary integration and FAC1 consequences.
