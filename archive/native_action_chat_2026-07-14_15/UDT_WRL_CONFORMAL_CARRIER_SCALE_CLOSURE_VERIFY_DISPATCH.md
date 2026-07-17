# DISPATCH — independent WR-L conformal-carrier scale-closure audit

## Mission

Independently verify or falsify the claim that the WR-L scale `X` provides only a boundary/global
lead, not a local bulk closure of the conditional metric-derived carrier. Evidence only. Do not
update `LIVE.md` or `CANON.md`, start GPU numerics, or identify the macro seat mismatch as matter.

## Cold inputs

Read in this order:

1. `UDT_WRL_CONFORMAL_CARRIER_SCALE_CLOSURE_MAP.md`
2. `UDT_WRL_CONFORMAL_CARRIER_SCALE_CLOSURE_DERIVATION_RESULTS.md`
3. `verify_udt_wrl_conformal_carrier_scale_closure.py` only after constructing an independent audit

The live macro metric remains

\[
A_L=1-r/X.
\]

The comparison family is

\[
A_\xi(x)=1+\xi x-(1+\xi)x^2,
\qquad x=r/X.
\]

## Required exact audit

1. Recompute the full four-dimensional Weyl invariant for arbitrary `xi` and verify or falsify

   \[
   C^2[A_\xi]=0.
   \]

2. Recompute the unrestricted Bach tensor, not only the reduced radial Euler operator, for at least
   three generic `xi` values.
3. Verify `A(0)=1`, `A(X)=0`, positive static signature for the stated range, finite wall curvature,
   and the simple-zero condition.
4. Verify the homothetic `X` cancellation in the action and dimensionless field equation, and the
   static conversion `E=(alpha_C c/X) epsilon`.
5. Independently verify the center expansions and scalar curvatures:

   \[
   q_L-1=\frac{r}{X-r},\quad R_L=\frac6{Xr},
   \]

   \[
   q_Q-1=\frac{r^2}{X^2-r^2},\quad R_Q=\frac{12}{X^2}.
   \]

6. Prove or falsify the stated Cartesian smoothness condition for

   \[
   (q-1)x_ix_j/r^2.
   \]

7. Recheck the ingoing horizon metric, determinant, curvature, crossing causal directions, proper
   distance, and optical distance. Do not turn coordinate-time asymptotics into an invariant hard
   wall.
8. Audit the radial boundary director degree and the `q=1` isotropic homotopy. State precisely which
   boundary data remain fixed.

## Adversarial closure search

Search for any currently adopted, coefficient-free CSN-compatible boundary principle that selects
one `xi`, supplies all fourth-order boundary data, and blocks the local isotropic homotopy. If one
exists, identify its exact canon provenance. Do not invent or fit it.

Separately test whether residual re-centering selects `xi=-1` only as a macro restriction or also
as an off-shell variation principle. Keep that distinction explicit.

## Evidence package

Return independent source, raw stdout/stderr, machine-readable JSON, exact commands and software
versions, curvature convention, and SHA-256 hashes.

## Verdicts

Return one primary verdict:

1. `BOUNDARY-ONLY SCALE LEAD CONFIRMED`
2. `BULK SCALE CLOSURE FOUND`
3. `TERMINAL-CELL CONDITIONAL CLOSURE ONLY`
4. `AUDIT UNRESOLVED`

Then report separately:

- `ENDPOINT C2 DEGENERACY: CONFIRMED/FALSIFIED`;
- `WR-L/SMOOTH-CENTER CONFLICT: CONFIRMED/FALSIFIED`;
- `HORIZON IS NOT AUTOMATIC REFLECTOR: CONFIRMED/FALSIFIED`;
- `METRIC AXIS TOPOLOGY UNPROTECTED AT q=1: CONFIRMED/FALSIFIED/CONDITIONAL`.

## Stop condition

Stop after the evidence package. Do not bank a native carrier, transition radius, boundary charge,
particle mass, or recycling law.
