# Complete-metric two-observer separation selector audit

Date: 2026-07-24

Base: `566686f0d05b149792b4e266e78d112830a77579`

Grade: **VERIFIED-WITH-CAVEATS**

## Result

No preregistered candidate defines one universal physical two-observer
separation across all registered causal and finite-cell completion classes.
The universal ruling remains:

```text
OPEN_SELECTOR
```

But the audit finds a genuine positive conditional construction.

On any complete branch where `dphi` is everywhere timelike and nonzero,
`phi` is a temporal function.  Every future-timelike observer history crosses
its levels monotonically, so equal `phi` pairs events without choosing a
preferred observer.  The CSN-invariant metric

\[
h_0=|g^{-1}(d\phi,d\phi)|g
\]

makes `dphi` unit timelike.  Its tensor

\[
q_0=h_0+d\phi\otimes d\phi
\]

is positive definite on each `phi` level.  Intrinsic Riemannian distance in
that level therefore supplies a symmetric, nonnegative, angularly complete,
chart/coframe-invariant observer separation.

Its exact grade is:

```text
DERIVED_CONDITIONAL_TEMPORAL_PHI_SEPARATION_FAMILY
NOT_UNIVERSAL_PHYSICAL_DG
```

## Why it does not close the universal problem

- Static WR-L has spacelike `dphi`, so the construction does not apply there.
- Spacelike `dphi` gives Lorentzian level sets; null `dphi` degenerates
  `h0`; zero `dphi` supplies no foliation; type change crosses one of those
  obstructions.
- The twelve registered completions contain zero complete on-shell
  `(g,phi)` branches. No current principle selects an everywhere-temporal
  `phi`, common observer range, complete connected levels, or global descent.
- `h0` is a canonical unit-gradient pre-scale metric, but the registered
  `h_f=exp(2f(phi))h0` family and the open physical CSN representative block
  its promotion to the unique physical ruler.
- The metric defines future-timelike histories kinematically; a native matter
  law selecting realized material observers remains absent.

## Other candidate rulings

All 24 candidates are recorded in `CANDIDATE_OUTCOMES.tsv`.

- Lorentzian interval and its absolute value fail as physical distance
  because noncoincident null pairs have zero interval.
- Causal time separation is directed and is not spatial distance.
- Spacelike curve length is path dependent until a spatial slice and
  intrinsic infimum are supplied.
- A supplied observer congruence or spatial slice gives an exact conditional
  distance, but the complete metric alone selects neither universally.
- `abs(delta phi)` and projective depth collapse distinct angular points.
- Projective/`atanh` kinematics remains `UNIQUE-CONDITIONAL` in its
  one-dimensional oriented class.
- WR-L radial proper and optical lengths remain exact conditional local
  controls, not complete observer distance.
- Complete coframe path length needs a path and spatial polarization.
- Finite-cell diameter needs a selected complete spatial metric and topology.
- Seal-normal distance needs a selected physical seal.
- Angular-fiber distance and torus dual-systole length are genuine intrinsic
  objects of the fiber, not distances between spacetime observers.
- Curvature can select a line only on special branches; the registered
  ensemble contains irreducible and flat-ambiguous controls.
- Causal accessibility supplies incidence/order, not distance magnitude.
- Reciprocity, CSN, finite-cell, seal, co-presence, and bootstrap constrain
  candidates but do not construct the missing universal object.

## Downstream stop

Because no universal candidate passed, the audit did not compute the global
diameter and did not test the local-WR-L-to-global-\(X_{\max}\) join.
Numerical \(X_{\max}\), complete action, source, boundary, carrier, density,
mass, and matter dynamics remain open.

## Evidence

- 24/24 candidate constructions adjudicated;
- 50/50 exact source identities replayed;
- five/five `dphi` causal classes classified;
- twelve/twelve completion classes classified;
- twelve principle roles separated;
- exact SymPy causal, slice, path, angular, and CSN controls;
- independent standard-library reconstruction with no production or SymPy
  import;
- 19/19 exercised catch-proofs pass;
- no external mechanics, topology, observer, representative, signal law,
  action, matter/time-live solve, GPU work, canon edit, or evidence mutation.

No fresh external-model adjudication was performed, which is the stated
caveat.
