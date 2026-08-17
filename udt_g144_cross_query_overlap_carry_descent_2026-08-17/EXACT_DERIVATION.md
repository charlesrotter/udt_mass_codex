# G144 exact derivation — cross-query carry exists exactly on genuine overlap

## 1. The overlap criterion

Let two supplied regular pair realizations be

\[
F_\alpha:\Sigma_\alpha\to M,
\qquad
F_\beta:\Sigma_\beta\to M.
\]

They are two presentations of the same relation on open subsets only when there is a
calibration-compatible diffeomorphism

\[
\psi_{\beta\alpha}:U_\alpha\to U_\beta,
\qquad
F_\beta\circ\psi_{\beta\alpha}=F_\alpha.
\]

If both restrictions are embeddings onto one image patch, this map is uniquely
`F_beta^-1 o F_alpha`. For a self-intersecting immersion, a branch must be supplied before that
inverse is single-valued.

The differential

\[
J_{\beta\alpha}=d\psi_{\beta\alpha}
\]

is the cross-query tangent carry. Pullback naturality gives

\[
h_\alpha=\psi_{\beta\alpha}^*h_\beta,
\qquad
H_\alpha=J_{\beta\alpha}^T H_\beta J_{\beta\alpha}.
\]

On triple overlaps the chain rule gives

\[
J_{\gamma\beta}J_{\beta\alpha}=J_{\gamma\alpha}.
\]

No new carry mechanism is needed once genuine overlap has been proved.

## 2. A genuine same-event overlap transition is isometric

Let endpoint/query factors satisfy

\[
H_i=R_i^T\eta R_i.
\]

The G142 total transition on the overlap is

\[
C_{\beta\alpha}=R_\beta J_{\beta\alpha}R_\alpha^{-1}.
\]

Using the pullback identity,

\[
\begin{aligned}
C_{\beta\alpha}^T\eta C_{\beta\alpha}
&=R_\alpha^{-T}J_{\beta\alpha}^TR_\beta^T\eta
  R_\beta J_{\beta\alpha}R_\alpha^{-1}\\
&=R_\alpha^{-T}H_\alpha R_\alpha^{-1}=\eta.
\end{aligned}
\]

Thus this overlap carry is an isometric change of presentation at the same ambient event, not a
nonisometric positional dilation between different observer events.

On the supplied positive-diagonal upper-triangular stratum, write

\[
C=\begin{pmatrix}a&n\\0&d\end{pmatrix},\qquad a,d>0.
\]

The equation `C^T eta C=eta` gives

\[
1-a^2=0,\qquad -an=0,\qquad d^2-n^2-1=0.
\]

Positivity forces `a=1`, then `n=0`, then `d=1`. Therefore

\[
O(1,1)\cap B^+(2)=\{I\}
\]

in this time/ruler oriented positive component. A genuine same-event overlap contributes zero
reciprocal grading in this gauge.

## 3. Shared observers and endpoints are not an overlap

In Minkowski four-space, consider two strip immersions

\[
F_0(t,s)=(t,s,0,0),
\]

\[
F_\epsilon(t,s)=(t,s,\epsilon s(1-s),0),
\qquad \epsilon>0,quad 0\le s\le1.
\]

They coincide on both observer boundaries `s=0` and `s=1`. Their induced metrics are

\[
h_0=\operatorname{diag}(-1,1),
\]

\[
h_\epsilon=\operatorname{diag}
\left(-1,1+\epsilon^2(1-2s)^2\right),
\]

so both are regular and timelike everywhere. But for `0<s<1`, the third ambient component of
`F_epsilon` is strictly positive while that of `F_0` is zero. Their images have no open interior
overlap; they meet only on the two boundaries. Consequently no map
`F_epsilon^-1 o F_0` exists on an open interior patch, and the shared observers do not supply a
cross-query differential carry.

This is not a claim that both strips are physical. It is an exact type countermodel: endpoint
incidence alone cannot prove that two query sheets are the same relation.

## 4. Resulting architecture

There are now three clean cases:

1. One calibrated query chart: G143 identity carry presentation.
2. Different charts/queries on a proved common relation overlap: `d psi` supplies isometric carry,
   with exact cocycle descent.
3. Distinct or unproved relation sheets: no cross-query carry is owned merely by common observers
   or endpoints; keep the branch labels separate.

This closes the carry question at the kinematic evaluation level. It does not select which relation
sheets Nature realizes, a complete metric history, proper length, or `X_max`.
