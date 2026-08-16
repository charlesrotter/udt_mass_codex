# G124 exact derivation — finite-radius live observer-transition junction

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__EXACT_FINITE_RADIUS_JUNCTION_DERIVED_CONDITIONALLY`

## 1. Result first

For one supplied normalized radial null point-observer query, use areal radius `R` as the calibrated
ruler coordinate on a regular branch where `K(R)=dR/dlambda` is nonzero. Then the terminal pair
common scale, reciprocal depth, source frequency depth, and spherical screen obey the exact
finite-radius junction

\[
\boxed{
\zeta=\phi_{\rm pair}-\kappa_{\rm pair}+\chi_s
}
\tag{1}
\]

with

\[
\chi_s=\log\frac{-g(K,U_s)}{-g(K,U_T)}.
\tag{2}
\]

Here `U_T` is the normalized observer-time variation of the same complete exponential query, and
`U_s` is a supplied endpoint/source clock. No mixture coefficient or external angular correction
appears.

The common-scale magnitude is not an unrelated nuisance:

\[
\boxed{
\kappa_{\rm pair}
=-\frac12\log|K(R)|
=-\frac12\log\left|\frac{R\,\theta_{\rm sky}}2\right|
}
\tag{3}
\]

on the regular `R>0` screen stratum, where G119 gives
`D_sky=R O` and `theta_sky=2K(R)/R`. Thus the local G116 “optical correction” is exactly the
finite-radius pair common-scale-magnitude term. It is not a new instrument bolted onto reciprocal
depth. The orientation sign remains in `K(R)`, the chosen regular branch, and `beta_pair`; it is not
contained in `kappa_pair`.

## 2. Raw metric/query proof

In affine query coordinates write

\[
F(\tau,\lambda,n)=\operatorname{Exp}_{z(\tau)}[\lambda k(\tau,n)],
\qquad
\bar T=F_*\partial_\tau|_\lambda,
\qquad
K=F_*\partial_\lambda.
\]

The ray is affinely geodesic, `g(K,K)=0`, and its observer normalization is
`g(K,u_o)=-1`. Since the variation coordinates commute and the connection is torsion free,

\[
\begin{aligned}
K\,g(\bar T,K)
&=g(\nabla_K\bar T,K)+g(\bar T,\nabla_KK)\\
&=g(\nabla_{\bar T}K,K)\\
&=\frac12\bar T\,g(K,K)=0.
\end{aligned}
\tag{4}
\]

Therefore `g(bar T,K)=-1` along the whole branch.

Where `R` is a valid ruler coordinate, let

\[
s=\frac{\partial\lambda}{\partial R}\bigg|_\tau=\frac1{K(R)}.
\tag{5}
\]

Changing from `(tau,lambda)` to `(tau,R)` changes the fixed-ruler time variation by a null
multiple,

\[
T=\bar T+\lambda_{,\tau}|_R K,
\]

so `g(T,K)=-1` remains exact. Define

\[
A=\sqrt{-g(T,T)}>0.
\]

The raw longitudinal pullback is then

\[
\boxed{
h_\parallel=
\begin{pmatrix}
-A^2&-s\\
-s&0
\end{pmatrix},
\qquad
\det h_\parallel=-s^2.
}
\tag{6}
\]

All complete-coframe, angular, and mixing contributions have already entered `T`, `K`, and their
Gram block before (6) is read. Equation (6) is a reduction of the completed query, not a frozen
replacement for it.

## 3. Exact terminal decomposition

The calibrated triangular decomposition gives

\[
T_{\rm pair}=A,
\qquad
L_{\rm pair}=\frac{|s|}{A},
\]

and therefore

\[
\boxed{
\kappa_{\rm pair}=\frac12\log|s|,
\qquad
\phi_{\rm pair}=\frac12\log|s|-\log A.
}
\tag{7}
\]

The null-ruler shift is no longer independent on this query class:

\[
\boxed{
\beta_{\rm pair}
=\frac{s}{A^2}
=\operatorname{sgn}(s)e^{2\phi_{\rm pair}}.
}
\tag{8}
\]

The terminal reciprocal calibration remains

\[
\frac{c_{\rm eff}^{(\rm pair)}}{c_E}
=\frac{A^2}{|s|}
=e^{-2\phi_{\rm pair}}.
\tag{9}
\]

Equation (8) is specific to the normalized null observer-ruler chart with `h_11=0`; it is not a
universal identity for arbitrary timelike pair immersions.

## 4. Exact source-frequency factorization

Normalize the query-time variation,

\[
U_T=\frac{T}{A}.
\]

Equation (4) gives its exact measured ray frequency

\[
\omega_T=-g(K,U_T)=\frac1A.
\tag{10}
\]

The original observer normalization makes `omega_o=1`. For a supplied endpoint clock `U_s`, let

\[
\omega_s=-g(K,U_s)>0,
\qquad
\zeta=\log\frac{\omega_s}{\omega_o},
\qquad
\chi_s=\log\frac{\omega_s}{\omega_T}.
\]

Then

\[
\zeta=-\log A+\chi_s.
\]

Using (7) proves (1). This is an exact factorization of one supplied query. `chi_s` is not a fitted
coefficient: it is the endpoint clock comparison that the query must supply before a source
frequency exists.

For a radial source clock

\[
U_s=\cosh\rho\,U_T+\sinh\rho\,E_T,
\qquad
K=\omega_T(U_T+E_T),
\]

one gets

\[
\frac{\omega_s}{\omega_T}=e^{-\rho}
=\sqrt{\frac{1-v}{1+v}},
\qquad
\chi_s=-\rho=-\operatorname{atanh}v.
\tag{11}
\]

Transverse source motion remains lawful and is retained through the invariant ratio in (2); it is
not forced into the radial formula (11).

### Fixed-label versus orthogonal-quotient clock

The identity must use one matched terminal clock definition throughout. For an active fixed-label
sky query, `T` includes its angular component, so both `phi_pair` and `U_T` include that component.
If the angular screen is orthogonally quotiented, define

\[
T_\perp=T-\operatorname{proj}_{\mathcal S}T,
\qquad
U_{T,\perp}=\frac{T_\perp}{\sqrt{-g(T_\perp,T_\perp)}}.
\]

Because the screen is orthogonal to `K`, `g(T_perp,K)=-1`, and the same proof gives

\[
\zeta=\phi_{\rm pair}^{\perp}-\kappa_{\rm pair}+\chi_s^{\perp}.
\tag{11a}
\]

At G115 two-jet order,

\[
\phi_{\rm pair}^{\rm fixed}
=\phi_{\rm pair}^{\perp}+\frac12|w|^2R^2,
\qquad
\chi_s^{\rm fixed}
=\chi_s^{\perp}-\frac12|w|^2R^2,
\]

so active sky drift cancels from the scalar frequency factorization only after it has entered both
matched channels. Replacing the fixed-label `phi` by the quotient `phi` while retaining the old
`chi_s`, or vice versa, would be an invalid shortcut. Passive screen relabeling remains gauge.

## 5. Exact screen ownership of common-scale magnitude

By (5) and (7),

\[
\kappa_{\rm pair}=-\frac12\log|K(R)|.
\tag{12}
\]

G119 derives on every regular central-spherical branch

\[
\mathcal D_{\rm sky}=R O,
\qquad
\mathfrak B=\frac{K(R)}R I_2.
\]

Taking the trace gives (3). Consequently the pair common-scale magnitude is the logarithmic
conversion between affine ray separation and areal screen size. In the user’s orchestra language,
it is the volume/rate channel already played by the same metric history. The signed direction of
that conversion is separately retained by `K(R)`, the branch orientation, and `beta_pair`.

This result removes one piece of scaffolding: the finite-radius optical contribution no longer
needs a separate correction slot. It does not remove the history dependence of `K(R)`.

## 6. Strata and chart failures

| Stratum | `K(R)` | Result |
| --- | ---: | --- |
| regular oriented areal chart | nonzero | equations (1)--(12) hold with `abs` and orientation sign |
| areal turning point | zero at `R>0` | `R` is not a ruler chart; the shared `log|s|/2` divergence cancels from `phi-kappa`, but `A` and `chi_s` may also be chart-singular |
| initial observer vertex | `R=0` at the normalized initial point | `D_sky=0` but the vertex normalization and initial Jacobi data are supplied; this is the query origin, not a later caustic |
| later spherical position caustic | `R=0` after propagation | the angular/areal chart degenerates and `D_sky=0`; retain signed/affine branch data and the surviving full Jacobi phase |
| multiple exponential preimages | branchwise | evaluate (1) on every regular branch; no occupancy or aggregation weight is supplied |
| `T` becomes null/non-timelike | `A` vanishes or is undefined | normalized query-time clock and this terminal chart fail; no continuation is asserted |

At an areal turning point the `log|s|/2` pieces in `phi_pair` and `kappa_pair` are coordinate
infinities and cancel algebraically. The fixed-`R` time variation itself can also become singular,
so G124 does not assert that `phi-kappa` or the physical frequency must always remain finite.
Returning to affine ruler coordinate removes the areal-coordinate singularity; frequency is finite
only when the affine query and the supplied clocks remain regular.

## 7. G116 is the two-jet reduction

G115/G116 give

\[
\phi_{\rm pair}=p_2R^2+O(R^3),
\]

and

\[
K(R)=1-\frac{\mathcal A_{\rm opt}}2R^2+O(R^3).
\]

Equation (12) therefore gives

\[
\kappa_{\rm pair}=\frac{\mathcal A_{\rm opt}}4R^2+O(R^3).
\]

The same endpoint-clock calculation gives

\[
\chi_s=v_{\rm rel}R+\dot v_{\rm rel}R^2+O(R^3).
\]

Substitution into (1) yields exactly

\[
\zeta
=\phi_{\rm pair}
+v_{\rm rel}R
+\left(\dot v_{\rm rel}-\frac{\mathcal A_{\rm opt}}4\right)R^2
+O(R^3),
\]

which is G116. The local optical coefficient has acquired its exact finite-radius owner:
`-kappa_pair`.

On the pure stationary reciprocal branch, areal radius is affine (`kappa_pair=0`) and the supplied
endpoint clock agrees with `U_T` (`chi_s=0`). Only on that reduction does

\[
\zeta=\phi_{\rm pair}
\]

follow exactly.

## 8. Relation to the G123 direct chart

For a supplied common-event query, G123 gives

\[
D_{BA}=(dF_B)^{-1}dF_A
\]

on every regular overlap, with exact composition, reversal, and full-pullback covariance. G124
does not replace this map with a scalar. It evaluates (1) separately on each calibrated source leg.
Only when a common source-clock/frequency calibration is supplied may two leg identities be
subtracted:

\[
\zeta_B-\zeta_A
=(\phi_B-\phi_A)-(\kappa_B-\kappa_A)+(\chi_B-\chi_A).
\tag{13}
\]

Equation (13) is not derived from bare endpoints or co-presence alone.

The direct transition still acts on query tangents, not full Jacobi phase. G114 source-phase
matching and its intersection ranks remain a separate boundary-compatibility channel. No
information is discarded to force a scalar closure.

## 9. Loop audit

This is not another history-selector census and it passes the preregistered loop stop:

- G116 is upgraded from a local `O(R^2)` relation to an exact finite-radius identity;
- `kappa_pair` is identified as the owner of the former optical correction;
- `beta_pair` loses independent status on the normalized null-ruler subclass;
- active fixed-label sky drift is retained upstream and cancels only between matched terminal and
  endpoint-clock readouts;
- the areal-turning divergence is retyped as a chart failure: its shared logarithmic term cancels,
  while the turning point alone establishes neither frequency finiteness nor divergence.

What remains open is smaller and explicit: the metric history determines `A`, `K(R)`, and the
endpoint clock relation; the founding postulates still do not select that history or source query.

## 10. Bounded landing

```text
EXACT_FINITE_RADIUS_KAPPA_PHI_SOURCE_CLOCK_JUNCTION_DERIVED_CONDITIONALLY
__ZETA_EQUALS_PHI_PAIR_MINUS_KAPPA_PAIR_PLUS_CHI_SOURCE
__KAPPA_PAIR_IS_THE_AFFINE_TO_AREAL_SCREEN_EXPANSION_MAGNITUDE
__NULL_PAIR_BETA_EQUALS_ORIENTATION_TIMES_EXP_TWO_PHI
__G116_TWO_JET_ACTIVE_SKY_CANCELLATION_AND_G119_SCREEN_THEOREM_RECOVERED
__AREAL_TURNING_IS_A_CHART_FAILURE_AND_ALONE_ESTABLISHES_NEITHER_FREQUENCY_FINITENESS_NOR_DIVERGENCE
__DIRECT_QUERY_TANGENT_AND_JACOBI_PHASE_REMAIN_DISTINCT
__HISTORY_QUERY_SOURCE_TRANSFER_XMAX_AND_SELECTION_OPEN
```

No physical history, source/query owner, transfer law, observation, `X_max`, bootstrap, action,
matter, mass, or signalling conclusion follows.
