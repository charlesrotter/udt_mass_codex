# Reverse-engineering the deeper UDT postulate — derivation results

> **FOUNDATIONAL INTERPRETATION SUPERSEDED (2026-07-15):** Charles Rotter subsequently proposed
> the upstream Reciprocal-c Identity: $c$ and $c^{-1}$ are coequal time-length conversion
> directions. Combined with the UDT Reciprocity Principle, that proposal makes the
> causal-measure-preservation rule studied here a derived consequence rather than the deeper
> postulate. See `UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md`. The algebra below
> remains valid within its stated premises.

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic reverse derivation; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Inputs | WR-L reciprocal metric; positional dilation; Reciprocity Principle; local invariant `c` |
| Adoption authority | No new postulate adopted; owner verdict and independent verification remain required |
| GPU | Not used or needed |

## 0. Result

The best deeper-postulate candidate found in the declared census is:

> **Principle of Positional Relativity and Causal-Measure Preservation.**
> Observational positions are related by reversible, composable transformations. A positional
> transformation may redistribute temporal and radial calibration, but it preserves their local
> oriented spacetime measure.

In plain language:

> **Changing observational position may trade clock scale against radial ruler scale, but it does
> not create or destroy their combined local spacetime capacity.**

This is not a conservation law in time and not a material incompressibility rule. It is an
invariance statement comparing positional frames.

Within the positive diagonal spherical areal sector, the candidate plus a nontrivial positional
representation gives

$$
\boxed{
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2 .
}
$$

The derivation is conditional because the candidate itself has been reverse-engineered from the
known metric and has not yet been independently established.

It does **not** derive $\phi(r)$, the universal scale $X$, the WR-L profile
$e^{-2\phi}=1-r/X$, a unique dynamical action, matter emergence, or an $S^2$ carrier.

## 1. Exact kinematic derivation

Let $\Delta$ be additive relative positional depth, and write the most general positive adapted
clock and radial-ruler comparison factors as

$$
ds^2=-T(\Delta)^2c^2dt^2+R(\Delta)^2dr^2+r^2d\Omega^2,
$$

with $T(0)=R(0)=1$. Positional relativity means that comparisons compose and reverse:

$$
T(\Delta_1+\Delta_2)=T(\Delta_1)T(\Delta_2),
\qquad
T(-\Delta)=T(\Delta)^{-1},
$$

and likewise for $R$. Continuity gives

$$
T(\Delta)=e^{a\Delta},
\qquad
R(\Delta)=e^{b\Delta}.
$$

Preservation of the oriented radial spacetime measure requires

$$
T(\Delta)R(\Delta)=1,
$$

so

$$
a+b=0.
$$

For the nontrivial branch, normalize the dimensionless depth by $\phi=-a\Delta$. Then

$$
T=e^{-\phi},
\qquad
R=e^{+\phi},
$$

which gives the UDT reciprocal metric.

### Status

- **DERIVED from the candidate premises:** exponential composition and reciprocal exponents.
- **CHOSE as a convention:** the sign and unit normalization of $\phi$.
- **OPEN:** why nature realizes a nontrivial positional representation rather than $a=b=0$.

The observed existence of positional redshift, or an independently established $X$-wall, can
select the nontrivial branch. The preservation principle alone cannot.

## 2. What is actually preserved

The radial metric block has determinant

$$
\det g_{(t,r)}=left(-e^{-2\phi}c^2\right)e^{2\phi}=-c^2.
$$

Therefore the full spherical determinant and volume form are

$$
\det g=-c^2r^4\sin^2\theta,
$$

$$
\boxed{
dV_4=\sqrt{-g}\,dt\,dr\,d\theta\,d\varphi
=c r^2\sin\theta\,dt\,dr\,d\theta\,d\varphi,
}
$$

on the usual $0\leq\theta\leq\pi$ chart. The dilation field does not appear in this volume form.

Equivalently, the positional calibration transformation is

$$
S(\phi)=
\begin{pmatrix}
e^{-\phi}&0\\
0&e^{\phi}
\end{pmatrix},
\qquad
\det S=1,
$$

with

$$
S(\phi_1)S(\phi_2)=S(\phi_1+\phi_2),
\qquad
S(\phi)^{-1}=S(-\phi).
$$

Thus reciprocity is not an added numerical coincidence: it is the determinant-one condition for
the positional transformation.

## 3. Independent consequences

### 3.1 Invariant relative comparison

For two positions $A$ and $B$,

$$
\frac12\operatorname{Tr}\!\left(S_A^{-1}S_B\right)
=\cosh(\phi_B-\phi_A).
$$

This supplies a reversal-symmetric comparison depending only on relative positional depth.

### 3.2 The quadratic norm appears, but an action does not

The group current is

$$
J=S^{-1}dS=
\begin{pmatrix}
-d\phi&0\\
0&d\phi
\end{pmatrix},
$$

so

$$
\operatorname{Tr}J=0,
\qquad
\boxed{\frac12\operatorname{Tr}(J^2)=d\phi^2.}
$$

Therefore the determinant-one positional geometry supplies a natural invariant quadratic tangent
norm. This strengthens the earlier quadratic-cost lead. It still does not prove that the physical
action must equal the integral of this norm; that requires an independent extremization/minimality
premise.

### 3.3 Allowed metric variations are trace-free

Under $\phi\mapsto\phi+\delta\phi$,

$$
\delta g_{tt}=-2g_{tt}\,\delta\phi,
\qquad
\delta g_{rr}=+2g_{rr}\,\delta\phi.
$$

Hence

$$
g^{\mu\nu}\delta g_{\mu\nu}=0,
\qquad
\delta\sqrt{-g}=0.
$$

The reciprocal mode is a volume-preserving, trace-free metric deformation in this sector.

### 3.4 Conditional source readout

If matter couples through the physical metric and a diagonal stress readout obeys
$T^t{}_t=-\rho$ and $T^r{}_r=p_r$, then

$$
T^{\mu\nu}\delta g_{\mu\nu}
=2(\rho+p_r)\delta\phi.
$$

Thus the reciprocal dilation mode reads the combination $\rho+p_r$, not the trace alone. This is
a **CONDITIONAL comparison/readout**, not a native UDT matter equation.

## 4. Coordinate and physical-content audit

A determinant value by itself is coordinate-dependent. The physical candidate must therefore be
stated as equality of volume forms under positional-frame transformations, relative to an
operational reference frame or reference volume form—not as the bare coordinate slogan
“$\det g$ is fixed.”

In a general static spherical areal chart,

$$
ds^2=-C(r)c^2dt^2+D(r)dr^2+r^2d\Omega^2,
$$

the areal meaning of $r$ fixes the radial gauge. A constant rescaling of $t$ changes $CD$ only by
a constant and cannot erase radial dependence in $CD$. Therefore $CD=1$, once the asymptotic or
reference clock is normalized, is a genuine restriction within this sector rather than an
arbitrary remaining coordinate choice.

The restriction still needs an operational reference-volume statement to be promoted to a
generally meaningful postulate.

## 5. Candidate census verdict

| Candidate | Verdict | Reason |
|---|---|---|
| C1: positional relativity alone | **INSUFFICIENT** | Composition gives two independent exponents $a,b$; it does not force reciprocity. |
| C2: invariant local $c$ alone | **INSUFFICIENT** | Any positive diagonal metric gives local measured null speed $c$; it does not force $TR=1$. |
| C3: reciprocal clock/ruler statement | **WORKING but shallow** | It gives the metric directly but mostly restates its desired structure. |
| C4: positional relativity plus causal-measure preservation | **PRIME KINEMATIC CANDIDATE** | It forces the reciprocal exponent, has group and variation consequences, and can be stated independently of the metric coefficients. |
| C5: quadratic invariant-distortion extremization | **OPEN DYNAMICAL PREMISE** | It could select a quadratic action, but it is an additional principle, not a consequence of C4. |

## 6. Why this still does not determine the action

Let

$$
Y=\frac12\operatorname{Tr}(J_\mu J^\mu).
$$

C4 allows every scalar action of the form

$$
I_F=\int dV_4\,F(Y),
$$

including, for example,

$$
F(Y)=\frac12Y
\quad\hbox{and}\quad
F(Y)=\frac12Y+\frac{\alpha}{4}Y^2.
$$

Both respect the same positional composition, reversal, and measure-preserving structure, but
their nonlinear Euler equations differ. Therefore

$$
\boxed{
\text{the deeper kinematic candidate does not uniquely determine UDT dynamics.}
}
$$

Selecting the quadratic member would require one more dynamical rule—for example exact local
additivity/orthogonality of independent infinitesimal dilation costs, or an explicitly adopted
minimal-derivative extremization principle. Neither is currently DERIVED.

## 7. Why this does not select WR-L or $X$

Every positive reciprocal profile

$$
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2
$$

preserves the same volume form. Consequently the candidate does not distinguish

$$
A(r)=1-\frac rX
$$

from infinitely many other $A(r)$. The already banked WR-L selector—residual re-centering plus wall
regularity—remains separate and is not weakened or replaced by this result.

## 8. Falsification and promotion gates

The candidate is useful precisely because it can fail. It would be falsified or require
generalization if:

1. a valid UDT sector requires a positional transformation whose operational volume form changes;
2. a full time-live or nonspherical UDT metric cannot implement the claimed determinant-one
   positional comparison;
3. reciprocal clock/ruler behavior is found to be coordinate-only after operational observables
   are specified;
4. an independently derived native UDT action requires a different positional transformation
   group;
5. observations require nonreciprocal positional clock and radial-ruler factors.

Promotion from reverse-engineered candidate to UDT postulate requires a cold derivation or an
explicit foundational choice, followed by tests outside the spherical static sector.

## 9. Honest status

$$
\boxed{
\begin{gathered}
\text{DERIVED from the candidate: reciprocal exponential metric structure,}\\
\text{fixed volume form, determinant-one group, trace-free mode, quadratic tangent norm;}\\
\text{OPEN: nontrivial branch, full covariance, profile }\phi(r),\ X,\text{ and dynamics;}\\
\text{NOT DERIVED: unique action, matter emergence, or }S^2\text{ carrier.}
\end{gathered}
}
$$

The candidate is the cleanest logical postulate presently beneath positional dilation, but it is
not yet UDT canon.
