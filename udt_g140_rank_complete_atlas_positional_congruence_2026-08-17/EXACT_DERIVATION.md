# G140 exact derivation — constant-metric faithfulness does not imply positional congruence

## 1. Two different closure questions

For supplied pair differentials `J_e` at one event, G129 pointwise metric faithfulness asks whether

\[
\mathcal M_J:g\longmapsto\{J_e^TgJ_e\}_e
\]

has rank ten. In the separated affine control below, the analogous pooled design reconstructs one
constant metric coefficient matrix because Minkowski affine structure canonically identifies all
tangent spaces. It is not a pointwise atlas for an arbitrary varying metric.

G138 positional descent instead asks whether a separately oriented scalar edge cochain obeys

\[
\sum_{e\in C}\delta_e=0
\]

on every matched composable cycle. Constant-metric reconstruction and endpoint descent are
different conditions; the following same-metric controls show that the first does not imply the
second.

## 2. One metric, explicit shared calibration, and affine pair strips

Choose a common positive length unit `ell_0` and its reciprocal clock unit

\[
\tau_0=\frac{\ell_0}{c_E}.
\]

Write `\hat y=t/\tau_0` and `\hat p=p/\ell_0`. In the dimensionless Minkowski affine chart use

\[
g=\operatorname{diag}(-1,1,1,1).
\]

Four static observer worldlines have dimensionless spatial positions `\hat p_i`. For every edge
define the dimensioned embedding

\[
F_{ij}(\hat y,s)=\ell_0\bigl(\hat y,(1-s)\hat p_i+s\hat p_j\bigr),
\qquad 0\le s\le1.
\]

Writing `\Delta\hat p_{ij}=\hat p_j-\hat p_i`, its normalized differential and physical pullback
are

\[
\widehat J_{ij}=(e_0,\Delta\hat p_{ij}),
\qquad
h_{ij}=\ell_0^2\widehat J_{ij}^Tg\widehat J_{ij}
=\ell_0^2\begin{pmatrix}-1&0\\0&|\Delta\hat p_{ij}|^2\end{pmatrix}.
\]

Every nonzero edge is a regular timelike strip. Its pullback-derived terminal scalar is unoriented:

\[
\bar\phi_{\{ij\}}=\frac14\log\frac{-\det h_{ij}}{h_{ij,00}^2}
=\frac14\log|\Delta\hat p_{ij}|^2.
\]

The arbitrary `ell_0` cancels. Reversing the affine strip parameter leaves `h_ij` and
`\bar\phi_{\{ij\}}` unchanged. The cycle test therefore uses a separately supplied antisymmetric
ordered lift

\[
\delta_{ij}=\epsilon_{ij}\bar\phi_{\{ij\}},\qquad
\delta_{ji}=-\delta_{ij},
\]

with the increasing-label lift used for the displayed residuals. G140 does not derive the physical
inverse observer query or promote this lift into a realized G139 groupoid.

The strips are not unrelated planes. With static worldlines
`z_i(\hat y)=\ell_0(\hat y,\hat p_i)`,

\[
F_{ij}(\hat y,0)=z_i(\hat y),\qquad F_{ij}(\hat y,1)=z_j(\hat y),
\]

so `F_ij` and `F_jk` meet on the same middle worldline with the identical clock tangent and can be
concatenated as a piecewise regular route. Their transverse ruler directions need not agree; that
carry remains separately typed. The direct strip `F_ik` is another realization. The metric
supplies all of them but does not identify the direct and composite realizations.

## 3. Pooled rank-ten nonclosing network

Choose

\[
\hat p_A=(0,0,0),\quad \hat p_B=(1,0,0),\quad
\hat p_C=(0,1,0),\quad \hat p_D=(0,0,1).
\]

Then

\[
|AB|^2=|AC|^2=|AD|^2=1,
\qquad
|BC|^2=|BD|^2=|CD|^2=2.
\]

After the Minkowski affine identification of the separated tangent spaces, the pooled six-plane
restriction matrix has exact rank ten. Solving all eighteen pullback entries recovers uniquely the
constant coefficient matrix

\[
g=\operatorname{diag}(-1,1,1,1).
\]

This proves constant-metric coefficient faithfulness in the bounded affine control. It is not a
G129 pointwise rank-ten atlas for an arbitrary metric. The same six `J_e` may separately be treated
as co-located algebraic plane germs at one tangent space, where their rank-ten statement is
pointwise, but that algebraic germ control is not the four separated-observer network.

For the registered increasing-label lift every triangular residual is

\[
\omega_{ABC}=\omega_{ABD}=\omega_{ACD}=\omega_{BCD}
=\frac14\log2\ne0.
\]

Equivalently, the bounded return is

\[
\tanh\!\left(\frac14\log2\right)\ne0,
\]

and the reciprocal product on the displayed cycle is

\[
e^{-2\omega}=\frac1{\sqrt2}\ne1.
\]

This failure is not an artifact of that particular sign lift. The three A-incident scalars vanish,
whereas `BC`, `BD`, and `CD` each have magnitude `log(2)/4`. Exhausting their `2^3=8` possible
signs leaves at least one nonzero face residual in every case. No antisymmetric sign choice turns
these terminal scalars into an exact endpoint cochain.

## 4. Pooled rank-ten closing control in the same metric

Now place the same four static observer types at the vertices of a unit regular tetrahedron:

\[
\begin{aligned}
\hat p_A&=(0,0,0),\\
\hat p_B&=(1,0,0),\\
\hat p_C&=(1/2,\sqrt3/2,0),\\
\hat p_D&=(1/2,\sqrt3/6,\sqrt{2/3}).
\end{aligned}
\]

All six squared normalized edge lengths equal one, so all six pullbacks are regular and all
terminal scalars and cycle residuals vanish. The pooled restriction design again has exact rank ten
and reconstructs the same constant Minkowski coefficient matrix uniquely.

This control is not promoted to the physical UDT observer network. It proves only that the same
ambient metric permits both closure outcomes when different regular observer-query embeddings and
their edge lifts are supplied.

## 5. Consequence

Because `g` is identical in both controls, no predicate of the metric alone can distinguish their
positional closure. A pooled rank-ten set of constant-metric pullbacks answers “which constant
bilinear form represents these relation data?” It does not answer “which pair queries and supplied
orientation lift are members of one composable positional family?”

Under the provisional G139 clarification, zero cycle returns become a genuine nonidentity
admissibility condition on the typed relation family `(g,Q,F,~_pos)`. The nonclosing witness is not
one admitted endpoint-positional family; its edges must be separately branch/path-labelled or not
composed as that family. This condition restricts query/relation data, not `g` by itself.

Nothing here proves that congruence must remain an independent postulate. A later native
observer-relation construction could derive it. G140 proves only that one constant metric,
regularity, shared calibration, pooled rank completeness, and a supplied edge lift do not.

## 6. Scope ceiling

The witnesses are stationary, affine, regular, finite, source-free, and explicitly normalized by
the arbitrary shared unit `ell_0`; no physical length scale is selected. They do not classify
singular/null strata, time-live global histories, causal route selection, physical observer
populations, `X_max`, proper length, light/EM, observations, bootstrap, action, matter, or dynamics.
