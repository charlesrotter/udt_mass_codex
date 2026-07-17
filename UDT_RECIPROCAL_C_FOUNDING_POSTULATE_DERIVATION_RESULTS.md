# Reciprocal-c founding postulate — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Origin | **Charles Rotter:** “$c$ is a reciprocal identity of time and length—not a one-way speed” |
| Combined premise | Reciprocal-c Identity plus the UDT Reciprocity Principle |
| Mode | Analytic derivation and circularity audit; DATA-BLIND |
| Repository | `grok` at `64af120`; unrelated dirt preserved |
| Verifier | `verify_udt_reciprocal_c_postulate.py`: **29/29 checks pass** |
| Adoption | User-proposed foundational postulate; independent verification still required before banking |
| GPU | Not used or needed |

## 0. Decisive result

The proposal is a genuine upstream candidate when stated as a **duality**, not merely as the
arithmetic observation that $c$ has an inverse.

> **Reciprocal-c Identity — proposed by Charles Rotter.** The universal constant $c$ is the
> reversible identity between temporal and spatial measure. Its two directions,
> $L=cT$ and $T=L/c$, are equally fundamental and must be respected by positional comparisons.

Together with the UDT Reciprocity Principle:

> A positional transformation acts reciprocally on the two sides of the time-length identity: the
> length-side action is the dual inverse of the time-side action.

the postulate derives the reciprocal UDT metric family:

$$
\boxed{
ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2.
}
$$

This is more than the earlier causal-measure reformulation. Under the new foundation, preservation
of the time-radial measure is a **derived consequence** of reciprocal time-length duality rather
than an independent postulate.

The result does not yet derive a unique action, the profile $\phi(r)$, or the scale $X$.

## 1. Why the derivation is short

Use the dimension-matched temporal/radial coframe pair

$$
q=\begin{pmatrix}c\,dt\\dr\end{pmatrix}.
$$

A positive diagonal positional comparison at relative depth $\Delta$ is

$$
P(\Delta)=
\begin{pmatrix}
u(\Delta)&0\\
0&v(\Delta)
\end{pmatrix}.
$$

Reciprocal-c makes the two entries a physical conversion pair. The Reciprocity Principle says the
positional actions on that pair are dual. Represent the dimensionless evaluation pairing by

$$
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

Preserving the reciprocal pairing gives

$$
P^T K P=K.
$$

But exactly

$$
P^T K P=u(\Delta)v(\Delta)K.
$$

Therefore

$$
\boxed{u(\Delta)v(\Delta)=1.}
$$

This is where metric reciprocity enters. It is **not** a theorem of the number $c$ alone; it is the
mathematical content of applying the independent UDT Reciprocity Principle to the user-proposed
two-way $c$ identity.

## 2. Positional composition fixes the exponential

No position is privileged, so only relative positional depth matters. Continuous comparisons
compose:

$$
P(\Delta_1+\Delta_2)=P(\Delta_1)P(\Delta_2).
$$

Thus

$$
u(\Delta)=e^{a\Delta},
\qquad
v(\Delta)=e^{b\Delta}.
$$

Dual reciprocity gives $a+b=0$. For a nontrivial representation, define the depth normalization
$\phi=-a\Delta$. Then

$$
u=e^{-\phi},
\qquad
v=e^{+\phi}.
$$

Using the local metric readout in the transformed physical coframe,

$$
ds^2=-(u c\,dt)^2+(v\,dr)^2+r^2d\Omega^2,
$$

produces the boxed UDT metric.

### Assumption ledger

| Ingredient | Status | Work performed |
|---|---|---|
| $c$ and $c^{-1}$ are coequal physical conversion directions | **PROPOSED FOUNDATIONAL — Charles Rotter** | Makes time and length a reciprocal physical pair rather than a one-way speed relation. |
| UDT Reciprocity acts contragrediently on that pair | **FOUNDATIONAL INTERPRETATION** | Forces $uv=1$. |
| Relative comparisons compose continuously | **POSIT / positional relativity** | Forces exponential dependence on additive depth. |
| At least one comparison is nonidentity | **OBSERVED or separate POSIT** | Excludes the trivial $u=v=1$ representation. |
| Local Lorentzian quadratic interval and spherical areal sector | **SR-CONTINUITY / DECLARED READOUT** | Converts the coframe scaling into the displayed metric and supplies signature/angular structure. |
| Sign and unit of $\phi$ | **CHOSE** | Coordinate convention on the one-dimensional positional group. |

Consequently it would be inaccurate to say that the arithmetic pair $c,1/c$ alone derives the
metric. It is accurate to say that the user-proposed Reciprocal-c Identity **combined with the
already stated UDT Reciprocity Principle**, positional composition, and local metric continuity
derives it.

## 3. The necessary adversarial alternative

Suppose instead that “$c$ is reversible” means only that $c:\mathcal T\to\mathcal L$ is an ordinary
isomorphism and positional transformations commute with it:

$$
P_L\,c=c\,P_T.
$$

In one dimension this gives

$$
v=u,
$$

not $v=u^{-1}$. The radial metric block would then be conformally scaled:

$$
ds^2_{(t,r)}=u^2(-c^2dt^2+dr^2),
$$

which is not the UDT reciprocal metric unless $u=1$.

This countercase proves two things:

1. invariant local $c$ alone is insufficient;
2. the UDT Reciprocity Principle is doing essential, independently visible work.

It also makes the new postulate falsifiable: if physical time-length conversion transforms
covariantly rather than dually under positional change, this proposed foundation fails to derive
UDT.

## 4. New consequences derived from the foundation

### 4.1 Causal-measure preservation is downstream

Since $uv=1$,

$$
\det P=1,
$$

and

$$
\det g_{(t,r)}=-c^2,
\qquad
\sqrt{-g}=c r^2\sin\theta.
$$

Thus positional dilation redistributes clock and radial-ruler calibration without changing the
adapted metric four-volume. The prior causal-measure principle is no longer required as an
independent foundation if the Reciprocal-c interpretation is accepted.

### 4.2 Positional depth is the unique additive group coordinate

The positional transformation is

$$
S(\phi)=\operatorname{diag}(e^{-\phi},e^{\phi}),
$$

with

$$
S(\phi_1)S(\phi_2)=S(\phi_1+\phi_2),
\qquad
S(-\phi)=S(\phi)^{-1}.
$$

The reversal-even relative comparison is

$$
\frac12\operatorname{Tr}(S_A^{-1}S_B)
=\cosh(\phi_B-\phi_A).
$$

### 4.3 A quadratic infinitesimal geometry is derived

The group current is

$$
J=S^{-1}dS
=\operatorname{diag}(-d\phi,d\phi),
$$

so

$$
\operatorname{Tr}J=0,
\qquad
\boxed{\frac12\operatorname{Tr}(J^2)=d\phi^2.}
$$

Because the positional group has a one-dimensional tangent algebra, every positive invariant
quadratic inner product on it is this norm multiplied by one constant. Therefore the postulate
does derive a canonical quadratic **infinitesimal geometry**, unique up to normalization.

This is an important advance toward an action principle. It is not yet the statement that physical
energy or action equals that norm.

## 5. Why a unique action still does not follow

> **SUBSEQUENT STRONGER AUDIT (2026-07-15):** The full inverse problem for arbitrary regular
> physical-metric $F(Y)$ has now been solved. Making WR-L stationary requires
> $F'(Y)\propto(4X^2Y)^{3/2}/(4X^2Y-1)^2$, which is singular at the regular center and explicitly
> contains $X$. See `UDT_WRL_SCAFFOLD_NATIVE_ACTION_SEPARATION_DERIVATION_RESULTS.md`.

> **SUBSEQUENT METRIC-ONLY FORK (2026-07-15):** If common local time-length scale is additionally
> declared representational, the lowest-order four-dimensional conformal metric action is $C^2$.
> Its full Bach equation admits WR-L with $X$ as a solution constant, but WR-L has $C^2=0$ and is
> not selected. See `UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md`.

For a spacetime-dependent depth field define

$$
Y=\frac12\operatorname{Tr}(J_\mu J^\mu).
$$

The Reciprocal-c Identity and Reciprocity allow

$$
I_F=\int dV_4\,F(Y)
$$

for arbitrary suitable $F$. In particular,

$$
F_1(Y)=\frac12Y,
\qquad
F_2(Y)=\frac12Y+\frac{\alpha}{4}Y^2
$$

obey the same kinematic symmetries but have different nonlinear Euler equations. Hence

$$
\boxed{
\text{reciprocal-c duality derives the quadratic norm, but not a unique physical action.}
}
$$

The missing statement is now sharply isolated: **why must physical cost equal the invariant
quadratic norm rather than an arbitrary function of it?** Exact additivity of independent local
distortions would answer that, but it has not yet been derived from reciprocal-c duality.

### Direct test of the simplest action

Choosing the canonical norm anyway, using the full reciprocal physical metric, and restricting
consistently to a static radial field gives, up to normalization,

$$
I_{\rm can}=\int dr\,r^2 e^{-2\phi}(\phi')^2.
$$

With $A=e^{-2\phi}$ this becomes

$$
I_{\rm can}=\int dr\,\frac{r^2(A')^2}{4A}.
$$

The exact Euler expression evaluated on WR-L, $A=1-r/X$, is

$$
\left.\mathcal E_A\right|_{\rm WR-L}
=-\frac{r(4X-3r)}{4(X-r)^2},
$$

which is nonzero throughout $0<r<X$. Therefore the obvious quadratic group action does **not**
produce WR-L. More action structure is required; inventing it would not be a derivation.

## 6. What happens to $X$

The new local postulate contains no length scale. It derives

$$
A=e^{-2\phi}>0
$$

but permits any positive profile $A(r)$. It cannot select $A=1-r/X$ or the numerical/global value
of $X$.

Nevertheless it clarifies the wall. For WR-L,

$$
\phi(r)=-\frac12\ln\left(1-\frac rX\right),
$$

so

$$
r\to X^-
\quad\Longrightarrow\quad
\phi\to+\infty.
$$

The wall is not a finite endpoint of the reciprocal positional group; it is infinite positional
depth. Thus asymptotic infinite dilation is natural once the WR-L profile is supplied. The local
group still does not determine the areal location $X$ where that infinity is approached.

Therefore:

- **Do not postulate $X$ yet for the local metric/action derivation.**
- Keep $X$ **OPEN / WORKING** as a global boundary datum, solution integration scale, or quantity
  potentially derived from total cosmic data.
- Adopt a fundamental $X_{\max}$ only if the global derivation fails and the owner explicitly
  chooses it.

## 7. Falsification gates

The proposed foundation fails or needs revision if any of the following occurs:

1. positional transformations do not act dually on the $c/c^{-1}$ conversion pair;
2. an operational comparison finds $uv\neq1$ after coordinate gauge is fixed;
3. the full time-live or nonspherical metric cannot extend the reciprocal pairing consistently;
4. nontrivial positional dilation cannot be distinguished from the identity representation;
5. a native UDT dynamical derivation requires a transformation structure incompatible with $S$;
6. cold verification finds that the pairing formulation merely relabels a hidden metric premise.

## 8. Honest conclusion

$$
\boxed{
\begin{gathered}
\text{FOUNDATIONAL CANDIDATE proposed by Charles Rotter: reciprocal-c identity;}\\
\text{DERIVED with UDT Reciprocity and declared continuity premises: reciprocal metric family;}\\
\text{DERIVED: determinant-one group, preserved volume, canonical quadratic tangent norm;}\\
\text{NOT DERIVED: nontriviality, unique action, WR-L radial profile, or }X;\\
\text{FALSIFIED: the obvious quadratic group action as the WR-L action.}
\end{gathered}
}
$$

The brevity of the metric derivation does not make the insight minor. Once the correct one-
dimensional dual structure is identified, the inverse exponential pair is mathematically forced.
The remaining difficulty has moved downstream: from “why this metric structure?” to “what native
dynamical rule selects its physical profile and matter content?”
