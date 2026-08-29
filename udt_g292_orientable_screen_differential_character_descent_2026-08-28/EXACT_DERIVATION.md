# G292 exact derivation — orientable screen differential character and metric freedom

Date: 2026-08-28
Grade: `EXTERNALLY_ACCEPTED_BOUNDED_G292__REPAIRS_ACCEPTED`

## Bounded landing

```text
ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY
__G225_SKY_AND_G290_PAIR_CONNECTIONS_REQUIRE_SUPPLIED_IDENTIFICATION
__GLOBAL_SAME_PAIR_BLOCK_SAME_EULER_CLASS_DIFFERENT_LOCAL_FLUX_METRIC_FAMILY
__NO_CONTINUOUS_FLUX_PROPAGATION_OR_HISTORY_SELECTION
```

Exact token:
`ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY__G225_SKY_AND_G290_PAIR_CONNECTIONS_REQUIRE_SUPPLIED_IDENTIFICATION__GLOBAL_SAME_PAIR_BLOCK_SAME_EULER_CLASS_DIFFERENT_LOCAL_FLUX_METRIC_FAMILY__NO_CONTINUOUS_FLUX_PROPAGATION_OR_HISTORY_SELECTION`.

## 1. Exact scope

Let `S -> W` be a supplied smooth oriented positive rank-two screen bundle over a supplied regular
complete-pair base. Let

\[
D_Xs=P_S\!\left(\nabla^g_{F_*X}s\right)
\]

be the G290 projected metric connection. The metric, pair base, screen carry, orientation, cycles,
and any comparison map are supplied exactly as recorded in the premise ledger.

The differential-character and affine-connection theorems cover the abstract smooth orientable
`SO(2)` metric-connection stratum on a fixed supplied bundle. G292 does not prove that every such
abstract connection is induced by a complete UDT metric history; it supplies the explicit global
metric family in Section 6 as one realized subfamily. The result does not cover nonorientable
`O(2)` reflection holonomy, rank loss, topology change, singularities, physical loop population, or
dynamics.

## 2. Differential-character descent

On an oriented orthonormal screen patch choose `(e_1,e_2)` and the G290 convention

\[
a(X)=g(e_1,D_Xe_2).
\]

On an overlap with frame rotation `theta_ij`,

\[
a_j=a_i-d\theta_{ij}.
\]

Therefore

\[
F_D=da_i
\]

is a globally defined closed two-form. On triple overlaps,

\[
\theta_{ij}+\theta_{jk}+\theta_{ki}=2\pi n_{ijk},
\qquad n_{ijk}\in\mathbb Z.
\]

The integer Cech cocycle is the Euler class of the oriented real two-plane bundle. With the frozen
orientation convention,

\[
\boxed{
\left[\frac{F_D}{2\pi}\right]=e(S)\in H^2(W;\mathbb Z)
}
\]

up to the corresponding global sign if orientation is reversed. Hence every closed oriented
two-cycle satisfies

\[
\boxed{
\frac{1}{2\pi}\int_\Sigma F_D
=\langle e(S),[\Sigma]\rangle\in\mathbb Z.
}
\]

Together with

\[
\operatorname{Hol}_D(\partial C)
=\exp\!\left(i\int_C F_D\right),
\]

closed-loop holonomy defines the degree-two differential character of the supplied screen
connection. The local potential is gauge-dependent; the character and characteristic class are
not.

## 3. What smooth continuation preserves

Let a fixed-rank oriented screen bundle extend smoothly over `W x I`. The slice inclusions

\[
i_s:W\hookrightarrow W\times I
\]

are homotopic, so

\[
i_{s_1}^*e(S)=i_{s_2}^*e(S).
\]

Thus the Euler sector cannot jump during a supplied smooth regular continuation. A jump requires
leaving this stratum through rank/orientation loss, a boundary, singularity, or topology change.
This is kinematic sector persistence, not a physical conservation or evolution law.

## 4. The continuous freedom inside one sector

After an orientation-preserving isometric identification of two screen bundles, the difference of
two metric connections is an `so(2)`-valued one-form. Because `so(2)` is one-dimensional, there is a
global real one-form `b` and oriented quarter-turn `J` such that

\[
D^b=D+bJ.
\]

The group is abelian, so

\[
\boxed{F_{D^b}=F_D+db},
\]

and for a closed loop

\[
\boxed{
\operatorname{Hol}_{D^b}(\gamma)
=\operatorname{Hol}_{D}(\gamma)
 \exp\!\left(i\oint_\gamma b\right).
}
\]

The Euler class and every closed-cycle period remain fixed because `db` is exact. Local curvature
and loop holonomy still vary continuously. If `b` is closed but not exact, curvature is unchanged
while a flat global holonomy sector can change. Full smooth thin-path holonomy reconstructs the
supplied connection up to gauge; it does not select one connection from this affine space.

## 5. G225 full sky versus a G290 pair-base screen

At one supplied calibrated observer event, G225 identifies the full celestial screen bundle with

\[
S_{\rm sky}=TS^2.
\]

The normalized round-sky connection has, on a standard oriented patch,

\[
a_0=-\cos\theta\,d\varphi,
\qquad
F_0=\sin\theta\,d\theta\wedge d\varphi,
\]

so

\[
\frac{1}{2\pi}\int_{S^2}F_0=2.
\]

This is the G225 hairy-ball obstruction in curvature form. It is kinematic direction-space
topology and is present even in flat spacetime.

A general G290 pair-base screen need not live over `S^2` and is not automatically `TS^2`. To
compare it with the celestial connection one must supply a direction map

\[
n:W\to S^2
\]

and an orientation-preserving isometric bundle map

\[
\iota:S\to n^*TS^2.
\]

Only after that typing may the pulled connection be compared. The two then differ by `bJ` as above.
Changing the identification can change `b`; the invariant comparison data are the curvature
difference `db` and closed-loop holonomy ratio. No universal sky/pair identification is inserted.

## 6. Exact global metric counterfamily

Take

\[
M=\mathbb R_t\times\mathbb R_z\times S^2
\]

and the two-free-parameter family

\[
\boxed{
g_{R,\epsilon}
=-c_E^2dt^2+dz^2
+R^2e^{2\epsilon\cos\theta}
\left(d\theta^2+\sin^2\theta\,d\varphi^2\right),
\quad R>0,\ \epsilon\in\mathbb R.
}
\]

The parameters remain free and are not fitted or selected. For every finite `epsilon` and positive
`R`, the screen metric is smooth and positive on the compact sphere. The spatial factor is complete;
the static product with unit lapse in `(c_E t)` units is globally hyperbolic and geodesically
complete.

The vector

\[
k=c_E^{-1}\partial_t+\partial_z
\]

is null. Its `t-z` pair block in the `(c_Edt,dz)` coframe is

\[
h=\operatorname{diag}(-1,1),
\]

so for every `R,epsilon`,

\[
m=1,
\qquad \Phi=\phi_{\rm pair}=0.
\]

The positive screen is `TS^2`. Set `u=epsilon cos(theta)` and use the orthonormal coframe

\[
e^1=Re^u d\theta,
\qquad
e^2=Re^u\sin\theta d\varphi.
\]

A direct Levi-Civita/Cartan calculation gives

\[
a_\epsilon
=-\bigl(u'\sin\theta+\cos\theta\bigr)d\varphi
=\left(-\cos\theta+\epsilon\sin^2\theta\right)d\varphi,
\]

and

\[
\boxed{
F_\epsilon
=\left(1+2\epsilon\cos\theta\right)
\sin\theta\,d\theta\wedge d\varphi.
}
\]

The radius `R` cancels from the curvature two-form. Relative to the round-sky connection,

\[
b=\epsilon\sin^2\theta\,d\varphi.
\]

This is global and pole-regular because on the unit sphere

\[
\sin^2\theta\,d\varphi=x\,dy-y\,dx.
\]

Its curvature change is exact:

\[
db=2\epsilon\sin\theta\cos\theta\,d\theta\wedge d\varphi.
\]

The total flux remains

\[
\boxed{
\int_{S^2}F_\epsilon=4\pi
}
\]

for every `epsilon`, while a north polar cap ending at `theta_0` carries

\[
\int_{C_{\theta_0}}F_\epsilon
=2\pi\left(1-\cos\theta_0
+\epsilon\sin^2\theta_0\right).
\]

Its change from the round member is therefore

\[
\boxed{
\Delta\int_{C_{\theta_0}}F
=2\pi\epsilon\sin^2\theta_0.
}
\]

The latitude connection phase differs from the cap flux by exactly `2 pi`, illustrating the
required patch/large-gauge integer while leaving exponentiated holonomy equal. A single loop phase
is periodic and does not uniquely unwrap flux.

This is a global metric-induced family with the same completed reciprocal pair state and the same
Euler sector but different local screen curvature and holonomy. It proves that present reciprocity,
global descent, and topology do not determine continuous screen flux or a complete history.

## 7. Exact classification

| Object | Result |
| --- | --- |
| Differential character and Euler periods | `DERIVED_CONDITIONAL` |
| Euler-sector persistence on supplied regular continuation | `DERIVED_CONDITIONAL_KINEMATIC` |
| G225 full-sky Euler number | `DERIVED_CONDITIONAL_REFRAME` |
| Sky/pair identification | `SUPPLIED_WHEN_USED` |
| Same-class connection freedom | `DERIVED_MATHEMATICAL` |
| Global `g_(R,epsilon)` counterfamily | `SYMBOLIC_AND_INDEPENDENTLY_REPLAYED` |
| Continuous screen-flux propagation | `NOT_DERIVED` |
| Complete physical history selection | `NOT_DERIVED` |
| Nonorientable reflection/twisted-Euler descent | `OPEN_STRATUM` |

No action, field equation, source, boundary, observation, mass, physical scale selection, Planck
cutoff, `X_max`, or protected work entered.

## 8. Evidence

- preregistration commit: `e6a1bdfb`;
- 22 exact symbolic metric/connection/flux checks and 12 separately typed conclusions;
- implementation-distinct standard-library replay: 3,600 direct Riemann/Cartan point cases, 105
  cap quadratures, and 25,446 assertions;
- maximum errors: density `1.24e-14`, connection `1.24e-14`, total flux `4.57e-13`, cap flux
  `3.35e-11` (rounded upward from machine output);
- eight of eight preregistered hostile claim witnesses passed;
- fresh sealed external review returned `ACCEPT_WITH_REPAIRS` and no scientific defects;
- repairs R1--R4 are applied; sealed repair-only follow-up returned `ACCEPT_G292_REPAIRS` with no
  remaining defect and no scientific change.
