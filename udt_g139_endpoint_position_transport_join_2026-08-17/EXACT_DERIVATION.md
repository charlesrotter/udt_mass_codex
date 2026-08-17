# G139 exact derivation — endpoint position beneath path transport

## 1. Typed arena

Let `P` be the groupoid of supplied compatible routes between calibrated observer endpoints. A
declared physical pair-relation family must additionally supply a route equivalence
`~_pos` that is compatible with composition and inversion. Let

\[
\mathcal E=\mathcal P/{\sim_{\rm pos}},
\qquad
\pi:\mathcal P\longrightarrow\mathcal E
\]

be the resulting positional quotient groupoid and quotient functor. This congruence is a
**conditional input** of the declared family; endpoint constancy by itself does not construct it or
prove closure. The approved clarification requires physical positional families to have this type,
but it does not select or generate one. The quotient forgets route information only in the
positional channel. It does not identify the complete route arrows.

Let

\[
\phi:\mathcal E\longrightarrow(\mathbb R,+)
\]

be the matched-calibration endpoint cocycle and let

\[
U:\mathcal P\longrightarrow\operatorname{Iso}(\mathscr S)
\]

be a supplied metric-derived screen/normal transport functor on compatible endpoint fibers. Define

\[
\xi(\gamma)=\tanh\!\bigl(\phi(\pi\gamma)\bigr).
\]

Let `B_M` be the one-object group whose arrows are `(-1,1)` with Mobius composition `oplus`.
Together with the endpoint-screen isometry groupoid `Iso(S)`, the categorical product
`B_M x Iso(S)` is well-defined. The joint output is the product functor

\[
J:\mathcal P\longrightarrow\mathbb B_M\times\operatorname{Iso}(\mathscr S),
\qquad
J(\gamma)=\bigl(\xi(\gamma),U_\gamma\bigr).
\]

This categorical product is bookkeeping for two compatible functors. It is not a physical product
decomposition of the metric and not automatically a global Cartesian product or literal fiber
bundle; those stronger descriptions require additional structure.

## 2. Composition

For `gamma_1:A->B` and `gamma_2:B->C`, with the same carried `B` calibration and screen fiber,

\[
\phi_{AC}=\phi_{AB}+\phi_{BC},
\]

\[
\xi_{AC}
=\xi_{AB}\oplus\xi_{BC}
=\frac{\xi_{AB}+\xi_{BC}}{1+\xi_{AB}\xi_{BC}},
\]

and

\[
U_{\gamma_2\circ\gamma_1}=U_{\gamma_2}U_{\gamma_1}.
\]

Thus the positional and transport components compose together without being forced into one
scalar. Reversal gives

\[
\phi(\gamma^{-1})=-\phi(\gamma),\qquad
\xi(\gamma^{-1})=-\xi(\gamma),\qquad
U_{\gamma^{-1}}=U_\gamma^{-1}.
\]

For the conditional conformal-screen representation already classified in G51,

\[
C_w(\gamma)=e^{w\phi(\pi\gamma)}U_\gamma,
\]

central scalar scaling gives

\[
C_w(\gamma_2\circ\gamma_1)=C_w(\gamma_2)C_w(\gamma_1).
\]

No new value of `w` or universal screen representation is selected here.

## 3. Same endpoints and loops

If two routes `gamma` and `gamma'` represent the same endpoint arrow in `E`, then

\[
\phi(\pi\gamma)=\phi(\pi\gamma'),\qquad
\xi(\gamma)=\xi(\gamma'),
\]

while

\[
U_\gamma\ne U_{\gamma'}
\]

is allowed. Their relative transport `U_gamma'^{-1} U_gamma` retains route information.

For a closed route whose endpoint relation is the identity,

\[
\phi=0,\qquad\xi=0,
\]

but `U_loop` need not be the identity. Therefore endpoint position descending globally does not
flatten the angular connection or erase holonomy.

## 4. The terminal-branch guard

Suppose direct and composite routes have the same named endpoints but produce

\[
r=\phi_{AC}^{\rm direct}-(\phi_{AB}+\phi_{BC})\ne0.
\]

Then one cannot simultaneously claim that both routes are the same arrow of an endpoint-descended
family and hide `r` inside angular transport. Inside the declared regular, matched-calibration,
composable exact arena, exactly two honest classifications remain:

1. endpoint identification fails; or
2. the outputs are separately labelled terminal pair realizations/branches, so the positional
   scalar itself remains path/branch-labelled across those arrows.

The approved clarification chooses endpoint descent **within each physical relation family** and
therefore requires the second classification whenever distinct terminal branches are retained.
It does not select which branch or family is realized.

This dichotomy does not classify singular, null, calibration-mismatched, undefined, or
noncomposable cases. They remain outside G139 rather than being forced into either outcome.

## 5. Where the orchestra enters

This separation does not bolt angular physics onto a radial scalar after the fact. There are two
different stages:

1. The complete metric, including angular, screen, shift, and mixing data, forms the supplied pair
   pullback. Its terminal decomposition owns `phi_pair`; G137 position is downstream of that full
   pullback. These contributions are inside the positional relation.
2. The same complete geometry may retain route-dependent screen or normal transport not reducible
   to terminal `phi_pair`. That information belongs to `U_gamma` or another correctly typed path
   channel.

The two stages are projections of one complete geometric comparison, not competing definitions of
distance and not an external correction layer.

## 6. Exact witnesses

With

\[
\xi_1=\frac14,\qquad\xi_2=\frac27,
\]

the position composite is exactly

\[
\xi_2\oplus\xi_1=\frac12.
\]

Two rational rotations compose to

\[
U_2U_1=
\begin{pmatrix}
-33/65&-56/65\\
56/65&-33/65
\end{pmatrix},
\]

which remains in `SO(2)` and is nonidentity. The same-endpoint witness fixes
`phi=2/5` on two routes while assigning distinct transports. The terminal-disagreement witness has
exact residual `-7/60` and therefore cannot be silently absorbed into transport.

## 7. Conclusion ceiling

The adopted clarification closes G138's positional relation-type fork only within each declared
physical pair-relation family after its compatible positional route congruence is supplied. It does
not derive that congruence, the family, pair realization, route, metric history, `X_max` value,
local signal law, EM carrier, or global completion.
