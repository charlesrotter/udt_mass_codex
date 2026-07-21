# P05 conditional full-equation and variation audit

Date: 2026-07-21

Base: `39dda1aac9a8dab16428f7d031e1668b9bc7fde0`

## Result first

P05 derived the unrestricted **bulk metric operators** for the two P04-authorized conditional
lanes before any symmetry reduction:

| lane | exact conditional bulk result | differential character | stopping obstruction |
|---|---|---|---|
| L01 pre-scale `C^2` | `B_ab = 0` for nonzero `alpha` | fourth order; diagnostic double metric-null factor after quotienting diffeomorphism and Weyl degeneracy | finite-cell polarization/action/corners and all non-metric equations open |
| L02 post-scale EH | `G_ab + Lambda g_ab = 0` for nonzero `kappa` | second order; diagnostic simple metric-null factor after quotienting diffeomorphism degeneracy | representative/scale, finite-cell polarization/action/corners, and all non-metric equations open |

The Euler density has zero regular four-dimensional bulk variation in both lanes, but its boundary
channel remains explicit. `Lambda` remains symbolic, including its zero subcase. Neither operator is
labeled native or selected by UDT.

The protocol-level conclusion was **not** earned. The banked maximum is:

```text
NAMED_BULK_OPERATORS_AND_VARIATION_OBSTRUCTIONS_CHARACTERIZED
```

No solution, ODE, PDE, bridge, source, carrier, scale, or physical representative was supplied.

## The decisive boundary result

For a curvature Lagrangian with `P^abcd = partial L / partial R_abcd`, P05 records the raw potential

```text
Theta^a = 2 P^abcd nabla_d h_bc - 2 nabla_d(P^abcd) h_bc.
```

For L01 this exposes both derivative-of-variation and undifferentiated-variation Weyl channels, plus
the Euler boundary channel. For L02 it gives the EH current
`kappa (nabla_b h^ab - nabla^a h)` plus the Euler channel. A raw current is not yet a differentiable
finite-cell variational principle. The static scalar seal wire `delta phi = 0` fixes only one scalar
variation and cannot select the complete metric boundary polarization.

This is why P05 stops. Importing familiar GHY, asymptotic, topology, or corner rules would fill the
actual UDT selector seam by habit.

## Variation-domain audit

Varying after imposing an ansatz generally yields only the tangent projection `J^T E = 0`, not all
ten metric equations. Exact witnesses establish that:

- a reduced stationary point can leave a nonzero normal Euler component;
- on the one-function reciprocal spherical metric, the reduced EH density is an exact radial
  boundary primitive even though the full Einstein equations are not empty; and
- conformal flatness makes both `C^2` and Bach vanish, so that reduction is a vacuous rather than
  discriminating equivalence test.

Consequently later branch work must start from the full operator and then verify every reduced
solution against it. A multiplier realization is separately tracked and is not silently equated to
unrestricted variation.

## Completeness census

All 21 P04 lane/field-realization pairs remain present. Only `L01/C01` and `L02/C01` have their named
metric bulk equation; even those have open boundary and global completion. Every branch with an
independent `phi`, coframe, projector, multiplier, bridge stage, or connection remains incomplete or
excluded because the named metric-only bulk does not provide that field's equation.

All 12 P03G global axes remain `FREE_UNSELECTED_UNSOLVED`. Regular inverse-metric principal-symbol
results do not erase degenerate or type-changing branches.

## Evidence gates

1. **Preregistered:** yes, commit `de09c58`, before operator generation.
2. **Full or bounded scope:** complete for both named ten-component metric bulk variations, their raw
   boundary channels, all 21 field pairs, and all 12 carried global axes; no global solution claim.
3. **Independent verification:** a non-importing implementation replayed source hashes and tables,
   reconstructed five load-bearing algebraic identities, and passed 31 deliberate corruptions. A
   fresh adversarial-context review is still a separate evidence gate, so the machine result remains
   `LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW` until that record exists.
4. **Premise audit:** yes; all inherited, added, open, comparison-only, and excluded inputs are stated
   in the preregistration and lane convention records.

No startup control or `CANON.md` is changed by P05.
