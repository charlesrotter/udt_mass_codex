# Exact derivation — global/local self-consistency premise

Date: 2026-08-01

Outcome: `BOOTSTRAP_IS_DISTINCT_POSIT`

This label is current frozen-record epistemic routing: no registered derivation makes global/local
mutual determination follow from the metric ontology, completeness requirement, finite-domain
structure, or Reciprocity. It is **not** a theorem that no future derivation from those same metric
premises is possible. The repository's current status remains `WORKING`; this audit does **not**
adopt or canonize the posit.

## 1. The key semantic separation

“The metric is the theory” is a provenance and ownership rule. It says that affirmative UDT
physics must be traced to the UDT metric and declared premises. It does not say that every law
needed to select a physical metric follows merely from uttering that rule.

A **complete metric configuration** similarly means that one supplied branch contains all fields,
charts, sectors, boundaries, joins, and moduli that its problem claims to contain. Completeness of
the description is not existence, uniqueness, physical selection, persistence, or dynamics.

The current metric record supplies many scoped forward readouts. Schematically,

```text
R: X -> O.
```

The graph

```text
Graph(R)={(X,R(X))}
```

contains every supplied `X`. It records what each configuration reads out; it does not distinguish
which configurations are realized.

## 2. Exact restriction/section control

Take four complete states and two readout values:

```text
G={0,1,2,3},
L={0,1},
R(0)=R(1)=0,
R(2)=R(3)=1.
```

`R` is surjective and noninjective. It has four different right-inverse sections, obtained by
choosing one state from each two-member fiber. Every section satisfies

```text
R(s(y))=y,
```

but the four sections have four different two-state images and therefore four different fixed
sets for `s o R`. Nothing in `R` selects one.

The graph has four rows and its projection onto `G` has all four states. A proper subrelation can
reduce the admitted set, but projection `Graph(R) -> G` is bijective. Such a subrelation is
extensionally just a predicate on `G`; it does not by itself show that the global readout is
load-bearing.

## 3. What Reciprocity adds

Let observer exchange swap states inside each readout fiber:

```text
0 <-> 1,
2 <-> 3.
```

The forward readout is invariant. Reciprocity requires a physical admissibility relation to be a
union of complete observer orbits. But two disjoint nonempty proper relations satisfy that demand:

```text
C_low ={(0,0),(1,0)},
C_high={(2,1),(3,1)}.
```

Both are proper subsets of `Graph(R)`, both are observer-saturated, and they select incompatible
states. Reciprocity constrains a supplied relation; it does not select which relation is physical.

This count belongs only to the chosen two-orbit control action. It does not derive the orbit
structure of UDT observers. Under a transitive action there is one orbit, so the only saturated
subsets are empty and full; no nonempty proper saturated subset exists. Reciprocity therefore
neither guarantees nor selects a nontrivial closure.

## 4. Finiteness and existence do not close the gap

A four-state domain admits sixteen Boolean admissibility predicates. Finiteness does not choose
one. Both `C_low` and `C_high` are nonempty, so an existence statement also cannot choose between
them. The statement “a self-consistent state exists” is compatible with inequivalent operational
laws.

This is an implication countermodel, not a model of UDT physics.

## 5. Smallest additional logical type

At the premise level, a nonconstant observer-invariant predicate on complete configurations is the
least nontrivial **admissibility** structure. After the forward readout is supplied, it is
equivalent to a nonempty proper observer-saturated subrelation of `Graph(R)`. But this is not yet
mutual determination: because `Graph(R) -> X` is bijective, the predicate can be purely local.

The least type that genuinely says global data feed back is instead:

> an observer-natural relation on independently varied `X` and `O`, with nontrivial dependence on
> both arguments and a nonempty proper intersection with `Graph(R)`.

Schematically, before closing the readout graph,

```text
C subset-of X times O,
C depends nontrivially on X and O,
solutions = C intersect Graph(R).
```

The final intersection must be nonempty and proper: some supplied configurations pass and some do
not. “Observer-natural” prevents a preferred description. A relation rather than a function allows
multiple branches and does not smuggle uniqueness, an action, or a scalar objective.

This is the minimum **operational mutual-determination type**. Current UDT authority does not define
membership in `C` or adopt it. To calculate anything, the next level would be an explicit
metric-native membership rule. A differentiable response one-form is stronger
again and is required only when asking for linear response or downstream action reconstruction.
A fixed-point operator, variational Euler map, boundary-to-bulk extension, or dynamical stability
law is stronger still. `MINIMUM_LEVEL_LEDGER.tsv` prevents those different meanings of “smallest
missing object” from being conflated.

## 6. Bounded theorem

Within the exact 1,424-source universe:

```text
metric-is-theory -> native provenance discipline                         DERIVED
complete metric -> fully specified supplied domain                       DERIVED_REQUIREMENT
complete metric -> physical selection                                    NOT_DERIVED
metric readouts -> partial Graph(R)                                       DERIVED_SCOPED
Graph(R) -> nontrivial feedback or fixed point                            NOT_DERIVED
finite domain -> boundary/admissibility law                               NOT_DERIVED
Reciprocity -> naturality of a supplied consistency relation              DERIVED_SCOPED
Reciprocity -> unique consistency relation                                NOT_DERIVED
weak bootstrap language -> independent-X/O relation type                   TYPE_SHARPENED
current frozen record -> definition or adoption of that relation           NOT_DERIVED_FOUND
```

Therefore the present frozen record has reached an evidential boundary. Repeating the already-audited
readout, finiteness, and Reciprocity implications would be circular. A genuinely new metric theorem
from the same founding premises remains possible and would supersede this epistemic routing.
