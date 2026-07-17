# DISPATCH — independent bootstrap-background carrier-coupling audit

## Mission

Independently verify or falsify the claimed metric-derived coupling between a nonuniform bootstrap
depth background and reciprocal-axis carrier gradients. Evidence only: do not update `LIVE.md` or
`CANON.md`, load empirical density values, start GPU numerics, or identify the axis with a physical
particle.

## Cold inputs

Read in this order:

1. `UDT_BOOTSTRAP_BACKGROUND_CARRIER_COUPLING_MAP.md`
2. `UDT_BOOTSTRAP_BACKGROUND_CARRIER_COUPLING_DERIVATION_RESULTS.md`
3. The local verifier scripts only after constructing an independent tensor calculation

## Required parallel calculation

Use

\[
g_{00}=-q(z)^{-1},
\qquad
g_{ij}=\delta_{ij}+(q(z)-1)n_i n_j,
\qquad
n=(\sin\theta(z),0,\cos\theta(z)).
\]

At `theta=0`, independently compute the full four-dimensional curvature and verify or falsify

\[
C^2
=\frac{(q q''-2q'^2+q^2(q-1)\theta'^2)^2}{3q^6}
+\frac{(q-1)^2}{q^2}\theta'^4.
\]

Verify the absence of `theta''` without assuming it, and derive

\[
K_\parallel
=\frac{2(q-1)}{3q}(q'/q^2)',
\qquad
c_\parallel=\frac{4(q-1)^2}{3q^2}.
\]

Audit all Riemann symmetries, Bianchi, Ricci symmetry, Weyl trace, and contraction identity at mixed
exact jets.

## Required background tests

1. For WR-L `q=(1-r/X)^-1`, verify `K_parallel=0` and `c_parallel=4(r/X)^2/3`.
2. For `q=(1-r^2/X^2)^-1`, verify

   \[
   K_\parallel=4(r/X)^2/(3X^2),
   \qquad
   c_\parallel=4(r/X)^4/3.
   \]

3. Reconstruct the transverse expansion, including the raw `p s` term, its boundary primitive, and
   the stated `K_eff`.
4. Explain whether any negative transverse coefficient represents carrier onset or merely alignment
   response. Do not decide from a local coefficient alone.

## Required adversarial checks

- Test a generic smooth positive `q(z)` with both signs of `(q'/q^2)'`.
- Determine whether the parallel square formula is coordinate/basis invariant within its stated
  one-coordinate alignment.
- Check whether freezing `q` loses a constraint capable of reversing the sign conclusion.
- State what full three-dimensional and backreaction terms remain absent.
- Search current canon for a normalized equation relating `(q'/q^2)'` to native density; report
  `FOUND` only with exact provenance.

## Evidence package

Return independent source, raw stdout/stderr, machine-readable JSON, exact commands/software
versions, tensor convention, input/output hashes, and every boundary term used.

## Verdicts

Return one primary verdict:

1. `BACKGROUND COUPLING CONFIRMED; SCALE CLOSURE OPEN`
2. `NATIVE BACKGROUND STABILIZATION CLOSED`
3. `BACKGROUND COUPLING FALSIFIED`
4. `OPERATOR AUDIT UNRESOLVED`

Then answer separately:

- Is the smooth-background two-/four-derivative sign pair confirmed?
- Is empirical density calibration currently admissible?
- What exact missing equation would make it admissible?

## Stop condition

Stop after the evidence package. Do not fit a density, radius, mass, carrier coupling, or bootstrap
equation.
