# G154 exact derivation — shared scale versus asymptotic response

Date: 2026-08-18

## 1. Types and exact starting law

On one supplied smooth regular calibrated pair family, write

\[
\rho=X\tanh\phi,
\]

where `phi` abbreviates the terminal `phi_pair` and `X` is the supplied realization of the
positional-dilation scale. For either normalized pair-frame vector \(V=u,n\), G153 gives

\[
\boxed{
V(\rho)=\tanh\phi\,V(X)+X\operatorname{sech}^2\phi\,V(\phi).
}
\]

This identity does not say that `rho` is proper length or that `V(rho)` is a unit-ruler response.

Three meanings of scale must remain separate:

1. one fixed scale \(X_*\) supplied to a connected dimensionful Mobius compositional leaf;
2. different constants \(X_*(\alpha)\) on different leaves or branches;
3. a live scalar \(X\) on a more general supplied pair family before such leaf descent is proved.

## 2. Conditional consistency theorem for a supplied fixed-scale leaf

First add a premise not owned by the normalized G136/G137 law: let a connected leaf carry a
dimensionful Mobius position law with one already fixed parameter \(X_*>0\). Put
\(F(\phi)=x(\phi)/X_*\). Its exact composition law is

\[
F(\phi_1+\phi_2)
=\frac{F(\phi_1)+F(\phi_2)}{1+F(\phi_1)F(\phi_2)}.
\]

Because \(|F|<1\), define \(Y=\operatorname{artanh}F\). Then

\[
Y(\phi_1+\phi_2)=Y(\phi_1)+Y(\phi_2).
\]

Continuity gives \(Y=k\phi\). The adopted normalized unit slope gives \(k=1\), hence

\[
F(\phi)=\tanh\phi,
\qquad
x(\phi)=X_*\tanh\phi.
\]

If the same leaf is presented as \(x=X(\phi)\tanh\phi\), then for every \(\phi\ne0\)

\[
X(\phi)=X_*.
\]

Continuity extends this through the identity. Therefore, **conditional on that supplied one-scale
law type**,

\[
\boxed{d_{\rm leaf}X=0}
\]

on that strict one-scale compositional leaf.

This is a consistency theorem, not a scale-selection theorem. The actually adopted normalized law

\[
\chi(\phi_1+\phi_2)
=\frac{\chi(\phi_1)+\chi(\phi_2)}{1+\chi(\phi_1)\chi(\phi_2)},
\qquad \chi=\tanh\phi,
\]

contains no dimensionful scale. It remains exact alongside, for example, a nonconstant supplied
field \(X(q)=X_*+q\). Consequently normalized composition does **not** derive \(dX=0\), and the
G137/G139 ownership results do not supply the missing premise.

The current premises also do not prove that a physical family belongs to the fixed-scale class,
that distinct leaves share the same \(X_*\), or that every direction of a supplied pair history is
a within-leaf compositional direction. G153's live `dX` term therefore remains generally
intrinsic; it becomes excluded only after a fixed-scale leaf premise is independently supplied or
derived.

## 3. Zero-order endpoint law does not own first response

For \(\epsilon=\pm1\), if

\[
\phi\to\epsilon\infty,
\qquad
X\to X_*\in(0,\infty),
\]

then

\[
\rho=X\tanh\phi\to\epsilon X_*.
\]

Conversely, with either one of the two limiting inputs fixed, the corresponding signed limit of
`rho` supplies the other. This is a zero-order equivalence only. It gives no limit for a normalized
derivative of `rho`.

Keep the exact contributions

\[
A_V=\tanh\phi\,V(X),
\qquad
B_V=X\operatorname{sech}^2\phi\,V(\phi),
\qquad
R_V=A_V+B_V.
\]

One may not replace \(A_V\) by \(\epsilon V(X)\) when `V(X)` is unbounded: the discarded product
\((\tanh\phi-\epsilon)V(X)\) need not vanish. Likewise,
\(\operatorname{sech}^2\phi\to0\) does not force \(B_V\to0\) unless the growth of `V(phi)` is
controlled.

On a conditionally supplied fixed-scale leaf,

\[
R_V=X_*\operatorname{sech}^2\phi\,V(\phi).
\]

It is quiet, finite-live, divergent, or nonconvergent according to that complete product—not the
hyperbolic coefficient alone.

## 4. Same position profile, four conditionally fixed-scale response classes

The nonselection can be shown without changing `phi`, `rho`, or `X_*` between classes. Let

\[
q=1-\sigma\in(0,1),
\qquad
p=\frac13,
\qquad
\phi_\epsilon(q)=\epsilon[-p\log q],
\qquad
X=X_*.
\]

For each positive \(\ell\), use the regular interior pair metric

\[
h_{\epsilon,\ell}
=-T_{\epsilon,\ell}^2d\tau^2+L_\ell^2d\sigma^2,
\qquad
L_\ell=q^{-\ell},
\qquad
T_{\epsilon,\ell}=L_\ell e^{-2\phi_\epsilon}.
\]

Then

\[
\phi_{\rm pair}=\frac12\log\frac{L}{T}=\phi_\epsilon
\]

for every \(\ell\), so all witnesses have the identical terminal position

\[
\rho_\epsilon(q)
=\epsilon X_*\frac{1-q^{2/3}}{1+q^{2/3}}.
\]

Only the retained metric common scale/ruler normalization changes. Since

\[
n=q^\ell(-\partial_q),
\]

the exact response is

\[
\boxed{
n(\rho)=
\epsilon\frac{4X_*p\,q^{2p+\ell-1}}{(1+q^{2p})^2}.
}
\]

Therefore:

| common-scale exponent | exact response class |
|---|---|
| \(\ell=1/2\) | \(n(\rho)\to0\) (`QUIET`) |
| \(\ell=1/3\) | \(n(\rho)\to\epsilon 4X_*/3\) (`FINITE_LIVE`) |
| \(\ell=1/4\) | \(n(\rho)\to\epsilon\infty\) (`DIVERGENT`) |

At the critical exponent, replace

\[
L=q^{-1/3}[1+\tfrac12\sin(1/q)]^{-1}.
\]

It remains positive and smooth at every interior point, but the response has subsequential limits
\(2X_*\) and \(2X_*/3\), so it is `NONCONVERGENT`.

The temporal dual is exact: take \(q=1-\tau\), \(T=q^{-\ell}\), and
\(L=Te^{2\phi}\). Then \(u=q^\ell(-\partial_q)\) and the same four classes follow for `u(rho)`.

Each two-metric can be embedded in a regular interior four-dimensional Lorentz metric by adjoining
a positive screen. These witnesses do not claim to be the physical history. Their role is narrower:
an alleged universal consequence of the active local premises must hold on this admitted
counterfamily unless another physical restriction is derived.

## 5. A finite shared endpoint also does not quiet a live scale

Before strict leaf descent, use the quiet profile

\[
\phi=-\frac12\log q,
\qquad
L=q^{-1/2},
\qquad
X_a(q)=X_*+q^a.
\]

Every \(a>0\) gives \(X_a\to X_*\), but

\[
n(X_a)=-a q^{a-1/2}.
\]

Thus `V(rho)` can be quiet for \(a>1/2\), finite nonzero for \(a=1/2\), or divergent for
\(a<1/2\), even though the endpoint value is the same. The smooth interior field

\[
X=X_*+q\sin(q^{-1/2})
\]

has the same endpoint and two response subsequences tending to \(+1/2\) and \(-1/2\).

Cancellation is also exact. For positive `phi`, let

\[
X=\frac{C}{\tanh\phi}.
\]

Then \(X\to C\), the two G153 terms are individually live, but

\[
\rho=C,
\qquad
V(\rho)=0.
\]

Therefore a quiet total response does not imply that both underlying terms quiet separately.
These live-`X` constructions are not members of a **supplied** strict single-scale dimensionful
compositional leaf. Because that leaf type has not been derived, they remain within the general
intrinsic/stateful branch retained by G153.

## 6. What Reciprocity and composition do—and do not—select

- The sign-paired witnesses pair the \(+\infty\) and \(-\infty\) classes under the same chosen
  normalized frame direction. Universal reversal of the oriented response additionally requires
  a carried-frame convention, which remains open.
- A **supplied** dimensionful one-scale Mobius law keeps `X_*` fixed within its leaf. The adopted
  normalized law does not select that law type or its scale.
- Additive depth composition constrains values of `phi`; it does not constrain the rate of `phi`
  against the normalized metric clock or ruler.
- That rate depends on retained metric common scale. Terminal reciprocal position is blind to the
  very common-scale freedom that controls the normalized asymptotic response in the witnesses.
- Cross-leaf equality of `X_*`, physical leaf population, and global completion remain open.

## 7. Landing

The preregistered primary landing is

```text
EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED
```

More precisely: a supplied strict one-scale dimensionful Mobius law is internally consistent and
forces \(X=X_*\) inside its own leaf. The active normalized composition law does not derive that
extra type. Even after it is supplied, quiet, finite-live, divergent, and nonconvergent asymptotic
responses all remain compatible with the current local metric premises because the metric
common-scale/history rate remains unselected.

No proper length, dynamics, physical history, numerical `X_max`, bootstrap law, or global
completion follows.
