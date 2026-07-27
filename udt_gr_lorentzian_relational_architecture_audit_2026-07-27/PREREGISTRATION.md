# GR/Lorentzian relational-architecture audit — preregistration

Date: 2026-07-27
Branch: `grok`
Mode: `MAP -> OBSERVE -> PONDER`; comparison-only; CPU/document work

## Whole question

How does the primary GR/Lorentzian literature type a complete observer-to-observer comparison, and
which parts of that architecture are supplied by a Lorentzian metric, an observer, a path, a
connection, gauge equivalence, global hypotheses, field equations, or boundary/initial data?

The UDT comparison question is narrower: does that dependency map expose a wrongly typed demand in
the current complete-extension problem—for example, demanding a preferred global coframe where a
derived equivalence class plus a pathwise transport object would be the appropriate mathematical
type? The audit may sharpen a UDT derive-or-fail question. It may not import a GR field equation,
matter model, signal ontology, observer mechanics, action, source, boundary, carrier, or physical
selection rule.

## Frame and scope

This is a bounded architecture survey of the frozen source families in `SOURCE_UNIVERSE.tsv`, not
an exhaustive survey of a century of relativity. The source universe deliberately spans the
original metric theory, constructive spacetime axiomatics, frames/connections/holonomy, two-point
geometry, null optics, observer space, global causality, and relational observables. Primary papers
are controlling. Later papers may be used only to locate an original source or expose a limitation;
they cannot silently replace a primary result.

The current UDT comparison targets are frozen in `UDT_TARGET_UNIVERSE.tsv`. Current status is
controlled by `LIVE.md`, `CURRENT_SCIENTIFIC_PREMISES.tsv`, and the cited active audit—not by any
analogy found in the external corpus.

## Observing, not targeting

The audit asks what dependency types the literature actually uses. It does not search for a paper
that validates co-presence, `X_max`, a Hopf carrier, bootstrap, an action, or matter emergence. A
construction that resembles UDT but requires extra physical input will be classified with that
input visible. A construction that does not map to UDT is still a valid census outcome.

## Registered dependency types

Each load-bearing proposition must be assigned one or more exact types:

1. `METRIC_LOCAL` — follows from a supplied Lorentzian metric locally.
2. `METRIC_PLUS_ORIENTATION` — additionally needs time/space orientation.
3. `OBSERVER_EVENT` — needs an observer/worldline/timelike direction at an event.
4. `OBSERVER_PAIR` — needs two observers or two events.
5. `PATH_OR_CONGRUENCE` — needs a curve, geodesic, ray bundle, or congruence.
6. `CONNECTION_TRANSPORT` — needs a connection and its parallel/Jacobi transport.
7. `GAUGE_EQUIVALENCE` — identifies frame representatives rather than selecting one.
8. `GLOBAL_HYPOTHESIS` — needs topology, causal/global regularity, completeness, or quotient data.
9. `DYNAMICS_AND_DATA` — needs field equations and initial/boundary/matter data.
10. `OPERATIONAL_POSTULATE` — needs a registered rule about clocks, light, free fall, or readout.

## Preregistered claims to test

- `H01`: standard GR does not generally select a unique local or global orthonormal tetrad.
- `H02`: separated-frame comparison is normally path-labelled connection transport, not a universal
  endpoint-only identification.
- `H03`: curvature/holonomy is the exact obstruction to generic path-independent frame comparison;
  reduced holonomy can preserve subspaces without selecting a complete frame.
- `H04`: two-point world-function/bitensor constructions are locally canonical only where the
  relevant connecting geodesic is suitably unique; cut/conjugate structure makes path data
  load-bearing globally.
- `H05`: null optical comparison uses endpoint observers plus a null path/congruence and Jacobi/Sachs
  transport; source-observer reciprocity has explicit hypotheses rather than being an unconstrained
  universal frame law.
- `H06`: constructive axiomatics derives progressively stronger spacetime structure only from
  explicitly supplied operational primitives and compatibility conditions.
- `H07`: observer-space formulations can place observers before spacetime, but spacetime recovery
  requires integrability/quotient conditions.
- `H08`: a frame-equivalence class plus connection/transport can be complete relational geometry
  without a preferred global section.
- `H09`: GR dynamics selects a metric solution from data; it does not thereby select a canonical
  tetrad representative in generic solutions.
- `H10`: the strongest allowed UDT inference is a dependency/type correction: test whether the
  founded reciprocal representation derives a complete associated bundle, transition/equivalence
  law, admissible sections, and pathwise comparison domain before demanding a preferred member.

`H10` can only be a `LEAD` unless it is derived from current UDT foundations in a separate audit.

## Falsification and certification contract

The corresponding exact gates are frozen in `FALSIFICATION_CONTRACT.tsv`. In particular:

- any counterexample showing that a claim was stated without its source hypotheses downgrades it;
- a general GR theorem selecting a canonical complete tetrad from the metric alone refutes `H01`;
- a general endpoint-only comparison independent of path on curved spacetimes refutes `H02/H03`;
- a globally single-valued world function through arbitrary cut loci refutes `H04`;
- observer-space recovery without integrability or quotient data refutes `H07`;
- treating local Lorentz gauge freedom as seven UDT extension directions fails the UDT crosswalk;
- using a GR equation or physical postulate as affirmative UDT physics fails the entire audit.

## Maximum conclusion

The maximum bankable conclusion is a verified, premise-scoped architecture map and one ranked UDT
derive-or-fail question. It cannot select the UDT extension, observer/path ontology, variation
domain, action, source, carrier, boundary, bootstrap equation, mass, `X_max`, or dynamics. It cannot
change `CANON.md` or the current scientific premise registry.

## Evidence gates required before banking

1. Every load-bearing external claim has a primary-source locator and exact scope.
2. Every architecture row separates metric, observer, path, connection, gauge, global, and dynamic
   inputs rather than collapsing them into “GR does this.”
3. The UDT crosswalk cites current on-disk evidence and preserves all premise stamps.
4. An independent adversarial pass reconstructs the source-to-claim map without reading the final
   verdict first and exercises every anti-import catch.
5. Repository tests and current-premise verification retain their documented baseline; unrelated
   dirty/untracked paths remain untouched.
