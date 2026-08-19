# G170 exact derivation — endpoint-relative bidirectional pair response

Date: 2026-08-19

## 1. The distinction recovered from the original endpoint work

A regular calibrated endpoint pair metric has the unique form

\[
h_X=-T_X^2(dy^0+\beta_Xdy^1)^2+L_X^2(dy^1)^2,
\qquad T_X,L_X>0.
\]

Therefore

\[
\det h_X=-T_X^2L_X^2,
\qquad
\Phi_X=\frac12\log\frac{L_X}{T_X}
=\frac14\log\frac{-\det h_X}{h_{00,X}^2},
\]

and the terminal reciprocal-\(c_E\) readout is

\[
q_X=\frac{c_{{\rm eff},X}^{({\rm pair})}}{c_E}
=\frac{T_X}{L_X}=e^{-2\Phi_X}.
\]

The 2026-08-09 derivation already proved that the ordered pair depth is not either endpoint density
alone. On one consistently calibrated pair tape it is

\[
\boxed{
\delta_{AB}
=-\frac12\log\frac{q_B}{q_A}
=\frac12\log\frac{L_B/T_B}{L_A/T_A}
=\Phi_B-\Phi_A.
}
\]

G170 restores this distinction after G169 temporarily conflated \(\Phi_A\) and \(\Phi_B\) with the
directed arrow depth.

## 2. Consistently calibrated pair-groupoid theorem

Let \(S_{\mathcal C}\) be one supplied family of regular endpoint states carrying the same
reciprocal calibration \(\mathcal C\). The 2026-08-09 realization is two points on one consistently
calibrated pair surface. Let \(q:S_{\mathcal C}\rightarrow\mathbb R_{>0}\) be the metric terminal
readout above. For an ordered pair inside that calibrated family define

\[
q_{AB}=\frac{q_B}{q_A},
\qquad
\delta_{AB}=-\frac12\log q_{AB}.
\]

Then, without any additional physical or ontological premise,

\[
q_{BA}=q_{AB}^{-1},
\qquad
\delta_{BA}=-\delta_{AB}.
\]

For a literally shared middle calibrated state,

\[
q_{AB}q_{BC}
=\frac{q_B}{q_A}\frac{q_C}{q_B}
=\frac{q_C}{q_A}=q_{AC},
\]

and hence

\[
\delta_{AB}+\delta_{BC}=\delta_{AC}.
\]

With \(\chi_{AB}=\tanh\delta_{AB}\), reversal is odd and matched composition has the usual bounded
form.

This is also the general form of a real cocycle on the thin pair groupoid of
\(S_{\mathcal C}\). Fix a reference state \(O\) in the same calibration class and write
\(\Phi_X=\delta_{OX}\). The composition identity
\(\delta_{OB}=\delta_{OA}+\delta_{AB}\) forces
\(\delta_{AB}=\Phi_B-\Phi_A\). The metric terminal readout fixes which endpoint potential is the
primary reciprocal channel.

This theorem does not create arrows between disjoint endpoint families carrying independently
chosen reciprocal calibrations. Such arrows require an explicit calibration carry. Under
\(\Phi_X\mapsto\Phi_X+c_X\), the candidate cross-family depth changes by \(c_B-c_A\).

If the middle state is rebuilt independently on the two pair tapes, the exact residual is

\[
(\Phi_{B,{\rm left}}-\Phi_A)
+(\Phi_C-\Phi_{B,{\rm right}})
-(\Phi_C-\Phi_A)
=\Phi_{B,{\rm left}}-\Phi_{B,{\rm right}}.
\]

Thus matched composition is derived, while arbitrary triangle closure remains correctly excluded.

## 3. Recovery of the founded G166 kernel

Choose A as the calibrated tape origin:

\[
T_A=L_A=1,
\qquad \Phi_A=0.
\]

For the founded B block,

\[
T_B=e^{-d},
\qquad L_B=e^d,
\]

so

\[
q_{AB}=e^{-2d},
\qquad
\delta_{AB}=d,
\qquad
\delta_{BA}=-d.
\]

G166 is therefore the anchored special case of the two-endpoint rule rather than a competing
single-endpoint definition.

## 4. Reclassification of the G169 surface witness

G169 used the exact endpoint metrics

\[
h_A=h_B=
\begin{pmatrix}
-1&0\\
0&1+a^2
\end{pmatrix}.
\]

Each endpoint has

\[
\Phi_A=\Phi_B=\frac14\log(1+a^2).
\]

At \(a=1\), each density is \(\log 2/4\). But the directed relation is

\[
\delta_{AB}=\Phi_B-\Phi_A=0,
\qquad
\delta_{BA}=\Phi_A-\Phi_B=0.
\]

Hence

\[
\delta_{BA}=-\delta_{AB}
\]

holds exactly. The witness remains valuable: it disproves using a single endpoint density as arrow
depth. It does not disprove metric-derived reciprocal reversal after the endpoints are compared.

## 5. The full orchestra remains inside each endpoint

For the primary static-spherical metric, G167 gives

\[
h_X=Y_X^TB_X^T\eta_2B_XY_X+Z_X^TQ_X^TQ_XZ_X.
\]

G170 evaluates two nonradial endpoints. At A,

\[
h_A=
\begin{pmatrix}
-391/100&9/50\\
9/50&2
\end{pmatrix},
\qquad
P_A=
\begin{pmatrix}
9/100&9/50\\
9/50&1
\end{pmatrix},
\]

with

\[
q_A^2=\frac{152881}{78524},
\qquad
(q_A^2)_{\rm base}=4.
\]

At B,

\[
h_B=
\begin{pmatrix}
-36699/10000&3739/7500\\
3739/7500&12446/5625
\end{pmatrix},
\]

and

\[
q_B^2=\frac{12121349409}{7531774000},
\qquad
(q_B^2)_{\rm base}=\frac{2531281}{627264}.
\]

Both endpoint shifts are nonzero and both angular Gram matrices change the terminal readout before
the relative ratio is formed. The exact squared relative ratio is

\[
q_{AB}^2=\frac{237954210248079}{287866285223500},
\qquad
q_{BA}^2=(q_{AB}^2)^{-1}.
\]

No scalar \(\mu\) or post-readout angular correction occurs.

## 6. Common scale and calibration

Under independent positive common endpoint rescalings

\[
h_A\mapsto\Omega_A^2h_A,
\qquad
h_B\mapsto\Omega_B^2h_B,
\]

each \(q_X\) is unchanged because both numerator and denominator scale equally. Consequently
\(q_{AB}\) and \(\delta_{AB}\) are unchanged.

A shared reciprocal-origin change \(\Phi_X\mapsto\Phi_X+c\) also cancels. Independent reciprocal
recalibrations do not cancel:

\[
(\Phi_B+c_B)-(\Phi_A+c_A)
=\delta_{AB}+c_B-c_A.
\]

That is a load-bearing calibration-carry boundary, not a failure of the endpoint-difference
algebra. Two differently calibrated experiments are different inputs until a lawful cross-query
carry is supplied. The theorem applies to one supplied consistently calibrated two-endpoint
calculation.

## 7. What co-presence does not do

No co-presence equation or premise appears in the derivation or implementations. The observer
pair, endpoint metrics, and calibration are the arguments of the evaluator. The metric does not
need to select which observers an experiment compares.

The remaining non-scalar problem is separate. A complete relation may retain screen orientation,
shift state, connection, or holonomy data not compressed by \(q\). G170 derives the primary scalar
reversal and matched scalar composition; it does not claim full matrix carry closure.

## 8. Landing

```text
ENDPOINT_RELATIVE_RECIPROCAL_DEPTH_DERIVED_FROM_TERMINAL_CEFF_RATIOS
__WITHIN_ONE_CONSISTENT_RECIPROCAL_CALIBRATION_CLASS
__BIDIRECTIONAL_REVERSAL_AND_MATCHED_COMPOSITION_AUTOMATIC
__G169_SINGLE_ENDPOINT_REVERSAL_COUNTEREXAMPLE_RECLASSIFIED
__COPRESENCE_NOT_LOAD_BEARING
__CROSS_QUERY_AND_FULL_NONSCALAR_CARRY_REMAIN_OPEN
```

This is a bounded integration repair, not a derivation of a positive metric-space distance or a
global theory. It establishes that the directed reciprocal scalar response is already metric-owned
once the actual calibrated observer endpoints are supplied.
