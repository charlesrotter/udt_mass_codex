# G293 run record

Date: 2026-08-29

## Frozen checkpoints

- original preregistration: `64611d65`, pushed before new witness execution;
- repair preregistration: `039db1e3`, pushed before repaired witness execution.

## Execution chronology

1. Initial production symbolic route passed 26 checks.
2. Initial independent floating replay failed in saturated `tanh` samples because of binary
   cancellation in a nearly singular Möbius denominator.
3. `R0`: the independent floating control range was narrowed to `|s|,|t|,|k| <= 1`; exact routes,
   formulas, and the scientific landing were unchanged. It then passed 33,021 assertions.
4. Independent specialists found the time-live mixed-curvature, architecture-scope, and
   scalar-homogeneity caveats. These became frozen repairs R1--R3 at `039db1e3`.
5. Repaired production passed 42 exact symbolic checks.
6. Repaired independent route passed 46,022 assertions with no production import or result read.
7. Twelve hostile catches and four semantic gates passed.
8. Three package routes replayed byte-identically without persistent runtime output.
9. The repository-wide 276-row scientific-premise and startup-surface audit passed.

No long process, ODE/PDE solve, observation, GPU, or protected input was used.
