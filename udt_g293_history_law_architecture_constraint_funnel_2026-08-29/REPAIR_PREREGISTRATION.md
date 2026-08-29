# G293 repair preregistration

Date: 2026-08-29
Status: `FROZEN_BEFORE_REPAIR_EXECUTION`

The initial symbolic production run passed 26 checks. The first independent numerical replay failed
only because saturated `tanh` samples made the Möbius denominator ill-conditioned in binary floating
point. The independent replay range was narrowed to a well-conditioned control interval; no symbolic
formula, scientific premise, tolerance, or landing changed. This already-applied mechanical repair is
recorded as `R0` and will remain visible in the run record.

The independent hostile panel then found three scientific-scope clarifications that must be repaired
before final evidence is generated.

## R1 — time-live Euler-family closure

The slice family

```text
F_s = [1+a(s) P2(cos theta)] omega_S2
```

has constant Euler period, but it is not by itself the full closed curvature on `S2 x I` when `a`
varies. Production and independent checks must add the global difference one-form

```text
b = (1/2) cos(theta) sin(theta)^2 dphi,
db = P2(cos theta) omega_S2,
```

and the lawful connection family

```text
A=A0+a(s)b,
F=F0+a db+a' ds wedge b.
```

The mixed term must make `dF=0`. The final report must distinguish this abstract connection family
from G292's already-owned complete-metric witness.

## R2 — architecture nonexhaustiveness

The four examples in the frozen preregistration are not an exhaustive partition of all laws. For
example, a local metric two-jet scalar residual such as `R[g]=0` leaves the G259 rank-two
identity-divergence-free class without being higher order, augmented-state, global, or source-driven.

The final claim must therefore be:

> Any non-GR completion must leave at least one G259 class hypothesis; the named architecture lanes
> are organized by primitive state and data dependence, not an exhaustive mechanism census.

Einstein-plus-source must be typed inside the augmented, metric-functional, or nonlocal lane
according to what the source actually is; it is not a disjoint top-level architecture.

## R3 — scalar theorem scope and hostile cases

The final derivation and catches must state and test:

1. endpoint composition alone does not imply a homogeneous additive parameter;
2. a generic autonomous scalar flow composes without being translation equivariant;
3. on a complete state, depth-translation equivariance allows dependence on other state variables;
4. constant depth flow becomes `dot(chi)=k(1-chi^2)` in projective coordinates;
5. `k=0` is the valid trivial branch;
6. reversal compatibility requires reversing the flow orientation for nonzero `k`;
7. requiring the quiet point to be an equilibrium forces `k=0` in the scalar homogeneous lane;
8. the supplied `P2` witness uses a supplied axis and is not a classification of all same-class
   connections.

## Landing effect

R0--R3 do not promote candidate landing 2 and do not alter the primary bounded conclusion. They
tighten candidate landing 1 to:

```text
SCALAR_RECIPROCAL_GENERATOR_IS_PARAMETERIZATION_ONLY
__EULER_SECTOR_LEAVES_CONTINUOUS_FLUX_FREE
__PRIMITIVE_STATE_AND_DATA_DEPENDENCE_PARTITION_REMAINS
__UDT_HISTORY_LAW_ARCHITECTURE_NARROWED_NOT_SELECTED
```

Any repair that makes a physical parameter attachment, selects a generator, adopts a field
equation, or claims exhaustive architecture closure is forbidden.
