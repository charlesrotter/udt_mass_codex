# G239 exact derivation — metric/reference-projected point-process operator

Date: 2026-08-23

## 1. Landing

```text
REFERENCE_PROJECTED_METRIC_INTENSITY_OPERATOR_DERIVED_CONDITIONALLY
__MATCHED_REFERENCE_AND_ANGULARLY_CONSTANT_RESPONSE_CANCEL_EXACTLY
__NONCONSTANT_METRIC_PUSHFORWARD_CAN_SURVIVE_FIXED_SURVEY_REFERENCE
__CONNECTED_PAIR_TERM_SEPARATES_EXACTLY
__PHYSICAL_HISTORY_SOURCE_AND_BRANCH_POPULATION_OPEN
```

No BOSS outcome, curve value, feature, covariance array, scale, P1 profile, `X_max`, or fitted
coefficient enters this result.

## 2. Typed metric observation relation

Let `S` be a supplied source-event domain and `O` one observer-coordinate shell. For each supplied
regular null branch `b`, let

\[
\Psi_b:S_b\longrightarrow O
\]

be the observation map generated conditionally by one supplied complete metric history and query.
Let `a_b(s)>=0` be supplied population/branch weights. If `mu_1` is the source one-point measure,
the observed one-point measure is

\[
\nu_1=\sum_b(\Psi_b)_*\bigl(a_b\,\mu_1\bigr).
\]

This is where the completed metric orchestra acts. Along each branch the primary coframe gives the
clock map, while its Levi--Civita curvature and quotient screen connection give the Jacobi map.
The operator is metric-derived **after** the history, incidence, and populated branches are
supplied; it does not select those inputs.

On a regular one-to-one branch with source coordinates `x` and observed coordinates `o`, the usual
pushforward density is

\[
\frac{d\nu_1}{do}(o)
=\frac{a(s)\,d\mu_1/dx}{|\det D\Psi(s)|},\qquad s=\Psi^{-1}(o).
\]

If instead the Jacobi map `D` is written in the observer-to-source direction, source screen area is
`dA_s=|det D|dOmega_o`; the same density factor is then written with `|det D|`. These are inverse
coordinate conventions, not competing physics. The invariant object used below is simply
`nu_1`.

## 3. Two-source pushforward and the Poisson control

Let `mu_2` be the source factorial pair measure and let `a_{bc}(s,t)` be the supplied joint branch
weight. The observed factorial pair measure is

\[
\nu_2=\sum_{b,c}(\Psi_b\times\Psi_c)_*
\bigl(a_{bc}\,\mu_2\bigr).
\]

For the explicitly chosen homogeneous-Poisson control,

\[
\mu_2=\mu_1\otimes\mu_1
\]

off the diagonal. If branch population also factorizes,

\[
a_{bc}(s,t)=a_b(s)a_c(t),
\]

then functoriality of product pushforward gives exactly

\[
\boxed{\nu_2=\nu_1\otimes\nu_1.}
\]

Thus an independently mapped Poisson source remains factorized. A metric map by itself does not
manufacture a connected factorial-pair measure. It can, however, alter the observed one-point
intensity relative to the separately constructed survey reference.

For a general populated relation define the connected remainder

\[
\Gamma=\bar\nu_2-P\otimes P,
\]

where `P=nu_1/nu_1(O)` and `bar nu_2` is the normalized observed factorial pair measure. Correlated
source structure, correlated branch choice, multiplicity, or a genuinely nonfactorizing physical
pair relation belongs in `Gamma`; none is silently inserted in G239.

## 4. Exact reference-projected identity

Let `Q` be the normalized random-reference measure, and let `K_theta(o_1,o_2)` be the symmetric
nonnegative kernel for one angular bin. In the population/conditioned-fixed-count limit, normalized
pair counts have expectations

\[
DD=\langle K,\bar\nu_2\rangle,\qquad
DR=\langle K,P\otimes Q\rangle,\qquad
RR=\langle K,Q\otimes Q\rangle.
\]

The borrowed Landy--Szalay readout is

\[
w_K=\frac{DD-2DR+RR}{RR}.
\]

Substituting `bar nu_2=P tensor P+Gamma` gives the exact decomposition

\[
\boxed{
w_K=
\frac{\langle K,(P-Q)\otimes(P-Q)\rangle}
     {\langle K,Q\otimes Q\rangle}
+
\frac{\langle K,\Gamma\rangle}
     {\langle K,Q\otimes Q\rangle}.}
\]

The first term is the **reference-mismatch intensity term**. The second is the **connected pair
term**. They are mathematically and physically distinct.

When `P` is absolutely continuous relative to `Q`, write `f=dP/dQ`. Since both are normalized,
`integral f dQ=1`, and the factorized term becomes

\[
\boxed{
w_K^{\rm intensity}=
\frac{\int K(o_1,o_2)[f(o_1)-1][f(o_2)-1],dQ_1dQ_2}
     {\int K(o_1,o_2),dQ_1dQ_2}.}
\]

An angular-bin kernel need not be positive semidefinite, so this term can be positive or negative.

## 5. Exact cancellations

### Matched reference

If the random reference is constructed from the complete metric-pushed intensity itself, then
`Q=P`, so the intensity term vanishes identically in every bin. A factorized Poisson control then
has `w_K=0`.

### Pure radial/common multiplier

On one angular shell, if the complete response multiplies the reference intensity by one positive
angularly constant number `c`, normalization removes it:

\[
P=\frac{cQ}{\int c,dQ}=Q.
\]

Therefore pure radial dilation, by itself, cannot create the nontrivial angular curve. This exactly
recovers the G126 boundary.

## 6. Conditional survival of metric angular response

The released random catalogue owns footprint/completeness semantics; it is not a sample from a
UDT-transformed physical source measure. Therefore the method contract does not force `Q=P`.
If a supplied complete history gives a nonconstant angular clock/screen Jacobian not absorbed into
that fixed reference, then `f` is nonconstant and the first term can survive.

The production witness uses exact rational distributions on four sky cells:

\[
Q=(1/10,1/5,3/10,2/5),
\]

with positive response `(1,2,1,3)`, giving

\[
P=(1/20,1/5,3/20,3/5).
\]

For the preregistered symmetric control-bin kernel, exact arithmetic gives

\[
DD=8/25,\qquad DR=11/25,\qquad RR=12/25,
\]

and hence

\[
\boxed{w_K=-1/6\ne0.}
\]

This finite witness certifies the operator algebra. Its four response values are not a proposed
metric history or a fit.

Metric liveness is separately supplied by the exact G127 local history witness. At `q=r=1` and
`sin(alpha)=4/5`, its radial optical-tidal eigenvalues are `(0,0)` while the tilted values are

\[
(8/25,4/25).
\]

For point-vertex Jacobi data,

\[
\mathcal D(\lambda)=\lambda I-rac{\lambda^3}{6}\mathcal T+O(\lambda^4),
\]

so

\[
\det\mathcal D_{\rm tilted}
=\lambda^2-\frac{2}{25}\lambda^4+O(\lambda^5),
\]

while the radial control is `lambda^2+O(lambda^5)`. Thus one supplied metric can genuinely generate
direction-dependent local screen area. This proves liveness, not the global BOSS response.

## 7. Connected-term control

The exact finite witness adds

\[
\Gamma=\frac1{1000}v\otimes v,\qquad v=(1,-1,0,0),
\]

to `P tensor P`. The full pair measure remains nonnegative and normalized. Exact arithmetic gives

\[
\frac{\langle K,\Gamma\rangle}{RR}=-\frac1{240},
\]

and

\[
w_K=-\frac16-\frac1{240}=-\frac{41}{240}.
\]

This demonstrates the decomposition without assigning a physical connected source or branch law.

## 8. What changed relative to G238

G238 left the reference-projected forward map open. G239 now owns its exact conditional measure
form and proves the cancellation/survival criteria. The gap is narrower:

- a complete supplied history and branch population determine `P` through the metric evaluator;
- an explicit source-pair/branch law determines `Gamma`;
- the frozen survey reference and bin kernels then determine `w_K` with no further response
  coefficient.

Still open are the values of `P` and `Gamma` for the physical observer sky. G239 does not turn the
finite G237 SNe state into that complete history.

## 9. Maximum conclusion

The complete metric can conditionally create a reference-surviving angular intensity pattern from
a featureless Poisson control when its angle-dependent pushforward differs from the fixed survey
reference. It cannot do so through a purely angularly constant radial multiplier, and an exactly
matched reference cancels the factorized response. Connected source/pair/branch physics enters as
a separately typed term.

No BOSS prediction, UDT validation, BAO origin, feature scale, `X_max`, physical history, source
law, or branch population follows.

