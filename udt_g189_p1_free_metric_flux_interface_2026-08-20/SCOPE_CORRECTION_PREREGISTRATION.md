# G189 scope-correction preregistration

Date: 2026-08-20

The initial preregistration simultaneously required a smooth regular central spherical static
history and proposed the control `R=R0 tanh(phi)`. Before banking the numerical outcome, direct
type-checking exposes a possible incompatibility that must be resolved rather than hidden.

For a smooth rotationally invariant scalar at a regular center,

```text
phi(R)=phi(0)+O(R^2),  hence phi'(0)=0.
```

The control instead implies

```text
phi(R)=artanh(R/R0),  hence phi'(0)=1/R0.
```

## Correction test fixed before implementation

1. Verify the nonzero derivative exactly.
2. Verify that a smooth-even control `phi=a R^2` has zero derivative and gives
   `R=sqrt(log(Z)/a)` rather than `R proportional tanh(log Z)`.
3. Reclassify the computed `R=R0 chi` likelihood as a formal outgoing annular/catalog curve
   control, not a globally regular central-static metric realization.
4. Do not infer that all metric-native P1-free constructions fail. Time-live source frequency,
   displaced/noncentral queries, and other fully regular complete histories remain open.

## Revised maximum conclusion

G189 may conclude only that the simplest direct identification of normalized reciprocal position
with central areal screen radius is both regular-center inadmissible and observationally rejected
under the declared imported transfer. It may still derive the conditional metric-to-flux
factorization and localize P1 to a supplied `phi(R)`/frequency-history role. It may not reject the
reciprocal kernel, a time-live realization, or UDT.
