# G268 exact derivation — relation equivalence versus operational content

Date: 2026-08-26

## Primary landing

```text
FINITE_REGULAR_SECH_STATE_IS_EXACTLY_EQUIVALENT_TO_THE_RECIPROCAL_RELATION_SPACE
__COMPACT_ENDPOINTS_FORM_ONLY_A_PARTIAL_NONGROUP_CLOSURE
__INDEPENDENT_M_WOULD_GIVE_A_CONDITIONAL_CROSS_READOUT_LAW
__NO_RELATION_NETWORK_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

This selects preregistered `R0+R2+O1`. `O2` is not established: no current premise independently
owns a mutual-clock measurement protocol for `M`.

## 1. Three exact presentations of one finite relation

On one supplied finite regular relation,

\[
r=e^{-\delta}>0,
\qquad
M=\operatorname{sech}\delta,
\qquad
\chi=\tanh\delta.
\]

The bounded state can be written rationally in the positive clock ratio:

\[
\boxed{M=\frac{2r}{1+r^2}},
\qquad
\boxed{\chi=\frac{1-r^2}{1+r^2}}.
\]

It obeys

\[
M>0,
\qquad
-1<\chi<1,
\qquad
M^2+\chi^2=1.
\]

Conversely, every point on that open right semicircle has

\[
\boxed{r=\frac{1-\chi}{M}>0},
\qquad
\boxed{r^{-1}=\frac{1+\chi}{M}},
\qquad
\boxed{\delta=\operatorname{artanh}\chi}.
\]

The derivative

\[
\frac{d\chi}{d\delta}=M^2>0
\]

never vanishes at finite real depth. Therefore the map is a global smooth bijection with smooth
inverse: the finite additive depth line, the positive multiplicative ratio line, and the open right
semicircle are three exact presentations of the same one-dimensional relation space.

## 2. Composition is transported, not newly restricted

Multiplication of clock ratios and addition of depths induce

\[
\chi_{12}=\frac{\chi_1+\chi_2}{1+\chi_1\chi_2},
\qquad
M_{12}=\frac{M_1M_2}{1+\chi_1\chi_2}.
\]

The denominator is positive throughout the finite interior. Identity, reversal, and associativity
are carried exactly:

\[
e=(1,0),
\qquad
(M,\chi)^{-1}=(M,-\chi).
\]

Thus the signed bounded state is a Lie-group presentation isomorphic to the original reciprocal
relation. Its circle equation is the equation defining the new coordinate image; it is not a
residual that rejects an old relation.

The qualifier “signed” is load-bearing. `M` alone is a two-to-one quotient away from the quiet
point and cannot compose. G267's full pair, not its even component by itself, is what is equivalent.

## 3. Every finite endpoint-potential network descends identically

Let supplied endpoint depths be `V_i`, and write `q_i=exp(-V_i)>0`. For an actual composite edge,

\[
r_{ij}=\frac{q_j}{q_i}.
\]

Then

\[
r_{ij}r_{jk}=r_{ik},
\qquad
r_{ij}r_{ji}=1,
\qquad
\prod_{(ij)\in C}r_{ij}=1
\]

on every finite cycle. Applying the bounded bijection edge by edge makes these precisely the G267
two-channel composition and cycle identities. Applying the inverse reconstructs every ratio and
all `q_i` up to one common positive reference factor.

Therefore arbitrary finite matched endpoint-potential networks are equivalent in the two
presentations. G268 rejects zero regular relations and zero finite networks. This agrees with G235:
faithful reconstruction is not value or history selection.

## 4. What the compact endpoints do—and do not do

The two limits are

\[
\delta\to+\infty\mapsto(0,+1),
\qquad
\delta\to-\infty\mapsto(0,-1).
\]

Same-sign endpoint composition has denominator `2`, but opposite endpoints have

\[
1+(+1)(-1)=0,
\]

so both displayed composition coordinates become indeterminate. This is the familiar
`(+infinity)+(-infinity)` ambiguity in bounded dress. The closed semicircle is therefore only a
partial ideal closure, not a total group completion.

The endpoints are not finite regular relations. Nothing here identifies them with an observer
population, a physical boundary, or `X_max`.

## 5. The conditional nonidentity content lives in an enlarged data type

Suppose a future operational protocol measures a mutual-clock magnitude `M_obs` independently of
the signed same-correspondence clock ratio `r`. The provisional candidate then predicts

\[
\boxed{M_{\rm obs}=\frac{2r}{1+r^2}}.
\]

This is coefficient-free and falsifiable. For example,

\[
r=2,
\qquad
M_{\rm obs}=\frac12
\]

has candidate value `4/5` and residual `-3/10`. It is rejected as an enlarged `(r,M_obs)` datum
even though `r=2` remains a perfectly valid reciprocal relation.

This separates the epistemic types:

- on the existing relation space, the circle is an exact bounded reparameterization;
- on an enlarged space with an independently supplied `M_obs`, it is a conditional cross-readout
  law;
- current premises do not derive the independent operational protocol, so the law is not yet an
  active observational prediction.

## 6. No history or distance law appears

For every admitted finite depth function `delta(q)`, pointwise mapping and inversion remain valid.
No differential residual relates distinct points of `q`, no distance unit or attachment enters,
and no valued history is rejected. The algebra clarifies a possible observable relation; it does
not provide the missing propagation law.

## Evidence

- 41 mechanically evaluated exact symbolic checks;
- 1,100 exact-rational ratio cases;
- 6,000 exact compositions and 2,000 associativity cases;
- 1,200 varied finite endpoint-potential networks with 34,742 checked edges;
- 95,617 implementation-distinct exact-rational assertions;
- 8/8 hostile mutations injected through one shared exact-rational validator and caught by their
  targeted failure class;
- zero regular-relation, finite-network, or history rejections.

The final zero-rejection counts and the absence of an owned operational protocol are analytic and
premise-scope conclusions. They are recorded in the result ledger but deliberately excluded from
the symbolic-check count.
