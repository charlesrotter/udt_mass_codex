# G291 whiteboard report — global screen-flux ownership

Date: 2026-08-28
Grade: `MULTI_AGENT_WHITEBOARD_LEAD__EXACT_DESCENT_NOT_YET_RUN`

## Hybrid landing

```text
PARTIAL_TOPOLOGICAL_OR_STRATUM_RESTRICTIONS_ONLY
__GLOBAL_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_RESTRICT_CONTINUOUS_SCREEN_CURVATURE_FLUX
__NO_COMPLETE_HISTORY_SELECTION
```

This is not a definitive bifurcation. It separates a discrete topological layer that is already
owned conditionally from a continuous geometric layer whose physical history remains open.

## Consensus theorem candidate

Let `S -> W` be a supplied smooth oriented positive rank-two screen bundle with the G290 projected
metric connection `D`. Its closed-loop holonomy and curvature form a degree-two differential
character. Up to the frozen orientation/sign convention,

\[
\operatorname{Hol}_D(\partial\Sigma)
=\exp\!\left(i\int_\Sigma F_D\right),
\qquad dF_D=0,
\qquad \left[\frac{F_D}{2\pi}\right]=e(S)\in H^2(W;\mathbb Z).
\]

Thus closed-cycle flux is integral, and the Euler class cannot change during a smooth regular
fixed-rank continuation. A class change requires leaving that stratum through degeneration,
boundary, singularity, or topology change.

This is genuine global compatibility and sector persistence. It does not fix local curvature or
propagate a metric history.

## Continuous same-sector freedom

For the oriented quarter-turn `J` and any global one-form `b`, two metric screen connections on the
same bundle may differ by

\[
D^b=D+bJ,
\qquad F^b=F+db,
\]

with

\[
\operatorname{Hol}_{D^b}(\gamma)
=\operatorname{Hol}_{D}(\gamma)
 \exp\!\left(i\oint_\gamma b\right).
\]

The Euler class, closed-cycle periods, overlap descent, reversal, composition, thin-homotopy rule,
and worldtube transgression all survive. Local flux and loop holonomy still vary continuously. A
closed nonexact `b` can also change flat holonomy without changing curvature.

Full thin-path holonomy can reconstruct the supplied connection up to gauge. Ambrose-Singer can
reconstruct its curvature-generated holonomy algebra. Neither reconstruction chooses values.

## Exact global metric witness proposed by the panel

On

\[
M=\mathbb R_t\times\mathbb R_z\times S^2,
\]

consider

\[
g_\epsilon=-dt^2+dz^2+e^{2\epsilon\cos\theta}q_{S^2}.
\]

With null direction `partial_t + partial_z`, the intrinsic `t-z` pair block is the same for every
`epsilon`, while the screen is `TS^2`. Up to orientation sign, its curvature form is

\[
F_\epsilon=(1+2\epsilon\cos\theta)dA_0.
\]

All members have total flux

\[
\int_{S^2}F_\epsilon=4\pi,
\]

but the flux change through a polar cap bounded at `theta_0` is

\[
2\pi\epsilon\sin^2\theta_0.
\]

This candidate counterfamily is smooth, complete, globally hyperbolic, globally nontrivial, and
metric-induced. It keeps the topological class and reciprocal pair block fixed while changing the
local screen-flux distribution. It must be rederived and checked independently before promotion
from whiteboard lead.

The already checked G290 conformal witness gives the same logical separator locally: completed-pair
normalization has terminal reciprocal state `Phi=chi=0` for every `alpha`, while

\[
F_S=-4\alpha\,dx\wedge dy.
\]

Therefore current completed-pair reciprocity does not entail a universal law `F_S=F(delta)`.

## Three distinct global objects

1. **G225 celestial-direction screen.** At one supplied observer event the full sky screen bundle is
   canonically `TS^2`. Its Euler number is `2`, so its total oriented flux has magnitude `4 pi`.
   This is a kinematic sky-fiber fact present even in flat spacetime.
2. **General G290 pair-base screen.** Its characteristic class depends on the supplied bundle over
   the supplied relation base. It is not automatically the G225 sky bundle.
3. **Time-live regular continuation.** It preserves the characteristic class while allowing the
   connection and curvature distribution to vary continuously within that class.

Identifying these objects without a supplied observer field and direction map would be an imported
premise.

## Scalar versus angular independence

G226's conformal-symplectic multiplier fixes the reciprocal clock grading. Screen rotations
`diag(H,H)` lie in the symplectic kernel of that multiplier. A scalar reciprocal loop can therefore
close while its screen holonomy remains nonidentity. G270's same-completed-pullback/different-screen
witness and G290's same-terminal-depth/different-flux witness express the same separation at
successively stronger levels.

No active premise currently couples reciprocal depth to the magnitude or distribution of screen
curvature.

## Nonorientable and singular strata

For a nonorientable screen bundle, determinant/reflection holonomy detects the first
Stiefel-Whitney class, and the Euler class lives in the orientation local system. G290's orientable
inverse/conjugacy classification does not close this stratum. Global hyperbolicity forbids closed
causal spacetime curves, not loops in sky, relation, or path-parameter space, so it does not flatten
screen holonomy.

## Exact status

| Question | Whiteboard result |
| --- | --- |
| Does global data reconstruct a supplied connection? | `YES_CONDITIONAL` |
| Does topology constrain global flux periods? | `YES_CONDITIONAL_PARTIAL` |
| Does smooth regular continuation preserve the sector? | `YES_CONDITIONAL_PARTIAL` |
| Does reciprocity fix local screen curvature? | `NO_ON_EXACT_G290_WITNESS` |
| Does the global network propagate continuous flux? | `NOT_DERIVED` |
| Does it select a complete physical history? | `NO_CURRENT_OWNER_FOUND` |

## Smallest next derivation

Preregister one orientable differential-character descent that:

1. derives the Euler-period and smooth-continuation statements;
2. rederives the global `g_epsilon` metric witness independently;
3. compares the G225 celestial connection with a G290 pair-base connection only after supplying an
   explicit direction map;
4. separates universal sky-fiber flux from the exact connection difference `bJ` that carries
   metric-history information;
5. leaves the nonorientable `O(2)` twisted-Euler stratum as an explicit follow-up.

That calculation would close the partial topological result. It would not create a dynamics or
select a universe.
