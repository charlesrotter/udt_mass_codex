# Killing-plane and two-stratum transition audit — preregistration

Date: 2026-07-28
Base: `b9cf86b878ae8b0d23928d9a855c9d7748e02435`
Mode: CPU-only exact/symbolic geometry; observing, not targeting

## Whole question

The registered stationary full-screen family contains two bounded geometric strata:

1. open configurations where three independent scalar-invariant gradients select a unique
   stationary Killing line and its nonzero twist selects the reciprocal ruler; and
2. configurations whose complete metric descends through the Hopf circle and therefore has a
   two-dimensional Abelian Killing plane spanned by `K` and the compact Hopf generator `V`.

This audit will determine, without assigning either stratum a physical label:

- all basis-independent Gram, causal, twist, orbit-topology, and fixed-point data of the constant
  Killing directions `K+Omega V`, including exceptional parameter strata;
- whether those data select one clock line inside the descended Killing plane or leave a residual
  framing class;
- whether the descended and unique-clock strata are disconnected, continuously adjacent, or joined
  only after leaving the registered family; and
- what exact invariant changes or degenerates at their interface.

The motivating possibility that both strata might later describe macro and micro/mass-emergence
regimes is deliberately **not** an acceptance criterion. The maximum physical statement is only
that the geometry permits or forbids such a later interpretation.

## Frozen bounded regime

The tested family is exactly

```text
theta0=exp(-phi)(c_E dt+alpha sigma3),
theta1=exp(+phi)sigma3,
(theta2,theta3)^T=P(sigma1,sigma2)^T,
g=-theta0^2+theta1^2+theta2^2+theta3^2
```

on the chosen stationary `R x S3` control, with the registered constant Maurer--Cartan coefficient
`kappa`, constant `alpha`, smooth finite stationary `phi`, and smooth invertible `P`. The descended
stratum obeys

```text
V(phi)=0,
V(h)+kappa(hR-Rh)=0,  h=P^T P.
```

All real constant `Omega` and the projective endpoint `V` will be classified. No preferred value of
`Omega` will be inserted.

## Premise ledger

| Input | Status for this audit | Source / limitation |
|---|---|---|
| additive reciprocal `phi` and pair weights | `pinned-by-THEORY`, `DERIVED` | `CURRENT_SCIENTIFIC_PREMISES.tsv` G01--G02 |
| measured `c_E != 0` | `pinned-by-THEORY` as `OBSERVED` calibration | G06; its numerical value is unnecessary |
| `R x S3`, stationary block-screen coframe | `pinned-by-HABIT` only in the sense of a `CHOSE` existence control | no universal-spacetime conclusion allowed |
| `K`, `V`, constant `alpha`, constant `kappa` | `free-and-explored` symbolically, including zero/degenerate strata where meaningful | no physical parameter value selected |
| every smooth invertible general screen `P` satisfying descent | `free-and-explored` at the invariant level | both shears retained; no round-screen filter |
| `Omega` in `K+Omega V` | `free-and-explored` over the full real projective line | no preferred frame inserted |
| Hopf circle lattice/compactness of `V` | `pinned-by-THEORY` inside the chosen `S3` control only | not a derived physical carrier |
| action, equation, source, carrier, density, bootstrap value, boundary law, dynamics | `OPEN` and absent | cannot be inferred by this audit |
| macro/micro interpretation | `OPEN`, postponed | never used to classify a branch |

No strong local CSN premise is active.

## Candidate outcomes fixed before calculation

Exactly one primary classification will be returned:

- `UNIQUE_METRIC_CLOCK_LINE_IN_DESCENDED_PLANE` — a basis-independent metric/global invariant has a
  single admissible line, including all allowed basis changes and exceptional strata;
- `RESIDUAL_GLOBAL_FRAMING_CLASS` — the complete tested metric data preserve two or more admissible
  noncompact clock lines;
- `MIXED_PARAMETER_STRATA` — uniqueness holds only on explicitly characterized subfamilies; or
- `AUDIT_INCOMPLETE_STOP` — the registered data or completeness checks do not support any of the
  above.

The relation between the two geometric strata will be independently classified as
`DISCONNECTED`, `CONTINUOUSLY_ADJACENT`, `JOINED_WITHIN_REGISTERED_FAMILY`, or `OPEN`.

## Falsification and certification contract

The following must be derived and independently reconstructed:

1. the full `2 x 2` Gram matrix on `span(K,V)`, its determinant, signature, and transformation under
   every lattice-compatible change of Killing basis;
2. the norm and causal-class boundaries for every constant `K+Omega V`;
3. the full twist three-form or twist one-form for every such direction, not only `K`;
4. compact/noncompact orbit classes, lattice-preserving algebra automorphisms, and any fixed-point
   data;
5. every proposed selector tested against constant-depth, variable-depth, zero-twist, and causal
   exceptional controls;
6. an explicit smooth family or obstruction establishing the two-stratum relation; and
7. catch-proofs rejecting a hidden choice of `Omega`, a coordinate-basis selector mislabeled as a
   metric invariant, omission of an exceptional stratum, promotion to macro/micro physics, or a
   claim that the old rank-three certificate applies on the descended stratum.

An independent implementation may use exact rational/SymPy algebra but must not import production
functions. A fresh adversarial semantic review is required before banking. The full repository test
suite, current-premise verifier, frozen manifests, current paths, frontier targets, and the unrelated
57-path dirty metadata set must remain unchanged.

## Maximum conclusion

At most this audit may classify the clock-line ambiguity and the geometric adjacency of the two
stationary strata. Even a positive connection does not identify macro versus micro regimes, derive
mass emergence, select a Hopf carrier, or supply dynamics, an action, source, density law, boundary,
or physical universe branch.
