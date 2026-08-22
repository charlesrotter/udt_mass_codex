# G215 exact derivation — completed scalar descent on shared observer clocks

Date: 2026-08-22

## Bounded landing

```text
COMPLETED_RECIPROCAL_SCALAR_DESCENDS_TO_A_SHARED_CALIBRATED_OBSERVER_CLOCK_GERM
__G171_ANGULAR_SCALAR_DEFECT_REGRADES_TO_AN_UNCOMPLETED_CONTROL
__SCALAR_NETWORK_CYCLES_TELESCOPE_ON_COMMON_CLOCK_CALIBRATION
__INDEPENDENT_EDGE_CLOCK_RECALIBRATION_RETAINS_THE_EXACT_INCIDENCE_DEFECT
__FULL_PAIR_METRIC_AND_IMMERSION_CARRY_REMAIN_STRICTLY_STRONGER
__NO_GERM_POPULATION_METRIC_VALUE_OR_HISTORY_EVOLUTION_DERIVED
```

Status: `EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__DERIVED_CONDITIONAL__NO_SCIENTIFIC_REPAIR`.

## 1. Generic completed incidence

Let one regular auxiliary pair pullback at an observer incidence be

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2,
\qquad T,L_\sigma>0.
\]

If the pair tangents are \(u=F_*\partial_0\) and \(s=F_*\partial_\sigma\), then

\[
T^2=-g(u,u),\qquad
\beta=\frac{g(u,s)}{g(u,u)},\qquad
L_\sigma^2=g(s,s)-\frac{g(u,s)^2}{g(u,u)}.
\]

Thus angular, screen, and mixing contributions enter the full Gram matrix before completion. Under
the G176 working clarification,

\[
m=T L_\sigma=\sqrt{-\det h_\sigma},
\qquad ds=m\,d\sigma.
\]

The completed pair metric is

\[
\boxed{
h_s=-T^2\left(dy^0+B\,ds\right)^2+T^{-2}ds^2,
\qquad B=\frac{\beta}{T L_\sigma},
}
\]

and \(\det h_s=-1\). Its reciprocal endpoint scalar is therefore

\[
\boxed{
\Phi_s=\frac14\log\frac{-\det h_s}{(h_s)_{00}^2}
=-\log T
=-\frac12\log[-g(u,u)].
}
\]

The ruler germ remains present in \(m\), \(B\), the completed pair plane, and its extrinsic data.
It no longer supplies an independent completed scalar once Dual Reciprocity has fixed \(m\).

## 2. Shared-clock incidence theorem

Consider two completed pair germs incident on the same event. If they use the same calibrated clock
tangent and parameter \(u_X\), then both have

\[
T_X=\sqrt{-g(u_X,u_X)}
\]

and hence the same scalar

\[
\boxed{\varphi_X=-\log T_X.}
\]

The incident ruler directions, angular components, auxiliary scales, and shifts may all differ.
They change the remaining completed tuple but not \(\varphi_X\).

Conversely, because \(T>0\) and \(T\mapsto-\log T\) is injective, two completed incidence scalars
agree if and only if their positive clock factors agree. A shared observer label without a shared
clock calibration is therefore insufficient; a shared calibrated clock germ is exact and
sufficient for scalar incidence descent.

## 3. Calibrated chart law

On one G214 overlap let

\[
P=\begin{pmatrix}a&n\\0&d\end{pmatrix},\qquad a,d>0,
\qquad h'=P^ThP.
\]

The first column of \(P\) gives

\[
(h')_{00}=a^2h_{00},\qquad T'=aT,
\]

so

\[
\boxed{\Phi_s'=\Phi_s-\log a.}
\]

The ruler Jacobian \(d\) and shear \(n\) do not enter the completed scalar. For a clock-preserving
incidence identification \(a=1\), the scalar is invariant. Thus the exact cross-pair scalar carry
is the clock calibration; it is not a hidden multiplication of full pair metrics.

## 4. Observer-network theorem

Let a supplied observer network assign one positive calibrated clock factor \(T_X\) to each
observer vertex, reused by every incident completed pair. Put

\[
\varphi_X=-\log T_X,
\qquad
\delta_{XY}=\varphi_Y-\varphi_X
=\log\frac{T_X}{T_Y}.
\]

Equivalently, \(q_X=e^{-2\varphi_X}=T_X^2\) and

\[
q_{XY}=\frac{q_Y}{q_X}.
\]

Every directed cycle telescopes:

\[
\boxed{
\sum_{i=0}^{N-1}\delta_{X_iX_{i+1}}=0,
\qquad
\prod_{i=0}^{N-1}q_{X_iX_{i+1}}=1,
\qquad X_N=X_0.
}
\]

This is scalar descent only. It neither composes the distinct pair metrics nor identifies their
shift, density, ruler direction, screen, or immersion jets.

## 5. Exact remaining defect

Let an incidence independently rescale the shared clock by

\[
u_{X|e}=a_{X|e}u_X,
\qquad a_{X|e}>0.
\]

Then

\[
\Phi_{X|e}=\varphi_X-\log a_{X|e}.
\]

For a triangle, G171's exact defect becomes

\[
\boxed{
\Omega_{ABC}
=\log\!\left(
\frac{a_{B|BC}}{a_{B|AB}}
\frac{a_{C|AC}}{a_{C|BC}}
\frac{a_{A|AB}}{a_{A|AC}}
\right).
}
\]

Therefore a nonzero completed scalar defect diagnoses unmatched clock calibration at the
incidences. It is not produced merely by changing an incident ruler direction after G176
completion.

## 6. Regrade of the G171 angular witness

G171 used

\[
h_1=\begin{pmatrix}-1&-1/2\\-1/2&3/4\end{pmatrix},
\qquad
h_2=\begin{pmatrix}-1&-1/2\\-1/2&211/100\end{pmatrix}.
\]

Before G176 completion,

\[
e^{4\Phi_{\sigma,1}}=1,
\qquad
e^{4\Phi_{\sigma,2}}=\frac{59}{25}.
\]

But both incidences have the same clock factor \(T=1\). Their G176 densities are

\[
m_1=1,
\qquad
m_2=\frac{\sqrt{59}}5,
\]

and both completed scalars satisfy

\[
\boxed{e^{4\Phi_{s,1}}=e^{4\Phi_{s,2}}=1.}
\]

The angular distinction survives: the densities differ and the completed shifts are
\(1/2\) and \(5/(2\sqrt{59})\). Thus G171 remains a valid uncompleted-pullback and full-tuple
control, but it is not a counterexample to observer-clock scalar descent under the later G176
physical-kernel clarification.

G214's algebraic incidence-defect formula also survives. Its scalar nonclosure branch now applies
to independently calibrated clocks; its full-tuple nonproduct boundary remains unchanged.

## 7. Primary static specialization

In the declared primary static metric, using dimension-matched common time \(x^0=c_Et\),

\[
g(\partial_{x^0},\partial_{x^0})=-e^{-2\phi},
\qquad T=e^{-\phi}.
\]

Therefore every regular completed pair incidence using that same clock tangent has

\[
\boxed{\Phi_s=\phi.}
\]

Arbitrary regular radial/angular participation of the ruler changes \(m\) and the non-scalar pair
channels, not this endpoint scalar. In a general time-live or moving-observer case the same theorem
holds with \(T=\sqrt{-g(u,u)}\); changing the observer clock tangent can change the scalar.

## 8. Carry hierarchy and ceiling

G182 already proves the strict hierarchy

\[
\text{shared completed scalar}
\;<\;
\text{shared completed pair metric}
\;<\;
\text{shared immersion germ jets}.
\]

G215 closes only the first incidence joint on a supplied common-clock network. The G214 theorem for
full tuple overlap descent remains conditional on charts of one supplied pair surface, and distinct
pair metrics still have no native matrix product.

- `WORKING_FOUNDATIONAL_CLARIFICATION`: G176 completed physical pair.
- `DERIVED_CONDITIONAL`: completed scalar depends only on the supplied calibrated clock germ.
- `DERIVED_CONDITIONAL`: all scalar cycles telescope when each observer clock is shared across its
  incidences.
- `RECLASSIFIED_CONTROL`: G171 angular scalar mismatch before completion.
- `RETAINED`: G171 incidence formula for unmatched clocks and G214 full-tuple nonproduct boundary.
- `OPEN`: physical observer/germ population, metric values and profiles, full cross-pair germ carry,
  singular/global strata, history evolution, and all downstream physics.

No `X_max`, fit, transfer, observation, action, source, matter, bootstrap, mass, or signalling claim
follows.
