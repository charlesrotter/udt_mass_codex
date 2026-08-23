# G227 audit — same-event null tidal curvature tomography

Date: 2026-08-22

## Landing

```text
COMMON_ALGEBRAIC_CURVATURE_COMPATIBILITY_DERIVED_CONDITIONALLY
__FROZEN_NINE_DIRECTION_GENERIC_WITNESS_RECOVERS_19_MODES
__ONE_CHOSEN_TIMELIKE_SECTIONAL_DATUM_RECOVERS_THE_TWENTIETH
```

Grade: `DERIVED_CONDITIONAL__WHITEBOARD_PILOT_DISCLOSED__EXACTLY_INDEPENDENTLY_VERIFIED__POST_OUTCOME_SCOPE_REPAIRED`.

## What changed

G226 showed that each supplied completed null chain carries one exact `CSp+(4,R)` phase whose
conformal multiplier is the proper-clock ratio and whose inverse is the ruler carry.  G227 now
shows that supplied normalized infinitesimal optical tides in different directions at one event
cannot be chosen independently if they claim one common algebraic curvature.  They must all be
contractions of one algebraic Riemann tensor.

This is the first nonidentity same-event common-curvature restriction in the active G226 route.
Graph composition by itself is automatic; common algebraic-curvature compatibility is not.  G114 already
owned a different nonidentity compatibility invariant—beam-Lagrangian intersection rank—so G227
does not claim to be the repository's first cross-direction restriction of every type.

### Exact input type

G227 consumes the infinitesimal affine Jacobi generator

\[
A_k=\begin{pmatrix}0&I\\-\mathcal T_k&0\end{pmatrix},
\]

or an equivalent differentiable short-edge phase germ from which `T_k` can be recovered after the
G226 clock normalization is stripped.  It does **not** infer local curvature from one isolated
finite G226 transfer matrix; path ordering and matrix-log ambiguity forbid that inference.

G188 writes the optical tide with its declared curvature convention.  G227's bilinear
`R(X,k,Y,k)` may differ from G188's displayed `g(Y,R(X,k)k)` by an overall sign under index-order
conventions.  Every load-bearing rank, kernel, syzygy, and reconstruction statement is invariant
under that common sign.

## Exact theorem on the supplied local arena

Let `(V,g)` be a supplied four-dimensional Lorentz vector space.  For every null vector `k`, let
`S_k=k_perp/<k>` be its positive rank-two screen and define

\[
\mathcal T_k(X,Y)=R(X,k,Y,k).
\]

The vector space of algebraic curvature tensors in four dimensions has dimension 20.  The
constant-curvature tensor

\[
K_{abcd}=g_{ac}g_{bd}-g_{ad}g_{bc}
\]

is invisible to every null screen:

\[
K(X,k,Y,k)
=g(X,Y)g(k,k)-g(X,k)g(Y,k)=0.
\]

G227 constructs nine fixed rational null directions and an exact `27 x 20` measurement matrix
`A_9`.  Its rank is 19 and its kernel is exactly `span{K}`.  Because the full-null-sky kernel is a
subset of this finite kernel while `K` is invisible to the full sky, it follows exactly that

\[
\ker\!\left(R\mapsto\{\mathcal T_k\}_{k\ null}\right)
=\operatorname{span}\{g\wedge g\}.
\]

Thus the full null tidal sky owns 19 of the 20 algebraic curvature modes.  The frozen, chosen
timelike sectional-curvature datum

\[
\mathcal S_U(R)=R(E,U,E,U)
\]

is nonzero on `K`; appending it raises the exact rank to 20.  On this supplied tetrad, the frozen
nine-direction generic witness plus one chosen non-null sectional datum reconstructs the complete
algebraic curvature tensor.  This does not claim that arbitrary or repeated sets of nine directions
have rank 19.

## Exact finite witness

In ordered bivectors `(01,02,03,12,13,23)`, an algebraic curvature tensor is represented by a
symmetric `6 x 6` matrix subject to

```text
Q[01,23] - Q[02,13] + Q[03,12] = 0.
```

The frozen direction sequence gives cumulative exact ranks

```text
3, 6, 9, 12, 15, 16, 17, 18, 19.
```

Nine directions therefore produce 27 measured entries constrained by eight exact left-null
syzygies.  A deterministic one-entry perturbation of a valid tide table raises the augmented rank
from 19 to 20 and is rejected as not common-algebraic-curvature-compatible.

Four held-out null directions add no rank and their 12 tide entries are predicted exactly from the
null-visible equivalence class.  The unresolved constant-curvature coefficient cannot affect any
held-out null tide.

The finite witness also proves that rank 19 holds on a nonempty algebraic-open set of direction
choices.  G227 does not claim nine is the globally minimal number for every possible arrangement.

## Verification gates

1. **Preregistered:** yes, the production and certification contract was banked at commit
   `0b9135c7` after a disclosed multi-agent exact-rational pilot.  Current premise/scope wording
   includes transparent post-outcome repairs; `PREREGISTRATION_HASHES.tsv` preserves the original
   committed bytes.
2. **Bounded scope justified:** yes, one event, one supplied Lorentz tetrad, algebraic second jet,
   nine frozen null directions, four held-out directions, and one timelike sectional datum.
3. **Independent verification:** yes.  A separately written standard-library `Fraction` builder
   and Gaussian eliminator reproduced the complete `27 x 20` matrix, cumulative ranks, null
   silence, timelike rank 20, and held-out rank zero exactly.
4. **Premises audited:** yes.  Every supplied, chosen, derived, free, open, and omitted item is
   recorded in `PREMISE_LEDGER.tsv`.

Structural negative controls: `7/7`.  They detect one deterministic incompatible one-entry tide
perturbation, false scalar-curvature visibility, a null-only full-rank overclaim, one tensor excluded
by the Bianchi-reduced basis, a non-null direction, a non-screen vector, and vacuous syzygies.  This
is not a claim that every arbitrary perturbation must fail: perturbations within the 19-dimensional
common-curvature image are valid by construction.

## Relation to the “history” and “germ” gaps

This result narrows both terms but does not erase their honest remainder.

- **Same-event second-jet/tidal germ compatibility:** substantially narrowed.  Several independent
  infinitesimal directional phase generators either solve one common 20-variable curvature system
  or they are not compatible with one algebraic curvature tensor.  G227 does not use the separate
  theorem realizing every algebraic curvature tensor as a local metric 2-jet.
- **Local reconstruction:** closed conditionally after the timelike datum.  The supplied valued
  directional family reconstructs the local algebraic curvature.
- **History representation:** the retained `CONDITIONAL` G212 architecture says a sufficiently
  complete valued reciprocal network may itself encode the metric and its jets; that is not a new
  G227 theorem and is not promoted here.
- **Value generation:** still open.  Compatibility does not calculate the numerical curvature
  functions from `c_E`, `G_obs`, or finitely many anchors.
- **Population:** still open.  The metric defines lawful relation families but does not say which
  observers, emitters, experiments, or winding branches are actually instantiated.
- **Global realization:** still open.  Eventwise curvature must still obey differential Bianchi,
  overlap, topology, smoothness, and holonomy conditions to form one global metric network.

## Strict scientific ceiling

G227 derives a local common-algebraic-curvature compatibility and tomography theorem on supplied
normalized infinitesimal null-screen tidal tensors.  Its conditional bridge to the active
reciprocal route requires a differentiable affine Jacobi generator or equivalent short-edge germ;
an isolated finite G226 matrix is insufficient.  It does not select a preferred path, physical
observer population, numerical curvature profile, global metric history, dynamics, source,
action, matter, bootstrap, boundary, `X_max`,
radiative transfer, observation, mass, or signalling law.

## Lay summary

These nine chosen mathematical direction probes constrain the data to a 19-dimensional null-visible
curvature class.  Null tides cannot see one isotropic constant-sectional-curvature algebraic mode at
that supplied event.  One supplied timelike sectional datum fixes that last mode.  This reconstructs
the 20 algebraic curvature components at one event; it neither determines their variation between
events nor selects a global metric history or physical observer population.
