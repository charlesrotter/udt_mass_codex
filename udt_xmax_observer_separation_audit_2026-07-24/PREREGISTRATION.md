# X_max observer-separation framing audit preregistration

Date: 2026-07-24

Base: `696cf401c441fdd3aefea6f3de188e6425ae5636`

Mode: CPU-only, metric-led and source-led provenance/dependency audit

## Owner correction being audited

The controlling owner framing for this audit is:

> `X_max` is the maximum possible separation between two observers. It is
> not, merely by definition, the edge of the universe.

This is registered as an owner-specified `WORKING` meaning, not silently
promoted to a metric derivation.

## Whole question

Across every tracked textual occurrence of `X_max` or a spelling variant:

1. Which claims require only a global length scale and remain unchanged?
2. Which claims are already relational or can be translated exactly into
   symmetric observer-pair language?
3. Which claims use a local static radial coordinate or finite-cell chart
   parameter that must remain distinct from global `X_max`?
4. Which claims infer an edge, boundary surface, preferred center, or radial
   direction from `X_max` and therefore require correction or regrading?
5. What is the smallest missing mathematical object needed to turn the owner
   meaning into a metric-derived invariant?

The audit characterizes dependencies. It does not seek a desired topology,
cosmology, horizon, boundary, mass law, or reciprocity formula.

## Candidate universe frozen before semantic inspection

`build_preregistered_census.py` mechanically selects every tracked textual
file of the registered extensions containing one or more of:

```text
X_max, Xmax, x_max, xmax, X_MAX, X_{\max}
```

The resulting exact path set, Git blob, SHA-256, size, and matching-line
count are frozen in `CANDIDATE_UNIVERSE.tsv`. Generated audit records do not
enter their own candidate universe.

`PREREGISTRATION_CORRECTION.md` expands this matcher to lowercase LaTeX and
freezes the census explicitly against the base commit. That correction was
registered before semantic classification continued.

Every candidate will receive exactly one provenance/lifecycle disposition.
Family-level evidence is allowed for repeated generated records, but every
path remains individually accounted for.

## Required distinctions

The audit must not collapse:

1. owner meaning versus metric derivation;
2. a symmetric observer-pair separation versus a coordinate radius;
3. a global diameter/supremum versus a boundary point or surface;
4. maximum versus unattained supremum;
5. local WR-L scale `X` versus global `X_max`;
6. finite-cell coordinate completion versus physical spatial edge;
7. pair exchange symmetry versus full equivalence of accelerated frames;
8. dimensional use of a length scale versus its physical selection;
9. asymptotic clock/mass behavior versus boundary topology;
10. historical evidence versus current authority.

## Premise and value ledger

All physical choices are frozen in `PREMISE_LEDGER.tsv`.

- No numerical value of `X_max`, `c`, `G`, density, mass, or scale is used.
- No observer separation functional, simultaneity convention, topology,
  boundary, source, carrier, or action is supplied by habit.
- No GR field equation or external dynamics is imported.
- Historical and frozen packages remain byte-identical; corrections are an
  overlay.

## Falsification contract

The classifications fail if any condition in
`FALSIFICATION_CONTRACT.tsv` is accepted. In particular, the audit must stop
short of a covariant formula if the complete metric and registered premises
do not presently define which events on two observer histories are compared.

## Maximum allowed conclusion

At most the audit may:

- establish the logically correct relational type of `X_max`;
- identify an exact candidate schema for a metric-derived observer-pair
  diameter;
- prove which consequences follow from that type alone;
- regrade all current dependencies and historical edge language;
- state the smallest genuinely missing object.

It may not derive a numerical `X_max`, select a topology or boundary, adopt
a radial universe, prove the clock/mass asymptote globally, close bootstrap,
construct an action or source, launch a matter/time-live solve, or use a GPU.
