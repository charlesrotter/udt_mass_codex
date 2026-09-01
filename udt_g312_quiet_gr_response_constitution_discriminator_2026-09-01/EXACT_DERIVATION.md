# G312 exact derivation — quiet-GR response-constitution discriminator

Date: 2026-09-01
Status: `EXTERNALLY_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY`

## 1. Landing

```text
TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED
```

This is not a return to an unrestricted formula search. Existing UDT structure leaves exactly two
independent architecture choices load-bearing in this bounded lane:

1. `FULL_QUIET_GR_PRINCIPAL_RESPONSE_OVERLAP`;
2. `LOCAL_FINITE_JET_RESPONSE_CONSTITUTION`.

If both are provisionally supplied, the active no-new-operator-scale, quiet-regular, metric-only
gates close the response to G301, and G311 then gives trace-free Ricci. Neither clause is currently
derived or owner-adopted in that strengthened form.

## 2. What G311 already fixes

Inside G301, a natural response has

\[
E_{ab}=aR_{ab}+bR g_{ab}.
\]

Its trace-free part is exactly

\[
\operatorname{TF}_g(E)_{ab}
=a\left(R_{ab}-\frac14R g_{ab}\right)=aS_{ab}.
\]

For the nondegenerate quiet-GR branch, \(a\ne0\). Universal Reciprocity therefore yields

\[
S_{ab}=0.
\]

The coefficient \(b\) is irrelevant to this response-shape equation. The unresolved issue is not
which coefficient in G301 to fit; it is whether the physical response belongs to G301 at all.

The production census verifies this identity on 128 exact rational symmetric tensors and arbitrary
rational \((a,b)\), totaling 2,048 component identities. The independent flattened-tensor census
checks 1,920 more identities with a different representation.

## 3. Why the G301 ray theorem is exact

Let \(K\) be algebraic curvature and \(F(K)\) the response. If

\[
F(tK)=tF(K),\qquad t>0,
\]

and \(F\) is differentiable at the quiet origin with \(F(0)=0\), then

\[
DF_0(K)=\lim_{t\to0^+}\frac{F(tK)-F(0)}t=F(K).
\]

Thus \(F=DF_0\) and is exactly linear in curvature. G301's externally certified Lorentz-natural
basis census then leaves only \(R_{ab}\) and \(Rg_{ab}\).

The quiet differentiability assumption matters. A nonlinear degree-one direction map such as

\[
H(x,y)=\frac{(x^3,y^3)}{x^2+y^2}
\]

is scale-free away from zero, but its directional derivatives are not additive and it is undefined
at the quiet origin.

## 4. Solution overlap is weaker than GR response overlap

Consider the regular local curvature-quadratic response

\[
Q_{ab}=\operatorname{TF}_g\!\left(R_{ac}R_b{}^c\right).
\]

Every Ricci-flat GR metric satisfies \(Q_{ab}=0\). Hence it passes **solution overlap**. But

\[
Q[tR]=t^2Q[R],
\]

so its first variation at flat curvature vanishes. It has no GR quiet principal operator. Exact
rational production and independent witnesses verify both facts.

Therefore the current bounded W3 result—exact embedding of a GR vacuum branch—does not by itself
own the complete GR quiet response germ. Charles's intended phrase “indistinguishable from GR at
lab and solar scales” may motivate that strengthening, but it has not yet been formally adopted in
this exact dynamical sense.

## 5. Why no operator scale removes regular local corrections

The GR-leading response has dimension \(L^{-2}\). A curvature polynomial of degree \(n>1\) has
dimension \(L^{-2n}\), so adding it to the GR-leading term requires a coefficient with dimension

\[
L^{2(n-1)}.
\]

Neither \(c_E\) alone nor \(G_{\rm obs}\) without a source/mass attachment supplies that vacuum
length. Physical \(X_{\max}\) remains open and is forbidden as an operator input. Curvature ratios
can restore weight one without a new scale, but they are singular or nondifferentiable at the
quiet origin. Consequently, **within a local finite-jet regular response**, full GR quiet-principal
overlap plus the active no-scale gate closes the response to G301.

## 6. Why locality is independent

There are metric-only, scale-free, quiet-regular nonlocal competitors. A representative type is

\[
u=\Box^{-2}(R_{ab}R^{ab}),
\qquad
E_{ab}=S_{ab}+\alpha\,\operatorname{TF}_g(\nabla_a u\nabla_b u).
\]

Here \(u\) is dimensionless and the correction again has dimension \(L^{-2}\). With a retarded
zero-source prescription it vanishes on Ricci-flat metrics and begins beyond first quiet order, so
the GR quiet principal response survives. But \(\Box^{-2}\) requires a Green function plus
boundary/history data. Two exact discrete histories with identical final local source data give
different terminal integrated carry in both implementations.

This is a counterarchitecture, not a proposed UDT law. It proves that GR principal overlap does not
imply locality. Metric causality also does not settle the issue: a retarded nonlocal response can be
causal while retaining history dependence. The non-signalling co-presence frame makes it especially
important not to assume locality by habit.

## 7. Independence and smallest honest closure

The two witnesses separate the choices:

| Witness | Local | GR solution overlap | GR principal overlap |
|---|---:|---:|---:|
| Pure curvature quadratic | yes | yes | no |
| Scale-free nonlocal metric history | no | yes | yes |

Thus neither missing clause entails the other. A sentence that simply conjoins them is one written
sentence but two logically independent premises.

The exact conditional theorem is:

> If the vacuum UDT response is a regular local finite-jet natural response of the complete metric,
> has the full GR quiet principal germ, and carries no independent operator scale, then it lies in
> G301; owner-adopted Universal Reciprocity then gives \(R_{ab}-\tfrac14Rg_{ab}=0\).

## 8. What remains open

- whether Charles intends W3 to include full quiet dynamical/principal equivalence;
- whether UDT response locality is a postulate, derivable from causal reciprocity, or intentionally
  relaxed by co-presence;
- the connected scalar's magnitude/sign, lawful data, global history, population, source/mass,
  observations, completion, and physical \(X_{\max}\).

No metric, reciprocal kernel, angular cancellation, or observational interface changed.

Fresh external review independently retained the mathematics and premise ownership. After the
single preregistered sealed-layout repair, the repair-only reviewer reproduced the aggregate replay
and returned `G312_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY`.
