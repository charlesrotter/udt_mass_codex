# G138 exact derivation — relational position network descent

## 1. Finite calibrated observer graph

Let `G=(V,E)` be a finite connected graph. Every oriented edge carries a supplied regular
calibrated complete-pair depth and its G137 position coordinate,

\[
\phi_{BA}=-\phi_{AB},
\qquad
\xi_{AB}=\tanh\phi_{AB}\in(-1,1),
\qquad
q_{AB}=e^{-2\phi_{AB}}>0.
\]

Define the native operation

\[
u\oplus v=\frac{u+v}{1+uv}.
\]

The map `tanh:(R,+)->((-1,1),oplus)` is a group isomorphism with inverse `atanh`.

## 2. Endpoint-descent theorem

The following statements are equivalent.

1. There is a function `Phi:V->R` such that
   \[
   \phi_{AB}=\Phi_B-\Phi_A.
   \]
2. Every oriented cycle `C` has
   \[
   \sum_{e\in C}\phi_e=0.
   \]
3. Every cycle has
   \[
   \prod_{e\in C}q_e=1.
   \]
4. Every cycle has
   \[
   \bigoplus_{e\in C}\xi_e=0.
   \]
5. Summing depths, or Mobius-adding bounded positions, from a chosen root to a vertex is independent
   of the chosen path.

Proof: endpoint differences telescope, proving `1=>2`. Conversely, choose a root `O` and set
`Phi_A` equal to the edge-depth sum along any root-to-`A` path. Two such paths form a cycle, so `2`
makes the definition path-independent and proves `2=>1`. The endpoint potential is unique up to one
common additive constant. Since the real exponential is injective,

\[
\prod_Cq_e=e^{-2\sum_C\phi_e}=1
\quad\Longleftrightarrow\quad
\sum_C\phi_e=0.
\]

The `tanh/atanh` group isomorphism proves equivalence with `4` and `5`.

For `n` vertices and `m` unoriented edges, any spanning tree leaves `m-n+1` chords. Their
fundamental cycles form a cycle-space basis, so exactly `m-n+1` independent residuals suffice.
The production witness has five vertices, seven edges, cycle rank three, and three exact zero
fundamental residuals.

## 3. Bounded observer charts and reference-gauge torsor

More generally, for any reference depth `lambda in R`, define

\[
u_A^{(\lambda)}=\tanh(\Phi_A-\lambda).
\]

Changing from `lambda` to `mu` acts by one Mobius translation with parameter
`tanh(lambda-mu)`. The family of all reference-depth gauges is therefore a torsor for
`((-1,1),oplus)`.

Choosing an observer `O` sets `lambda=Phi_O` and gives the observer-rooted chart

\[
u_A^{(O)}=\tanh(\Phi_A-\Phi_O).
\]

Then every pair relation is

\[
\boxed{
\xi_{AB}
=\frac{u_B^{(O)}-u_A^{(O)}}
       {1-u_A^{(O)}u_B^{(O)}}
}.
\]

Choose a different reference observer `R`. The chart transition is

\[
\boxed{
u_A^{(R)}
=\frac{u_A^{(O)}-u_R^{(O)}}
       {1-u_A^{(O)}u_R^{(O)}}
}.
\]

Substitution leaves every `xi_AB` unchanged. Observer-rooted charts are a subset of the full gauge
torsor and are related by these Mobius translations. The relational equations select no coordinate
root. This does not prove that a supplied physical graph or a later law cannot distinguish an
observer or geometric feature for another reason.

With the working common scale,

\[
X_A^{(O)}=X_{\max}u_A^{(O)},
\]

and the dimensionful pair formula is G137's law. Replacing `X_max` by any positive multiple rescales
all displayed dimensional coordinates while leaving every normalized closure and chart-transition
identity unchanged. Network descent therefore does not determine the value of `X_max`.

## 4. Nonzero cycles: path-labelled holonomy

If one cycle has

\[
h_C=\sum_{e\in C}\phi_e\ne0,
\]

no endpoint potential exists on the base graph. Two routes between the same endpoints differ by
`h_C`; their bounded discrepancy is `tanh(h_C)`. The production witness perturbs one chord by
exactly `1/11` and recovers exact holonomy `1/11`.

This is not automatically an inconsistency. Only if the two routes remain distinct physical arrows
does depth remain additive on paths while the cycle value is real holonomy. An endpoint potential exists on a
tree or universal-cover lift and descends to the base graph exactly when every holonomy vanishes.
Only when direct and composite routes are declared to represent the same physical relation does
nonzero cycle depth violate composition.

## 5. Scope ceiling

G138 classifies the scalar positional network. It does not select whether the physical global
relation family is endpoint-descended or path-labelled. It also does not select edge values, pair
realizations, a rank-complete full-pullback network, the complete metric history, or the dimensional
value of `X_max`. The scalar torsor is not by itself the full four-dimensional metric, proper length,
areal radius, signal distance, universe size, or global topology.
