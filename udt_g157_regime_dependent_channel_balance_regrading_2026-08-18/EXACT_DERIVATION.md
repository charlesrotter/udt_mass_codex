# G157 exact derivation — lawful composition does not mean fixed channel balance

## 1. The complete positive-triangular pair transition

Let a supplied typed observer comparison have total transition

\[
C=\begin{pmatrix}a&n\\0&d\end{pmatrix},
\qquad a,d>0.
\]

It has the unique coordinates

\[
\boxed{
\sigma=\frac12\log(ad),\qquad
\delta=\frac12\log\frac da,\qquad
\mu=\frac na,
}
\]

and therefore

\[
\boxed{
C(\sigma,\delta,\mu)
=e^\sigma
\begin{pmatrix}e^{-\delta}&0\\0&e^{\delta}\end{pmatrix}
\begin{pmatrix}1&\mu\\0&1\end{pmatrix}.
}
\]

The three coordinates have distinct roles:

- \(\sigma\): common-scale/determinant grading;
- \(\delta\): reciprocal clock/ruler grading;
- \(\mu\): normalized shift carried by the upper-unipotent channel.

The Jacobian from \((\sigma,\delta,\mu)\) to the three matrix entries has determinant

\[
-2e^{3\sigma-\delta}\ne0.
\]

Thus the complete positive-triangular arena contains three locally independent channels. No
algebraic relation \(\sigma=f(\delta)\), \(\mu=g(\delta)\), or fixed relative channel strength
follows from its type.

## 2. The native base-transition semidirect score

For chronological matrix composition \(C_2C_1\), direct multiplication gives

\[
\boxed{
(\sigma_2,\delta_2,\mu_2)*(\sigma_1,\delta_1,\mu_1)
=\left(
\sigma_2+\sigma_1,
\delta_2+\delta_1,
\mu_1+e^{2\delta_1}\mu_2
\right).
}
\]

The inverse is

\[
\boxed{
(\sigma,\delta,\mu)^{-1}
=(-\sigma,-\delta,-e^{-2\delta}\mu).
}
\]

Common scale is central in \(B^+(2)\). Reciprocal depth acts nontrivially on normalized shift:

\[
D(\delta)U(\mu)D(-\delta)=U(e^{-2\delta}\mu).
\]

This is coupling, not lockstep. These base channels compose as one transition, but the amount
carried in each channel need not be proportional or constant across regimes.

The proof is exactly scoped to \(B^+(2)\). It does not yet give the group law for all complete
coframe screen and mixing variables. Since a lawful three-channel subarena already admits changing
balance, however, no universal claim that *all* channels must march at fixed ratios can follow from
composition alone.

## 3. Exact changing-balance family

Consider the smooth positive-triangular endpoint frame family, for \(t\ge0\),

\[
R(t)=\begin{pmatrix}1+t&t^2\\0&1+t^2\end{pmatrix}.
\]

At \(t=0,1,2\),

\[
R_0=I,
\qquad
R_1=\begin{pmatrix}2&1\\0&2\end{pmatrix},
\qquad
R_2=\begin{pmatrix}3&4\\0&5\end{pmatrix}.
\]

Their common-scale, reciprocal, and normalized-shift balances are plainly not fixed. Nevertheless,
the edge comparisons

\[
C_{ji}=R_jR_i^{-1}
\]

obey

\[
C_{21}C_{10}=C_{20}
\]

exactly. This telescoping construction works for arbitrary smooth regular endpoint-state functions.
It is a kinematic existence theorem, not a claim that this polynomial family is physical.

## 4. Where lockstep would actually enter

Suppose one additionally demands that the **entire \(B^+(2)\) transition** be a one-parameter
subgroup of one scalar parameter \(t\):

\[
C(t+u)=C(t)C(u).
\]

For a fixed generator, the channels are then constrained to

\[
\sigma(t)=pt,
\qquad
\delta(t)=qt,
\qquad
\mu(t)=r\frac{e^{2qt}-1}{2q}
\]

for \(q\ne0\), with \(\mu(t)=rt\) when \(q=0\). The generator constants \((p,q,r)\) fix the entire
channel relationship.

That is a legitimate conditional ansatz, but it is stronger than composition of arbitrary
observer relations. The founding result

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{\delta})
\]

derives precisely the reciprocal \(\sigma=\mu=0\) subgroup after ordered reciprocal depth is
supplied. It does not say that the full \(B^+(2)\) comparison must be only a function of that one
depth.

Promoting the founded reciprocal one-parameter subgroup into a depth-only law for the full
\(B^+(2)\) comparison would therefore be scaffolding. Full screen/mixing composition remains open.

## 5. Regrading the recent chain

The 20-source ledger finds no active statement imposing that scaffolding.

### Expected freedom, not a missing selector

- G141 and G156 already separate determinant, reciprocal, and shift characters.
- G148--G150 demonstrate independent first-jet liveness and, for four named outputs, local
  surjectivity. These are capacity results for changing balance, not failures to select one ratio.
- G153 shows the realized differential depends on live metric/history derivatives.
- G154's response classes characterize possible supplied histories. They need not be interpreted as
  instruments that should have been forced into one universal strength.

### History values, not an extra chooser

G145 proves that a rank-complete valued relation network can encode its supplied metric history.
The changing channel balance can be part of those values—the score represented by that history.
This is a reconstruction statement, not a physical-history or dynamics theorem. A separate demand
that all channels share one ratio is not required.

What remains open is how the values are determined or propagated: by a future native equation,
global condition, or supplied initial/boundary/observational data. That is a law/data question, not
a demand for lockstep.

### Genuine open types that do not disappear

- G142--G144 still do not construct a nonisometric carry between unrelated query sheets.
- G146--G147 still require a typed output protocol, physical carrier, or independent screen solder
  for claims that need them.
- G155 still finds no active common-scale constraint or evolution equation; kinematic permission to
  vary \(\kappa\) is not a prediction of its realized variation.
- singular/global completion and the physical query population remain open.

## 6. Landing

`MIXED_REGRADING__BPLUS2_NO_FIXED_CHANNEL_RATIO_DERIVED__REGIME_DEPENDENT_BASE_BALANCE_ALLOWED_BY_NATIVE_SEMIDIRECT_COMPOSITION__SUPPLIED_VALUED_HISTORY_CAN_CARRY_CHANGING_SCORE__FULL_SCREEN_MIXING_COMPOSITION_PHYSICAL_CROSS_QUERY_CARRY_AND_HISTORY_EVOLUTION_REMAIN_OPEN`

The poor framing was present mainly in repeated selection language and conversational goals, not as
an active equation in the current banked chain. Most algebra survives unchanged. The correction is
to stop treating independent regime amplitudes as defects while retaining the genuine distinction
between allowed histories and a law or data that determines the realized score.

No physical regime profile, loud--quiet--loud prediction, full screen/mixing composition law,
action, source, or history is derived.
