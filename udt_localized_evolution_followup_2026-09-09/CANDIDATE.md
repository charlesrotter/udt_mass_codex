# LE1 — weakening curvature does not erase early-time curvature shape

Initial candidate, UNPROMOTED. Author /root, 2026-09-09. One bounded result;
not an evolution simulation or a new Kasner identity. WORK_ORDER.md controls
scope; review is still pending at this initial freeze.

## 1. Precise conditional statement

Fix an LG2 datum at its effective reviewed scope: the initial candidate PLUS
its step_02/REPAIR.md. Thus fix T0>0, the supplied G324 compact split quotient,
embedded nested balls, a sufficiently high finite norm and sufficiently small
0<|u|<min(u_*,1/10). Let B_r be any open concentric ball with 0<r<r_- inside
the EXACT Kasner core. The existence threshold u_* is inherited, not computed.

For EVERY smooth globally constraint-compatible completion with this core,
and EVERY smooth local globally hyperbolic vacuum development of that datum,
there is a common marked local development with the explicit Kasner solution
near each compact subball of B_r. The marking agrees with the supplied initial
data and future normal. On that common domain the statements below hold
exactly. There is a positive early interval on each compact subball, possibly
depending on the completion and the chosen development. No common quantitative
lifespan over all completions is asserted.

The active equation is OWNER-PROVISIONAL G310/G312 Ric(g)=Lambda g; the
unchanged Ricci-flat exterior fixes Lambda=0 for THIS comparison, not UDT
generally. G303/G315 supply the conditional smooth local-development and
geometric-uniqueness interface. This result uses reviewed UNPROMOTED LG2
conditionally; it cannot convert that dependency or its method assumptions
into accepted science. No carrier, action, source or instrument is introduced.

In the inherited local orthonormal initial coordinates put

    c=(1-u^2)/(1+u^2), s=2u/(1+u^2),
    p=((1-2c)/3, (1+c-sqrt(3)s)/3, (1+c+sqrt(3)s)/3).

Then sum p_i=sum p_i^2=1, and the common core metric is

    g_p=-dT^2+sum_i (T/T0)^(2p_i)(dx^i)^2,  T>0.             (1)

T is the proper time of its normal comoving congruence, with the supplied
value T0 on the initial slice. No preferred universal clock is selected.

## 2. Two different geometric questions

Use the absolute scalar Kcal=R_abcd R^abcd. Independently define a
dimensionless curvature-shape diagnostic from the FULL complex self-dual
Weyl endomorphism Q:

    I2=tr(Q^2), I3=tr(Q^3), A=1-6 I3^2/I2^3,   I2 != 0.     (2)

We normalize Q so that in the comoving purely electric frame its eigenvalues
are E_i=p_i(1-p_i)/T^2. A common nonzero convention factor/sign cancels in A;
opposite orientation complex-conjugates A, which is real here. The trace
invariants are basis/observer independent because Q is the self-dual Weyl
operator, not the electric matrix viewed in isolation in an arbitrary frame.
This A is one minus the established speciality index, not a new UDT object
or a complete invariant of arbitrary geometry. Outside the core it may be
complex or undefined; it is neither energy nor physical carried content.

Let P=p1 p2 p3. Direct curvature calculation and the Kasner constraints give

    B=0, E_i=p_i(1-p_i)/T^2=-p_j p_k/T^2,
    I2=-2P/T^4, I3=-3P^2/T^6,
    Kcal=-16P/T^4, A=1+(27/4)P.                             (3)

Consequently, in the nonflat inherited core,

    dKcal/dT=-4Kcal/T < 0,   dA/dT=0,
    A(u)=u^2(u^2-3)^2/(1+u^2)^3 > 0.                       (4)

The original Taub geometry has A=0 everywhere, and Kcal_0=64/(27T^4).
Thus the localized core remains algebraically different from Taub throughout
this actual early-time domain, while its absolute curvature decreases.
No reslicing or common change of overall metric scale removes the nonzero A.
This is NOT a theorem that the spacetime stays a finite distance from Taub
in any specified metric/Sobolev norm: A divides by a curvature scale.
Nor may one take T to infinity in the localized development merely because
the homogeneous expression (1) exists there for every positive T.

The diagnostic is second-order sensitive near this symmetric background:
A=9u^2-33u^4+O(u^6). A zero first variation is therefore a blind spot of this
particular diagnostic, not evidence of pure gauge or absence of a difference.
The exact rational formula, not the expansion, supports the statement.

## 3. Why this describes actual localized evolution

The completed global datum obeys all original vacuum constraints. Its
restriction to B_r coincides with the data induced by (1), including K, with
the same sign convention K_ij=-(1/2)partial_T gamma_ij. G303/G315's imported
smooth Cauchy theorem gives local developments and geometric uniqueness.
Apply local uniqueness to these common restricted data: the two spacetimes
have an initial-data-preserving isometric common development. On a compact
subball, shrink to a positive common time neighborhood if necessary. This
is the actual comparison used in (3)--(4), not an arbitrary perturbed field
or a formal homogeneous solution assumed to cover the transition region.

The usual causal domain-of-dependence property of the same hyperbolic metric
system controls dependence on the exterior data. To exhibit a usable INNER
bound in the Kasner chart, let p_min=min_i p_i<0 and T>=T0. For any causal
curve parameterized by T, (1) gives

    sum_i (T/T0)^(2p_i)(dx^i/dT)^2 <= 1,
    |dx/dT|_Euclidean <= (T/T0)^(-p_min).

Define

    L_p(T)=integral[T0,T](s/T0)^(-p_min) ds
          =T0*((T/T0)^(1-p_min)-1)/(1-p_min).              (5)

Every past causal path from a point satisfying

    |x|+L_p(T)<r                                            (6)

stays within the Kasner cylinder over B_r until reaching T0: at an earlier
time t its radius is at most |x|+L_p(T)-L_p(t)<r. Smoothness and bounded
coordinate speed in a compact positive-time slab prevent an interior
endpoint. Thus (6) is a sufficient inner subset of the homogeneous future
domain of dependence of B_r. It does not give the exact anisotropic front.

Use (6) ONLY in the justified local common-development comparison just
described. We do not infer from it that an arbitrary chosen/truncated local
development exists all the way to the time L_p(T)=r, nor any uniform lifetime
from the unspecified transition data. For each compact subball there is a
positive interval in that common neighborhood where (6) holds. Causal
uniqueness supplies the comparison, and the elementary estimate supplies a
sufficient chart-domain check; neither substitutes for the other.

Shrinkage of this guaranteed inner set is shrinkage of the region controlled
by the core data alone. It is NOT measured shrinkage of a geometric object,
nor proof of outgoing radiation, dispersal, confinement or collapse.

## 4. What has and has not advanced

Known homogeneous Kasner curvature identities plus conditional local
uniqueness now give an explicit, completion-independent EARLY behavior for
the lawful LG2 localized core. Absolute weakening alone does not force its
dimensionless curvature shape to approach Taub in that domain. LG2 already
gave the initial algebraic distinction and existence of a local Kasner
patch; this is a bounded diagnostic/evolution consequence, not an additional
localization theorem or new general stability result.

The core parameter, scale, shape, radii, initial slicing and completion data
remain supplied choices. LG2's sufficient reflection/smallness restrictions
and source-deformation assumptions are retained, not established necessary
or physically selected. Beyond the causal comparison, this result does NOT
determine whether a localized difference disperses, persists or focuses.
The transition data's functional freedom is ordinary constrained initial
data, not itself a missing physical law. No examples of different late-time
outcomes, nonuniqueness for fixed full data or impossibility theorem are claimed.

Checks reconstruct the coordinate Riemann tensor and its contraction, reduce
by the exact constraints, test the diagnostic and reject relevant shortcuts.
Structural zero components are consistency checks, not independent evidence
for general PDE existence. Fresh source-first/direct review is required.
No accepted grade/canon/manuscript change; full365 remains failed at G325.

Primary method references: Bini--Cherubini--Jantzen,
https://arxiv.org/pdf/0710.4902v1, equations(8),(10),(31)--(33);
Sbierski, https://arxiv.org/pdf/1309.7591v3, section2, Theorem2.6.
The latter documents the existing smooth local-uniqueness interface; no
global-completeness result is invoked. METHOD_ACCESS.md pins exact versions.
