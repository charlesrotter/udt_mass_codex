# DISPATCH — independent smooth bootstrap-substrate closure audit

## Mission

Independently verify or falsify the conditional selection of

\[
A_B=1-r^2/X^2
\]

as the unique smooth fixed-endpoint minimum of the reciprocal spherical `C^2` functional, together
with its uniform reciprocal-flux profile and carrier coefficients.

Evidence only. Do not update `LIVE.md` or `CANON.md`, replace WR-L, load empirical density values, or
start GPU carrier numerics.

## Cold inputs

Read in this order:

1. `UDT_SMOOTH_BOOTSTRAP_SUBSTRATE_CLOSURE_MAP.md`
2. `UDT_SMOOTH_BOOTSTRAP_SUBSTRATE_CLOSURE_DERIVATION_RESULTS.md`
3. `verify_udt_smooth_bootstrap_substrate_closure.py` only after constructing an independent audit

## Required action audit

1. Starting from the full reciprocal spherical metric, independently derive

   \[
   C^2=W[A]^2/(3r^4),
   \qquad
   W=r^2A''-2rA'+2(A-1).
   \]

2. Include the exact measure and prove positivity of the reduced static functional.
3. Solve `W=0` completely.
4. Apply `A(0)=1`, Cartesian smooth-center regularity, and `A(X)=0`; verify uniqueness.
5. Recompute the unrestricted Bach tensor on the result rather than trusting reduced variation.
6. Search for any other finite-action smooth zero-action metric satisfying the same domain data.

## Required flux audit

Verify or falsify

\[
J_q=q'/q^2=-A'=2r/X^2,
\]

\[
\mathcal D_q=r^{-2}(r^2J_q)'=6/X^2,
\]

including the integrated sphere-flux identity. State explicitly why this is not yet a normalized
mass density.

## Required counterprofile audit

For

\[
A_m=1-(r/X)^m,
\]

verify

\[
W=-(m-1)(m-2)(r/X)^m
\]

and the stated reduced action. Test noninteger `m>1` as well as smooth even integers; distinguish
finite action from Cartesian smoothness.

## Required carrier bridge

Independently combine the selected substrate with

\[
K_\parallel=2(q-1)J_q'/(3q),
\qquad
c_\parallel=4(q-1)^2/(3q^2),
\]

and verify the coefficients, dimensions, signs, and pointwise ratio. Do not promote the formal
three-dimensional scale balance without deriving the full operator and backreaction.

## Adversarial provenance checks

- Confirm that this branch does not revise the WR-L macro canon.
- Identify every premise needed to call the smooth metric a global substrate rather than merely a
  comparison solution.
- Search for a same-premise alternate action or boundary primitive selecting another smooth
  profile.
- Determine whether the historical quadratic-profile exclusion belongs to a different action
  branch, with exact source citation.

## Evidence package

Return independent source, raw stdout/stderr, machine-readable JSON, commands/software versions,
tensor convention, and SHA-256 hashes.

## Verdict

Return exactly one primary verdict:

1. `SMOOTH BOOTSTRAP SUBSTRATE SELECTED CONDITIONALLY`
2. `SUBSTRATE MODULUS REMAINS`
3. `REDUCED/FULL EQUATION CONFLICT`
4. `AUDIT UNRESOLVED`

Then answer separately:

- Is `D_q=6/X^2` derived or assumed?
- Are the carrier coefficient signs confirmed?
- Is physical density calibration admissible yet?

## Stop condition

Stop after the evidence package. Do not bank the substrate, carrier, density normalization, radius,
mass, or macro/readout map.
