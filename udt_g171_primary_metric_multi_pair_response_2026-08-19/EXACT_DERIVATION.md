# G171 exact derivation — primary-metric multi-pair response

Date: 2026-08-19

## 1. Native object and notation

Let each ordered pair relation (e=XY) supply its own regular calibrated endpoint germs. The
declared primary metric is pulled back at both ends:

\[
h_{X|e}=F_e^*g\big|_X,
\qquad
h_{Y|e}=F_e^*g\big|_Y.
\]

The angular Gram and every live component of that germ are already inside each (h). On the
regular Lorentzian stratum define

\[
\Phi_{X|e}
=\frac14\log\!\left(\frac{-\det h_{X|e}}{h_{00,X|e}^2}\right).
\]

G170 then gives the directed scalar response of that pair:

\[
\boxed{\delta_{XY}=\Phi_{Y|XY}-\Phi_{X|XY}.}
\]

The vertical bar matters. It records that the endpoint density comes from the complete (XY)
pair germ. Nothing in the primary metric turns it into a scalar (Phi_X) belonging to observer
(X) independently of every partner and pair calibration.

This construction contains no comparison matrix, calibration torsor, score, selected history,
preferred path, or post-readout orchestra.

## 2. Reversal is pair-local and exact

Reversal swaps the same two completed endpoint pullbacks:

\[
\delta_{YX}^{(e)}
=\Phi_{X|e}-\Phi_{Y|e}
=-\delta_{XY}^{(e)}.
\]

It does not independently rebuild the (YX) germ. A separately prepared reverse experiment is a
different pair input until its relation to the first experiment is established.

## 3. Exact three-pair identity

For independently evaluated pairs (AB), (BC), and (AC), define

\[
\Omega_{ABC}
=\delta_{AB}+\delta_{BC}-\delta_{AC}.
\]

Direct substitution gives

\[
\boxed{
\begin{aligned}
\Omega_{ABC}
={}&(\Phi_{B|AB}-\Phi_{B|BC})\\
&+(\Phi_{C|BC}-\Phi_{C|AC})\\
&+(\Phi_{A|AC}-\Phi_{A|AB}).
\end{aligned}}
\]

Therefore arbitrary scalar triangle closure is not an identity of the primary metric. It follows
on the matched subfamily where every incident pair uses the same completed endpoint readout:

\[
\Phi_{A|AB}=\Phi_{A|AC},
\quad
\Phi_{B|AB}=\Phi_{B|BC},
\quad
\Phi_{C|BC}=\Phi_{C|AC}.
\]

Equivalently, if the pair-indexed endpoint densities happen to descend to observer-only values
(\varphi_A,\varphi_B,\varphi_C), then (Omega_{ABC}=0). This is sufficient, not generally
forced. Matching only the middle (B) readout is insufficient to identify an independently
evaluated direct (AC) pair; the (A) and (C) incidence values must match too.

Nonzero (Omega_{ABC}) is not automatically calibration failure, path holonomy, or a force. In
this bounded theorem it says only that three different pair germs were evaluated and their
endpoint densities do not descend to one observer-only scalar field.

## 4. Exact same-observer primary-metric witness

Use the G168 primary-metric point

\[
g=\operatorname{diag}\!\left(-\frac14,4,9,\frac{144}{25}\right)
\]

and hold fixed the event, clock tangent, and base components:

\[
u=(2,0,0,0),
\qquad
s_1=\left(1,\frac12,0,0\right),
\qquad
s_2=\left(1,\frac12,\frac13,\frac14\right).
\]

Only the angular participation differs. Direct metric pullback gives

\[
h_1=
\begin{pmatrix}
-1&-1/2\\
-1/2&3/4
\end{pmatrix},
\qquad
h_2=
\begin{pmatrix}
-1&-1/2\\
-1/2&211/100
\end{pmatrix}.
\]

Their exact difference is the metric-owned angular Gram contribution

\[
h_2-h_1=
\begin{pmatrix}
0&0\\
0&34/25
\end{pmatrix}.
\]

Both pair metrics are regular:

\[
\det h_1=-1,
\qquad
\det h_2=-\frac{59}{25}.
\]

The terminal readouts are

\[
q_1^2=1,
\qquad
q_2^2=\frac{25}{59},
\]

and

\[
\boxed{
\Phi_{B|1}=0,
\qquad
\Phi_{B|2}=\frac14\log\frac{59}{25}.
}
\]

Thus the same metric, event, clock tangent, time component, and radial component do not force an
observer-only endpoint density when the complete pair germ changes. The angular sector does not
act afterward; it changes (h) before the terminal readout.

This witness does not say that every two physical pair germs must differ. It proves that the
primary metric permits and evaluates the distinction natively.

## 5. Exact local triangle witness

Let

\[
p=\frac14\log\frac{59}{25}.
\]

Choose locally realizable radial endpoint readouts equal to zero for the (AB) and (AC) pairs,
and use the angular witness at the (B) incidence of the (BC) pair:

\[
\delta_{AB}=0,
\qquad
\delta_{BC}=-p,
\qquad
\delta_{AC}=0.
\]

Then

\[
\Omega_{ABC}=-p\ne0.
\]

Each edge still reverses exactly when its same endpoint data are exchanged. The nonzero triangle
quantity does not contradict pair Reciprocity; it disproves importing a universal observer-only
potential or arbitrary scalar additivity into a network of independently evaluated pair germs.
The witness is local and does not assert that an arbitrary collection of germs extends to one
global realization.

## 6. Calibration and pair-chart scope

For one pair metric

\[
h=-T^2(dy^0+\beta dy^1)^2+L^2(dy^1)^2
\]

and one shared positive upper-triangular rechart

\[
P=\begin{pmatrix}a&n\\0&d\end{pmatrix},
\qquad a,d>0,
\qquad h'=P^ThP,
\]

direct substitution gives

\[
\Phi(h')-\Phi(h)=\frac12\log\frac da.
\]

Applying the same calibrated rechart at both endpoints shifts both endpoint densities equally and
therefore leaves (delta_{XY}) unchanged. Independent endpoint recharting leaves the exact
residual difference of those two shifts. This is a statement internal to the supplied pair
calibration, not a reason to introduce a separate kernel or carry mechanism.

Spacetime-coordinate changes also leave the pullback tensor itself unchanged. Arbitrary
independent pair recalibrations are different inputs and are not declared gauge.

## 7. Graph interpretation without new machinery

The primary metric supplies a scalar at each **observer–pair incidence** after that pair germ is
supplied. A network therefore has values such as

\[
\Phi_{A|AB},\quad \Phi_{B|AB},\quad \Phi_{B|BC},\quad \Phi_{C|BC},\ldots
\]

rather than automatically having one value per observer. Each edge response is the difference of
its two incidence values. A special network may collapse to one value per observer and telescope;
the general pair-germ-relative network need not.

This is ordinary metric evaluation of different two-planes. It is not an additional field or
mechanism.

## 8. Landing and boundary

```text
PRIMARY_METRIC_PAIR_GERM_RELATIVE_NETWORK
__EACH_ORDERED_PAIR_RESPONSE_NATIVE_FROM_ITS_COMPLETE_PULLBACK
__SAME_PAIR_REVERSAL_AUTOMATIC
__SHARED_OBSERVER_DOES_NOT_FORCE_PAIR_INDEPENDENT_ENDPOINT_DENSITY
__GENERAL_TRIANGLE_ADDITIVITY_NOT_DERIVED_OR_REQUIRED
__MATCHED_ENDPOINT_READOUT_SUBFAMILY_TELESCOPES
__NO_SCAFFOLDED_CARRY_KERNEL
```

This is complete for the displayed local regular scalar algebra of the declared primary metric.
It does not select the physical pair germs, prove global extendability, define a positive
metric-space distance, or derive ambient time dependence, singular strata, completion, `X_max`,
dynamics, action, source, matter, bootstrap, observations, or signalling.
