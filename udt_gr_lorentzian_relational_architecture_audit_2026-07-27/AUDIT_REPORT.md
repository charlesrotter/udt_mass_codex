# GR/Lorentzian relational-architecture audit

Date: 2026-07-27

Verdict: **VERIFIED-WITH-CAVEATS** architecture map; **LEAD** for UDT dependency order.

## Result first

The century-scale comparison produced a concrete type correction, not an imported mechanism.
General relativity does not encode a complete observer-to-observer relationship in one preferred
global frame. Its mature architecture separates:

1. the local Lorentzian metric and its frame-equivalence class;
2. an observer/worldline or timelike direction;
3. a path, geodesic, ray bundle, loop, or congruence;
4. connection transport along that path;
5. transition functions, gauge equivalence, holonomy, and global quotient gates;
6. field equations plus initial/boundary/matter data; and
7. an operational readout using clocks, light, free fall, or reference variables.

The metric compares norms locally. It does not canonically identify directions at two separated
events. That comparison is path-labelled transport. Curvature appears as holonomy: different paths
can return different frame orientations, while reduced holonomy may preserve a subspace without
selecting a complete frame. A two-point world function becomes canonical only in a suitable
unique-geodesic domain; it is not a general escape from path data. Observer-space approaches can
start from observers, but reconstructing spacetime requires explicit integrability and quotient
conditions.

## The UDT consequence

The strongest justified inference is that the current UDT extension problem may have been ordered
too narrowly. We have repeatedly asked which member of the exact seven-parameter complete-coframe
extension class is *the* physical member. The corpus shows another possibility that must be tested
first:

> The next missing object may be a UDT-derived equivalence, descent, and transport law that says
> which local complete-coframe representatives belong to one relational geometry and how they are
> compared along observer/event paths.

This does **not** mean the seven extension directions are Lorentz gauge. They change the physical
metric in the registered pointwise classification and remain inequivalent metric data unless UDT
itself derives an equivalence relation. Nor does the survey supply a Lorentz/Cartan connection,
world function, geodesic rule, observer mechanics, or dynamics for UDT.

The existing conditional UDT construction

```text
X_q = U_gamma X_p U_gamma^{-1}
A_gamma = U_gamma exp(rho X_p)
```

already has the right composition shape when `X`, `gamma`, `rho`, and `U_gamma` are supplied. The
newly sharpened question is whether the UDT metric derives the base objects, path category,
structure group, transition cocycle, connection, and admissible sections that make this a physical
comparison functor rather than a conditional algebraic one.

## Mechanical census

- 18 frozen primary-source identities inspected and access-graded;
- one append-only bibliographic correction for Synge's 1931 source;
- 15 relational objects classified against 10 dependency types (`150` cells);
- all 10 preregistered hypotheses adjudicated;
- 10 current UDT targets crosswalked without a premise promotion;
- 12 independently keyed source facts; and
- 15 exercised anti-import/typing mutations, all rejected.

The exact dependency map is in `RELATIONAL_ARCHITECTURE_MATRIX.tsv`; results are in
`HYPOTHESIS_OUTCOMES.tsv`; the UDT boundary is in `UDT_CROSSWALK.tsv`.

## What remains unchanged

- founded `phi` identity and reciprocal pair action: `DERIVED`;
- exact seven-parameter pointwise complete-extension class: `DERIVED_CLASSIFICATION`, not selected;
- physical observer/event/path assignment and realized profile: `OPEN`;
- strong local CSN: inactive, challenged/not derived;
- `c_E` and `G_obs`: observed anchors retained;
- `S^2` carrier: `POSIT`;
- bootstrap: `WORKING` on-shell admissibility only;
- `X_max`: `WORKING` global observer-pair schema;
- complete action, source, boundary, unconditional mass, and dynamics: `OPEN`.

No GR field equation, matter model, signal ontology, clock postulate, or connection entered UDT as
affirmative physics.

## Evidence gates

1. **Preregistered:** yes; commit `8fae218`, pushed before the architecture and outcome tables.
2. **Full or bounded:** complete for the frozen 18-source, 15-object architecture census; not an
   exhaustive review of all relativity literature.
3. **Independently checked:** a separate fact table and standard-library verifier reconstructed
   coverage, dependency gates, status preservation, and 15 catch-proofs. No fresh independent model
   context was used, so semantic interpretation retains that explicit caveat.
4. **Premises audited:** yes; all UDT inputs and forbidden imports remain explicit.

Maximum conclusion: a ranked derive-or-fail question about UDT-native bundle/descent/transport
structure. No extension, section, action, carrier, source, boundary, bootstrap equation, `X_max`,
mass, or dynamics is selected.
