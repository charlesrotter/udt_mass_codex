# Calibrated reciprocal-readout descent audit

Date: 2026-07-26

Preregistration: `9cf083e`

Pre-result scope correction: `77a0a74`

Grade: `VERIFIED_WITH_CAVEATS`

## Result first

The founding calibrated clock/ruler readout and a physical reciprocal-swap
isometry are incompatible.

More precisely: if the reciprocal `-1` eigenline is the physical timelike
clock and the `+1` eigenline is the physical spacelike ruler, the reciprocal
generator is self-adjoint. No Lorentzian metric in that complete class makes
an inverting transition that swaps the two eigenlines an isometry—or even a
positive conformal isometry.

This conditionally removes the most direct interpretation of the previous
`lambda=0` result:

```text
lambda=0 is not an aligned physical Levi-Civita/metric swap holonomy.
```

It does **not** remove `lambda=0` from UDT. Two different routes remain:

1. an internal sign-twisted reciprocal bundle that is not itself physical
   tangent-frame holonomy; or
2. a mixed Lorentzian readout where the swap is an isometry, but the physical
   clock is a mixture of reciprocal eigenchannels and the reciprocal action
   is not a pure self-adjoint dilation.

Neither route is presently selected.

## Exact pair classification

For the complete real symmetric pair readout

```text
H=[[A,B],[B,C]],
```

the results are exhaustive:

- Lorentzian: `AC-B^2<0`.
- Self-adjoint reciprocal dilation: `B=0`, hence `AC<0`.
- Reciprocal-swap isometry: `C=A b^2` and
  `B^2>A^2 b^2`.
- Both simultaneously: no Lorentzian solution.
- Positive conformal swap: no enlargement, because involutivity forces the
  positive conformal factor to one.

In the swap-isometric family, the two reciprocal eigenlines have the same
causal sign, or both are null. Therefore they cannot simultaneously be the
aligned physical clock and ruler.

## What observed c does and does not do

The mixed family is genuinely Lorentzian, so it possesses an orthonormal
frame and can be calibrated with observed `c_E`. Calibration alone therefore
does not force `B=0` or align the reciprocal eigenchannels with the physical
clock/ruler frame.

The founding derivation contains more than the scalar value of `c_E`: its
declared local metric readout explicitly aligns `c_E dt` and `dr` with the
reciprocal pair. That aligned slice is exact. Whether the complete
four-dimensional extension must preserve that alignment is still recorded as
open. The audit therefore does not silently promote the local slice into a
global theorem.

## Complete four-dimensional extension

Self-adjointness gives an exact block atlas:

- generic `lambda`, including zero: `1+1+2`, five metric parameters;
- `lambda=+1`: `1+3`, seven metric parameters;
- `lambda=-1`: `3+1`, seven metric parameters.

All have aligned Lorentzian local witnesses. Rejecting the aligned physical
swap does not choose among them.

The ordinary holonomy atlas therefore remains intact:

- trivial or screen-only `SO(2)` holonomy retains every `lambda`;
- a selected timelike-line `SO(3)` reduction would force `lambda=+1`;
- a selected spacelike-line `SO+(1,2)` reduction would force `lambda=-1`.

No such reduction is currently selected.

## Readout fork

The open choice is now sharply typed:

1. **Aligned physical channels:** founding clock/ruler interpretation;
   physical reciprocal swap is obstructed.
2. **Mixed physical readout:** reciprocal swap can be metric-isometric, but
   the physical clock/ruler are mixtures and a new complete solder is needed.
3. **Internal twisted bundle:** exact reciprocal descent survives without
   claiming physical metric holonomy.
4. **Ordinary holonomy:** no reciprocal swap is required; branch-dependent
   `lambda` classification remains.

This is progress because it prevents the elegant `lambda=0` seam result from
being promoted through an incompatible physical interpretation.

## What remains open

- whether the founding channel alignment is a required property of every
  complete UDT metric or only its local/simple slice;
- whether a mixed readout has any native complete-coframe solder;
- actual complete metric branch, holonomy, seams, and monodromy;
- `lambda` selection;
- action, carrier, source, boundary functional, density response, bootstrap,
  mass, and dynamics.

`G_obs` and provisional `hbar` do not affect this directional readout rank;
`hbar` was not activated.

## Evidence gates

1. **Preregistered:** yes, `9cf083e`, with the ordinary-family scope corrected
   append-only at `77a0a74` before outcome algebra.
2. **Full or bounded:** complete for all real symmetric nondegenerate `2x2`
   readouts, constant reciprocal swaps, positive conformal factors, four
   complete self-adjoint `lambda` strata, twelve routes, and seventeen
   readout strata.
3. **Independent:** yes, a no-SymPy exact-rational implementation includes a
   complete bounded integer census with 18 self-adjoint Lorentzian readouts,
   18 swap-isometric Lorentzian readouts, and zero simultaneous examples,
   plus complete block witnesses.
4. **Premises audited:** yes. Calibration, alignment, self-adjointness,
   isometry, conformal sign, mixed solder, internal descent, ordinary
   holonomy, and excluded physics remain distinct.

No fresh external-model review was authorized; that is the caveat.

Maximum conclusion:

```text
BOUNDED_CALIBRATED_RECIPROCAL_READOUT_DESCENT_CLASSIFICATION;
ALIGNED_CAUSAL_SELF_ADJOINT_READOUT_HAS_NO_PHYSICAL_INVERTING_ISOMETRY;
MIXED_AND_INTERNAL_TWISTED_ROUTES_REMAIN_CONDITIONAL;
NO_LAMBDA_OR_GLOBAL_READOUT_SELECTED.
```
