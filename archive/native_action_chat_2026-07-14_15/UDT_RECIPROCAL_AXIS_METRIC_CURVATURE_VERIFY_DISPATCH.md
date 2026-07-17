# DISPATCH — independent reciprocal-axis metric curvature verification

## Mission

Independently verify or falsify the claimed **RANK-ONE WEYL COST** of the conditional reciprocal-axis
metric. This is an evidence-only audit. Do not update `LIVE.md` or `CANON.md`, do not start F/G, and
do not infer carrier stability or particle mass.

## Inputs

Read only:

1. `UDT_RECIPROCAL_AXIS_METRIC_CURVATURE_MAP.md`
2. `UDT_RECIPROCAL_AXIS_METRIC_CURVATURE_DERIVATION_RESULTS.md`
3. `verify_udt_reciprocal_axis_metric_curvature.py` only after building an independent calculation

Use

\[
g_{00}=-q^{-1},
\qquad
g_{ij}=\delta_{ij}+(q-1)n_i n_j,
\qquad
n(z)=(\cos kz,\sin kz,0),
\qquad q>0.
\]

## Required independent audit

1. Compute the full four-dimensional Christoffels, Riemann tensor, Ricci tensor, scalar curvature,
   and Weyl tensor from the metric. Do not use field equations or a symmetry-restricted action.
2. Verify `det(g)=-1` and prove

   \[
   F_{ij}=n\cdot(\partial_i n\times\partial_j n)=0
   \]

   identically from rank-one dependence.
3. Verify or falsify, allowing for the opposite Riemann sign convention,

   \[
   R=-\frac{(q-1)^2}{2q}k^2,
   \]

   \[
   R_{\mu\nu}R^{\mu\nu}
   =\frac{(q-1)^2(3q^2+2q+3)}{4q^2}k^4,
   \]

   \[
   R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
   =\frac{(q-1)^2(11q^2+10q+11)}{4q^2}k^4,
   \]

   \[
   C_{\mu\nu\rho\sigma}C^{\mu\nu\rho\sigma}
   =\frac{4(q-1)^2(q^2+q+1)}{3q^2}k^4.
   \]

4. Audit all Riemann pair symmetries, the first Bianchi identity, Ricci symmetry, Weyl
   tracelessness, and

   \[
   C^2=Riem^2-2Ric^2+R^2/3.
   \]

5. Check `q=1`, `k=0`, and at least three nontrivial rational `q` values with exact or high-
   precision arithmetic.
6. Recompute at a generic `z` or explain rigorously why the scalar results are `z`-independent.
7. Determine whether any coordinate or common-conformal calibration can remove the nonzero Weyl
   tensor. Distinguish a tensor invariant from a component artifact.
8. If cheap, give one second independently chosen rank-one texture and state whether it supports or
   falsifies the same functional discrimination. Do not generalize beyond what is actually tested.

## Raw evidence required

Return:

- verifier source;
- raw stdout/stderr;
- machine-readable JSON containing parameters, tensor-convention statement, all invariants, and
  pass/fail gates;
- exact software versions and invocation;
- SHA-256 hashes of inputs and outputs.

## Verdict vocabulary

Return exactly one primary verdict:

1. `RANK-ONE WEYL COST CONFIRMED`
2. `RICCI-ONLY RANK-ONE COST`
3. `RANK-ONE FLAT`
4. `TENSOR AUDIT UNRESOLVED`

Then state separately whether the stronger claim

\[
C^2[g(\phi,n)]\equiv F^2
\]

is falsified for the conditional metric.

## Stop condition

Stop after the evidence package. Do not bank a native action, `S^2` carrier, soliton stability,
electron identity, or mass conclusion.
