# UDT Phi Causal-Interface and Regime-Assembly Atlas — Preregistration

Date: 2026-07-22

Base: `03e0e9407c756ad4cae2fbf4a4814c820aeaf5fc`

Branch: `codex/udt-phi-causal-interface-atlas-2026-07-22`

Status: `PREREGISTERED_BEFORE_OUTCOME_INSPECTION`

## Question and mode

This is a metric-led solution-space audit:

> Across the complete retained analytic path registry, what causal types does `dphi` have, which
> paths contain certified changes of causal type, what geometric object exists at every interface,
> how do the registered projector motifs and nonintegrability data behave there, and which local
> transition types are compatible with each registered finite-cell completion row?

The audit observes and classifies. It does not seek a particle, force, cosmological background,
clock, lump, quotient, carrier, action, or preferred universe.

## Frozen candidate universe

The candidate universe is fixed before outcomes:

- all `95,232` unique `(identity_id,family_id)` paths already frozen in
  `udt_motif_hopf_correspondence_audit_2026-07-22/PATH_FAMILY_ATLAS.tsv.gz`;
- all `3,072` analytic metric identities represented by those paths;
- the full path parameter interval `u in [0,1]`, reconstructed from the frozen analytic generator,
  not inferred only from the seventeen saved nodes;
- all 31 nonempty registered instrument-family presentations;
- every causal-type root on every reconstructed path, including repeated/tangent roots and roots
  coincident with metric or gradient degeneracy;
- all twelve rows of the registered global completion/behavior taxonomy, preserving their overlap.

Generated records from this audit may not alter candidate selection.

## Invariant objects and classifications

For each path define

```text
s(u) = g^{-1}(dphi,dphi).
```

To avoid confusing failure of the normalized projector with failure of the metric, also reconstruct

```text
Delta(u) = det(g),
n(u) = adj(g)^{ab} phi_a phi_b,
s(u) = n(u)/Delta(u) when Delta(u) != 0.
```

Every real root in `[0,1]` is classified exactly once:

- `REGULAR_NULL_CROSSING`: `Delta != 0`, Lorentzian metric, `dphi != 0`, and the sign of `s`
  changes;
- `REGULAR_NULL_TANGENCY`: the same regularity conditions, but no sign change;
- `ZERO_GRADIENT_EVENT`: all components of `dphi` vanish at the root;
- `METRIC_DEGENERACY`: `Delta=0` at or inseparably coincident with the candidate root;
- `SIGNATURE_TRANSITION`: the metric remains algebraically nonzero but leaves the registered
  Lorentzian signature;
- `UNRESOLVED_MULTIPLE_OR_NUMERIC`: certification cannot separate the above cases.

At `s=0`, `P_phi=(grad(phi) tensor dphi)/s` is not admitted. The audit must retain the unnormalized
dyad `D=grad(phi) tensor dphi`, test `D^2=sD`, and classify its rank/nilpotent behavior without
calling the metric singular merely because `P_phi` is undefined.

## Root-certification contract

1. Reconstruct `g(u)` and `dphi(u)` through the frozen generator used by the source atlas.
2. Prefer exact rational/symbolic numerator and determinant polynomials whenever the frozen data
   permit them.
3. Isolate every real root in `[0,1]` by an exact polynomial method (square-free factorization plus
   certified isolating intervals or an equivalent Sturm method).
4. If a source coefficient is not exactly reconstructible, use preregistered high-precision interval
   subdivision at at least 80 decimal digits and label any uncertified case unresolved.
5. Endpoints count separately from interior crossings. Repeated roots are retained.
6. A seventeen-node sign change is a discovery diagnostic only, never root certification.
7. An independent verifier must reconstruct the load-bearing numerator, determinant, roots, and
   sign sides without importing the production builder.

## Motif and regime-assembly contract

For every certified interface:

- record the causal type of `dphi` on both adjacent open intervals;
- record metric determinant, signature, gradient rank, `D` rank, and `D^2` behavior at the root;
- record the instrument-family motif on both sides and whether the fine projector description
  persists, changes rank, or becomes undefined;
- record whether a unique timelike line persists independently of `P_phi`;
- when a four-line family is present, record its already-audited complement-integrability/twist
  class without interpreting it physically;
- distinguish a local analytic join, a path-presentation join, and a globally completed metric
  witness.

The global cross-product may classify exact requirements and incompatibilities for all twelve
taxonomy rows. It may not claim that a local path already supplies periods, caps, a quotient,
holonomy, a physical seal lift, or a complete metric witness.

## Premise ledger

| object | status | use or limit |
|---|---|---|
| signed scalar `phi` | `pinned-by-THEORY` | native scalar and exact differential |
| metric gradient dyad `D` | `DERIVED_FROM_METRIC_AND_PHI` | no carrier meaning assigned |
| positive Common-Scale transformations | `pinned-by-THEORY` | sign/zero set of `s` must be checked invariant |
| Reciprocity | `pinned-by-THEORY` | constrains registered reciprocal structure; cannot select a branch |
| finite cell and static phi seal | `pinned-by-THEORY_WITH_OPEN_LIFT` | bounds global taxonomy; no complete time-live boundary inferred |
| four-dimensional Lorentzian representative | `CHOSE_CONDITIONAL` | every causal-type statement is representative-scoped |
| path registry and amplitude family | `free-and-explored_WITHIN_FROZEN_REGISTRY` | complete for the retained registry, not arbitrary metrics |
| interface position and multiplicity | `free-and-explored` | no root location is pinned |
| instrument family | `free-and-explored` | all 31 presentations retained |
| completion taxonomy row | `free-and-explored` | all twelve overlapping rows retained |
| action, EOM, source, carrier, scale, density | `NOT_LOADED` | no dynamics or physical selection conclusion |
| particle/force/cosmic interpretation | `FORBIDDEN_AS_FILTER` | may be pondered only after the neutral atlas |
| root precision and subdivision | `CHOSE_NUMERICAL_CATEGORY_A` | certification controls, not physics |

No physics premise is `pinned-by-HABIT`.

## Falsifiers and catches

The verifier must fail closed on at least:

- a missing or duplicate path;
- a missing, duplicated, or fabricated root;
- a sample-node sign change reported as a certified root;
- a repeated root discarded;
- `P_phi` evaluated by division at `s=0`;
- a regular null-gradient event mislabeled metric degeneracy;
- metric degeneracy mislabeled a causal interface;
- a non-Lorentzian interval assigned timelike/spacelike language;
- a path presentation counted as an independent universe;
- a local interface promoted to a global completion;
- any completion row omitted or treated as disjoint when it overlaps another;
- a particle, force, cosmic, carrier, action, or time-live label inserted as a selection criterion;
- an unregistered physical boundary condition, scale, or empirical anchor;
- failure to preserve frozen-source hashes and the original dirty-checkout metadata gate.

Each reported catch must perform an explicit corruption and demonstrate rejection through a
fail-closed validation path.

## Coverage and limits

This covers all registered paths, their full reconstructed parameter intervals, all roots, every
registered instrument presentation, and every registered completion row. It does not cover:

- arbitrary metrics outside the frozen analytic registry;
- an action/EOM solution space;
- physical evolution or a time-live topology theorem;
- a selected physical representative, branch, future direction, or global quotient;
- carrier, matter, force, cosmological, mass, scale, or empirical identification.

## Maximum conclusion

At most:

`BOUNDED_REGISTERED_PHI_CAUSAL_INTERFACE_AND_REGIME_ASSEMBLY_ATLAS_CHARACTERIZED`

If no certified crossing exists, the negative is limited to the frozen analytic path registry. If
crossings exist, they establish permitted local metric joins only. Neither result selects a physical
regime or supplies dynamics.

CPU only. No GPU work, physics fitting, carrier adoption, action selection, canonization,
navigation update, repository reorganization, or artifact relocation.
