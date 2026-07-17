# DISPATCH — independent reciprocal-axis functional-structure audit

## Mission

Independently verify or falsify the exact one-coordinate functional, its differential order, and
the metric-topology conclusion. Evidence only: do not update `LIVE.md` or `CANON.md`, do not begin
GPU carrier numerics, and do not adopt an `S^2` or `RP^2` carrier.

## Cold inputs

Read in this order:

1. `UDT_RECIPROCAL_AXIS_FUNCTIONAL_STRUCTURE_MAP.md`
2. `UDT_RECIPROCAL_AXIS_FUNCTIONAL_STRUCTURE_DERIVATION_RESULTS.md`
3. The two local verifier scripts only after constructing an independent tensor calculation

Use

\[
g_{00}=-q(z)^{-1},
\qquad
g_{ij}=\delta_{ij}+(q(z)-1)n_i n_j,
\qquad
n=(\cos\theta(z),\sin\theta(z),0).
\]

At a point with `theta=0`, set

\[
u=q',\quad v=q'',\quad p=\theta',\quad s=\theta''.
\]

## Required tensor audit

1. Rebuild the full four-dimensional connection, Riemann tensor, Ricci tensor, scalar curvature,
   and Weyl tensor without using a restricted action or field equation.
2. Verify all tensor symmetries, first Bianchi, Weyl trace, and

   \[
   C^2=Riem^2-2Ric^2+R^2/3.
   \]

3. Verify or falsify the full `R`, `Ricci2`, and `Riemann2` formulas in the results document.
4. Verify or falsify the exact square decomposition

   \[
   \begin{aligned}
   C^2={}&
   \left(\frac vq-\frac{u^2}{q^2}-\frac{q-1}{q}p^2\right)^2
   +\frac{((q-1)s+2up)^2}{q}\\
   &+\frac{(u^2-(q-1)q(2q+1)p^2)^2}{3q^4}.
   \end{aligned}
   \]

5. Use at least twelve mixed exact or high-precision jets, including `q<1`, `q=1`, and `q>1`,
   both signs of every first and second jet, and nonzero cross terms.
6. Recompute at a generic nonzero `theta` or prove basis-rotation invariance.

## Required variational audit

For constant `q!=1`, independently reduce to

\[
L=a(\theta'')^2+b(\theta')^4
\]

and verify the coefficients, fourth-order Euler operator, and raw boundary variation. Explicitly
distinguish this tangent equation from the unrestricted Bach equation.

## Required topology and scaling audit

1. Verify that

   \[
   q_t=1+t(q-1)
   \]

   is a positive, nondegenerate metric homotopy for every `q>0` and erases all axis dependence at
   `t=0`.
2. State precisely which boundary conditions preserve the homotopy and whether the conclusion can
   fail on a non-isotropic finite-cell boundary.
3. Verify the static rescaling

   \[
   E_C(R)=E_C(1)/R
   \]

   and list every assumption required for the dilation to be an admissible variation.
4. Do not infer absence of all non-topological or finite-cell solutions from either result.

## Evidence package

Return verifier source, raw stdout/stderr, machine-readable JSON, exact software versions and
commands, tensor convention, and SHA-256 hashes of all inputs and outputs.

## Verdicts

Return one primary verdict:

1. `IRREDUCIBLE SECOND-JET SECTOR CONFIRMED`
2. `FIRST-JET REDUCTION FOUND`
3. `REDUCED FUNCTIONAL DISAGREES`
4. `TENSOR AUDIT UNRESOLVED`

Then return separate `CONFIRMED / FALSIFIED / CONDITIONAL` judgments for:

- manifest static one-coordinate nonnegativity;
- loss of axis topology at `q=1`;
- absence of a finite stationary size under admissible free dilation.

## Stop condition

Stop after the evidence package. Do not bank a native matter carrier, unique dynamical completion,
particle stability, electron identity, or mass.
