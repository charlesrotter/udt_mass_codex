# G167 exact derivation — bounded primary-metric general pair pullback

Date: 2026-08-18

## 1. Bounded arena

The declared primary static-spherical UDT metric is

\[
g=-c_E^2e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2
  +r^2d\theta^2+r^2\sin^2\theta\,d\varphi^2.
\]

This is a four-dimensional metric, not only a radial line element. Its static, spherical, diagonal,
and areal properties remain the declared macro slice. The function \(\phi(r)\) is supplied here; no
field equation or profile is derived.

Let a supplied regular ordered-pair realization be a local rank-two immersion

\[
F:\Sigma^2\to M^4,
\qquad
X_i=F_*\partial_i
    =t_i\partial_t+r_i\partial_r
      +\theta_i\partial_\theta+\varphi_i\partial_\varphi.
\]

The two tangent directions need not be radial, static, geodesic, or aligned with the ambient chart.
The pair metric is not another ansatz. It is the pullback \(h=F^*g\).

## 2. Exact general-pair pullback

Direct substitution gives

\[
\boxed{
h_{ij}
=-c_E^2e^{-2\phi}t_it_j
+e^{2\phi}r_ir_j
+r^2\theta_i\theta_j
+r^2\sin^2\theta\,\varphi_i\varphi_j.
}
\]

Equivalently, if \(w_i\) is the angular component of \(X_i\) and \(\gamma_{S^2}\) is the unit-sphere
metric,

\[
h_{ij}
=-c_E^2e^{-2\phi}t_it_j
+e^{2\phi}r_ir_j
+r^2\gamma_{S^2}(w_i,w_j).
\]

This formula is angular-coordinate covariant. Under an angular coordinate change with Jacobian
\(K\), \(Z\mapsto KZ\) and \(q_{S^2}\mapsto K^{-T}q_{S^2}K^{-1}\), so

\[
Z^Tq_{S^2}Z
\mapsto
Z^TK^TK^{-T}q_{S^2}K^{-1}KZ
=Z^Tq_{S^2}Z.
\]

## 3. Exact relation to the conditional complete-coframe evaluator

In the primary coframe,

\[
B=\begin{pmatrix}c_Ee^{-\phi}&0\\0&e^\phi\end{pmatrix},
\qquad
Q=\begin{pmatrix}r&0\\0&r\sin\theta\end{pmatrix},
\qquad
S=0.
\]

For

\[
Y=\begin{pmatrix}t_0&t_1\\r_0&r_1\end{pmatrix},
\qquad
Z=\begin{pmatrix}\theta_0&\theta_1\\\varphi_0&\varphi_1\end{pmatrix},
\]

the uncompressed formula reduces exactly to

\[
\boxed{
h=Y^TB^T\eta_2BY+Z^TQ^TQZ.
}
\]

Thus, in this bounded primary arena:

- \(B\) is fixed by \(c_E\) and the supplied \(\phi\) profile;
- \(Q\) is fixed by the areal spherical metric;
- ambient base-screen mixing \(S\) is exactly zero in this coframe;
- \(Y,Z\) are the supplied pair tangents;
- the angular Gram matrix \(P=Z^TQ^TQZ\) is derived from the metric and pair realization.

The conditional \(B,Q,S,Y,Z\) evaluator therefore does not require five independent histories in
this slice. It collapses to one supplied primary metric plus one supplied pair realization.

## 4. Angular terms and terminal shift are internal

Writing

\[
P=\begin{pmatrix}x&z\\z&y\end{pmatrix},
\]

the complete pair metric is \(h=h_{\rm base}+P\) before the terminal kernel is evaluated. Although
the ambient metric is diagonal, the pair metric generally is not:

\[
h_{01}
=-c_E^2e^{-2\phi}t_0t_1
+e^{2\phi}r_0r_1
+r^2\theta_0\theta_1
+r^2\sin^2\theta\,\varphi_0\varphi_1.
\]

Therefore the calibrated terminal shift state

\[
\beta_{\rm pair}=\frac{h_{01}}{h_{00}}
\]

can be nonzero even when the base contribution to \(h_{01}\) and every ambient off-diagonal metric
component vanish. This is pair-embedding geometry in the supplied calibrated pair chart, not a
separately posited or chart-invariant ambient shift.

## 5. Terminal reciprocal kernel

On the regular calibrated Lorentzian stratum

\[
h_{00}<0,
\qquad
\det h<0,
\]

the unique terminal readout remains

\[
\boxed{
\phi_{\rm pair}
=\frac14\log\frac{-\det h}{h_{00}^2},
\qquad
\left(\frac{c_{\rm eff}^{(\rm pair)}}{c_E}\right)^2
=\frac{h_{00}^2}{-\det h}.
}
\]

All angular terms have already entered \(h\). No post-readout angular correction occurs.

An exact nonradial witness with \(c_E=1\), \(e^\phi=2\), \(r=3\), and
\(\sin\theta=4/5\) gives

\[
h=
\begin{pmatrix}
-391/100&9/50\\
9/50&2
\end{pmatrix},
\qquad
P=
\begin{pmatrix}
9/100&9/50\\
9/50&1
\end{pmatrix}.
\]

Here

\[
\det h=-\frac{19631}{2500},
\qquad
\beta_{\rm pair}=-\frac{18}{391},
\qquad
\left(\frac{c_{\rm eff}^{(\rm pair)}}{c_E}\right)^2
=\frac{152881}{78524}.
\]

The base-only value is \(4\), so the metric-derived angular Gram changes the terminal reciprocal
readout exactly.

## 6. The radial and central boundary

For the calibrated radial pair

\[
J=(\partial_t,\partial_r),
\qquad
Z=0,
\]

the pullback is the founded block

\[
h=\operatorname{diag}(-e^{-2\phi},e^{2\phi})
\]

after setting \(c_E=1\) in dimension-matched coordinates. Hence

\[
\phi_{\rm pair}=\phi,
\qquad
\frac{c_{\rm eff}^{(\rm pair)}}{c_E}=e^{-2\phi}.
\]

For this exact radial pair the scalar angular Gram is zero. The primary angular sector still owns
the separate finite-radius screen/Jacobi response of G119, but it does not automatically modulate
the scalar depth of every radial pair. Angular modulation of the scalar requires angular components
in the pair realization or a genuine ambient nonspherical/mixed extension.

This boundary prevents the result from being promoted into a universal loud-orchestra claim.

## 7. Query-live derivative versus ambient dynamics

Along any supplied parameter \(\lambda\),

\[
\boxed{
\dot h
=\dot J^TgJ+J^Tg\dot J+J^T\dot gJ.
}
\]

For the primary metric,

\[
\dot g=\operatorname{diag}\!\left(
2c_E^2e^{-2\phi}\dot\phi,
2e^{2\phi}\dot\phi,
2r\dot r,
2r\dot r\sin^2\theta
+2r^2\sin\theta\cos\theta\dot\theta
\right).
\]

When \(\phi=\phi(r)\), \(\dot\phi=\phi'(r)\dot r\) along the supplied realization. The terminal
variation is

\[
\dot\phi_{\rm pair}
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}}.
\]

Production algebra proves this equals the full directional derivative with every metric and pair
tangent term retained. On the exact generic witness, profile, areal-radius, angular-chart,
clock-tangent, radial-tangent, theta-tangent, and varphi-tangent variations are all nonzero.

This is a complete query-live kinematic identity in the declared static ambient metric. It is not
an ambient time-evolution equation and does not derive a time-dependent UDT metric.

## 8. No independent scalar `mu`

The primary metric supplies the full angular Gram matrix \(P\), not a scalar mixing coefficient.
Even \(\operatorname{tr}P\) is insufficient: for the same base metric,

\[
P_1=\operatorname{diag}(1,0),
\qquad
P_2=\operatorname{diag}(0,1)
\]

have equal trace but produce different terminal reciprocal ratios. Thus no scalar `mu` may replace
the full metric-derived Gram data without an additional, presently unowned reduction rule.

## 9. What is closed and what remains open

`DERIVED_CONDITIONAL` in the bounded primary arena:

- the exact pullback for every local rank-two pair tangent;
- the internal angular Gram contribution;
- pair-induced terminal shift from a diagonal ambient metric;
- the complete query-live first derivative;
- reduction to the founded radial kernel;
- the metric-fixed identification \(B,Q,S=0\) and query-supplied identification \(Y,Z\).

Still `OPEN` or outside this bounded slice:

- which event/calibration pair realization is physical when bare observer names are supplied;
- cross-query carry and global observer networks;
- a genuine nonspherical, ambient-mixed, or ambient-time-dependent UDT metric;
- singular/null/rank-changing strata and global completion;
- dynamics, source, action, matter, bootstrap, observations, signalling, and \(X_{\max}\).

The result removes independent orchestra histories from the declared primary spherical pair
calculation. It does not prove that the primary static-spherical slice is the complete UDT theory.
Connection, Jacobi, normal-transport, and holonomy channels also remain separately typed; the local
terminal pair metric does not reconstruct them by itself.
