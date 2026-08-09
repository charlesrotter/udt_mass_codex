# Complete-angular family-atlas design MAP — preregistration

Date: 2026-08-09  
Mode: `MAP` with exact operator algebra; no eigenvalue solve  
Base: `0a0602b580126e39969141598cfeb140dbade999`

## Whole question

Design the smallest honest, non-postselected atlas capable of characterizing complete angular mode
families after the equatorial FD1 roots were shown not to lift unchanged. Derive the common
stationary screen-plus-shift scalar operator, classify every registered symmetry/coupling class,
specify the basis and regularity closure each class requires, and partition later work into bounded
solve batches.

This is metric-led architecture. It does not solve a spectrum, seek a CMB match, select a screen,
or restart FD2.

## Frozen mathematical envelope

Use coordinates `(t,r,y^1,y^2)` and the stationary block form

```text
g = [[-A, 0, b_B],
     [ 0, 1/A, 0 ],
     [ b_A, 0, q_AB]],
```

where `q_AB` is a positive two-screen metric and `b_A` is angular clock/screen mixing. This is a
mathematical envelope for organizing registered representatives. It is not itself a selected UDT
completion. Direct pair/screen off-blocks, time dependence, and radial-angular off-blocks remain
outside this envelope and must be listed as dropped sectors.

## Frozen family axes

Every cross-product cell must receive exactly one disposition, even when no solve is proposed.

1. **Screen amplitudes:** round/isotropic; area only; diagonal shear only; off-diagonal shear only;
   both shears; area plus both shears; degenerate control.
2. **Mixing:** zero; one axial shift component; general two-component angular shift; twist-free
   control; sign/null causal controls.
3. **coordinate dependence:** radial only; axisymmetric `(r,theta)`; fully angular
   `(r,theta,psi)`; conditional homogeneous/global `S3` control.
4. **symmetry:** `SO(3)`; axial `U(1)` plus optional reflection; discrete only; none certified;
   symmetry enhanced/non-uniquely owned.
5. **global status:** local spherical chart; conditional complete `S3`; global screen not toric;
   missing WR-L/global join.

The 18 registered general-screen candidates C01-C18 and the five ownership classes from the parent
audit are fixed evidence inputs. They are not all to be cross-spliced into the same radial
background.

## Premise ledger

| input | status |
|---|---|
| complete-angular ownership audit | `DERIVED/OPEN` as recorded; controls this MAP |
| general screen area plus two shears | `DERIVED` configuration availability |
| stationary block-screen `S3` candidates C01-C18 | `CHOSE` bounded controls; not selected physics |
| C1 round axial lift | `CHOSE` conditional representative |
| general `(q_AB,b_A)` envelope | `CHOSE` mathematical organization device; each physical specialization separately stamped |
| scalar `Box_g` | `CHOSE` metric-native diagnostic, not native UDT dynamics |
| stationarity | `CHOSE`; time-live is an explicit dropped axis |
| center, poles, seams, wall | no physical choice; classify required conditions only |
| CMB positions/heights/polarization data | excluded |
| source/state weights | absent/open |

## Deliverables

- **D1:** exact determinant, inverse, volume density, and mode-reduced scalar operator for general
  positive `q_AB` and `b_A`, including the divergence term missed by a naive `omega-m Omega` copy.
- **D2:** `FAMILY_UNIVERSE.tsv`, with one row per atomic family and explicit registered witness,
  symmetry, couplings, global status, and disposition.
- **D3:** `BASIS_COUPLING_ATLAS.tsv`, specifying good quantum labels, coupling blocks, regularity,
  dimensionality, and a convergence basis without claiming physical selection.
- **D4:** `SOLVE_BATCH_DESIGN.tsv`, separating algebra-only, bounded CPU anchors, and later
  converged CPU/GPU work. No batch is authorized by this MAP.
- **D5:** exact verification, anti-postselection catches, completeness map, audit and lay reports.

## Certification and falsification contract

1. The block inverse and determinant must be derived in matrix notation and verified on symbolic
   two-by-two screen entries plus independent rational controls.
2. The scalar operator must include all derivatives of the volume, inverse screen, and shift. A
   general shift with nonzero angular divergence must generate its exact zero-order frequency term.
3. The operator must recover the C1 formula and the `h=0` round control exactly.
4. A family may retain `m` only when an axial Killing field is established. Axisymmetric shear may
   mix `ell` but not `m`; nonaxisymmetric coefficients may mix both. Reflection parity may be used
   only when explicitly present.
5. Every one of C01-C18 must route to exactly one family/disposition, with C14 symmetry-enhanced,
   C15 twist-free, C16/C17 causal controls, and C18 degenerate retained.
6. Conditional `S3` controls may inform topology/symmetry classes but cannot be spliced to the WR-L
   radial profile or C1 wall.
7. No family is ranked by CMB resemblance, no representative is discarded for an inconvenient
   spectrum, and no `m`, `ell`, parity, boundary, or source weight is privileged.
8. Fail-closed mutations must catch: lost area/shear mode; omitted shift divergence; false universal
   `m`; false separability; C1 promotion; C01-C18 omission/duplication; WR-L/S3 cross-splice;
   data-driven merit filter; and premature solve authorization.

## Maximum allowed conclusion

A verified design map for later complete-angular characterization, including exact operator home,
atomic families, basis blocks, and bounded solve ordering. It may identify impossible joins or
tractability classes. It may not derive the physical complete screen, a native source/population
law, a CMB prediction, or authorize FD2/GPU work.

## Completeness and stop boundary

Covered: stationary scalar diagnostic in the general screen-plus-angular-shift envelope; current
registered screen/global controls; basis and solve architecture.

Dropped but potentially emergent: time-live geometry; radial-angular and direct pair-screen
off-blocks outside the envelope; complex modes; vector/tensor channels; native action/source;
physical boundary; global WR-L/S3 join; source/state populations; polarization.

Stop after the MAP, exact independent verification, startup update, commit, and push.
