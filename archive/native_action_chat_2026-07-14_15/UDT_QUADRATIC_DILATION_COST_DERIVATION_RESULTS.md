# Deriving quadratic dilation cost from existing UDT premises — results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + countermodel audit; DATA-BLIND |
| Repository | grok at 64af120; unrelated dirt preserved |
| MAP | UDT_QUADRATIC_DILATION_COST_DERIVATION_MAP.md, SHA-256 b14cdb8d5b58e4e0da6f726e7c88c14dcbf7c25ef0a7ed02c6088069b030e09f |
| Driver | DISCLOSED NON-COLD |
| Symbolic verifier | verify_udt_quadratic_dilation_cost.py — **26/26 checks pass**, SymPy 1.13.3 |
| GPU | Not used; no determined numerical problem emerged |
| Independent verification | **OPEN** |
| Build-on grade | **CONDITIONAL QUADRATIC TANGENT NORM; FULL ACTION NOT DERIVED**, not banked |

No GR field equation, EH action, carrier, observed mass, fit, cutoff, or imported SR energy formula
is used.

## 0. Result

The attempted derivation succeeds at one level and fails at the two stronger levels:

$$
\boxed{
\begin{array}{rcl}
\text{Invariant infinitesimal dilation-state norm}
&:& \textbf{CONDITIONAL-DERIVED},\\
\text{Exact full local quadratic action}
&:& \textbf{NOT DERIVED},\\
\text{Specific WR-L inverse functional}
&:& \textbf{NOT DERIVED}.
\end{array}}
$$

The additive dilation depth is $\phi$. If one asks for a smooth Riemannian line element on its
one-dimensional state space that is invariant under common-depth shifts and reciprocity, then

$$
\boxed{d\sigma^2=Z\,d\phi^2}
$$

is unique up to the positive normalization $Z$. In residual variables,

$$
A=e^{-2\phi},\qquad B=1-A,
$$

this same norm is

$$
\boxed{
d\sigma^2
=\frac{Z}{4}\frac{dA^2}{A^2}
=\frac{Z}{4}\frac{dB^2}{(1-B)^2}.
}
$$

That is a real result: the natural quadratic coordinate is the additive depth $\phi$, not the
linear depletion $B=1-A$.

But a spacetime/local field action may still be

$$
S_F=\int d\mu\,F(Y),
\qquad
Y=\mathcal G^{ab}\partial_a\phi\,\partial_b\phi,
$$

and every smooth $F$ respects common-depth shifts and reversal. For example,

$$
F_1(Y)=\frac12Y,
\qquad
F_2(Y)=\frac12Y+\frac{\alpha}{4}Y^2
$$

obey the same existing UDT symmetries but have different full nonlinear Euler equations. Therefore
the state-space metric fixes how an infinitesimal displacement is measured; it does not force the
action to be linear in that squared displacement.

Most decisively, the WR-L inverse functional

$$
\mathcal I_0[A]
=\frac12\int dr
\left[r(A')^2+\frac{(A-1)^2}{r}\right]
$$

uses a flat $dB^2$ kinetic metric and an additional $B^2/r$ term. Neither follows from
$d\phi^2$. Hence:

$$
\boxed{
\text{Existing UDT derives a quadratic infinitesimal geometry, but not the quadratic WR-L dynamics.}
}
$$

## 1. Exact dilation-state geometry

R1/R2 make depth additive:

$$
\phi\mapsto\phi+C,
$$

while reciprocity reverses a comparison:

$$
\Delta\phi\mapsto-\Delta\phi.
$$

Write a general one-dimensional Riemannian state metric as

$$
d\sigma^2=h(\phi)\,d\phi^2.
$$

Translation invariance for every $C$ requires

$$
h(\phi+C)=h(\phi)
\quad\Longrightarrow\quad
h'(\phi)=0.
$$

Thus $h=Z>0$. Reflection is then automatically an isometry. This proves uniqueness inside the
explicitly named class of smooth Riemannian state metrics.

The qualification is load-bearing: the founding postulates do not themselves say that dynamics is
the integral of this state-space squared length. “Metric is the theory” fixes physical comparison
geometry; promoting a new field-space metric to the action is an additional dynamical step.

## 2. What reciprocity says about finite costs

For two positions,

$$
D=e^{\Delta\phi},
\qquad
D^{-1}=e^{-\Delta\phi}.
$$

Their arithmetic reciprocal invariant is

$$
\Gamma
=\frac12(D+D^{-1})
=\cosh\Delta\phi.
$$

Its excess has the exact square form

$$
\boxed{
\Gamma-1
=\cosh\Delta\phi-1
=\frac12\left[2\sinh\left(\frac{\Delta\phi}{2}\right)\right]^2.
}
$$

So the simplest reciprocal excess is exactly quadratic in a hyperbolic chord variable. This is the
closest exact realization of the owner's SR-like intuition.

However, reciprocity permits every

$$
C_F(\Delta\phi)=F(\cosh\Delta\phi),
\qquad F(1)=0.
$$

For smooth $F$,

$$
C_F
=\frac{F'(1)}2(\Delta\phi)^2
+\left[\frac{F'(1)}{24}+\frac{F''(1)}8\right](\Delta\phi)^4
+O((\Delta\phi)^6).
$$

Thus a nondegenerate cost with $F'(1)>0$ has a quadratic leading term. But

$$
C_4=(\cosh\Delta\phi-1)^2
=\frac14(\Delta\phi)^4+O((\Delta\phi)^6)
$$

obeys the same existing symmetries and has zero quadratic stiffness at coincidence. Reciprocity
does not forbid it.

Therefore:

$$
\boxed{
\text{quadratic leading response}
\Longleftrightarrow
\text{smooth reciprocal cost plus a nondegenerate Hessian premise}.
}
$$

The nondegenerate-Hessian premise is physically reasonable, but it is not presently a derived UDT
theorem.

## 3. Controlled local limit of reciprocal resistance

There is a second route. Let $W(z)$ be an even local kernel and consider

$$
E_\ell
=\frac{1}{\ell^2}
\int d\mu(x)\int d^nz\,W(z)
\left[
\cosh\!\left(\phi(x+\ell z)-\phi(x)\right)-1
\right].
$$

For a smooth field,

$$
\phi(x+\ell z)-\phi(x)
=\ell z^i\partial_i\phi+O(\ell^2).
$$

If the second kernel moment is

$$
M^{ij}=\int d^nz\,W(z)z^iz^j,
$$

then evenness removes the odd orders and

$$
\boxed{
E_\ell
=\frac12\int d\mu\,M^{ij}\partial_i\phi\,\partial_j\phi
+O(\ell^2).
}
$$

For an isotropic kernel, $M^{ij}$ is proportional to the inverse spatial metric. Therefore a
quadratic scalar-gradient cost is the unique controlled zero-range limit after choosing:

1. locality through $\ell\to0$;
2. an even pair kernel;
3. an isotropic second moment;
4. the $\ell^{-2}$ normalization;
5. a nonzero second moment and a base measure.

These choices were not all supplied by the founding postulates. The limit also removes the exact
finite-separation barrier: quartic and higher reciprocal terms vanish as $O(\ell^2)$.

### Wall control fails uniformly

For WR-L,

$$
\phi'=\frac{1}{2(X-r)}.
$$

In a symmetric one-dimensional pair expansion, the relative first correction is

$$
\frac{\Delta C}{C_2}
=\frac{15}{16}\frac{\ell^2}{(X-r)^2}
+\cdots.
$$

The local quadratic approximation is controlled on every interior region
$r\le X-\epsilon$ when $\ell\ll\epsilon$. It is not uniformly controlled as $r\to X$. Consequently
the local-limit theorem cannot be extrapolated to the WR-L wall without a boundary-layer theory or
an exact nonlocal action.

## 4. Why local covariance does not finish the derivation

Once a base metric and measure are chosen, define

$$
Y=\mathcal G^{ab}\partial_a\phi\,\partial_b\phi.
$$

The general local first-gradient action is

$$
S_F=\int d\mu\,F(Y),
$$

with Euler equation

$$
\nabla_a\left(2F_Y\nabla^a\phi\right)=0.
$$

Both $F_1$ and $F_2$ above are local, reciprocal-even, common-depth shift invariant, and use the same
metric contraction. Their equations are different. Full covariance tells us how to form $Y$; it
does not require the action to be linear in $Y$.

This also shows why a quadratic spacetime line element does not prove a quadratic field action.
Functions such as $Y^2$ remain scalars.

## 5. Exact additivity would select the quadratic action

There is one clean selector theorem. Suppose a spatial local cost depends only on squared gradient
length:

$$
C(u)=f(|u|^2),\qquad f(0)=0.
$$

For orthogonal gradients $u\perp v$,

$$
|u+v|^2=|u|^2+|v|^2.
$$

If independent orthogonal dilation gradients have exactly additive costs,

$$
C(u+v)=C(u)+C(v),
$$

then

$$
f(x+y)=f(x)+f(y),\qquad x,y\ge0.
$$

Continuity gives the unique solution

$$
\boxed{f(x)=\kappa x.}
$$

This would eliminate every $Y^2,Y^3,\ldots$ counterterm and derive an exact quadratic local
gradient cost.

But **orthogonal additivity at the same point is not currently an R1/R2/R3 theorem**. Locality only
guarantees additivity over disjoint regions; it does not guarantee that overlapping orthogonal
field components do not interact. Moreover the current UDT metric construction fixes the
gradient-parallel reciprocal slot while the transverse off-shell structure remains open.

Thus orthogonal additivity is the smallest identifiable new principle that would select
$F(Y)=\kappa Y$. It must not be silently attributed to existing reciprocity.

## 6. Direct WR-L comparison

For WR-L,

$$
A=1-\frac rX,
\qquad
B=\frac rX,
\qquad
\phi=-\frac12\ln A.
$$

The invariant state metric becomes

$$
d\phi^2
=\frac14\frac{dB^2}{(1-B)^2}.
$$

The factor $(1-B)^{-2}=A^{-2}$ diverges at the wall. The inverse functional
$\mathcal I_0$ instead uses the flat kinetic term $dB^2$. The two agree only at leading weak depth:

$$
\frac{1}{4(1-B)^2}
=\frac14+\frac B2+\frac{3B^2}{4}+\cdots,
$$

and WR-L spans the full interval $0\le B<1$. The weak-depth replacement is therefore uncontrolled
globally.

The shift-clean quadratic depth action with the historical radial measure gives

$$
(r^2\phi')'=0.
$$

On WR-L,

$$
(r^2\phi')'
=\frac{r(2X-r)}{2(X-r)^2}
\ne0.
$$

A four-dimensional scalar kinetic contraction reduced consistently to the reciprocal one-field
metric likewise has radial density

$$
L_{\rm cov}
=\frac{r^2(A')^2}{4A}
$$

and Euler residual

$$
E_A\big|_{\rm WR-L}
=-\frac{r(4X-3r)}{4(X-r)^2}
\ne0.
$$

Finally, a pure state-space norm supplies no derivation of the additional WR-L term

$$
\frac{(A-1)^2}{r}.
$$

Therefore no presently derived quadratic norm reproduces the complete WR-L inverse functional.

## 7. Why even a derived quadratic Hessian would be insufficient

The prior off-shell audit constructed nonlinear actions $L_\lambda$ with

$$
E[L_\lambda]
=r\left[
1+\frac{\lambda}{16}(B^2-r^2(B')^2)^2
\right]
\left(B''+\frac{B'}r-\frac{B}{r^2}\right).
$$

On WR-L, $B=r/X$, so

$$
B^2-r^2(B')^2=0.
$$

The linearized Euler multiplier is therefore exactly $r$ for every $\lambda$. The whole
counterfamily has the same quadratic fluctuation equation around WR-L even though its nonlinear
action and boundary momentum differ.

Hence deriving the quadratic infinitesimal response does not select the nonlinear action or mass
generator. Higher off-shell information is mathematically necessary.

## 8. Status ledger

| Claim | Status |
|---|---|
| Reciprocal mean $\Gamma=\cosh\Delta\phi$ | **DERIVED algebraic readout** |
| $\Gamma-1$ is an exact chord square | **DERIVED** |
| Unique invariant Riemannian metric on additive depth space | **CONDITIONAL-DERIVED**, given Riemannian state-cost class |
| Every reciprocal cost begins quadratically | **FALSE** without nondegenerate Hessian |
| Smooth nondegenerate reciprocal cost begins quadratically | **DERIVED leading-order statement** |
| Even/isotropic zero-range pair limit is quadratic | **CONDITIONAL-DERIVED**, controlled away from wall |
| Exact finite-$X$ barrier survives that local limit | **FALSE** |
| R1/R2/R3 plus covariance force $F(Y)\propto Y$ | **FALSE / counterfamily survives** |
| Orthogonal additivity forces $F(Y)=\kappa Y$ | **DERIVED mathematical theorem** |
| Orthogonal additivity is already a UDT principle | **NOT DERIVED** |
| Invariant depth norm produces $\mathcal I_0[A]$ | **FALSE** |
| Existing premises uniquely determine quadratic WR-L dynamics | **NOT DERIVED** |

## 9. Honest conclusion and next step

The requested derivation was worth doing. It narrows the missing principle sharply:

$$
\boxed{
\begin{gathered}
\text{UDT already contains a natural quadratic infinitesimal depth geometry;}\\
\text{what it lacks is a rule saying local costs of independent metric directions add exactly,}\\
\text{plus the measure/boundary structure that generates the WR-L potential term.}
\end{gathered}}
$$

No GPU numerics are justified. The next action is independent CPU verification. After that, the
owner has an honest conceptual choice:

1. derive orthogonal additivity from a stronger statement about the UDT metric product structure; or
2. adopt it explicitly as a new off-shell principle; or
3. retain the nonlinear allowed family and seek another action selector.

Even option 1 or 2 would select only the quadratic gradient dependence. A separate derivation would
still be required for the radial measure, the $(A-1)^2/r$ term, and the boundary generator.

## 10. Self-audit

- No SR kinetic-energy formula was imported as UDT dynamics.
- A field-space Riemannian metric was labeled as a class premise.
- Leading-order quadratic response was not extrapolated to the nonlinear WR-L wall.
- The zero-range kernel assumptions and $O(\ell^2)$ loss of the barrier were displayed.
- The invariant additive-depth metric was not replaced by a flat residual metric.
- Covariance was not treated as a ban on nonlinear scalar functions.
- The existing $L_\lambda$ counterfamily was retained.
- Independent verification remains OPEN.

## 11. Reproduction

With SymPy 1.13.3:

    python3 verify_udt_quadratic_dilation_cost.py

The script verifies 26 exact identities. Passing verifies the encoded algebra, not adoption of a
quadratic UDT action.

