# Pre-P06 native boundary-selector audit

Date: 2026-07-21

Base: `fad7fd602087f1e4e609ba15e502470995e9f4db`

## Result first

The existing UDT finite-cell, Reciprocity, CSN, seal, `X_max`, co-presence, and bootstrap structure
does **not** determine one complete boundary polarization or one boundary functional for either P05
conditional dynamics lane.

It does determine one genuine, scoped piece:

```text
static spatial seal: phi=0, parity-preserving delta_phi=0,
normal derivative of phi remains free.
```

In an adapted reciprocal coframe this fixes one clock/ruler ratio tangent. It does not fix the
common scale, angular shape, off-diagonal/time-on slots, the complete induced metric, normal metric
jet, extra fields, corner data, causal type, orientation, reference, or generator normalization.

The primary classification is:

```text
PARTIAL_NATIVE_DATA_ONLY_MULTIPLE_POLARIZATIONS_AND_FUNCTIONALS_REMAIN
```

Lane outcomes:

| lane | outcome |
|---|---|
| L01 pre-scale `C^2` | `PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS` |
| L02 post-scale EH | `PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS` |
| L03 two-stage bridge | `EXCLUDED_NO_BULK_OPERATOR` |

All five registered boundary/domain branches remain visible and all 21 lane/field pairs remain
accounted. Zero pairs are P06-ready.

## What each UDT principle actually supplies

- **Finite cell:** supplies boundary/domain ontology and rejects spatial infinity. It does not type
  the boundary or prescribe its metric two-jet.
- **Static seal:** supplies `delta phi=0` in one sector while expressly leaving the reciprocal normal
  derivative free. Therefore “mirror” cannot be promoted to a full metric reflection or `K_ij=0`.
- **Reciprocity:** supplies the determinant-one clock/ruler ratio. Its exact swap conjugates
  `D(phi)` to `D(-phi)`, but the raw swap is an anti-isometry of the conditional diagonal Lorentz
  readout and has multiple inequivalent angular/time completions.
- **CSN:** leaves the pre-scale common-Weyl direction null. A null/gauge direction is not a chosen
  boundary section or a physical scale.
- **Co-presence:** is whole-solution semantics, not an off-shell variation rule.
- **`X_max` reciprocity:** is conditional dimensionless positional compatibility. It does not
  identify the local seal, choose null versus non-null character, or provide a value/reference.
- **Bootstrap:** in its current primary reading tests completed matter-bearing solutions. No varied
  bootstrap functional, response map, or boundary transversality equation has been supplied.

These statements do not conflict. They simply live at different logical layers from a complete
variational boundary principle.

## L01: conditional `C^2` lane

P05 and the frozen parent boundary audit give the covariant raw potential

```text
Theta^a = 4 alpha C^abcd nabla_d h_bc
          -4 alpha nabla_d(C^abcd) h_bc
          + Euler boundary channel.
```

On a fixed non-null Gaussian-normal diagnostic it contains independent induced-metric, normal-jet,
and corner slots. Two inequivalent allowed-variation witnesses preserve every actually supplied
seal clause, including the free normal jet:

1. fix only the reciprocal ratio tangent; leave common scale, angular, off-diagonal, and all normal
   jets free, producing the corresponding natural momentum and corner equations;
2. additionally fix transverse shape and off-diagonal induced data while leaving common scale and
   all normal jets free, producing fewer projected natural equations.

The second witness adds an unforced choice; it is not proposed physics. Its role is to prove that the
current clauses do not logically choose the first witness. Clamped/fixed-normal-jet prescriptions
remain mathematical comparisons but cannot be inferred from the canonically free `phi` derivative.

## L02: conditional post-scale EH lane

The raw potential is

```text
Theta^a = kappa (nabla_b h^ab - nabla^a h)
          + Euler boundary channel.
```

A fixed induced metric with an orientation-dependent GHY-like completion and a partially free
induced metric with projected natural momentum equations are inequivalent mathematical completions
consistent with the one seal wire. The GHY-like term is a standard comparison witness only; UDT has
not adopted it. Bare clamping of the full first metric jet is another differentiable mathematical
choice, but it would remove the free reciprocal normal-jet variation if promoted to the seal.

The null WR-L horizon cannot inherit this non-null bookkeeping automatically. Its generator,
auxiliary null direction, normalization, joints, and crossing/quotient ontology remain open.

## Why the boundary functional is independently underdetermined

Even after a polarization is declared, the current foundation leaves exact functional ambiguities:

1. a nonzero overall action rescaling preserves the stationary bulk equation and rescales momenta
   and charges;
2. the free coefficient `beta` multiplying the four-dimensional Euler density changes boundary and
   corner data while contributing no regular four-dimensional bulk metric equation;
3. adding an exact bulk divergence changes the boundary primitive without changing the bulk Euler
   equation;
4. symplectic-potential improvements `Theta -> Theta + delta Y + dZ` change potential/corner
   representatives;
5. a boundary Legendre transform exactly exchanges coordinate and momentum polarization while
   preserving the bulk symplectic form; and
6. reference, orientation, generator normalization, causal type, and joint rules remain unselected.

The exact finite-dimensional witness `p dq -> -q dp` after adding `delta(-pq)` verifies the
polarization ambiguity without importing a gravitational law. The free Euler coefficient is an
in-family counterexample to functional uniqueness for both P05 lanes.

## Boundary-type and completeness result

The audit retained:

- a fixed non-null mirror-fold branch;
- a null causal-horizon branch;
- moving or type-changing boundaries;
- quotient, crossing, or internal-match interpretations; and
- the present state in which no local realization of global `X_max` is selected.

The CMB fold and WR-L wall are already known to be distinct in their recorded branches, so one may
not be used to eliminate the other. Non-null decompositions were not extrapolated to null or moving
surfaces.

All seven field realizations remain. Metric-only L01/C01 and L02/C01 still lack a selected boundary
completion and global solution. C02--C07 additionally lack equations or declared roles for their
extra fields. L03 has no operator to vary.

## Four evidence gates

1. **Preregistered:** yes, initial commit `3048b1d`; a parent-manifest transcription was corrected in
   separate pre-algebra commit `9dd8bbd`.
2. **Full or bounded scope:** complete current-authority clause-to-slot mapping for both P05 lanes,
   all 21 field pairs, and five boundary/domain branches; no claim about an unknown future principle.
3. **Independent verification:** a non-importing implementation reconstructed the reciprocal
   involution obstruction, seal tangent rank, EH current, Legendre ambiguity, and Euler-coefficient
   ambiguity, then exercised 42 corruptions. Fresh adversarial-context attempts did not complete the
   full source read and verdict; `FRESH_ADVERSARIAL_REVIEW_STATUS.md` records the exact limitation.
   The package grade therefore remains `LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW`.
4. **Premise audit:** every theory, conditional, working, comparison-only, free, and excluded input
   is stated in the preregistration and machine tables.

Maximum conclusion:

```text
EXISTING_UDT_BOUNDARY_SELECTOR_STATUS_CLASSIFIED_FOR_P05_LANES
```

No boundary action, physical polarization, normalized charge, matter source, dynamics lane, or
P06 work is selected by this audit.
