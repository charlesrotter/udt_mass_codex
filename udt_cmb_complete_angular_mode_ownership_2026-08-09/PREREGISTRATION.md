# Complete-angular mode-family ownership and observer-pair projection audit — preregistration

Date: 2026-08-09  
Mode: `MAP -> OBSERVE -> DERIVE`  
Computation: bounded CPU exact/symbolic algebra only; no GPU or spectral fitting

## Whole question

The corrected FD1 scalar atlas contains three interleaved equatorial Fourier ladders labeled
`m=-1,0,+1`, but it does not supply a physical multiplet or population rule. Determine what the
registered complete UDT metric structure actually permits one to say about those labels and about
an observer-pair projection:

1. Does a registered complete angular lift turn the three equatorial ladders into independent
   full-angular families, components of a larger representation, or coordinate artifacts?
2. Does the metric alone supply an invariant projection or spectral weighting that selects which
   families enter one observer-pair readout?
3. If the registered complete structure does not select either object, state the exact missing
   operation and the honest form of any later FD2 characterization.

This is metric-led. It does not seek a CMB match, a singlet, a triplet, polarization, or a preferred
ladder.

## Frozen candidate classes

Every class is retained even if it defeats the hoped-for projection.

| id | class | premise status | purpose |
|---|---|---|---|
| C0 | FD1 stationary equatorial scalar `Box_g` slice | `CHOSE`, inherited provenance control | establish exactly what the existing `m` labels mean |
| C1 | axis-regular round-screen lift `ds^2=-A dt^2+dr^2/A+r^2 dtheta^2+r^2 sin^2(theta)dpsi^2+2h(r)sin^2(theta)dt dpsi` | `CHOSE` conditional spherical inheritance named by RA1; not a selected complete UDT metric | derive the strongest clean full-angular conditional realization |
| C2 | C1 with `h=0` | derived limit control only | expose the symmetry-restored spherical representation structure |
| C3 | registered complete general screen with area plus two shears and possible mixing | available configuration class; response values and global realization unselected | test whether `m` survives without an imposed axial Killing field |
| C4 | registered complete `S3`/global controls | conditional configuration evidence only | test whether any existing authority selects C1 or a unique mode projection; no WR-L/S3 cross-splice |

The C1 lift is not silently promoted. Failure of C1 to be native does not prevent its exact
conditional algebra from being useful, and success inside C1 does not select it.

## Premise ledger

| object | status |
|---|---|
| founded reciprocal depth and complete-pair phi/orchestra structure | `DERIVED` within their registered scopes |
| FD1 462-row original-field atlas | `OBSERVED`, `VERIFIED-WITH-CAVEATS`, equatorial scalar slice only |
| scalar `Box_g Psi=0` | `CHOSE` metric-native diagnostic; not the native UDT dynamics |
| `A(r)`, `h(r)`, stationarity, axial chart, real `omega` | supplied/`CHOSE` for C0/C1; no profile fitting here |
| round screen and `sin^2(theta)` mixing completion | `CHOSE` axis-regular C1 representative |
| general screen area/shear/mixing modes | `DERIVED` as available configuration directions; not selected values |
| D/N wall representatives | `free-and-explored` in FD1; no wall selection in this audit |
| observer endpoints, path/query, source state, mode amplitudes | `OPEN`; no values invented |
| `S^2` matter carrier, native action/source, polarization law | absent; no import |
| CMB peak/trough values | excluded from derivation and acceptance criteria |

## Exact deliverables

- **D1:** determinant, inverse metric, volume density, and full scalar `Box_g` operator for C1,
  checked against the equatorial and `h=0` limits.
- **D2:** exact symmetry and separation atlas: axial generator, broken/restored rotations,
  `r-theta` coupling, and discrete symmetry relations.
- **D3:** ownership map from C0 `m` labels to C1/C2/C3 mode labels, including the full-center
  regularity distinction from the equatorial `r^|m|` rule.
- **D4:** metric-only observer-pair projection audit. Separate invariant operator/spectral
  decomposition from state/source populations and from an endpoint/path readout.
- **D5:** machine-readable status and completeness ledgers, exact algebra, and a lay report.

## Falsification and certification contract

1. Direct symbolic inversion must satisfy `g*g_inverse=I`, and the determinant must reproduce both
   the equatorial C0 determinant and the round `h=0` determinant.
2. The derived scalar operator must reduce at `theta=pi/2` only after explicitly suppressing
   theta-dependence; that operation must remain labeled a slice, not an identity of the full PDE.
3. For generic nonzero `h`, a product `R(r)Theta(theta)` may be called separated only if every
   coefficient can be written as a sum of a pure-r and pure-theta term after one common multiplier.
   A mixed derivative witness or a nonzero exact cross-derivative fails separability.
4. The C1 symmetry claim must be checked by Lie derivatives: `partial_psi` must survive; at least one
   non-axial round-sphere rotation must fail for generic `h` and return at `h=0`.
5. C2 must recover spherical harmonics labeled by `ell,m`, with fixed `ell` rather than equal radial
   index defining an `SO(3)` multiplet. C1 must not inherit that multiplet without its symmetry.
6. Any claimed observer-pair projection must be constructed from registered metric/query data,
   commute with admissible frame/chart changes, and specify its domain, codomain, measure, and
   variation/dynamical ownership. A source state, Green-function prescription, boundary choice, or
   arbitrary family weight fails metric-only selection.
7. C3/C4 evidence must be checked for an actually selected axial Killing line and projection. Mere
   existence of an axial or round representative is not selection.
8. Independent verification must reconstruct load-bearing algebra by a separate implementation and
   exercise mutations that omit `sin^2(theta)`, erase theta coupling, restore false `SO(3)`, assert a
   same-index triplet, or insert arbitrary mode weights.

No tolerance, candidate class, or conclusion wording may be changed after inspecting results.

## Maximum allowed conclusion

At most: a bounded exact ownership/projection theorem or nonselection theorem for C0-C4. Even a
positive result would not derive a CMB source, peak heights, polarization, native dynamics, a
physical boundary, or an observational prediction. If no unique projection is selected, FD2 may
later characterize all surviving families but may not optimize one preferred ladder.

## Completeness stamp

Covered: scalar probe; exact stationary C1 full angular lift; its symmetry-restored limit; current
general-screen/global selection evidence; algebraic projection ownership.

Dropped and still potentially emergent: time-live geometry, generic nonblock four-metrics, higher
angular content outside the selected C1 representative, Robin/complex spectra, vector/tensor
probes, physical source/state, action, boundary, bootstrap return, and polarization. This package is
one structural tile, not a complete CMB or UDT solver.

## Stop boundary

Stop after derivation, independent verification, startup update, commit, and push. Do not restart
FD2, fit data, choose mode weights, run polarization, or launch GPU work.
