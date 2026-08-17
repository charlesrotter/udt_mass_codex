# G131 exact derivation — terminal reciprocal scalar determines conformal geometry

Date: 2026-08-16

## 1. Result

On a shared open regular all-plane certification domain,

\[
\Phi_g(A)=\Phi_{\widetilde g}(A)\quad\hbox{for every }A=[t,r]
\]

holds if and only if

\[
\widetilde g=\lambda g,\qquad \lambda>0.
\]

Pointwise on a smooth covered region, the factor may vary:

\[
\widetilde g(x)=\Omega(x)^2g(x),\qquad \Omega(x)>0.
\]

Thus the complete terminal-scalar network is faithful to the positive conformal class, not to the
full metric.

```text
ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY
__COMMON_SCALE_OPEN
```

This is a classification of a supplied scalar valuation. It does not derive the physical query
population or the scalar values.

## 2. Remove the logarithm

For a known plane embedding `A=[t,r]`, write

\[
a_g=g(t,t),\qquad b_g=g(t,r),\qquad c_g=g(r,r).
\]

The terminal formula is

\[
\Phi_g(t,r)=\frac14\log Q_g(t,r),
\]

where

\[
Q_g(t,r)=\frac{b_g^2-a_gc_g}{a_g^2}
=\frac{-\det(A^TgA)}{g(t,t)^2}>0.
\]

The logarithm is injective, so equality of `Phi` is exactly equality of `Q`.

## 3. Positive conformal factors are invisible

For every positive `lambda`, all three pair entries scale by `lambda`. Therefore

\[
Q_{\lambda g}(t,r)
=\frac{\lambda^2(b_g^2-a_gc_g)}{\lambda^2a_g^2}
=Q_g(t,r).
\]

Consequently

\[
\Phi_{\lambda g}(t,r)=\Phi_g(t,r).
\]

Exact metric faithfulness is impossible from `Phi` alone.

## 4. No larger kernel survives all plane tilts

Assume `g` and `g_tilde` give equal `Q` on a shared open regular domain. Choose one common timelike
vector and a basis in which

\[
g=\eta=\operatorname{diag}(-1,1,1,1),\qquad t_0=e_0.
\]

Write the second Lorentz form in blocks

\[
\widetilde g=
\begin{pmatrix}
a&b^T\\
b&C
\end{pmatrix},
\qquad a<0.
\]

### 4.1 Every ruler with one fixed clock

For a spatial ruler `r=(0,x)`, the reference scalar is

\[
Q_\eta(e_0,r)=x^Tx.
\]

Equality for every `x` gives

\[
\frac{(b^Tx)^2-a\,x^TCx}{a^2}=x^Tx.
\]

As a quadratic-form identity,

\[
bb^T-aC=a^2I_3,
\]

hence

\[
C=\frac{bb^T}{a}-aI_3. \tag{1}
\]

One clock direction therefore leaves four apparent parameters: `a` and the three components of
`b`. This is why one radial or frozen observer family cannot settle the scalar kernel.

### 4.2 Tilt the clock

Now keep `r=(0,x)` and use the nearby clock

\[
t_\epsilon=e_0+\epsilon(0,x).
\]

The shared open-domain hypothesis makes this a legal comparison for sufficiently small
`epsilon`. For the reference metric,

\[
\left.\frac{d}{d\epsilon}Q_\eta(t_\epsilon,r)\right|_{\epsilon=0}=0.
\]

Substituting (1) into the second metric and differentiating exactly gives

\[
\left.\frac{d}{d\epsilon}Q_{\widetilde g}(t_\epsilon,r)
\right|_{\epsilon=0}
=-\frac4a(x^Tx)(b^Tx). \tag{2}
\]

Equality for every spatial `x` makes (2) vanish identically. Taking `x=e_1,e_2,e_3` yields

\[
b=0.
\]

Equation (1) then reduces to

\[
C=-aI_3,
\]

so

\[
\widetilde g=(-a)\eta.
\]

Because `a<0`, the factor `lambda=-a` is positive. Undoing the basis choice proves

\[
\boxed{\widetilde g=\lambda g,\quad\lambda>0.}
\]

Only an open set is needed: after multiplying by the nonzero clock-norm denominators, equality of
the two rational `Q` functions becomes a polynomial identity in the components of `t` and `r`.
Equality on a nonempty open subset makes that polynomial vanish identically. The unrestricted `x`
steps above are therefore consequences of the shared open-domain hypothesis, not an added
all-vector premise.

The proof is nonlinear. The executable differentiates the exact rational function, not a
linearized metric ansatz.

## 5. Why the shared open domain is load-bearing

The comparison requires known identical embeddings `A` and a nonempty full-dimensional common
regular open set in the ordered-embedding topology of `V x V`. If the scalar functions are declared
only on disjoint metric-dependent domains, or on a lower-dimensional frozen-clock slice, equality
does not support this conclusion. G131 therefore proves a faithfulness theorem for one supplied
common certification domain, not a theorem that the founding postulates populate that domain
physically.

## 6. Smooth pointwise extension and curvature witness

Applying the theorem at every point gives

\[
\widetilde g(x)=\Omega(x)^2g(x),\qquad\Omega(x)>0.
\]

The factor is not merely a coordinate convention. Take Minkowski `eta` and

\[
\Omega(x)=1+x^2,
\qquad
\widetilde g=(1+x^2)^2\eta.
\]

Every terminal scalar on every common regular pair plane is identical for the two metrics, but a
direct Christoffel/Ricci calculation gives

\[
R[\widetilde g]=\frac{-12}{(1+x^2)^3},
\]

while `R[eta]=0`. The independent finite-jet implementation recovers `R=-12` at the origin without
using the production curvature formula.

So the all-plane scalar network fixes causal/conformal geometry but not complete curvature or
proper scale.

## 7. What fixed `c_E` does and does not fix

`c_E` is load-bearing as the observed conversion that makes the clock and ruler coordinates
dimensionally commensurate. Once those coordinates are calibrated, the terminal scalar is the
dimensionless ratio

\[
\frac{-\det h}{h_{00}^2}.
\]

A common rescaling `h -> lambda h` cancels exactly. Therefore fixed `c_E` does not by itself supply
the missing pointwise `lambda` or `Omega(x)`.

This does not make UDT scale-free. It says only that this one reciprocal readout is common-scale
blind. A full pullback `h`, one independent norm/area/volume density, or an equivalent common-scale
channel can remove the ambiguity if that datum is natively owned.

## 8. The new narrowed joint

G129 showed that full pair pullbacks recover the metric. G130 showed that co-presence and
Reciprocity do not assign their values. G131 now places the terminal scalar precisely between them:

```text
all-plane Phi values  <->  conformal Lorentz geometry
all-plane full h      <->  complete Lorentz metric
```

Only one type of information separates the two: common local scale.

The next bounded question is therefore concrete:

> Does any already-derived, query-independent norm, area, or volume density of known conformal
> weight own the common scale that completes the conformal metric?

The reciprocal measure and angular/areal sector are candidates to audit, not presupposed owners.

No action, source, bootstrap mechanism, observational fit, or preferred history should be invented
before that ownership question is answered.
