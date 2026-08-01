# Cold-review repair registration

Date: 2026-08-01  
State: post-primary-outcome, pre-repair  
Primary outcome retained provisionally: `TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED`

## Issue found by the fresh cold derivation

The preregistration required the angular-penalty interpolation to be derived. The primary package
correctly used the effective rank-one family

```text
A_tau=A0+tau|g><g|,  0<=tau<=s^2/J,
```

and correctly identified its R05 and R06 field-core endpoints, but the initial derivation document
presented intermediate `tau` as a diagnostic interpolation without deriving it from an admissible
finite aligned second wall germ.

The cold auditor independently found the missing elimination formula. If `beta>=0` is the
dimensionless finite aligned angular-trace Hessian coordinate before angular-field elimination,
then

```text
tau(beta)=s^2 beta/(1+beta J).
```

Thus `beta=0` gives R05, finite `beta>0` fills `0<tau<s^2/J`, and `beta->infinity` gives the R06
zero-trace limit `tau_infinity=s^2/J`.

## Registered repair, before mutation

1. Add the explicit one-coordinate angular minimization and derive `tau(beta)`.
2. Add exact controls for `tau(0)=0`, monotonicity, the infinite-`beta` limit, and the inverse
   `beta=tau/(s^2-tau J)` on the open interval.
3. Record `beta` in the premise and status ledgers as `FREE_AND_EXPLORED`, not supplied, selected,
   native, or physical.
4. Add a fail-closed catch rejecting a finite-`beta` claim at `tau=tau_infinity`.
5. Preserve every certified threshold and conclusion ceiling unless the completed cold review finds
   a mathematical contradiction.
6. Record any further cold-review bookkeeping or independence caveat explicitly; do not silently
   rewrite the preregistration or the original primary artifacts.

## Scope guard

This repair establishes that the intermediate coordinate is a mathematically permissible
conditional second-germ slice. It does not derive that UDT chooses such a germ, does not specify an
underlying physical wall functional, and does not enlarge the calculation to the full wall Hessian.
