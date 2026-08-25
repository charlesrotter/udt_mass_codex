# G259 exact derivation — metric-only parent-operator fork

Date: 2026-08-25

## 1. Primary landing

```text
CONDITIONAL_LOVELOCK_CLASS_SELECTS_EINSTEIN_ZERO_SET
__CLASS_ASSUMPTIONS_NOT_UDT_DERIVED
__EXTREME_METRIC_DEPARTURE_REQUIRES_EXPLICIT_NEW_STRUCTURE
__SOURCE_HISTORY_REMAINS_OPEN
```

The result is a conditional classification theorem, not a derivation of the Einstein equation from
F1--F4/W1/W3 and not a modified-gravity proposal.

## 2. The exact conditional class

Consider a four-dimensional Lorentz metric and a candidate vacuum operator

\[
\mathcal E_{ab}[g]
\]

that is:

1. natural under diffeomorphisms;
2. a symmetric rank-two tensor;
3. local in the metric through second differential order;
4. divergence-free as an identity.

The exact theorem scope and hypothesis map are recorded in `LOVELOCK_NAVARRO_SCOPE.md`. Navarro's
stronger Theorem 5.3 classifies smooth natural two-contravariant tensors on the fixed-signature
metric two-jet bundle whose divergence vanishes identically. It does not require symmetry as a
separate hypothesis; the resulting two-index Lovelock basis is symmetric. In four dimensions the
bound `2m <= n-1` leaves only the inverse metric and Einstein tensor. Lowering indices gives

\[
\boxed{\mathcal E_{ab}=aG_{ab}+b g_{ab}.}
\]

This use of the theorem is mathematical method. The four numbered restrictions are additional
operator-class premises. F1--F4 derive the reciprocal metric form; W1 completes a supplied pair;
W3 requires GR reduction. None of them proves all four restrictions.

References: José Navarro, “On second-order, divergence-free tensors,” arXiv:1306.4354, Theorem 5.3;
Alberto Navarro and José Navarro, “Lovelock's theorem revisited,” arXiv:1005.2386.

## 3. What quiet-flat inclusion and W3 actually fix

On a flat quiet-vacuum member,

\[
G_{ab}=0.
\]

Because the metric is nondegenerate, requiring this member to satisfy
\(\mathcal E_{ab}=0\) forces

\[
b=0.
\]

Thus

\[
\mathcal E_{ab}=aG_{ab}.
\]

The degenerate case \(a=0\) is the identically zero operator. Its equation accepts every metric,
so it is not a physical parent law and does not have the Einstein vacuum zero set. It is explicitly
excluded from the conditional landing. No sign or normalization of the remaining nonzero \(a\) is
selected.

For nonzero \(a\), the vacuum zero set is exactly

\[
\boxed{G_{ab}=0.}
\]

The value of \(a\) is irrelevant to the vacuum zero set. Its physical normalization becomes
meaningful only after a source tensor and coupling are supplied. W3 can normalize the GR
comparison convention, but it does not create that source attachment.

Therefore the conditional theorem is precise:

> If the UDT parent operator belongs to the declared Lovelock class and is a nonidentity equation,
> its flat-compatible vacuum zero set is Einstein's. This does not prove that UDT owns the
> Lovelock-class assumptions or select the nonzero normalization.

## 4. Primary spherical reduction and source freedom

For

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\]

the two displayed Einstein residuals are

\[
\mathcal E_0=rf'+f-1,
\]

\[
\mathcal E_1=rf'+\frac{r^2}{2}f''.
\]

They obey

\[
\boxed{r\frac{d\mathcal E_0}{dr}=2\mathcal E_1.}
\]

Vacuum therefore has one independent equation and the complete positive-interval family

\[
\boxed{f=1+\frac Cr.}
\]

Now define the dimensionless geometric mass aspect

\[
\mu(r)=\frac r2(1-f(r)).
\]

This is merely a change of variables; it does not assert matter. Direct substitution gives

\[
\boxed{\mathcal E_0=-2\mu',\qquad \mathcal E_1=-r\mu''.}
\]

Hence:

- vacuum fixes \(\mu'=0\) and gives the one-constant GR exterior;
- an arbitrary supplied primary profile is equivalent to an arbitrary supplied \(\mu(r)\);
- an Einstein-type metric operator with an unspecified right-hand side does not select the
  history—the missing freedom has moved into the source/constitutive history.

Introducing dimensions through

\[
M(r)=\frac{c_E^2}{G_{\rm obs}}\mu(r)
\]

would be an observational source attachment. G259 does not declare it to be a UDT matter law.

## 5. Relaxing the class immediately restores nonuniqueness

Varying the natural local functional \(\int R^2\sqrt{-g}\,d^4x\) gives the symmetric,
identity-divergence-free tensor

\[
H^{(R^2)}_{ab}
=2RR_{ab}-\frac12g_{ab}R^2
+2\left(g_{ab}\Box-\nabla_a\nabla_b\right)R.
\]

It is fourth order in the metric and vanishes on every Ricci-flat metric. Consequently every member
of the family

\[
\boxed{
\mathcal E^{(\lambda)}_{ab}
=G_{ab}+\lambda\ell^2H^{(R^2)}_{ab}
}
\]

retains the exact G257 quiet vacuum branch for arbitrary \(\lambda\), while differing away from it.

On the explicit time-live control

\[
ds^2=-dt^2+e^{2bt^2}(dx^2+dy^2+dz^2),
\]

the exact values at \(t=0\) are

\[
H^{(R^2)}_{00}=-72b^2,
\qquad
\frac{H^{(R^2)}_{ij}}{g_{ij}}=-216b^2.
\]

The production calculation also verifies the identity-level FLRW divergence residual is zero.
Thus \(\lambda=1\) and \(\lambda=2\) are explicit inequivalent continuations that agree on every
Ricci-flat quiet metric. W3 alone cannot choose between them.

This family is a counterexample, not a candidate UDT law. It demonstrates the exact cost of leaving
the second-order class.

## 6. Scale audit

The Einstein tensor has inverse-length-squared dimension; \(H^{(R^2)}_{ab}\) has
inverse-length-fourth dimension. Their sum therefore requires a coefficient \(\ell^2\).

Let

\[
[c_E]=L T^{-1},
\qquad
[G_{\rm obs}]=L^3M^{-1}T^{-2}.
\]

For \(c_E^xG_{\rm obs}^y\) to be a pure length, mass neutrality forces \(y=0\), time neutrality
then forces \(x=0\), and the remaining length exponent is zero rather than one. Therefore

\[
\boxed{c_E\ \text{and}\ G_{\rm obs}\ \text{alone do not supply}\ \ell.}
\]

A mass, density, global attachment, integration constant, or new dimensionful premise would be
required. G259 does not choose one.

## 7. Why the reciprocal scalar does not yet evade the fork

On a positive untrapped spherical branch, areal radius \(R\) is geometrically supplied by the
symmetry orbits and

\[
e^{-2\phi}=\lVert\nabla R\rVert_g^2,
\qquad
\phi=-\frac12\log\lVert\nabla R\rVert_g^2.
\]

So \(\phi\) is metric-reconstructible in that declared branch. A generic four-dimensional metric
has no canonical spherical areal-radius scalar or preferred pair plane. Promoting \(\phi\), the
group current \(\mathcal J\), or a `2+2` split to an independent global field would therefore be
additional relational structure—not a metric-only consequence already derived by F1--F4.

## 8. Why G258 cannot choose this fork

G258 fixes twelve conditional values \((R_i,f_i)\) up to one scale, but it supplies no continuous
first or second derivatives and no native source residual.

For any twelve distinct radii, define

\[
P(R)=\prod_{i=1}^{12}(R-R_i).
\]

If \(f_0\) is one regular interpolant, then

\[
f_\epsilon=f_0+\epsilon P
\]

has exactly the same twelve values. For sufficiently small \(\epsilon\) on a compact regular
interval it preserves positivity, while

\[
P'(R_i)=\prod_{j\ne i}(R_i-R_j)\ne0.
\]

Thus the GR residual, a fourth-order residual, and any inferred source derivative can change while
all twelve G258 knots remain fixed. The knots are legitimate future tests only after an operator
and source/transfer family reduce the freedom.

## 9. The narrowed scientific fork

The current options are now sharply typed:

1. **GR metric dynamics, UDT relational novelty.** Adopt the conditional local second-order class.
   The vacuum metric operator is Einstein's; UDT-specific behavior must arise through the completed
   observer-pair readout and a still-missing source/population/transfer history.
2. **Modified metric dynamics.** UDT must explicitly own at least one assumption outside that
   class: higher metric order plus its scale, a nonlocal/global completed-relation operator, or an
   additional covariant reciprocal state.

Current premises select neither fork. The result nevertheless removes an important ambiguity:
there is no hidden non-GR local second-order metric-only tensor waiting inside the existing
four-dimensional natural/divergence-free class.

## 10. Exact conclusion ceiling

G259 conditionally selects the Einstein vacuum zero set only after four explicit operator-class
premises and the nonidentity `a != 0` equation gate are added. The excluded `a=0` operator would
accept every metric. G259 does not derive the class premises from UDT, select a source history,
prove that local metric dynamics remains GR, or prove that UDT modifies it. It does show precisely
what any claimed loud-end metric modification must add and why G258's present value knots cannot
make that choice.
