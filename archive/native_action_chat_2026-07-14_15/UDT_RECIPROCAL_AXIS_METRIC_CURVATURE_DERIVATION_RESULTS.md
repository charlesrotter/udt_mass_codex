# UDT reciprocal-axis metric curvature — derivation results

## Hygiene header

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Repository | `grok` at `64af120`; pre-existing dirty work preserved |
| Mode | Exact analytic manufactured-field curvature audit; DATA-BLIND |
| Frozen map | `UDT_RECIPROCAL_AXIS_METRIC_CURVATURE_MAP.md`, SHA-256 `3d7c13a47edf1998ba1f94905985efe79989283f6b40a3bf40c19fc946a5a0ab` |
| Exact verifier | `verify_udt_reciprocal_axis_metric_curvature.py` — 26/26 checks pass |
| Metric status | Reciprocal single-axis completion is CONDITIONAL |
| Action status | Metric-only conformal `C^2` branch is CONDITIONAL |
| GPU | Not used or needed |
| Independent verification | OPEN |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 0. Decisive result

The conditional reciprocal-axis metric does **not** reduce the metric-only conformal invariant to
the historical area-only carrier.

Take

\[
g_{00}=-q^{-1},
\qquad
g_{ij}=\delta_{ij}+(q-1)n_i n_j,
\qquad
q=e^{2\phi}>0,
\]

with constant depth and the rank-one axis texture

\[
n(z)=(\cos kz,\sin kz,0).
\]

Because every derivative of `n` is proportional to `dz`, its target-area two-form vanishes
identically:

\[
F_{ij}=n\cdot(\partial_i n\times\partial_j n)=0.
\]

Nevertheless, exact full four-dimensional curvature gives

\[
\boxed{
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
=\frac{4(q-1)^2(q^2+q+1)}{3q^2}\,k^4.
}
\]

Hence, for `q>0`, `q!=1`, and `k!=0`,

\[
\boxed{F^2=0\quad\text{but}\quad C^2>0.}
\]

The pre-registered outcome is therefore **RANK-ONE WEYL COST**.

This is a genuine conformal-geometric effect in the conditional branch: nonzero Weyl curvature
cannot be removed by a coordinate change or by the common local scale calibration.

## 1. Exact construction and provenance

Coordinates are `(t,x,y,z)`. At `z=0`,

\[
g_{\mu\nu}=\operatorname{diag}(-q^{-1},q,1,1),
\qquad
g^{\mu\nu}=\operatorname{diag}(-q,q^{-1},1,1),
\]

and the only nonzero first derivatives are

\[
\partial_zg_{xy}=\partial_zg_{yx}=(q-1)k.
\]

The only nonzero second derivatives are

\[
\partial_z^2g_{xx}=-2(q-1)k^2,
\qquad
\partial_z^2g_{yy}=+2(q-1)k^2.
\]

The verifier constructs `partial g^{-1}`, the Christoffels, `partial Gamma`, the full Riemann and
Ricci tensors, the scalar curvature, and the four-dimensional Weyl tensor using exact rational
arithmetic. It does not use finite differences or linearization.

The result holds at every `z`: shifting `z` rotates the `(x,y)` basis rigidly, so scalar invariants
are unchanged.

The determinant is exactly constant,

\[
\det g=-1,
\]

as required by reciprocal time/axis dilation in this dimensionless convention.

## 2. Exact invariant census

With the curvature sign convention stated in the verifier,

\[
\boxed{R=-\frac{(q-1)^2}{2q}k^2,}
\]

\[
\boxed{
R_{\mu\nu}R^{\mu\nu}
=\frac{(q-1)^2(3q^2+2q+3)}{4q^2}k^4,
}
\]

\[
\boxed{
R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
=\frac{(q-1)^2(11q^2+10q+11)}{4q^2}k^4,
}
\]

\[
\boxed{
C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
=\frac{4(q-1)^2(q^2+q+1)}{3q^2}k^4.
}
\]

The implementation verifies

\[
C^2=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-2R_{\mu\nu}R^{\mu\nu}+\frac13R^2
\]

and the Riemann symmetries, first Bianchi identity, Ricci symmetry, and Weyl tracelessness. It also
checks the closed forms at six exact rational values of `q` and verifies the expected `k^2` and
`k^4` scaling.

At either `q=1` or `k=0`, every curvature invariant vanishes exactly.

## 3. What is derived, and what is not

**DERIVED, conditional on the single-axis metric:** rank-one reciprocal-axis strain produces
nonzero Weyl curvature even when the target-area form vanishes.

**DERIVED:** the conformal metric invariant `C^2[g(phi,n)]` is strictly larger than the historical
area-only `F^2` functional.

**EXCLUDED:** the claim that substituting the reciprocal-axis metric into the metric-only conformal
branch automatically reproduces the historical `S^2` area carrier.

**NOT EXCLUDED:** a separate loop-holonomy matter principle could still select `F^2`; it would be an
additional principle rather than a consequence of the tested metric invariant.

**OPEN:** whether the conditional single-axis completion is native UDT; whether its axis target is
physically `RP^2` or an oriented `S^2` lift; and whether the full metric-derived orientation
functional supports localized matter.

**NOT DERIVED:** a unique native action, a stable carrier, an electron identification, a mass, or a
dynamical matter-emergence law.

## 4. Consequence for the derivation program

The area-only shortcut should not be adopted while “the metric is the theory” remains binding. The
next analytic task is the unrestricted invariant decomposition of

\[
C^2[g(\phi,n)]
\]

for variable `phi(x)` and `n(x)`, including all second-derivative and quartic first-derivative
terms. Only after its full continuum functional, boundary terms, target identification, and
variation are known is a numerical carrier search meaningful.

This result also clarifies why the solution space did not collapse earlier: the metric contains a
real rank-one orientation-strain sector that the area two-form deliberately discards.

## 5. Honest current status

\[
\boxed{
\begin{gathered}
\text{Existing postulates do not select area-only matter;}\\
\text{conditional reciprocal-axis metric found;}\\
\text{exact rank-one Weyl cost derived;}\\
C^2\not\equiv F^2;\\
\text{full metric-native matter functional and unique action remain OPEN.}
\end{gathered}
}
\]
