# G159 exact derivation — the complete score descends through one calibrated pair first jet

Date: 2026-08-18

## 1. Supplied regular pair family

Let

\[
V=EJ,
\qquad
h=V^T\eta V,
\]

on one supplied smooth rank-two pair family with $h_{00}<0$ and $\det h<0$. G158 gives, in its
registered gauge,

\[
\Omega_R=\dot E E^{-1},
\qquad
P:=\dot V=\Omega_RV+E\dot J.
\]

No query sector is frozen. Direct differentiation gives the single supplied calibrated pair first jet

\[
\boxed{
\dot h=P^T\eta V+V^T\eta P
=2\operatorname{sym}(V^T\eta P).
}
\]

Every live base, screen, mixing, and query channel is retained upstream in $P$ and can reach the
terminal response through $(h,\dot h)$. This is an exact kinematic descent of supplied data, not a
history equation.

## 2. Exact terminal rates

In the supplied calibrated clock/ruler coordinates,

\[
\kappa_{\rm pair}=\frac14\log(-\det h),
\]

\[
\phi_{\rm pair}=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right),
\qquad
\beta_{\rm pair}=\frac{h_{01}}{h_{00}}.
\]

Therefore

\[
\boxed{
\dot\kappa_{\rm pair}
=\frac14\operatorname{tr}(h^{-1}\dot h),
}
\]

\[
\boxed{
\dot\phi_{\rm pair}
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}},
}
\]

and

\[
\boxed{
\dot\beta_{\rm pair}
=\frac{\dot h_{01}h_{00}-h_{01}\dot h_{00}}{h_{00}^2}.
}
\]

On the already conditional endpoint calibration

\[
\frac{c_{\rm eff}^{({\rm pair})}}{c_E}=e^{-2\phi_{\rm pair}},
\]

the exact logarithmic rate is

\[
\boxed{
\partial_\lambda\log\!\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right)
=-2\dot\phi_{\rm pair}.
}
\]

This joins G158 to formulas already present in the uncompressed kernel. It does not supply a native
light law or make pair `c_eff` a local signal speed.

## 3. Live Lorentz coframe gauge cancels from the pair first jet

Let $E'=\Lambda(\lambda)E$ with

\[
\Lambda^T\eta\Lambda=\eta.
\]

Then

\[
V'=\Lambda V,
\qquad
P'=\dot\Lambda V+\Lambda P,
\]

while the right score has the inhomogeneous law

\[
\Omega_R'
=\dot\Lambda\Lambda^{-1}+\Lambda\Omega_R\Lambda^{-1}.
\]

The score entries are therefore presentation data. Nevertheless,

\[
h'=V'^T\eta V'=h,
\]

and differentiation of $\Lambda^T\eta\Lambda=\eta$ gives

\[
\dot\Lambda^T\eta\Lambda+\Lambda^T\eta\dot\Lambda=0.
\]

Consequently

\[
\boxed{\dot h'=\dot h.}
\]

Thus $(h,\dot h)$ and all terminal rates computed from a fixed calibrated pair chart are invariant
under live Lorentz coframe gauge even though the ten registered score components are not.

## 4. Pair-chart covariance is not terminal-coefficient invariance

Let the pair basis change by a live $A(\lambda)\in GL^+(2)$:

\[
J'=JA,
\qquad
V'=VA,
\qquad
P'=PA+V\dot A.
\]

Then

\[
\boxed{h'=A^ThA,}
\]

\[
\boxed{
\dot h'
=\dot A^ThA+A^T\dot hA+A^Th\dot A.
}
\]

The tensor and its first jet transform lawfully, but their calibrated coefficients need not stay
numerically fixed. In particular,

\[
\kappa_{\rm pair}'
=\kappa_{\rm pair}+\frac12\log\det A,
\]

\[
\boxed{
\dot\kappa_{\rm pair}'
=\dot\kappa_{\rm pair}
+\frac12\operatorname{tr}(A^{-1}\dot A).
}
\]

Let $a_0,a_1$ be the columns of $A$ and assume the new clock column remains timelike,
$a_0^Tha_0<0$. Then

\[
\phi_{\rm pair}'
=\phi_{\rm pair}
+\frac12\log\det A
-\frac12\log\!\left(\frac{-a_0^Tha_0}{-h_{00}}\right),
\]

so

\[
\boxed{
\dot\phi_{\rm pair}'-\dot\phi_{\rm pair}
=\frac12\operatorname{tr}(A^{-1}\dot A)
-\frac12\partial_\lambda
 \log\!\left(\frac{-a_0^Tha_0}{-h_{00}}\right).
}
\]

Also

\[
\beta_{\rm pair}'=\frac{a_0^Tha_1}{a_0^Tha_0}.
\]

Writing

\[
N=a_0^Tha_1,
\qquad
D=a_0^Tha_0<0,
\]

gives the full arbitrary-live law

\[
\dot N
=\dot a_0^Tha_1+a_0^T\dot h a_1+a_0^Th\dot a_1,
\]

\[
\dot D
=\dot a_0^Tha_0+a_0^T\dot h a_0+a_0^Th\dot a_0,
\]

\[
\boxed{
\dot\beta_{\rm pair}'=\frac{\dot N D-N\dot D}{D^2}.
}
\]

These are calibration laws, not extra metric effects.

## 5. Transparent diagonal calibration control

For a positive live clock/ruler recalibration

\[
A=\operatorname{diag}(a,b),
\]

the exact laws reduce to

\[
\kappa'=\kappa+\frac12\log(ab),
\qquad
\phi'=\phi+\frac12\log\!\left(\frac ba\right),
\qquad
\beta'=\frac ba\,\beta,
\]

and

\[
\boxed{
\dot\kappa'
=\dot\kappa+\frac12\left(\frac{\dot a}{a}+\frac{\dot b}{b}\right),
}
\]

\[
\boxed{
\dot\phi'
=\dot\phi+\frac12\left(\frac{\dot b}{b}-\frac{\dot a}{a}\right),
}
\]

\[
\boxed{
\dot\beta'
=\frac ba\left[
\dot\beta+\beta\left(\frac{\dot b}{b}-\frac{\dot a}{a}\right)
\right].
}
\]

The conditional pair calibration transforms correspondingly as

\[
\boxed{
\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right)'
=\frac ab\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right),
}
\]

\[
\boxed{
\partial_\lambda\log\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right)'
=\partial_\lambda\log\left(\frac{c_{\rm eff}^{({\rm pair})}}{c_E}\right)
+\frac{\dot a}{a}-\frac{\dot b}{b}.
}
\]

Therefore an unrecorded live calibration can imitate terminal scale, reciprocal, and shift rates.
Physical comparisons require one fixed calibrated query or lawful calibration carry; G159 does not
derive that carry.

## 6. Query motion cannot be discarded

With fixed $E=I$, take at one point

\[
V=\begin{pmatrix}1&0\\0&1\\0&0\\0&0\end{pmatrix},
\qquad
E\dot J=P=
\begin{pmatrix}0&1\\0&1\\0&0\\0&0\end{pmatrix}.
\]

Then

\[
h=\begin{pmatrix}-1&0\\0&1\end{pmatrix},
\qquad
\dot h=\begin{pmatrix}0&-1\\-1&2\end{pmatrix},
\]

and

\[
\boxed{
(\dot\kappa,\dot\phi,\dot\beta)
=\left(\frac12,\frac12,1\right).
}
\]

Freezing $\dot J$ would erase this valid supplied response. The observer query is part of what the
complete metric evaluates, not a post-processing correction.

## 7. Landing

`CALIBRATED_PAIR_FIRST_JET_DERIVED__COMPLETE_SCORE_DESCENDS_WITH_DOTJ_LIVE__H_AND_DOTH_LIVE_LORENTZ_COFRAME_GAUGE_INVARIANT__KAPPA_DENSITY_COEFFICIENT_AND_PHI_BETA_CEFF_REQUIRE_PAIR_CALIBRATION_CARRY__PHYSICAL_HISTORY_QUERY_LAMBDA_AND_GLOBAL_COMPLETION_OPEN`

Premise-stamped meaning:

- `DERIVED_CONDITIONAL`: exact descent from the supplied complete score and live query to
  $(h,\dot h)$ and all calibrated terminal rates;
- `DERIVED`: live Lorentz coframe-gauge cancellation from $(h,\dot h)$;
- `DERIVED_CONDITIONAL`: arbitrary live pair-chart coefficient laws on the recharted timelike-clock
  domain $a_0^Tha_0<0$, plus the diagonal recalibration control;
- `OPEN`: physical history, query population, meaning of $\lambda$, calibration carry, full global
  relation family, and singular/global completion;
- not derived: a regime score, loud--quiet--loud prediction, $X_{\max}$ value, action, source,
  bootstrap, matter, mass, light propagation, or signalling.
