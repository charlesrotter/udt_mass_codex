# G275 exact derivation — projective position, one scale, and Xmax separation

Date: 2026-08-26

## Landing

```text
W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT
__ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE
__DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY
__XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION
```

This is a bounded `DERIVED_CONDITIONAL` theorem after W5 and a supplied complete dimensionless
history. It neither selects an anchor nor promotes the attached scale to `X_max`.

## 1. Constant homothety

Let

\[
g_\ell=\ell^2\bar g,\qquad \ell>0.
\]

Because \(\ell\) is constant,

\[
g_\ell^{-1}=\ell^{-2}\bar g^{-1},\qquad
\partial g_\ell=\ell^2\partial\bar g,
\]

and the factors cancel in the Levi-Civita formula:

\[
\Gamma[g_\ell]^a{}_{bc}=\Gamma[\bar g]^a{}_{bc}.
\]

If an orthonormal endpoint frame is \(U\), then

\[
U_\ell=\ell^{-1}\bar U
\]

is orthonormal for \(g_\ell\). For a supplied transported frame map \(P\),

\[
\Lambda_\ell
=U_{B,\ell}^{-1}P U_{A,\ell}
=(\ell\bar U_B^{-1})P(\ell^{-1}\bar U_A)
=\bar\Lambda.
\]

Therefore its complete projective clock column

\[
\boldsymbol\chi(\Lambda)
=\frac{(\Lambda^1{}_0,\Lambda^2{}_0,\Lambda^3{}_0)}{\Lambda^0{}_0},
\qquad \|\boldsymbol\chi\|<1,
\]

is homothety invariant. W5 identifies this complete, screen-retaining state with physical
**normalized** pair position. It does not fix \(\ell\).

## 2. Full frame carry remains necessary

The exact active-screen witness uses two noncollinear boosts and a nontrivial right spatial carry.
The carry leaves the projective clock column of the individual arrow unchanged but changes the
projective state after composition. Hence neither \(\boldsymbol\chi\) nor

\[
\mathbf x=\ell\boldsymbol\chi
\]

is a standalone nonradial composition law. The full path-labelled frame morphism remains the
composable object. Attaching a dimension does not discard the angular/screen orchestra.

On the radial stratum only,

\[
\chi=\tanh\delta,
\qquad
x=\ell\tanh\delta.
\]

The second equation is a conditional dimensional representative, not a new kernel equation.

## 3. One matched anchor

Suppose one independently calibrated datum is attached to the exact same geometric object and has
known nonzero homothety weight \(w\):

\[
O_\ell=\ell^w\bar O,\qquad w\ne0,\qquad O_*,\bar O>0.
\]

Then the unique positive scale is

\[
\boxed{\ell=\left(\frac{O_*}{\bar O}\right)^{1/w}}.
\]

For every real \(w\ne0\), the map \(\ell\mapsto\ell^w\) is strictly monotone on the positive
half-line, so the positive solution is unique. Equivalently, writing \(\ell=e^s\) turns the anchor
equation into \(\log(O_*/\bar O)=ws\).

Exact positive and negative weights \(-3,-2,-1,1,2,3\) were checked. A second independent anchor
must return the same \(\ell\); it tests the supplied dimensionless history rather than introducing
a second scale. A zero-weight datum is scale blind.

The observed conversion \(c_E\) has unit type \(L T^{-1}\). No power of \(c_E\) alone has unit type
\(L\): the length exponent would require power 1 while eliminating time requires power 0. A
proper-clock attachment can fix \(\ell\) through the already audited G252 contract, after which
\(c_E\) converts the attached time to length.

## 4. Attached scale is not automatically Xmax

For a supplied physical relation domain \(\mathcal R\) in the open projective ball, define

\[
q_{\mathcal R}=\sup_{\mathcal R}\|\boldsymbol\chi\|,
\qquad
X_{\rm sup}(\mathcal R)=\ell q_{\mathcal R}.
\]

Then

\[
0\le q_{\mathcal R}\le1,
\qquad
X_{\rm sup}(\mathcal R)\le\ell.
\]

For \(\ell>0\), equality holds exactly when \(q_{\mathcal R}=1\). A finite-domain control with
\(q_{\mathcal R}=9/10\) gives \(X_{\rm sup}=9\ell/10<\ell\). A separately populated sequence

\[
q_n=\frac{n}{n+1}\longrightarrow1
\]

gives the conditional equality \(X_{\rm sup}=\ell\). An empty or unpopulated domain supplies no
such supremum witness.

Thus an anchor fixes the ruler multiplier \(\ell\); it does not prove which relations Nature
populates or that they approach the projective boundary. The identification

\[
X_{\max}=\ell
\]

requires a separately owned global populated-boundary completion.

## Scope

No observational value, fitted coefficient, profile, field equation, source, action, matter law,
GPU solve, protected package, or numerical `X_max` entered. The founding metric, reciprocal kernel,
W5 projective state, and GR-quiet angular cancellation were not modified.
