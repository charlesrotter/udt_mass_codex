# G173 exact derivation — primary-metric turning-chart calibration atlas

Date: 2026-08-19

## Landing

`PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE`

At a radial turn, the primary-metric pair tensor remains smooth and Lorentzian whenever the
angular tangent is nonzero. What fails is only the G172 calibration by areal radius. The raw
terminal component formula is an affine log-density under spatial reparameterization, so a scalar
readout requires one positive line-density calibration. The active premises do not select a unique
such density through the turn.

Two distinct densities constructed from the declared metric, areal radius, and supplied tangent
both transform lawfully, remain positive at a genuine turn, and recover the G172 radial answer on
purely radial segments. They nevertheless disagree for generic nonradial data. Therefore the
metric owns the complete tensor and a calibration atlas, not one unique finite scalar extension of
the G172 areal chart.

## 1. General static non-areal family

Use the declared primary metric in dimension-matched time,

\[
g=-e^{-2\phi(r)}(dx^0)^2+e^{2\phi(r)}dr^2+r^2\gamma_{S^2},
\]

and a supplied smooth time-independent immersion

\[
F(x^0,\sigma)=(x^0,r(\sigma),\gamma(\sigma)),
\qquad r>0.
\]

Write

\[
v=\frac{dr}{d\sigma},
\qquad
b^2=\gamma_{S^2}\!\left(\frac{d\gamma}{d\sigma},
\frac{d\gamma}{d\sigma}\right)\ge0.
\]

The tangent fields are

\[
K=\partial_{x^0},
\qquad
S=v\partial_r+\dot\gamma.
\]

Their complete pullback is

\[
\boxed{
h=F^*g=
\begin{pmatrix}
-e^{-2\phi}&0\\
0&H
\end{pmatrix},
\qquad
H=e^{2\phi}v^2+r^2b^2.
}
\]

Thus

\[
\boxed{\det h=-e^{-2\phi}H.}
\]

For finite \(\phi\) and \(r>0\), \(H>0\) exactly when \(v\) and the angular tangent do not both
vanish. Hence:

- `v != 0`: the monotone-radial G172 overlap;
- `v = 0`, `b > 0`: a regular radial turn or pure-angular tangent, with
  \(\det h=-e^{-2\phi}r^2b^2<0\);
- `v = b = 0`: the spatial tangent vanishes, the immersion drops to rank one, and \(\det h=0\).

The true first local rank boundary is therefore zero **complete** spatial tangent, not zero radial
component.

The explicit immersion already proves integrability. Independently, time independence gives

\[
[K,S]=0
\]

even at \(v=0\). No co-presence, path, or dynamics premise enters.

## 2. The raw terminal component is not a scalar

Applying the terminal component formula directly in the \((x^0,\sigma)\) chart gives

\[
\Phi_\sigma^{\rm raw}
=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right)
=\frac14\log\!\left(e^{2\phi}H\right).
\]

Let \(\sigma=\sigma(\widetilde\sigma)\) be a regular reparameterization and set

\[
\lambda=\frac{d\sigma}{d\widetilde\sigma}\ne0.
\]

Then

\[
\widetilde v=\lambda v,
\qquad
\widetilde b^2=\lambda^2b^2,
\qquad
\widetilde H=\lambda^2H,
\]

so

\[
\boxed{
\widetilde\Phi^{\rm raw}
=\Phi^{\rm raw}+\frac12\log|\lambda|.
}
\]

The raw component is therefore an affine log-density. Calling it a scalar without a declared
spatial calibration would be a type error.

## 3. General calibrated scalar chart

A lawful spatial calibration is a positive weight-one line density \(m\) along the supplied
family:

\[
\widetilde m=|\lambda|m.
\]

Define

\[
\boxed{
\Phi_m
=\Phi^{\rm raw}-\frac12\log m
=\frac14\log\!\left(\frac{e^{2\phi}H}{m^2}\right).
}
\]

The two transformation terms cancel, so \(\Phi_m\) is invariant under every regular orientation-
preserving or orientation-reversing reparameterization. For two calibrations \(m,n\),

\[
\boxed{
\Phi_n-\Phi_m=\frac12\log\frac{m}{n}.
}
\]

This is a chart transition, not a force, holonomy, or new physical channel.

## 4. Exact G172 overlap

Where \(v\ne0\), the G172 areal-radius calibration is

\[
m_r=|v|.
\]

It gives

\[
\begin{aligned}
\Phi_r
&=\frac14\log\!\left(\frac{e^{2\phi}H}{v^2}\right)\\
&=\phi+rac14\log\!\left(
1+r^2e^{-2\phi}\frac{b^2}{v^2}
\right),
\end{aligned}
\]

which is exactly G172 with \(a^2=b^2/v^2\).

For any non-areal calibration \(m\), the exact overlap law is

\[
\boxed{
\Phi_m
=\Phi_r+rac12\log\frac{|v|}{m}.
}
\]

Thus the tensor agrees on the overlap, while its scalar components are related by calibration
transition rather than numerical equality.

## 5. Two inequivalent metric-built turning calibrations

The declared spherical metric supplies areal radius, the unit-sphere angular Gram, and the
reciprocal factor \(e^{-2\phi}\). Two positive weight-one densities constructed only from those
objects and the supplied tangent are

\[
\boxed{m_A^2=v^2+r^2b^2,}
\]

the undilated areal-reference spatial density, and

\[
\boxed{m_P^2=v^2+e^{-2\phi}r^2b^2=e^{-2\phi}H,}
\]

the clock-weighted proper-spatial density. Both scale by \(|\lambda|\), are positive whenever the
complete spatial tangent is nonzero, and contain no fitted coefficient or selected curve.

Their invariant readouts satisfy

\[
e^{4\Phi_A}
=\frac{e^{2\phi}(e^{2\phi}v^2+r^2b^2)}{v^2+r^2b^2},
\]

while

\[
\boxed{e^{4\Phi_P}=e^{4\phi},\qquad \Phi_P=\phi.}
\]

On a purely radial tangent \(b=0\), both give

\[
\Phi_A=\Phi_P=\Phi_r=\phi.
\]

At a genuine radial turn \(v=0,b>0\), however,

\[
\boxed{
\Phi_A=\frac{\phi}{2},
\qquad
\Phi_P=\phi.
}
\]

They differ whenever \(\phi\ne0\). The exact rational witness

\[
e^{2\phi}=4,
\qquad r=3,
\qquad v=0,
\qquad b^2=1
\]

has

\[
\det h=-\frac94,
\qquad
e^{4\Phi_A}=4,
\qquad
e^{4\Phi_P}=16.
\]

This falsifies both radial-turn rank failure and unique scalar calibration under the active gates.

More generally, every supplied positive scalar \(f\) gives the algebraic density

\[
m_f^2=v^2+f r^2b^2,
\]

with radial recovery and turning value

\[
e^{4\Phi_f}\big|_{v=0}=\frac{e^{2\phi}}{f}.
\]

G173 does not promote arbitrary \(f\) to physics. This family only displays the size of the
calibration solution space; \(f=1\) and \(f=e^{-2\phi}\) are the two registered metric-built
witnesses.

## 6. No finite pointwise extension of the G172 scalar

Let \(\sigma_0\) be an isolated genuine radial turn with \(v(\sigma_0)=0\) and
\(b(\sigma_0)>0\). Suppose a positive continuous calibration \(m\) obeys

\[
\Phi_m=\Phi_r
\]

at every neighboring point where \(v\ne0\). Since \(e^{2\phi}H>0\), equality of the two readouts
forces

\[
m^2=v^2
\]

throughout that punctured neighborhood. Continuity then gives

\[
m^2(\sigma_0)=0,
\]

contradicting the required positive calibration at the turn.

Therefore no finite smooth scalar chart can be numerically identical to the G172 areal scalar at
every punctured monotone point and also remain calibrated at the turn. The finite non-areal charts
are related to G172 by the exact transition term above. The divergence of \(\Phi_r\) as
\(v\to0\) with \(b>0\) is a calibration singularity, not a tensor singularity.

## 7. Reversal and telescoping remain calibration-local

For one fixed calibration density \(m\) on a connected regular family, define

\[
\delta_m(\sigma_1,\sigma_2)
=\Phi_m(\sigma_2)-\Phi_m(\sigma_1).
\]

Then reversal and telescoping are exact endpoint identities. Changing from \(m\) to \(n\) changes
the endpoint difference by

\[
\delta_n-\delta_m
=\frac12\log\!\left(
\frac{m_2/n_2}{m_1/n_1}
\right).
\]

This is the G170 calibration-class boundary. G173 does not invent a cross-calibration carry or
promote scalar closure to screen, connection, Jacobi, orientation, or holonomy transport.

## 8. Premise and conclusion ledger

- `DERIVED_BOUNDED`: full non-areal pullback, determinant, rank classification, affine raw
  transformation, calibrated scalar formula, overlap transitions, regular-turn theorem, and true
  zero-spatial-tangent boundary.
- `DERIVED_NONUNIQUENESS_UNDER_ACTIVE_GATES`: both \(m_A\) and \(m_P\) survive the registered
  covariance, positivity, radial-recovery, and metric/germ-provenance gates but disagree.
- `CHOSE_BOUNDED_CLASS`: static, time-orthogonal, spherical, \(r>0\) pair surfaces.
- `SUPPLIED`: \(\phi(r)\), the regular metric interval, and the smooth pair family.
- `OPEN`: physical calibration/family ownership, any rule preferring one atlas chart, turning
  extension with time-live shift, nonspherical/micro assembly, center and global completion, and
  non-scalar transport.
- `INACTIVE`: co-presence, `X_max`, G142--G160, fits, observations, action, source, matter,
  bootstrap, and signalling.

The maximum conclusion is local calibration-atlas nonuniqueness in the declared primary metric
slice. It is not a theorem that physical UDT has multiple rulers, nor permission to choose one by
phenomenology. A future native relation law may select a calibration; no active premise currently
does.
