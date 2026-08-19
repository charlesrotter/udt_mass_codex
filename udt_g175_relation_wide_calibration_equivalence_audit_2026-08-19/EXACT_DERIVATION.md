# G175 exact derivation — relation-wide calibration equivalence

Date: 2026-08-19

## Landing

```text
A_LOCAL_CALIBRATION_DOES_NOT_OWN_RELATION_WIDE_CARRY
__ONE_SUPPLIED_CALIBRATED_PAIR_MAP_DOES
__ALL_ENDPOINT_DEPTHS_FIX_EXACTLY_ONE_CONSTANT_UNIT_CLASS
__POINTWISE_METRIC_UNIT_IS_A_DIFFERENT_CALIBRATION_NOT_THE_FOUNDED_CARRIED_TAPE
```

G175 finds no new scalar ambiguity and no new propagation mechanism. It locates the remaining
boundary exactly. A local ruler calibration at A—even one fixed on an entire neighborhood of A—does
not determine its continuation to B. A supplied relation-wide ruler coordinate does, by G174.
Among such coordinates, the complete endpoint-depth network forgets exactly one positive constant:
the overall choice of ruler unit.

## 1. One bounded regular tape

Use the G173/G174 static time-orthogonal pullback on a connected interval (I):

\[
h_\sigma=
\begin{pmatrix}
-e^{-2\phi}&0\\
0&H
\end{pmatrix},
\qquad
H=e^{2\phi}v^2+r^2b^2>0.
\]

For one supplied ruler coordinate (s), write

\[
ds=\mu\,d\sigma,
\qquad m=|\mu|>0.
\]

Then

\[
h_m=
\begin{pmatrix}
-e^{-2\phi}&0\\
0&H/m^2
\end{pmatrix},
\qquad
K_m:=e^{4\Phi_m}=\frac{e^{2\phi}H}{m^2}.
\]

The tensor, angular contribution, and calibration all precede terminal readout.

## 2. Exact recalibration law

Let (n=fm), where (f:I\to\mathbb R_{>0}) is smooth. This is not an auxiliary-coordinate change:
the image and auxiliary tangent stay fixed while the calibrated ruler vector changes by

\[
R_n=\frac1f R_m.
\]

The terminal quantity transforms as

\[
K_n=\frac{K_m}{f^2},
\qquad
\boxed{\Phi_n=\Phi_m-\frac12\log f}.
\]

For endpoints (p,q\in I),

\[
\delta_m(p,q)=\Phi_m(q)-\Phi_m(p),
\]

and therefore

\[
\boxed{
\delta_n(p,q)-\delta_m(p,q)
=\frac12\log\frac{f(p)}{f(q)}.
}
\]

This retains G170 reversal automatically. It also shows why a constant unit change is invisible and
a varying regrading is not.

## 3. Exact A-anchored counterfamily

Take (I=[0,1]), A at (0), and B at (1). Define the standard smooth shoulder

\[
b(x)=
\begin{cases}
0,&x\le 1/3,\\
\exp\!\left(\frac94-\frac1{(x-1/3)^2}\right),&x>1/3.
\end{cases}
\]

It is (C^\infty), equals zero on an open neighborhood of A, and satisfies (b(1)=1). For any
nonzero real (a), let

\[
f_a(x)=e^{a b(x)}.
\]

Then (n_a=f_am) has exactly the same metric, pair image, auxiliary parameter, orientation, rank,
and calibrated ruler on an entire A-neighborhood. All A jets agree. Yet

\[
f_a(A)=1,
\qquad f_a(B)=e^a,
\]

so

\[
\boxed{
\delta_{n_a}(A,B)-\delta_m(A,B)=-\frac a2\ne0.
}
\]

Thus neither a point calibration nor any finite or infinite local germ at A determines the
relation-wide calibration. An active continuation equation could remove this counterfamily, but
none occurs in the frozen sources.

## 4. Complete classification of scalar-equivalent calibrations

### Theorem

Let (m,n>0) be smooth ruler densities on a connected regular tape. They give identical directed
depths for every endpoint pair if and only if

\[
n=cm
\]

for one positive constant (c) on that tape.

### Proof

Set (f=n/m>0). If all endpoint depths agree, the recalibration law gives

\[
\log f(p)=\log f(q)
\]

for every (p,q). Hence (f=c) is constant. Conversely, constant (f=c) shifts every endpoint
density by the same number (-\tfrac12\log c), so every difference is unchanged. QED.

Therefore the complete scalar network determines a relation-wide calibration only modulo one
constant ruler-unit choice. It does not tolerate a free regime-dependent ratio while preserving
the same scalar response; any such ratio changes endpoint depths unless some other upstream metric
or pair datum changes with it.

## 5. What a supplied calibrated pair map owns

A complete input ((g,F,x^0,s)) supplies (s) on its domain. Its density (m=|ds/d\sigma|), pair
metric, and terminal scalar are then unique by G174. Calling this relation-wide sufficiency a
propagation theorem would reverse the logic: the coordinate is part of the supplied map.

An A-local datum fixes only (s(A)) and its local scale. To extend it one needs an affine structure,
connection, differential equation, integral normalization, or the complete coordinate itself.
None is generated merely by the word "calibrated."

## 6. The pointwise metric-unit option

The metric does provide a canonical local normalization on the supplied spatial curve:

\[
m_{\rm unit}=\sqrt H,
\qquad h_{ss}=1.
\]

It is a lawful metric arclength coordinate, unique up to translation, orientation, and constant
unit convention once the entire curve is supplied. But its terminal readout is

\[
K_{\rm unit}=e^{2\phi},
\qquad \Phi_{\rm unit}=\frac\phi2.
\]

On the founded pure reciprocal radial branch, the founded coordinate has

\[
H=e^{2\phi}v^2,
\qquad m_{\rm founded}=|v|,
\qquad \Phi_{\rm founded}=\phi.
\]

Thus pointwise metric-unit normalization is not the founded carried reciprocal ruler except at
(phi=0). It independently re-normalizes the ruler as the metric changes and thereby removes half
the founded reciprocal imbalance in this bounded chart. Promoting it would be an additional
physical calibration choice, not a consequence of the existing terminal rule.

A different attractive choice enforces (det h=-1):

\[
m_{\det}^2=e^{-2\phi}H,
\qquad \Phi_{\det}=\phi.
\]

This is G173's `m_P`. It preserves the founded scalar but extends determinant-one normalization to
the angular pair metric. No active premise requires that extension, so it remains a lawful
candidate rather than a selected carry law.

## 7. What `c_E` fixes

The observed (c_E) converts A's clock unit into a ruler unit and types

\[
y^0=c_E\tau_A.
\]

Together with a supplied (s_A), it makes the terminal ratio dimensionless. It does not contain a
derivative of (m), an affine connection on the pair domain, or a boundary-value rule. The smooth
counterfamily above leaves the entire A calibration unchanged and therefore respects (c_E) while
changing the B readout.

The founding reciprocal character likewise maps an already-supplied depth to its reciprocal
squeeze. It does not determine the continuation of (m).

## 8. Status and maximum conclusion

- `DERIVED_BOUNDED`: exact recalibration law and constant-unit equivalence theorem.
- `DERIVED_COUNTEREXAMPLE`: A-local calibration, even on a full neighborhood, does not determine
  relation-wide carry under current premises.
- `SUPPLIED_CONDITIONAL`: one relation-wide calibrated pair map is sufficient.
- `DERIVED_OPTION_NOT_SELECTED`: metric arclength is a lawful local normalization but is not the
  founded carried reciprocal calibration.
- `RETAINED`: G170 reversal/telescoping, G171 pair relativity, G173 tensor/rank, and G174 local
  calibrated-germ uniqueness.
- `OPEN`: physical calibrated pair-map ownership, cross-tape carry, and every ambient/global or
  downstream extension.

No path, connection, dynamics, observation, `X_max`, action, source, matter, bootstrap, signalling,
or canon claim follows.
