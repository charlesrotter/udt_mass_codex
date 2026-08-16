# G116 exact derivation — calibrated frequency / terminal-pair junction

Date: 2026-08-16

## 1. Result first

On the exact G115 regular central spherical time-live metric/query two-jet, define

\[
\zeta=\log\frac{\omega_s}{\omega_o},\qquad
v_{\rm rel}=b-q,\qquad
\dot v_{\rm rel}=\dot b-\dot q,
\]

and the optical coefficient

\[
\mathcal A=2\ell+2n+\dot b.
\]

The orthogonal-quotient terminal depth is

\[
\phi_{\rm pair}=p_2R^2+O(R^3),\qquad
p_2=\frac12\left(\ell-n+b^2-\frac{\dot b}{2}\right).
\]

Direct substitution of the independently derived G115 channels gives the coefficient-free identity

\[
\boxed{
\zeta
=\phi_{\rm pair}
+v_{\rm rel}R
+\left(\dot v_{\rm rel}-\frac{\mathcal A}{4}\right)R^2
+O(R^3)
}.
\]

Since the terminal reciprocal-`c_E` evaluator gives

\[
\frac{c_{\rm eff}^{\rm(pair)}}{c_E}=e^{-2\phi_{\rm pair}},
\]

the same result is

\[
\boxed{
\zeta
=-\frac12\log\frac{c_{\rm eff}^{\rm(pair)}}{c_E}
+v_{\rm rel}R
+\left(\dot v_{\rm rel}-\frac{\mathcal A}{4}\right)R^2
+O(R^3)
}.
\]

For an active fixed-label sky query,

\[
\phi_{\rm pair}^{\rm fixed}
=\phi_{\rm pair}^{\rm quotient}+\frac12|w|^2R^2+O(R^3),
\]

so the same frequency contraction is recovered by subtracting `|w|^2/2` inside the quadratic
junction. A passive time-dependent sky relabeling remains gauge.

This is a relation among channels produced by one complete metric/query construction. It is not a
post-processing correction and contains no fitted coefficient.

## 2. Load-bearing raw coefficients

G115 independently derived

\[
\phi_{\rm pair}^{\rm quotient}
=\frac12\left(\ell-n+b^2-\frac{\dot b}{2}\right)R^2+O(R^3)
\]

and

\[
\zeta
=(b-q)R
+\left(\frac{b^2}{2}-n+\frac{\dot b}{2}-\dot q\right)R^2
+O(R^3).
\]

The affine null and sky-Jacobi calculation separately gave

\[
K^R=1-\frac{\mathcal A}{2}R^2+O(R^3),
\qquad
R(\lambda)=\lambda-\frac{\mathcal A}{6}\lambda^3+O(\lambda^4).
\]

No coefficient was introduced to join these formulas. The identity follows because

\[
\frac{b^2}{2}-n+\frac{\dot b}{2}-\dot q
=p_2-\frac{\mathcal A}{4}+\dot v_{\rm rel}.
\]

Thus the optical term in the junction is the same invariant already controlling affine and angular
propagation. It is not a new phenomenological “angular correction.”

The linear term has an equally direct geometric meaning. With Eulerian unit vectors `u,e_R`,

\[
\partial_T=N u+L\beta e_R.
\]

The fixed-`R` line therefore has radial velocity `L beta/N=bR+O(R^3)` relative to `u`, while the
supplied source has velocity `qR+O(R^3)`. Their leading relative drift is exactly
`v_rel R=(b-q)R`. This interpretation is residual-slicing invariant even though `b` and `q`
separately are not.

## 3. Residual-gauge audit

Under the residual areal-time slicing

\[
T'=T+a(T)R^2+O(R^4),
\]

the individual coefficients transform as recorded in G115. Direct symbolic substitution gives

\[
p_2'=p_2,qquad
\mathcal A'=\mathcal A,qquad
v_{\rm rel}'=v_{\rm rel},qquad
\dot v_{\rm rel}'=\dot v_{\rm rel}.
\]

Consequently every term in the junction is invariant. Calling `b`, `q`, or either derivative alone
physical would be a regression.

## 4. Exact pure reciprocal reduction

The regular central stationary reciprocal control has, through this order,

\[
N=e^{-pR^2},\qquad L=e^{+pR^2},\qquad
n=-p,\quad\ell=p,\quad b=q=0.
\]

Therefore

\[
v_{\rm rel}=0,qquad \dot v_{\rm rel}=0,qquad \mathcal A=0,
\]

and

\[
\zeta=\phi_{\rm pair}=pR^2+O(R^3),
\qquad
\frac{c_{\rm eff}^{\rm(pair)}}{c_E}=e^{-2\zeta}.
\]

This proves that the historical conditional identification `1+z=e^{phi_pair}` is the exact pure
stationary reciprocal reduction. It is not a universal identity on a generic live source query.

## 5. What composes exactly

For one supplied null covector calibration and three endpoint clocks, let

\[
\omega_i=-g(k,U_i)>0,
\qquad Z_{ij}=\frac{\omega_i}{\omega_j}.
\]

Then

\[
Z_{ij}Z_{jk}=Z_{ik},\qquad Z_{ji}=Z_{ij}^{-1},
\]

and the additive frequency depth `zeta_ij=log Z_ij` composes and reverses exactly. Scaling `k`
cancels.

Terminal pair ratios compose separately only after their clock/ruler states are placed in one
matched calibration system. If `C_i=T_i/L_i`, then

\[
C_{ij}=\frac{C_j}{C_i}
\]

telescopes. Independently rebuilt pair tapes need not supply this common state. The exact frequency
cocycle does not repair an unowned terminal middle reset.

## 6. The uniqueness result is typed, not universal

Once a query supplies source clock `U_s`, observer clock `U_o`, ray covector `k`, and declares the
direct frequency-ratio measurement type, the positive
ratio

\[
Z=\frac{-g(k,U_s)}{-g(k,U_o)}
\]

is its canonical normalized clock-frequency comparison. Its logarithm is `zeta`. This is a
query-derived metric readout; it is not a uniqueness theorem over arbitrary functions of the same
endpoint data.

Once a regular calibrated pair metric `h` is supplied, `phi_pair` is separately the unique
common-scale-free clock/ruler imbalance in its triangular terminal decomposition. This is a
pair-tape readout.

The founding character alone does not declare these two types identical. On the full abstract
two-channel additive group `(zeta,phi) in (R^2,+)`—or on a realized channel image that spans that
group—every continuous additive scalar normalized on the pure branch is

\[
\delta_\alpha
=\alpha\zeta+(1-\alpha)\phi_{\rm pair},
\qquad \alpha\in\mathbb R.
\]

Neutrality, reversal, composition, and the pure reduction `zeta=phi_pair` leave `alpha` free. This
is the complete continuous character family because a continuous homomorphism
`(R^2,+)->(R,+)` is linear. In particular:

- `alpha=1` is the frequency query;
- `alpha=0` is the terminal pair query;
- naively adding both gives `2 phi` on the pure branch and double counts the founded normalization.

Thus the algebraic junction is unique for the declared G115 metric/query jet, but the founding
group laws do not manufacture a universal scalar measurement protocol. The query type selects the
readout. No empirical mixing coefficient is justified.

## 7. Frozen low-distance frequency series

If a later observational query explicitly identifies its measured ratio with `Z=e^zeta`, then

\[
Z-1
=v_{\rm rel}R
+\left(
p_2-\frac{\mathcal A}{4}+\dot v_{\rm rel}
+\frac12v_{\rm rel}^2
\right)R^2
+O(R^3).
\]

This gives three distinct regular strata:

1. `v_rel!=0`: a linear leading clock-frequency relation;
2. `v_rel=0` with nonzero quadratic coefficient: a quadratic leading relation;
3. both coefficients zero: higher jets control any later first nonzero term, if one exists; exact
   cancellation remains possible.

The series is frozen algebraically. The metric history and source query still own the invariant
coefficients; G116 does not fit or choose them.

## 8. Maximum conclusion

```text
COEFFICIENT_FREE_METRIC_QUERY_JUNCTION_DERIVED_CONDITIONALLY
__TERMINAL_RECIPROCAL_DEPTH_RELATIVE_SOURCE_TAPE_DRIFT_AND_OPTICAL_FOCUSING_ARE_ONE_CONNECTED_LOCAL_IDENTITY
__PURE_STATIONARY_RECIPROCAL_BRANCH_RECOVERS_ZETA_EQUALS_PHI_AND_CEFF_OVER_CE_EQUALS_EXP_MINUS_2_ZETA
__FREQUENCY_QUERY_AND_TERMINAL_PAIR_QUERY_EACH_HAVE_UNIQUE_TYPED_READOUTS
__FOUNDING_COMPOSITION_REVERSAL_AND_PURE_NORMALIZATION_DO_NOT_SELECT_A_UNIVERSAL_COMBINED_SCALAR
__PHYSICAL_HISTORY_OBSERVED_REDSHIFT_PROTOCOL_GLOBAL_DESCENT_TRANSFER_AND_OBSERVATIONS_REMAIN_OPEN
```

No SNe, BAO, CMB, `X_max`, action, bootstrap, source dynamics, matter, mass, or signalling conclusion
follows.
