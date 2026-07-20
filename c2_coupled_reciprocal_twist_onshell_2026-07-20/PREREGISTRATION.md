# Coupled reciprocal-background/full-Bach twist selector — preregistration

Date: 2026-07-20

Base: `2d2809ca7c83d9262d8db99d7962806c9487dfff`

Branch: `codex/c2-coupled-reciprocal-twist-onshell-2026-07-20`

Mode: CPU-only exact symbolic and independent automatic-differentiation metric audit

## Whole question

The parent audit exactly derived, for the local reciprocal/twist coframe,

```text
L_twist = exp(-4p) [u_second^2
          + (4/3)(p_second - 2 p_first^2) u_first^2].
```

The lower-order coefficient can have either sign while `p(r)` is an arbitrary off-shell
background. This audit asks the next necessary question:

> When the twist-free reciprocal background is required to satisfy the complete metric-only Bach
> equation in this exact local ansatz—not merely the reduced `p` Euler equation—does that equation
> force the coefficient stratum `p_second - 2 p_first^2` to be positive, zero, negative, or
> genuinely branch-dependent?

This is `METRIC_LED` and `OBSERVING`. It tests whether the simplest on-shell reciprocal background
supports the two-order bridge. It does not target a favorable sign or a particle.

## Exact bounded frame

Use the parent coframe

```text
e0 = exp[-p(r)] dt
e1 = exp[+p(r)] dr
e2 = dx
e3 = dy + epsilon*u(r) dx.
```

At `epsilon=0`, construct the full four-dimensional Bach tensor directly from the metric. Derive
all independent component equations for arbitrary local jets of `p`. Separately vary the exact
twist-free reduced `C2` density with respect to `p` and compare its equation with the full tensor
conditions. A reduced stationary point is not promoted unless every full Bach component vanishes.

Then substitute every characterized full-Bach branch into the already verified twist coefficient

```text
Q = p_second - 2 p_first^2.
```

No finite-cell boundary condition is imposed. Local analytic branch characterization is allowed;
global regularity, caps, and bootstrap closure are not inferred.

## Premise ledger

| Object | Status |
|---|---|
| The metric is the theory | `pinned-by-THEORY` |
| Reciprocal exponential clock/radial block | `DERIVED-CONDITIONAL` under the existing representative, sign, unit, and slot premises |
| Four-dimensional conformal-Lorentzian readout | `INHERITED / CONDITIONAL` |
| Metric-only local `C2` bulk | `UNIQUE-CONDITIONAL` only in the frozen pre-scale action class |
| Static cohomogeneity-one direct product with flat transverse tile | `pinned-by-HABIT / BOUNDED SLICE` |
| Reciprocal profile `p(r)` | `free-and-varied`; arbitrary local analytic jets before the equation is imposed |
| Transverse twist `u(r)` | zero in the background; retained only through the exact parent Jacobi coefficient |
| Full Bach tensor | `pinned-by` the conditional `C2` variation; derived directly, not imported GR dynamics |
| Restricted reduced-p Euler equation | category-A diagnostic; never sufficient for full on-shellness |
| Local chart and interval | `pinned-by-HABIT`; no global topology |
| Boundary conditions and boundary action | `OPEN / EXCLUDED` |
| Angular curvature, caps, finite-cell seal, bootstrap | `OPEN / EXCLUDED` |
| Carrier, `S2`, `L2+L4`, source, mass | `OPEN / EXCLUDED` |
| Symbolic algebra and AD witnesses | category-A methods |

No EH equation, GR source, carrier action, fitted coefficient, cutoff, or physical scale enters.

## Frozen calculations

1. Derive the exact twist-free `C2` density, scalar curvature, full Bach tensor, and all independent
   component equations from the four-dimensional metric.
2. Express the component equations in a minimal invariant jet basis including
   `Q=p_second-2 p_first^2` where useful, without dividing by a quantity that may vanish.
3. Derive the reduced Euler equation from the one-function background density and display its
   complete endpoint variation.
4. Determine whether reduced stationarity is weaker than full Bach stationarity, with explicit
   counter-witnesses if so.
5. Characterize every local full-Bach solution branch admitted by the component equations, including
   degenerate/zero strata.
6. Substitute each branch into the parent twist coefficient and classify its sign or vanishing.
7. Independently reconstruct the Bach components by a separate Torch forward-AD implementation at
   preregistered analytic witnesses.
8. Exercise mutations that use only the reduced equation, discard a Bach component, divide by `Q`,
   assume nonzero curvature, choose a sign, or promote the result beyond the local tile.

## Independent witness profiles

Before outcome inspection, freeze:

```text
P1: p = r/3 + r^2/5 - r^3/7,       r = -1/3, 1/5, 2/3
P2: p = -r/4 + 2 r^2/7 + r^4/13,  r = -2/5, 1/7, 3/5
P3: p = constant 1/6,              r = -1/2, 1/4
```

The direct component comparison tolerance is relative `1e-8` in float64, with absolute `1e-9` for
zero controls. These are algebra witnesses, not physical solutions.

## Frozen outcome classes

1. `FULL_BACH_FORCES_Q_ZERO_IN_THIS_TILE` — every full-Bach branch has `Q=0`, so the induced
   lower-order twist term disappears in this bounded on-shell background.
2. `FULL_BACH_SELECTS_NONZERO_Q_SIGN` — all admitted full-Bach branches have one nonzero sign.
3. `FULL_BACH_PERMITS_MULTIPLE_Q_STRATA` — distinct full-Bach branches realize different signs or a
   zero/nonzero mixture.
4. `REDUCED_STATIONARITY_FALSELY_SELECTS_EXTRA_BRANCHES` — the one-function Euler equation admits
   branches rejected by an omitted full Bach component.
5. `FULL_BACH_BRANCH_CLASSIFICATION_INCONCLUSIVE` — algebraic factorization, independent replay, or
   local branch completeness fails.

Multiple outcome classes may apply if, for example, the full equation forces zero while the reduced
equation admits spurious extra branches.

## Completeness and certification contract

- Exact component and variation identities must simplify to zero without dividing by `Q` or a
  derivative that can vanish.
- All nonzero independent Bach components must be retained.
- The independent tensor implementation must match every registered component witness within the
  frozen tolerances.
- Any branch claim must be established from the complete local component system, not selected
  examples.
- The complete endpoint variation must be recorded separately from the bulk equation.
- A local result cannot be promoted to global regularity, finite-cell closure, stability, carrier,
  matter, or mass.

Maximum positive conclusion:

`CONDITIONAL_LOCAL_FULL_BACH_RECIPROCAL_BACKGROUND_TWIST_COEFFICIENT_STRATUM_CHARACTERIZED`.

This tile omits intrinsic angular curvature, transverse size/shear, nontoric dependence, finite-cell
caps and seal, time dependence, unrestricted metric components, physical scale, boundary
completion, bootstrap, carrier, source, and mass. Failure of a nonzero coefficient here would
redirect the bridge toward those omitted sectors; it would not refute a complete UDT geometry.
