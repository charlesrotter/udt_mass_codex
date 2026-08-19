# G174 exact derivation — native calibrated pair-germ chart ownership

Date: 2026-08-19

## Landing

`CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS`

G173's calibration density is not a second field added to the pair metric. It is exactly the
Jacobian between an arbitrary auxiliary curve parameter and the ruler coordinate already required
by the terminal reciprocal construction. Once that calibrated ruler coordinate—or equivalently
its nonzero tangent vector or ruler one-form—is supplied, the density and terminal scalar are
unique. Distinct G173 densities define distinct calibrated germs on the same unparameterized line.

The simplification is bounded. The primary metric and an unscaled pair plane do not choose the
physical ruler calibration. G174 removes a false downstream scalar ambiguity; it does not solve
the upstream ownership and carry problem.

## 1. G173 tensor in an auxiliary chart

Use the declared primary metric in dimension-matched time,

\[
g=-e^{-2\phi}(dx^0)^2+e^{2\phi}dr^2+r^2\gamma_{S^2},
\]

and the supplied static time-orthogonal image

\[
F(x^0,\sigma)=(x^0,r(\sigma),\gamma(\sigma)).
\]

Set

\[
v=\frac{dr}{d\sigma},\qquad
b^2=\gamma_{S^2}(\dot\gamma,\dot\gamma),\qquad
H=e^{2\phi}v^2+r^2b^2.
\]

G173 gives

\[
h_\sigma=F^*g=
\begin{pmatrix}
-e^{-2\phi}&0\\
0&H
\end{pmatrix}.
\]

The tensor is Lorentzian whenever the complete spatial tangent is nonzero. In particular,
`v=0,b>0` is regular. Only `v=b=0` loses rank.

The symbol \(\sigma\) is not yet the physical ruler coordinate. It is only an arbitrary regular
parameter on the same image.

## 2. The calibration density is a Jacobian

Let \(s\) be the ruler coordinate of the supplied calibrated pair map. Locally write

\[
ds=\mu(\sigma)d\sigma,
\qquad \mu\ne0,
\qquad m=|\mu|>0.
\]

The calibrated spatial tangent is

\[
R=F_*\partial_s=\frac{1}{\mu}F_*\partial_\sigma.
\]

In the calibrated coordinates \((x^0,s)\), the pair metric is therefore

\[
\boxed{
h_s=
\begin{pmatrix}
-e^{-2\phi}&0\\
0&H/m^2
\end{pmatrix}.
}
\]

Its terminal reciprocal scalar is

\[
\boxed{
e^{4\Phi_s}
=\frac{-\det h_s}{h_{00,s}^2}
=\frac{e^{2\phi}H}{m^2}.
}
\]

This is exactly G173's \(\Phi_m\). Thus \(m\) is not an extra post-pullback response. It records
how the arbitrary display parameter \(\sigma\) is related to the supplied physical ruler
coordinate \(s\).

## 3. Auxiliary-chart covariance

Let \(\sigma=\sigma(\widetilde\sigma)\) with

\[
\lambda=\frac{d\sigma}{d\widetilde\sigma}\ne0.
\]

Then

\[
\widetilde H=\lambda^2H,
\qquad
\widetilde\mu=\lambda\mu,
\qquad
\widetilde m=|\lambda|m.
\]

The calibrated tangent is unchanged:

\[
F_*\partial_s
=\frac{1}{\mu}F_*\partial_\sigma
=\frac{1}{\widetilde\mu}F_*\partial_{\widetilde\sigma}.
\]

Consequently

\[
\frac{\widetilde H}{\widetilde m^2}=\frac{H}{m^2},
\qquad
\widetilde\Phi_s=\Phi_s.
\]

This is ordinary covariance: the auxiliary components and calibration density change together,
while the calibrated pair metric does not.

Holding \(m\) fixed while rescaling the tangent is not this coordinate change. It changes
\(ds/d\sigma\), hence changes the ruler calibration.

## 4. Uniqueness for one calibrated germ

Fix a nonzero auxiliary tangent \(S=F_*\partial_\sigma\) and a nonzero calibrated ruler vector
\(R=F_*\partial_s\) on the same oriented line. If

\[
S=\mu R=\nu R,
\]

then

\[
(\mu-\nu)R=0.
\]

Because \(R\ne0\), \(\mu=\nu\), and therefore \(m=|\mu|\) is unique. Equivalently, a supplied
ruler one-form \(ds\) fixes \(m=|ds(\partial_\sigma)|\).

The weaker object, an unoriented line or two-plane, does not fix a vector scale. Replacing

\[
R\mapsto c^{-1}R,
\qquad
m\mapsto cm,
\qquad c>0,
\]

preserves the line and image but changes the calibrated ruler. This is exactly the freedom seen by
G173 after it intentionally forgot the calibrated parameterization.

Therefore there cannot be two terminal reciprocal scalars for the same complete input
\((g,F,x^0,s)\). Apparent alternatives either are auxiliary charts with the density transformed
lawfully, in which case the scalar agrees, or are different calibrations, in which case the input
has changed.

## 5. Constant unit changes versus varying recalibration

Let \(n=cm\) with one positive constant \(c\) along an entire pair tape. Then

\[
\Phi_n=\Phi_m-\frac12\log c.
\]

Every endpoint density shifts by the same constant, so the G170 directed response is unchanged:

\[
\boxed{
[\Phi_n(2)-\Phi_n(1)]
=[\Phi_m(2)-\Phi_m(1)].
}
\]

This is a uniform ruler-unit change. Translation of the ruler origin and orientation reversal also
leave the density response unchanged.

For a position-dependent recalibration \(n=f m\),

\[
\delta_n-\delta_m
=\frac12\log\!\left(\frac{f_1}{f_2}\right).
\]

It changes the grading of the tape between the endpoints and is a different calibrated relation,
not a gauge transformation of one fixed calibration. Cross-calibration carry remains open.

## 6. Reclassification of the G173 witnesses

G173 registered

\[
m_A^2=v^2+r^2b^2,
\qquad
m_P^2=v^2+e^{-2\phi}r^2b^2.
\]

They remain lawful, but their correct type is now explicit:

\[
R_A=\frac{S}{m_A},
\qquad
R_P=\frac{S}{m_P}.
\]

Whenever \(m_A\ne m_P\), they are different calibrated vectors. They define the same
unparameterized line and pair image, but not the same fully calibrated germ.

At a genuine radial turn,

\[
m_P=e^{-\phi}m_A,
\qquad
R_P=e^{\phi}R_A,
\]

and the two readouts are

\[
\Phi_A=\frac{\phi}{2},
\qquad
\Phi_P=\phi.
\]

For the exact witness

\[
e^{2\phi}=4,
\qquad r=3,
\qquad v=0,
\qquad b^2=1,
\]

one has

\[
m_A^2=9,
\qquad m_P^2=\frac94,
\qquad e^{4\Phi_A}=4,
\qquad e^{4\Phi_P}=16.
\]

The disagreement is therefore evidence that the calibrated vectors differ. It is not evidence
that one calibrated vector produces two scalar answers.

On a pure radial segment, \(m_A=m_P=|v|\), so both recover G172. Along a general interval they
belong to the same directed-response calibration class only when \(m_P/m_A\) is constant. Current
premises do not force that condition or select either density. Neither is selected here.

## 7. Exact regrade of G168 and G173

G168 derived a unique pair plane from a supplied nonzero separation germ and explicitly noted that
positive rescaling preserves the plane while terminal components retain their calibration. G174
sharpens that boundary:

- a separation **line** owns the plane but not the ruler scale;
- a calibrated separation **vector** or ruler one-form owns the scale locally;
- a supplied calibrated pair map carries that datum along its domain;
- bare observer labels and the primary metric still do not select the physical calibrated map.

G173's tensor and rank theorem survives unchanged. Its calibration-atlas nonuniqueness is retained
as a classification of uncalibrated line/image data. It is not a nonuniqueness theorem for the
terminal kernel on one fully calibrated pair metric.

## 8. Premise and conclusion ledger

- `DERIVED_BOUNDED`: \(m=|ds/d\sigma|\), the calibrated-coordinate pullback, auxiliary-chart
  covariance, uniqueness of \(m\) for a fixed nonzero calibrated vector, and constant-unit
  cancellation from endpoint depth.
- `RETAINED_DERIVED_BOUNDED`: G173 tensor regularity at `v=0,b>0` and rank loss only at zero complete
  spatial tangent.
- `RECLASSIFIED`: `m_A` and `m_P` are different supplied calibrations when they differ, not multiple
  outputs from one fully calibrated germ.
- `CHOSE_BOUNDED_CLASS`: static, time-orthogonal, spherical, `r>0` turning families.
- `SUPPLIED_CONDITIONAL`: the calibrated pair germ or ruler coordinate.
- `OPEN`: which physical pair relation supplies that calibration, how it is carried across
  independently built pair tapes, and all ambient/global extensions.
- `INACTIVE`: co-presence, G142--G160 scaffolds, `X_max`, fitting, observations, action, source,
  matter, bootstrap, and signalling.

## Maximum conclusion

```text
CALIBRATED_GERM_OWNS_UNIQUE_SCALAR
__UNCALIBRATED_LINE_RETAINS_ATLAS
__G173_TENSOR_AND_RANK_THEOREM_RETAINED
__PHYSICAL_CALIBRATION_AND_CARRY_OWNER_REMAIN_OPEN
```

No path, dynamics, physical ruler selection, global completion, or downstream observational claim
has been derived.
