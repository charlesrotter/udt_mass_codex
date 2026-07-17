# UDT reciprocal-axis loop closure and area-form matter — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | grok at 64af120; pre-existing dirty work preserved |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| MAP frozen first | UDT_RECIPROCAL_LOOP_CLOSURE_MATTER_MAP.md, SHA-256 bf1a57da51d4be00f8229a594d5e4d25c5baa0bb5eb81a2dc032f271e203a469 |
| Exact verifier | verify_udt_reciprocal_loop_closure_matter.py — 27/27 checks pass |
| Carrier status | \(S^2\) remains reopened |
| GPU | Not used; next test is metric curvature algebra |
| Independent verification | OPEN |
| Build-on grade | PROVISIONAL CONDITIONAL DERIVATION; not banked and not canon |

## 0. Result

The existing UDT foundation does **not** derive rank-one-zero or the historical \(F^2\) matter
action. The positive quartic countermodel

\[
\int\sqrt{-g}\,\operatorname{tr}(M^2)
\]

respects the currently stated covariance, CSN, parity, and target-rotation symmetries while assigning
positive cost to rank-one derivatives.

\[
\boxed{
\text{Reciprocal-c + Reciprocity + CSN}
\not\Longrightarrow
\text{rank-one-zero or }F^2.
}
\]

However, the metric admits a concrete conditional extension that may explain why the historical
carrier looked like \(S^2\):

\[
\boxed{
g_{00}=-e^{-2\phi},
\qquad
h_{ij}=\delta_{ij}+(e^{2\phi}-1)n_i n_j.
}
\]

Here \(n\) is the local reciprocal spatial axis. Because the metric depends only on \(n_i n_j\), the
native axis space is

\[
\boxed{\mathbb{RP}^2=S^2/(n\sim-n),}
\]

with \(S^2\) available as an oriented double cover.

If one adds a new geometric matter principle—

> material content is the irreducible holonomy/enclosed target area of the reciprocal axis around
> infinitesimal loops, while path-only axis variation is non-material—

then the area two-form and its lowest positive CSN norm follow:

\[
F_{\mu\nu}
=n\cdot(\partial_\mu n\times\partial_\nu n),
\qquad
S_{\rm loop}\propto
\int\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}.
\]

That is a **CONDITIONAL derivation from a new principle**, not a consequence already hidden in
Reciprocity.

The more conservative next step is therefore not to adopt the principle. It is to compute the full
curvature of the generalized reciprocal-axis metric and ask whether the metric-only conformal action
itself generates the required orientation-strain functional.

## 1. Exact non-implication from the existing foundation

For the scoped \(S^2\) probe, define

\[
M_{\mu\nu}
=\partial_\mu n\cdot\partial_\nu n.
\]

Both

\[
Q_2=\operatorname{tr}(M^2)
\]

and

\[
Q_1-Q_2
=(\operatorname{tr}M)^2-\operatorname{tr}(M^2)
\]

are:

- local covariant four-derivative scalars;
- CSN-compatible in four dimensions;
- parity even;
- invariant under proper target rotations;
- invariant under \(n\mapsto-n\) after squaring;
- statically nonnegative.

For a rank-one derivative field,

\[
\partial_\mu n=v\,\partial_\mu s,
\]

all derivative vectors are proportional. Then

\[
Q_1=Q_2>0
\]

for a nonconstant field, while

\[
Q_1-Q_2=0.
\]

Thus \(Q_2\) is an explicit same-foundation/different-rank-one-cost countermodel. It is not proposed
as UDT physics. It proves that the current principles do not select area-only matter.

Common-Scale Neutrality cannot close the gap: it gauges common metric scale, not variation of an
independent carrier direction. Equating those transformations would be a category error.

## 2. The existing reciprocal-depth group has no loop defect

The derived positional group is one-dimensional:

\[
D(\phi)=\operatorname{diag}(e^{-\phi},e^\phi),
\qquad
J=D^{-1}dD=H\,d\phi.
\]

It is Abelian, and for smooth \(\phi\),

\[
dJ+J\wedge J=0,
\]

because

\[
d^2\phi=0,
\qquad
d\phi\wedge d\phi=0.
\]

Therefore a nonzero loop-holonomy matter tensor cannot be extracted from the scalar depth field
alone:

\[
\boxed{
\text{pure reciprocal depth is locally integrable and loop-flat.}
}
\]

An orientation field, multi-axis state, singularity, or other enlarged geometry is genuinely new
content.

## 3. Conditional single-axis completion of the metric

Suppose the radial reciprocal relation is the symmetry-reduced member of a local state with one
spatial reciprocal axis. Let

\[
P_n=n\otimes n,
\qquad
P_\perp=I-P_n,
\qquad
n\cdot n=1.
\]

The minimal transverse-neutral spatial metric is

\[
\boxed{
h=P_\perp+e^{2\phi}P_n
=I+(e^{2\phi}-1)n\otimes n.
}
\]

Its spatial eigenvalues are

\[
(e^{2\phi},1,1),
\]

so

\[
\det h=e^{2\phi}.
\]

Together with

\[
g_{00}=-e^{-2\phi},
\]

the full determinant is constant:

\[
\boxed{\det g=-1}
\]

in the dimensionless orthonormal convention, or \(-c^2\) with the time-length conversion restored.

For the radial axis \(n=\hat r\),

\[
\delta_{ij}dx^idx^j=dr^2+r^2d\Omega^2,
\qquad
n_i dx^i=dr,
\]

and therefore

\[
h_{ij}dx^idx^j
=e^{2\phi}dr^2+r^2d\Omega^2.
\]

This exactly recovers the reciprocal UDT spatial metric.

### Status

- **DERIVED:** the displayed metric algebra, determinant, and radial reduction.
- **CHOSE conditional extension:** one reciprocal axis and neutral transverse directions exhaust
  the local spatial state.
- **OPEN:** whether general UDT positional geometry has one axis or a larger determinant-one strain
  space.

This is not the quarantined free-\(D_A\) construction: the transverse eigenvalues remain fixed and
the only added datum is the orientation of the already reciprocal longitudinal axis. It nevertheless
extends the live spherical ansatz and requires independent provenance before adoption.

## 4. Why the natural target is \(\mathbb{RP}^2\), not automatically \(S^2\)

The metric depends on

\[
P_n=n\otimes n,
\]

so

\[
P_{-n}=P_n.
\]

Thus the metric sees an unoriented axis:

\[
[n]\in\mathbb{RP}^2.
\]

An oriented vector \(n\in S^2\) is a double-cover representation. It becomes physical only if UDT
distinguishes the two axis orientations through additional structure.

At

\[
\phi=0,
\]

the metric becomes spatially isotropic:

\[
h=I,
\]

and the axis orientation is metrically invisible. This provides a possible geometric locus for
axis defects or topology change, but no dynamics is inferred from it.

For a simply connected compactified spatial domain \(S^3\), every continuous map

\[
S^3\to\mathbb{RP}^2
\]

lifts to \(S^2\), and the covering induces

\[
\pi_3(\mathbb{RP}^2)\cong\pi_3(S^2)\cong\mathbb Z.
\]

Therefore the historical Hopf classification can survive conditionally even if the native target is
an unoriented reciprocal axis. This does not prove that such textures are material or stable.

## 5. Conditional loop-holonomy matter principle

For an oriented local lift \(n\), two coordinate directions map an infinitesimal parallelogram to two
tangent vectors on the axis sphere. Their oriented target-area density is

\[
\boxed{
F_{\mu\nu}
=n\cdot
(\partial_\mu n\times\partial_\nu n).
}
\]

This satisfies:

\[
F_{\nu\mu}=-F_{\mu\nu}.
\]

If the field varies through only one local parameter,

\[
n=n(s(x)),
\]

then all derivatives are proportional and

\[
\boxed{F_{\mu\nu}=0.}
\]

Under the lift reversal \(n\mapsto-n\),

\[
F_{\mu\nu}\mapsto-F_{\mu\nu},
\]

so

\[
F_{\mu\nu}F^{\mu\nu}
\]

is well-defined on \(\mathbb{RP}^2\) even when \(F\) itself changes sign between lifts.

Geometrically, \(F\) measures enclosed target area and the leading holonomy of a transported tangent
frame. It is not a failure of ordinary mixed partial derivatives of \(n\) to commute.

## 6. Why \(F^2\) follows after—not before—the new principle

Adopt conditionally:

> **Reciprocal-Axis Holonomy Matter Principle.** A smooth change of reciprocal-axis orientation
> along a single path is frame/configuration variation, not material content. Matter is the
> irreducible loop holonomy of that axis.

Then the primitive matter object is the antisymmetric two-form \(F\), not \(dn\) itself.

For dimensionless \(n\):

- \(F_{\mu\nu}\) with lower indices has CSN weight zero;
- two inverse metrics give \(F_{\mu\nu}F^{\mu\nu}\) weight \(-4\);
- \(\sqrt{-g}\) has weight \(+4\).

Therefore

\[
\int d^4x\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}
\]

is CSN invariant.

Inside the declared class—local, parity even, quadratic in the primitive loop defect, lowest
derivative order—the positive static norm is unique up to normalization. The parity-odd quadratic
\(F\wedge F\) vanishes pointwise for this decomposable pullback two-form.

Thus

\[
\boxed{
\begin{gathered}
\text{single reciprocal axis}\\
+\ \text{holonomy defines matter}\\
+\ \text{local parity-even lowest positive norm}
\end{gathered}
\Longrightarrow
S_{\rm matter}\propto\int\sqrt{-g}\,F^2.
}
\]

This is a valid conditional derivation. It contains new matter content and is not yet native UDT.

## 7. Why the metric should be tested before adopting the new principle

The single-axis metric already makes \(n\) part of geometry. When \(n(x)\) varies, its derivatives
enter the connection and curvature. The conditional metric action

\[
S_C=\mathcal A\int\sqrt{-g}\,C^2
\]

therefore generates an orientation-strain functional without adding a separate carrier action.

That functional need not equal \(F^2\). Because curvature contains second derivatives of the metric,
it may contain

\[
(\partial^2n)^2,\qquad
(\partial n)^2\partial^2n,\qquad
(\partial n)^4,
\]

with fixed nonlinear combinations.

This is the decisive next metric-native test:

\[
\boxed{
\text{compute }C^2[g(\phi,n)]
\text{ and determine whether its orientation sector reduces to }F^2,
\text{ a larger fixed functional, or zero.}
}
\]

It honors “the metric is the theory” and may derive, replace, or falsify the historical carrier
before a new matter postulate is considered.

## 8. What remains open

Even the conditional holonomy principle does not derive:

- whether the local reciprocal state has one axis;
- why the axis is oriented rather than projective;
- the relative metric–matter coupling;
- a finite stable \(\sigma=R/X\);
- the global boundary/charge and \(\widehat g\);
- an electron branch or its non-mass properties.

The flat \(F^2\)-only scale result remains:

\[
E_4(R)\propto\frac1R,
\]

so no finite unbounded-flat stationary radius follows. Global geometry would still have to select a
dimensionless size.

## 9. Falsification

The conditional holonomy-matter route fails if:

1. the native reciprocal state requires multi-axis strain rather than one axis;
2. a rank-one axis texture carries irreducible material energy;
3. the full metric curvature produces a different unavoidable orientation functional;
4. no regular stable nontrivial branch exists on the complete cell;
5. its predicted ratios fail after one-mass calibration.

The historical \(S^2,F^2\) model would remain a useful conditional approximation only if its scoped
numerical successes survived the native comparison.

## 10. Status ledger

| Claim | Status |
|---|---|
| Existing Reciprocity/CSN implies rank-one-zero | **FALSE; explicit countermodel** |
| Scalar reciprocal-depth current has loop curvature | **NO; identically flat for smooth \(\phi\)** |
| Single-axis metric formula and determinant | **DERIVED conditional algebra** |
| Single-axis completion is forced by current foundation | **NO; CHOSE extension** |
| Metric axis target is \(\mathbb{RP}^2\) | **DERIVED given single-axis metric** |
| \(S^2\) can be an oriented lift | **DERIVED topology/representation** |
| Hopf \(\mathbb Z\) survives on simply connected compactification | **CONDITIONAL-DERIVED** |
| Pullback area form is rank-one-zero | **DERIVED** |
| Holonomy-matter principle selects \(F^2\) | **CONDITIONAL-DERIVED in stated class** |
| Holonomy-matter principle is currently foundational | **NO; candidate only** |
| Metric-only \(C^2[g(\phi,n)]\) orientation action | **OPEN; next analytic test** |
| Stable matter/electron identification | **OPEN** |

## 11. Frontier

\[
\boxed{
\begin{gathered}
\text{Rank-one-zero is not hidden in current Reciprocity.}\\
\text{A single-axis extension makes an }\mathbb{RP}^2\text{ carrier geometric, with }S^2\text{ as lift.}\\
\text{Loop-holonomy matter would derive }F^2\text{ but is a new principle.}\\
\text{Next: let the generalized metric decide its own orientation functional.}
\end{gathered}}
\]

## 12. Verification scope

The dependency-free script checks 27 exact statements: the single-axis metric eigenvalues,
determinant and \(n\sim-n\) identity; target tangency and area antisymmetry; rank-one countermodel;
flatness of the one-dimensional depth wedge; orientation and \(O(3)\) behavior; Gram identity; CSN
weight; decomposable \(F\wedge F=0\); and static norm positivity. It does not derive the single-axis
extension, loop-holonomy matter principle, full curvature action, stable branch, or electron.

